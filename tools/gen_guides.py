"""Genera los artículos-guía SEO (/guides/<slug>/index.html) — contenido
editorial original enlazado a las landings de tema/nivel y a worksheets
reales del catálogo, siguiendo el "clusters de guías" que recomendó la
auditoría (guía → landing de tema → ficha → recursos relacionados).

Uso:
  python tools/gen_guides.py
"""
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GUIDES = [
    {
        'slug': 'guides/how-to-teach-present-simple',
        'title': 'How to Teach Present Simple: A Complete Guide for A1-A2 Classes | Workshido',
        'description': 'A practical, step-by-step guide to teaching present simple to A1-A2 ESL students, with common mistakes, warm-up ideas, and free printable worksheets.',
        'h1': 'How to Teach Present Simple: A Complete Guide for A1-A2 Classes',
        'reading_time': '7 min read',
        'body': '''
<p>Present simple is usually the first real "grammar point" A1 students meet beyond basic verb-to-be sentences, and it comes with a trap most teachers know well: students can recite the rule (add -s in third person) but still say "she go to school" three sentences after the drill. The fix isn't more explanation — it's the right sequence of practice.</p>

<h2>1. Start with routine, not rules</h2>
<p>Present simple is the tense of habits and routines, so the fastest way into it is a real routine, not a grammar box. Ask students what time they wake up, what they eat for breakfast, how they get to school. Write the answers on the board in first person ("I wake up at 7"), then ask about a classmate ("What time does <em>he</em> wake up?") — this is where the third-person -s naturally becomes necessary instead of arbitrary.</p>

<h2>2. Isolate the third-person -s before mixing persons</h2>
<p>Most present simple errors are really just third-person-singular errors. Before combining all persons in one exercise, spend five minutes on transformation drills: give students a list of base verbs (work, watch, go, study, have) and have them produce only the "he/she/it" form. This catches the spelling patterns early — consonant+y → ies (study → studies), -sh/-ch/-ss/-x → es (watch → watches) — without the extra cognitive load of choosing the right pronoun at the same time.</p>

<h2>3. Drill negatives and questions as chunks, not rules</h2>
<p>"Don't/doesn't + base verb" and "Do/Does + subject + base verb" are best taught as fixed chunks students can slot a verb into, rather than a rule about auxiliary verbs (which most A1 students don't have the metalanguage for yet). A simple, high-repetition drill works better here than explanation: hold up a routine picture, students answer "Does she wake up early?" — "Yes, she does" / "No, she doesn't."</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Missing third-person -s:</strong> "She like coffee." — the single most common A1/A2 error. Fix with the transformation drill above before moving to freer practice.</li>
  <li><strong>Double marking with do/does:</strong> "Does she likes coffee?" — students add -s in both the auxiliary and the main verb. Point out that only ONE part of the sentence carries the "signal" — either does, or -s, never both.</li>
  <li><strong>Present simple for actions happening now:</strong> "Look, she cooks now!" instead of "she's cooking." This usually clears up once students meet present continuous — the two tenses are best contrasted directly, not taught in isolation.</li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up: elicit routines orally, no writing yet.</li>
  <li><strong>10 min —</strong> Isolate and drill the third-person -s spelling rules.</li>
  <li><strong>15 min —</strong> Controlled practice: complete-the-sentence and choose-the-correct-form exercises.</li>
  <li><strong>10 min —</strong> Freer practice: students interview a partner about their routine and report back in third person.</li>
  <li><strong>5 min —</strong> Quick error-correction round using mistakes you overheard during the interview stage.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<p>These printable PDFs follow the same progression above — spelling focus, controlled practice, then freer production:</p>
<ul>
  <li><a href="/workshido-worksheet.html?id=8b8b6396-eff9-444f-87d5-9bd1db3ab2b7">Third Person Singular – Present Simple</a> (A1) — isolates the -s spelling rules.</li>
  <li><a href="/workshido-worksheet.html?id=c1d21578-f780-426c-ac6a-cab091b70861">Third Person Singular – Grammar</a> (A1) — more controlled practice.</li>
  <li><a href="/workshido-worksheet.html?id=4c739616-3d20-405a-a86c-7b4ec3b5f873">Present Simple – Grammar</a> (A2) — full reference and practice: affirmative, negative, questions, and a daily-routine text, with a complete Teacher Edition.</li>
  <li><a href="/workshido-worksheet.html?id=e8639be1-b0f6-47b0-a7c0-f12235d5cbd3">Present Simple Tense – Practice</a> (A2) — 10 mixed exercises for extra practice, from controlled to freer production.</li>
  <li><a href="/workshido-worksheet.html?id=af1d60b9-39fd-494b-bca5-d184bf3eac2e">Present Simple vs. Present Continuous</a> (A2) — for contrasting the two tenses once present simple is solid.</li>
  <li><a href="/workshido-worksheet.html?id=ca2452e9-ed4f-4139-9093-4f09c3e6fa65">My Daily Routine – Present Simple Writing</a> (A2) — freer production to close the lesson.</li>
</ul>
<p>Browse the full set of <a href="/worksheets/grammar/">grammar worksheets</a> or filter by <a href="/worksheets/levels/a1/">A1</a> and <a href="/worksheets/levels/a2/">A2</a> level.</p>
''',
    },
    {
        'slug': 'guides/cefr-levels-guide',
        'title': 'CEFR Levels Explained: A1 to B1 — Which Worksheets to Use | Workshido',
        'description': 'A plain-English guide to the CEFR levels (A1, A2, B1) for English teachers: what students can actually do at each level, and how to pick the right worksheet.',
        'h1': 'CEFR Levels Explained: A1 to B1 — Which Worksheets to Use',
        'reading_time': '6 min read',
        'body': '''
<p>The CEFR (Common European Framework of Reference for Languages) is the standard most English course books, worksheets, and placement tests use to describe how much a student can actually do in the language — not how many grammar points they've "covered." That distinction matters more than it sounds: a student can technically have "learned" the present perfect and still be solidly A2, because CEFR levels are about real communicative ability, not a checklist of tenses.</p>

<p>Here's what that means in practice for the levels you'll teach most often.</p>

<h2>A1 — Beginner</h2>
<p>An A1 student can understand and use very basic phrases aimed at satisfying concrete needs: introducing themselves, asking simple questions about where someone lives or what they do, and interacting slowly with a patient speaker. Grammatically, this is verb-to-be, basic present simple, simple plurals, basic prepositions of place, and a core vocabulary of everyday objects and routines.</p>
<p><strong>What A1 worksheets should look like:</strong> short sentences, high visual support (label-and-learn style vocabulary sheets work very well here), heavily controlled exercises (matching, fill-in-the-blank with a word bank) rather than open production. Explore the <a href="/worksheets/levels/a1/">full set of A1 worksheets</a>.</p>

<h2>A2 — Elementary</h2>
<p>A2 students can communicate in simple, routine tasks requiring a direct exchange of information on familiar topics — describing their family, their job, their neighborhood, in simple terms. This is where past simple, present continuous, comparatives, and the first modal verbs (can, must, should) typically get introduced, alongside a wider vocabulary range across everyday topics.</p>
<p><strong>What A2 worksheets should look like:</strong> slightly longer texts (a short story, a simple dialogue), a mix of controlled and semi-controlled exercises, and the first real writing tasks — a short paragraph rather than single sentences. See the <a href="/worksheets/levels/a2/">full set of A2 worksheets</a>.</p>

<h2>B1 — Intermediate</h2>
<p>A B1 student can deal with most situations likely to arise while travelling, produce simple connected text on familiar topics, and describe experiences, events, and ambitions with brief reasons and explanations. This level introduces present perfect in more depth, the full range of past tenses working together (past simple vs. past continuous), first and second conditionals, and reported speech.</p>
<p><strong>What B1 worksheets should look like:</strong> authentic-feeling texts (an email, a blog post, a news snippet), open-ended comprehension questions, and writing tasks that ask for opinion and justification, not just description.</p>

<h2>A quick way to level-check a worksheet before you use it</h2>
<ul>
  <li>If most sentences are 5 words or fewer and everything is present tense → almost certainly A1.</li>
  <li>If the text mixes tenses and includes connectors like "because," "but," "so" → A2 territory.</li>
  <li>If a text requires students to explain a reason or describe a past experience in some detail → you're already at B1.</li>
</ul>

<p>Browse the full catalog by <a href="/workshido-index.html">level and skill</a>, or start with <a href="/worksheets/grammar/">grammar</a>, <a href="/worksheets/vocabulary/">vocabulary</a>, <a href="/worksheets/reading/">reading</a>, or <a href="/worksheets/writing/">writing</a> worksheets.</p>
''',
    },
    {
        'slug': 'guides/esl-warm-up-activities',
        'title': '10 Quick ESL Warm-Up Activities (5-10 Minutes, No Prep) | Workshido',
        'description': '10 fast, low-prep warm-up activities for ESL classes, organized by CEFR level, to get students speaking English in the first five minutes of class.',
        'h1': '10 Quick ESL Warm-Up Activities (5-10 Minutes, No Prep)',
        'reading_time': '5 min read',
        'body': '''
<p>The first five minutes of class set the tone for the rest of the lesson — and they're also the easiest to lose to late arrivals, phones, and small talk in the students' first language. A short, structured warm-up fixes both problems: it gets everyone talking in English immediately, and it gives latecomers something to slot into without disrupting the class.</p>

<p>These ten need almost no preparation and work across most levels — adjust the vocabulary, not the format, for A1 vs. B1 classes.</p>

<h2>1. Two truths and a lie</h2>
<p>Each student says three sentences about themselves — two true, one false — and the class guesses which is the lie. Great for present simple and past simple review depending on the tense you ask for.</p>

<h2>2. Chain story</h2>
<p>One student starts a sentence, the next student repeats it and adds one word or short phrase. Builds listening and sentence-structure awareness; works well as a past-tense narrative warm-up.</p>

<h2>3. Category race</h2>
<p>Call out a category (animals, food, jobs) and a letter; students race in pairs to write as many words as possible in 60 seconds. Zero prep, instantly reviews vocabulary from a previous unit.</p>

<h2>4. Would you rather</h2>
<p>Ask a "would you rather" question (coffee or tea? beach or mountains?) and have students justify their answer to a partner using "because." Good for A2+ opinion language.</p>

<h2>5. Yesterday I...</h2>
<p>Students go around in a circle completing "Yesterday I ___" with a real activity, and the next student has to recall and repeat everyone before them before adding their own — a memory-game format that drills past simple naturally.</p>

<h2>6. Picture description sprint</h2>
<p>Show any image (a slide, a magazine photo, a worksheet illustration you're about to use anyway) for 15 seconds, then have students describe everything they remember. Doubles as a natural bridge into the main lesson if the image is from that day's worksheet.</p>

<h2>7. Question swap</h2>
<p>Give each student one question card; they ask a classmate, then trade cards and find a new partner. Works for any grammar point you want to review — just write the target structure into the questions.</p>

<h2>8. Odd one out</h2>
<p>Put four words on the board, three related, one not. Students discuss in pairs which one doesn't belong and why. Cheap to prepare and naturally elicits justification language.</p>

<h2>9. Mime the verb</h2>
<p>One student mimes an action verb, the class guesses using the correct tense you specify ("She is cooking" vs. "She cooks every day" vs. "She cooked yesterday"). Physical, energizing, and directly reviews tense form.</p>

<h2>10. Board race</h2>
<p>Split the class into two teams at the board. Call out a prompt (a translated word, a scrambled sentence, a grammar transformation) and the first student to run up and write the correct answer wins a point. Works as a warm-up for almost any grammar point you're about to teach or review.</p>

<h2>Pairing warm-ups with a full lesson</h2>
<p>Most warm-ups here work best when they preview the grammar or vocabulary you're about to teach — "Yesterday I..." before a past simple lesson, "Mime the verb" before contrasting present simple and present continuous. Browse worksheets by <a href="/worksheets/grammar/">grammar point</a> or by <a href="/workshido-index.html">level</a> to find a matching main activity.</p>
''',
    },
]


