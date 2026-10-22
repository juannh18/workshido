// Public teacher profiles: /teacher/<public_slug>/.
//
// Why this exists: a teacher's profile (name, avatar, what they teach, bio and
// the worksheets they saved) was only visible to themselves. Opting in
// (profiles.is_public, set by the set_profile_public RPC from the private
// profile page) publishes it here — a shareable page that brings new teachers
// in, and a real, crawlable page of internal links to the worksheets they use.
//
// Fully server-rendered, same approach as topic-page.js: the page chrome (head
// CSS, nav, mobile menu, footer) is borrowed at runtime from the A1 level
// template, so it never drifts from the catalog pages.
//
// Thin profiles (no bio/teaches, or fewer than INDEX_MIN_FAVS saved
// worksheets) render for visitors but carry noindex — a name and an empty grid
// is not a page Google should index. sitemap.js lists only the indexable ones
// (same rule, netlify/lib/teacher-rules.js).
const { createClient } = require('@supabase/supabase-js');
const { isIndexable, INDEX_MIN_FAVS } = require('../lib/teacher-rules');

const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
// Site constants — the only lines that differ in Spanishido's copy of this file.
const SITE = 'https://workshido.com';
const BRAND = 'Workshido';
const CATALOG = '/workshido-index.html';
const SIGNUP = '/workshido-signup.html';
const PROFILE = '/workshido-profile.html';
const LEGACY_WS = '/workshido-worksheet.html';
const SUBJECT = 'English';
const INSTAGRAM = 'workshido';
const AV_COLORS = { blue: '#DCEBFB', teal: '#D3F0E6', amber: '#FBEAD0', pink: '#FBDDEC', purple: '#E7E5FB', coral: '#FADDD2', green: '#E4F1D3', slate: '#E6EBF1' };

const LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1'];
const LEVEL_COLORS = { A1: 'teal', A2: 'blue', B1: 'amber', B2: 'purple', C1: 'coral' };
const MAX_FAVS = 48;
// Everyone who joined before 2027 gets the "Founding member" badge.
const FOUNDING_BEFORE = '2027-01-01';

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
function trimDesc(s, max = 160) {
  s = String(s).replace(/\s+/g, ' ').trim();
  if (s.length <= max) return s;
  const cut = s.slice(0, max);
  const word = cut.lastIndexOf(' ');
  return cut.slice(0, word > 0 ? word : max - 1).replace(/[,;:—–-]+$/, '').trim() + '…';
}
const initials = (s) => (s || '').split(/\s+/).filter(Boolean).map((n) => n[0]).join('').toUpperCase().slice(0, 2) || '?';

// Same storage format the private profile writes (js/*-profile.js):
// "dicebear:<query>" character, "<emoji>|<colourkey>" icon, or nothing.
// The Google photo is deliberately NOT used here — it was never chosen for a
// public page.
function avatarHtml(p) {
  const a = p.avatar || '';
  if (a.indexOf('dicebear:') === 0 && /^dicebear:[A-Za-z0-9=&,_%.\-]+$/.test(a)) {
    return `<div class="tp-avatar"><img src="https://api.dicebear.com/9.x/avataaars/svg?${esc(a.slice(9))}" alt="${esc(p.display_name)}" width="120" height="120"></div>`;
  }
  const i = a.lastIndexOf('|');
  if (i > 0 && AV_COLORS[a.slice(i + 1)]) {
    return `<div class="tp-avatar tp-emoji" style="background:${AV_COLORS[a.slice(i + 1)]}">${esc(a.slice(0, i))}</div>`;
  }
  return `<div class="tp-avatar">${esc(initials(p.display_name))}</div>`;
}

