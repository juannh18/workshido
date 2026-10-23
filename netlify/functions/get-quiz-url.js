const { createClient } = require('@supabase/supabase-js');
const { S3Client, GetObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

// Same short-lived presigned links as get-teacher-edition-url.js — see the
// note there on R2_PREMIUM_BUCKET.
const R2_PUBLIC_BASE = 'https://files.workshido.com';
const R2_PREMIUM_BUCKET = process.env.R2_PREMIUM_BUCKET || 'workshido-files';
const LINK_TTL_SECONDS = 300;

const s3 = new S3Client({
  region: 'auto',
  endpoint: `https://${process.env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: process.env.R2_ACCESS_KEY_ID,
    secretAccessKey: process.env.R2_SECRET_ACCESS_KEY,
  },
});

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
    if (!quiz[column].startsWith(R2_PUBLIC_BASE + '/')) {
      return { statusCode: 500, body: JSON.stringify({ error: 'Quiz file is not an R2 file' }) };
    }

    const url = await getSignedUrl(
      s3,
      new GetObjectCommand({
        Bucket: R2_PREMIUM_BUCKET,
        Key: quiz[column].slice((R2_PUBLIC_BASE + '/').length),
        ResponseContentType: 'application/pdf',
      }),
      { expiresIn: LINK_TTL_SECONDS }
    );

    return { statusCode: 200, headers: { 'Cache-Control': 'no-store' }, body: JSON.stringify({ url }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
