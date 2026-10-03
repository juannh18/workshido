// Grammar-topic hubs: /worksheets/topics/ (index) and /worksheets/topics/<slug>/.
//
// Why this exists: a teacher searching "present simple worksheets" lands on a
// level page (all A1 topics mixed) or on a single worksheet. A hub gathers every
// worksheet on one grammar point across all levels, grouped A1 → B2 and, inside
// each level, in set order (Grammar → Reading → Writing → Practice → Speaking),
// with the matching teaching guide on top. Topic list, patterns and copy live in
// netlify/lib/topics.js, shared with worksheet-page.js so the worksheet's
// breadcrumb/hub link and the hub's contents always agree.
//
// Fully server-rendered (no client fetch): the card grid is real HTML for
// crawlers. The page chrome (head CSS, nav, mobile menu, footer) is borrowed at
// runtime from the A1 level template, so it can never drift from the rest of
// the catalog pages.
const { createClient } = require('@supabase/supabase-js');
const { fetchAllRows } = require('../lib/fetch-all');
const { HUBS, hubBySlug, topicFor } = require('../lib/topics');

const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
// Site constants — the only lines that differ in Spanishido's copy of this file.
const SITE = 'https://workshido.com';
const BRAND = 'Workshido';
const CATALOG = '/workshido-index.html';
const LEGACY_WS = '/workshido-worksheet.html';
const SUBJECT = 'English';
const LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1'];
const TYPE_ORDER = ['Grammar', 'Reading', 'Writing', 'Practice', 'Speaking', 'Vocabulary'];
const LEVEL_COLORS = { A1: 'teal', A2: 'blue', B1: 'amber', B2: 'purple', C1: 'coral' };

function originFor(event) {
  const host = (event.headers && (event.headers['x-forwarded-host'] || event.headers.host)) || '';
  return host ? `https://${host}` : SITE;
}

const templateCache = {};
async function getChrome(event) {
  const url = `${originFor(event)}/worksheets/levels/a1/index-app.html`;
  const hit = templateCache[url];
  if (hit && Date.now() - hit.at < 5 * 60 * 1000) return hit.html;
  const html = await (await fetch(url)).text();
  templateCache[url] = { html, at: Date.now() };
  return html;
}