function card(ws, eager) {
  const lvl = (ws.level || 'A1').toLowerCase();
  const href = esc(wsHref(ws));
  const thumb = ws.thumbnail_url
    ? `<img src="${esc(smThumb(ws.thumbnail_url))}" onerror="this.onerror=null;this.src='${esc(ws.thumbnail_url)}'" alt="${esc(ws.title)} worksheet preview" ${eager ? '' : 'loading="lazy"'} width="440" height="311">`
    : `<div class="ws-preview"><div class="wl"></div><div class="wl"></div><div class="wl short"></div><div class="wb"></div><div class="wb"></div></div>`;
  return `<div class="ws-card">
    <a href="${href}" class="card-thumb ${LEVEL_COLORS[ws.level] || 'teal'}" style="display:block;text-decoration:none;">${thumb}</a>
    <div class="card-body">
      <div class="card-meta"><span class="badge-level ${lvl}">${esc(ws.level)}</span><span class="badge-type free">${esc(ws.category || 'Worksheet')}</span></div>
      <a href="${href}" class="card-title" style="text-decoration:none;color:inherit;">${esc(ws.title)}</a>
      <div class="card-footer"><span></span><a href="${href}" class="btn-download" style="text-decoration:none;">↓ Download</a></div>
    </div>
  </div>`;
}

const TP_CSS = `<style>
  .tp-hero { background: var(--white); border-bottom: 1px solid var(--gray-100); }
  .tp-cover { height: 140px; background:
      radial-gradient(circle at 1px 1px, rgba(255,255,255,.16) 1px, transparent 0) 0 0 / 18px 18px,
      linear-gradient(120deg, var(--blue-900) 0%, var(--blue-600) 62%, var(--blue-400) 100%); }
  .tp-inner { max-width: 1100px; margin: 0 auto; padding: 16px 32px 28px; display: flex; gap: 24px; align-items: flex-start; flex-wrap: wrap; }
  .tp-avatar { width: 128px; height: 128px; margin-top: -72px; border-radius: 50%; border: 5px solid var(--white); box-shadow: 0 6px 20px rgba(0,0,0,.12); background: var(--blue-50); color: var(--blue-600); display: flex; align-items: center; justify-content: center; font-family: var(--font-display); font-size: 40px; font-weight: 700; overflow: hidden; flex-shrink: 0; }
  .tp-avatar img { width: 100%; height: 100%; display: block; }
  .tp-avatar.tp-emoji { font-size: 60px; }
  .tp-id { flex: 1 1 320px; min-width: 0; }
  .tp-eyebrow { font-size: 12px; font-weight: 700; color: var(--blue-600); text-transform: uppercase; letter-spacing: .6px; margin-bottom: 4px; }
  .tp-id h1 { font-family: var(--font-display); font-size: 30px; line-height: 1.2; color: var(--gray-900); margin: 0; overflow-wrap: anywhere; }
  .tp-teaches { font-size: 15px; font-weight: 600; color: var(--gray-900); margin-top: 6px; }
  .tp-bio { font-size: 15px; color: var(--gray-600); line-height: 1.6; margin-top: 8px; max-width: 640px; }
  .tp-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
  .tp-chip { font-size: 12px; font-weight: 600; color: var(--gray-600); background: var(--gray-50); border: 1px solid var(--gray-100); border-radius: 20px; padding: 5px 12px; }
  .tp-chip.badge { background: var(--amber-50, #FAEEDA); color: var(--amber-600, #854F0B); border-color: transparent; }
  .tp-actions { display: flex; gap: 10px; padding-top: 6px; }
  .tp-btn { font-family: var(--font-body); font-size: 13px; font-weight: 700; border-radius: 8px; padding: 10px 18px; cursor: pointer; border: 1.5px solid var(--gray-100); background: var(--white); color: var(--gray-900); text-decoration: none; display: inline-flex; align-items: center; gap: 6px; white-space: nowrap; }
  .tp-btn:hover { border-color: var(--blue-200); color: var(--blue-600); }
  .tp-btn.primary { background: var(--blue-600); border-color: var(--blue-600); color: var(--white); }
  .tp-btn.primary:hover { background: var(--blue-800); color: var(--white); }
  .tp-section-title { font-family: var(--font-display); font-size: 20px; color: var(--gray-900); margin: 0 0 4px; }
  .tp-section-sub { font-size: 13.5px; color: var(--gray-600); margin: 0 0 18px; }
  .tp-empty { text-align: center; padding: 40px 20px; border: 1.5px dashed var(--gray-100); border-radius: 14px; color: var(--gray-600); font-size: 14px; }
  .tp-cta { margin: 36px 0 8px; border-radius: 18px; padding: 28px; background: linear-gradient(120deg, var(--blue-900), var(--blue-600)); color: var(--white); display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap; }
  .tp-cta h2 { font-family: var(--font-display); font-size: 20px; margin: 0 0 6px; color: var(--white); }
  .tp-cta p { font-size: 14px; color: var(--blue-100); margin: 0; max-width: 520px; line-height: 1.5; }
  .tp-cta .tp-btn { background: var(--white); color: var(--blue-800); border-color: var(--white); }
  .tp-follow { text-align: center; font-size: 13.5px; color: var(--gray-600); margin: 14px 0 0; }
  .tp-follow a { color: var(--blue-600); font-weight: 700; }
  .tp-owner { background: var(--amber-50, #FAEEDA); border-bottom: 1px solid rgba(0,0,0,.06); }
  .tp-owner-in { max-width: 1100px; margin: 0 auto; padding: 10px 32px; display: flex; align-items: center; justify-content: space-between; gap: 14px; flex-wrap: wrap; font-size: 13.5px; color: var(--gray-900); }
  .tp-owner .tp-btn { padding: 7px 14px; }
  @media (max-width: 640px) { .tp-owner-in { padding: 10px 16px; } }
  @media (max-width: 640px) {
    .tp-cover { height: 100px; }
    .tp-inner { padding: 12px 16px 22px; gap: 12px; }
    .tp-avatar { width: 100px; height: 100px; margin-top: -60px; font-size: 32px; }
    .tp-id h1 { font-size: 24px; }
    .tp-actions { width: 100%; }
    .tp-actions .tp-btn { flex: 1; justify-content: center; }
    .tp-cta { padding: 22px 18px; }
  }
</style>`;

