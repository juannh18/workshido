"""Genera las Teaching Guides de Spanishido (/guides/<slug>/index.html + hub
/guides/index.html) en la carpeta del sitio Spanishido.

Mismo diseño que las guías de Workshido, con la marca de Spanishido (paleta
terracota, nav/footer propios, rutas /spanishido-*) y el tag ELE en metadatos.
Público: profesores de español (ELE). Nunca "ESL"/"English" como lo que se enseña.

Uso:
  python tools/gen_guides_spanishido.py
"""
import os, html

SITE_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Spanishido')
SITE = 'https://spanishido.com'
SUPABASE = 'https://trlavtvbglzugwjevuen.supabase.co'
V = '20260923'


def ws(slug, label, note):
    return f'<li><a href="/worksheet/{slug}/">{label}</a> (A1) &mdash; {note}</li>'


GUIDES = [
    {
        'slug': 'guides/how-to-teach-ser-vs-estar',
        'title': 'How to Teach Ser vs. Estar (and Hay) to A1 Spanish Classes | Spanishido',
        'description': 'A practical A1 guide to teaching ser, estar and hay in Spanish class (ELE): clear uses, common mistakes, a lesson plan and free worksheets.',
        'h1': 'How to Teach Ser vs. Estar (and Hay): A Practical Guide for A1 Spanish',
        'keywords': 'ser vs estar, hay vs estar, teaching ser and estar, A1 Spanish, ELE, Spanish grammar lesson',
        'reading_time': '8 min read',
        'body': '''
<p>Ser and estar are the first place where Spanish refuses to map onto English: two verbs for one "to be", and a third structure, <em>hay</em>, for "there is / there are". Students who learn a list of rules on day one usually still say <em>*Soy en casa</em> a week later. What works better is to build the three one at a time, each tied to one clear job, and only then put them side by side.</p>

<h2>1. Start with ser: who and what something is</h2>
<p>At A1, ser covers the things that describe <strong>identity</strong>: name, nationality and origin, profession, and the basic characteristics of a person or thing.</p>
<ul>
  <li><em>Soy Marta. Soy de Colombia. Soy profesora.</em></li>
  <li><em>Mi casa es grande. Los perros son simpáticos.</em></li>
  <li>Time and dates also use ser: <em>Son las tres. Hoy es lunes.</em></li>
</ul>
<p><strong>In class:</strong> teach ser through mini-profiles before you ever mention estar. Students introduce themselves and a classmate (<em>Él es Tom. Es de Chicago. Es estudiante.</em>). The conjugation (soy, eres, es, somos, sois, son) sticks faster when every form is attached to a real person in the room.</p>

<h2>2. Then estar: where something is and how someone is</h2>
<p>Keep estar to two jobs at A1: <strong>location</strong> and <strong>states or conditions</strong>.</p>
<ul>
  <li>Location: <em>El baño está al fondo. Estamos en clase.</em></li>
  <li>States: <em>Estoy cansado. ¿Cómo estás? La sopa está fría.</em></li>
</ul>
<p>A simple test students can apply themselves: <strong>"Can I answer the question <em>where?</em> or <em>how is it right now?</em>"</strong> If yes, it is estar. Physical and emotional states (<em>cansado, contento, enfermo, nervioso</em>) are the easiest entry point, because students already feel them.</p>

<h2>3. Hay: whether something exists</h2>
<p><em>Hay</em> answers "is there any?" and introduces something new. Estar locates something the listener already knows about. The article is the giveaway, and it is worth teaching as a mechanical signal:</p>
<ul>
  <li><strong>hay + un/una/unos/unas, numbers or no article:</strong> <em>Hay un banco en la plaza. Hay dos baños. Hay café.</em></li>
  <li><strong>el/la/los/las or a name + estar:</strong> <em>El banco está en la plaza. Madrid está en España.</em></li>
</ul>
<p><em>Hay</em> never changes for plural (<em>hay un libro, hay tres libros</em>), which students find reassuring after the ser/estar conjugations.</p>

<h2>4. Put them side by side only at the end</h2>
<p>Contrast works once each verb has its own "home". A short sorting task does most of the work: give students 12 sentence halves (<em>...de México, ...en la cocina, ...un parque cerca</em>) and have them decide ser, estar or hay, justifying each choice with the job it does (identity, location, state, existence).</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Ser for location:</strong> <em>*El museo es en el centro.</em> Point back to the "where?" test. (Events are the one exception students will meet later: <em>La fiesta es en mi casa</em>. Leave that for when it comes up.)</li>
  <li><strong>Estar for professions:</strong> <em>*Estoy profesor.</em> Professions are identity, so they take ser, with no article: <em>Soy profesor.</em></li>
  <li><strong>Hay with a definite article:</strong> <em>*Hay el libro en la mesa.</em> The definite article signals estar: <em>El libro está en la mesa.</em></li>
  <li><strong>Estar de for origin:</strong> <em>*Estoy de Texas.</em> Origin is identity: <em>Soy de Texas.</em></li>
</ul>
<div class="callout"><strong>A note on shortcuts:</strong> acronyms like DOCTOR/PLACE help some students, but they leak (<em>Es de noche</em>, <em>Está muerto</em>). At A1, the four questions (who/what, where, how right now, is there any) cover almost every sentence students will actually produce.</div>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min &mdash;</strong> Warm-up: students describe a famous person with ser (origin, profession, one adjective).</li>
  <li><strong>10 min &mdash;</strong> Estar for location with a classroom map: <em>¿Dónde está la puerta?</em></li>
  <li><strong>10 min &mdash;</strong> Hay vs. estar with a picture of a room: first <em>¿Qué hay?</em>, then <em>¿Dónde está la lámpara?</em></li>
  <li><strong>15 min &mdash;</strong> Controlled practice: ser/estar/hay sorting and gap-fill.</li>
  <li><strong>5 min &mdash;</strong> Exit ticket: three sentences about their own home, one with each structure.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<p>These printable PDFs follow the same order: ser first, hay and estar next, then the three together.</p>
<ul>
''' + '\n'.join([
            ws('verb-ser-to-be-spanish-grammar-worksheet-a1', 'Verb SER (to be) &ndash; Grammar', 'identity, origin, profession and description.'),
            ws('verb-ser-to-be-spanish-reading-worksheet-a1', 'Verb SER (to be) &ndash; Reading', 'three short profiles in context.'),
            ws('hay-vs-estar-spanish-grammar-worksheet-a1', 'Hay vs. Estar &ndash; Grammar', 'existence vs. location, with picture prompts.'),
            ws('hay-vs-estar-spanish-writing-worksheet-a1', 'Hay vs. Estar &ndash; Writing', 'describe a bedroom with hay and está/están.'),
            ws('ser-estar-hay-review-spanish-grammar-worksheet-a1', 'Ser, Estar &amp; Hay Review &ndash; Grammar', 'the three structures side by side.'),
            ws('ser-estar-hay-review-spanish-practice-worksheet-a1', 'Ser, Estar &amp; Hay Review &ndash; Practice', 'mixed choice and error correction.'),
            ws('describing-people-objects-places-ser-estar-hay-que-spanish-writing-worksheet-a1', 'Describing People, Objects &amp; Places &ndash; Writing', 'freer production to close the unit.'),
        ]) + '''
</ul>
<p>Browse all <a href="/worksheets/grammar/">Spanish grammar worksheets</a> or the full <a href="/worksheets/levels/a1/">A1 collection</a>.</p>
''',
    },
    {
        'slug': 'guides/how-to-teach-spanish-noun-gender-agreement',
        'title': 'How to Teach Spanish Noun Gender, Number & Agreement (A1) | Spanishido',
        'description': 'Teach Spanish noun gender, plurals, articles and adjective agreement at A1 (ELE): patterns, exceptions worth teaching, mistakes and free worksheets.',
        'h1': 'How to Teach Spanish Noun Gender, Number and Agreement at A1',
        'keywords': 'Spanish noun gender, Spanish plurals, adjective agreement Spanish, el la los las, A1 Spanish, ELE',
        'reading_time': '8 min read',
        'body': '''
<p>Gender and agreement are not one lesson; they are a habit students build over the whole of A1. Every noun comes with a gender, and the article and every adjective around it has to follow. The goal of the first lessons is not perfect accuracy but a reflex: <strong>learn every noun with its article</strong>, and look at the noun before choosing the adjective ending.</p>

<h2>1. Teach nouns with their article from day one</h2>
<p>Never write <em>mesa</em> on the board; write <em>la mesa</em>. Vocabulary lists, flashcards and labels in the classroom should all carry the article. It costs nothing at the start and saves months of correction later.</p>

<h2>2. The patterns that cover most nouns</h2>
<ul>
  <li><strong>-o is usually masculine:</strong> <em>el libro, el perro</em>. <strong>-a is usually feminine:</strong> <em>la casa, la silla</em>.</li>
  <li><strong>Endings that are reliably feminine:</strong> -ción/-sión, -dad/-tad, -tud: <em>la canción, la ciudad, la actitud</em>.</li>
  <li><strong>Endings that are usually masculine:</strong> -or and -aje: <em>el color, el viaje</em> (with <em>la flor</em> as the classic exception).</li>
  <li><strong>-e and consonants:</strong> no reliable rule at A1 (<em>la noche, el coche; la luz, el lápiz</em>). These are the nouns where "learn it with its article" matters most.</li>
</ul>

<h2>3. The handful of exceptions worth teaching early</h2>
<p>Only teach exceptions students will actually use this term: <em>el día, el mapa, el problema, el idioma</em> (masculine despite -a), and <em>la mano, la foto, la moto, la radio</em> (feminine despite -o). Present them as a short "rebels" list that stays on the classroom wall, not as a rule.</p>

<h2>4. Plurals: three rules</h2>
<ul>
  <li>Ends in a vowel: add <strong>-s</strong> (<em>libro &rarr; libros</em>).</li>
  <li>Ends in a consonant: add <strong>-es</strong> (<em>ciudad &rarr; ciudades, reloj &rarr; relojes</em>).</li>
  <li>Ends in <strong>-z</strong>: change to <strong>-ces</strong> (<em>lápiz &rarr; lápices, luz &rarr; luces</em>).</li>
</ul>
<p>Written accents can move or disappear in the plural (<em>canción &rarr; canciones, examen &rarr; exámenes</em>). At A1 this is best treated as spelling to notice, not a rule to explain.</p>

<h2>5. Agreement: articles and adjectives follow the noun</h2>
<p>Adjectives ending in -o have four forms (<em>alto, alta, altos, altas</em>). Adjectives ending in -e or a consonant have two (<em>grande/grandes, azul/azules</em>). Nationalities ending in a consonant are the exception students notice: <em>español, española, españoles, españolas</em>. Most descriptive adjectives also go <strong>after</strong> the noun: <em>una casa blanca</em>.</p>
<p><strong>In class:</strong> a "change one thing" drill works well. Show <em>el gato negro</em>, then change the noun (<em>la gata</em>, <em>los gatos</em>) and have students change everything else to match, out loud, before writing anything.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Gender by ending only:</strong> <em>*la problema, *el mano.</em> Send students back to the "rebels" list.</li>
  <li><strong>Adjective agreeing with the speaker, not the noun:</strong> a male student writing <em>*la casa es bonito</em>. Ask "what is <em>bonita</em> describing?"</li>
  <li><strong>Plural noun, singular adjective:</strong> <em>*los libros interesante.</em> Highlight every -s in the phrase with a colour: all or none.</li>
  <li><strong>Adjective before the noun by English habit:</strong> <em>*un rojo coche.</em></li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min &mdash;</strong> Warm-up: label objects in the classroom with el/la sticky notes.</li>
  <li><strong>10 min &mdash;</strong> Sort 20 nouns into masculine/feminine using the ending patterns, then find the rebels.</li>
  <li><strong>10 min &mdash;</strong> Plural rules with the same nouns.</li>
  <li><strong>15 min &mdash;</strong> Agreement: "change one thing" drill, then describe three objects in writing.</li>
  <li><strong>5 min &mdash;</strong> Error hunt: five sentences with one agreement mistake each.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
''' + '\n'.join([
            ws('noun-gender-number-spanish-grammar-worksheet-a1', 'Noun Gender &amp; Number &ndash; Grammar', 'masculine/feminine, singular/plural and el/la/los/las.'),
            ws('noun-gender-number-spanish-practice-worksheet-a1', 'Noun Gender &amp; Number &ndash; Practice', 'fast sorting and plural drills.'),
            ws('definite-indefinite-articles-spanish-grammar-worksheet-a1', 'Definite &amp; Indefinite Articles &ndash; Grammar', 'el/la/los/las vs. un/una/unos/unas.'),
            ws('definite-indefinite-articles-spanish-reading-worksheet-a1', 'Definite &amp; Indefinite Articles &ndash; Reading', 'articles in a classroom-and-house text.'),
            ws('adjective-agreement-spanish-grammar-worksheet-a1', 'Adjective Agreement &ndash; Grammar', 'adjectives that agree in gender and number.'),
            ws('adjective-agreement-spanish-writing-worksheet-a1', 'Adjective Agreement &ndash; Writing', 'a guided description of a person.'),
        ]) + '''
</ul>
<p>Browse all <a href="/worksheets/grammar/">Spanish grammar worksheets</a> or the full <a href="/worksheets/levels/a1/">A1 collection</a>.</p>
''',
    },
    {
        'slug': 'guides/how-to-teach-spanish-present-tense',
        'title': 'How to Teach the Spanish Present Tense (Regular & Irregular) | Spanishido',
        'description': 'Teach the Spanish present tense at A1 (ELE): -ar/-er/-ir endings, yo-go verbs, ir and stem changers, with mistakes, a lesson plan and free worksheets.',
        'h1': 'How to Teach the Spanish Present Tense: Regular and Common Irregular Verbs (A1)',
        'keywords': 'Spanish present tense, presente de indicativo, -ar -er -ir verbs, Spanish irregular verbs, stem-changing verbs, A1 Spanish, ELE',
        'reading_time': '9 min read',
        'body': '''
<p>The present tense (<em>presente de indicativo</em>) is where A1 students first meet Spanish verb endings, and it sets the pattern for every tense after it. The biggest early win is not memorising tables. It is understanding that <strong>the ending tells you who is doing the action</strong>, which is why Spanish can drop the subject pronoun.</p>

<h2>1. Teach -ar verbs first, and alone</h2>
<p>-ar verbs are the largest group and the most regular. Give them a full lesson before -er and -ir appear. <em>Hablar</em>: hablo, hablas, habla, hablamos, habláis, hablan.</p>
<p><strong>In class:</strong> point at a student and say the verb form only (<em>¿Hablas inglés?</em> &mdash; <em>Sí, hablo inglés</em>). Students learn quickly that <em>-as</em> means "you" and <em>-o</em> means "I" without a pronoun in sight.</p>

<h2>2. Add -er and -ir as "the same pattern, different vowel"</h2>
<p><em>Comer</em>: como, comes, come, comemos, coméis, comen. <em>Vivir</em>: vivo, vives, vive, vivimos, vivís, viven. -er and -ir share every ending except nosotros and vosotros, which is the one detail worth highlighting.</p>
<div class="callout"><strong>Vosotros or not?</strong> Many programmes in the Americas teach <em>ustedes</em> for all plural "you" and only recognise <em>vosotros</em>. Pick the variety your curriculum uses and be consistent. Just tell students the other form exists so it doesn't surprise them in a text.</div>

<h2>3. Irregulars: teach them in families, not one by one</h2>
<ul>
  <li><strong>Yo-go verbs</strong> are only irregular in the first person: <em>tengo, hago, pongo, salgo, vengo</em>. (Tener and venir are also stem-changers in other forms: <em>tienes, vienes</em>.)</li>
  <li><strong>Ir</strong> is fully irregular and too frequent to delay: <em>voy, vas, va, vamos, vais, van</em>.</li>
  <li><strong>Stem-changers</strong> (e&rarr;ie <em>querer: quiero</em>; o&rarr;ue <em>poder: puedo</em>; e&rarr;i <em>pedir: pido</em>) change in every form except nosotros and vosotros. The "boot" drawing, circling the four forms that change, is a visual most students remember.</li>
</ul>

<h2>4. Drop the pronoun, keep the meaning</h2>
<p>Students who say <em>Yo hablo, yo como, yo vivo</em> in every sentence are grammatically correct but sound unnatural. Once endings are secure, have them retell a short paragraph without any subject pronouns, then add one back only for contrast or emphasis (<em>Yo trabajo, pero él estudia</em>).</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Regularising irregulars:</strong> <em>*tieno, *hago</em> used correctly but <em>*quero</em>. Drill the yo form of each family on its own.</li>
  <li><strong>Infinitive instead of a conjugated form:</strong> <em>*Yo vivir en Texas.</em></li>
  <li><strong>An extra "do" in questions:</strong> <em>*¿Hace tú hablas español?</em> Spanish questions need no helper verb: <em>¿Hablas español?</em></li>
  <li><strong>Progressive for habits:</strong> <em>*Estoy trabajando en un banco</em> for a permanent job. The simple present covers habits and routines.</li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min &mdash;</strong> Warm-up: yes/no questions about habits (<em>¿Trabajas? ¿Comes carne?</em>).</li>
  <li><strong>10 min &mdash;</strong> Build the -ar table together from the answers students just gave.</li>
  <li><strong>10 min &mdash;</strong> -er/-ir: same pattern, spot the nosotros/vosotros difference.</li>
  <li><strong>15 min &mdash;</strong> Controlled practice, then a short paragraph about a classmate's week.</li>
  <li><strong>5 min &mdash;</strong> Irregular preview: tengo and voy, the two students will need tomorrow.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
''' + '\n'.join([
            ws('present-tense-regular-verbs-spanish-grammar-worksheet-a1', 'Present Tense Regular Verbs &ndash; Grammar', 'hablar, comer, vivir across all persons.'),
            ws('present-tense-regular-verbs-spanish-reading-worksheet-a1', 'Present Tense Regular Verbs &ndash; Reading', 'a daily routine text with regular verbs.'),
            ws('present-tense-regular-verbs-spanish-writing-worksheet-a1', 'Present Tense Regular Verbs &ndash; Writing', 'describe someone&rsquo;s routine with time expressions.'),
            ws('common-irregular-verbs-ir-hacer-tener-querer-spanish-grammar-worksheet-a1', 'Common Irregular Verbs (ir, hacer, tener, querer) &ndash; Grammar', 'the high-frequency irregulars.'),
            ws('common-irregular-verbs-ir-hacer-tener-querer-spanish-practice-worksheet-a1', 'Common Irregular Verbs &ndash; Practice', 'mixed exercises for extra repetition.'),
        ]) + '''
</ul>
<p>Browse all <a href="/worksheets/grammar/">Spanish grammar worksheets</a> or the full <a href="/worksheets/levels/a1/">A1 collection</a>.</p>
''',
    },
    {
        'slug': 'guides/how-to-teach-gustar',
        'title': 'How to Teach Gustar in Spanish Class (Me Gusta / Me Gustan) | Spanishido',
        'description': 'Teach gustar at A1 (ELE): me gusta vs. me gustan, indirect object pronouns, "a mí", encantar and preferir, with mistakes and free worksheets.',
        'h1': 'How to Teach Gustar: Me Gusta, Me Gustan and Talking About Likes (A1)',
        'keywords': 'how to teach gustar, me gusta me gustan, indirect object pronouns, encantar, A1 Spanish, ELE',
        'reading_time': '7 min read',
        'body': '''
<p>Gustar is the verb every beginner wants on day one and the one that breaks their English instinct. In English, <em>I</em> like <em>chocolate</em>. In Spanish, chocolate is the subject and does the pleasing: <em>Me gusta el chocolate</em>, literally "chocolate is pleasing to me". Once students see who the real subject is, gusta vs. gustan stops being a mystery.</p>

<h2>1. Show the real structure first</h2>
<p>Write it as three blocks on the board: <strong>(to whom) + gusta/gustan + (the thing liked)</strong>.</p>
<ul>
  <li><em>Me gusta el café.</em> &mdash; one thing &rarr; gusta</li>
  <li><em>Me gustan los perros.</em> &mdash; plural &rarr; gustan</li>
  <li><em>Me gusta bailar y cantar.</em> &mdash; activities (infinitives) are always gusta, even two of them.</li>
</ul>
<p>The verb agrees with the thing liked, never with the person. That single sentence is the whole rule.</p>

<h2>2. Then the pronouns: me, te, le, nos, os, les</h2>
<p>Introduce them as "the person who is pleased": <em>me gusta, te gusta, le gusta, nos gusta, os gusta, les gusta</em>. Keep the verb fixed and change only the pronoun first, so students don't try to conjugate gustar for the person.</p>

<h2>3. Add "a + person" for clarity and emphasis</h2>
<ul>
  <li>Clarity: <em>A Ana le gusta el tenis. A mis padres les gusta viajar.</em></li>
  <li>Emphasis and contrast: <em>A mí me gusta el fútbol, pero a ti no.</em></li>
</ul>
<p>Note that the pronoun stays even when the "a" phrase is there: <em>A Ana le gusta</em>, never <em>*A Ana gusta</em>.</p>

<h2>4. Encantar and preferir</h2>
<p><em>Encantar</em> works exactly like gustar and means "to love (a thing or activity)": <em>Me encantan las películas de terror.</em> <em>Preferir</em>, by contrast, is a normal (stem-changing) verb: <em>Prefiero el té.</em> Putting them side by side stops students from building <em>*Me prefiero</em>.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>English word order:</strong> <em>*Yo gusto el chocolate</em> (which actually means "I am pleasing to chocolate"). Rebuild it with the three blocks.</li>
  <li><strong>Agreeing with the person:</strong> <em>*Nos gustamos el cine.</em> The verb looks at the thing liked, not at "nosotros".</li>
  <li><strong>Missing article:</strong> <em>*Me gusta café.</em> Things you like in general take el/la/los/las: <em>Me gusta el café.</em></li>
  <li><strong>Missing pronoun after "a":</strong> <em>*A Juan gusta el rock.</em></li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min &mdash;</strong> Warm-up: thumbs up/down to pictures of food, sports and music.</li>
  <li><strong>10 min &mdash;</strong> The three-block structure, gusta vs. gustan sorting.</li>
  <li><strong>10 min &mdash;</strong> Pronouns with a class survey: <em>¿Te gusta...?</em></li>
  <li><strong>15 min &mdash;</strong> Report the survey: <em>A Sam le gustan los gatos, pero a Lucía no.</em></li>
  <li><strong>5 min &mdash;</strong> Encantar vs. preferir in two example sentences each.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
''' + '\n'.join([
            ws('the-verb-gustar-me-gusta-me-gustan-spanish-grammar-worksheet-a1', 'The Verb GUSTAR (Me Gusta / Me Gustan) &ndash; Grammar', 'pronouns and the gusta/gustan rule.'),
            ws('the-verb-gustar-me-gusta-me-gustan-spanish-reading-worksheet-a1', 'The Verb GUSTAR &ndash; Reading', 'four friends&rsquo; likes and dislikes.'),
            ws('the-verb-gustar-me-gusta-me-gustan-spanish-practice-worksheet-a1', 'The Verb GUSTAR &ndash; Practice', 'fill-in, error correction and dialogues.'),
            ws('likes-preferences-interests-gustar-encantar-preferir-spanish-grammar-worksheet-a1', 'Likes, Preferences &amp; Interests (Gustar, Encantar, Preferir) &ndash; Grammar', 'gustar, encantar and preferir together.'),
            ws('likes-preferences-interests-gustar-encantar-preferir-spanish-writing-worksheet-a1', 'Likes, Preferences &amp; Interests &ndash; Writing', 'a personal interests profile.'),
        ]) + '''
</ul>
<p>Browse all <a href="/worksheets/grammar/">Spanish grammar worksheets</a> or the full <a href="/worksheets/levels/a1/">A1 collection</a>.</p>
''',
    },
    {
        'slug': 'guides/how-to-teach-spanish-reflexive-verbs',
        'title': 'How to Teach Spanish Reflexive Verbs and Daily Routine (A1) | Spanishido',
        'description': 'Teach Spanish reflexive verbs at A1 (ELE) through the daily routine: me/te/se pronouns, placement, stem changes, mistakes and free worksheets.',
        'h1': 'How to Teach Spanish Reflexive Verbs Through the Daily Routine (A1)',
        'keywords': 'Spanish reflexive verbs, daily routine in Spanish, levantarse, me levanto, reflexive pronouns, A1 Spanish, ELE',
        'reading_time': '7 min read',
        'body': '''
<p>Reflexive verbs look intimidating in a grammar table and feel natural in a daily routine. <em>Me levanto, me ducho, me visto</em>: students have been doing these actions every morning of their lives. Teaching reflexives <strong>through the routine</strong> gives the pronoun a clear meaning: the action goes back to the person doing it.</p>

<h2>1. Start with the routine, not the rule</h2>
<p>Mime or show pictures of a morning: <em>me despierto, me levanto, me ducho, me lavo los dientes, me visto, me peino</em>. Students repeat in the first person only. The pronoun <em>me</em> becomes part of the chunk before anyone calls it a "reflexive pronoun".</p>

<h2>2. Then the full pronoun set: me, te, se, nos, os, se</h2>
<p>Build the table from one verb: <em>me levanto, te levantas, se levanta, nos levantamos, os levantáis, se levantan</em>. Two things to point out:</p>
<ul>
  <li>The pronoun and the verb ending always match the same person.</li>
  <li><em>Se</em> covers él, ella, usted, ellos, ellas and ustedes, so the verb ending is what tells you who.</li>
</ul>

<h2>3. Where the pronoun goes</h2>
<p>Before a conjugated verb: <em>Me levanto a las siete.</em> With an infinitive, it can attach to the end or go before the whole verb phrase: <em>Voy a ducharme</em> = <em>Me voy a duchar</em>. At A1, teach the attached form first; it keeps students from dropping the pronoun.</p>

<h2>4. Watch the stem changers inside the routine</h2>
<p>Several routine verbs change their stem: <em>despertarse &rarr; me despierto</em> (e&rarr;ie), <em>acostarse &rarr; me acuesto</em> (o&rarr;ue), <em>vestirse &rarr; me visto</em> (e&rarr;i). If students already know the "boot" pattern from the present tense, this is a quick reminder rather than new grammar.</p>

<h2>5. Body parts take the article, not a possessive</h2>
<p><em>Me lavo las manos</em>, not <em>*me lavo mis manos</em>. The reflexive pronoun already says whose hands they are.</p>

<h2>Common mistakes and how to catch them</h2>
<ul>
  <li><strong>Dropping the pronoun:</strong> <em>*Levanto a las siete.</em> (Without "me" it means you lift something else.)</li>
  <li><strong>Pronoun and ending don't match:</strong> <em>*Me levantas.</em> Have students underline both and check they point to the same person.</li>
  <li><strong>Frozen infinitive pronoun:</strong> <em>*Tengo que levantarse.</em> The pronoun changes with the person: <em>Tengo que levantarme.</em></li>
  <li><strong>Possessive with body parts:</strong> <em>*Me cepillo mis dientes.</em></li>
</ul>

<h2>A 45-minute lesson shape that works</h2>
<ol>
  <li><strong>5 min &mdash;</strong> Warm-up: mime a morning; students call out the verb.</li>
  <li><strong>10 min &mdash;</strong> Routine chunks in the first person, with times (<em>a las siete</em>).</li>
  <li><strong>10 min &mdash;</strong> Full pronoun table and a partner interview: <em>¿A qué hora te levantas?</em></li>
  <li><strong>15 min &mdash;</strong> Write a partner&rsquo;s routine in the third person with <em>primero, luego, después, por último</em>.</li>
  <li><strong>5 min &mdash;</strong> Error check: pronoun and ending must match.</li>
</ol>

<h2>Free worksheets for this lesson</h2>
<ul>
''' + '\n'.join([
            ws('reflexive-verbs-daily-routine-spanish-grammar-worksheet-a1', 'Reflexive Verbs &amp; Daily Routine &ndash; Grammar', 'pronouns with levantarse, ducharse, vestirse, acostarse.'),
            ws('reflexive-verbs-daily-routine-spanish-reading-worksheet-a1', 'Reflexive Verbs &amp; Daily Routine &ndash; Reading', 'a student&rsquo;s day in context.'),
            ws('reflexive-verbs-daily-routine-spanish-writing-worksheet-a1', 'Reflexive Verbs &amp; Daily Routine &ndash; Writing', 'write a routine across persons.'),
            ws('reflexive-verbs-daily-routine-spanish-practice-worksheet-a1', 'Reflexive Verbs &amp; Daily Routine &ndash; Practice', 'extra repetition on pronouns.'),
        ]) + '''
</ul>
<p>Pair this with the <a href="/guides/how-to-teach-spanish-present-tense/">present tense guide</a> for the stem-changing pattern, and browse the full <a href="/worksheets/levels/a1/">A1 collection</a>.</p>
''',
    },
    {
        'slug': 'guides/how-to-sequence-spanish-lessons',
        'title': 'How to Sequence a Spanish Topic: Grammar, Reading, Writing | Spanishido',
        'description': 'A practical order for teaching a Spanish (ELE) topic across several lessons: grammar, reading, writing and practice, with free worksheets for each stage.',
        'h1': 'How to Sequence a Spanish Topic: Grammar, Reading, Writing, Practice',
        'keywords': 'Spanish lesson sequence, how to plan Spanish lessons, ELE lesson planning, Spanish unit plan, A1 Spanish',
        'reading_time': '6 min read',
        'body': '''
<p>Most Spanish teachers don't run out of worksheets. They run out of worksheets that <em>connect</em>: a grammar sheet from one site, a reading from another, a writing task from a third, each at a slightly different level and focus. The topic gets taught, but in one crowded lesson that doesn't stick.</p>
<p>A more reliable approach is to treat every topic as a short sequence: one skill per lesson, in a fixed order, with the gap between classes doing part of the work.</p>

<h2>The order, and why it's in this order</h2>
<p>The sequence moves from <strong>recognising</strong> a structure to <strong>producing</strong> it, and from <strong>controlled</strong> practice to <strong>free</strong> practice.</p>
<table class="sequence-table">
  <thead><tr><th>Lesson</th><th>Worksheet</th><th>What it does</th></tr></thead>
  <tbody>
    <tr><td>1</td><td>Grammar</td><td>Meet and notice the rule with controlled exercises.</td></tr>
    <tr><td>2</td><td>Reading</td><td>See the structure inside a real Spanish text, carrying meaning.</td></tr>
    <tr><td>3</td><td>Writing</td><td>Produce the structure in a guided task.</td></tr>
    <tr><td>&mdash;</td><td>Practice <em>(optional)</em></td><td>Extra repetition: homework, warm-up or fast finishers.</td></tr>
  </tbody>
</table>

<h3>1. Grammar: meet the rule</h3>
<p>The grammar worksheet isolates the target form with a short explanation and controlled exercises. Put two example sentences on the board and elicit the rule before you confirm it; students remember a rule they helped build.</p>

<h3>2. Reading: see it working</h3>
<p>In the next lesson the same structure appears in a text. Students read for gist first, answer comprehension questions, and only then go back to notice the structure: "Underline every <em>está</em> and <em>hay</em> in the text. Why is each one used there?"</p>

<h3>3. Writing: produce it</h3>
<p>Production is the hardest step, so it comes once input is solid. The writing worksheets are guided (model text, word bank, sentence frames), so students produce the target structure instead of fighting a blank page. Put two or three success criteria on the board and have students self-check before handing in.</p>

<h3>Practice: optional reinforcement</h3>
<p>Most topics also have a Practice worksheet with mixed exercises on the same point. Use it for a group that needs more repetition, as homework, or as a warm-up recap. Skipping it is not cutting a corner.</p>

<h2>Why one skill per lesson</h2>
<p>Splitting a topic across lessons feels slower, but students forgetting a little between Tuesday and Thursday, and then having to recall the rule, is exactly what makes it stick. At A1, one skill per lesson also keeps the load manageable while students are still decoding much of what they read.</p>

<h2>On Spanishido, this sequence is a "set"</h2>
<p>Every topic in the catalogue has grammar, reading, writing and practice worksheets at the same CEFR level. Together that is a <strong>set</strong>: a ready-made mini-unit you can teach in order without assembling it yourself.</p>
<div class="callout">On any worksheet page, the <strong>"More on this topic"</strong> section shows the rest of that set. <a href="/worksheet/hay-vs-estar-spanish-grammar-worksheet-a1/">See a complete A1 set for hay vs. estar&nbsp;&rarr;</a></div>
<p>Every worksheet is free to download and print. Teacher Editions, with the full answer key and a lesson plan, are part of Premium.</p>

<h2>Adapt it to your class</h2>
<ul>
  <li>Run a short <strong>writing task first</strong> as a diagnostic.</li>
  <li><strong>Front-load the reading</strong> when a topic is vocabulary-heavy.</li>
  <li><strong>Combine grammar and reading</strong> in one lesson for a strong group.</li>
  <li>In a mixed-level class, keep everyone on the same grammar&ndash;reading&ndash;writing spine and give the practice sheet to early finishers.</li>
</ul>

<h2>Free worksheets to build your first set</h2>
<p>A complete A1 set for hay vs. estar, in teaching order:</p>
<ul>
''' + '\n'.join([
            ws('hay-vs-estar-spanish-grammar-worksheet-a1', 'Hay vs. Estar &ndash; Grammar', 'existence vs. location.'),
            ws('hay-vs-estar-spanish-reading-worksheet-a1', 'Hay vs. Estar &ndash; Reading', 'a room-by-room house tour.'),
            ws('hay-vs-estar-spanish-writing-worksheet-a1', 'Hay vs. Estar &ndash; Writing', 'describe a bedroom.'),
            ws('hay-vs-estar-spanish-practice-worksheet-a1', 'Hay vs. Estar &ndash; Practice', '24 fast items for extra repetition.'),
        ]) + '''
</ul>
<p>Then read the topic guide on <a href="/guides/how-to-teach-ser-vs-estar/">how to teach ser vs. estar</a>, or browse the full <a href="/worksheets/levels/a1/">A1 collection</a>.</p>
''',
    },
]

