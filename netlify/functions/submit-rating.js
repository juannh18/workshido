const { createClient } = require('@supabase/supabase-js');
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method Not Allowed' };
  try {
    const { worksheetId, rating } = JSON.parse(event.body);
    if (!worksheetId || !rating || rating < 1 || rating > 5)
      return { statusCode: 400, body: 'Invalid data' };
    const { data } = await sb.from('worksheets').select('rating, ratings_count').eq('id', worksheetId).single();
    const count = (data?.ratings_count || 0) + 1;
    const avg = (((data?.rating || 0) * (count - 1)) + rating) / count;
    await sb.from('worksheets').update({ rating: avg, ratings_count: count }).eq('id', worksheetId);
    return { statusCode: 200, body: JSON.stringify({ rating: avg, ratings_count: count }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