function fill(chrome, p) {
  return chrome
    .replace(/<title>[\s\S]*?<\/title>/, `<title>${esc(p.title)}</title>`)
    .replace(/<meta name="description" content="[^"]*">/, `<meta name="description" content="${esc(p.desc)}">${p.noindex ? '\n<meta name="robots" content="noindex, follow">' : ''}`)
    .replace(/<link rel="canonical" href="[^"]*">/, `<link rel="canonical" href="${esc(p.url)}">`)
    .replace(/<meta property="og:type" content="[^"]*">/, '<meta property="og:type" content="profile">')
    .replace(/<meta property="og:title" content="[^"]*">/, `<meta property="og:title" content="${esc(p.title)}">`)
    .replace(/<meta property="og:description" content="[^"]*">/, `<meta property="og:description" content="${esc(p.desc)}">`)
    .replace(/<meta property="og:url" content="[^"]*">/, `<meta property="og:url" content="${esc(p.url)}">`)
    .replace(/<meta name="twitter:title" content="[^"]*">/, `<meta name="twitter:title" content="${esc(p.title)}">`)
    .replace(/<meta name="twitter:description" content="[^"]*">/, `<meta name="twitter:description" content="${esc(p.desc)}">`)
    .replace(/(<script type="application\/ld\+json">[\s\S]*?<\/script>\s*)+/, `${p.jsonld}\n`)
    .replace('</head>', `${TP_CSS}\n</head>`)
    .replace(/<div class="breadcrumb"[\s\S]*?<\/div>/, `<div class="breadcrumb" role="navigation" aria-label="Breadcrumb">${p.crumbs}</div>`)
    .replace(/<section class="hero hero-lite">[\s\S]*?<\/section>/, p.hero)
    .replace(/<main class="content">[\s\S]*?<\/main>/, `<main class="content">${p.body}</main>`)
    .replace(/<section class="related-section">[\s\S]*?<\/section>/, `<section class="related-section"><h2>Explore more</h2><div class="related-links">${p.related}</div></section>`)
    .replace(/<script>\s*const sb2 = [\s\S]*?<\/script>/, `<script>
document.getElementById('yr').textContent = new Date().getFullYear();
function openMobileMenu()  { document.getElementById('mobileMenu').classList.add('open'); document.body.style.overflow = 'hidden'; }
function closeMobileMenu() { document.getElementById('mobileMenu').classList.remove('open'); document.body.style.overflow = ''; }
async function shareProfile(btn) {
  var url = location.origin + location.pathname, title = document.title;
  try { if (navigator.share) { await navigator.share({ title: title, url: url }); return; } } catch (e) { return; }
  try { await navigator.clipboard.writeText(url); btn.textContent = '✓ Link copied'; setTimeout(function () { btn.textContent = '🔗 Share profile'; }, 2000); } catch (e) { prompt('Copy this link:', url); }
}
// Owner-only bar: the page is CDN-cached and identical for everyone, so the
// "is this mine?" check runs here, against the visitor's own profiles row
// (RLS: own row only), via the nav's sbGuides client (js/guides-auth.js).
document.addEventListener('DOMContentLoaded', async function () {
  var bar = document.getElementById('tpOwner');
  if (!bar || typeof sbGuides === 'undefined') return;
  try {
    var u = (await sbGuides.auth.getUser()).data.user;
    if (!u) return;
    var row = (await sbGuides.from('profiles').select('public_slug').eq('id', u.id).maybeSingle()).data;
    if (!row || location.pathname.indexOf('/teacher/' + row.public_slug + '/') !== 0) return;
    bar.querySelector('.tp-owner-tip').textContent = bar.getAttribute('data-tip');
    bar.hidden = false;
  } catch (e) {}
});
</script>`);
}

