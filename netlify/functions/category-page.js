// Server-side internal-linking injection for the 6 category/level landing
// pages (/worksheets/grammar/, /worksheets/vocabulary/, /worksheets/reading/,
// /worksheets/writing/, /worksheets/levels/a1/, /worksheets/levels/a2/).
//
// Why this exists: these pages render their worksheet cards entirely via
// client-side JS (loadWorksheets() -> Supabase -> innerHTML). The raw HTML
// a non-JS crawler sees has zero <a href> links to individual worksheets —
// only a "Loading worksheets..." placeholder. A sitemap gets pages crawled;
// real anchor links from an already-indexed page are what get pages ranked.
// This function injects a real, plain <ul> of worksheet links into the
// static HTML before the JS-driven grid ever loads, using the same
// self-fetch + string-replace pattern as worksheet-page.js.
const { createClient } = require('@supabase/supabase-js');

const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
const SITE = 'https://workshido.com';

// path -> { templateUrl, filterCol, filterVal, label }
const PAGES = {
  '/worksheets/grammar/':    { template: 'grammar/index-app.html',    col: 'category', val: 'Grammar',    label: 'Grammar' },
  '/worksheets/vocabulary/': { template: 'vocabulary/index-app.html', col: 'category', val: 'Vocabulary', label: 'Vocabulary' },
  '/worksheets/reading/':    { template: 'reading/index-app.html',    col: 'category', val: 'Reading',    label: 'Reading' },
  '/worksheets/writing/':    { template: 'writing/index-app.html',    col: 'category', val: 'Writing',    label: 'Writing' },
  '/worksheets/levels/a1/':  { template: 'levels/a1/index-app.html',  col: 'level',    val: 'A1',         label: 'A1' },
  '/worksheets/levels/a2/':  { template: 'levels/a2/index-app.html',  col: 'level',    val: 'A2',         label: 'A2' },
};

const templateCache = {}; // path -> { html, fetchedAt }
async function getTemplate(templatePath) {
  const now = Date.now();
  const cached = templateCache[templatePath];
  if (cached && now - cached.fetchedAt < 5 * 60 * 1000) return cached.html;
  const res = await fetch(`${SITE}/worksheets/${templatePath}`);
  const html = await res.text();
  templateCache[templatePath] = { html, fetchedAt: now };
  return html;
}

function esc(s) {
  return String(s).replace(/[<>&'"]/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]));
}

exports.handler = async (event) => {
  const page = PAGES[event.path];
  if (!page) return { statusCode: 404, body: 'Not found' };

  try {
    const [template, { data, error }] = await Promise.all([
      getTemplate(page.template),
      sb.from('worksheets').select('id, title, level, category').eq(page.col, page.val).order('created_at', { ascending: false }).limit(60),
    ]);

    if (error || !data || !data.length) {
      return { statusCode: 200, headers: { 'Content-Type': 'text/html; charset=utf-8' }, body: template };
    }

    const links = data
      .map((ws) => `<li><a href="${SITE}/workshido-worksheet.html?id=${esc(ws.id)}">${esc(ws.title)} (${esc(ws.level)})</a></li>`)
      .join('');

    const block = `
<section aria-label="All ${esc(page.label)} worksheets" style="max-width:1100px;margin:0 auto;padding:0 32px 8px;">
  <h2 style="font-family:'Sora',sans-serif;font-size:13px;font-weight:700;color:#5F5E5A;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:10px;">All ${esc(page.label)} worksheets (${data.length})</h2>
  <ul style="columns:3;column-gap:24px;list-style:none;padding:0;margin:0 0 8px;font-size:13px;line-height:1.9;">${links}</ul>
</section>`;

    // ItemList mirrors the injected <ul> above — gives crawlers/AI assistants
    // an explicit "this page is a list of N free worksheets" signal instead
    // of having to infer it from a plain bullet list.
    const itemListLD = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      name: `${page.label} worksheets`,
      numberOfItems: data.length,
      itemListElement: data.map((ws, i) => ({
        '@type': 'ListItem',
        position: i + 1,
        url: `${SITE}/workshido-worksheet.html?id=${ws.id}`,
        name: ws.title,
      })),
    }).replace(/</g, '\\u003c');

    // Inserted right before the JS-driven grid takes over — real crawlable
    // links now exist in the raw HTML regardless of whether JS ever runs.
    const html = template
      .replace('<main class="content">', `${block}\n<main class="content">`)
      .replace('</head>', `<script type="application/ld+json">${itemListLD}</script>\n</head>`);

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'public, max-age=600' },
      body: html,
    };
  } catch (err) {
    const template = await getTemplate(page.template);
    return { statusCode: 200, headers: { 'Content-Type': 'text/html; charset=utf-8' }, body: template };
  }
};
