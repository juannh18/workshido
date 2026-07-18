"""Convierte PNGs de worksheets a PDF de 1 página, ajustado al máximo tamaño que
quepa en A4 preservando la proporción de la imagen (sin deformar). Antes se usaba
una escala fija de 150dpi, que producía páginas más chicas que una hoja A4/Carta
real (~7x10in) e imprimía todo -incluido el texto- más pequeño de lo necesario.

Uso:
  python tools/png_to_pdf.py manifest.json            # convierte todos los del manifiesto
  python tools/png_to_pdf.py in.png out.pdf [...]     # pares explícitos

Rutas relativas se resuelven contra C:\\Users\\juand\\Downloads.
"""
import sys, os, json
import fitz

DL = r'C:\Users\juand\Downloads'
A4_WIDTH, A4_HEIGHT = 595.28, 841.89


def resolve(p):
    return p if os.path.isabs(p) else os.path.join(DL, p)


def convert(png, pdf):
    src, out = resolve(png), resolve(pdf)
    img = fitz.Pixmap(src)
    dpi = max(img.width * 72 / A4_WIDTH, img.height * 72 / A4_HEIGHT)
    doc = fitz.open()
    page = doc.new_page(width=img.width * 72 / dpi, height=img.height * 72 / dpi)
    page.insert_image(page.rect, filename=src)
    doc.save(out, deflate=True)
    d2 = fitz.open(out)
    assert len(d2) == 1 and len(d2[0].get_images()) == 1, f'PDF inválido: {out}'
    print(f'{pdf}: 1 página, {round(d2[0].rect.width)}x{round(d2[0].rect.height)}pt, {os.path.getsize(out)}b')


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 1 and args[0].endswith('.json'):
        manifest = json.load(open(args[0], encoding='utf-8'))
        pairs = [(w['png'], w['pdf']) for w in manifest['worksheets']]
    else:
        pairs = list(zip(args[::2], args[1::2]))
    if not pairs:
        sys.exit(__doc__)
    for png, pdf in pairs:
        convert(png, pdf)