// A profile that was made private (or a mistyped link) still gets the site's
// nav, footer and a way back into the catalog — not a dead-end blank page.
const RELATED_BASE = `<a href="/worksheets/topics/" class="related-link">Grammar by topic</a><a href="/guides/" class="related-link">Teaching guides</a><a href="${CATALOG}" class="related-link">Full catalog →</a>`;
async function notFound(event) {
  const headers = { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'public, max-age=0, must-revalidate', 'Netlify-CDN-Cache-Control': 'public, s-maxage=60' };
  const plain = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Profile not found | ${BRAND}</title></head>`
    + `<body style="font-family:system-ui,sans-serif;text-align:center;padding:80px 20px;color:#2C2C2A"><h1>This profile isn't public</h1>`
    + `<p>The teacher may have made it private, or the link has changed.</p><p><a href="${CATALOG}">Browse ${SUBJECT} worksheets →</a></p></body></html>`;
  try {
    const chrome = await getChrome(event);
    const body = fill(chrome, {
      title: `Profile not found | ${BRAND}`,
      desc: `This ${BRAND} teacher profile is private or no longer exists.`,
      url: `${SITE}/`, noindex: true, jsonld: '',
      crumbs: `<a href="/">Home</a><span>›</span><span aria-current="page">Profile not found</span>`,
      hero: `<section class="hero hero-lite"><h1 style="max-width:720px;margin-left:auto;margin-right:auto;">This profile isn’t public</h1>
  <div class="intro"><p>The teacher may have made it private, or the link has changed. Meanwhile, every worksheet on ${BRAND} is free to browse.</p>
  <a href="${CATALOG}" class="browse-all">Browse ${SUBJECT} worksheets →</a></div></section>`,
      body: `<div class="tp-cta"><div><h2>Teach ${SUBJECT}?</h2><p>Create your free ${BRAND} profile, save the worksheets you love and share your own shortlist with other teachers.</p></div><a href="${SIGNUP}" class="tp-btn">Create my free profile →</a></div>`,
      related: RELATED_BASE,
    });
    return { statusCode: 404, headers, body };
  } catch (e) {
    return { statusCode: 404, headers, body: plain };
  }
}