function esc(s) {
  return String(s == null ? '' : s).replace(/[<>&'"]/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]));
}
const ld = (o) => `<script type="application/ld+json">${JSON.stringify(o).replace(/</g, '\\u003c')}</script>`;
const smThumb = (u) => (u && /\.webp(\?|$)/i.test(u) ? u.replace(/\.webp(\?|$)/i, '_sm.webp$1') : u);
const wsHref = (ws) => (ws.slug ? `/worksheet/${ws.slug}/` : `${LEGACY_WS}?id=${ws.id}`);

function card(ws, eager) {
  const lvl = (ws.level || 'A1').toLowerCase();
  const href = esc(wsHref(ws));
  const thumb = ws.thumbnail_url
    ? `<img src="${esc(smThumb(ws.thumbnail_url))}" onerror="this.onerror=null;this.src='${esc(ws.thumbnail_url)}'" alt="${esc(ws.title)} worksheet preview" ${eager ? '' : 'loading="lazy"'} width="440" height="311">`
    : `<div class="ws-preview"><div class="wl"></div><div class="wl"></div><div class="wl short"></div><div class="wb"></div><div class="wb"></div></div><div class="card-thumb-overlay"><span class="overlay-logo">${BRAND}</span><span class="overlay-level ${lvl}">${esc(ws.level)}</span></div>`;
  return `<div class="ws-card">
    <a href="${href}" class="card-thumb ${LEVEL_COLORS[ws.level] || 'teal'}" style="display:block;text-decoration:none;">${thumb}</a>
    <div class="card-body">
      <div class="card-meta"><span class="badge-level ${lvl}">${esc(ws.level)}</span><span class="badge-type free">${esc(ws.category || 'Worksheet')}</span></div>
      <a href="${href}" class="card-title" style="text-decoration:none;color:inherit;">${esc(ws.title)}</a>
      <div class="card-footer"><span></span><a href="${href}" class="btn-download" style="text-decoration:none;">↓ Download</a></div>
    </div>
  </div>`;
}

const HUB_CSS = `<style>
  .topic-jump { display:flex; flex-wrap:wrap; gap:8px; margin: 0 0 20px; }
  .topic-jump a { font-size:13px; font-weight:600; padding:6px 12px; border-radius:999px; background:var(--gray-50); color:var(--gray-900); text-decoration:none; border:1px solid var(--gray-100); }
  .topic-jump a:hover { border-color: var(--blue-600); }
  .topic-guide { background:var(--blue-50); border:1px solid var(--blue-100); border-radius:12px; padding:14px 18px; font-size:14px; line-height:1.6; margin: 0 0 28px; color:var(--gray-900); }
  .topic-guide a { color:var(--blue-600); font-weight:600; }
  .topic-level { margin: 0 0 36px; scroll-margin-top: 80px; }
  .topic-level h2 { font-family: var(--font-display, 'Sora', sans-serif); font-size: 20px; margin: 0 0 14px; color: var(--gray-900); }
  .topic-level h2 span { font-weight: 500; color: var(--gray-300); font-size: 15px; }
  .hub-list { display:grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap:16px; }
  .hub-item { display:block; padding:18px 20px; border:1px solid var(--gray-100); border-radius:14px; text-decoration:none; color:inherit; background:#fff; }
  .hub-item:hover { border-color: var(--blue-600); }
  .hub-item strong { display:block; font-family: var(--font-display, 'Sora', sans-serif); font-size:16px; margin-bottom:4px; color: var(--gray-900); }
  .hub-item span { font-size:13px; color: var(--gray-600); }
</style>`;

// Swap the level page's content for ours; everything else (CSS, nav, footer)
// stays. Each replace targets a block the level templates all share — if one
// ever stops matching, the page still renders, just with that block missing.
function fill(chrome, p) {
  return chrome
    .replace(/<title>[\s\S]*?<\/title>/, `<title>${esc(p.title)}</title>`)
    .replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${esc(p.desc)}">`)
    .replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="${esc(p.url)}">`)
    .replace(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${esc(p.title)}">`)
    .replace(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${esc(p.desc)}">`)
    .replace(/<meta property="og:url" content="[^"]*">/, `<meta property="og:url" content="${esc(p.url)}">`)
    .replace(/<meta name="twitter:title" content="[^"]*">/, `<meta name="twitter:title" content="${esc(p.title)}">`)
    .replace(/<meta name="twitter:description" content="[^"]*">/, `<meta name="twitter:description" content="${esc(p.desc)}">`)
    .replace(/(<script type="application\/ld\+json">[\s\S]*?<\/script>\s*)+/, `${p.jsonld}\n`)
    .replace('</head>', `${HUB_CSS}\n</head>`)
    .replace(/<div class="breadcrumb"[\s\S]*?<\/div>/, `<div class="breadcrumb" role="navigation" aria-label="Breadcrumb">${p.crumbs}</div>`)
    .replace(/<section class="hero hero-lite">[\s\S]*?<\/section>/, `<section class="hero hero-lite">
  <div class="hero-eyebrow" style="margin-left:auto;margin-right:auto;"><span class="dot"></span><span>Free · Print-ready PDFs · Grouped by level</span></div>
  <h1 style="max-width:760px;margin-left:auto;margin-right:auto;">${esc(p.h1)}</h1>
  <div class="intro"><p>${p.intro}</p></div>
</section>`)
    .replace(/<main class="content">[\s\S]*?<\/main>/, `<main class="content">${p.body}</main>`)
    .replace(/<section class="related-section">[\s\S]*?<\/section>/, `<section class="related-section"><h2>Explore more</h2><div class="related-links">${p.related}</div></section>`)
    // The level page's own script fetches and renders A1 cards into #cardGrid,
    // which no longer exists here — keep only the footer year + mobile menu.
    .replace(/<script>\s*const sb2 = [\s\S]*?<\/script>/, `<script>
document.getElementById('yr').textContent = new Date().getFullYear();
function openMobileMenu()  { document.getElementById('mobileMenu').classList.add('open'); document.body.style.overflow = 'hidden'; }
function closeMobileMenu() { document.getElementById('mobileMenu').classList.remove('open'); document.body.style.overflow = ''; }
</script>`);
}

const levelRange = (levels) => (levels.length > 1 ? `${levels[0]}–${levels[levels.length - 1]}` : levels[0] || '');

function hubPage(topic, rows) {
  const h = topic.hub;
  const url = `${SITE}/worksheets/topics/${h.slug}/`;
  const byLevel = LEVELS.map((lv) => ({
    lv,
    items: rows.filter((w) => w.level === lv).sort((a, b) =>
      (TYPE_ORDER.indexOf(a.category) + 99) % 99 - (TYPE_ORDER.indexOf(b.category) + 99) % 99 || a.title.localeCompare(b.title)),
  })).filter((g) => g.items.length);

  let n = 0;
  const sections = byLevel.map((g) => `<section class="topic-level" id="${g.lv.toLowerCase()}">
  <h2>${g.lv} ${esc(h.name)} worksheets <span>(${g.items.length})</span></h2>
  <div class="card-grid">${g.items.map((w) => card(w, n++ < 4)).join('')}</div>
</section>`).join('');

  const body = `
  <div class="topic-jump" role="navigation" aria-label="Jump to level">${byLevel.map((g) => `<a href="#${g.lv.toLowerCase()}">${g.lv} · ${g.items.length}</a>`).join('')}</div>
  ${topic.guide ? `<p class="topic-guide">📘 Planning the lesson? Read <a href="/guides/${topic.guide.slug}/">${esc(topic.guide.label)}</a> — stages, common mistakes and activity ideas, with the worksheets to use at each step.</p>` : ''}
  ${sections}`;

  const others = HUBS.filter((t) => t !== topic)
    .map((t) => `<a href="/worksheets/topics/${t.hub.slug}/" class="related-link">${esc(t.hub.name)}</a>`).join('');
  const levelLinks = byLevel.map((g) => `<a href="/worksheets/levels/${g.lv.toLowerCase()}/" class="related-link">All ${g.lv} worksheets</a>`).join('');

  const crumbs = [
    { name: 'Home', url: `${SITE}/` },
    { name: 'Topics', url: `${SITE}/worksheets/topics/` },
    { name: h.name, url },
  ];
  const jsonld = ld({
    '@context': 'https://schema.org', '@type': 'CollectionPage', name: `${h.name} Worksheets`, description: h.desc, url,
    isPartOf: { '@type': 'WebSite', name: BRAND, url: `${SITE}/` },
    mainEntity: {
      '@type': 'ItemList', numberOfItems: rows.length,
      itemListElement: byLevel.flatMap((g) => g.items).slice(0, 60).map((w, i) => ({ '@type': 'ListItem', position: i + 1, url: `${SITE}${wsHref(w)}`, name: w.title })),
    },
  }) + '\n' + ld({
    '@context': 'https://schema.org', '@type': 'BreadcrumbList',
    itemListElement: crumbs.map((c, i) => ({ '@type': 'ListItem', position: i + 1, name: c.name, item: c.url })),
  });

  // Level range computed from the rows, so <title> and <h1> never claim a
  // level the hub doesn't have (or miss one added later).
  const range = levelRange(byLevel.map((g) => g.lv));
  const long = `${h.name} Worksheets (${range}) – Free PDFs | ${BRAND}`;
  return {
    title: long.length <= 60 ? long : `${h.name} Worksheets (${range}) | ${BRAND}`, desc: h.desc, url, jsonld,
    // U+2060 word joiners keep "(A1–A2)" from wrapping mid-range in the hero.
    h1: `${h.name} Worksheets (${range.replace('–', '\u2060–\u2060')})`,
    intro: h.intro,
    crumbs: crumbsHtml(crumbs),
    body, related: others + levelLinks,
  };
}

function indexPage(counts) {
  const url = `${SITE}/worksheets/topics/`;
  const items = HUBS.map((t) => {
    const c = counts[t.hub.slug] || { n: 0, levels: [] };
    return `<a class="hub-item" href="/worksheets/topics/${t.hub.slug}/"><strong>${esc(t.hub.name)}</strong><span>${c.n} worksheets · ${levelRange(c.levels)}</span></a>`;
  }).join('');
  const crumbs = [{ name: 'Home', url: `${SITE}/` }, { name: 'Topics', url }];
  const desc = `Free ${SUBJECT} grammar worksheets grouped by topic: ${HUBS.map((t) => t.hub.name.toLowerCase()).slice(0, 6).join(', ')} and more.`;
  return {
    title: `${SUBJECT} Grammar Worksheets by Topic | ${BRAND}`, desc, url,
    jsonld: ld({ '@context': 'https://schema.org', '@type': 'CollectionPage', name: 'Grammar Worksheets by Topic', description: desc, url, isPartOf: { '@type': 'WebSite', name: BRAND, url: `${SITE}/` } })
      + '\n' + ld({ '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: crumbs.map((c, i) => ({ '@type': 'ListItem', position: i + 1, name: c.name, item: c.url })) }),
    h1: 'Grammar Worksheets by Topic',
    intro: 'Every worksheet on one grammar point, from its first introduction to its review at higher levels. Each topic page groups the grammar, reading, writing, practice and speaking sheets by CEFR level and links the teaching guide for that point.',
    crumbs: crumbsHtml(crumbs),
    body: `<div class="hub-list">${items}</div>`,
    related: [...new Set(Object.values(counts).flatMap((c) => c.levels))].sort((a, b) => LEVELS.indexOf(a) - LEVELS.indexOf(b)).map((x) => x.toLowerCase()).map((l) => `<a href="/worksheets/levels/${l}/" class="related-link">${l.toUpperCase()} worksheets</a>`).join('')
      + `<a href="/guides/" class="related-link">Teaching guides</a><a href="${CATALOG}" class="related-link">Full catalog →</a>`,
  };
}

function crumbsHtml(crumbs) {
  return crumbs.map((c, i) => (i === crumbs.length - 1
    ? `<span aria-current="page">${esc(c.name)}</span>`
    : `<a href="${esc(c.url.replace(SITE, ''))}">${esc(c.name)}</a>`)).join('<span>›</span>');
}

exports.handler = async (event) => {
  const path = event.path || '';
  const m = path.match(/^\/worksheets\/topics\/(?:([a-z0-9-]+)\/?)?$/);
  const slug = m && m[1];
  const topic = slug ? hubBySlug(slug) : null;
  if (!m || (slug && !topic)) {
    return { statusCode: 404, headers: { 'Content-Type': 'text/html; charset=utf-8' }, body: '<h1>Not found</h1><p><a href="/worksheets/topics/">All topics</a></p>' };
  }
  if (!path.endsWith('/')) {
    return { statusCode: 301, headers: { Location: `${path}/` }, body: '' };
  }

  try {
    const [chrome, { data, error }] = await Promise.all([
      getChrome(event),
      fetchAllRows(() => sb.from('worksheets').select('id,slug,title,level,category,thumbnail_url,topic_key').order('created_at', { ascending: false }).order('id')),
    ]);
    if (error || !data) throw error || new Error('no data');

    let page;
    if (topic) {
      page = hubPage(topic, data.filter((w) => topicFor(w) === topic));
    } else {
      const counts = {};
      for (const w of data) {
        const t = topicFor(w);
        if (!t || !t.hub) continue;
        const c = (counts[t.hub.slug] = counts[t.hub.slug] || { n: 0, levels: [] });
        c.n++;
        if (!c.levels.includes(w.level)) c.levels.push(w.level);
      }
      for (const c of Object.values(counts)) c.levels.sort((a, b) => LEVELS.indexOf(a) - LEVELS.indexOf(b));
      page = indexPage(counts);
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'public, max-age=0, must-revalidate',
        'Netlify-CDN-Cache-Control': 'public, s-maxage=600, stale-while-revalidate=86400, durable',
      },
      body: fill(chrome, page),
    };
  } catch (err) {
    return { statusCode: 503, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Retry-After': '60' }, body: `<h1>Temporarily unavailable</h1><p><a href="${CATALOG}">Browse all worksheets</a></p>` };
  }
};
