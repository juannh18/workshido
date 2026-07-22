const { createClient } = require('@supabase/supabase-js');
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const SITE = 'https://workshido.com';

const STATIC_PAGES = [
  { loc: '/', changefreq: 'daily', priority: '1.0' },
  { loc: '/workshido-index.html', changefreq: 'daily', priority: '0.9' },
  { loc: '/workshido-forteachers.html', changefreq: 'weekly', priority: '0.8' },
  { loc: '/workshido-pricing.html', changefreq: 'monthly', priority: '0.7' },
  { loc: '/worksheets/grammar/', changefreq: 'weekly', priority: '0.8' },
  { loc: '/worksheets/vocabulary/', changefreq: 'weekly', priority: '0.8' },
  { loc: '/worksheets/reading/', changefreq: 'weekly', priority: '0.8' },
  { loc: '/worksheets/writing/', changefreq: 'weekly', priority: '0.8' },
  { loc: '/worksheets/levels/a1/', changefreq: 'weekly', priority: '0.8' },
  { loc: '/worksheets/levels/a2/', changefreq: 'weekly', priority: '0.8' },
  { loc: '/guides/', changefreq: 'monthly', priority: '0.7' },
  { loc: '/guides/how-to-teach-present-simple/', changefreq: 'monthly', priority: '0.6' },
  { loc: '/guides/cefr-levels-guide/', changefreq: 'monthly', priority: '0.6' },
  { loc: '/guides/esl-warm-up-activities/', changefreq: 'monthly', priority: '0.6' },
  { loc: '/workshido-privacy.html', changefreq: 'yearly', priority: '0.3' },
  { loc: '/workshido-terms.html', changefreq: 'yearly', priority: '0.3' },
];

function escapeXml(s) {
  return String(s).replace(/[<>&'"]/g, (c) => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;', "'": '&apos;', '"': '&quot;' }[c]));
}

exports.handler = async () => {
  try {
    const { data: worksheets, error } = await sb
      .from('worksheets')
      .select('id, created_at')
      .order('created_at', { ascending: false });

    if (error) throw error;

    const staticEntries = STATIC_PAGES.map(p => `  <url>
    <loc>${SITE}${p.loc}</loc>
    <changefreq>${p.changefreq}</changefreq>
    <priority>${p.priority}</priority>
  </url>`);

    const worksheetEntries = (worksheets || []).map(ws => {
      const lastmod = ws.created_at ? new Date(ws.created_at).toISOString().slice(0, 10) : '';
      return `  <url>
    <loc>${SITE}/workshido-worksheet.html?id=${escapeXml(ws.id)}</loc>${lastmod ? `\n    <lastmod>${lastmod}</lastmod>` : ''}
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>`;
    });

    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${[...staticEntries, ...worksheetEntries].join('\n')}
</urlset>
`;

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/xml; charset=utf-8',
        'Cache-Control': 'public, max-age=3600',
      },
      body: xml,
    };
  } catch (err) {
    return { statusCode: 500, body: 'Sitemap generation error: ' + err.message };
  }
};
