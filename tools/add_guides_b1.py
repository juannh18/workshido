# -*- coding: utf-8 -*-
"""Crea 5 teaching guides B1 (26/09/2026) usando como plantilla una guía YA publicada.

POR QUÉ NO gen_guides.py: ese generador solo conoce 8 de las 15 guías y regenera
guides/index.html con esas 8 — correrlo borraría 7 guías del índice y pisaría arreglos
posteriores (auth del nav, footer). Aquí se copia el HTML vivo de una guía y se
reemplazan solo los campos propios de cada artículo.

Idempotente: re-correrlo reescribe las 5 páginas y no duplica tarjetas, entradas del
sitemap, líneas de llms.txt ni enlaces "More teaching guides".

Uso: python tools/add_guides_b1.py
"""
import html, json, os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(REPO, 'guides', 'how-to-teach-conditionals', 'index.html')
T_SLUG = 'how-to-teach-conditionals'

W = lambda slug, text, note: f'<li><a href="/worksheet/{slug}/">{text}</a> — {note}</li>'

GUIDES = [
# ─────────────────────────────── PASSIVE VOICE ───────────────────────────────
{
 'slug': 'how-to-teach-passive-voice',
 'title': 'How to Teach the Passive Voice to B1 Classes | Workshido',
 'h1': 'How to Teach the Passive Voice: A Step-by-Step Guide for B1',
 'card': 'How to Teach the Passive Voice (B1)',
 'description': 'Teach the passive voice at B1: why we use it, be + past participle across tenses, when to add "by", common mistakes and free printable worksheets.',
 'reading_time': '8 min read',
 'howto_name': 'How to Teach the Passive Voice in a 45-Minute Lesson',
 'steps': [('5 min', 'Warm-up: show three real-world sentences (a product label, a news headline, a sign) and ask who did the action — and whether we care.'),
           ('10 min', 'Present be + past participle with present simple and past simple only, building each sentence from its active version.'),
           ('10 min', 'Controlled practice: transform active to passive, deciding each time whether the agent (by …) is worth keeping.'),
           ('10 min', 'Tense-matching drill: students keep the tense of "be" from the active verb (is made / was made / will be made).'),
           ('10 min', 'Freer practice: students write a short process description (how chocolate is made, how a school is run) in the passive.')],
 'body': '''
<p>The passive voice is one of the first B1 structures where students already know every word they need — <em>be</em> and the past participle — and still get it wrong, because the difficulty isn't the form. It's knowing <strong>why</strong> anyone would choose it. Teach the reason first and the form becomes almost obvious.</p>

<h2>1. Start with "who did it?" — and whether it matters</h2>
<p>The passive exists to move the focus from the person who acts to the thing that is affected. Show a few sentences from real life: <em>"This bridge was built in 1932." "English is spoken here." "My phone was stolen."</em> Ask students who built the bridge, who speaks English, who stole the phone. The honest answer — "we don't know" or "it doesn't matter" — is the whole point of the passive. When students see that the agent is unknown, obvious or unimportant, the structure stops feeling like a grammar trick and starts feeling useful.</p>

<h2>2. Build every passive from its active sentence</h2>
<p>Write an active sentence, then rebuild it in three moves: the object moves to the front, <em>be</em> takes the tense of the original verb, and the main verb becomes a past participle. <em>"Workers <u>clean</u> the rooms every day" → "The rooms <u>are cleaned</u> every day."</em> Start with present simple and past simple only. The rule that unlocks every later tense is simple: <strong>the tense lives in "be", the meaning lives in the participle</strong> — so <em>will be cleaned, has been cleaned, is being cleaned</em> are just new forms of <em>be</em> in front of the same participle.</p>

<h2>3. Teach "by + agent" as the exception, not the rule</h2>
<p>Students who learn the passive through transformation drills tend to keep the agent every time: <em>"The pizza was eaten by someone."</em> Tell them explicitly that most passive sentences have <strong>no</strong> agent, and that "by …" is only added when the agent is new or important information: <em>"Guernica was painted by Picasso."</em> A quick sorting task — keep or delete the agent in ten sentences — fixes this faster than any explanation.</p>

<h2>4. Move to more tenses and modals only when the core is automatic</h2>
<p>Once present and past are secure, add future (<em>will be + participle</em>), <em>be going to</em>, and modals (<em>must be done, can be recycled</em>). These are the forms students meet in instructions, rules and news, so tie them to those text types: a list of school rules, a recycling guide, a news report about a new stadium.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Missing "be":</strong> <em>"The house built in 1990."</em> Students drop the auxiliary because it carries no meaning for them. Point back to the three-move rebuild: no <em>be</em>, no tense.</li>
  <li><strong>Wrong participle:</strong> <em>"The window was broke."</em> This is an irregular-verb problem, not a passive problem — review the third column before the lesson.</li>
  <li><strong>Tense lost in the transformation:</strong> <em>"They built it" → "It is built."</em> Have students underline the active verb and write its tense above it before they rewrite.</li>
  <li><strong>Passive with intransitive verbs:</strong> <em>"The accident was happened."</em> Only verbs with an object can go into the passive; <em>happen, arrive, die</em> can't.</li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up with real sentences: who did it, and do we care?</li>
  <li><strong>10 min —</strong> Present <em>be</em> + past participle in present and past simple, rebuilding from active sentences.</li>
  <li><strong>10 min —</strong> Controlled practice: active → passive, deciding whether to keep the agent.</li>
  <li><strong>10 min —</strong> Tense-matching drill: the tense always moves into <em>be</em>.</li>
  <li><strong>10 min —</strong> Freer practice: describe a process in the passive.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<p>These printable PDFs follow the same progression — present and past first, then more tenses and modals — each with its grammar, reading and writing piece:</p>
<ul>
''' + '\n'.join([
    W('passive-voice-in-present-simple-grammar', 'Passive Voice in Present Simple – Grammar', 'the core form, with processes and facts.'),
    W('passive-voice-in-present-simple-reading', 'Passive Voice in Present Simple – Reading', 'recognising the passive in a connected text.'),
    W('the-passive-voice-past-simple-grammar', 'The Passive Voice: Past Simple – Grammar', 'history, inventions and "was/were + participle".'),
    W('passive-voice-present-and-past-practice', 'Passive Voice: Present and Past – Practice', 'mixed practice once both tenses are introduced.'),
    W('the-passive-voice-in-future-simple-grammar', 'The Passive Voice in Future Simple – Grammar', '"will be + participle" for plans and predictions.'),
    W('the-passive-voice-with-modal-verbs-grammar', 'The Passive Voice with Modal Verbs – Grammar', 'rules and instructions: must be done, can be used.'),
    W('the-passive-voice-in-all-tenses-writing', 'The Passive Voice in All Tenses – Writing', 'freer production to close the unit.'),
]) + '''
</ul>
<p>Browse all <a href="/worksheets/grammar/">grammar worksheets</a> or the full <a href="/worksheets/levels/b1/">B1 collection</a>.</p>
''',
},
# ─────────────────────────────── PHRASAL VERBS ───────────────────────────────
{
 'slug': 'how-to-teach-phrasal-verbs',
 'title': 'How to Teach Phrasal Verbs to B1 Students | Workshido',
 'h1': 'How to Teach Phrasal Verbs: A Practical Guide for B1 Classes',
 'card': 'How to Teach Phrasal Verbs (B1)',
 'description': 'Teach phrasal verbs by topic, not alphabet: meaning in context, separable vs. inseparable (pick it up, look after him), common mistakes and free worksheets.',
 'reading_time': '8 min read',
 'howto_name': 'How to Teach Phrasal Verbs in a 45-Minute Lesson',
 'steps': [('5 min', 'Warm-up: a short story or dialogue with 6-8 phrasal verbs from one topic; students guess each meaning from context.'),
           ('10 min', 'Meaning focus: match each phrasal verb to a one-word synonym and a situation from the students\' own day.'),
           ('10 min', 'Grammar focus: separable vs. inseparable, and the rule that pronouns go in the middle (turn it off).'),
           ('10 min', 'Controlled practice: gap-fill and rewrite sentences replacing formal verbs with phrasal verbs.'),
           ('10 min', 'Freer practice: students tell a partner about their routine or weekend using at least five of the verbs.')],
 'body': '''
<p>Phrasal verbs have a reputation as the part of English that "just has to be memorised". That's only half true. Students do need to learn each one as vocabulary, but the way you group, present and practise them decides whether they stick or disappear by next week.</p>

<h2>1. Group them by topic, never by particle or alphabet</h2>
<p>Lists like <em>"look after, look for, look into, look up"</em> are exactly how students end up confusing them — four verbs that look almost identical, taught at the same time. Group them by <strong>situation</strong> instead: a morning routine (<em>wake up, get up, put on, turn off</em>), travel (<em>check in, set off, get on, pick up</em>), relationships (<em>get on with, fall out, make up</em>). The topic gives each verb a memorable context and a reason to be used together in the same conversation.</p>

<h2>2. Meaning first, from context</h2>
<p>Present new phrasal verbs inside a short story or dialogue and ask students to guess the meaning before you explain anything. A one-word synonym helps — <em>find out = discover, give up = stop, put off = postpone</em> — and it also teaches a useful register point: the phrasal verb is usually the natural, spoken choice, and the one-word verb sounds more formal.</p>

<h2>3. Teach separable vs. inseparable with one rule students can use</h2>
<p>Most B1 students don't need the full theory. They need one rule that prevents the most common error: <strong>with a pronoun, separable verbs split</strong>. <em>"Turn off the light" / "Turn the light off" / "Turn it off"</em> — but never <em>"Turn off it."</em> Inseparable verbs never split: <em>"I look after my sister" / "I look after her."</em> Drill this with pronouns specifically, because nouns hide the problem.</p>

<h2>4. Recycle them, or lose them</h2>
<p>A phrasal verb met once is forgotten. Build them into warm-ups, reading texts and writing tasks for the next few lessons. A quick recycling game: say the one-word synonym (<em>"postpone!"</em>) and students race to give the phrasal verb (<em>"put off!"</em>).</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Pronoun in the wrong place:</strong> <em>"Can you pick up me?"</em> → <em>"Can you pick me up?"</em> Drill separable verbs with pronouns, not only nouns.</li>
  <li><strong>Particle dropped or changed:</strong> <em>"I'm looking my keys."</em> (for) — students translate the base verb and forget the particle is part of the meaning.</li>
  <li><strong>Literal interpretation:</strong> students read <em>"give up"</em> as giving something upwards. Always anchor meaning in a context sentence.</li>
  <li><strong>Wrong tense on the particle:</strong> <em>"She wake upped."</em> Only the verb changes: <em>woke up, has woken up</em>.</li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up story: guess 6-8 phrasal verbs from context.</li>
  <li><strong>10 min —</strong> Meaning: synonyms and personal situations.</li>
  <li><strong>10 min —</strong> Separable vs. inseparable, with pronouns.</li>
  <li><strong>10 min —</strong> Controlled practice: gap-fill and formal → phrasal rewrites.</li>
  <li><strong>10 min —</strong> Freer speaking about routines or weekends.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
''' + '\n'.join([
    W('phrasal-verbs-for-everyday-life-grammar', 'Phrasal Verbs for Everyday Life – Grammar', 'meaning, word order and separable verbs.'),
    W('phrasal-verbs-for-everyday-life-reading', 'Phrasal Verbs for Everyday Life – Reading', 'phrasal verbs in a connected text about daily life.'),
    W('phrasal-verbs-for-everyday-life-practice', 'Phrasal Verbs for Everyday Life – Practice', 'extra controlled practice and recycling.'),
    W('phrasal-verbs-for-everyday-life-writing', 'Phrasal Verbs for Everyday Life – Writing', 'freer production about the students\' own routines.'),
    W('phrasal-and-multi-word-verbs-grammar', 'Phrasal and Multi-Word Verbs – Grammar', 'the B2 next step: three-part verbs like get on with.'),
]) + '''
</ul>
<p>Browse all <a href="/worksheets/grammar/">grammar worksheets</a> or the full <a href="/worksheets/levels/b1/">B1 collection</a>.</p>
''',
},
# ─────────────────────────────── USED TO ───────────────────────────────
{
 'slug': 'how-to-teach-used-to',
 'title': 'How to Teach Used To for Past Habits (B1) | Workshido',
 'h1': 'How to Teach Used To: Past Habits and States for B1 Classes',
 'card': 'How to Teach Used To (Past Habits)',
 'description': 'Teach used to for past habits and states: didn\'t use to, questions, used to vs. past simple vs. be used to, common mistakes and free B1 worksheets.',
 'reading_time': '7 min read',
 'howto_name': 'How to Teach Used To in a 45-Minute Lesson',
 'steps': [('5 min', 'Warm-up: students compare a childhood photo (real or imagined) with today — what was different?'),
           ('10 min', 'Present used to + base verb for past habits and states, with a then/now timeline.'),
           ('10 min', 'Negatives and questions: didn\'t use to / Did you use to …? — the -d disappears after did.'),
           ('10 min', 'Contrast drill: used to (repeated or long-term) vs. past simple (one occasion, or with a number of times).'),
           ('10 min', 'Freer practice: students interview a partner about their childhood and report three changes.')],
 'body': '''
<p><em>Used to</em> is one of the most rewarding B1 structures to teach, because students immediately want to talk about themselves: how they used to be, what they used to do, what has changed. The structure itself is simple. The two things that go wrong are the spelling in negatives and questions, and knowing when <em>not</em> to use it.</p>

<h2>1. Start with a "then and now" comparison</h2>
<p>Draw a simple timeline with <em>then</em> on the left and <em>now</em> on the right. Talk about yourself: <em>"I used to live in a small town. Now I live in a city. I used to have long hair."</em> The key meaning to make visible is that the situation was true for a period in the past and <strong>is not true now</strong>. That contrast with the present is what makes <em>used to</em> different from a plain past simple.</p>

<h2>2. Habits and states — both work</h2>
<p><em>Used to</em> covers repeated actions (<em>I used to walk to school</em>) and long-term states (<em>I used to be shy, We used to have a dog</em>). This is worth pointing out because the alternative students may meet later — <em>would</em> for past habits — only works for actions, not states: <em>"I would be shy"</em> means something else entirely.</p>

<h2>3. Negatives and questions: where the -d goes</h2>
<p>The single most common written error is <em>"I didn't used to"</em>. Explain it with a rule students already know from the past simple: after <em>did</em> the verb goes back to its base form — <em>did go, did play</em> — so it's <em>didn't use to</em> and <em>Did you use to …?</em> A short transformation drill (affirmative → negative → question) fixes this quickly.</p>

<h2>4. Contrast it with past simple</h2>
<p>Students overuse <em>used to</em> once they learn it. Give them the boundary: use the past simple for a single event (<em>I went to Paris in 2019</em>) or when you say how many times (<em>I visited my grandmother three times</em>). <em>Used to</em> doesn't combine with a specific number of times or a single date.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>"Didn't used to":</strong> the -d stays after <em>did</em>. Link it to <em>didn't go</em>, not <em>didn't went</em>.</li>
  <li><strong>Using it for the present:</strong> <em>"I use to play tennis on Sundays."</em> For present habits, use the present simple: <em>I usually play</em>.</li>
  <li><strong>Confusing it with "be used to":</strong> <em>"I'm used to getting up early"</em> means it's normal for me, not a past habit. At B1, mention it only if students raise it, and keep the two apart on the board.</li>
  <li><strong>With a single event:</strong> <em>"I used to go to Rome last year."</em> → <em>I went to Rome last year.</em></li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up: then vs. now, from a childhood photo.</li>
  <li><strong>10 min —</strong> Present <em>used to</em> for habits and states on a timeline.</li>
  <li><strong>10 min —</strong> Negatives and questions: <em>didn't use to / Did you use to</em>.</li>
  <li><strong>10 min —</strong> Contrast drill with past simple.</li>
  <li><strong>10 min —</strong> Childhood interview and report back.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
''' + '\n'.join([
    W('used-to-past-habits-grammar', 'Used To (Past Habits) – Grammar', 'form, negatives, questions and the then/now contrast.'),
    W('used-to-past-habits-reading', 'Used To (Past Habits) – Reading', 'a text about how life used to be.'),
    W('used-to-past-habits-practice', 'Used To (Past Habits) – Practice', 'extra controlled practice and error correction.'),
    W('used-to-past-habits-writing', 'Used To (Past Habits) – Writing', 'students write about how their own life has changed.'),
]) + '''
</ul>
<p>Pair it with the <a href="/guides/how-to-teach-past-simple/">past simple guide</a> for the contrast stage, or browse the full <a href="/worksheets/levels/b1/">B1 collection</a>.</p>
''',
},
# ─────────────────────────────── PAST PERFECT ───────────────────────────────
{
 'slug': 'how-to-teach-past-perfect',
 'title': 'How to Teach the Past Perfect to B1 Classes | Workshido',
 'h1': 'How to Teach the Past Perfect: A Clear Guide for B1 Classes',
 'card': 'How to Teach the Past Perfect (B1)',
 'description': 'Teach the past perfect with timelines: had + past participle, "the earlier past", when you don\'t need it, common mistakes and free B1 worksheets.',
 'reading_time': '8 min read',
 'howto_name': 'How to Teach the Past Perfect in a 45-Minute Lesson',
 'steps': [('5 min', 'Warm-up: tell a short story out of order ("When I arrived, the train had left") and ask what happened first.'),
           ('10 min', 'Present had + past participle on a two-point timeline: past simple = the story, past perfect = the earlier past.'),
           ('10 min', 'Controlled practice: order two events, then join them with when, by the time, before or because.'),
           ('10 min', 'Contrast drill: decide whether the past perfect is needed or whether the sequence is already clear.'),
           ('10 min', 'Freer practice: students tell a "bad day" story in which things had already gone wrong before a key moment.')],
 'body': '''
<p>The past perfect is easy to form — <em>had</em> + past participle, the same for every person — and surprisingly hard for students to use, because many languages don't mark "the past before the past" at all. The goal isn't to make students use it everywhere. It's to help them see the one situation where it changes the meaning.</p>

<h2>1. Draw two points in the past, not one</h2>
<p>Every past perfect explanation should start with a timeline that has <strong>two</strong> past moments and "now". The story happens at the later point (past simple); the past perfect reaches back to something that happened before it. <em>"When I arrived at the station, the train had left."</em> Ask: did I see the train leave? No — it left first, and I arrived to find it gone. That meaning disappears with two past simples: <em>"When I arrived, the train left"</em> means it left at the moment I got there.</p>

<h2>2. Teach it inside stories</h2>
<p>The past perfect lives in narratives: stories, excuses, news reports, explanations of why something went wrong. <em>"I was hungry because I hadn't eaten all day." "By the time the police came, the thieves had escaped."</em> Present it inside a short story and let students find each past perfect and explain what happened first.</p>

<h2>3. Show when you don't need it</h2>
<p>A useful B1 insight — and a relief for students — is that when the order is already clear, the past simple is fine: <em>"I finished my homework and then I went out."</em> <em>Then, after</em> and <em>before</em> already show the sequence. The past perfect is essential when the sentence would otherwise mean something different, and useful with <em>by the time, already, because</em> and <em>when</em>.</p>

<h2>4. Negatives and questions come almost free</h2>
<p><em>Hadn't</em> + participle and <em>Had you …?</em> follow the same logic as the present perfect with <em>have</em>. If students already know the present perfect, point out that the past perfect is "the same structure, moved one step back in time".</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Overuse:</strong> students start using the past perfect for any past event (<em>"Yesterday I had gone to the cinema"</em>). Ask: before what? If there's no second past moment, it's past simple.</li>
  <li><strong>Wrong order of events:</strong> the past perfect on the later action (<em>"When the train had arrived, I left"</em> for "I had left before the train arrived"). Always draw the two points.</li>
  <li><strong>Past simple instead of participle:</strong> <em>"She had went."</em> Review irregular participles before the lesson.</li>
  <li><strong>Confusion with the present perfect:</strong> the present perfect connects to <em>now</em>; the past perfect connects to a moment in the past.</li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up: a story told out of order.</li>
  <li><strong>10 min —</strong> Two-point timeline: <em>had</em> + past participle.</li>
  <li><strong>10 min —</strong> Order and join events with <em>when, by the time, because</em>.</li>
  <li><strong>10 min —</strong> Needed or not? The sequence test.</li>
  <li><strong>10 min —</strong> "A bad day" stories.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
''' + '\n'.join([
    W('past-perfect-grammar', 'Past Perfect – Grammar', 'form, timelines and the earlier past.'),
    W('past-perfect-reading', 'Past Perfect – Reading', 'the past perfect inside a real narrative.'),
    W('past-perfect-practice', 'Past Perfect – Practice', 'extra practice: joining and ordering events.'),
    W('past-perfect-writing', 'Past Perfect – Writing', 'students write their own story.'),
    W('past-perfect-simple-and-past-perfect-continuous-grammar', 'Past Perfect Simple and Continuous – Grammar', 'the B2 next step.'),
]) + '''
</ul>
<p>See also the <a href="/guides/how-to-teach-present-perfect/">present perfect guide</a>, or browse the full <a href="/worksheets/levels/b1/">B1 collection</a>.</p>
''',
},
# ─────────────────────────────── LINKING WORDS ───────────────────────────────
{
 'slug': 'how-to-teach-linking-words',
 'title': 'How to Teach Linking Words (B1): Although, However | Workshido',
 'h1': 'How to Teach Linking Words: Although, However, Therefore and Whereas',
 'card': 'How to Teach Linking Words (B1)',
 'description': 'Teach linking words by function: because, so, therefore, although, however, while, whereas — with punctuation rules, mistakes and free B1 worksheets.',
 'reading_time': '8 min read',
 'howto_name': 'How to Teach Linking Words in a 45-Minute Lesson',
 'steps': [('5 min', 'Warm-up: show a paragraph with every linker removed and ask students why it is hard to follow.'),
           ('10 min', 'Sort linkers by function (reason, result, contrast, comparison) in a four-column chart.'),
           ('10 min', 'Punctuation focus: although inside the sentence vs. However, / Therefore, at the start of a new sentence.'),
           ('10 min', 'Controlled practice: join pairs of sentences with a given linker, then correct punctuation errors.'),
           ('10 min', 'Freer practice: a balanced opinion paragraph using at least five different linkers.')],
 'body': '''
<p>At B1, students start writing paragraphs instead of sentences — and suddenly their writing reads like a list. The missing piece is almost always linking words. The good news is that a small set of linkers, taught by <strong>function</strong> and with clear punctuation rules, transforms their writing quickly.</p>

<h2>1. Show the problem before the solution</h2>
<p>Give students a short paragraph with every linker removed: <em>"The hotel was cheap. It was very clean. We didn't like the area. We moved to another hotel."</em> Ask why it feels strange. Then show the linked version: <em>"Although the hotel was cheap, it was very clean. However, we didn't like the area, so we moved."</em> Students see immediately that linkers aren't decoration — they show the logic between ideas.</p>

<h2>2. Teach by function, not as a list</h2>
<p>Build a four-column chart on the board and keep it up all unit: <strong>reason</strong> (<em>because</em>), <strong>result</strong> (<em>so, therefore</em>), <strong>contrast</strong> (<em>but, although, however</em>) and <strong>comparison</strong> (<em>while, whereas</em>). When a student chooses the wrong linker, ask which column the idea belongs to. That question fixes most meaning errors on its own.</p>

<h2>3. Make punctuation part of the meaning</h2>
<p>The biggest difference between B1 and A2 writing is where linkers go in the sentence, and that is a punctuation issue:</p>
<ul>
  <li><em>because, so, although, while, whereas</em> join two clauses inside one sentence: <em>"It was late, so we took a taxi."</em></li>
  <li><em>However</em> and <em>Therefore</em> usually start a <strong>new</strong> sentence and take a comma: <em>"It was expensive. However, we bought it."</em></li>
  <li><em>Although</em> already contains the contrast, so it never needs <em>but</em>: <em>"Although he was tired, he finished."</em></li>
</ul>
<p>Error correction with these three rules is one of the most effective B1 writing activities you can run.</p>

<h2>4. Finish with a paragraph, not sentences</h2>
<p>Linkers only make sense in connected writing. Close the unit with a balanced opinion paragraph — a topic sentence, an argument for, an argument against, and a conclusion — where students must use at least five different linkers from the chart.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>"However" as a conjunction:</strong> <em>"It was cold, however we went out."</em> → a full stop (or semicolon) before <em>However,</em>.</li>
  <li><strong>"Although … but":</strong> double contrast. Delete <em>but</em>.</li>
  <li><strong>"Because of" + clause:</strong> <em>"because of she was late"</em> → <em>because she was late</em> (<em>because of</em> + noun).</li>
  <li><strong>Reason and result reversed:</strong> <em>"We stayed inside so it was raining."</em> Ask which column the idea belongs to.</li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up: the paragraph without linkers.</li>
  <li><strong>10 min —</strong> Sort linkers by function.</li>
  <li><strong>10 min —</strong> Punctuation: inside the sentence vs. starting a new one.</li>
  <li><strong>10 min —</strong> Join sentences and correct errors.</li>
  <li><strong>10 min —</strong> A balanced opinion paragraph.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
''' + '\n'.join([
    W('linking-words-and-paragraph-cohesion-grammar', 'Linking Words and Paragraph Cohesion – Grammar', 'function, joining and punctuation.'),
    W('linking-words-and-paragraph-cohesion-reading', 'Linking Words and Paragraph Cohesion – Reading', 'an article on online learning, analysed for linkers.'),
    W('linking-words-and-paragraph-cohesion-practice', 'Linking Words and Paragraph Cohesion – Practice', 'extra practice and error correction.'),
    W('linking-words-and-paragraph-cohesion-writing', 'Linking Words and Paragraph Cohesion – Writing', 'planning and writing a balanced opinion paragraph.'),
]) + '''
</ul>
<p>Premium members also get a full graded quiz for this set. Browse the full <a href="/worksheets/levels/b1/">B1 collection</a>.</p>
''',
},
]


