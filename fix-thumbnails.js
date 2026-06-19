// Script para generar miniaturas de worksheets que no tienen thumbnail_url
// Ejecutar con: node fix-thumbnails.js

const SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co';
const SUPABASE_KEY = 'sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo';
const THUMBNAIL_SERVICE = 'https://workshido-thumbnail-service.onrender.com';

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  return res.json();
}

async function getWorksheetsWithoutThumbnail() {
  // Trae todos y filtra los que tienen URL de Cloudinary (thumbnails viejos) o null
  const data = await fetchJSON(
    `${SUPABASE_URL}/rest/v1/worksheets?select=id,title,file_url,file_type,thumbnail_url`,
    { headers: { apikey: SUPABASE_KEY, Authorization: `Bearer ${SUPABASE_KEY}` } }
  );
  return data.filter(ws =>
    !ws.thumbnail_url || ws.thumbnail_url.includes('cloudinary.com')
  );
}

async function generateThumbnail(fileUrl, fileName) {
  const fileRes = await fetch(fileUrl);
  if (!fileRes.ok) throw new Error(`No se pudo descargar el archivo: ${fileUrl}`);
  const blob = await fileRes.blob();

  const formData = new FormData();
  formData.append('file', blob, fileName);

  const res = await fetch(`${THUMBNAIL_SERVICE}/generate-thumbnail`, {
    method: 'POST',
    body: formData
  });

  if (!res.ok) throw new Error(`Thumbnail service error: ${await res.text()}`);
  const data = await res.json();
  if (!data.thumbnailUrl) throw new Error('No thumbnailUrl en la respuesta');
  return data.thumbnailUrl;
}

async function updateThumbnail(id, thumbnailUrl) {
  const res = await fetch(
    `${SUPABASE_URL}/rest/v1/worksheets?id=eq.${id}`,
    {
      method: 'PATCH',
      headers: {
        apikey: SUPABASE_KEY,
        Authorization: `Bearer ${SUPABASE_KEY}`,
        'Content-Type': 'application/json',
        Prefer: 'return=minimal'
      },
      body: JSON.stringify({ thumbnail_url: thumbnailUrl })
    }
  );
  if (!res.ok) throw new Error(`DB error ${res.status}: ${await res.text()}`);
}

async function main() {
  console.log('Buscando worksheets sin miniatura...');
  const worksheets = await getWorksheetsWithoutThumbnail();

  if (worksheets.length === 0) {
    console.log('✅ Todos los worksheets ya tienen miniatura.');
    return;
  }

  console.log(`Encontrados ${worksheets.length} worksheets sin miniatura.\n`);

  for (const ws of worksheets) {
    const ext = ws.file_url.split('.').pop().split('?')[0].toLowerCase();
    const fileName = `${ws.id}.${ext}`;
    process.stdout.write(`Procesando: ${ws.title} ... `);
    try {
      const thumbnailUrl = await generateThumbnail(ws.file_url, fileName);
      await updateThumbnail(ws.id, thumbnailUrl);
      console.log(`✅ OK`);
    } catch (e) {
      console.log(`❌ Error: ${e.message}`);
    }
  }

  console.log('\n¡Listo! Recarga el catálogo en workshido.com');
}

main().catch(console.error);
