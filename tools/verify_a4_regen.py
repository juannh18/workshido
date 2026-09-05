"""Verifica el resultado de tools/regenerate_png_pdfs_a4.py: re-descarga cada PDF
desde su URL pública y confirma que el tamaño de página coincide con lo esperado
(log 'new'), que sigue teniendo exactamente 1 imagen y 1 página.

Uso:
  python tools/verify_a4_regen.py tools/regenerate_a4_log.json
"""
import sys, io, json, time
import pip_system_certs.wrapt_requests  # noqa: usa el almacén de certificados de Windows en vez de desactivar la verificación TLS
import requests, fitz


def get_with_retry(url, tries=3):
    last = None
    for _ in range(tries):
        try:
            return requests.get(url, timeout=30)
        except Exception as e:
            last = e
            time.sleep(2)
    raise last


def main(log_path):
    entries = json.load(open(log_path, encoding='utf-8'))
    problems = 0
    for e in entries:
        if e['status'] != 'ok':
            print(f'SKIP (ya marcado error en regen): {e["title"]}')
            problems += 1
            continue
        try:
            d = get_with_retry(e['file_url'])
        except Exception as ex:
            print(f'PROBLEMA {e["title"]}: {ex}')
            problems += 1
            continue
        if d.status_code != 200:
            print(f'PROBLEMA {e["title"]}: HTTP {d.status_code}')
            problems += 1
            continue
        doc = fitz.open(stream=io.BytesIO(d.content), filetype='pdf')
        w, h = doc[0].rect.width, doc[0].rect.height
        exp_w, exp_h = e['new']
        ok = (len(doc) == 1 and len(doc[0].get_images()) == 1
              and abs(w - exp_w) < 1 and abs(h - exp_h) < 1)
        if not ok:
            print(f'PROBLEMA {e["title"]}: esperado {exp_w}x{exp_h}, real {w}x{h}, '
                  f'paginas={len(doc)}, imgs={len(doc[0].get_images())}')
            problems += 1
    print(f'\n{len(entries) - problems}/{len(entries)} verificados OK')
    return problems


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(1 if main(sys.argv[1]) else 0)
