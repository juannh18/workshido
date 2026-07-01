const SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co';
const SUPABASE_KEY = 'sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo';

async function fetchJSON(url, opts) {
  const res = await fetch(url, opts);
  const text = await res.text();
  if (!res.ok) throw new Error(`${res.status}: ${text}`);
  return text ? JSON.parse(text) : null;
}

async function run() {
  // Fetch all worksheets
  const worksheets = await fetchJSON(
    `${SUPABASE_URL}/rest/v1/worksheets?select=id,tags`,
    { headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}` } }
  );

  console.log(`Found ${worksheets.length} worksheets`);
  let updated = 0, skipped = 0;

  for (const ws of worksheets) {
    const tags = (ws.tags || '').toLowerCase();
    if (tags.includes('worksheet')) { skipped++; continue; }

    const newTags = ws.tags ? `worksheet, ${ws.tags}` : 'worksheet';
    const res = await fetch(
      `${SUPABASE_URL}/rest/v1/worksheets?id=eq.${ws.id}`,
      {
        method: 'PATCH',
        headers: {
          apikey: SUPABASE_KEY,
          Authorization: `Bearer ${SUPABASE_KEY}`,
          'Content-Type': 'application/json',
          Prefer: 'return=minimal'
        },
        body: JSON.stringify({ tags: newTags })
      }
    );
    if (res.ok) { updated++; console.log(`  Updated: ${ws.id}`); }
    else console.warn(`  FAIL: ${ws.id} — ${await res.text()}`);
  }

  console.log(`\nDone. Updated: ${updated} | Already had tag: ${skipped}`);
}

run().catch(console.error);
