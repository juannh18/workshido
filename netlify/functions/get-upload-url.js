const { createClient } = require('@supabase/supabase-js');
const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');

const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const ADMIN_EMAIL = 'juanda.5790@hotmail.com';
const R2_BUCKET = 'workshido-files';
const R2_PUBLIC_BASE = 'https://files.workshido.com';

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
    if (user.email !== ADMIN_EMAIL) return { statusCode: 403, body: JSON.stringify({ error: 'Not allowed' }) };

    const { path, contentType } = JSON.parse(event.body);
    if (!path || !contentType) return { statusCode: 400, body: JSON.stringify({ error: 'Missing path or contentType' }) };

    const command = new PutObjectCommand({ Bucket: R2_BUCKET, Key: path, ContentType: contentType });
    const uploadUrl = await getSignedUrl(s3, command, { expiresIn: 300 });

    return { statusCode: 200, body: JSON.stringify({ uploadUrl, publicUrl: `${R2_PUBLIC_BASE}/${path}` }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
