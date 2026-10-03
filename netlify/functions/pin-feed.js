// Feed RSS por tablero para "Auto-publish Pins" de Pinterest (03/10/2026).
//
//   /pinterest/feed/<tablero>.xml  →  este archivo (redirect en netlify.toml)
//
// Pinterest revisa cada feed una vez al día y crea un pin por cada ítem que no
// haya visto. Así nadie tiene que subir CSV: el goteo sale solo.
// - Ítems del calendario (netlify/lib/pin-schedule.json, lo arma
//   tools/pinterest/build_schedule.js): solo los que ya llegaron a su fecha.
// - Fichas subidas después del calendario: entran solas al día siguiente de su
//   created_at, al tablero de su tema/skill/nivel, con su imagen de pin si ya se
//   pintó (tools/pinterest/render_pins.py) o la vista previa real como respaldo.
//
// Mismo archivo en Workshido y Spanishido; el sitio sale de pin-schedule.json.
const { createClient } = require('@supabase/supabase-js');
const { topicFor } = require('../lib/topics');
const schedule = require('../lib/pin-schedule.json');

const ES = schedule.site === 'spanishido';
const SITE = ES ? 'https://spanishido.com' : 'https://workshido.com';
const BRAND = ES ? 'Spanishido' : 'Workshido';
const MAX_ITEMS = 50;
const NEW_WINDOW_DAYS = 60;
const known = new Set(schedule.known);
const boardSlug = (s) => s.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const esc = (s) => String(s || '').replace(/[<>&'"]/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]));

// --- same naming rules as tools/gen_pinterest_csv.js (kept short on purpose) ---
const displayCategory = (r) => (r.category === 'Grammar' && /\bpractice\b/i.test(r.title || '')) ? 'Practice' : (r.category || 'Grammar');
const stripLevel = (t) => (t || '').replace(/\s*\((?:A1|A2|B1|B2|C1)\)\s*/gi, ' ').replace(/\s+/g, ' ').trim();
const enBase = (base) => base.replace(/\s*\([^()]+\)\s*$/, '').trim();
const SKILL_BOARDS = ES
  ? { Reading: 'Spanish Reading Comprehension Worksheets', Writing: 'Spanish Writing Worksheets' }
  : { Grammar: 'ESL Grammar Worksheets', Practice: 'ESL Grammar Worksheets', Vocabulary: 'ESL Vocabulary Worksheets', Reading: 'ESL Reading Comprehension Worksheets', Writing: 'ESL Writing Worksheets', Speaking: 'ESL Speaking Activities' };
const LEVEL_BOARDS = { A1: 'Spanish 1 Worksheets (A1)', A2: 'Spanish 2 Worksheets (A2)', B1: 'Spanish 3 Worksheets (B1)', B2: 'Spanish 4 Worksheets (B2)' };

function newItem(r) {
  const topic = topicFor(r);
  const skill = displayCategory(r);
  const board = topic && topic.hub ? `${topic.hub.name} Worksheets` : (SKILL_BOARDS[skill] || (ES ? LEVEL_BOARDS[r.level] : 'ESL Grammar Worksheets'));
  const [base, type] = stripLevel(r.title).split(/\s[–-]\s/);
  let title;
  if (ES) title = `${enBase(base)} Spanish ${skill} Worksheet ${r.level} | Free PDF`;
  else {
    let what = type && !new RegExp(`^${skill}$`, 'i').test(type) ? `${base} ${type}` : `${base} ${skill}`;
    if (!/worksheet/i.test(what)) what += ' Worksheet';
    title = `${what} ${r.level} | Free PDF`;
  }
  const tail = ES ? ' Free printable PDF for Spanish classes - download it at Spanishido.' : ' Free printable PDF for ESL/EFL classes - download it at Workshido.';
  return {
    k: r.slug,
    b: boardSlug(board),
    t: title.slice(0, 100),
    d: ((r.description || '').trim() + tail).slice(0, 495),
    l: `${SITE}/worksheet/${r.slug}/?utm_source=pinterest&utm_medium=organic&utm_campaign=new_${(r.level || '').toLowerCase()}&utm_content=${r.slug}`,
    m: `https://files.workshido.com/${ES ? 'es/' : ''}pins/${r.slug}.jpg`,
    fallback: r.thumbnail_url,
    at: new Date(Date.parse(r.created_at) + 86400000).toISOString(),
  };
}

async function newWorksheets(board, now) {
  if (!process.env.SUPABASE_URL) return [];
  const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);
  const since = new Date(now - NEW_WINDOW_DAYS * 86400000).toISOString();
  const { data } = await sb.from('worksheets')
    .select('slug,title,level,category,description,thumbnail_url,created_at,topic_key,tags')
    .gte('created_at', since).not('slug', 'is', null).not('thumbnail_url', 'is', null)
    .order('created_at', { ascending: false }).limit(500);
  const items = (data || []).filter((r) => !known.has(r.slug)).map(newItem)
    .filter((i) => i.b === board && Date.parse(i.at) <= now);
  // Use the framed pin image when it has been rendered, else the real preview.
  await Promise.all(items.map(async (i) => {
    try {
      const res = await fetch(i.m, { method: 'HEAD', headers: { 'User-Agent': 'Mozilla/5.0 (compatible; Pinterestbot/1.0)' } });
      if (!res.ok) i.m = i.fallback;
    } catch (e) { i.m = i.fallback; }
  }));
  return items;
}

exports.handler = async (event) => {
  // Netlify keeps the ORIGINAL path on a rewrite (the ?board= in netlify.toml
  // doesn't reach the function), so the board comes from /pinterest/feed/<board>.xml.
  const fromPath = ((event.path || '').match(/\/pinterest\/feed\/([^/?]+)/) || [])[1] || '';
  const raw = decodeURIComponent((event.queryStringParameters || {}).board || fromPath).replace(/\.xml$/i, '');
  const name = schedule.boards[raw];
  if (!name) return { statusCode: 404, headers: { 'Content-Type': 'text/plain' }, body: 'unknown board' };
  const now = Date.now();
  let items = schedule.items.filter((i) => i.b === raw && Date.parse(i.at) <= now);
  try { items = items.concat(await newWorksheets(raw, now)); } catch (e) { /* the schedule alone still works */ }
  items.sort((a, b) => Date.parse(b.at) - Date.parse(a.at));
  items = items.slice(0, MAX_ITEMS);

  const xmlItems = items.map((i) => {
    const type = /\.webp(\?|$)/i.test(i.m) ? 'image/webp' : 'image/jpeg';
    return `<item>
  <title>${esc(i.t)}</title>
  <link>${esc(i.l)}</link>
  <guid isPermaLink="false">${esc(schedule.site + ':' + i.k)}</guid>
  <pubDate>${new Date(i.at).toUTCString()}</pubDate>
  <description>${esc(i.d)}</description>
  <enclosure url="${esc(i.m)}" type="${type}" length="0"/>
  <media:content url="${esc(i.m)}" medium="image" type="${type}"/>
</item>`;
  }).join('\n');

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>${esc(`${BRAND} - ${name}`)}</title>
<link>${SITE}/</link>
<atom:link href="${SITE}/pinterest/feed/${raw}.xml" rel="self" type="application/rss+xml"/>
<description>${esc(`${name}: free printable worksheets from ${BRAND}.`)}</description>
<language>en</language>
${xmlItems}
</channel>
</rss>
`;
  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
      'Cache-Control': 'public, max-age=0, must-revalidate',
      'Netlify-CDN-Cache-Control': 'public, s-maxage=3600, durable',
      // A feed for Pinterest's crawler, not a page for search results.
      'X-Robots-Tag': 'noindex',
    },
    body,
  };
};
