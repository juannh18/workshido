# -*- coding: utf-8 -*-
"""Identidad de marca por sitio para las plantillas de PDF (worksheet / quiz / TE).

Separado de i18n.py a proposito: marca e idioma son ejes distintos y no se
mueven juntos. Spanishido cambia los dos; un futuro "Workshido UK" cambiaria
solo la marca; vender ELE a profes de España cambiaria solo el idioma.

Las plantillas se escriben con los valores de Workshido (marron = navy, etc.).
apply() hace reemplazo literal de esos valores por los del sitio pedido, igual
que i18n.translate(). No hay plantillas duplicadas.

Los hex de Spanishido estan copiados TAL CUAL del CSS del fork (los 6 mas
usados); no son reinterpretaciones ni tonos "parecidos" elegidos por mi.
"""
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))


def _logo(fname):
    return open(os.path.join(TOOLS, 'te_output', fname), encoding='utf-8').read().strip()


BRANDS = {
    'workshido': {
        'domain': 'workshido.com',
        'logo_file': '_logo_datauri.txt',
        'wordmark': 'Work<span class="brand-accent">shido</span>',
        'alt': 'Workshido',
        # dark, accent, edition, card_bg, card_border
        'colors': None,          # la plantilla ya viene en estos valores
        'section_cycle': None,
    },
    'spanishido': {
        'domain': 'spanishido.com',
        'logo_file': '_logo_datauri_es.txt',
        'wordmark': 'Spanish<span class="brand-accent">ido</span>',
        'alt': 'Spanishido',
        'colors': {
            '#1a3a5c': '#3B160A',   # oscuro primario: borde, titulos, barra default
            '#6ea8dc': '#EFAD86',   # acento claro del wordmark
            '#e67e22': '#A6401D',   # naranja "FICHA GRATUITA" + barra ambar
            '#f5f8fb': '#FBEDE5',   # fondo de las tarjetas del panel
            '#dbe4ee': '#F6CBB0',   # borde de esas tarjetas
        },
        # Barras de seccion. Solo hex de la paleta del fork, y elegidos para que
        # dos barras CONSECUTIVAS nunca queden casi iguales: la paleta de
        # Spanishido es casi monocroma calida, asi que marron-sobre-marron se
        # lee como un error de impresion. El orden real del ciclo es
        # default, teal, amber, purple, green, red (ver COLOR_CYCLE).
        'section_cycle': {
            '#0e7c66': '#534AB7',   # teal   -> morado de marca (rompe el marron)
            '#7b2d8b': '#5C2A12',   # purple -> marron medio
            '#1e8449': '#64230E',   # green  -> marron rojizo
            '#c0392b': '#A6401D',   # red    -> terracota (sin esto se colaba el rojo de Workshido)
        },
    },
}


def apply(html, site):
    """Aplica marca al HTML ya construido. 'workshido' lo devuelve intacto."""
    if site not in BRANDS:
        raise ValueError('sitio %r desconocido; agregalo a BRANDS' % site)
    b = BRANDS[site]
    if site == 'workshido':
        return html
    for en, es in (b.get('colors') or {}).items():
        html = html.replace(en, es)
    for en, es in (b.get('section_cycle') or {}).items():
        html = html.replace(en, es)
    html = html.replace('Work<span class="brand-accent">shido</span>', b['wordmark'])
    html = html.replace('alt="Workshido"', 'alt="%s"' % b['alt'])
    html = html.replace('workshido.com', b['domain'])
    # La plantilla de la Teacher Edition trae el logo incrustado en base64 (una
    # vez por cabecera de pagina), no un placeholder {{LOGO}} como la de
    # worksheet. En esa no hay nada que reemplazar y esto es un no-op.
    html = html.replace(_logo(BRANDS['workshido']['logo_file']), logo_datauri(site))
    return html


def logo_datauri(site):
    return _logo(BRANDS[site]['logo_file'])


if __name__ == '__main__':
    for site, b in BRANDS.items():
        print('%-12s %-16s logo=%d chars' % (site, b['domain'], len(logo_datauri(site))))
