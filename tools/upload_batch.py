"""Sube un lote de worksheets a R2 (archivos) + Supabase (metadata) desde un manifiesto JSON.

Uso:
  python tools/upload_batch.py manifest.json

Formato del manifiesto (rutas relativas: PDFs/PNGs contra Downloads):
{
  "worksheets": [
    {
      "slug": "pluralnounspracticea1",
      "pdf": "pluralnounspracticea1.pdf",
      "thumb": "Pluralnounspracticeworksheeta1.png",
      "te_pdf": "te_pluralnouns_practice_a1.pdf",     // opcional (null = sin TE)
      "te_html": "te_pluralnouns_practice_a1.html",   // solo lo usa html_to_pdf_cdp.py
      "title": "Plural Nouns – Practice Worksheet",
      "level": "A1",
      "category": "Grammar",
      "tags": "worksheet, plural nouns, ...",          // 'worksheet' SIEMPRE primero
      "description": "..."
    }
  ]
}

Reglas fijas: is_free siempre True; tag 'worksheet' primero (se valida).
Después de subir, correr tools/verify_uploads.py N para confirmar desde las URLs públicas.

Requiere: pip install boto3
Nota: R2_PUBLIC_BASE asume que files.workshido.com ya está apuntando al bucket R2
(Fase 3 de la migración). Si el dominio custom todavía no está activo, las URLs
que este script genera no van a cargar hasta que se complete ese paso.
"""
import pip_system_certs.wrapt_requests  # noqa: usa el almacén de certificados de Windows en vez de desactivar la verificación TLS
import requests, boto3, os, uuid, io, json, sys
from datetime import datetime
from botocore.config import Config
from PIL import Image

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from env_secrets import SUPABASE_URL, SERVICE_KEY, R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY

HEADERS_AUTH = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
}

R2_BUCKET = 'workshido-files'
R2_PUBLIC_BASE = 'https://files.workshido.com'

s3 = boto3.client(
    's3',
    endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name='auto',
    config=Config(signature_version='s3v4'),
)

DL = r'C:\Users\juand\Downloads'

def resolve(p):
    return p if os.path.isabs(p) else os.path.join(DL, p)

def check_r2_domain():
    """Aborta si files.workshido.com todavía no resuelve (dominio custom de R2, Fase 3
    de la migración) — evita subir worksheets nuevas con links rotos."""
    try:
        requests.head(R2_PUBLIC_BASE, timeout=5)
    except requests.RequestException:
        sys.exit(
            f'ERROR: {R2_PUBLIC_BASE} no responde todavia.\n'
            'El dominio custom de R2 (files.workshido.com) todavia no esta activo.\n'
            'No subas worksheets nuevas hasta completar ese paso, o quedaran con links rotos.'
        )

def upload_pdf(local_path, storage_path):
    try:
        s3.upload_file(local_path, R2_BUCKET, storage_path, ExtraArgs={
            'ContentType': 'application/pdf',
            'CacheControl': 'public, max-age=31536000, immutable',
        })
    except Exception as e:
        print(f'  ERROR PDF upload: {e}')
        return None
    return f'{R2_PUBLIC_BASE}/{storage_path}'

THUMB_MAX_WIDTH = 640  # catalog cards render thumbnails at ~217-320px wide;
                        # 640px covers 2x/retina without shipping full A4-page
                        # resolution (1055x1491) for a ~300px card image.

def upload_thumb(local_path, storage_path):
    img = Image.open(local_path).convert('RGB')
    if img.width > THUMB_MAX_WIDTH:
        ratio = THUMB_MAX_WIDTH / img.width
        img = img.resize((THUMB_MAX_WIDTH, round(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'WEBP', quality=88)
    buf.seek(0)
    try:
        s3.put_object(
            Bucket=R2_BUCKET, Key=storage_path, Body=buf.read(),
            ContentType='image/webp', CacheControl='public, max-age=31536000, immutable',
        )
    except Exception as e:
        print(f'  ERROR thumb upload: {e}')
        return None
    return f'{R2_PUBLIC_BASE}/{storage_path}'

def insert_worksheet(record):
    res = requests.post(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers={**HEADERS_AUTH, 'Content-Type': 'application/json', 'Prefer': 'return=representation'},
        json=record
    )
    return res.status_code, res.text[:300]

def main(manifest_path):
    check_r2_domain()
    manifest = json.load(open(manifest_path, encoding='utf-8'))
    for ws in manifest['worksheets']:
        assert ws['tags'].startswith('worksheet'), f"{ws['slug']}: el tag 'worksheet' debe ir primero"

    level_folder_default = manifest.get('level_folder', 'a1')
    for ws in manifest['worksheets']:
        ts = int(datetime.now().timestamp() * 1000)
        lf = ws.get('level_folder', level_folder_default)
        print(f'\n{"="*60}')
        print(f'Uploading: {ws["title"]}')

        pdf_url = upload_pdf(resolve(ws['pdf']), f'{lf}/{ts}-{ws["slug"]}.pdf')
        if not pdf_url:
            continue
        print('  OK: PDF uploaded')

        thumb_url = upload_thumb(resolve(ws['thumb']), f'thumbnails/{ts}-{ws["slug"]}.webp')
        if not thumb_url:
            continue
        print('  OK: Thumbnail uploaded')

        te_url = None
        if ws.get('te_pdf'):
            te_url = upload_pdf(resolve(ws['te_pdf']), f'teacher-editions/{lf}/{ts}-te_{ws["slug"]}.pdf')
            print('  OK: Teacher Edition uploaded' if te_url else '  WARNING: TE upload failed, continuing without it')

        record = {
            'id': str(uuid.uuid4()),
            'title': ws['title'],
            'level': ws['level'],
            'category': ws['category'],
            'tags': ws['tags'],
            'description': ws['description'],
            'file_url': pdf_url,
            'thumbnail_url': thumb_url,
            'teacher_edition_url': te_url,
            'is_free': True,   # regla fija: todas las worksheets son gratis
            'downloads': 0,
        }
        status, text = insert_worksheet(record)
        if status in (200, 201):
            print('  OK: DB record inserted')
        else:
            print(f'  ERROR DB insert: {status} {text}')

    print(f'\n{"="*60}')
    print('Done!')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