STYLE = '''<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --blue-900: #3B160A; --blue-800: #64230E; --blue-600: #A6401D; --blue-400: #CE6538;
    --blue-200: #EFAD86; --blue-100: #F6CBB0; --blue-50: #FBEDE5;
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
  .nav-links { display: flex; gap: 28px; list-style: none; }
  .nav-links a { font-size: 13px; color: var(--blue-100); text-decoration: none; font-weight: 500; }
  .nav-links a:hover { color: var(--white); }
  .nav-actions { display: flex; gap: 10px; align-items: center; }
  .btn-ghost { font-family: var(--font-body); font-size: 13px; font-weight: 500; color: var(--blue-100); background: transparent; border: 1px solid rgba(255,255,255,0.2); border-radius: var(--radius-sm); padding: 7px 16px; cursor: pointer; text-decoration: none; }
  .btn-white { font-family: var(--font-body); font-size: 13px; font-weight: 600; color: var(--blue-900); background: var(--white); border: none; border-radius: var(--radius-sm); padding: 7px 18px; cursor: pointer; text-decoration: none; }
  .breadcrumb { padding: 16px 32px; font-size: 13px; color: var(--gray-300); max-width: 760px; margin: 0 auto; }
  .breadcrumb a { color: var(--gray-600); text-decoration: none; }
  .breadcrumb span { margin: 0 6px; }
  .article-hero { padding: 24px 32px 8px; max-width: 760px; margin: 0 auto; }
  .article-meta { font-size: 12px; font-weight: 600; color: var(--teal-600); text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px; }
  .article-hero h1 { font-family: var(--font-display); font-size: clamp(26px, 4vw, 38px); font-weight: 700; color: var(--gray-900); line-height: 1.25; margin-bottom: 10px; }
  .article-desc { font-size: 16px; color: var(--gray-600); line-height: 1.6; }
  article { max-width: 760px; margin: 24px auto 0; padding: 0 32px 60px; font-size: 16px; line-height: 1.75; color: #333; }
  article h2 { font-family: var(--font-display); font-size: 21px; font-weight: 700; color: var(--blue-900); margin: 32px 0 12px; }
  article h3 { font-family: var(--font-display); font-size: 17px; font-weight: 600; color: var(--gray-900); margin: 24px 0 8px; }
  article p { margin-bottom: 16px; }
  article ul, article ol { margin: 0 0 16px 22px; }
  article li { margin-bottom: 8px; }
  article a { color: var(--blue-600); }
  article strong { color: var(--gray-900); }
  .sequence-table { width: 100%; border-collapse: collapse; margin: 8px 0 20px; font-size: 15px; }
  .sequence-table th, .sequence-table td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--gray-100); vertical-align: top; }
  .sequence-table th { font-family: var(--font-display); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--gray-600); }
  .sequence-table td:first-child { white-space: nowrap; font-weight: 600; color: var(--blue-900); }
  .callout { background: var(--blue-50); border: 1px solid var(--blue-100); border-radius: var(--radius-md); padding: 16px 18px; margin: 8px 0 20px; font-size: 15px; }
  .callout strong { color: var(--blue-900); }
  .related-guides { max-width: 760px; margin: 0 auto 60px; padding: 0 32px; }
  .related-guides h2 { font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--gray-900); margin-bottom: 14px; }
  .guide-links { display: flex; flex-direction: column; gap: 10px; }
  .guide-link { display: block; padding: 14px 18px; border: 1px solid var(--gray-100); border-radius: var(--radius-md); text-decoration: none; color: var(--blue-900); font-weight: 600; font-size: 14px; transition: border-color 0.15s, background 0.15s; }
  .guide-link:hover { border-color: var(--blue-200); background: var(--blue-50); }
  .hub-hero { text-align: center; padding: 56px 32px 40px; background: linear-gradient(160deg, var(--blue-900) 0%, var(--blue-800) 100%); }
  .hub-hero h1 { font-family: var(--font-display); font-size: clamp(28px, 4.5vw, 42px); font-weight: 700; color: var(--white); margin-bottom: 12px; }
  .hub-hero p { font-size: 16px; color: var(--blue-100); max-width: 540px; margin: 0 auto; }
  .hub-grid { max-width: 760px; margin: 40px auto 60px; padding: 0 32px; display: flex; flex-direction: column; gap: 16px; }
  .hub-card { display: flex; flex-direction: column; gap: 6px; padding: 20px 22px; border: 1px solid var(--gray-100); border-radius: var(--radius-lg); text-decoration: none; transition: border-color 0.15s, transform 0.15s; }
  .hub-card:hover { border-color: var(--blue-200); transform: translateY(-1px); }
  .hub-card-meta { font-size: 11px; font-weight: 600; color: var(--teal-600); text-transform: uppercase; letter-spacing: 0.5px; }
  .hub-card-title { font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--gray-900); }
  .hub-card-desc { font-size: 14px; color: var(--gray-600); line-height: 1.5; }
  html.ws-authed #navActions .btn-ghost,html.ws-authed #navActions .btn-primary,html.ws-authed #navActions .btn-primary-nav,html.ws-authed #navActions .btn-white{display:none!important}
  footer { background: linear-gradient(160deg, var(--blue-900) 0%, var(--blue-800) 60%, #5C2A12 100%); color: var(--blue-100); padding: 48px 32px 32px; }
  .footer-grid { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; margin-bottom: 40px; }
  .footer-logo { font-family: var(--font-display); font-size: 20px; font-weight: 700; color: var(--white); margin-bottom: 12px; }
  .footer-logo span { color: var(--blue-200); }
  .footer-desc { font-size: 13px; color: var(--blue-100); line-height: 1.7; max-width: 260px; }
  .footer-social { display: flex; gap: 10px; margin-top: 16px; }
  .footer-social a { display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.08); color: var(--blue-100); transition: background 0.15s, color 0.15s; }
  .footer-social a:hover { background: rgba(255,255,255,0.16); color: var(--white); }
  .footer-col h4 { font-size: 12px; font-weight: 600; color: var(--white); text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 14px; }
  .footer-col a { display: block; font-size: 13px; color: var(--blue-100); text-decoration: none; margin-bottom: 8px; transition: color 0.12s; }
  .footer-col a:hover { color: var(--white); }
  .footer-link-soon { display: block; font-size: 13px; color: rgba(246,203,176,0.45); margin-bottom: 8px; cursor: default; }
  .footer-link-soon small { font-size: 10px; opacity: 0.85; }
  .footer-bottom { border-top: 1px solid rgba(255,255,255,0.08); padding-top: 24px; display: flex; justify-content: space-between; font-size: 12px; color: var(--blue-200); }
  @media (max-width: 768px) { .nav-links { display: none; } .footer-grid { grid-template-columns: 1fr 1fr; } }
  @media (max-width: 480px) { nav { padding: 0 16px; } .breadcrumb, .article-hero, article, .related-guides, .hub-grid { padding-left: 16px; padding-right: 16px; } .footer-grid { grid-template-columns: 1fr; } .footer-bottom { flex-direction: column; gap: 6px; text-align: center; } }
</style>'''

