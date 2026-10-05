# -*- coding: utf-8 -*-
"""Teaching guide /guides/how-to-teach-functional-english/ (05/10/2026).

Explica por qué los temas de Functional English (roadmap: A2 31-35, B1 36-50,
B2 36-50) tienen Reading + Practice + Writing y NO ficha de Grammar.

La lista "Functional English sets on Workshido" se arma SOLA desde Supabase con
las fichas cuyo tag incluye "functional english", agrupadas por topic_key.
→ Cada vez que se suba un set funcional nuevo (B1 41-50, B2), volver a correr:

    python tools/add_guide_functional.py

y desplegar. Reusa la maquinaria de add_guides_b1.py (plantilla viva, hub,
sitemap, llms.txt, "More teaching guides"); todo es idempotente.
"""
import os, re, sys
from collections import defaultdict

import pip_system_certs.wrapt_requests  # noqa: certificados de Windows
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import add_guides_b1 as base
import guide_dates
from env_secrets import supabase_creds

SLUG = 'how-to-teach-functional-english'
TODAY = '2026-10-05'  # datePublished (la plantilla trae la de conditionals)

# Nombre visible del tema cuando el título de la ficha no sirve (sets A2 con títulos dispares)
TOPIC_NAMES = {
    'shopping-a2': 'Shopping and Asking for Help',
    'giving-directions-a2': 'Asking for and Giving Directions',
    'health-problems-a2': 'Health Problems and Advice',
}
# Etiqueta de la ficha cuando el título no dice Reading/Writing
LABEL_OVERRIDE = {
    'asking-about-sizes-and-prices-functional-english-speaking': 'Speaking',
}
LABEL_ORDER = {'Reading': 0, 'Practice': 1, 'Speaking': 2, 'Writing': 3}


def fetch_functional():
    url, key = supabase_creds('en')
    r = requests.get(f'{url}/rest/v1/worksheets',
                     headers={'apikey': key, 'Authorization': f'Bearer {key}'},
                     params={'select': 'slug,title,level,topic_key,created_at',
                             'tags': 'ilike.*functional english*', 'order': 'created_at.asc'},
                     timeout=30)
    r.raise_for_status()
    return r.json()


def label_of(row):
    if row['slug'] in LABEL_OVERRIDE:
        return LABEL_OVERRIDE[row['slug']]
    t = row['title'].lower()
    return 'Reading' if 'reading' in t else 'Writing' if 'writing' in t else 'Practice'