function page(p, favs) {
  const name = p.display_name.trim();
  const url = `${SITE}/teacher/${p.public_slug}/`;
  const since = p.created_at ? new Date(p.created_at) : null;
  const byLevel = {};
  favs.forEach((w) => { byLevel[w.level] = (byLevel[w.level] || 0) + 1; });
  const levels = LEVELS.filter((l) => byLevel[l]);
  const topLevel = Object.entries(byLevel).sort((a, b) => b[1] - a[1])[0]?.[0];

  const chips = [];
  if (since && p.created_at < FOUNDING_BEFORE) chips.push('<span class="tp-chip badge">🌱 Founding member</span>');
  if (favs.length >= 10) chips.push('<span class="tp-chip badge">📚 Curator</span>');
  if (since) chips.push(`<span class="tp-chip">📅 Member since ${since.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}</span>`);
  if (favs.length) chips.push(`<span class="tp-chip">♥ ${favs.length} favourite worksheet${favs.length === 1 ? '' : 's'}</span>`);
  if (topLevel) chips.push(`<span class="tp-chip">🎯 Mostly ${esc(topLevel)}</span>`);

  // What the owner still needs for the page to be indexed (same rule as
  // isIndexable) — shown only to them, by the script in fill().
  const missing = [];
  if (!(p.bio || p.teaches)) missing.push('add a bio or what you teach');
  const need = INDEX_MIN_FAVS - favs.length;
  if (need > 0) missing.push(`save ${need} more worksheet${need === 1 ? '' : 's'}`);
  const ownerTip = missing.length ? `To appear on Google, ${missing.join(' and ')}.` : 'Your page is ready to appear on Google ✓';

  const hero = `<div class="tp-owner" id="tpOwner" hidden data-tip="${esc(ownerTip)}">
  <div class="tp-owner-in"><span>👋 <strong>This is your public profile.</strong> <span class="tp-owner-tip"></span></span><a href="${PROFILE}#edit" class="tp-btn">Edit profile</a></div>
</div>
<section class="tp-hero">
  <div class="tp-cover"></div>
  <div class="tp-inner">
    ${avatarHtml(p)}
    <div class="tp-id">
      <div class="tp-eyebrow">${SUBJECT} teacher on ${BRAND}</div>
      <h1>${esc(name)}</h1>
      ${p.teaches ? `<p class="tp-teaches">Teaches ${esc(p.teaches)}</p>` : ''}
      ${p.bio ? `<p class="tp-bio">${esc(p.bio)}</p>` : ''}
      <div class="tp-chips">${chips.join('')}</div>
    </div>
    <div class="tp-actions">
      <button class="tp-btn primary" type="button" onclick="shareProfile(this)">🔗 Share profile</button>
    </div>
  </div>
</section>`;

  const first = esc(name.split(/\s+/)[0]);
  const grid = favs.length
    ? `<div class="card-grid">${favs.map((w, i) => card(w, i < 4)).join('')}</div>`
    : `<div class="tp-empty">${first} hasn't picked any favourite worksheets yet.<br><br><a href="${CATALOG}" class="tp-btn">Browse the catalog</a></div>`;
  const body = `
  <h2 class="tp-section-title">${first}'s favourite worksheets</h2>
  <p class="tp-section-sub">The ${SUBJECT} worksheets ${first} saves for class${levels.length ? ` — ${levels.join(', ')}` : ''}. Free, print-ready PDFs.</p>
  ${grid}
  <div class="tp-cta">
    <div><h2>Teach ${SUBJECT} too?</h2><p>Create your free ${BRAND} profile, save the worksheets you love and share your own shortlist with other teachers.</p></div>
    <a href="${SIGNUP}" class="tp-btn">Create my free profile →</a>
  </div>
  <p class="tp-follow">📸 New worksheets and class ideas every week on Instagram: <a href="https://www.instagram.com/${INSTAGRAM}/" target="_blank" rel="noopener">@${INSTAGRAM}</a></p>`;

  const desc = trimDesc(p.bio
    ? `${name}: ${p.bio}`
    : `${name}${p.teaches ? ` teaches ${p.teaches}` : ` is a ${SUBJECT} teacher`}. See the free ${SUBJECT} worksheets ${first} uses and recommends on ${BRAND}.`);
  const crumbs = [{ name: 'Home', url: `${SITE}/` }, { name, url }];
  const jsonld = ld({
    '@context': 'https://schema.org', '@type': 'ProfilePage', url, name: `${name} — ${SUBJECT} teacher`,
    dateCreated: p.created_at || undefined,
    isPartOf: { '@type': 'WebSite', name: BRAND, url: `${SITE}/` },
    mainEntity: {
      '@type': 'Person', name, url,
      description: p.bio || undefined,
      jobTitle: `${SUBJECT} teacher`,
      knowsAbout: p.teaches || undefined,
    },
    hasPart: favs.length ? {
      '@type': 'ItemList', name: `${name}'s favourite worksheets`, numberOfItems: favs.length,
      itemListElement: favs.slice(0, 30).map((w, i) => ({ '@type': 'ListItem', position: i + 1, url: `${SITE}${wsHref(w)}`, name: w.title })),
    } : undefined,
  }) + '\n' + ld({
    '@context': 'https://schema.org', '@type': 'BreadcrumbList',
    itemListElement: [{ name: 'Home', item: `${SITE}/` }, { name, item: url }].map((c, i) => ({ '@type': 'ListItem', position: i + 1, ...c })),
  });

  const title = `${name} — ${SUBJECT} Teacher | ${BRAND}`;
  return {
    title, desc, url, jsonld, hero, body,
    noindex: !isIndexable(p, favs.length),
    crumbs: crumbs.map((c, i) => (i === crumbs.length - 1
      ? `<span aria-current="page">${esc(c.name)}</span>`
      : c.url ? `<a href="${esc(c.url.replace(SITE, '') || '/')}">${esc(c.name)}</a>` : `<span>${esc(c.name)}</span>`)).join('<span>›</span>'),
    related: levels.map((l) => `<a href="/worksheets/levels/${l.toLowerCase()}/" class="related-link">${l} worksheets</a>`).join('')
      + RELATED_BASE,
  };
}

