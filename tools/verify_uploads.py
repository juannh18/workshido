"""Verifica los últimos N worksheets subidos re-descargándolos desde las URLs públicas.

Uso:
  python tools/verify_uploads.py [N] [--es]     # default N=6; --es = esquema es (Spanishido)

Chequea por cada fila: status 200 de PDF/thumb/TE, tag 'worksheet' primero,
páginas del PDF (imagen presente) y del TE (2 páginas, marca WORKSHIDO/SPANISHIDO).
Correr con PYTHONIOENCODING=utf-8 si la consola es cp1252.
"""
import sys, io
import pip_system_certs.wrapt_requests  # noqa: usa el almacén de certificados de Windows en vez de desactivar la verificación TLS
import requests, fitz

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from env_secrets import SUPABASE_URL, SERVICE_KEY

H = {'apikey': SERVICE_KEY, 'Authorization': f'Bearer {SERVICE_KEY}'}

def main(n, es=False):
    headers = {**H, 'Accept-Profile': 'es'} if es else H
    res = requests.get(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers=headers,
        params={'select': 'title,file_url,thumbnail_url,teacher_edition_url,is_free,category,tags',
                'order': 'created_at.desc', 'limit': str(n)})
    rows = res.json()
    print(f'{len(rows)} filas mas recientes:\n')
    problems = 0
    for r in rows:
        print('*', r['title'], '| cat:', r['category'], '| free:', r['is_free'])
        if not r['tags'].startswith('worksheet'):
            print("   PROBLEMA: tag 'worksheet' no va primero")
            problems += 1
        for label, url in [('pdf', r['file_url']), ('thumb', r['thumbnail_url']), ('te', r['teacher_edition_url'])]:
            if not url:
                print(f'   {label}: (sin url)')
                continue
            d = requests.get(url)
            info = f'{d.status_code} {len(d.content)}b'
            ok = d.status_code == 200
            if label in ('pdf', 'te') and ok:
                doc = fitz.open(stream=io.BytesIO(d.content), filetype='pdf')
                info += f' pages={len(doc)}'
                if label == 'te':
                    txt = doc[0].get_text()[:40].replace('\n', ' ')
                    info += f' text="{txt}"'
                    brand = 'SPANISHIDO' if es else 'WORKSHIDO'
                    ok = len(doc) == 2 and brand in txt.upper()
                else:
                    info += f' imgs={len(doc[0].get_images())}'
                    ok = len(doc[0].get_images()) >= 1
            if not ok:
                info += '  <-- PROBLEMA'
                problems += 1
            print(f'   {label}: {info}')
        print()
    print('TODO OK' if problems == 0 else f'{problems} PROBLEMAS ENCONTRADOS')
    return problems

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--es']
    es = '--es' in sys.argv
    n = int(args[0]) if args else 6
    sys.exit(1 if main(n, es) else 0)
