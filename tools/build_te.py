"""Genera el HTML de una Teacher Edition (template v2, 2 páginas) desde un JSON de contenido.

Uso:
  python tools/build_te.py contenido.json salida.html   # salida relativa a la raíz del repo

Formato del JSON de contenido:
{
  "ws_title": "Plural Nouns &bull; Practice &bull; A1",
  "answer_key_html": "<div class='ex-title'>...</div> ...",   // columna izquierda completa
  // Nota: la línea de metadatos del Lesson Plan (pág. 2) se deriva sola de info_rows
  //       (Level/Skill/Topic/Exercises/Est. Time); no requiere campo aparte.
  "teacher_tip": "texto/html del tip",
  "mistakes": [["This is mine book.", "This is my book."], ...],   // 4 pares ✗/✓
  "activity_title": "Plural Corners (10 min)",
  "activity_body": "texto/html de la actividad",
  "info_rows": [["Level","A1"], ["Skill","Grammar"], ...],
  "materials": ["Printed worksheet copies (1 per student)", ...],
  "lesson_title": "Lesson Plan (45–50 minutes)",
  "lesson_rows": [["5 min","Warm-Up","procedimiento..."], ...],
  "followup": "texto/html",
  "support": "texto/html",
  "challenge": "texto/html",

  // --- Secciones opcionales de página 2 (RECOMENDADO llenarlas: aprovechan el
  //     espacio sobrante con info útil para el profesor; si se omiten, el bloque
  //     desaparece). Ajustar la cantidad para que la TE quede en 2 páginas exactas. ---
  "extension": ["idea 1 para quienes terminan rápido", "idea 2", ...],  // bullets (2 columnas)
  "key_language": "<b>Target:</b> ... <br><b>Board:</b> ...",           // frases clave / plan de pizarra
  "exit_ticket": "<ul class='ans'><li>...</li>...</ul>"                  // 2-3 preguntas de cierre
}

Clases CSS útiles dentro de answer_key_html: .ex-title, .ans-grid-2 + .ans-item,
ul.ans + li, .flag (notas ⚠), span.n (números).
"""
import sys, os, json, re

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)


def _strip_block(tpl, name):
    """Elimina el bloque opcional <!--NAME_START--> ... <!--NAME_END--> del template."""
    return re.sub(rf'\s*<!--{name}_START-->.*?<!--{name}_END-->', '', tpl, flags=re.DOTALL)


def build(content):
    tpl = open(os.path.join(TOOLS, 'te_template_base.html'), encoding='utf-8').read()

    mistakes = '\n'.join(
        f'      <div class="mistake-row"><span class="wrong">✗ {w}</span><br>'
        f'<span class="correct">✓ {c}</span></div>'
        for w, c in content['mistakes'])
    info_rows = '\n'.join(f'        <tr><td>{k}</td><td>{v}</td></tr>' for k, v in content['info_rows'])
    materials = '\n'.join(f'      <span>{m}</span>' for m in content['materials'])
    lesson_rows = '\n'.join(
        f'      <tr><td>{t}</td><td>{s}</td><td>{p}</td></tr>' for t, s, p in content['lesson_rows'])
    info = {k: v for k, v in content['info_rows']}
    lp_meta = '\n'.join(
        f'    <span><b>{k}:</b> {info[k]}</span>'
        for k in ('Level', 'Skill', 'Topic', 'Exercises', 'Est. Time') if k in info)

    # Envolver cada ejercicio del answer key en .ak-item para que el flujo de 2
    # columnas (.ak-flow) no parta un ejercicio a la mitad.
    segs = content['answer_key_html'].split("<div class='ex-title'>")
    answer_key = ''
    if segs[0].strip():
        answer_key += f"<div class='ak-item'>{segs[0]}</div>"
    for s in segs[1:]:
        answer_key += f"<div class='ak-item'><div class='ex-title'>{s}</div>"

    repl = {
        '{{WS_TITLE}}': content['ws_title'],
        '{{ANSWER_KEY}}': answer_key,
        '{{LP_META}}': lp_meta,
        '{{TEACHER_TIP}}': content['teacher_tip'],
        '{{MISTAKES}}': mistakes,
        '{{ACTIVITY_TITLE}}': content['activity_title'],
        '{{ACTIVITY_BODY}}': content['activity_body'],
        '{{INFO_ROWS}}': info_rows,
        '{{MATERIALS}}': materials,
        '{{LESSON_TITLE}}': content['lesson_title'],
        '{{LESSON_ROWS}}': lesson_rows,
        '{{FOLLOWUP}}': content['followup'],
        '{{SUPPORT}}': content['support'],
        '{{CHALLENGE}}': content['challenge'],
    }

    # Secciones opcionales de página 2 (llenan el espacio sobrante). Si el JSON no
    # las trae, el bloque se elimina limpiamente en vez de quedar vacío.
    if content.get('extension'):
        repl['{{EXTENSION}}'] = '\n'.join(f'      <span>{e}</span>' for e in content['extension'])
    else:
        tpl = _strip_block(tpl, 'EXTENSION')
    if content.get('key_language'):
        repl['{{KEYLANG}}'] = content['key_language']
    else:
        tpl = _strip_block(tpl, 'KEYLANG')
    if content.get('exit_ticket'):
        repl['{{EXIT_TICKET}}'] = content['exit_ticket']
    else:
        tpl = _strip_block(tpl, 'EXITTICKET')

    for k, v in repl.items():
        tpl = tpl.replace(k, v)
    assert '{{' not in tpl, 'Quedaron placeholders sin reemplazar'
    return tpl


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    content = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]
    if not os.path.isabs(out):
        out = os.path.join(REPO, out)
    html = build(content)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'OK: {out} ({len(html)} chars)')
