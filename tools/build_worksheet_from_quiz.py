"""Reusa build_quiz.py (mismo HTML/CSS 'premium' de las evaluaciones) para
generar un WORKSHEET de practica GRATIS en vez de un Quiz de la tabla
`quizzes`. El Quiz completo es una feature de Premium, asi que el worksheet
NO puede verse identico: se le quita todo lo que se lee como "examen
puntuado" (badge de puntos por seccion, caja de Total Score/Grade) y el
eyebrow pasa de 'Quiz' a la destreza principal del worksheet.

Uso:
  python tools/build_worksheet_from_quiz.py contenido.json ws_salida.html te_key_salida.html
  (el segundo archivo es el answer-key con el mismo diseno premium; se usa
  solo como referencia interna, la Teacher Edition real se genera aparte
  con tools/build_te.py)
"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_quiz

REPO = build_quiz.REPO


def de_quizify(html):
    # Quita el badge "(N points)  Score: ___" de cada seccion.
    html = re.sub(
        r'<span class="badge">\(\d+ points\)[^<]*<span class="earn"></span></span>',
        '', html)
    # Quita la caja de Total Score / Grade al final.
    html = re.sub(r'<div class="total-score-box">.*?</div>\s*', '', html, flags=re.DOTALL)
    # Quita la columna "Score" del encabezado Name/Class/Date/Score y pasa la
    # tarjeta a 3 columnas (un worksheet gratis no es un examen calificado).
    html = html.replace(
        '<div class="student-card">\n  <div><label>Name</label></div>\n  <div><label>Class</label></div>\n  <div><label>Date</label></div>\n  <div><label>Score</label></div>\n</div>',
        '<div class="student-card" style="grid-template-columns:2.2fr 0.9fr 1.5fr">\n  <div><label>Name</label></div>\n  <div><label>Class</label></div>\n  <div><label>Date</label></div>\n</div>')
    return html


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    content = json.load(open(sys.argv[1], encoding='utf-8'))
    ws_out, key_out = sys.argv[2], sys.argv[3]
    if not os.path.isabs(ws_out):
        ws_out = os.path.join(REPO, ws_out)
    if not os.path.isabs(key_out):
        key_out = os.path.join(REPO, key_out)

    ws_html, key_html = build_quiz.build(content)
    eyebrow = content.get('skills', ['Grammar'])[0] + ' Worksheet'
    ws_html = ws_html.replace('<div class="eyebrow">Quiz</div>', f'<div class="eyebrow">{eyebrow}</div>', 1)
    ws_html = de_quizify(ws_html)

    with open(ws_out, 'w', encoding='utf-8') as f:
        f.write(ws_html)
    with open(key_out, 'w', encoding='utf-8') as f:
        f.write(key_html)
    print(f'OK: {ws_out} ({len(ws_html)} chars)')
    print(f'OK: {key_out} ({len(key_html)} chars)')