def esc(s):
    return html.escape(s, quote=True)


def related_links(exclude_slug):
    """Enlaces 'More teaching guides' = los de la plantilla viva + las guías nuevas, sin la propia."""
    tpl = open(TEMPLATE, encoding='utf-8').read()
    block = re.search(r'<div class="guide-links">(.*?)</div>', tpl, re.S).group(1)
    links = re.findall(r'\s*<a class="guide-link" href="([^"]+)">(.*?)</a>', block)
    links = [(h, t) for h, t in links if h != '/workshido-index.html']
    links.insert(0, (f'/guides/{T_SLUG}/', 'How to Teach Conditionals: Zero, First, and Second for A2-B1'))
    links += [(f"/guides/{g['slug']}/", g['h1']) for g in GUIDES]
    out, seen = [], set()
    for h, t in links:
        if h == f'/guides/{exclude_slug}/' or h in seen:
            continue
        seen.add(h); out.append(f'    <a class="guide-link" href="{h}">{t}</a>')
    out.append('    <a class="guide-link" href="/workshido-index.html">Browse the full worksheet catalog →</a>')
    return '\n' + '\n'.join(out) + '\n  '


def build_page(g):
    s = open(TEMPLATE, encoding='utf-8').read()
    old_h1 = re.search(r'<h1>(.*?)</h1>', s).group(1)
    old_desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    old_title = re.search(r'<title>(.*?)</title>', s).group(1)
    s = s.replace(f'<title>{old_title}</title>', f'<title>{esc(g["title"])}</title>')
    s = s.replace(f'content="{old_title}"', f'content="{esc(g["title"])}"')
    s = s.replace(f'content="{old_desc}"', f'content="{esc(g["description"])}"')
    s = s.replace(f'/guides/{T_SLUG}/', f'/guides/{g["slug"]}/')
    # JSON-LD Article + Breadcrumb (texto plano dentro de JSON)
    s = s.replace(json.dumps(old_h1, ensure_ascii=False)[1:-1], json.dumps(g['h1'], ensure_ascii=False)[1:-1])
    s = s.replace(json.dumps(old_desc, ensure_ascii=False)[1:-1], json.dumps(g['description'], ensure_ascii=False)[1:-1])
    # HowTo
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": g['howto_name'], "description": g['description'],
             "step": [{"@type": "HowToStep", "name": n, "text": f"{n} — {t}"} for n, t in g['steps']], "totalTime": "PT45M"}
    s = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "HowTo".*?</script>',
               lambda m: '<script type="application/ld+json">' + json.dumps(howto, ensure_ascii=False) + '</script>', s, flags=re.S)
    # Hero, breadcrumb, artículo
    s = s.replace(f'<h1>{old_h1}</h1>', f'<h1>{g["h1"]}</h1>')
    s = s.replace(f'<span>{old_h1}</span>', f'<span>{g["h1"]}</span>')
    s = re.sub(r'<p class="article-desc">.*?</p>', lambda m: f'<p class="article-desc">{g["description"]}</p>', s, flags=re.S)
    s = re.sub(r'(<div class="article-meta">Teaching Guide · )[^<]*(</div>)', lambda m: m.group(1) + g['reading_time'] + m.group(2), s)
    s = re.sub(r'<article>.*?</article>', lambda m: '<article>\n' + g['body'] + '\n</article>', s, flags=re.S)
    s = re.sub(r'(<div class="guide-links">).*?(</div>)', lambda m: m.group(1) + related_links(g['slug']) + m.group(2), s, count=1, flags=re.S)
    # Guardas: nada de la plantilla debe sobrevivir
    for leftover in (T_SLUG, 'onditional', old_desc[:40]):
        assert leftover not in s.split('<div class="related-guides">')[0], (g['slug'], leftover)
    return s


