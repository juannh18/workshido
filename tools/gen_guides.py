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
    {
        'slug': 'guides/how-to-teach-past-simple',
        'title': 'How to Teach Past Simple: Regular and Irregular Verbs for A1-A2 | Workshido',
        'description': 'A practical guide to teaching past simple to A1-A2 ESL students — how to sequence regular and irregular verbs, the -ed pronunciation rule, and common mistakes.',
        'h1': 'How to Teach Past Simple: Regular and Irregular Verbs for A1-A2',
        'reading_time': '6 min read',
        'body': '''
<p>Past simple hits students with two unrelated challenges at once: a spelling rule for regular verbs (add -ed, with a few twists) and a list of irregular forms that just have to be memorized. Teach both at the same time and most students default to over-regularizing everything — "goed," "buyed," "runned." The fix is sequencing, not more repetition.</p>

<h2>1. Separate regular from irregular completely at first</h2>
<p>Don't introduce a mixed list. Spend one full activity on regular verbs only (play → played, watch → watched, study → studied) until the -ed pattern feels automatic, then introduce irregular verbs as their own closed set, explicitly framed as "these don't follow the rule — you just have to know them." Mixing the two from day one is the single biggest reason students regularize irregular verbs for months.</p>

<h2>2. Teach the three -ed sounds explicitly</h2>
<p>-ed is pronounced three different ways — /t/ (watched), /d/ (played), /ɪd/ (wanted, needed) — and almost no A1-A2 course actually drills this as a listening/pronunciation point, even though it's entirely predictable from the final sound of the base verb. Five minutes sorting verbs by ending sound (voiceless consonant → /t/, voiced consonant/vowel → /d/, t/d → /ɪd/) pays off every time students read past simple text aloud afterward.</p>

<h2>3. Anchor the tense with time expressions, not just verb forms</h2>
<p>"Yesterday," "last week," "in 2020," "two days ago" give past simple a reason to exist instead of being an abstract verb-form drill. Have students build sentences that start from the time expression, not the verb — it also pre-empts the most common present-perfect confusion later ("I have seen him yesterday"), since past simple's time-anchored nature becomes obvious early.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Regularizing irregular verbs:</strong> "She goed to the park." — expected during the mixing stage; the fix is upstream (see point 1), not more correction in the moment.</li>
  <li><strong>Double marking with did:</strong> "Did she went?" — students add past marking to both the auxiliary and the main verb, same pattern as the do/does double-marking error in present simple. Point out that only did carries the past signal in questions and negatives; the main verb goes back to base form.</li>
  <li><strong>Confusing already/yet with past simple time markers:</strong> "I saw him already" instead of "I've already seen him" — a present perfect structure leaking into past simple territory. Usually resolves once present perfect is taught as its own contrastive lesson.</li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up: elicit what students did yesterday, in first person, no writing yet.</li>
  <li><strong>10 min —</strong> Regular verbs only: -ed spelling and the three pronunciation sounds.</li>
  <li><strong>10 min —</strong> Irregular verbs as a closed list: matching base form to past form, high repetition.</li>
  <li><strong>10 min —</strong> Controlled practice mixing both, now that each is solid individually.</li>
  <li><strong>10 min —</strong> Freer practice: students write or tell a partner about their weekend.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
  <li><a href="/workshido-worksheet.html?id=a1b62051-77bf-481d-8244-d4d0ff3c35d8">Regular Verbs in the Past Simple</a> (A1) — isolates the -ed spelling and sound rules.</li>
  <li><a href="/workshido-worksheet.html?id=5e9cfabd-bed3-411e-8516-5da083beea99">Irregular Verbs in the Past Simple</a> (A1) — closed-list drilling once regular forms are solid.</li>
  <li><a href="/workshido-worksheet.html?id=00cc48bf-4e17-4e3c-8260-4bbe683f1fbf">Past Simple – Grammar Focus</a> (A1) — full reference combining both once each is separately secure.</li>
  <li><a href="/workshido-worksheet.html?id=96fb9b61-cdbe-4abd-ae42-083e2d0f866d">Reading Comprehension – Past Simple</a> (A1) — receptive practice in context.</li>
  <li><a href="/workshido-worksheet.html?id=1889ff4e-a6f8-49c2-a69c-2c189d31d10b">Past Simple Tense</a> (A2) — mixed controlled practice, both verb types.</li>
  <li><a href="/workshido-worksheet.html?id=3f516e86-52a3-41aa-a8cf-17046310f48a">A Weekend Story – Past Simple Reading</a> (A2) — narrative context, good freer-stage lead-in.</li>
  <li><a href="/workshido-worksheet.html?id=34d90bdd-3d9f-49dc-aab8-e1f7a314ae03">Write About Yesterday – Past Simple Writing</a> (A2) — freer production to close the lesson.</li>
</ul>
<p>Browse the full set of <a href="/worksheets/grammar/">grammar worksheets</a> or filter by <a href="/worksheets/levels/a1/">A1</a> and <a href="/worksheets/levels/a2/">A2</a> level.</p>
''',
    },
    {
        'slug': 'guides/how-to-teach-present-perfect',
        'title': 'How to Teach Present Perfect: A Practical Guide for A2-B1 Classes | Workshido',
        'description': 'A practical guide to teaching present perfect — why it confuses students, how to sequence for/since and just/already/yet, and how to contrast it with past simple.',
        'h1': 'How to Teach Present Perfect: A Practical Guide for A2-B1 Classes',
        'reading_time': '8 min read',
        'body': '''
<p>Present perfect is the tense most likely to make an otherwise strong B1 student sound wrong, because the problem usually isn't grammar — it's translation. Many languages don't distinguish "an action connected to now" from "an action finished in the past" the way English does; they collapse both into one past tense. A student can conjugate "have/has + past participle" flawlessly and still choose the wrong tense every time, because they're translating the concept, not applying an English rule.</p>

<h2>1. Anchor the meaning as "connection to now," not "past time"</h2>
<p>Before touching form, spend real time on the concept: present perfect is used when the past action still matters right now — the result, the experience, the unfinished time period. Contrast two real classroom facts: "I taught here for three years" (finished, past simple) vs. "I have taught here for three years" (still true now, present perfect). Students need to hear the meaning difference before the form makes sense.</p>

<h2>2. Teach for/since and just/already/yet as separate mini-lessons</h2>
<p>These three sub-uses get taught as one grab-bag far too often, and that's what overwhelms students. Split them: "for" (duration) and "since" (starting point) is one lesson about time; "just," "already," and "yet" is a separate lesson about recency and completion, each with its own drill. Trying to teach all five words in the same 20 minutes is the most common reason students freeze when choosing between them.</p>

<h2>3. Contrast directly against past simple with minimal pairs</h2>
<p>Once the form is stable, the highest-value activity is minimal-pair contrast: the same information, one sentence in each tense. "I lost my keys yesterday" (past simple, finished, time-stamped) vs. "I have lost my keys" (present perfect, still lost right now, no time stamp). This is usually the moment the whole tense finally clicks — isolated present perfect practice rarely gets students there on its own.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Using present perfect with a finished-time expression:</strong> "I have seen him yesterday." — the single most common error, and a direct sign the student is translating a simple past from their L1. Redirect to "I saw him yesterday" and ask what changed (a specific finished time appeared, so past simple takes over).</li>
  <li><strong>Have/has confusion:</strong> "She have finished" — usually a leftover from present simple's he/she/it rule not being applied to the new auxiliary. Drill have/has in isolation before adding the past participle.</li>
  <li><strong>Irregular past participles:</strong> "I have went" instead of "I have gone" — students reach for the past simple form because it's more familiar. A participle-specific list, separate from the past simple irregular list, avoids the cross-contamination.</li>
</ul>

<h2>A 50-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up: two true sentences about the teacher, one past simple, one present perfect, ask students to spot the meaning difference.</li>
  <li><strong>10 min —</strong> Form drill: have/has + past participle, mixing regular and irregular participles.</li>
  <li><strong>10 min —</strong> For/since as its own focused practice block.</li>
  <li><strong>10 min —</strong> Just/already/yet as its own focused practice block.</li>
  <li><strong>10 min —</strong> Minimal-pair contrast against past simple.</li>
  <li><strong>5 min —</strong> Freer practice: "Have you ever...?" mingle activity.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
  <li><a href="/workshido-worksheet.html?id=7a65d22a-1db5-46b2-9966-ecdbaa5e3985">Present Perfect Tense (A2) – Grammar</a> — form introduction before the B1 sub-uses.</li>
  <li><a href="/workshido-worksheet.html?id=d21f4012-17fc-4ce3-879b-18dea5f2ce72">Present Perfect: For and Since – Grammar</a> (B1) — the duration/starting-point mini-lesson.</li>
  <li><a href="/workshido-worksheet.html?id=e4d1b1c0-56cb-4230-9c37-5efc7cb6dd35">Present Perfect: Just, Already &amp; Yet – Grammar</a> (B1) — the recency/completion mini-lesson.</li>
  <li><a href="/workshido-worksheet.html?id=0a872f36-3940-49b9-a820-d0d1772634b4">Present Perfect: Life Experiences – Grammar</a> (B1) — "have you ever" experience questions.</li>
  <li><a href="/workshido-worksheet.html?id=5ab381ef-b12e-472f-b8bb-31177f26acc2">Present Perfect vs. Past Simple – Grammar</a> (B1) — the minimal-pair contrast stage.</li>
  <li><a href="/workshido-worksheet.html?id=360d3f7c-d5b3-477b-863f-17379c592bd9">Experiences to Remember – Present Perfect Reading</a> (B1) — receptive practice in context.</li>
  <li><a href="/workshido-worksheet.html?id=7182f63f-c932-451f-8915-fea669f1aff6">Present Perfect: Life Experiences – Writing</a> (B1) — freer production to close the lesson.</li>
</ul>
<p>Browse the full set of <a href="/worksheets/grammar/">grammar worksheets</a> or filter by <a href="/worksheets/levels/a2/">A2</a> and B1 level.</p>
''',
    },
    {
        'slug': 'guides/how-to-teach-present-continuous',
        'title': 'How to Teach Present Continuous (Present Progressive) for A2 Classes | Workshido',
        'description': 'A practical guide to teaching present continuous — the -ing spelling rules, stative verbs that break the pattern, and how to contrast it with present simple.',
        'h1': 'How to Teach Present Continuous (Present Progressive) for A2 Classes',
        'reading_time': '6 min read',
        'body': '''
<p>Present continuous is usually taught right after present simple, and that's exactly why students mix the two up for weeks — "she is work at the hospital" instead of "she works" or "she is working." The tense itself (be + verb-ing) isn't hard to form; the hard part is knowing which of the two present tenses a situation actually calls for.</p>

<h2>1. Nail the -ing spelling rules before anything else</h2>
<p>Three patterns cover almost every case: double the final consonant after a single stressed vowel (run → running, sit → sitting), drop a silent -e (make → making, write → writing), and change -ie to -y (lie → lying, die → dying). Five minutes of transformation drilling here prevents spelling errors from distracting students during the more important meaning-focused practice later.</p>

<h2>2. Teach stative verbs as an explicit exception list</h2>
<p>Verbs like like, know, want, love, believe, and understand don't normally take the continuous form ("I am liking this" is a common, very noticeable A2 error) because they describe states, not actions in progress. This is rarely taught as its own point — usually students just meet the exceptions one at a time as errors come up. Teaching the stative-verb category explicitly, with a short list on the board, heads off months of scattered correction.</p>

<h2>3. Drill the contrast against present simple directly</h2>
<p>The real skill isn't forming present continuous — it's choosing it. Give students paired prompts and have them pick the tense: a permanent habit ("He works in a bank" — present simple) vs. something happening right now ("Look, he's answering the phone" — present continuous). Time expressions are a useful anchor here: "usually/every day/on Mondays" signals present simple, "now/right now/at the moment/look!" signals present continuous.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Missing the auxiliary be:</strong> "She working now." — very common when a student's L1 doesn't require a linking verb. Drill the full chunk "is/are + verb-ing" as one unit rather than teaching -ing in isolation.</li>
  <li><strong>Present continuous with stative verbs:</strong> "I am knowing the answer." — see point 2; the fix is the exception list, not repeated correction.</li>
  <li><strong>Present continuous for habits:</strong> "I am playing football every Sunday" instead of "I play football every Sunday" — usually a sign the student hasn't yet internalized which time expressions belong to which tense; go back to the contrast drill in point 3.</li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up: mime an action, students describe it ("You are writing").</li>
  <li><strong>10 min —</strong> -ing spelling rules, transformation drill only.</li>
  <li><strong>8 min —</strong> Stative verbs as an explicit exception list.</li>
  <li><strong>12 min —</strong> Contrast practice: present simple vs. present continuous, choosing the correct tense from context.</li>
  <li><strong>10 min —</strong> Freer practice: describe what's happening in a picture, or a "right now" classroom description.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
  <li><a href="/workshido-worksheet.html?id=1d236bc0-38f9-4b46-bb30-95d018efbf73">Present Continuous – Grammar Focus</a> (A2) — form introduction.</li>
  <li><a href="/workshido-worksheet.html?id=93b4f991-1635-45c0-b969-e077e42ac126">Present Continuous – Spelling &amp; Practice</a> (A2) — isolates the -ing spelling rules.</li>
  <li><a href="/workshido-worksheet.html?id=af1d60b9-39fd-494b-bca5-d184bf3eac2e">Present Simple vs. Present Continuous</a> (A2) — the contrast stage.</li>
  <li><a href="/workshido-worksheet.html?id=164fc5ec-ad00-4280-aa00-a6378b78f0cb">Present Continuous – Reading</a> (A2) — receptive practice in context.</li>
  <li><a href="/workshido-worksheet.html?id=8076079b-de0b-4479-90c9-c1640e9e06cf">What's Happening Now? – Present Continuous Speaking Practice</a> (A2) — freer oral production.</li>
  <li><a href="/workshido-worksheet.html?id=12e7fc47-238f-4919-bb4f-ba40f7a30d67">Present Continuous – Writing Practice</a> (A2) — freer written production.</li>
  <li><a href="/workshido-worksheet.html?id=3e86ba78-2359-4574-aa39-c63964aea988">Present Simple &amp; Present Continuous Review – Grammar</a> (B1) — consolidation once both are solid.</li>
</ul>
<p>Browse the full set of <a href="/worksheets/grammar/">grammar worksheets</a> or filter by <a href="/worksheets/levels/a2/">A2</a> level.</p>
''',
    },
    {
        'slug': 'guides/how-to-teach-comparatives-superlatives',
        'title': 'How to Teach Comparative and Superlative Adjectives for A1-A2 | Workshido',
        'description': 'A practical guide to teaching comparative and superlative adjectives — the syllable-counting rule, irregular forms, and the most common student mistakes.',
        'h1': 'How to Teach Comparative and Superlative Adjectives for A1-A2',
        'reading_time': '6 min read',
        'body': '''
<p>Comparatives and superlatives look like a simple spelling rule from the teacher's side of the desk, but students are actually managing three decisions at once: how many syllables does this adjective have, does that change its spelling, and is it one of the handful of words that ignores the rule entirely. Teaching the rule as one flat list is what produces "more taller" and "the most best."</p>

<h2>1. Teach the syllable-count rule with real classroom objects, not a chart</h2>
<p>The rule itself is simple — one syllable, add -er/-est (tall → taller → tallest); two or more syllables, use more/most (beautiful → more beautiful → most beautiful) — but it lands much better through comparison than memorization. Compare two students' heights, two pens' lengths, two backpacks' weights out loud as you introduce each form, so the grammar is attached to something real and countable in the room.</p>

<h2>2. Isolate irregular forms as their own short list</h2>
<p>Good/better/best, bad/worse/worst, far/farther(further)/farthest(furthest) don't follow either pattern and have to be memorized directly — treat them explicitly as "no rule, just learn these four," the same way irregular past simple verbs get isolated. Mixing them into general practice too early is what produces "gooder" and "bestest."</p>

<h2>3. Drill "the" + superlative + in/of as a fixed chunk</h2>
<p>Superlatives almost always need three things together: the article "the," the superlative form, and a following phrase with "in" (a place/group) or "of" (a set) — "the tallest student in the class," "the best of the three." Teaching the superlative form alone, without this surrounding chunk, is why students drop "the" or leave the sentence dangling without the in/of phrase.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Double marking:</strong> "more taller," "more easier" — students add both -er and more to the same adjective. Point out that an adjective only gets ONE comparison signal, never both, exactly like the do/does double-marking pattern in present simple questions.</li>
  <li><strong>Missing "the" with superlatives:</strong> "She is tallest in the class." — drill the full chunk in point 3 rather than the superlative form in isolation.</li>
  <li><strong>Regularizing irregular forms:</strong> "gooder," "bestest," "more good" — expected before the irregular list in point 2 is solid; not worth correcting in the moment if that lesson hasn't happened yet.</li>
</ul>

<h2>A 40-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up: compare two real objects or students out loud, no writing yet.</li>
  <li><strong>10 min —</strong> One-syllable -er/-est rule, drilling with real classroom comparisons.</li>
  <li><strong>10 min —</strong> Two-or-more-syllable more/most rule, same approach.</li>
  <li><strong>8 min —</strong> Irregular forms as an explicit short list.</li>
  <li><strong>7 min —</strong> Freer practice: students compare three classmates or three cities they know, using "the ___est/most ___ ... in/of ...".</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
  <li><a href="/workshido-worksheet.html?id=40a1d4f3-b043-4733-8e66-edc7e1345491">Comparative Adjectives – Grammar Focus</a> (A1) — the -er/more rule introduction.</li>
  <li><a href="/workshido-worksheet.html?id=bbc629f9-935e-43a9-89ee-0b1e441abb9e">Superlative Adjectives – Grammar Focus</a> (A1) — the -est/most rule introduction.</li>
  <li><a href="/workshido-worksheet.html?id=297173fd-0fe6-4fab-bc49-70cb5b154908">Comparative Adjectives – Practice</a> (A1) — controlled practice.</li>
  <li><a href="/workshido-worksheet.html?id=82cbfaf6-ac46-4e9c-b84c-4208b473778c">Comparative Adjectives – Reading Practice</a> (A1) — receptive practice in context.</li>
  <li><a href="/workshido-worksheet.html?id=e7dec3d9-b76e-4caf-bab4-f199e35f546d">Comparative and Superlative Review</a> (A2) — consolidation once both forms are solid.</li>
  <li><a href="/workshido-worksheet.html?id=ad58c5ce-b960-45a1-ab69-cc69f19ffe4d">Comparative &amp; Superlative Adjectives – Practice</a> (A2) — mixed extra practice.</li>
</ul>
<p>Browse the full set of <a href="/worksheets/grammar/">grammar worksheets</a> or filter by <a href="/worksheets/levels/a1/">A1</a> and <a href="/worksheets/levels/a2/">A2</a> level.</p>
''',
    },
    {
        'slug': 'guides/how-to-teach-reported-speech',
        'title': 'How to Teach Reported Speech for B1 Classes | Workshido',
        'description': 'A practical guide to teaching reported speech — how to isolate tense backshift, pronoun changes, and reported questions/commands instead of teaching them all at once.',
        'h1': 'How to Teach Reported Speech for B1 Classes',
        'reading_time': '7 min read',
        'body': '''
<p>Reported speech is rarely hard because of one rule — it's hard because it asks students to apply three transformations at the same time: shift the tense back, change the pronouns and possessives, and often change time/place words too ("today" becomes "that day," "here" becomes "there"). Teaching all three simultaneously from the first example is what produces reported sentences that are wrong in two or three places at once instead of just one.</p>

<h2>1. Isolate tense backshift first, with pronouns already matching</h2>
<p>Start with first-person quotes reported by the same person ("I am tired," she said → She said she was tired) so the pronoun doesn't have to change — only the tense does. This lets students focus entirely on the present→past, past→past perfect, will→would pattern before pronoun-switching adds a second variable.</p>

<h2>2. Add pronoun and possessive changes as a separate step</h2>
<p>Once backshift is automatic, move to third-person reporting ("I have lost my keys," he said → He said he had lost his keys), where I→he and my→his now have to change too. Naming this explicitly as "step two" — not folding it into the first lesson — keeps students from having to solve two problems in one sentence too early.</p>

<h2>3. Treat reported questions and reported commands as their own structures</h2>
<p>Reported questions drop the auxiliary and question word order ("Where do you live?" → She asked where I lived, not "where did I live"), and reported commands use told/asked + object + to-infinitive ("Close the door," she said → She told me to close the door). Both are different enough from reporting statements that they deserve their own practice block rather than being mixed into general reported-speech drilling.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Keeping question word order in reported questions:</strong> "She asked where did I live." — the single most common reported-speech error. Drill the word-order shift with 2-3 board examples, physically crossing out "did" each time to show it disappears.</li>
  <li><strong>Forgetting to backshift the tense:</strong> "He said he is tired" instead of "he was tired" — usually means step 1 (see above) wasn't drilled to automaticity before pronouns were added on top of it.</li>
  <li><strong>Wrong reporting verb:</strong> using "said" where "told" is needed ("She said me to wait") — told always takes a direct object (told + someone), said doesn't. Teach them as two different sentence patterns, not interchangeable synonyms.</li>
</ul>

<h2>A 50-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min —</strong> Warm-up: teacher reports something a student said earlier in the week, class identifies what changed.</li>
  <li><strong>10 min —</strong> Tense backshift only, same-person reporting so pronouns don't change.</li>
  <li><strong>10 min —</strong> Add third-person reporting: pronouns and possessives shift too.</li>
  <li><strong>10 min —</strong> Reported questions: word-order drill, crossing out "did/do/does."</li>
  <li><strong>10 min —</strong> Reported commands: told/asked + object + to-infinitive.</li>
  <li><strong>5 min —</strong> Freer practice: report a real classmate's answer to a question you ask aloud.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
  <li><a href="/workshido-worksheet.html?id=e463b99e-a776-42c0-b697-69b8794266a8">Reported Speech: Present Simple to Past Simple – Grammar</a> (B1) — isolates tense backshift with minimal pronoun changes.</li>
  <li><a href="/workshido-worksheet.html?id=9b8e388f-1ea6-44e8-bded-f86f1dfb213e">Reported Speech: Present Simple to Past Simple – Practice</a> (B1) — controlled backshift practice.</li>
  <li><a href="/workshido-worksheet.html?id=1230b2e8-2927-42da-9c2f-0411054b9887">Reported Questions and Commands (Reported Speech) – Grammar</a> (B1) — reported questions and told/asked + to-infinitive commands.</li>
  <li><a href="/workshido-worksheet.html?id=71ce167d-ac63-4d51-82bd-6950c1732b35">Reported Questions and Commands (Reported Speech) Practice – Grammar</a> (B1) — word-order-focused practice for reported questions.</li>
  <li><a href="/workshido-worksheet.html?id=83087583-ae8f-400e-9384-df99d1bd7ff7">Reported Questions and Commands (Reported Speech): Instructions from a School Trip Leader – Reading</a> (B1) — receptive practice in context.</li>
  <li><a href="/workshido-worksheet.html?id=11f56a84-487e-404b-969a-4641069807f2">Reported Questions and Commands (Reported Speech) – Writing</a> (B1) — freer production to close the lesson.</li>
</ul>
<p>Browse the full set of <a href="/worksheets/grammar/">grammar worksheets</a> or filter by B1 level in the <a href="/workshido-index.html">full catalog</a>.</p>
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
