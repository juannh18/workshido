"""Reemplaza in-place archivos de worksheets en R2 (mismo key => misma URL publica => no toca la DB).

Uso: python tools/ws_replace_upload.py <manifest.json>
manifest: { "items": [ {"slug","pdf","thumb","te_pdf","pdf_key","thumb_key","te_key"} ] }
Rutas locales absolutas o relativas a la raiz del repo. te_pdf/te_key opcionales.
"""
import sys, os, json
import pip_system_certs.wrapt_requests  # noqa: usa el store de certs de Windows
import boto3
from botocore.config import Config

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from env_secrets import R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY

R2_BUCKET = 'workshido-files'
s3 = boto3.client(
    's3', endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
    aws_access_key_id=R2_ACCESS_KEY_ID, aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name='auto', config=Config(signature_version='s3v4'))

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rp(p): return p if os.path.isabs(p) else os.path.join(REPO, p)

def head(key):
    try:
        return s3.head_object(Bucket=R2_BUCKET, Key=key)['ContentLength']
    except Exception:
        return None

def put(local, key, ctype):
    before = head(key)
    with open(rp(local), 'rb') as f:
        data = f.read()
    s3.put_object(Bucket=R2_BUCKET, Key=key, Body=data, ContentType=ctype,
                  CacheControl='public, max-age=31536000, immutable')
    after = head(key)
    ok = after == len(data)
    print(f"    {key}\n      {before} -> {after} bytes (local {len(data)})  {'OK' if ok else 'MISMATCH!'}")
    return ok

def main(mf):
    m = json.load(open(mf, encoding='utf-8'))
    allok = True
    for it in m['items']:
        print(f"\n=== {it['slug']}")
        if it.get('pdf'):    allok &= put(it['pdf'], it['pdf_key'], 'application/pdf')
        if it.get('thumb'):  allok &= put(it['thumb'], it['thumb_key'], 'image/webp')
        if it.get('te_pdf'): allok &= put(it['te_pdf'], it['te_key'], 'application/pdf')
    print("\n" + ("ALL OK" if allok else "SOME MISMATCH - REVISAR"))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
