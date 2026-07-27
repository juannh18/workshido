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

    const m = quiz[column].match(/\/object\/(?:public|sign)\/([^/]+)\/([^?]+)/);
    if (!m) return { statusCode: 500, body: JSON.stringify({ error: 'Unexpected file path' }) };

    const { data: signed, error: signErr } = await sb.storage.from(m[1]).createSignedUrl(m[2], 60);
    if (signErr || !signed) return { statusCode: 500, body: JSON.stringify({ error: 'Could not sign URL' }) };

    return { statusCode: 200, body: JSON.stringify({ url: signed.signedUrl }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
