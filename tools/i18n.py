# -*- coding: utf-8 -*-
"""Etiquetas traducibles de las plantillas (worksheet / quiz / TE).

POR QUE UN DICCIONARIO Y NO PLANTILLAS *_es.html DUPLICADAS
----------------------------------------------------------
Las plantillas inglesas se siguen mejorando (el 13/09 se rediseño
worksheet_template_base.html entero). Una copia traducida se habria quedado
atras en silencio. Y el costo escala mal: N plantillas x M idiomas archivos
que mantener, contra N plantillas + M columnas aqui.

DOS EJES, NO UNO
----------------
El idioma no es una sola decision. Cada mercado combina dos:

  * student_lang -> lo que ve el ALUMNO (la ficha).
  * teacher_lang -> lo que lee el PROFESOR (Teacher Edition, answer key del
                    quiz) y donde vive el SEO (titulos, descripciones, sitio).

Spanishido hoy es student=es / teacher=en: el alumno recibe español (norma en
ELE: Aula, Bitacora, Gente), pero quien compra es un profe de EE. UU. que
busca en Google en ingles ("ser vs estar worksheet") y lee su lesson plan en
ingles. Mañana, si se le vende a profes de España o LATAM, es UN valor en
SITES lo que cambia, no una tanda de plantillas nuevas.

COMO AGREGAR UN IDIOMA
----------------------
1. Agregar su columna a cada entrada de STRINGS.
2. Agregar la fila del mercado a SITES.
3. Correr `python tools/i18n.py` (se autoverifica: falla si falta una etiqueta).
No se toca ninguna plantilla.
"""
import sys

# Mercados. student = idioma de la ficha del alumno; teacher = idioma de la
# Teacher Edition, el answer key y el sitio (donde vive el SEO).
SITES = {
    'workshido':  {'student': 'en', 'teacher': 'en'},   # ingles como L2
    'spanishido': {'student': 'es', 'teacher': 'en'},   # ELE para profes de EE. UU.
}

# Las plantillas se escriben en INGLES; la clave es el literal ingles tal como
# aparece en el HTML ya construido. El valor por idioma es su reemplazo.
# No hace falta ordenarlas: translate() aplica primero las mas largas, para que
# "Score" no destroce "Total Score".
STRINGS = {
    # --- atributo de idioma del documento (accesibilidad + hyphenation) ---
    '<html lang="en">':                {'es': '<html lang="es">'},

    # --- encabezado / tarjeta del alumno ---
    '<div class="eyebrow">Quiz</div>': {'es': '<div class="eyebrow">Evaluación</div>'},
    '>Free Worksheet<':                {'es': '>Ficha gratuita<'},
    '<label>Name</label>':             {'es': '<label>Nombre</label>'},
    '<label>Class</label>':            {'es': '<label>Clase</label>'},
    '<label>Date</label>':             {'es': '<label>Fecha</label>'},
    '<label>Score</label>':            {'es': '<label>Puntuación</label>'},
    '<span>Name</span>':               {'es': '<span>Nombre</span>'},
    '<span>Class</span>':              {'es': '<span>Clase</span>'},
    '<span>Date</span>':               {'es': '<span>Fecha</span>'},

    # --- bloques de informacion ---
    'Learning Objective':              {'es': 'Objetivo de aprendizaje'},
    'Worksheet Info':                  {'es': 'Datos de la ficha'},

    # --- pie y puntuacion ---
    '<span class="label">Total Score</span>': {'es': '<span class="label">Puntuación total</span>'},
    'Grade:':                          {'es': 'Nota:'},
    '&bull;&nbsp; Free Worksheet':     {'es': '&bull;&nbsp; Ficha gratuita'},

    # --- generadas en codigo por build_quiz.py, no en la plantilla ---
    ' points)':                        {'es': ' puntos)'},
    'Score: <span class="earn">':      {'es': 'Puntos: <span class="earn">'},
}

LANGS = ['en'] + sorted({lang for v in STRINGS.values() for lang in v})


def translate(html, lang):
    """Traduce el HTML ya construido. 'en' lo devuelve intacto (es el original).

    Falla ruidosamente ante un idioma sin traducir: una ficha a medio traducir
    llegando al alumno es peor que un build que se cae.
    """
    if lang == 'en':
        return html
    if lang not in LANGS:
        raise ValueError('idioma %r sin traducciones en STRINGS' % lang)
    faltan = [k for k, v in STRINGS.items() if lang not in v]
    if faltan:
        raise ValueError('faltan %d etiquetas en %r: %s' % (len(faltan), lang, faltan[:3]))
    for en in sorted(STRINGS, key=len, reverse=True):   # largas primero
        html = html.replace(en, STRINGS[en][lang])
    return html


def langs_for(site):
    """('es', 'en') para spanishido: idioma del alumno, idioma del profesor."""
    if site not in SITES:
        raise ValueError('sitio %r desconocido; agregalo a SITES' % site)
    s = SITES[site]
    return s['student'], s['teacher']


if __name__ == '__main__':
    # Autoverificacion: que ningun idioma quede a medias.
    for lang in LANGS:
        translate('', lang)
    for site, cfg in SITES.items():
        print('%-12s alumno=%s  profesor=%s' % (site, cfg['student'], cfg['teacher']))
    print('OK: %d etiquetas x %d idiomas' % (len(STRINGS), len(LANGS)))