exports.handler = async (event) => {
  const path = event.path || '';
  const m = path.match(/^\/teacher\/([a-z0-9-]{1,48})\/?$/);
  if (!m) return notFound(event);
  if (!path.endsWith('/')) return { statusCode: 301, headers: { Location: `${path}/` }, body: '' };

  try {
    const { data: p, error } = await sb.from('profiles')
      .select('id, display_name, avatar, bio, teaches, created_at, public_slug, is_public')
      .eq('public_slug', m[1]).maybeSingle();
    if (error) throw error;
    if (!p || !p.is_public || !(p.display_name || '').trim()) return notFound(event);

    const [chrome, saved] = await Promise.all([
      getChrome(event),
      sb.from('saved_worksheets').select('worksheet_id').eq('user_id', p.id).order('created_at', { ascending: false }).limit(MAX_FAVS),
    ]);
    const ids = (saved.data || []).map((s) => s.worksheet_id);
    let favs = [];
    if (ids.length) {
      const { data: ws } = await sb.from('worksheets').select('id,slug,title,level,category,thumbnail_url').in('id', ids);
      const byId = {};
      (ws || []).forEach((w) => { byId[w.id] = w; });
      favs = ids.map((id) => byId[id]).filter(Boolean);
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'public, max-age=0, must-revalidate',
        // Short CDN cache: turning a profile private must take effect quickly.
        'Netlify-CDN-Cache-Control': 'public, s-maxage=60, stale-while-revalidate=120',
      },
      body: fill(chrome, page(p, favs)),
    };
  } catch (err) {
    console.error('teacher-page failed', err);
    return { statusCode: 503, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Retry-After': '60' }, body: `<h1>Temporarily unavailable</h1><p><a href="${CATALOG}">Browse all worksheets</a></p>` };
  }
};