AUTH_GUARD = '''<script>/* auth-flash guard: hide logged-out nav instantly for signed-in users */(function(){try{var now=Date.now()/1000;for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(!k||k.indexOf("-auth-token")<0)continue;var v=JSON.parse(localStorage.getItem(k)||"null")||{};var s=v.currentSession||v;var exp=s.expires_at||v.expires_at;if(s.access_token&&(!exp||exp>now)){document.documentElement.classList.add("ws-authed");setTimeout(function(){var n=document.getElementById("navActions");if(n&&!/profile|avatar|Log ?out/i.test(n.innerHTML))document.documentElement.classList.remove("ws-authed");},4500);break;}}}catch(e){}})();</script>'''

NAV = '''<nav>
  <a href="/spanishido-index.html" class="nav-logo">Spanish<span>ido</span></a>
  <ul class="nav-links">
    <li><a href="/spanishido-index.html">Browse Worksheets</a></li>
    <li><a href="/worksheets/grammar/">Grammar</a></li>
    <li><a href="/guides/">Teaching guides</a></li>
    <li><a href="/spanishido-forteachers.html">For teachers</a></li>
  </ul>
  <div class="nav-actions" id="navActions">
    <a href="/spanishido-login.html" class="btn-ghost">Log in</a>
    <a href="/spanishido-signup.html" class="btn-white">Sign up free</a>
  </div>
</nav>'''