ARTICLE_STYLE = '''<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --blue-900: #042C53; --blue-800: #0C447C; --blue-600: #185FA5; --blue-400: #378ADD;
    --blue-200: #85B7EB; --blue-100: #B5D4F4; --blue-50: #E6F1FB;
    --teal-600: #0F6E56; --teal-400: #1D9E75; --teal-50: #E1F5EE;
    --gray-900: #2C2C2A; --gray-600: #5F5E5A; --gray-300: #B4B2A9; --gray-100: #D3D1C7; --gray-50: #F1EFE8;
    --white: #ffffff; --radius-sm: 6px; --radius-md: 10px; --radius-lg: 16px;
    --font-display: 'Sora', sans-serif; --font-body: 'Inter', sans-serif;
  }
  html { scroll-behavior: smooth; }
  body { font-family: var(--font-body); background: var(--white); color: var(--gray-900); line-height: 1.6; -webkit-font-smoothing: antialiased; }
  nav { position: sticky; top: 0; z-index: 100; background: var(--blue-900); display: flex; align-items: center; justify-content: space-between; padding: 0 32px; height: 60px; }
  .nav-logo { font-family: var(--font-display); font-size: 20px; font-weight: 700; color: var(--white); text-decoration: none; }
  .nav-logo span { color: var(--blue-200); }
  .nav-actions { display: flex; gap: 10px; align-items: center; }
  .btn-ghost { font-family: var(--font-body); font-size: 13px; font-weight: 500; color: var(--blue-100); background: transparent; border: 1px solid rgba(255,255,255,0.2); border-radius: var(--radius-sm); padding: 7px 16px; cursor: pointer; text-decoration: none; }
  .btn-primary { font-family: var(--font-body); font-size: 13px; font-weight: 600; color: var(--blue-900); background: var(--white); border: none; border-radius: var(--radius-sm); padding: 7px 18px; cursor: pointer; text-decoration: none; }
  .breadcrumb { padding: 16px 32px; font-size: 13px; color: var(--gray-300); max-width: 760px; margin: 0 auto; }
  .breadcrumb a { color: var(--gray-600); text-decoration: none; }
  .breadcrumb span { margin: 0 6px; }
  .article-hero { padding: 24px 32px 8px; max-width: 760px; margin: 0 auto; }
  .article-meta { font-size: 12px; font-weight: 600; color: var(--teal-600); text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px; }
  .article-hero h1 { font-family: var(--font-display); font-size: clamp(26px, 4vw, 38px); font-weight: 700; color: var(--gray-900); line-height: 1.25; margin-bottom: 10px; }
  .article-desc { font-size: 16px; color: var(--gray-600); line-height: 1.6; }
  article { max-width: 760px; margin: 24px auto 0; padding: 0 32px 60px; font-size: 16px; line-height: 1.75; color: #333; }
  article h2 { font-family: var(--font-display); font-size: 21px; font-weight: 700; color: var(--blue-900); margin: 32px 0 12px; }
  article p { margin-bottom: 16px; }
  article ul, article ol { margin: 0 0 16px 22px; }
  article li { margin-bottom: 8px; }
  article a { color: var(--blue-600); }
  article strong { color: var(--gray-900); }
  .related-guides { max-width: 760px; margin: 0 auto 60px; padding: 0 32px; }
  .related-guides h2 { font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--gray-900); margin-bottom: 14px; }
  .guide-links { display: flex; flex-direction: column; gap: 10px; }
  .guide-link { display: block; padding: 14px 18px; border: 1px solid var(--gray-100); border-radius: var(--radius-md); text-decoration: none; color: var(--blue-900); font-weight: 600; font-size: 14px; transition: border-color 0.15s, background 0.15s; }
  .guide-link:hover { border-color: var(--blue-200); background: var(--blue-50); }
  footer { border-top: 1px solid var(--gray-100); padding: 32px; text-align: center; font-size: 13px; color: var(--gray-300); }
  footer a { color: var(--blue-600); text-decoration: none; }
  @media (max-width: 480px) { nav { padding: 0 16px; } .breadcrumb, .article-hero, article, .related-guides { padding-left: 16px; padding-right: 16px; } }
</style>'''


