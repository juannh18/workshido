const { createClient } = require('@supabase/supabase-js');
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method Not Allowed' };

  const token = (event.headers.authorization || event.headers.Authorization || '').replace('Bearer ', '');
  if (!token) return { statusCode: 401, body: JSON.stringify({ error: 'Not authenticated' }) };

  try {
    const { data: { user }, error: userErr } = await sb.auth.getUser(token);
    if (userErr || !user) return { statusCode: 401, body: JSON.stringify({ error: 'Invalid session' }) };

    const { data: profile } = await sb.from('profiles').select('is_premium').eq('id', user.id).single();
    if (!profile?.is_premium) return { statusCode: 403, body: JSON.stringify({ error: 'Premium required' }) };

    const { worksheetId } = JSON.parse(event.body);
    if (!worksheetId) return { statusCode: 400, body: JSON.stringify({ error: 'Missing worksheetId' }) };

    const { data: ws } = await sb.from('worksheets').select('teacher_edition_url').eq('id', worksheetId).single();
    if (!ws?.teacher_edition_url) return { statusCode: 404, body: JSON.stringify({ error: 'No Teacher Edition for this worksheet' }) };

    return { statusCode: 200, body: JSON.stringify({ url: ws.teacher_edition_url }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
