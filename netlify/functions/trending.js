const { createClient } = require('@supabase/supabase-js');
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

// Top 5 most-downloaded worksheets in the last 7 days, for the homepage
// "Trending this week" strip. Aggregated server-side (not a client query)
// so we never expose raw analytics_events rows to the public, and cached
// so the homepage never pays for this computation on every load.
exports.handler = async () => {
  try {
    const since = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();

    const { data: events, error: evErr } = await sb
      .from('analytics_events')
      .select('properties')
      .eq('event_name', 'download_completed')
      .gte('created_at', since);
    if (evErr) throw evErr;

    const counts = {};
    for (const e of events || []) {
      const wid = e.properties?.worksheet_id;
      if (wid) counts[wid] = (counts[wid] || 0) + 1;
    }

    const topIds = Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([id]) => id);

    if (!topIds.length) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=3600' },
        body: JSON.stringify({ items: [] }),
      };
    }

    const { data: worksheets, error: wsErr } = await sb
      .from('worksheets')
      .select('id, title, level, category, thumbnail_url')
      .in('id', topIds);
    if (wsErr) throw wsErr;

    const items = topIds
      .map(id => {
        const ws = (worksheets || []).find(w => w.id === id);
        return ws ? { ...ws, weekly_downloads: counts[id] } : null;
      })
      .filter(Boolean);

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Cache-Control': 'public, max-age=3600' },
      body: JSON.stringify({ items }),
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
