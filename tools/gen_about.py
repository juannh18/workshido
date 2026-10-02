"""Genera /about/ (estándares editoriales: quién hace las fichas y cómo) para
Workshido y Spanishido. Auditoría SEO/marketing 02/10/2026: faltaba la capa
E-E-A-T — /about/ daba 404 y las guías firmaban solo "Workshido".

Reutiliza el esqueleto de una guía real de cada sitio (nav, footer, CSS,
guides-auth.js) para no duplicar plantillas: se reemplazan <head> SEO, JSON-LD,
breadcrumb y <main>. Firma: "<Marca> Editorial Team" (decisión de Juan, 02/10).

Todo lo que dice la página tiene que ser verdad: describe el pipeline real
(CLAUDE.md, pasos de revisión de PNG/TE). Nada de credenciales inventadas.

Uso:  python tools/gen_about.py
"""
import json
import os
import re

DESKTOP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SITES = {
    'workshido': {
        'root': os.path.join(DESKTOP, 'Workshido'),
        'shell': 'guides/how-to-teach-verb-to-be/index.html',
        'brand': 'Workshido',
        'domain': 'https://workshido.com',
        'subject': 'English',
        'audience': 'teachers of A1–B2 English (ESL/EFL) classes',
        'levels': 'A1, A2, B1 or B2',
        'catalog': '/workshido-index.html',
        'pricing': '/workshido-pricing.html',
        'sequence_guide': '/guides/how-to-sequence-esl-lessons/',
        'cefr_guide': '/guides/cefr-levels-guide/',
        'contact': 'hello@workshido.com',
        'language_note': '',
    },
    'spanishido': {
        'root': os.path.join(DESKTOP, 'Spanishido'),
        'shell': 'guides/how-to-teach-ser-vs-estar/index.html',
        'brand': 'Spanishido',
        'domain': 'https://spanishido.com',
        'subject': 'Spanish',
        'audience': 'teachers of Spanish as a foreign language (ELE), starting at A1–A2',
        'levels': 'A1 or A2 (more levels are on the way)',
        'catalog': '/spanishido-index.html',
        'pricing': '/spanishido-pricing.html',
        'sequence_guide': '/guides/how-to-sequence-spanish-lessons/',
        'cefr_guide': None,
        'contact': 'hello@spanishido.com',
        'language_note': (
            '<p>Student pages are written entirely in Spanish, following the conventions of '
            'well-known ELE course books. Teacher Editions and answer-key notes are written in '
            'English, because they are written for the teacher, not the student.</p>\n'),
    },
}


