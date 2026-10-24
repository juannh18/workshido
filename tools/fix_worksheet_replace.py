# -*- coding: utf-8 -*-
"""Publica la versión CORREGIDA de una worksheet ya subida (ficha + miniaturas + TE) con keys NUEVOS.

Regla (26/09/2026): error encontrado en una ficha publicada → corregir ficha → rehacer TE → revisar quiz.
Keys nuevos (timestamp) en vez de sobrescribir: files.workshido.com se cachea immutable/1 año en
Cloudflare, así que reemplazar el mismo key obligaría a purgar a mano. Con key nuevo la URL cambia y
el usuario ve la versión corregida de inmediato.

Uso:
  python tools/fix_worksheet_replace.py --lang es|en --id <uuid> --pdf ficha.pdf --thumb ficha.png [--te te.pdf]
  python tools/fix_worksheet_replace.py --lang es|en --id <uuid> --te te.pdf      # solo la TE (la ficha no cambió)

Hace: sube PDF / miniatura (+ _sm) / TE con el mismo esquema de keys que upload_batch.py, PATCH de
file_url / thumbnail_url / teacher_edition_url, relee la fila y comprueba que cada archivo responde y
que su tamaño coincide con el local (PDF y miniatura por su URL pública; la TE con head_object en el
bucket privado workshido-premium, porque ya no es pública). Los objetos viejos quedan en R2 (sin
referencias); no se borran aquí.
"""
import argparse, json, os, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import upload_batch as ub  # upload_pdf, upload_thumb, resolve, R2 client, esquema de keys
import requests
from env_secrets import supabase_creds

ap = argparse.ArgumentParser()
ap.add_argument('--lang', choices=['en', 'es'], required=True)
ap.add_argument('--id', required=True)
ap.add_argument('--pdf')
ap.add_argument('--thumb')
ap.add_argument('--te')
a = ap.parse_args()
assert (a.pdf and a.thumb) or (a.te and not a.pdf and not a.thumb), 'pasar --pdf y --thumb juntos, o solo --te'

url, key = supabase_creds(a.lang)
H = {'apikey': key, 'Authorization': f'Bearer {key}'}
row = requests.get(f'{url}/rest/v1/worksheets?id=eq.{a.id}&select=id,slug,title,file_url,thumbnail_url,teacher_edition_url', headers=H).json()
assert len(row) == 1, f'no existe la worksheet {a.id}'
row = row[0]
prefix = 'es/' if a.lang == 'es' else ''
# carpeta de nivel tomada de la URL actual: .../<prefix><lf>/<ts>-<slug>.pdf
lf = row['file_url'].split(ub.R2_PUBLIC_BASE + '/')[1][len(prefix):].split('/')[0]
ts = int(datetime.now().timestamp() * 1000)
slug = row['slug']
print(f"{row['title']}\n  carpeta={lf} ts={ts}")

new = {}
if a.pdf:
    new['file_url'] = ub.upload_pdf(ub.resolve(a.pdf), f'{prefix}{lf}/{ts}-{slug}.pdf')
    new['thumbnail_url'] = ub.upload_thumb(ub.resolve(a.thumb), f'{prefix}thumbnails/{ts}-{slug}.webp')
if a.te:
    new['teacher_edition_url'] = ub.upload_pdf(ub.resolve(a.te), f'{prefix}teacher-editions/{lf}/{ts}-te_{slug}.pdf')
assert all(new.values()), f'fallo una subida: {new}'

r = requests.patch(f'{url}/rest/v1/worksheets?id=eq.{a.id}', headers={**H, 'Content-Type': 'application/json', 'Prefer': 'return=minimal'}, json=new)
assert r.status_code in (200, 204), (r.status_code, r.text[:300])

back = requests.get(f'{url}/rest/v1/worksheets?id=eq.{a.id}&select=file_url,thumbnail_url,teacher_edition_url', headers=H).json()[0]
ok = True
for k, v in new.items():
    same = back[k] == v
    if k == 'teacher_edition_url':
        # The TE has no public URL any more: check it in the private bucket.
        obj_key = v[len(ub.R2_PUBLIC_BASE) + 1:]
        head = ub.s3.head_object(Bucket=ub.bucket_for_key(obj_key), Key=obj_key)
        status, size = 200, head['ContentLength']
    else:
        resp = requests.get(v)
        status, size = resp.status_code, len(resp.content)
    size_ok = True
    if k != 'thumbnail_url':
        local = ub.resolve(a.pdf if k == 'file_url' else a.te)
        size_ok = size == os.path.getsize(local)
    sm = requests.get(v[:-5] + '_sm.webp').status_code if k == 'thumbnail_url' else 200
    good = same and status == 200 and size_ok and sm == 200
    ok &= good
    print(f"  {'OK' if good else 'XX'} {k}: {v}")
print('TODO OK' if ok else 'HAY FALLOS')
sys.exit(0 if ok else 1)
