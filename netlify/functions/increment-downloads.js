const { createClient } = require('@supabase/supabase-js');
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method Not Allowed' };

  const token = (event.headers.authorization || event.headers.Authorization || '').replace('Bearer ', '');
  if (!token) return { statusCode: 401, body: 'Not authenticated' };
  const { data: { user }, error: userErr } = await sb.auth.getUser(token);
  if (userErr || !user) return { statusCode: 401, body: 'Invalid session' };

  try {
    const { worksheetId } = JSON.parse(event.body);
    if (!worksheetId) return { statusCode: 400, body: 'Missing worksheetId' };
    // Atomic increment (single UPDATE ... RETURNING in Postgres) — avoids the
    // lost-update race of a separate read-then-write under concurrent requests.
    const { data: newCount, error } = await sb.rpc('increment_downloads', { ws_id: worksheetId });
    if (error) throw error;
    return { statusCode: 200, body: JSON.stringify({ downloads: newCount }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
