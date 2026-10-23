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
const { fetchAllRows } = require('../lib/fetch-all');
const { topicFor, seoTitle, isFunctional } = require('../lib/topics');

const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
const SITE = 'https://workshido.com';

// The real SPA shell lives at this filename (not workshido-worksheet.html —
// that public URL is now owned by this function via a netlify.toml redirect,
// so fetching it here would recurse into this same function).
//
// The origin is taken from the incoming request, NOT hardcoded to SITE: on a
// draft/preview deploy this function must fetch THAT deploy's template, or a
// pre-production test would silently validate the live production template
// instead of the change being tested. Canonical/OG URLs below stay pinned to
// SITE on purpose — a preview must never emit preview URLs as canonical.
function templateUrlFor(event) {
  const host = (event.headers && (event.headers['x-forwarded-host'] || event.headers.host)) || '';
  const origin = host ? `https://${host}` : SITE;
  return `${origin}/workshido-worksheet-app.html`;
}

// Cached across warm invocations of the same function container; refetched
// after 5 minutes so a template edit + deploy shows up without a cold start.
// Keyed by origin so a container can never serve one deploy's template under
// another deploy's host.
const templateCache = new Map();
async function getTemplate(event) {
  const url = templateUrlFor(event);
  const now = Date.now();
  const hit = templateCache.get(url);
  if (hit && now - hit.fetchedAt < 5 * 60 * 1000) return hit.html;
  const res = await fetch(url);
  const html = await res.text();
  templateCache.set(url, { html, fetchedAt: now });
  return html;
}