FOOTER = '''<footer>
  <div class="footer-grid">
    <div>
      <div class="footer-logo">Spanish<span>ido</span></div>
      <p class="footer-desc">Free, high-quality Spanish worksheets for teachers and learners worldwide. Download, print, and teach.</p>
      <div class="footer-social">
        <a href="https://www.instagram.com/spanishido.teachers/" target="_blank" rel="noopener" aria-label="Spanishido on Instagram">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.6" cy="6.4" r="1.1" fill="currentColor" stroke="none"/></svg>
        </a>
      </div>
    </div>
    <div class="footer-col">
      <h4>Browse</h4>
      <a href="/worksheets/grammar/">Grammar</a>
      <a href="/worksheets/vocabulary/">Vocabulary</a>
      <a href="/worksheets/reading/">Reading</a>
      <a href="/worksheets/writing/">Writing</a>
      <a href="/spanishido-index.html?topic=practice">Practice</a>
    </div>
    <div class="footer-col">
      <h4>Levels</h4>
      <a href="/worksheets/levels/a1/">A1 Beginner</a>
      <a href="/worksheets/levels/a2/">A2 Elementary</a>
      <a href="/worksheets/levels/b1/">B1 Intermediate</a>
      <span class="footer-link-soon" title="B2 worksheets are coming soon">B2 Upper-intermediate <small>(coming soon)</small></span>
      <span class="footer-link-soon" title="C1 worksheets are coming soon">C1 Advanced <small>(coming soon)</small></span>
    </div>
    <div class="footer-col">
      <h4>Company</h4>
      <a href="/spanishido-forteachers.html">For teachers</a>
      <a href="/guides/">Teaching guides</a>
      <a href="/about/">About</a>
      <a href="/spanishido-pricing.html">Premium</a>
      <a href="mailto:hola@spanishido.com">Contact</a>
      <a href="/spanishido-privacy.html">Privacy</a>
      <a href="/spanishido-terms.html">Terms</a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; <span id="yr"></span> Spanishido. All rights reserved.</span>
    <span>Made with &hearts; for teachers worldwide</span>
  </div>
</footer>'''

