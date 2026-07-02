"""Sube un lote de worksheets a Supabase desde un manifiesto JSON.

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
"""
import requests, os, uuid, io, json, sys
from datetime import datetime
from PIL import Image

SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co'
SERVICE_KEY  = 'REDACTED_SUPABASE_SERVICE_KEY'

HEADERS_AUTH = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
}

DL = r'C:\Users\juand\Downloads'


def resolve(p):
    return p if os.path.isabs(p) else os.path.join(DL, p)


def upload_pdf(local_path, storage_path):
    with open(local_path, 'rb') as f:
        res = requests.post(
            f'{SUPABASE_URL}/storage/v1/object/worksheets/{storage_path}',
            headers={**HEADERS_AUTH, 'Content-Type': 'application/pdf', 'x-upsert': 'true'},
            data=f, verify=False
        )
    if res.status_code not in (200, 201):
        print(f'  ERROR PDF upload: {res.status_code} {res.text[:200]}')
        return None
    return f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{storage_path}'


def upload_thumb(local_path, storage_path):
    img = Image.open(local_path)
    buf = io.BytesIO()
    img.save(buf, 'WEBP', quality=88)
    buf.seek(0)
    res = requests.post(
        f'{SUPABASE_URL}/storage/v1/object/worksheets/{storage_path}',
        headers={**HEADERS_AUTH, 'Content-Type': 'image/webp', 'x-upsert': 'true'},
        data=buf.read(), verify=False
    )
    if res.status_code not in (200, 201):
        print(f'  ERROR thumb upload: {res.status_code} {res.text[:200]}')
        return None
    return f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{storage_path}'


def insert_worksheet(record):
    res = requests.post(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers={**HEADERS_AUTH, 'Content-Type': 'application/json', 'Prefer': 'return=representation'},
        json=record, verify=False
    )
    return res.status_code, res.text[:300]


def main(manifest_path):
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
