const SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co';
const SUPABASE_KEY = 'sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo';

fetch(`${SUPABASE_URL}/rest/v1/worksheets?select=id,title,thumbnail_url&limit=20`, {
  headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}` }
})
.then(r => r.json())
.then(data => data.forEach(ws => console.log(`${ws.title}: ${ws.thumbnail_url || '(vacío)'}`)))
.catch(console.error);
