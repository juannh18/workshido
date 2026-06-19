exports.handler = async function(event) {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') return { statusCode: 200, headers, body: '' };
  if (event.httpMethod !== 'POST') return { statusCode: 405, headers, body: 'Method not allowed' };

  const CLOUDCONVERT_KEY = process.env.CLOUDCONVERT_KEY;
  const CLOUDINARY_CLOUD = 'dbx9boxvu';
  const CLOUDINARY_PRESET = 'workshido';

  try {
    const body = JSON.parse(event.body);
    const { fileBase64, fileName } = body;

    // 1. Crear job y loguear respuesta completa
    const jobRes = await fetch('https://api.cloudconvert.com/v2/jobs', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${CLOUDCONVERT_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        tasks: {
          'import-file': {
            operation: 'import/base64',
            file: fileBase64,
            filename: fileName
          },
          'convert-file': {
            operation: 'convert',
            input: 'import-file',
            output_format: 'png',
            pages: '1',
            pixel_density: 150,
            width: 800
          },
          'export-file': {
            operation: 'export/url',
            input: 'convert-file'
          }
        }
      })
    });

    const rawText = await jobRes.text();
    console.log('CloudConvert raw response:', rawText.substring(0, 500));
    
    const jobData = JSON.parse(rawText);
    
    if (!jobData.data) {
      throw new Error('No data in response: ' + rawText.substring(0, 200));
    }
    
    const jobId = jobData.data.id;
    console.log('Job ID:', jobId);

    // 2. Polling
    let pngUrl = null;
    for (let i = 0; i < 30; i++) {
      await new Promise(r => setTimeout(r, 2000));
      
      const statusRes = await fetch(`https://api.cloudconvert.com/v2/jobs/${jobId}`, {
        headers: { 'Authorization': `Bearer ${CLOUDCONVERT_KEY}` }
      });
      const statusText = await statusRes.text();
      console.log(`Poll ${i}:`, statusText.substring(0, 300));
      
      const statusData = JSON.parse(statusText);
      const jobStatus = statusData?.data?.status;

      if (jobStatus === 'finished') {
        const tasks = statusData.data.tasks;
        console.log('Tasks type:', typeof tasks, Array.isArray(tasks));
        const tasksArray = Array.isArray(tasks) ? tasks : Object.values(tasks || {});
        const exportTask = tasksArray.find(t => t.operation === 'export/url');
        pngUrl = exportTask?.result?.files?.[0]?.url;
        break;
      }
      if (jobStatus === 'error') throw new Error('Conversion error');
    }

    if (!pngUrl) throw new Error('No PNG URL obtained');

    // 3. Subir a Cloudinary
    const pngRes = await fetch(pngUrl);
    const pngBuffer = await pngRes.arrayBuffer();
    const pngBase64out = Buffer.from(pngBuffer).toString('base64');

    const cloudRes = await fetch(`https://api.cloudinary.com/v1_1/${CLOUDINARY_CLOUD}/image/upload`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        file: `data:image/png;base64,${pngBase64out}`,
        upload_preset: CLOUDINARY_PRESET
      })
    });

    const cloudData = await cloudRes.json();
    if (!cloudData.secure_url) throw new Error('Cloudinary error: ' + JSON.stringify(cloudData).substring(0,100));

    return { statusCode: 200, headers, body: JSON.stringify({ thumbnailUrl: cloudData.secure_url }) };

  } catch (err) {
    console.error('FINAL ERROR:', err.message);
    return { statusCode: 500, headers, body: JSON.stringify({ error: err.message }) };
  }
};
