const { createClient } = require('@supabase/supabase-js');
const { S3Client, GetObjectCommand } = require('@aws-sdk/client-s3');
const { getSignedUrl } = require('@aws-sdk/s3-request-presigner');

// Why this exists: the "Download free" button used to do a cross-origin
// fetch() of the PDF from files.workshido.com, turn it into a Blob, and
// click an <a download>. That breaks whenever the browser can't complete the
// cross-origin fetch — ad blockers / tracking protection that block requests
// to a different subdomain, a stale CDN response missing the per-Origin CORS
// header, corporate proxies — and the old code then fell back to
// window.open(), which just renders the PDF in a new tab instead of saving.
//
// This endpoint is hit SAME-ORIGIN (workshido.com -> workshido.com), so that
// class of failure disappears. It returns a short-lived R2 presigned URL that
// carries response-content-disposition=attachment, so navigating to it
// downloads the file directly (works on iOS/Safari too, which can't force a
// Blob download). Bytes still stream straight from R2 — $0 egress — the
// function only returns a ~1 KB JSON payload with the URL.

const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

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

// ASCII-safe filename for the Content-Disposition header (no smart dashes,
// no path separators, no quotes).
function safeFilename(title) {
  const base = (title || 'worksheet')
    .normalize('NFKD')
    .replace(/[‐-―]/g, '-')      // hyphens / en/em dashes -> "-"
    .replace(/[^\x20-\x7E]/g, '')           // drop remaining non-ASCII
    .replace(/["\\/:*?<>|]+/g, '')          // filesystem-unsafe
    .replace(/\s+/g, ' ')
    .trim();
  return (base || 'worksheet') + '.pdf';
}

exports.handler = async (event) => {
  const token = (event.headers.authorization || event.headers.Authorization || '').replace('Bearer ', '');
  if (!token) return { statusCode: 401, body: JSON.stringify({ error: 'Not authenticated' }) };

  try {
    const { data: { user }, error: userErr } = await sb.auth.getUser(token);
    if (userErr || !user) return { statusCode: 401, body: JSON.stringify({ error: 'Invalid session' }) };

    const id = (event.queryStringParameters || {}).id;
    if (!id) return { statusCode: 400, body: JSON.stringify({ error: 'Missing id' }) };

    const { data: ws, error } = await sb
      .from('worksheets')
      .select('title, file_url')
      .eq('id', id)
      .single();
    if (error || !ws || !ws.file_url) {
      return { statusCode: 404, body: JSON.stringify({ error: 'Worksheet not found' }) };
    }
    if (!ws.file_url.startsWith(R2_PUBLIC_BASE + '/')) {
      // Legacy Supabase-hosted file (pre-R2). Nothing to presign — let the
      // client fall back to its old path.
      return { statusCode: 409, body: JSON.stringify({ error: 'Not an R2 file', file_url: ws.file_url }) };
    }

    const key = ws.file_url.slice((R2_PUBLIC_BASE + '/').length);
    const url = await getSignedUrl(
      s3,
      new GetObjectCommand({
        Bucket: R2_BUCKET,
        Key: key,
        ResponseContentDisposition: `attachment; filename="${safeFilename(ws.title)}"`,
        ResponseContentType: 'application/pdf',
      }),
      { expiresIn: 300 }
    );

    return {
      statusCode: 200,
      headers: { 'Cache-Control': 'no-store' },
      body: JSON.stringify({ url }),
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
