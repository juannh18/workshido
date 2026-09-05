"""Backfill puntual: convierte a WEBP los ultimos thumbnails que quedaron en
PNG (7 de 683 al 04/09/2026 -- el resto ya se sube como WEBP desde
upload_batch.py, ver THUMB_MAX_WIDTH/upload_thumb ahi).

A diferencia de resize_existing_thumbnails.py (pre-R2, hacia upsert al mismo
path en Supabase Storage), esto sube a una key NUEVA en R2 (mismo bucket,
extension .webp) y despues actualiza thumbnail_url en la tabla worksheets,
porque el path viejo termina en .png y R2 no permite "renombrar" un objeto.

Uso:
  python tools/backfill_png_thumbnails.py           # aplica el cambio
  python tools/backfill_png_thumbnails.py --dry-run # solo muestra que haria
"""
import sys, os, io, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pip_system_certs.wrapt_requests  # noqa: usa el almacen de certificados de Windows
import requests
from PIL import Image
from upload_batch import s3, R2_BUCKET, R2_PUBLIC_BASE, THUMB_MAX_WIDTH, SUPABASE_URL, HEADERS_AUTH


def main(dry_run=False):
    r = requests.get(
        f'{SUPABASE_URL}/rest/v1/worksheets?select=id,title,thumbnail_url&thumbnail_url=ilike.*.png*',
        headers=HEADERS_AUTH)
    rows = r.json()
    print(f'{len(rows)} filas con thumbnail PNG')

    done = failed = 0
    for i, row in enumerate(rows, 1):
        url = row['thumbnail_url']
        try:
            img_res = requests.get(url, timeout=30)
            img_res.raise_for_status()
            img = Image.open(io.BytesIO(img_res.content)).convert('RGB')
        except Exception as e:
            print(f'[{i}/{len(rows)}] ERROR descargando {row["title"]}: {e}')
            failed += 1
            continue

        if img.width > THUMB_MAX_WIDTH:
            ratio = THUMB_MAX_WIDTH / img.width
            img = img.resize((THUMB_MAX_WIDTH, round(img.height * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, 'WEBP', quality=88)
        new_size = buf.tell()
        buf.seek(0)

        new_key = f"thumbnails/{row['id']}.webp"
        new_url = f'{R2_PUBLIC_BASE}/{new_key}'

        if dry_run:
            print(f'[{i}/{len(rows)}] DRY-RUN {row["title"]}: {len(img_res.content)}b -> {new_size}b -> {new_url}')
            continue

        try:
            s3.put_object(
                Bucket=R2_BUCKET, Key=new_key, Body=buf.read(),
                ContentType='image/webp', CacheControl='public, max-age=31536000, immutable',
            )
        except Exception as e:
            print(f'[{i}/{len(rows)}] ERROR subiendo {row["title"]}: {e}')
            failed += 1
            continue

        patch = requests.patch(
            f'{SUPABASE_URL}/rest/v1/worksheets?id=eq.{row["id"]}',
            headers={**HEADERS_AUTH, 'Content-Type': 'application/json', 'Prefer': 'return=minimal'},
            json={'thumbnail_url': new_url})
        if patch.status_code not in (200, 204):
            print(f'[{i}/{len(rows)}] ERROR actualizando DB {row["title"]}: {patch.status_code} {patch.text[:150]}')
            failed += 1
            continue

        print(f'[{i}/{len(rows)}] OK {row["title"]}: {len(img_res.content)}b -> {new_size}b')
        done += 1

    print(f'\nHecho. Convertidas: {done}  Fallidas: {failed}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    main(args.dry_run)