SCRIPTS = f'''<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.110.7" defer></script>
<script src="/js/guides-auth.js?v={V}" defer></script>
<script src="/js/analytics.js?v={V}" defer></script>
<script>var __y=document.getElementById('yr');if(__y)__y.textContent=new Date().getFullYear();</script>'''


def head(title, description, url, keywords, og_type, ld):
    e = html.escape
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="keywords" content="{e(keywords)}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="Spanishido">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(description)}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<meta name="theme-color" content="#3B160A">
{ld}
<link rel="preconnect" href="{SUPABASE}" crossorigin>
<link rel="preload" href="/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/sora-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/fonts/fonts.css?v=20260908">
{STYLE}
</head>
<body>
{AUTH_GUARD}
{NAV}'''


def ld_json(obj):
    import json
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace('</', '<\\/') + '</script>'


# Guide slug -> (hub slug, name); mirrors the hubs in Spanishido's netlify/lib/topics.js.
TOPIC_HUBS = {
    'guides/how-to-teach-ser-vs-estar': ('ser-vs-estar', 'Ser vs. Estar'),
    'guides/how-to-teach-spanish-present-tense': ('spanish-present-tense', 'Spanish Present Tense'),
    'guides/how-to-teach-gustar': ('gustar', 'Gustar'),
}


def topic_hub_link(g):
    h = TOPIC_HUBS.get(g['slug'])
    if not h:
        return ''
    return (f'<p class="topic-hub-link">📚 <a href="/worksheets/topics/{h[0]}/"><strong>See all {h[1]} worksheets</strong></a>'
            ' — every grammar, reading, writing and practice sheet on this point, grouped by CEFR level.</p>' + chr(10))


def render_page(g, others):
    url = f"{SITE}/{g['slug']}/"
    ld = ld_json({
        '@context': 'https://schema.org', '@type': 'Article', 'headline': g['h1'], 'description': g['description'],
        'keywords': g['keywords'], 'inLanguage': 'en', 'about': 'Teaching Spanish as a foreign language (ELE)',
        'author': {'@type': 'Organization', 'name': 'Spanishido'},
        'publisher': {'@type': 'Organization', 'name': 'Spanishido', 'logo': {'@type': 'ImageObject', 'url': f'{SITE}/favicon-192.png'}},
        'mainEntityOfPage': url,
    }) + '\n' + ld_json({
        '@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Teaching Guides', 'item': f'{SITE}/guides/'},
            {'@type': 'ListItem', 'position': 2, 'name': g['h1'], 'item': url},
        ]})
    related = '\n    '.join(f'<a class="guide-link" href="/{o["slug"]}/">{o["h1"]}</a>' for o in others)
    return head(g['title'], g['description'], url, g['keywords'], 'article', ld) + f'''
