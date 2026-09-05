"""Redimensiona en el sitio las miniaturas ya subidas (bug: upload_batch.py
subia el WEBP a resolucion completa 1055x1491, ~130-250KB, sin cache-control
largo). Descarga cada thumbnail_url publico, la reduce a THUMB_MAX_WIDTH
preservando proporcion, y la re-sube al MISMO storage path (upsert) con
Cache-Control inmutable -- no toca file_url/teacher_edition_url ni la fila
en la tabla, la URL publica no cambia.

Uso:
  python tools/resize_existing_thumbnails.py           # todas las filas
  python tools/resize_existing_thumbnails.py --limit 5  # prueba con pocas
"""
import sys, os, io, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pip_system_certs.wrapt_requests  # noqa: usa el almacén de certificados de Windows en vez de desactivar la verificación TLS
import requests
from PIL import Image
from upload_batch import SUPABASE_URL, SERVICE_KEY, HEADERS_AUTH

THUMB_MAX_WIDTH = 640


def main(limit=None):
    r = requests.get(
        f'{SUPABASE_URL}/rest/v1/worksheets?select=id,title,thumbnail_url&thumbnail_url=not.is.null&order=created_at.desc',
        headers=HEADERS_AUTH)
    rows = r.json()
    if limit:
        rows = rows[:limit]
    print(f'{len(rows)} filas con thumbnail_url')

    resized = skipped = failed = 0
    for i, row in enumerate(rows, 1):
        url = row['thumbnail_url']
        path = url.split('/worksheets/')[-1] if '/worksheets/' in url else None
        if not path:
            print(f'[{i}/{len(rows)}] SKIP (path raro): {url}')
            skipped += 1
            continue
        try:
            img_res = requests.get(url, timeout=30)
            img_res.raise_for_status()
            img = Image.open(io.BytesIO(img_res.content)).convert('RGB')
        except Exception as e:
            print(f'[{i}/{len(rows)}] ERROR descargando {row["title"]}: {e}')
            failed += 1
            continue

        if img.width <= THUMB_MAX_WIDTH:
            skipped += 1
            continue

        ratio = THUMB_MAX_WIDTH / img.width
        img = img.resize((THUMB_MAX_WIDTH, round(img.height * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, 'WEBP', quality=88)
        new_size = buf.tell()
        buf.seek(0)

        up = requests.post(
            f'{SUPABASE_URL}/storage/v1/object/worksheets/{path}',
            headers={**HEADERS_AUTH, 'Content-Type': 'image/webp', 'x-upsert': 'true',
                      'Cache-Control': 'public, max-age=31536000, immutable'},
            data=buf.read())
        if up.status_code not in (200, 201):
            print(f'[{i}/{len(rows)}] ERROR subiendo {row["title"]}: {up.status_code} {up.text[:150]}')
            failed += 1
            continue

        print(f'[{i}/{len(rows)}] OK {row["title"]}: {len(img_res.content)}b -> {new_size}b')
        resized += 1

    print(f'\nHecho. Redimensionadas: {resized}  Ya OK/omitidas: {skipped}  Fallidas: {failed}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=None)
    args = ap.parse_args()
    main(args.limit)
