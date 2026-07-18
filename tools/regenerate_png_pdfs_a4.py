"""Regenera in-place los PDFs de worksheets PNG-based que quedaron más chicos que
A4 (ver tools/audit_png_page_sizes.py -> tools/png_audit.json), sin tocar diseño:
descarga el PDF actual, extrae la imagen embebida (misma imagen, sin recomprimir
con pérdida), la reinserta en una página del tamaño máximo que quepa en A4
preservando proporción (mismo criterio que el nuevo tools/png_to_pdf.py), y sube
el PDF resultante al MISMO storage path (upsert) -> no cambia file_url ni requiere
tocar la fila en la tabla worksheets.

Uso:
  python tools/regenerate_png_pdfs_a4.py tools/png_audit.json

Escribe un log de resultados en tools/regenerate_a4_log.json.
"""
import sys, io, json, os, time
import requests, fitz, urllib3
urllib3.disable_warnings()

SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co'
SERVICE_KEY  = 'REDACTED_SUPABASE_SERVICE_KEY'
HEADERS_AUTH = {'apikey': SERVICE_KEY, 'Authorization': f'Bearer {SERVICE_KEY}'}

A4_WIDTH, A4_HEIGHT = 595.28, 841.89
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def storage_path_from_url(url):
    marker = '/public/worksheets/'
    i = url.index(marker)
    return url[i + len(marker):]


def download(url, tries=3):
    last = None
    for _ in range(tries):
        try:
            d = requests.get(url, verify=False, timeout=30)
            if d.status_code == 200:
                return d.content
            last = f'HTTP {d.status_code}'
        except Exception as e:
            last = str(e)
        time.sleep(2)
    raise RuntimeError(last)


def regenerate(pdf_bytes):
    doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype='pdf')
    page = doc[0]
    imgs = page.get_images()
    xref = imgs[0][0]
    base = doc.extract_image(xref)
    img_bytes, ext = base['image'], base['ext']
    pix = fitz.Pixmap(io.BytesIO(img_bytes))
    dpi = max(pix.width * 72 / A4_WIDTH, pix.height * 72 / A4_HEIGHT)
    new_doc = fitz.open()
    new_page = new_doc.new_page(width=pix.width * 72 / dpi, height=pix.height * 72 / dpi)
    new_page.insert_image(new_page.rect, stream=img_bytes)
    out = io.BytesIO()
    new_doc.save(out, deflate=True)
    return out.getvalue(), new_page.rect.width, new_page.rect.height


def upload(pdf_bytes, storage_path, tries=3):
    last = None
    for _ in range(tries):
        try:
            res = requests.post(
                f'{SUPABASE_URL}/storage/v1/object/worksheets/{storage_path}',
                headers={**HEADERS_AUTH, 'Content-Type': 'application/pdf', 'x-upsert': 'true'},
                data=pdf_bytes, verify=False, timeout=30)
            if res.status_code in (200, 201):
                return True
            last = f'HTTP {res.status_code} {res.text[:200]}'
        except Exception as e:
            last = str(e)
        time.sleep(2)
    raise RuntimeError(last)


def main(audit_path):
    audit = json.load(open(audit_path, encoding='utf-8'))
    candidates = audit['candidates']
    print(f'{len(candidates)} worksheets a regenerar\n')

    results = []
    for i, c in enumerate(candidates, 1):
        title, url = c['title'], c['file_url']
        try:
            pdf_bytes = download(url)
            old_w, old_h = c['width'], c['height']
            new_bytes, new_w, new_h = regenerate(pdf_bytes)
            storage_path = storage_path_from_url(url)
            upload(new_bytes, storage_path)
            growth = round((new_w * new_h) / (old_w * old_h) * 100 - 100)
            print(f'[{i}/{len(candidates)}] OK {title}: '
                  f'{round(old_w)}x{round(old_h)} -> {round(new_w)}x{round(new_h)}pt (+{growth}% area)')
            results.append({'id': c['id'], 'title': title, 'file_url': url, 'status': 'ok',
                             'old': [old_w, old_h], 'new': [new_w, new_h]})
        except Exception as e:
            print(f'[{i}/{len(candidates)}] ERROR {title}: {e}')
            results.append({'id': c['id'], 'title': title, 'file_url': url, 'status': 'error',
                             'error': str(e)})

    ok = sum(1 for r in results if r['status'] == 'ok')
    err = len(results) - ok
    print(f'\n{ok} OK, {err} errores')
    log_path = os.path.join(REPO, 'tools', 'regenerate_a4_log.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f'Log: {log_path}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
