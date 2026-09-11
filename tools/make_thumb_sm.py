"""Genera una version chica (_sm) de cada miniatura para las TARJETAS del
catalogo/home/relacionadas (audit ChatGPT 08/09/2026: las tarjetas cargan la
miniatura de 640px/~92KB para mostrarla a 200-360px).

ADITIVO: crea un key NUEVO en R2 (thumbnails/X_sm.webp) a partir de la
miniatura actual. NO toca la miniatura grande (que sigue usando el preview
de la ficha) ni la tabla worksheets. Como el key es nuevo, NO hace falta
purgar Cloudflare.

  python tools/make_thumb_sm.py --dry-run        # solo reporta
  python tools/make_thumb_sm.py --limit 3        # procesa 3 (prueba)
  python tools/make_thumb_sm.py                  # todas (salta las que ya tienen _sm)
  python tools/make_thumb_sm.py --force          # regenera aunque ya exista
"""
import sys, os, io, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pip_system_certs.wrapt_requests  # noqa
import requests
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env_secrets import (SUPABASE_URL, SERVICE_KEY, R2_ACCOUNT_ID,
                         R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY)

HEADERS_AUTH = {'apikey': SERVICE_KEY, 'Authorization': f'Bearer {SERVICE_KEY}'}
R2_BUCKET = 'workshido-files'
R2_PUBLIC_BASE = 'https://files.workshido.com'

SM_WIDTH = 440      # tarjetas del catalogo van de ~150 a ~280px; 440 cubre
SM_Q = 74           # retina 2x en la mayoria sin volver a mandar 640px/92KB

s3 = boto3.client(
    's3', endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
    aws_access_key_id=R2_ACCESS_KEY_ID, aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name='auto', config=Config(signature_version='s3v4'))


def key_from_url(url):
    if not url or R2_PUBLIC_BASE not in url:
        return None
    return url.split(R2_PUBLIC_BASE + '/', 1)[-1].split('?', 1)[0]


def sm_key(key):
    """thumbnails/abc.webp -> thumbnails/abc_sm.webp  (solo si es .webp)"""
    if not key or not key.lower().endswith('.webp'):
        return None
    return key[:-5] + '_sm.webp'


def exists(key):
    try:
        s3.head_object(Bucket=R2_BUCKET, Key=key)
        return True
    except ClientError:
        return False


def main(limit=None, dry=False, force=False):
    r = requests.get(
        f'{SUPABASE_URL}/rest/v1/worksheets'
        f'?select=id,title,thumbnail_url&thumbnail_url=not.is.null&order=created_at.desc',
        headers=HEADERS_AUTH, timeout=30)
    r.raise_for_status()
    rows = r.json()
    if limit:
        rows = rows[:limit]
    print(f'{len(rows)} filas  (target _sm {SM_WIDTH}px q{SM_Q}, dry={dry}, force={force})\n')

    made = skip = fail = 0
    tot_big = tot_sm = 0
    for i, row in enumerate(rows, 1):
        tag = f'[{i}/{len(rows)}] {row["title"][:44]}'
        key = key_from_url(row['thumbnail_url'])
        skey = sm_key(key)
        if not skey:
            print(f'{tag}  SKIP (no .webp/R2: {row["thumbnail_url"][:55]})'); skip += 1; continue
        if not force and exists(skey):
            skip += 1; continue
        try:
            src = s3.get_object(Bucket=R2_BUCKET, Key=key)['Body'].read()
            im = Image.open(io.BytesIO(src)).convert('RGB')
        except Exception as e:
            print(f'{tag}  ERROR get {key}: {e}'); fail += 1; continue

        if im.width > SM_WIDTH:
            im = im.resize((SM_WIDTH, round(im.height * SM_WIDTH / im.width)), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=SM_Q, method=6)
        new = buf.getvalue()
        tot_big += len(src); tot_sm += len(new)
        line = f'{tag}  {len(src)/1024:.0f}KB -> _sm {im.size[0]}x{im.size[1]} {len(new)/1024:.0f}KB'
        if dry:
            print(line + '  [dry]'); made += 1; continue
        try:
            s3.put_object(Bucket=R2_BUCKET, Key=skey, Body=new, ContentType='image/webp',
                          CacheControl='public, max-age=31536000, immutable')
            got = s3.head_object(Bucket=R2_BUCKET, Key=skey)['ContentLength']
        except Exception as e:
            print(line + f'  ERROR put: {e}'); fail += 1; continue
        ok = got == len(new)
        print(line + ('  OK' if ok else f'  MISMATCH r2={got}'))
        made += 1 if ok else 0
        fail += 0 if ok else 1

    print(f'\nHecho. Creadas: {made}  Omitidas (ya existian / no-webp): {skip}  Fallidas: {fail}')
    if tot_big:
        print(f'Por tarjeta: {tot_big/max(made,1)/1024:.0f}KB -> {tot_sm/max(made,1)/1024:.0f}KB aprox')
    print('\nNo hace falta purgar Cloudflare (keys nuevos).')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=None)
    ap.add_argument('--dry-run', dest='dry', action='store_true')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    main(a.limit, a.dry, a.force)
