// Server-side meta-tag injection for /workshido-worksheet.html?id=...
//
// Why this exists: the page is a client-rendered SPA — title, meta
// description, canonical, and OG/Twitter tags were only ever set by
// js/workshido-worksheet.js AFTER fetching the worksheet from Supabase.
// Any crawler or scraper that doesn't execute JS (WhatsApp, Pinterest,
// Twitter/X, many SEO tools, and Googlebot's first, non-rendered pass)
// saw the same generic "Workshido" title/description/canonical on all
// ~364 worksheet pages — a textbook duplicate-content signal that
// actively works against indexing individual worksheets.
//
// This function fetches the real worksheet row, then serves the exact
// same static HTML with the real values already baked into the <head>,
// before the client JS ever runs. The client JS still runs afterward and
// re-sets the same tags to the same values — harmless, idempotent, and
// it's what keeps this a one-file change instead of a bigger refactor.
const { createClient } = require('@supabase/supabase-js');

const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
const SITE = 'https://workshido.com';
// The real SPA shell lives at this filename (not workshido-worksheet.html —
// that public URL is now owned by this function via a netlify.toml redirect,
// so fetching it here would recurse into this same function).
const TEMPLATE_URL = `${SITE}/workshido-worksheet-app.html`;

// Cached across warm invocations of the same function container; refetched
// after 5 minutes so a template edit + deploy shows up without a cold start.
let templateCache = { html: null, fetchedAt: 0 };
async function getTemplate() {
  const now = Date.now();
  if (templateCache.html && now - templateCache.fetchedAt < 5 * 60 * 1000) return templateCache.html;
  const res = await fetch(TEMPLATE_URL);
  const html = await res.text();
  templateCache = { html, fetchedAt: now };
  return html;
}

function escapeHtml(s) {
  return String(s).replace(/[<>&'"]/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]));
}
function escapeAttr(s) {
  return String(s).replace(/[&'"]/g, (c) => ({ '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]));
}

exports.handler = async (event) => {
  const id = event.queryStringParameters && event.queryStringParameters.id;

  // No id (or malformed request) — serve the template untouched, same as
  // the static file always did. Never block the page from loading.
  if (!id) {
    const template = await getTemplate();
    return { statusCode: 200, headers: { 'Content-Type': 'text/html; charset=utf-8' }, body: template };
  }

  try {
    const [template, { data, error }] = await Promise.all([
      getTemplate(),
      sb.from('worksheets').select('id, title, level, category, description, thumbnail_url').eq('id', id).single(),
    ]);

    if (error || !data) {
      return { statusCode: 200, headers: { 'Content-Type': 'text/html; charset=utf-8' }, body: template };
    }

    const title = `${data.title} — Workshido`;
    const desc = data.description
      ? data.description.slice(0, 160)
      : `Free ${data.level || ''} ${data.category || 'English'} worksheet — download and print for class.`.replace(/\s+/g, ' ').trim();
    const url = `${SITE}/workshido-worksheet.html?id=${encodeURIComponent(data.id)}`;
    const image = data.thumbnail_url || `${SITE}/og-image.png`;

    let html = template
      .replace('<title>Workshido</title>', `<title>${escapeHtml(title)}</title>`)
      .replace(
        '<link rel="canonical" href="https://workshido.com/workshido-worksheet.html">',
        `<link rel="canonical" href="${escapeAttr(url)}">`
      )
      .replace(
        '<meta name="description" content="Free English worksheet — download and print for class.">',
        `<meta name="description" content="${escapeAttr(desc)}">`
      )
      .replace('<meta property="og:title" content="Workshido">', `<meta property="og:title" content="${escapeAttr(title)}">`)
      .replace(
        '<meta property="og:description" content="Free English worksheet — download and print for class.">',
        `<meta property="og:description" content="${escapeAttr(desc)}">`
      )
      .replace('<meta property="og:image" content="https://workshido.com/og-image.png">', `<meta property="og:image" content="${escapeAttr(image)}">`)
      .replace('<meta property="og:url" content="https://workshido.com/workshido-worksheet.html">', `<meta property="og:url" content="${escapeAttr(url)}">`)
      .replace('<meta name="twitter:title" content="Workshido">', `<meta name="twitter:title" content="${escapeAttr(title)}">`)
      .replace(
        '<meta name="twitter:description" content="Free English worksheet — download and print for class.">',
        `<meta name="twitter:description" content="${escapeAttr(desc)}">`
      )
      .replace('<meta name="twitter:image" content="https://workshido.com/og-image.png">', `<meta name="twitter:image" content="${escapeAttr(image)}">`);

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'public, max-age=300' },
      body: html,
    };
  } catch (err) {
    // Never let a Supabase hiccup take the page down — fall back to the
    // plain template, same as before this function existed.
    const template = await getTemplate();
    return { statusCode: 200, headers: { 'Content-Type': 'text/html; charset=utf-8' }, body: template };
  }
};
