const { createClient } = require('@supabase/supabase-js');
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method Not Allowed' };
  try {
    const { worksheetId } = JSON.parse(event.body);
    if (!worksheetId) return { statusCode: 400, body: 'Missing worksheetId' };
    const { data } = await sb.from('worksheets').select('downloads').eq('id', worksheetId).single();
    const newCount = (data?.downloads || 0) + 1;
    await sb.from('worksheets').update({ downloads: newCount }).eq('id', worksheetId);
    return { statusCode: 200, body: JSON.stringify({ downloads: newCount }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
