// Calendario de pines para el feed RSS de Pinterest (03/10/2026).
//
// Pinterest "Auto-publish Pins by connecting an RSS feed": un feed por tablero;
// Pinterest lo revisa cada día y crea un pin por cada ítem nuevo. El feed lo
// sirve netlify/functions/pin-feed.js y solo muestra los ítems cuya fecha ya
// llegó → goteo de PER_DAY pines por día sin subir CSV nunca más.
//
// Entrada: tools/pinterest/pins.json | pins_es.json (gen_pinterest_csv.js).
// Salida:  <repo del sitio>/netlify/lib/pin-schedule.json
//
// Uso: node tools/pinterest/build_schedule.js <workshido|spanishido> <YYYY-MM-DD inicio> [saltar N] [pines/día]
//   saltar N = los primeros N pines ya programados por otra vía (Workshido: la
//   tanda 1 se subió por CSV el 03/10 para el 04→17/10 → saltar 70, inicio 2026-10-18).
const fs = require('fs');
const path = require('path');

const [site, start, skipArg, perDayArg] = process.argv.slice(2);
if (!['workshido', 'spanishido'].includes(site) || !start) {
  console.error('uso: node tools/pinterest/build_schedule.js <workshido|spanishido> <YYYY-MM-DD> [saltar] [por día]');
  process.exit(1);
}
const ES = site === 'spanishido';
const SKIP = Number(skipArg || 0);
const PER_DAY = Number(perDayArg || 5);
const slug = (s) => s.toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

const all = JSON.parse(fs.readFileSync(path.join(__dirname, ES ? 'pins_es.json' : 'pins.json'), 'utf8')).slice(SKIP);
const day0 = new Date(start + 'T14:00:00Z').getTime();
const toItem = (p, at) => ({ k: p.key, b: slug(p.board), t: p.title, d: p.description, l: p.link, m: p.media, at: new Date(at).toISOString() });
// Seed: each board's first pin is available right away, so no feed is empty
// when it gets connected in Pinterest (an empty feed can be rejected). The
// rest drips at PER_DAY from `start`.
const seedAt = Date.now() - 3600000;
const seeded = new Set();
const seeds = [];
for (const p of all) {
  const b = slug(p.board);
  if (!seeded.has(b)) { seeded.add(b); seeds.push(p); }
}
const rest = all.filter((p) => !seeds.includes(p));
const boards = {};
for (const p of all) boards[slug(p.board)] = p.board;
const items = [
  ...seeds.map((p) => toItem(p, seedAt)),
  ...rest.map((p, i) => toItem(p, day0 + Math.floor(i / PER_DAY) * 86400000 + (i % PER_DAY) * 2 * 3600000)),
];
// Every worksheet key already planned (incl. the skipped CSV batch): the feed
// treats any other worksheet as "new since this schedule" and adds it itself.
const known = JSON.parse(fs.readFileSync(path.join(__dirname, ES ? 'pins_es.json' : 'pins.json'), 'utf8')).map((p) => p.key);
const out = {
  site,
  generated: new Date().toISOString(),
  boards,
  known,
  items,
};
const repo = path.resolve(__dirname, '..', '..', '..', ES ? 'Spanishido' : 'Workshido');
const dest = path.join(repo, 'netlify', 'lib', 'pin-schedule.json');
fs.writeFileSync(dest, JSON.stringify(out));
console.log(`${site}: ${items.length} pines, ${items[0].at.slice(0, 10)} → ${items[items.length - 1].at.slice(0, 10)}, ${Object.keys(boards).length} tableros → ${dest} (${Math.round(fs.statSync(dest).size / 1024)} KB)`);
console.log(Object.keys(boards).map((b) => `  /pinterest/feed/${b}.xml  →  ${boards[b]}`).join('\n'));