def sets_html(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[(r['level'], r['topic_key'] or r['title'].split(' – ')[0])].append(r)
    by_level = defaultdict(list)
    for (level, tk), items in groups.items():
        name = TOPIC_NAMES.get(tk) or items[0]['title'].split(' – ')[0]
        items.sort(key=lambda r: LABEL_ORDER[label_of(r)])
        links = ' · '.join(f'<a href="/worksheet/{r["slug"]}/">{label_of(r)}</a>' for r in items)
        by_level[level].append((min(r['created_at'] for r in items), name, links))
    out = []
    for level in sorted(by_level):
        out.append(f'<h3>{level}</h3>\n<ul>')
        out += [f'  <li><strong>{name}</strong> — {links}</li>' for _, name, links in sorted(by_level[level])]
        out.append('</ul>')
    return '\n'.join(out), sorted(by_level)


def guide(rows):
    lists, levels = sets_html(rows)
    level_links = ', '.join(f'<a href="/worksheets/levels/{l.lower()}/">{l}</a>' for l in levels)
    return {
 'slug': SLUG,
 'title': 'How to Teach Functional English: Phrases Before Rules | Workshido',
 'h1': 'How to Teach Functional English — and Why It Has No Grammar Worksheet',
 'card': 'How to Teach Functional English (A2-B2)',
 'description': 'Why functional English topics like complaints, opinions and invitations have reading, practice and writing worksheets but no grammar sheet, and how to teach them.',
 'reading_time': '6 min read',  # ~1050 palabras
 'howto_name': 'How to Teach a Functional English Lesson in 45 Minutes',
 'steps': [('5 min', 'Warm-up: set up the situation before any language — "Your new phone stopped working after two days. What do you say in the shop?" — and board what students would say.'),
           ('10 min', 'Reading: read the model conversation or email for gist, then highlight every phrase that does the job.'),
           ('10 min', 'Sort the phrases: by function (open, ask, respond, close) and from most direct to most polite.'),
           ('10 min', 'Practice worksheet: choose the phrase that fits the situation and the person, and soften blunt sentences.'),
           ('10 min', 'Role-play in pairs, then swap roles so everyone practises both sides; the writing task follows next lesson.')],
 'body': f'''
<p>Most topics on Workshido come as a full set: a Grammar worksheet, a Reading, a Writing, often a Practice sheet and a Full Quiz. But some sets — <em>Making Complaints</em>, <em>Asking for Clarification</em>, <em>Ordering Food</em>, <em>Making Invitations</em> — have only <strong>Reading, Practice and Writing</strong>. That isn't a missing piece. These are <strong>Functional English</strong> topics, and for them a grammar worksheet is the wrong tool.</p>

<h2>1. Grammar topics and functional topics are built differently</h2>
<p>A grammar topic is organised around a <strong>form</strong>: the past simple, the passive, comparatives. Everything in the set serves that one structure. A functional topic is organised around a <strong>purpose</strong> — something people need to do with English in daily life: invite a friend, complain about a faulty product, disagree without offending, ask someone to repeat what they said.</p>
<table class="compare-table">
  <thead><tr><th></th><th>Grammar topic</th><th>Functional topic</th></tr></thead>
  <tbody>
    <tr><td>Built around</td><td>One structure (past simple, passive)</td><td>One communicative goal (complain, suggest, invite)</td></tr>
    <tr><td>Key question</td><td>Is it formed correctly?</td><td>Does it work in this situation, with this person?</td></tr>
    <tr><td>Students learn</td><td>A rule they can apply to new sentences</td><td>A set of ready-made phrases and when to use each one</td></tr>
    <tr><td>Typical error</td><td><em>"He goed home."</em></td><td><em>"I want my money back."</em> — correct, but too blunt</td></tr>
  </tbody>
</table>

<h2>2. Why there's no Grammar worksheet</h2>
<h3>The phrases cut across grammar</h3>
<p>Look at the language for making suggestions: <em>Let's</em> + base verb, <em>Why don't we</em> + base verb, <em>How about</em> + <em>-ing</em>, <em>We could</em> + base verb. That's four different structures for one job — and <em>Why don't we…?</em> is a negative question that isn't negative at all. A grammar worksheet would have to teach four unrelated rules, or teach one of them out of the context that gives it meaning. Neither helps students make a suggestion.</p>
<h3>They're learned as chunks</h3>
<p>Fluent speakers don't build <em>"Would it be possible to…?"</em> from modal-verb rules in real time; they retrieve it whole, like a single word. Students who learn these expressions as fixed chunks use them sooner and more confidently than students who try to assemble them.</p>
<h3>The real difficulty is choosing the right phrase</h3>
<p><em>"I disagree"</em> and <em>"I see your point, but…"</em> are both grammatically perfect. Only one keeps the conversation friendly. What students need to practise is <strong>appropriacy</strong>: register, softening, knowing what to say first and how to respond. The CEFR treats this as pragmatic competence — a separate area from grammatical accuracy — and it needs its own kind of practice.</p>

<h2>3. Where the grammar went</h2>
<p>It isn't missing; it lives in two places. First, <strong>inside the phrases</strong>: students meet <em>would</em>, <em>could</em> and <em>-ing</em> forms as part of an expression, before they need the rule behind them. Second, in <strong>its own sets</strong>. The modals behind polite requests are covered in <a href="/guides/how-to-teach-modal-verbs/">how to teach modal verbs</a>, and the connectors that hold an opinion together in <a href="/guides/how-to-teach-linking-words/">how to teach linking words</a>. If a group struggles to form <em>Could you…?</em>, teach the modal set first and come back to the functional set afterwards.</p>

<h2>4. How a functional set works</h2>
<p>Every functional set follows the same three steps, from meeting the language to using it:</p>
<ul>
  <li><strong>Reading — meet the language in a real exchange.</strong> A conversation, an email or a discussion where the phrases are doing their job. Students see who says what, to whom, and how the other person responds.</li>
  <li><strong>Practice — choose the right phrase.</strong> In a functional set this sheet does the job a grammar worksheet does elsewhere: matching phrases to functions, choosing the most polite option, completing mini-dialogues and rewriting blunt sentences politely.</li>
  <li><strong>Writing — use it for real.</strong> A guided dialogue, email or short text with a planner and a checklist, so students produce the phrases in a complete piece of communication.</li>
</ul>
<p>Teach them in that order: <strong>Reading → Practice → Writing</strong>. In <a href="/guides/how-to-sequence-esl-lessons/">grammar sets</a> the Practice sheet is optional extra repetition; in a functional set it is the controlled-practice step, so don't skip it.</p>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Set up the situation before any language and board what students would say.</li>
  <li><strong>10 min —</strong> Reading: gist first, then highlight every phrase that does the job.</li>
  <li><strong>10 min —</strong> Sort the phrases by function and from most direct to most polite.</li>
  <li><strong>10 min —</strong> Practice worksheet: the right phrase for the situation and the person.</li>
  <li><strong>10 min —</strong> Role-play in pairs, then swap roles. The writing task follows next lesson.</li>
</ol>

<h2>Common problems and how to fix them</h2>
<ul>
  <li><strong>Correct but too direct:</strong> <em>"I want a refund." "Repeat, please."</em> Draw a politeness scale on the board and have students move each sentence one step up: <em>I'd like a refund, please. Sorry, could you repeat that?</em></li>
  <li><strong>One phrase for everything:</strong> every opinion starts with <em>"I think"</em>. Add "use three different phrases" to the writing checklist.</li>
  <li><strong>Knowing the phrase but not the reply:</strong> students can invite but freeze at <em>"Sorry, I can't make it."</em> Always practise both sides of the exchange and swap roles.</li>
  <li><strong>Translating from their first language:</strong> polite formulas rarely transfer word for word. Ask students how they would say it in their own language and compare what each version does.</li>
  <li><strong>Right words, wrong tone:</strong> a polite phrase in a flat or impatient voice still sounds rude. Model it aloud and drill the intonation chorally before the role-play.</li>
</ul>

<h2>Functional English sets on Workshido</h2>
<p>Each set below has the same structure — Reading, Practice and Writing at the same level — so you can teach it as a ready-made mini-unit:</p>
{lists}
<p>More functional topics are on the way, following the same structure. B1 continues with travel problems, formal and informal emails, reviews and presentations, and B2 moves on to negotiating, speculating, managing a discussion and writing reports. Every worksheet is free to download and print — browse the full {level_links} collections.</p>
''',
    }


def main():
    rows = fetch_functional()
    print(len(rows), 'fichas con tag functional english')
    g = guide(rows)
    base.GUIDES = [g]
    base.main()  # página, hub, sitemap, llms.txt, "More teaching guides"

    p = os.path.join(base.REPO, 'guides', SLUG, 'index.html')
    s = open(p, encoding='utf-8').read()
    s = re.sub(r'"datePublished":\s*"[^"]*"', f'"datePublished":"{TODAY}"', s, count=1)
    # build_page no cambia el tiempo de lectura si la plantilla ya trae "Updated <time>"
    s = re.sub(r'(<div class="article-meta">Teaching Guide · )\d+ min read', lambda m: m.group(1) + g['reading_time'], s, count=1)
    if '.compare-table' not in s.split('</style>')[0]:
        s = s.replace('</style>', '''  .compare-table { width: 100%; border-collapse: collapse; margin: 8px 0 20px; font-size: 15px; }
  .compare-table th, .compare-table td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--gray-100); vertical-align: top; }
  .compare-table th { font-family: var(--font-display); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--gray-600); }
  .compare-table td:first-child { font-weight: 600; color: var(--blue-900); }
  @media (max-width: 560px) { .compare-table { font-size: 14px; } .compare-table th, .compare-table td { padding: 8px 6px; } }
</style>''', 1)
    open(p, 'w', encoding='utf-8', newline='').write(s)
    guide_dates.stamp(p)
    hub = os.path.join(base.REPO, 'guides', 'index.html'); h = open(hub, encoding='utf-8').read()
    h2 = re.sub(r'(href="/guides/%s/">\s*<span class="hub-card-meta">)[^<]*' % SLUG, lambda m: m.group(1) + g['reading_time'], h)
    if h2 != h:
        open(hub, 'w', encoding='utf-8', newline='').write(h2)
    print('OK fechas + estilos de tabla')


if __name__ == '__main__':
    main()
