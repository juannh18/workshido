// Server-side content injection for /workshido-worksheet.html?id=...
//
// Why this exists: the page is a client-rendered SPA — title, meta
// description, canonical, OG/Twitter tags, JSON-LD, and the visible <h1> +
// description were only ever set by js/workshido-worksheet.js AFTER fetching
// the worksheet from Supabase. Any crawler or scraper that doesn't execute
// JS (WhatsApp, Pinterest, Twitter/X, Bing, AI assistants, many SEO tools,
// and Googlebot's first, non-rendered pass) saw the same generic "Workshido"
// title/description on all ~700 worksheet pages, with no body content at all
// — a textbook duplicate-content / thin-page signal that actively works
// against indexing individual worksheets.
//
// This function fetches the real worksheet row, then serves the exact same
// static HTML with the real values already baked into the <head> AND into
// the #pageWrap SSR block, before the client JS ever runs. The client JS
// still runs afterward: it re-sets the same tags to the same values and
// replaces #pageWrap wholesale (its own <h1 class="ws-title"> carries the
// same text) — harmless, idempotent, and it keeps this a two-file change
// instead of a full SSR rewrite.
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
      sb.from('worksheets').select('*').eq('id', id).single(),
    ]);

    if (error || !data) {
      // A real, since-deleted/renamed worksheet id — this is the exact
      // shape of a "soft 404" (200 OK, no real content) that Search Console
      // flags. Serve the shell but say so with the status code, so it's an
      // unambiguous 404 instead of looking like a valid empty page.
      return { statusCode: 404, headers: { 'Content-Type': 'text/html; charset=utf-8' }, body: template };
    }

    // Brand suffix kept on OG/Twitter (social cards) but NOT on <title>: the
    // worksheet titles are already descriptive, and the extra " — Workshido"
    // just pushed them past Google's ~60-char SERP cutoff.
    const title = `${data.title} — Workshido`;
    const pageTitle = data.title;
    const desc = data.description
      ? data.description.slice(0, 160)
      : `Free ${data.level || ''} ${data.category || 'English'} worksheet — download and print for class.`.replace(/\s+/g, ' ').trim();
    const url = `${SITE}/workshido-worksheet.html?id=${encodeURIComponent(data.id)}`;
    const image = data.thumbnail_url || `${SITE}/og-image.png`;
    // Visible body copy for no-JS crawlers — full description when there is
    // one, otherwise the same generated line used for the meta description.
    const bodyDesc = data.description || desc;

    // Mirrors the LearningResource JSON-LD that js/workshido-worksheet.js
    // builds client-side (kept in sync with that block). Stringified with < → <
    // so a title containing "</script>" can't break out of the tag.
    const schemaLD = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'LearningResource',
      name: data.title,
      description: data.description || '',
      educationalLevel: data.level,
      learningResourceType: 'Worksheet',
      inLanguage: 'en',
      isAccessibleForFree: data.is_free !== false,
      image: image,
      provider: { '@type': 'Organization', name: 'Workshido', url: 'https://workshido.com' },
    }).replace(/</g, '\\u003c');

    let html = template
      .replace('<title>Workshido</title>', `<title>${escapeHtml(pageTitle)}</title>`)
      .replace(
        '<h1 class="ws-title" id="ssrTitle">English worksheet</h1>',
        `<h1 class="ws-title" id="ssrTitle">${escapeHtml(data.title)}</h1>`
      )
      .replace(
        '<p class="ws-desc" id="ssrDesc" hidden></p>',
        `<p class="ws-desc" id="ssrDesc">${escapeHtml(bodyDesc)}</p>`
      )
      .replace(
        '<script type="application/ld+json" id="schemaLD"></script>',
        `<script type="application/ld+json" id="schemaLD">${schemaLD}</script>`
      )
      // Inline the full worksheet row so js/workshido-worksheet.js can render
      // immediately instead of waiting on its own round-trip for the same data.
      .replace(
        '<script type="application/json" id="wsData"></script>',
        `<script type="application/json" id="wsData">${JSON.stringify(data).replace(/</g, '\\u003c')}</script>`
      )
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
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'public, max-age=0, must-revalidate',
        // Let Netlify's edge serve the rendered HTML directly (≈50ms) instead
        // of cold-running this function (≈800ms) on every view. Vary is on
        // ?id (Netlify-Vary below). stale-while-revalidate keeps it instant
        // even past the 5-min TTL while a fresh copy is fetched in the
        // background; the client JS re-hydrates live data regardless.
        'Netlify-CDN-Cache-Control': 'public, s-maxage=300, stale-while-revalidate=3600, durable',
        'Netlify-Vary': 'query=id',
      },
      body: html,
    };
  } catch (err) {
    // Never let a Supabase hiccup take the page down — fall back to the
    // plain template, same as before this function existed.
    const template = await getTemplate();
    return { statusCode: 200, headers: { 'Content-Type': 'text/html; charset=utf-8' }, body: template };
  }
};
