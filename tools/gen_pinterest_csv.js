// Genera el plan de pines de Pinterest para Workshido (02-03/10/2026):
//   tools/pinterest/pins.json — los 811 pines en orden, con los datos de la
//     imagen (los pinta tools/pinterest/render_pins.py y los sube a R2 en
//     files.workshido.com/pins/<key>.jpg).
//   tools/pinterest/workshido_pins_NN.csv — tandas de 70 pines para "Crear pines
//     en bloque" de Pinterest (Title, Media URL, Pinterest board, Thumbnail,
//     Description, Link, Publish date, Keywords). Pinterest solo deja programar
//     14 días por adelantado → 14 días × 5 pines = 70 por archivo; cada tanda se
//     genera con la fecha del día en que Juan la va a subir.
//
// Reglas (auditoría SEO/marketing 02/10):
// - Cada pin enlaza a la página HTML exacta (/worksheet/<slug>/ o el hub del
//   tema), NUNCA al PDF ni a la home, con UTM por pin para medir en
//   analytics_events qué tema/tablero trae registros.
// - Título: la búsqueda primero (~40 primeros caracteres son los visibles):
//   "<Tema> <Skill> Worksheet <Nivel> | Free PDF".
// - Tablero: el del tema (11 hubs de netlify/lib/topics.js) o el de la skill.
// - Primero 1 pin de set por hub (enlaza al hub), luego las fichas por
//   descargas; 5 pines por día — ritmo constante, no 800 de golpe.
//
// Vive en tools/ (bloqueado con 404 en netlify.toml): la raíz del repo es pública.
// Uso: node tools/gen_pinterest_csv.js <tanda 1..12> [YYYY-MM-DD primer día] [pines por día]
const fs = require('fs');
const path = require('path');
const { topicFor, HUBS } = require('../netlify/lib/topics');

const SITE = 'https://workshido.com';
const SB = 'https://mhbgxdsdaalvtgobnvbh.supabase.co/rest/v1';
const KEY = 'sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo';
const BATCH = Number(process.argv[2] || 1);
const START = process.argv[3] || new Date(Date.now() + 86400000).toISOString().slice(0, 10);
const PER_DAY = Number(process.argv[4] || 5);
const BATCH_SIZE = 14 * PER_DAY;
const MEDIA = (key) => `https://files.workshido.com/pins/${key}.jpg`;

const SKILL_BOARDS = {
  Grammar: 'ESL Grammar Worksheets', Practice: 'ESL Grammar Worksheets',
  Vocabulary: 'ESL Vocabulary Worksheets', Reading: 'ESL Reading Comprehension Worksheets',
  Writing: 'ESL Writing Worksheets', Speaking: 'ESL Speaking Activities', Listening: 'ESL Listening Worksheets',
};
const displayCategory = (r) => (r.category === 'Grammar' && /\bpractice\b/i.test(r.title || '')) ? 'Practice' : (r.category || 'Grammar');
const stripLevel = (t) => t.replace(/\s*\((?:A1|A2|B1|B2|C1)\)\s*/gi, ' ').replace(/\s+/g, ' ').trim();
const slugify = (s) => s.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
// Plain ASCII punctuation in the CSV: en dashes / curly quotes risk turning into
// mojibake ("A1â€"B1") depending on how Pinterest decodes the upload.
const ascii = (s) => s.replace(/[–—]/g, '-').replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/…/g, '...');
const csv = (v) => `"${ascii(String(v ?? '')).replace(/"/g, '""')}"`;

// Text on the image: "PAST SIMPLE" / "The 30 Most Common Irregular Verbs".
function creative(r) {
  const [base, type] = stripLevel(r.title).split(/\s[–-]\s/);
  const skill = displayCategory(r);
  const [head, ...rest] = base.split(/:\s*/);
  let sub = rest.join(': ');
  if (!sub && type && !new RegExp(`^${skill}$`, 'i').test(type)) sub = type;
  return { type: 'WORKSHEET', label: `${r.level} · ${skill}`, title: head, sub, cta: 'VIEW THE FREE WORKSHEET', thumbs: [r.thumbnail_url] };
}

function pinTitle(r) {
  const [base, type] = stripLevel(r.title).split(/\s[–-]\s/);
  const skill = displayCategory(r);
  // "Daily Routines – Vocabulary" → "Daily Routines Vocabulary Worksheet A1 | Free PDF".
  // The type part ("Word Search", "Color and Learn") is kept when it is more
  // specific than the skill; titles that already say "worksheet" aren't doubled.
  let what = type && !new RegExp(`^${skill}$`, 'i').test(type) ? `${base} ${type}` : `${base} ${skill}`;
  if (!/worksheet/i.test(what)) what += ' Worksheet';
  let t = `${what} ${r.level} | Free PDF`;
  if (t.length > 100) t = `${what} ${r.level}`.slice(0, 100);
  return t;
}

function pinDescription(r) {
  const d = (r.description || '').trim().replace(/\s+/g, ' ');
  const tail = ' Free printable PDF for ESL/EFL classes — download it at Workshido.';
  return (d + tail).slice(0, 495);
}

function keywords(r, topic) {
  const skill = displayCategory(r).toLowerCase();
  const set = new Set([
    topic && topic.hub ? `${topic.hub.name.toLowerCase()} worksheets` : null,
    `${skill} worksheet`, `${r.level} english worksheets`, 'esl worksheets', 'free printable worksheets',
  ].filter(Boolean));
  return [...set].join(', ');
}