def render_page(guide, others):
    related = '\n    '.join(
        f'<a class="guide-link" href="/{o["slug"]}/">{o["h1"]}</a>' for o in others
    )
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{guide['title']}</title>
<meta name="description" content="{guide['description']}">
<link rel="canonical" href="https://workshido.com/{guide['slug']}/">
<meta property="og:site_name" content="Workshido">
<meta property="og:type" content="article">
<meta property="og:title" content="{guide['title']}">
<meta property="og:description" content="{guide['description']}">
<meta property="og:image" content="https://workshido.com/og-image.png">
<meta property="og:url" content="https://workshido.com/{guide['slug']}/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{guide['title']}">
<meta name="twitter:description" content="{guide['description']}">
<meta name="theme-color" content="#042C53">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{guide['h1']}","description":"{guide['description']}","author":{{"@type":"Organization","name":"Workshido"}},"publisher":{{"@type":"Organization","name":"Workshido","logo":{{"@type":"ImageObject","url":"https://workshido.com/favicon-192.png"}}}},"mainEntityOfPage":"https://workshido.com/{guide['slug']}/"}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Guides","item":"https://workshido.com/guides/"}},{{"@type":"ListItem","position":2,"name":"{guide['h1']}","item":"https://workshido.com/{guide['slug']}/"}}]}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">
{ARTICLE_STYLE}
</head>
<body>
<nav>
  <a href="/index.html" class="nav-logo">work<span>shido</span></a>
  <div class="nav-actions" id="navActions">
    <a href="/workshido-login.html" class="btn-ghost">Log in</a>
    <a href="/workshido-signup.html" class="btn-primary">Sign up free</a>
  </div>
