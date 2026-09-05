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

    const { quizId, kind } = JSON.parse(event.body);
    if (!quizId) return { statusCode: 400, body: JSON.stringify({ error: 'Missing quizId' }) };
    const column = kind === 'key' ? 'key_pdf_url' : 'quiz_pdf_url';

    const { data: quiz } = await sb.from('quizzes').select(column).eq('id', quizId).single();
    if (!quiz?.[column]) return { statusCode: 404, body: JSON.stringify({ error: 'No quiz file found' }) };

    return { statusCode: 200, body: JSON.stringify({ url: quiz[column] }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