def main():
    for g in GUIDES:
        d = os.path.join(REPO, 'guides', g['slug']); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(build_page(g))
        print('OK page', g['slug'])

    # Índice /guides/: tarjetas nuevas antes del cierre del grid (sin duplicar)
    p = os.path.join(REPO, 'guides', 'index.html'); s = open(p, encoding='utf-8').read()
    cards = ''.join(f'''    <a class="hub-card" href="/guides/{g["slug"]}/">
      <span class="hub-card-meta">{g["reading_time"]}</span>
      <span class="hub-card-title">{g["h1"]}</span>
      <span class="hub-card-desc">{g["description"]}</span>
    </a>
''' for g in GUIDES if f'/guides/{g["slug"]}/' not in s)
    if cards:
        anchor = '    <a class="hub-card" href="/guides/how-to-teach-conditionals/">'
        assert s.count(anchor) == 1
        s = s.replace(anchor, cards + anchor)
        open(p, 'w', encoding='utf-8').write(s)
    print('OK hub (+%d)' % cards.count('hub-card"'))

    # Sitemap
    p = os.path.join(REPO, 'netlify', 'functions', 'sitemap.js'); s = open(p, encoding='utf-8').read()
    anchor = "  { loc: '/guides/how-to-learn-irregular-verbs/', changefreq: 'monthly', priority: '0.6' },\n"
    assert s.count(anchor) == 1
    add = ''.join(f"  {{ loc: '/guides/{g['slug']}/', changefreq: 'monthly', priority: '0.6' }},\n" for g in GUIDES if f"/guides/{g['slug']}/" not in s)
    s = s.replace(anchor, anchor + add); open(p, 'w', encoding='utf-8').write(s)
    print('OK sitemap (+%d)' % add.count('loc:'))

    # llms.txt
    p = os.path.join(REPO, 'llms.txt'); s = open(p, encoding='utf-8').read()
    anchor = '- [CEFR Levels Explained ('
    assert s.count(anchor) == 1
    add = ''.join(f"- [{g['card']}](https://workshido.com/guides/{g['slug']}/)\n" for g in GUIDES if f"/guides/{g['slug']}/" not in s)
    s = s.replace(anchor, add + anchor); open(p, 'w', encoding='utf-8').write(s)
    print('OK llms.txt (+%d)' % add.count('- ['))

    # "More teaching guides" de las guías existentes (con bloque guide-links)
    n = 0
    for name in sorted(os.listdir(os.path.join(REPO, 'guides'))):
        p = os.path.join(REPO, 'guides', name, 'index.html')
        if name in [g['slug'] for g in GUIDES] or not os.path.exists(p):
            continue
        s = open(p, encoding='utf-8').read()
        anchor = '    <a class="guide-link" href="/workshido-index.html">Browse the full worksheet catalog →</a>'
        if s.count(anchor) != 1:
            print('   (sin bloque guide-links, se omite)', name); continue
        add = ''.join(f'    <a class="guide-link" href="/guides/{g["slug"]}/">{g["h1"]}</a>\n' for g in GUIDES if f'/guides/{g["slug"]}/' not in s)
        if add:
            s = s.replace(anchor, add + anchor); open(p, 'w', encoding='utf-8').write(s); n += 1
    print('OK related links en', n, 'guías existentes')


if __name__ == '__main__':
    main()