<div class="breadcrumb" role="navigation" aria-label="Breadcrumb">
  <a href="/guides/">Teaching guides</a>
  <span>&rsaquo;</span>
  <span>{g['h1']}</span>
</div>
<main>
<div class="article-hero">
  <div class="article-meta">Teaching Guide &middot; Spanish (ELE) &middot; {g['reading_time']}</div>
  <h1>{g['h1']}</h1>
  <p class="article-desc">{g['description']}</p>
</div>
<article>
{g['body']}
{topic_hub_link(g)}</article>
<div class="related-guides">
  <h2>More teaching guides</h2>
  <div class="guide-links">
    {related}
    <a class="guide-link" href="/spanishido-index.html">Browse the full worksheet catalog &rarr;</a>
  </div>
</div>
</main>
{FOOTER}
{SCRIPTS}
</body>
</html>
'''


def render_hub():
    url = f'{SITE}/guides/'
    title = 'Teaching Guides for Spanish Teachers (ELE) | Spanishido'
    desc = 'Free, practical guides for Spanish teachers (ELE): how to teach ser vs. estar, gender and agreement, the present tense, gustar and more at A1.'
    ld = ld_json({'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'Teaching Guides for Spanish Teachers',
                  'url': url, 'isPartOf': {'@type': 'WebSite', 'name': 'Spanishido', 'url': f'{SITE}/'}})
    cards = '\n    '.join(f'''<a class="hub-card" href="/{g["slug"]}/">
      <span class="hub-card-meta">{'All levels' if 'sequence' in g['slug'] else 'A1'} &middot; {g['reading_time']}</span>
      <span class="hub-card-title">{g['h1']}</span>
      <span class="hub-card-desc">{g['description']}</span>
    </a>''' for g in GUIDES)
    return head(title, desc, url, 'Spanish teaching guides, ELE, teaching Spanish as a foreign language, A1 Spanish lesson plans', 'website', ld) + f'''
<main>
<section class="hub-hero">
  <h1>Teaching Guides</h1>
  <p>Practical guides for Spanish teachers (ELE): how to teach the grammar points that trip up beginners, with lesson shapes and free worksheets.</p>
</section>
<div class="hub-grid">
    {cards}
</div>
</main>
{FOOTER}
{SCRIPTS}
</body>
</html>
'''


def main():
    for g in GUIDES:
        assert len(g['description']) <= 160, (g['slug'], len(g['description']))
        others = [o for o in GUIDES if o['slug'] != g['slug']]
        out_dir = os.path.join(SITE_ROOT, g['slug'])
        os.makedirs(out_dir, exist_ok=True)
        page = render_page(g, others)
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(page)
        print(f"OK: {g['slug']}/index.html ({len(page)} chars)")
    hub = render_hub()
    with open(os.path.join(SITE_ROOT, 'guides', 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(hub)
    print(f'OK: guides/index.html ({len(hub)} chars)')


if __name__ == '__main__':
    main()
    # Fechas (datePublished/dateModified + 'Updated' visible) — ver tools/guide_dates.py
    import guide_dates
    guide_dates.stamp_site(SITE_ROOT)