def body(c):
    cefr = (f' Our <a href="{c["cefr_guide"]}">CEFR levels guide</a> explains what each level means in class.'
            if c['cefr_guide'] else '')
    return f'''<div class="article-hero">
  <div class="article-meta">About {c["brand"]} · Editorial standards</div>
  <h1>How {c["brand"]} Worksheets Are Made</h1>
  <p class="article-desc">Who makes {c["brand"]} worksheets, how each one is levelled and checked before it goes live, and what we do when a teacher finds a mistake.</p>
  <p class="article-byline">By the {c["brand"]} Editorial Team</p>
</div>
<article>

<p>{c["brand"]} is an independent library of free, printable {c["subject"]} worksheets for {c["audience"]}. It is built and maintained by a small team — the {c["brand"]} Editorial Team — with one goal: a teacher should be able to print a worksheet and teach it the same day, without fixing anything first.</p>

<h2>1. Every topic is a set, not a single sheet</h2>
<p>Most free worksheet sites give you one isolated page. We build each topic as a <strong>set</strong> you can teach in order: a <strong>Grammar</strong> sheet that presents the form, a <strong>Reading</strong> that shows it in context, a <strong>Writing</strong> task where students produce it, and a <strong>Practice</strong> sheet for extra controlled work — closed by a graded <strong>Quiz</strong>. The <a href="{c["sequence_guide"]}">sequencing guide</a> explains why that order works.</p>
{c["language_note"]}
<h2>2. Levelled against the CEFR</h2>
<p>Every topic is placed at {c["levels"]} using the Common European Framework of Reference (CEFR) descriptors, and every worksheet is tagged by level, skill and language focus, so the catalog filters match what you actually need for your class.{cefr}</p>

<h2>3. What we check before a worksheet goes live</h2>
<p>Each worksheet is read in full, line by line, before publishing. A sheet that fails any of these checks is corrected or discarded — never published as it is:</p>
<ul>
  <li><strong>Every word is legible.</strong> Garbled or unreadable text is a hard stop.</li>
  <li><strong>Closed items have exactly one correct answer.</strong> Multiple choice, word-bank gap-fills and matching items are checked one by one; if two answers could fit (a missing subject, a missing time or detail), the item is rewritten.</li>
  <li><strong>Matching exercises balance.</strong> Every option on the right has exactly one partner on the left — no spare options and no two items competing for the same answer.</li>
  <li><strong>Facts stay consistent.</strong> A price, time or quantity that appears in two activities must match in both.</li>
  <li><strong>Puzzles are solvable.</strong> Word searches and crosswords are checked letter by letter so every listed word is really in the grid.</li>
  <li><strong>It prints cleanly.</strong> Each worksheet is rendered and checked as a single A4 page before upload.</li>
</ul>

<h2>4. Answer keys and Teacher Editions</h2>
<p>Answer keys are written from the finished worksheet, item by item — never from a summary. Most worksheets also have a two-page <strong>Teacher Edition</strong> with the complete answer key, a ready lesson plan (presentation, guided practice and independent practice), the mistakes students typically make, and ideas for fast finishers.</p>

<h2>5. The tools behind the page</h2>
<p>Like most publishers today, we use a mix of digital tools to design our pages, including some AI-assisted tools for illustrations and layout. The topics, the level and the structure of every set are planned by the editorial team, and every exercise and answer is checked by hand before publishing, using the checks above.</p>

<h2>6. When we get something wrong</h2>
<p>If you find an error, email us at <a href="mailto:{c["contact"]}">{c["contact"]}</a>. We correct the worksheet itself — not just a note in the answer key — and then update its Teacher Edition and the topic quiz, so every piece of the set stays consistent.</p>

<h2>7. What is free and what is Premium</h2>
<p>Every worksheet is free to download and print. Teacher Editions and the graded quizzes are part of <a href="{c["pricing"]}">Premium</a>, which keeps the free library growing.</p>

<p><a href="{c["catalog"]}"><strong>Browse the worksheet catalog →</strong></a></p>

</article>'''


def build(key):
    c = SITES[key]
    s = open(os.path.join(c['root'], c['shell']), encoding='utf-8').read()
    url = f'{c["domain"]}/about/'
    title = f'How {c["brand"]} Worksheets Are Made — Editorial Standards'
    desc = (f'Who makes {c["brand"]} worksheets and how: CEFR-levelled topic sets, line-by-line answer '
            f'checks, Teacher Editions, and how we fix errors teachers report.')

    def sub(pattern, repl, count=1):
        nonlocal s
        s, n = re.subn(pattern, lambda m: repl, s, count=count, flags=re.S)
        assert n, pattern

    sub(r'<title>[^<]*</title>', f'<title>{title}</title>')
    sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">')
    sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">')
    sub(r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="website">')
    sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">')
    sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">')
    sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">')
    sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">')
    sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc}">')

    team = {'@type': 'Organization', 'name': f'{c["brand"]} Editorial Team', 'url': url}
    ld = [
        {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': title, 'description': desc, 'url': url,
         'author': team,
         'about': {'@type': 'Organization', 'name': c['brand'], 'url': c['domain'] + '/',
                   'email': c['contact'], 'logo': c['domain'] + '/favicon-192.png'}},
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': c['domain'] + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'About', 'item': url}]},
    ]
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', s, flags=re.S)
    ld_html = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    s = s.replace('</head>', ld_html + '</head>', 1)
    sub(r'<div class="breadcrumb" role="navigation" aria-label="Breadcrumb">.*?</div>',
        '<div class="breadcrumb" role="navigation" aria-label="Breadcrumb">\n  <a href="/">Home</a>\n  <span>›</span>\n  <span>About</span>\n</div>')
    sub(r'<main>.*?</main>', '<main>\n' + body(c) + '\n</main>')
    # byline style (same one guide_dates.stamp_byline adds to the guides)
    if '.article-byline' not in s:
        s = s.replace('</style>', '  .article-byline { font-size: 13px; color: var(--gray-600); margin-top: 10px; }\n  .article-byline a { color: inherit; }\n</style>', 1)
    out = os.path.join(c['root'], 'about', 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)
    print(f'OK: {out} ({len(s)} chars)')


if __name__ == '__main__':
    for k in SITES:
        build(k)
