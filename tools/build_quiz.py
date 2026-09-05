"""Genera el HTML de una Evaluación (Quiz) completa desde un JSON de contenido.

Produce DOS documentos separados a partir del mismo JSON:
  1. Quiz del estudiante — listo para imprimir, SIN respuestas (quiz_template_base.html)
  2. Answer Key del profesor — respuestas + tabla de puntos (quiz_key_template_base.html)

Nunca deben ir en el mismo PDF: el quiz del estudiante debe poder imprimirse y
entregarse directamente sin riesgo de filtrar las respuestas.

Diseño pedagógico (ver memory/reference_design_manual / conversación de referencia):
cada quiz debe declarar un learning_objective explícito y cubrir varios niveles
de Bloom repartidos en secciones con dificultad progresiva. Distribución típica
de puntos: Remember/Understand ~25%, Apply ~50%, Analyze/Evaluate/Create ~25%.

Uso:
  python tools/build_quiz.py contenido.json quiz_salida.html key_salida.html
  (rutas relativas a la raíz del repo)

Formato del JSON de contenido:
{
  "ws_title": "Passive Voice – Present Simple • B1",   // Topic + Level; SIN categoría única (Grammar/Reading/...)
                                                        // porque el quiz evalúa varias destrezas a la vez
  "learning_objective": "The student identifies and correctly forms the present simple passive voice...",
  "skills": ["Grammar", "Reading", "Writing"],   // destrezas que realmente cubre el quiz (se muestran como pills)
  "info_rows": [["Level","B1"], ["Topic","Passive Voice"], ["Est. Time","40-45 min"]],
  "rubric_note": "opcional, texto/html con criterios de calificación",
  "sections": [
    {
      "title": "Vocabulary Review",       // sin numerar; el script antepone la letra (A, B, C... igual que las worksheets)
      "bloom": "Remember",                // Remember | Understand | Apply | Analyze | Evaluate | Create
      "points": 10,
      "instructions": "Match each verb to its past participle.",
      "items_html": "<div class='quiz-grid-2'>...</div>",   // HTML libre del cuerpo (preguntas EN BLANCO, sin respuestas)
      "reading_html": null                 // opcional: texto de lectura antes de items_html (ej. Reading Comprehension)
    },
    ...
  ],
  "answer_key_html": "<div class='ex-title'>1. Vocabulary Review</div>...respuestas de todas las secciones..."
}

Clases CSS útiles: .quiz-grid-2 + .q-item + .n (numeración), .mc-options (opción
inline "a. ... b. ... c. ... d. ..."), .blank (línea de espacio para completar),
.write-lines (líneas para escritura, usar <div></div> por cada renglón),
.reading-box (texto de lectura). Dentro de answer_key_html: .ex-title, .ans-grid-2
+ .ans-item, ul.ans + li, span.n, .flag (notas ⚠).
"""
import sys, os, json, re, string

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOLS)

LETTERS = list(string.ascii_uppercase)  # A, B, C... — same section-labeling convention as the worksheets


def _strip_block(tpl, name):
    return re.sub(rf'\s*<!--{name}_START-->.*?<!--{name}_END-->', '', tpl, flags=re.DOTALL)


def _wrap_answer_key(answer_key_html):
    # Igual que build_te.py: envolver cada ejercicio en .ak-item para que el
    # flujo de 2 columnas no parta un ejercicio a la mitad.
    segs = answer_key_html.split("<div class='ex-title'>")
    wrapped = ''
    if segs[0].strip():
        wrapped += f"<div class='ak-item'>{segs[0]}</div>"
    for s in segs[1:]:
        wrapped += f"<div class='ak-item'><div class='ex-title'>{s}</div>"
    return wrapped


def build(content):
    total_points = sum(s['points'] for s in content['sections'])

    sections_html = []
    rubric_rows = []
    for i, s in enumerate(content['sections'], start=1):
        letter = LETTERS[i - 1] if i <= len(LETTERS) else str(i)
        reading = f"<div class='reading-box'>{s['reading_html']}</div>" if s.get('reading_html') else ''
        sections_html.append(f'''
<div class="quiz-section">
  <div class="section-title">
    <span class="letter-badge">{letter}</span>
    <span class="title-text">{s['title']}</span>
    <span class="badge">({s['points']} points) &nbsp; Score: <span class="earn"></span></span>
  </div>
  <div class="quiz-body">
    <div class="instructions">{s['instructions']}</div>
    {reading}
    {s['items_html']}
  </div>
</div>''')
        rubric_rows.append(
            f"<tr><td>{letter}. {s['title']}</td><td>{s['bloom']}</td><td>{s['points']}</td></tr>")

    # Level ya se muestra como pill junto al título; no repetirlo en la línea de info.
    info_rows = '  '.join(f'<span><b>{k}:</b> {v}</span>' for k, v in content['info_rows'] if k != 'Level')

    info_map = dict(content['info_rows'])
    skills = content.get('skills', [])
    if len(skills) > 1:
        skills_text = ', '.join(skills[:-1]) + ' &amp; ' + skills[-1]
    else:
        skills_text = ''.join(skills)

    # --- Quiz del estudiante (sin respuestas) ---
    quiz_tpl = open(os.path.join(TOOLS, 'quiz_template_base.html'), encoding='utf-8').read()
    quiz_repl = {
        '{{WS_TITLE}}': content['ws_title'],
        '{{LEARNING_OBJECTIVE}}': content['learning_objective'],
        '{{LEVEL}}': info_map.get('Level', ''),
        '{{SKILLS_TEXT}}': skills_text,
        '{{INFO_ROWS}}': info_rows,
        '{{SECTIONS}}': '\n'.join(sections_html),
        '{{TOTAL_POINTS}}': str(total_points),
    }
    for k, v in quiz_repl.items():
        quiz_tpl = quiz_tpl.replace(k, v)
    assert '{{' not in quiz_tpl, 'Quedaron placeholders sin reemplazar en el quiz'

    # --- Answer Key del profesor ---
    key_tpl = open(os.path.join(TOOLS, 'quiz_key_template_base.html'), encoding='utf-8').read()
    key_repl = {
        '{{WS_TITLE}}': content['ws_title'],
        '{{LEVEL}}': info_map.get('Level', ''),
        '{{ANSWER_KEY}}': _wrap_answer_key(content['answer_key_html']),
        '{{RUBRIC_ROWS}}': '\n    '.join(rubric_rows),
        '{{TOTAL_POINTS}}': str(total_points),
    }
    if content.get('rubric_note'):
        key_repl['{{RUBRIC_NOTE}}'] = content['rubric_note']
    else:
        key_tpl = _strip_block(key_tpl, 'RUBRICNOTE')
    for k, v in key_repl.items():
        key_tpl = key_tpl.replace(k, v)
    assert '{{' not in key_tpl, 'Quedaron placeholders sin reemplazar en el answer key'

    return quiz_tpl, key_tpl


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    content = json.load(open(sys.argv[1], encoding='utf-8'))
    quiz_out, key_out = sys.argv[2], sys.argv[3]
    if not os.path.isabs(quiz_out):
        quiz_out = os.path.join(REPO, quiz_out)
    if not os.path.isabs(key_out):
        key_out = os.path.join(REPO, key_out)
    quiz_html, key_html = build(content)
    with open(quiz_out, 'w', encoding='utf-8') as f:
        f.write(quiz_html)
    with open(key_out, 'w', encoding='utf-8') as f:
        f.write(key_html)
    print(f'OK: {quiz_out} ({len(quiz_html)} chars)')
    print(f'OK: {key_out} ({len(key_html)} chars)')