function escapeHtml(s) {
  return String(s).replace(/[<>&'"]/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]));
}
// Google cuts the SERP snippet around 160 chars. Slicing blindly left it
// mid-word ("...writing ad"), so end on a sentence when one lands close to the
// limit, otherwise on a whole word plus an ellipsis.
function trimDesc(s, max = 160) {
  s = String(s).replace(/\s+/g, ' ').trim();
  if (s.length <= max) return s;
  const cut = s.slice(0, max);
  const sentence = Math.max(cut.lastIndexOf('. '), cut.lastIndexOf('; '), cut.lastIndexOf(': '));
  if (sentence >= max * 0.75) return cut.slice(0, sentence + 1).trim();
  const word = cut.lastIndexOf(' ');
  return cut.slice(0, word > 0 ? word : max - 1).replace(/[,;:—–-]+$/, '').trim() + '…';
}

function escapeAttr(s) {
  return String(s).replace(/[&'"]/g, (c) => ({ '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]));
}

// SEO URL migration switch.
//
// false (phase 1–2): the legacy /workshido-worksheet.html?id=… URL still
//   answers 200 with the full page, but its canonical already points at the
//   new /worksheet/<slug>/ URL. Google starts consolidating on its own and
//   NOTHING is destructive — every old link keeps working exactly as before.
// true  (phase 3): the legacy URL answers 301 to the slug URL.
//
// Flip this to true ONLY after the slug route is verified live, because a
// 301 is cached hard by browsers and is the one genuinely irreversible step
// of this migration.
const LEGACY_REDIRECTS_301 = true;

// Matches /worksheet/<slug> and /worksheet/<slug>/ (the trailing-slash form
// is canonical; the other 301s to it below).
const SLUG_ROUTE = /^\/worksheet\/([^/]+)\/?$/;

const slugUrl = (slug) => `${SITE}/worksheet/${slug}/`;

const CATEGORY_PAGES = { Grammar: 'grammar', Vocabulary: 'vocabulary', Reading: 'reading', Writing: 'writing' };

// Home › A1 Worksheets › <topic hub, or category page> › <title>. Returned as
// data so the visible trail, the BreadcrumbList JSON-LD and the client
// re-render (via #wsSeo) are built from the same list.
function breadcrumbFor(data, topic, url) {
  const items = [{ name: 'Home', url: `${SITE}/` }];
  if (data.level) items.push({ name: `${data.level} Worksheets`, url: `${SITE}/worksheets/levels/${data.level.toLowerCase()}/` });
  if (topic && topic.hub) items.push({ name: topic.hub.name, url: `${SITE}/worksheets/topics/${topic.hub.slug}/` });
  else if (CATEGORY_PAGES[data.category]) items.push({ name: data.category, url: `${SITE}/worksheets/${CATEGORY_PAGES[data.category]}/` });
  items.push({ name: data.title, url });
  return items;
}

// "Complete the set" — this worksheet's same-level siblings on the same topic
// (same topic_key, or the same "Topic – Type" title base), in teaching order.
// Same membership rule as the client's "These worksheets form a set" line in
// js/workshido-worksheet.js (titleBase / isEasyWordSearch / displayCategory are
// copies of the client's): 2+ siblings spanning 2+ categories, otherwise it's
// not a teaching sequence and nothing is shown. Rendered here so no-JS
// crawlers get the sibling links; the client reuses this markup verbatim.
const SET_ORDER = ['Grammar', 'Reading', 'Writing', 'Practice', 'Vocabulary', 'Speaking', 'Listening'];
const titleBase = (t) => (t || '').split(/\s[–-]\s/)[0].replace(/\s*\((?:a1|a2|b1|b2|c1)\)\s*$/i, '').trim().toLowerCase();
const isEasyWordSearch = (t) => /\(easy version\)/i.test(t || '');
const displayCategory = (r) => (r.category === 'Grammar' && /\bpractice\b/i.test(r.title || '')) ? 'Practice' : (r.category || 'Other');

function setFor(data, rows) {
  if (!data.level || isEasyWordSearch(data.title)) return [];
  const base = titleBase(data.title);
  const sibs = rows.filter((r) => r.id !== data.id && r.level === data.level && !isEasyWordSearch(r.title)
    && ((data.topic_key && r.topic_key === data.topic_key) || (base && titleBase(r.title) === base)));
  const all = [data, ...sibs];
  if (sibs.length < 2 || new Set(all.map(displayCategory)).size < 2) return [];
  const rank = (r) => { const i = SET_ORDER.indexOf(displayCategory(r)); return i < 0 ? 99 : i; };
  // Max 6 rows: this worksheet + one per category first, so a set with two
  // Grammar variants never loses its Practice row to the cap; extras after.
  const picked = [data], cats = new Set([displayCategory(data)]);
  for (const r of sibs) if (!cats.has(displayCategory(r))) { cats.add(displayCategory(r)); picked.push(r); }
  for (const r of sibs) if (picked.length < 6 && !picked.includes(r)) picked.push(r);
  return picked.slice(0, 6)
    .sort((a, b) => rank(a) - rank(b) || (a.id === data.id ? -1 : b.id === data.id ? 1 : 0))
    .map((r) => ({ id: r.id, slug: r.slug, title: r.title, cat: displayCategory(r), current: r.id === data.id }));
}

function setHtml(set, ws) {
  if (!set.length) return '<div class="ws-set" id="ssrSet" hidden></div>';
  const items = set.map((r, i) => {
    const inner = `<span class="ws-set-dot">${i + 1}</span><span class="ws-set-cat">${escapeHtml(r.cat)}</span>`
      + `<span class="ws-set-name">${r.current ? 'You&apos;re here' : escapeHtml(r.title)}</span>`;
    return r.current
      ? `<li class="cur" data-id="${escapeAttr(r.id)}" aria-current="page">${inner}</li>`
      : `<li data-id="${escapeAttr(r.id)}"><a href="/worksheet/${escapeAttr(r.slug)}/" title="${escapeAttr(r.title)}">${inner}</a></li>`;
  }).join('');
  return `<div class="ws-set" id="ssrSet" role="navigation" aria-label="Worksheets in this set">`
    // Functional English sets have no Grammar sheet and their own order
    // (Reading → Practice → Writing), explained in their own guide.
    + (isFunctional(ws)
      ? `<div class="ws-set-head"><span>Complete the set</span><a href="/guides/how-to-teach-functional-english/">How to teach functional English →</a></div>`
      : `<div class="ws-set-head"><span>Complete the set</span><a href="/guides/how-to-sequence-esl-lessons/">Teach it in order →</a></div>`)
    + `<ol class="ws-set-list">${items}</ol></div>`;
}

// The inlined row is public page source: drop the paid Teacher Edition URL
// (only get-teacher-edition-url hands it out, after the premium check) and keep
// just the yes/no the page needs to show the button.
function publicRow(data) {
  const { teacher_edition_url, ...row } = data;
  return { ...row, has_teacher_edition: !!(data.has_teacher_edition ?? teacher_edition_url) };
}

exports.handler = async (event) => {
  const path = event.path || '';
  const slugMatch = path.match(SLUG_ROUTE);
  const slug = slugMatch ? decodeURIComponent(slugMatch[1]) : null;
  const id = event.queryStringParameters && event.queryStringParameters.id;

  // One canonical spelling per page: /worksheet/foo → /worksheet/foo/.
  // Safe to 301 unconditionally — this namespace is brand new, so no
  // already-indexed URL is affected.
  if (slug && !path.endsWith('/')) {
    return { statusCode: 301, headers: { Location: `/worksheet/${slugMatch[1]}/`, 'Cache-Control': 'public, max-age=0, must-revalidate' }, body: '' };
  }

  // Neither a slug nor an id (or a malformed request) — serve the template
  // untouched, same as the static file always did. Never block the page.
  // Bare /workshido-worksheet.html (no id, no slug) is an empty shell titled just
  // "Workshido" with a self-canonical — a soft-404 in Search Console. Send it to
  // the catalog instead.
  if (!slug && !id) {
    return { statusCode: 301, headers: { Location: '/workshido-index.html', 'Cache-Control': 'public, max-age=3600' }, body: '' };
  }

  try {
    const query = slug
      ? sb.from('worksheets').select('*').eq('slug', slug).single()
      : sb.from('worksheets').select('*').eq('id', id).single();
    const [template, { data, error }] = await Promise.all([getTemplate(event), query]);

    // .single() reports "no row" as PGRST116; any other error is Supabase
    // being unreachable, which must not tell Google a live worksheet is gone.
    if (error && error.code !== 'PGRST116') {
      return { statusCode: 503, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Retry-After': '60', 'Cache-Control': 'no-store' }, body: template };
    }
    if (error || !data) {
      // A real, since-deleted/renamed worksheet id — this is the exact
      // shape of a "soft 404" (200 OK, no real content) that Search Console
      // flags. Serve the shell but say so with the status code, so it's an
      // unambiguous 404 instead of looking like a valid empty page.
      return { statusCode: 404, headers: { 'Content-Type': 'text/html; charset=utf-8' }, body: template };
    }

    // Legacy ?id= URL, once the migration is armed: send its accumulated
    // ranking to the slug URL. max-age=0 keeps browsers revalidating rather
    // than freezing the redirect locally while the rollout is being watched;
    // Google still treats a 301 as permanent regardless of caching headers.
    if (!slug && LEGACY_REDIRECTS_301 && data.slug) {
      return {
        statusCode: 301,
        headers: {
          Location: slugUrl(data.slug),
          'Cache-Control': 'public, max-age=0, must-revalidate',
          'Netlify-CDN-Cache-Control': 'public, s-maxage=300, durable',
          'Netlify-Vary': 'query=id',
        },
        body: '',
      };
    }

    // Brand suffix kept on OG/Twitter (social cards) but NOT on <title>: the
    // worksheet titles are already descriptive, and the extra " — Workshido"
    // just pushed them past Google's ~60-char SERP cutoff.
    const title = `${data.title} — Workshido`;
    const pageTitle = seoTitle(data);
    const desc = data.description
      ? trimDesc(data.description)
      : `Free ${data.level || ''} ${data.category || 'English'} worksheet — download and print for class.`.replace(/\s+/g, ' ').trim();
    // Canonical/OG always point at the slug URL — including when this request
    // came in on the legacy ?id= path. That is what lets Google consolidate
    // the two URLs onto the new one before any redirect exists. Falls back to
    // the legacy shape if a row somehow has no slug, so the tag is never empty.
    const url = data.slug
      ? slugUrl(data.slug)
      : `${SITE}/workshido-worksheet.html?id=${encodeURIComponent(data.id)}`;
    const image = data.thumbnail_url || `${SITE}/og-image.png`;
    // Visible body copy for no-JS crawlers. description is capped at 160 so the
    // meta description isn't truncated in the SERP; description_long keeps the
    // fuller text, which is worth more here as indexable page content.
    const bodyDesc = data.description_long || data.description || desc;

    // Same-level rows only (~250, light columns) for the set nav. Not the whole
    // catalog: PostgREST caps a response at 1000 rows, which the catalog will
    // pass. Only runs on a CDN cache miss (s-maxage below).
    const { data: levelRows } = data.level
      ? await fetchAllRows(() => sb.from('worksheets').select('id,slug,title,level,category,topic_key').eq('level', data.level).not('slug', 'is', null).order('id'))
      : { data: [] };
    const set = setFor(data, levelRows || []);
    const previewAlt = (/worksheet/i.test(data.title || '') ? `${data.title} – preview` : `${(data.title || '').replace(/\s*\((?:A1|A2|B1|B2|C1)\)\s*$/i, '')} – ${data.level || ''} ${data.category || 'English'} worksheet preview`).replace(/\s+/g, ' ');
    const topic = topicFor(data);
    const crumbs = breadcrumbFor(data, topic, url);
    const crumbsHtml = crumbs
      .map((c, i) => (i === crumbs.length - 1
        ? `<span aria-current="page">${escapeHtml(c.name)}</span>`
        : `<a href="${escapeAttr(c.url.replace(SITE, ''))}">${escapeHtml(c.name)}</a>`))
      .join('<span>›</span>');
    const breadcrumbLD = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: crumbs.map((c, i) => ({ '@type': 'ListItem', position: i + 1, name: c.name, item: c.url })),
    }).replace(/</g, '\\u003c');
    const topicLinks = [];
    if (topic && topic.guide) topicLinks.push({ href: `/guides/${topic.guide.slug}/`, text: `📘 ${topic.guide.label} →` });
    if (topic && topic.hub) topicLinks.push({ href: `/worksheets/topics/${topic.hub.slug}/`, text: `All ${topic.hub.name} worksheets →` });
    const topicLinksHtml = topicLinks.map((l) => `<a href="${escapeAttr(l.href)}">${escapeHtml(l.text)}</a>`).join('');
    // Read by js/workshido-worksheet.js so its re-render keeps the same title,
    // trail and links without duplicating the topic map client-side.
    const seoData = JSON.stringify({ title: pageTitle, crumbs, links: topicLinks }).replace(/</g, '\\u003c');

    // Mirrors the LearningResource JSON-LD that js/workshido-worksheet.js
    // builds client-side (kept in sync with that block). Stringified with < → <
    // so a title containing "</script>" can't break out of the tag.
    const schemaLD = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'LearningResource',
      name: data.title,
      description: bodyDesc,
      educationalLevel: data.level,
      learningResourceType: 'Worksheet',
      inLanguage: 'en',
      isAccessibleForFree: data.is_free !== false,
      image: image,
      // Was missing entirely: without these, the structured data never told
      // Google which URL it describes — exactly the ambiguity to avoid while
      // two URLs serve the same worksheet.
      url: url,
      mainEntityOfPage: url,
      provider: { '@type': 'Organization', name: 'Workshido', url: 'https://workshido.com' },
    }).replace(/</g, '\\u003c');

    let html = template
      .replace('<title>Workshido</title>', `<title>${escapeHtml(pageTitle)}</title>`)
      .replace(
        '<h1 class="ws-title" id="ssrTitle">English worksheet</h1>',
        `<h1 class="ws-title" id="ssrTitle">${escapeHtml(data.title)}</h1>`
      )
      .replace(
        /<div class="breadcrumb" id="breadcrumb" role="navigation" aria-label="Breadcrumb">[\s\S]*?<\/div>/,
        `<div class="breadcrumb" id="breadcrumb" role="navigation" aria-label="Breadcrumb">${crumbsHtml}</div>`
      )
      .replace(
        '<div class="ws-topic-links" id="ssrTopicLinks" hidden></div>',
        topicLinksHtml ? `<div class="ws-topic-links" id="ssrTopicLinks">${topicLinksHtml}</div>` : ''
      )
      .replace('<div class="ws-set" id="ssrSet" hidden></div>', () => setHtml(set, data))  // fn: titles may contain "$"
      .replace(
        '<script type="application/ld+json" id="breadcrumbLD"></script>',
        `<script type="application/ld+json" id="breadcrumbLD">${breadcrumbLD}</script>`
      )
      .replace(
        '<script type="application/json" id="wsSeo"></script>',
        `<script type="application/json" id="wsSeo">${seoData}</script>`
      )
      // Real preview image in the initial HTML: it is the LCP element, and
      // with explicit width/height it reserves its box, so the client re-render
      // of #pageWrap doesn't shift the page. Same attributes the client uses.
      // Preload the LCP image from <head> so it starts downloading before the
      // parser reaches the body (the inline CSS in <head> is large).
      .replace(
        '<link rel="preconnect" href="https://files.workshido.com">',
        data.thumbnail_url
          ? `<link rel="preconnect" href="https://files.workshido.com">
<link rel="preload" as="image" href="${escapeAttr(data.thumbnail_url)}" fetchpriority="high">`
          : '<link rel="preconnect" href="https://files.workshido.com">'
      )
      .replace(
        '<div class="preview-box" id="ssrPreview"><div class="loading">Loading worksheet...</div></div>',
        data.thumbnail_url
          ? `<div class="preview-box" id="ssrPreview"><img src="${escapeAttr(data.thumbnail_url)}" alt="${escapeAttr(previewAlt)}" fetchpriority="high" decoding="async" width="640" height="904"></div>`
          : '<div class="preview-box" id="ssrPreview"></div>'
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
        `<script type="application/json" id="wsData">${JSON.stringify(publicRow(data)).replace(/</g, '\\u003c')}</script>`
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
        // s-maxage raised 300 → 3600 (02/10/2026): with ~800 pages and a 5-min
        // TTL most views missed the cache — worksheet TTFB p75 was ~950ms in
        // our own web_vitals. Content only changes on upload (≤1h stale is
        // fine; the client re-reads the live row) and every deploy purges it.
        'Netlify-CDN-Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400, durable',
        'Netlify-Vary': 'query=id',
      },
      body: html,
    };
  } catch (err) {
    // Never let a Supabase hiccup take the page down — fall back to the
    // plain template, same as before this function existed. 503, not 200: the
    // bare template is titled just "Workshido" with a generic canonical, and a
    // crawler that caught it as a 200 would index that instead of the worksheet.
    const template = await getTemplate(event);
    return { statusCode: 503, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Retry-After': '60', 'Cache-Control': 'no-store' }, body: template };
  }
};
