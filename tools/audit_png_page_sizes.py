"""Audita el catálogo de worksheets subidos: para cada fila con file_url, descarga
el PDF y reporta si es un PDF de una sola imagen (PNG-based, generado con
tools/png_to_pdf.py) y si su página es más chica que A4 (candidato a regenerar
con el fit-A4 nuevo).

Uso:
  python tools/audit_png_page_sizes.py

Escribe el resultado en tools/manifest.json bajo la clave "png_audit" (no se
sobreescribe el resto del archivo si ya existe).
"""
import sys, io, json, os
import pip_system_certs.wrapt_requests  # noqa: usa el almacén de certificados de Windows en vez de desactivar la verificación TLS
import requests, fitz

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from env_secrets import SUPABASE_URL, SERVICE_KEY

H = {'apikey': SERVICE_KEY, 'Authorization': f'Bearer {SERVICE_KEY}'}

A4_WIDTH, A4_HEIGHT = 595.28, 841.89
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    rows = []
    offset = 0
    page_size = 200
    while True:
        res = requests.get(
            f'{SUPABASE_URL}/rest/v1/worksheets',
            headers=H,
            params={'select': 'id,title,file_url,category,tags',
                     'order': 'created_at.asc',
                     'limit': str(page_size), 'offset': str(offset)},
            )
        batch = res.json()
        if not isinstance(batch, list) or not batch:
            break
        rows.extend(batch)
        if len(batch) < page_size:
            break
        offset += page_size

    print(f'{len(rows)} worksheets en total\n')
    png_based = []
    for r in rows:
        url = r.get('file_url')
        if not url:
            continue
        try:
            d = requests.get(url, timeout=30)
            doc = fitz.open(stream=io.BytesIO(d.content), filetype='pdf')
        except Exception as e:
            print(f'ERROR {r["title"]}: {e}')
            continue
        page = doc[0]
        imgs = page.get_images()
        text_len = len(page.get_text().strip())
        is_png_based = len(doc) == 1 and len(imgs) == 1 and text_len == 0
        w, h = page.rect.width, page.rect.height
        smaller_than_a4 = w < A4_WIDTH - 5 or h < A4_HEIGHT - 5
        if is_png_based:
            status = 'CHICO' if smaller_than_a4 else 'ok'
            print(f'[PNG {status}] {r["title"]} | {round(w)}x{round(h)}pt ({round(w/72,2)}x{round(h/72,2)}in) | {url}')
            if smaller_than_a4:
                png_based.append({'id': r['id'], 'title': r['title'], 'file_url': url,
                                   'width': w, 'height': h})
        else:
            print(f'[HTML/otro] {r["title"]}')

    print(f'\n{len(png_based)} worksheets PNG-based más chicos que A4 (candidatos a regenerar)')

    manifest_path = os.path.join(REPO, 'tools', 'png_audit.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump({'candidates': png_based}, f, indent=2, ensure_ascii=False)
    print(f'Guardado: {manifest_path}')

if __name__ == '__main__':
    main()
