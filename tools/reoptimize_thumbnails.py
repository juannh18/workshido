"""Re-optimiza las miniaturas ya subidas en R2 (audit ChatGPT 08/09/2026:
se sirven a 640x904 ~92KB WEBP q88 para mostrarse a ~200-360px en las
tarjetas del catalogo). Baja ancho a TARGET_WIDTH y calidad a TARGET_Q,
re-sube al MISMO key en R2 (misma URL publica -> NO toca la tabla
worksheets). Requiere purga manual de Cloudflare despues (files.workshido.com
esta cacheado immutable/1 anio).

  python tools/reoptimize_thumbnails.py --dry-run          # solo reporta tamanos proyectados
  python tools/reoptimize_thumbnails.py --limit 3          # procesa 3 de verdad (prueba)
  python tools/reoptimize_thumbnails.py                    # todas

Idempotente: salta las que ya esten <= TARGET_WIDTH y no mejoren >=10%.
"""
import sys, os, io, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pip_system_certs.wrapt_requests  # noqa: cert store de Windows
import requests
import boto3
from botocore.config import Config
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env_secrets import (SUPABASE_URL, SERVICE_KEY, R2_ACCOUNT_ID,
                         R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY)

HEADERS_AUTH = {'apikey': SERVICE_KEY, 'Authorization': f'Bearer {SERVICE_KEY}'}
R2_BUCKET = 'workshido-files'
R2_PUBLIC_BASE = 'https://files.workshido.com'

TARGET_WIDTH = 500          # ~2x para tarjetas de ~250px; el preview de la
TARGET_Q = 78               # ficha lo muestra a ~1x-1.3x (aceptable, no es el PDF)
MIN_GAIN = 0.10             # si el nuevo pesa > 90% del viejo, no vale la pena

s3 = boto3.client(
    's3', endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
    aws_access_key_id=R2_ACCESS_KEY_ID, aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name='auto', config=Config(signature_version='s3v4'))


def key_from_url(url):
    """https://files.workshido.com/thumbnails/xxx.webp -> thumbnails/xxx.webp"""
    if not url or R2_PUBLIC_BASE not in url:
        return None
    return url.split(R2_PUBLIC_BASE + '/', 1)[-1].split('?', 1)[0]


def main(limit=None, dry=False):
    r = requests.get(
        f'{SUPABASE_URL}/rest/v1/worksheets'
        f'?select=id,title,thumbnail_url&thumbnail_url=not.is.null&order=created_at.desc',
        headers=HEADERS_AUTH, timeout=30)
    r.raise_for_status()
    rows = r.json()
    if limit:
        rows = rows[:limit]
    print(f'{len(rows)} filas con thumbnail_url  (target {TARGET_WIDTH}px q{TARGET_Q}, dry={dry})\n')

    done = skip = fail = 0
    tot_before = tot_after = 0
    for i, row in enumerate(rows, 1):
        key = key_from_url(row['thumbnail_url'])
        tag = f'[{i}/{len(rows)}] {row["title"][:44]}'
        if not key:
            print(f'{tag}  SKIP (url no-R2: {row["thumbnail_url"][:60]})'); skip += 1; continue
        try:
            obj = s3.get_object(Bucket=R2_BUCKET, Key=key)
            src = obj['Body'].read()
            im = Image.open(io.BytesIO(src)).convert('RGB')
        except Exception as e:
            print(f'{tag}  ERROR get {key}: {e}'); fail += 1; continue

        w0, h0 = im.size
        if im.width > TARGET_WIDTH:
            ratio = TARGET_WIDTH / im.width
            im = im.resize((TARGET_WIDTH, round(im.height * ratio)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=TARGET_Q, method=6)
        new = buf.getvalue()

        gain = 1 - len(new) / len(src)
        line = (f'{tag}  {w0}x{h0} {len(src)/1024:.0f}KB -> '
                f'{im.size[0]}x{im.size[1]} {len(new)/1024:.0f}KB  ({gain*100:+.0f}%)')
        if gain < MIN_GAIN:
            print(line + '  skip (poca ganancia)'); skip += 1; continue
        tot_before += len(src); tot_after += len(new)
        if dry:
            print(line + '  [dry]'); done += 1; continue

        try:
            s3.put_object(Bucket=R2_BUCKET, Key=key, Body=new, ContentType='image/webp',
                          CacheControl='public, max-age=31536000, immutable')
            got = s3.head_object(Bucket=R2_BUCKET, Key=key)['ContentLength']
        except Exception as e:
            print(line + f'  ERROR put: {e}'); fail += 1; continue
        ok = got == len(new)
        print(line + ('  OK' if ok else f'  MISMATCH (r2={got})'))
        done += 1 if ok else 0
        fail += 0 if ok else 1

    print(f'\nHecho. Procesadas: {done}  Omitidas: {skip}  Fallidas: {fail}')
    if tot_before:
        print(f'Peso miniaturas afectadas: {tot_before/1024:.0f} KB -> {tot_after/1024:.0f} KB '
              f'({(1-tot_after/tot_before)*100:.0f}% menos)')
    if not dry and done:
        print('\n>> PURGAR Cloudflare (files.workshido.com) para que los usuarios reciban las nuevas.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--dry-run', dest='dry', action='store_true')
    a = ap.parse_args()
    main(a.limit, a.dry)