</nav>
<div class="breadcrumb" role="navigation" aria-label="Breadcrumb">
  <a href="/guides/">Guides</a>
  <span>›</span>
  <span>{guide['h1']}</span>
</div>
<div class="article-hero">
  <div class="article-meta">Teaching Guide · {guide['reading_time']}</div>
  <h1>{guide['h1']}</h1>
  <p class="article-desc">{guide['description']}</p>
</div>
<article>
{guide['body']}
</article>
<div class="related-guides">
  <h2>More teaching guides</h2>
  <div class="guide-links">
    {related}
    <a class="guide-link" href="/workshido-index.html">Browse the full worksheet catalog →</a>
  </div>
</div>
<footer>
  <span>© 2026 Workshido — <a href="/workshido-index.html">Free English worksheets</a></span>
</footer>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.110.7" defer></script>
<script src="/js/guides-auth.js" defer></script>
<script src="/js/analytics.js" defer></script>
</body>
</html>
'''


HUB_STYLE = '''<style>
  .hub-hero { text-align: center; padding: 56px 32px 40px; background: linear-gradient(160deg, var(--blue-900) 0%, var(--blue-800) 100%); }
  .hub-hero h1 { font-family: var(--font-display); font-size: clamp(28px, 4.5vw, 42px); font-weight: 700; color: var(--white); margin-bottom: 12px; }
  .hub-hero p { font-size: 16px; color: var(--blue-100); max-width: 520px; margin: 0 auto; }
  .hub-grid { max-width: 760px; margin: 40px auto 60px; padding: 0 32px; display: flex; flex-direction: column; gap: 16px; }
  .hub-card { display: flex; flex-direction: column; gap: 6px; padding: 20px 22px; border: 1px solid var(--gray-100); border-radius: var(--radius-lg); text-decoration: none; transition: border-color 0.15s, transform 0.15s; }
  .hub-card:hover { border-color: var(--blue-200); transform: translateY(-1px); }
  .hub-card-meta { font-size: 11px; font-weight: 600; color: var(--teal-600); text-transform: uppercase; letter-spacing: 0.5px; }
  .hub-card-title { font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--gray-900); }
  .hub-card-desc { font-size: 14px; color: var(--gray-600); line-height: 1.5; }
  @media (max-width: 480px) { .hub-grid { padding: 0 16px; } }