const utm = (campaign, content) =>
  `utm_source=pinterest&utm_medium=organic&utm_campaign=${campaign}&utm_content=${content}`;

(async () => {
  const res = await fetch(`${SB}/worksheets?select=id,slug,title,level,category,description,tags,thumbnail_url,downloads,created_at,file_type&slug=not.is.null`,
    { headers: { apikey: KEY, Range: '0-4999' } });
  const rows = (await res.json()).filter((r) => r.thumbnail_url && (r.file_type || '').toLowerCase() !== 'docx' && !/\.docx(\?|$)/i.test(r.file_url || ''));

  const pins = [];
  // 1) One "complete set" pin per topic hub → the hub page (needs its own
  //    creative: 4 small previews + "Grammar · Reading · Writing · Practice").
  for (const h of HUBS) {
    const members = rows.filter((r) => { const t = topicFor(r); return t && t.hub && t.hub.slug === h.hub.slug; })
      .sort((a, b) => (b.downloads || 0) - (a.downloads || 0));
    if (!members.length) continue;
    const levels = [...new Set(members.map((r) => r.level))].sort().join('–').replace(/^(\w+)–.*–(\w+)$/, '$1–$2');
    // 4 previews, one per skill where possible (Grammar, Reading, Writing, Practice).
    const thumbs = [];
    for (const cat of ['Grammar', 'Reading', 'Writing', 'Practice', 'Vocabulary']) {
      const m = members.find((r) => displayCategory(r) === cat && !thumbs.includes(r.thumbnail_url));
      if (m) thumbs.push(m.thumbnail_url);
    }
    for (const m of members) if (thumbs.length < 4 && !thumbs.includes(m.thumbnail_url)) thumbs.push(m.thumbnail_url);
    const key = `set-${h.hub.slug}`;
    pins.push({
      type: 'SET',
      key,
      creative: { type: 'SET', label: `${levels} · Complete set`, title: `${h.hub.name} Worksheets`, sub: 'One topic. Four skills. Zero prep.', cta: 'GET THE FREE SET', thumbs },
      title: `${h.hub.name} Worksheets ${levels} | Free ESL Set`,
      media: MEDIA(key),
      board: `${h.hub.name} Worksheets`,
      description: `Free ${h.hub.name} worksheets for ${levels} ESL/EFL classes: grammar, reading, writing and practice sheets designed to be taught in order. Print-ready PDFs at Workshido.`,
      link: `${SITE}/worksheets/topics/${h.hub.slug}/?${utm(slugify(h.hub.name) + '_set', 'set_pin')}`,
      keywords: `${h.hub.name.toLowerCase()} worksheets, esl worksheets, free printable worksheets, english grammar worksheets`,
    });
  }
  // 2) One pin per worksheet → its own page. Most downloaded first (what
  //    teachers already pick), newest breaking ties.
  rows.sort((a, b) => (b.downloads || 0) - (a.downloads || 0) || String(b.created_at).localeCompare(String(a.created_at)));
  for (const r of rows) {
    const topic = topicFor(r);
    const board = topic && topic.hub ? `${topic.hub.name} Worksheets` : SKILL_BOARDS[displayCategory(r)] || 'Free English Worksheets';
    pins.push({
      type: 'WORKSHEET',
      key: r.slug,
      creative: creative(r),
      title: pinTitle(r),
      media: MEDIA(r.slug),
      board,
      description: pinDescription(r),
      link: `${SITE}/worksheet/${r.slug}/?${utm(slugify(topic && topic.hub ? topic.hub.name : displayCategory(r)) + '_' + r.level.toLowerCase(), r.slug)}`,
      keywords: keywords(r, topic),
    });
  }

  const dir = path.join(__dirname, 'pinterest');
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'pins.json'), JSON.stringify(pins, null, 1), 'utf8');

  const slice = pins.slice((BATCH - 1) * BATCH_SIZE, BATCH * BATCH_SIZE);
  const total = Math.ceil(pins.length / BATCH_SIZE);
  if (!slice.length) { console.log(`no hay tanda ${BATCH} (son ${total})`); return; }
  // 14:00 UTC (9:00 en Colombia / mañana en EE. UU.), luego cada 2 h.
  const day0 = new Date(START + 'T14:00:00Z');
  const lines = [['Title', 'Media URL', 'Pinterest board', 'Thumbnail', 'Description', 'Link', 'Publish date', 'Keywords'].map(csv).join(',')];
  slice.forEach((p, i) => {
    const d = new Date(day0.getTime() + Math.floor(i / PER_DAY) * 86400000 + (i % PER_DAY) * 2 * 3600000);
    lines.push([p.title, p.media, p.board, '', p.description, p.link, d.toISOString().slice(0, 19), p.keywords].map(csv).join(','));
  });
  const out = path.join(dir, `workshido_pins_${String(BATCH).padStart(2, '0')}.csv`);
  fs.writeFileSync(out, lines.join('\r\n'), 'utf8');
  const boards = [...new Set(slice.map((p) => p.board))];
  console.log(`${pins.length} pines en total (${total} tandas). Tanda ${BATCH}: ${slice.length} pines, ${START} → ${lines[lines.length - 1].split('","')[6]}`);
  console.log(`→ ${out}`);
  console.log('tableros usados en esta tanda:', boards.join(' | '));
})();
