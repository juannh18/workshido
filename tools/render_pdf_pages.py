"""Renderiza todas las páginas de uno o más PDFs a PNG para verificación visual.

Uso:
  python tools/render_pdf_pages.py salida_dir archivo1.pdf [archivo2.pdf ...]

PDFs relativos se resuelven contra Downloads. Imprime el conteo de páginas de cada PDF.
"""
import sys, os
import fitz

DL = r'C:\Users\juand\Downloads'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    for p in sys.argv[2:]:
        path = p if os.path.isabs(p) else os.path.join(DL, p)
        d = fitz.open(path)
        base = os.path.splitext(os.path.basename(p))[0]
        print(f'{os.path.basename(p)} -> {len(d)} páginas')
        for i in range(len(d)):
            d[i].get_pixmap(dpi=55).save(os.path.join(out_dir, f'{base}_p{i+1}.png'))