</style>'''


def render_hub():
    cards = '\n    '.join(
        f'''<a class="hub-card" href="/{g["slug"]}/">
      <span class="hub-card-meta">{g['reading_time']}</span>
      <span class="hub-card-title">{g['h1']}</span>
      <span class="hub-card-desc">{g['description']}</span>
    </a>''' for g in GUIDES
    )
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Teaching Guides for English Teachers | Workshido</title>
<meta name="description" content="Practical, free teaching guides for ESL teachers: how to teach specific grammar points, understand CEFR levels, and run better classroom warm-ups.">
<link rel="canonical" href="https://workshido.com/guides/">
<meta property="og:site_name" content="Workshido">
<meta property="og:type" content="website">
<meta property="og:title" content="Teaching Guides for English Teachers | Workshido">
<meta property="og:description" content="Practical, free teaching guides for ESL teachers.">
<meta property="og:image" content="https://workshido.com/og-image.png">
<meta property="og:url" content="https://workshido.com/guides/">
<meta name="theme-color" content="#042C53">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Teaching Guides","url":"https://workshido.com/guides/","isPartOf":{{"@type":"WebSite","name":"Workshido","url":"https://workshido.com/"}}}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">
{ARTICLE_STYLE}
{HUB_STYLE}
</head>
<body>
<nav>
  <a href="/index.html" class="nav-logo">work<span>shido</span></a>
  <div class="nav-actions" id="navActions">
    <a href="/workshido-login.html" class="btn-ghost">Log in</a>
    <a href="/workshido-signup.html" class="btn-primary">Sign up free</a>
  </div>
</nav>
<section class="hub-hero">
  <h1>Teaching Guides</h1>
  <p>Practical guides for ESL teachers — how to teach specific grammar points, understand CEFR levels, and run better classroom activities.</p>
</section>
<div class="hub-grid">
    {cards}
</div>
<footer>
  <span>© 2026 Workshido — <a href="/workshido-index.html">Free English worksheets</a></span>
</footer>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.110.7" defer></script>
<script src="/js/guides-auth.js" defer></script>
<script src="/js/analytics.js" defer></script>
</body>
</html>
'''


def main():
    for guide in GUIDES:
        others = [g for g in GUIDES if g['slug'] != guide['slug']]
        html = render_page(guide, others)
        out_dir = os.path.join(REPO, guide['slug'])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"OK: {guide['slug']}/index.html ({len(html)} chars)")

    hub_html = render_hub()
    hub_dir = os.path.join(REPO, 'guides')
    os.makedirs(hub_dir, exist_ok=True)
    with open(os.path.join(hub_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(hub_html)
    print(f"OK: guides/index.html ({len(hub_html)} chars)")


if __name__ == '__main__':
    main()
