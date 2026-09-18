"""Genera el HTML de un WORKSHEET de practica gratis (no un Quiz premium)
desde el mismo formato de JSON de contenido que build_quiz.py, pero con un
diseno propio: header con logo+wordmark ("Free Worksheet"), secciones con
barra de color (como la Teacher Edition) en vez del "letter-badge" de examen,
sin puntos ni caja de Total Score/Grade. Pensado para que un worksheet
gratuito nunca se vea identico al Full Quiz de Premium.

Uso:
  python tools/build_worksheet.py contenido.json ws_salida.html [--site spanishido]
  (misma estructura de contenido['sections'] que build_quiz.py: title,
  instructions, items_html, reading_html opcional. No usa answer_key_html
  ni bloom/points -- esos campos, si estan presentes, se ignoran aqui; la
  Teacher Edition real se genera aparte con tools/build_te.py)

--site cambia DOS ejes independientes sobre la MISMA plantilla (ver i18n.py y
brand.py): el idioma de lo que ve el alumno y la identidad de marca. Para
spanishido eso da chrome en español + paleta terracota. El contenido en si
(instrucciones, items, lecturas) va escrito en el idioma que toque dentro del
JSON; esto solo traduce las etiquetas fijas de la plantilla.
"""
import sys, os, json

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import i18n, brand

COLOR_CYCLE = ['', 'teal', 'amber', 'purple', 'green', 'red']  # '' = navy (default)


def section_html(index, title, instructions, items_html, reading_html):
    letter = chr(ord('A') + index)
    color = COLOR_CYCLE[index % len(COLOR_CYCLE)]
    cls = f'section-title {color}'.strip()
    reading = f"<div class='reading-box'>{reading_html}</div>" if reading_html else ''
    return f'''
<div class="ws-section">
  <div class="{cls}">{letter}. {title}</div>
  <div class="ws-body">
    <div class="instructions">{instructions}</div>
    {reading}
    {items_html}
  </div>
</div>'''


def build(content, site='workshido'):
    student_lang, _teacher_lang = i18n.langs_for(site)
    sections_html = ''.join(
        section_html(i, s['title'], s['instructions'], s['items_html'], s.get('reading_html'))
        for i, s in enumerate(content['sections']))

    info_map = dict(content['info_rows'])
    info_rows = '\n'.join(
        f'      <tr><td>{k}</td><td>{v}</td></tr>' for k, v in content['info_rows'] if k != 'Level')

    skills = content.get('skills', [])
    if len(skills) > 1:
        skills_text = ', '.join(skills[:-1]) + ' &amp; ' + skills[-1]
    else:
        skills_text = ''.join(skills)

    fit = content.get('fit', {})
    fit_vars = ':root{' + ';'.join(
        f'--{k.replace("_", "-")}:{v}{"px" if k in ("ans_h", "write_h", "row_gap") else ""}'
        for k, v in fit.items()) + '}' if fit else ''

    tpl = open(os.path.join(TOOLS, 'worksheet_template_base.html'), encoding='utf-8').read()
    # Idioma y marca se aplican a la PLANTILLA VACIA, antes de inyectar nada.
    # Asi el reemplazo literal no puede tocar el contenido del alumno ni el
    # base64 del logo -- solo las etiquetas y los colores de la plantilla.
    tpl = i18n.translate(tpl, student_lang)
    tpl = brand.apply(tpl, site)
    repl = {
        '{{LOGO}}': brand.logo_datauri(site),
        '{{WS_TITLE}}': content['ws_title'],
        '{{SKILLS_TEXT}}': skills_text,
        '{{LEVEL}}': info_map.get('Level', ''),
        '{{LEARNING_OBJECTIVE}}': content['learning_objective'],
        '{{INFO_ROWS}}': info_rows,
        '{{SECTIONS}}': sections_html,
        '{{FIT_VARS}}': fit_vars,
    }
    for k, v in repl.items():
        tpl = tpl.replace(k, v)
    assert '{{' not in tpl, 'Quedaron placeholders sin reemplazar en el worksheet'
    return tpl


if __name__ == '__main__':
    args = sys.argv[1:]
    site = 'workshido'
    if '--site' in args:
        i = args.index('--site')
        site = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    content = json.load(open(args[0], encoding='utf-8'))
    out = args[1]
    if not os.path.isabs(out):
        out = os.path.join(REPO, out)
    html = build(content, site)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'OK [{site}]: {out} ({len(html)} chars)')
