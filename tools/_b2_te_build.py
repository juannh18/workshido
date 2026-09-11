# -*- coding: utf-8 -*-
"""Build the 20 B2 Teacher-Edition content JSONs for the Sep-2026 batch
(Advanced Articles & Determiners, Advanced Quantifiers, Contrast & Concession,
Cause/Reason/Purpose/Result, Advanced Comparison). One dict per worksheet ->
tools/te_content/te_<topic>_<type>_b2.json  (schema: tools/build_te.py)."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "te_content")
DASH, ARR, BUL = "&ndash;", "&rarr;", "&bull;"

def info(skill, topic, exercises):
    return [["Level", "B2"], ["Skill", skill], ["Topic", topic],
            ["Exercises", exercises], ["Est. Time", "45&ndash;50 minutes"],
            ["Answer Key", "Included above"]]

MAT_G = ["Printed worksheet copies (1 per student)", "Pens or pencils",
         "Board for the target structures and example sentences"]
MAT_R = ["Printed worksheet copies (1 per student)", "Pens or pencils",
         "Board for pre-teaching key vocabulary", "Dictionaries (optional, for Language in context)"]
MAT_W = ["Printed worksheet copies (1 per student)", "Pens or pencils",
         "Board for the model paragraph and useful language", "Lined paper for a second draft (optional)"]

LT = "Lesson Plan (45&ndash;50 minutes)"

def w(d):
    path = os.path.join(OUT, d["_file"])
    dd = {k: v for k, v in d.items() if not k.startswith("_")}
    json.dump(dd, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote", d["_file"])

TES = []

# =====================================================================
# 1. ADVANCED ARTICLES AND DETERMINERS
# =====================================================================
TES.append({
 "_file": "te_articles_grammar_b2.json",
 "ws_title": "Advanced Articles and Determiners " + BUL + " Grammar " + BUL + " B2",
 "info_rows": info("Grammar", "Generic reference, institutions, geographical names and abstract nouns", "6 (A" + DASH + "F)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Grammar focus</div><p>Reference box &ndash; no written answers. Check students can state each rule (generic reference, institutions, geographical names, abstract nouns).</p>"
  "<div class='ex-title'>B. Choose the correct option</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> A &ndash; a</div>"
  "<div class='ans-item'><span class='n'>2.</span> C &ndash; &mdash; (institution)</div>"
  "<div class='ans-item'><span class='n'>3.</span> C &ndash; &mdash;</div>"
  "<div class='ans-item'><span class='n'>4.</span> C &ndash; &mdash; (institution)</div>"
  "<div class='ans-item'><span class='n'>5.</span> B &ndash; the (most of the&hellip;)</div>"
  "<div class='ans-item'><span class='n'>6.</span> B &ndash; the (superlative)</div>"
  "<div class='ans-item'><span class='n'>7.</span> A &ndash; a/an</div>"
  "<div class='ans-item'><span class='n'>8.</span> C &ndash; &mdash; (institution)</div>"
  "<div class='ans-item'><span class='n'>9.</span> C &ndash; &mdash;</div>"
  "<div class='ans-item'><span class='n'>10.</span> C &ndash; &mdash; (accept A)</div></div>"
  "<div class='ex-title'>C. Complete the sentences</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> &mdash;</div>"
  "<div class='ans-item'><span class='n'>2.</span> &mdash; (in hospital)</div>"
  "<div class='ans-item'><span class='n'>3.</span> a</div>"
  "<div class='ans-item'><span class='n'>4.</span> &mdash; / a little</div>"
  "<div class='ans-item'><span class='n'>5.</span> The</div>"
  "<div class='ans-item'><span class='n'>6.</span> &mdash; (to school)</div>"
  "<div class='ans-item'><span class='n'>7.</span> &mdash; (little evidence)</div>"
  "<div class='ans-item'><span class='n'>8.</span> a (a great deal of)</div></div>"
  "<div class='ex-title'>D. Complete the text</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> &mdash;</div><div class='ans-item'><span class='n'>2.</span> &mdash; / The</div>"
  "<div class='ans-item'><span class='n'>3.</span> &mdash;</div><div class='ans-item'><span class='n'>4.</span> &mdash;</div>"
  "<div class='ans-item'><span class='n'>5.</span> the</div><div class='ans-item'><span class='n'>6.</span> the</div>"
  "<div class='ans-item'><span class='n'>7.</span> the</div><div class='ans-item'><span class='n'>8.</span> &mdash;</div>"
  "<div class='ans-item'><span class='n'>9.</span> the</div><div class='ans-item'><span class='n'>10.</span> &mdash; / the</div></div>"
  "<div class='ex-title'>E. Find and correct the mistake</div><ul class='ans'>"
  "<li><span class='n'>1.</span> Freedom <b>is</b> essential for a thriving society. (agreement: <i>are</i> &rarr; <i>is</i>; the abstract noun itself is correct with zero article)</li>"
  "<li><span class='n'>2.</span> She went to <b>&mdash;</b> university in London. (institution &ndash; drop <i>the</i>)</li>"
  "<li><span class='n'>3.</span> <b>&mdash;</b> Life in modern cities can be stressful. (general &ndash; drop <i>The</i>)</li>"
  "<li><span class='n'>4.</span> He is in <b>&mdash;</b> prison for financial crimes. (institution &ndash; drop <i>the</i>)</li>"
  "<li><span class='n'>5.</span> Most people agree on <b>the</b> importance of education. (specific &ndash; add <i>the</i>)</li>"
  "<li><span class='n'>6.</span> Asia is <b>the</b> largest continent in the world. (superlative &ndash; add <i>the</i>)</li></ul>"
  "<div class='ex-title'>F. Short production</div><p>Accept any accurate sentence, e.g. <b>1.</b> My brother is in hospital after an accident. <b>2.</b> The government should invest more in equality. <b>3.</b> The Nile flows through several countries in Africa.</p>"
 ),
 "teacher_tip": "The five boxes in the Grammar focus each map to one exercise pattern. Before Exercises B and C, have students name which box applies (institution? geographical name? abstract noun?) and then choose &ndash; this stops them guessing article by &ldquo;sound&rdquo;.",
 "mistakes": [
  ["She is studying at the university, not working.", "She is studying at university, not working."],
  ["The life is difficult for many families.", "Life is difficult for many families."],
  ["We travelled across the Asia last summer.", "We travelled across Asia last summer."],
  ["He showed the great patience during the talks.", "He showed great patience during the talks."]
 ],
 "activity_title": "Article Auction (8 min)",
 "activity_body": "Read out ten short sentences, some correct and some with an article error (e.g. &ldquo;She works for the government&rdquo;, &ldquo;He is the in prison&rdquo;, &ldquo;We visited the Mount Everest&rdquo;). Teams &ldquo;buy&rdquo; a sentence only if they think it is correct; if it is wrong they must say the fix. Award points for correct buys and correct fixes.",
 "materials": MAT_G,
 "lesson_title": LT,
 "learning_objective": "Students will be able to choose zero article, a/an or the with generic references, institutions, geographical names and abstract nouns, and correct common article and determiner errors in extended text.",
 "success_criteria": "I can use zero article for institutions used for their purpose and for abstract nouns in general. I can use <i>the</i> with rivers, seas, ranges and plural country names, zero article with continents and most countries, and <i>the</i> when an abstract noun is made specific.",
 "prior_knowledge": "Basic a/an vs the (A2); countable and uncountable nouns.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;He is in ___ prison&rdquo; and &ldquo;He visited his brother in ___ prison&rdquo;. Elicit the difference (purpose vs building) and why one takes zero article. Part 2: write four place names on the board (the Netherlands, Asia, the Nile, Mount Fuji) and ask which need <i>the</i> and why."],
  ["8 min", "Presentation (I Do)", "Explain the four systems with the &ldquo;why&rdquo; each time. (1) <b>Generic reference:</b> countable and uncountable nouns talked about in general take zero article, because we mean the whole idea, not one example (&ldquo;Computers have changed the way we work&rdquo;); use <i>the</i> + singular only to mean a whole species (&ldquo;The tiger is endangered&rdquo;). (2) <b>Institutions:</b> zero article when someone is there for the institution&rsquo;s purpose (in <i>hospital</i> as a patient, at <i>university</i> to study), but <i>the</i> for the building or a specific one. (3) <b>Geographical names:</b> <i>the</i> with rivers, seas, deserts, mountain ranges, island groups and plural / &ldquo;union&rdquo; country names (the Netherlands, the United Kingdom); zero article with continents, most countries, single mountains, lakes and cities &ndash; the pattern follows whether the name is felt as one place or a group. (4) <b>Abstract nouns:</b> zero article for a quality or idea in general (&ldquo;Freedom is important&rdquo;), but <i>the</i> for a specific instance (&ldquo;the importance of education&rdquo;). Model Exercise E item 3: &ldquo;The life in modern cities&rdquo; &rarr; general, so drop <i>the</i>."],
  ["10 min", "Guided Practice (We Do)", "Exercise B as a class: for each item, name the rule box first, then choose A/B/C. Then start Exercise D together, deciding items 1&ndash;4 with the class and giving the reason each time."],
  ["10 min", "Independent Practice (You Do)", "Students finish Exercise D and do Exercise C and Exercise E individually, then compare Exercise E in pairs, stating the rule for each correction."],
  ["7 min", "Assessment", "Review Exercise E on the board; students must name the category (institution / abstract / superlative / agreement) for each fix. Then the Exit Ticket individually."],
  ["5 min", "Closure", "Students write one sentence each for Exercise F item 3 (a geographical name with the correct article) and read two or three aloud for class checking."]
 ],
 "followup": "Homework: write a short paragraph about public services in your area, using at least one institution with zero article, one geographical name with <i>the</i>, and one abstract noun in a general sense.",
 "support": "Give a desk card with the four boxes and one example each; students label every gap with the box (G / I / Geo / Ab) before writing the article.",
 "challenge": "Students rewrite three Exercise D gaps as full sentences that change the meaning by swapping zero article for <i>the</i>, and explain the difference.",
 "anticipated_problems": [
  ["Students add <i>the</i> to abstract and uncountable nouns used in general (&ldquo;the freedom&rdquo;, &ldquo;the education&rdquo;), often from a first-language habit.", "Test question: &ldquo;Do I mean this idea in general, or one specific instance?&rdquo; General &rarr; zero article; specific (usually followed by <i>of&hellip;</i> or a relative clause) &rarr; <i>the</i>."],
  ["Students treat all country and place names the same and either add or drop <i>the</i> everywhere.", "Board two columns &ndash; THE (rivers, seas, ranges, plural/union names) vs NO ARTICLE (continents, most countries, single mountains, lakes, cities) &ndash; and sort ten names before Exercise B."]
 ],
 "key_language": "<b>Grammar:</b> zero article for generic reference, institutions for their purpose and abstract nouns in general; <i>the</i> with rivers/seas/ranges/plural country names and with a specific instance of an abstract noun. <br><b>Board:</b> Life is hard. / The life she led was hard. &bull; the United Kingdom &ndash; Asia &bull; in prison / at the prison",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Correct: &ldquo;The happiness is the goal.&rdquo; &rarr; <i>Happiness&hellip;</i></li><li><span class='n'>2.</span> &ldquo;sailed across ___ Pacific to ___ Australia&rdquo; &rarr; <i>the / &mdash;</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_articles_reading_b2.json",
 "ws_title": "Advanced Articles and Determiners " + BUL + " Reading " + BUL + " B2",
 "info_rows": info("Reading", "Society and public institutions; articles and determiners in extended text", "A" + DASH + "F (comprehension, language, summary)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Before you read</div><p>Discussion &ndash; answers vary. Push students to name specific institutions (education, healthcare, transport, justice) and give reasons.</p>"
  "<div class='ex-title'>C. Reading comprehension</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> B</div><div class='ans-item'><span class='n'>2.</span> B</div>"
  "<div class='ans-item'><span class='n'>3.</span> B</div>"
  "<div class='ans-item'><span class='n'>4.</span> It prevents isolation and keeps access to education, healthcare and jobs open.</div>"
  "<div class='ans-item'><span class='n'>5.</span> Act in the national interest, use public money wisely and be transparent.</div>"
  "<div class='ans-item'><span class='n'>6.</span> (model) People would &ldquo;lose faith in the system&rdquo;, cooperation would break down and society would become weaker and less fair.</div></div>"
  "<div class='ex-title'>D. Language in context</div><ul class='ans'>"
  "<li><span class='n'>1.</span> Zero article, institution in a general sense: e.g. <i>Education gives young people&hellip;</i> / <i>Healthcare is another essential service</i> / <i>Transport networks connect&hellip;</i></li>"
  "<li><span class='n'>2.</span> <i>the</i> + collective/public institution: <i>the National Health Service (NHS)</i> / <i>the government</i> / <i>the public</i></li>"
  "<li><span class='n'>3.</span> Geographical name with the correct article: <i>the United Kingdom</i></li>"
  "<li><span class='n'>4.</span> Determiner showing quantity: <i>many people</i> / <i>A few communities</i> / <i>Most citizens</i> / <i>different groups</i></li>"
  "<li><span class='n'>5.</span> (model) <i>trust</i> in general = the idea of trust, no article (&ldquo;Trust in public institutions is vital&rdquo;); a specific reference = &ldquo;the trust between citizens and this government&rdquo;.</li></ul>"
  "<div class='ex-title'>E. Complete the summary</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> &mdash;</div><div class='ans-item'><span class='n'>2.</span> &mdash;</div>"
  "<div class='ans-item'><span class='n'>3.</span> &mdash;</div><div class='ans-item'><span class='n'>4.</span> the</div>"
  "<div class='ans-item'><span class='n'>5.</span> the</div><div class='ans-item'><span class='n'>6.</span> the</div>"
  "<div class='ans-item'><span class='n'>7.</span> The</div><div class='ans-item'><span class='n'>8.</span> &mdash;</div></div>"
  "<div class='ex-title'>F. Reflection</div><p>Free writing &ndash; look for a real public institution, at least one article/determiner used deliberately, and a clear reason it matters to society.</p>"
 ),
 "teacher_tip": "Before Exercise D, tell students the text was written to show every article rule at least once. As they read, have them box each <i>the</i> and each zero-article noun in the first two paragraphs and label why.",
 "mistakes": [
  ["The good education strengthens society.", "Good education strengthens society."],
  ["A few communities still lacks reliable transport.", "A few communities still lack reliable transport."],
  ["In United Kingdom, the NHS is free.", "In the United Kingdom, the NHS is free."],
  ["The trust is important for a fair society.", "Trust is important for a fair society."]
 ],
 "activity_title": "Article Hunt (8 min)",
 "activity_body": "In pairs, students find in the text: one zero-article institution, one <i>the</i> + institution, one geographical <i>the</i>, one quantity determiner and one abstract noun. They write each with a one-word label. Fastest correct pair reads their list to the class.",
 "materials": MAT_R,
 "lesson_title": LT,
 "learning_objective": "Students will be able to read an information text for gist and detail, and identify how zero article, a/an and the are used with institutions, geographical names and abstract nouns in context.",
 "success_criteria": "I can find the main idea and specific details in the text. I can explain why a noun in the text takes zero article, a/an or the. I can complete a summary with the correct articles.",
 "prior_knowledge": "The four article systems from the Grammar worksheet (or equivalent); reading for gist and scanning for detail.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: ask &ldquo;Which public institutions matter most for a fair society?&rdquo; and collect four or five on the board. Part 2: next to each, ask whether we say it with <i>the</i> or with no article when we mean it in general (education, healthcare, the government, the NHS)."],
  ["8 min", "Presentation (I Do)", "Recap the rule the text is built on: institutions and abstract nouns take <b>zero article</b> when we mean them in general or use them for their purpose (&ldquo;Education gives&hellip;&rdquo;, &ldquo;in prison&rdquo;), but <b>the</b> for a specific, named or shared one (&ldquo;the National Health Service&rdquo;, &ldquo;the government&rdquo;, &ldquo;the trust between&hellip;&rdquo;). Geographical names follow the fixed list &ndash; <i>the</i> with the United Kingdom, zero article with continents. Model the first paragraph aloud, stopping at each noun to say which rule applies and why."],
  ["10 min", "Guided Practice (We Do)", "Students read the text once for gist, then do Exercise C items 1&ndash;3 as a class, underlining the sentence in the text that gives each answer."],
  ["10 min", "Independent Practice (You Do)", "Students complete Exercise C items 4&ndash;6, Exercise D and Exercise E individually, then compare Exercise D in pairs."],
  ["7 min", "Assessment", "Review Exercise E on the board; for each gap a student states the rule. Then the Exit Ticket individually."],
  ["5 min", "Closure", "Two or three students share one sentence from Exercise F; the class checks the articles."]
 ],
 "followup": "Homework: write a 100&ndash;120 word paragraph about one public institution in the student&rsquo;s country, using at least two of the article rules from the text.",
 "support": "Give a shortened text (first three paragraphs only) and let students do Exercise C 1&ndash;3 and Exercise D from that section.",
 "challenge": "Students rewrite two sentences from the text, changing a general reference to a specific one (adding <i>the</i> + a defining phrase) and explaining how the meaning shifts.",
 "anticipated_problems": [
  ["Students choose comprehension answers from prior knowledge rather than the text (e.g. picking &ldquo;the government should be smaller&rdquo; for the main idea).", "Insist every answer is backed by an underlined sentence; if it isn&rsquo;t in the text, it isn&rsquo;t the answer."],
  ["In Exercise E students default to <i>the</i> for the generic nouns in gaps 1&ndash;3.", "Remind them: gaps 1&ndash;3 name education / healthcare / transport in general &ndash; zero article, exactly as in the opening of the text."]
 ],
 "key_language": "<b>Grammar:</b> zero article for institutions and abstract nouns in general; <i>the</i> for a specific / named institution and for <i>the</i> + geographical names such as the United Kingdom. <br><b>Board:</b> Education helps society. / The education system needs reform. &bull; the NHS &bull; Trust is vital.",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> &ldquo;___ healthcare improves lives.&rdquo; &rarr; <i>&mdash;</i></li><li><span class='n'>2.</span> &ldquo;She works for ___ government.&rdquo; &rarr; <i>the</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_articles_writing_b2.json",
 "ws_title": "Advanced Articles and Determiners " + BUL + " Writing " + BUL + " B2",
 "info_rows": info("Writing", "Discuss social and cultural topics; accurate articles and determiners", "A" + DASH + "F (model, plan, 180" + DASH + "220-word essay)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Analyse the model</div><ul class='ans'>"
  "<li><span class='n'>1.</span> <i>public education</i> has zero article because it means education as a whole idea / an institution in general, not one specific instance.</li>"
  "<li><span class='n'>2.</span> <i>the government</i> and <i>the United Kingdom</i> take <i>the</i>: the government is a specific, shared institution understood from context; the United Kingdom is a fixed <i>the</i> country name (a political union / contains a common noun).</li>"
  "<li><span class='n'>3.</span> Two determiners, e.g. <i>many people</i> (large, non-specific number + plural countable) and <i>a little support</i> (a small but sufficient amount + uncountable) / <i>each individual</i> (every one, considered singly). Accept any two with a correct explanation.</li>"
  "<li><span class='n'>4.</span> <i>education</i> and <i>equality</i> are abstract / uncountable nouns used in a general sense, so they take zero article.</li></ul>"
  "<div class='ex-title'>B. Organise your ideas / C. Useful language</div><p>Planning notes and phrase bank &ndash; not marked. Check the plan names one public institution and one geographical reference, and that the phrases in C are used naturally in Exercise E.</p>"
  "<div class='ex-title'>D&ndash;E. Writing task</div><p>Model band (strong response): clear position on the chosen topic; a range of articles and determiners used accurately, including at least one institution with zero article (&ldquo;public education&rdquo;), one geographical name with <i>the</i> or zero article as appropriate, and one abstract noun in a general sense; ideas developed with reasons and examples; 180&ndash;220 words; well organised into 2&ndash;3 paragraphs.</p>"
  "<div class='ex-title'>F. Self-check</div><p>Students tick each box; spot-check that &ldquo;a variety of determiners&rdquo; and &ldquo;one public institution / geographical reference / abstract noun&rdquo; are genuinely present.</p>"
 ),
 "teacher_tip": "Do Exercise A as a class &ndash; it is the mini-lesson. Then have students copy three phrases from Exercise C into their plan before they draft, so the target language is built in from the start.",
 "mistakes": [
  ["The public education is a powerful force for equality.", "Public education is a powerful force for equality."],
  ["In the large cities, the cost of living is high.", "In large cities, the cost of living is high."],
  ["Each of individual can contribute to the common good.", "Each individual can contribute to the common good."],
  ["Many of people believe there is still a gap.", "Many people believe there is still a gap."]
 ],
 "activity_title": "Sentence Frames (8 min)",
 "activity_body": "Put five frames on the board (&ldquo;___ education is&hellip;&rdquo;, &ldquo;In ___ United Kingdom,&hellip;&rdquo;, &ldquo;Most of ___ population&hellip;&rdquo;, &ldquo;A little ___ can&hellip;&rdquo;, &ldquo;Each ___ should&hellip;&rdquo;). Students complete each with the correct article/determiner and a real idea, then read two aloud.",
 "materials": MAT_W,
 "lesson_title": LT,
 "learning_objective": "Students will be able to plan and write a 180&ndash;220-word discussion paragraph on a social or cultural topic, using articles and determiners accurately for generic reference, institutions, geographical names and abstract nouns.",
 "success_criteria": "I can use zero article for generic and abstract nouns, and <i>the</i> for specific institutions and certain place names. I can use a range of determiners (many, most of, each, a little). I can develop my ideas with reasons and examples in 180&ndash;220 words.",
 "prior_knowledge": "The four article systems (from the Grammar worksheet); basic paragraph structure (topic sentence, support, conclusion).",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;___ education&rdquo; and &ldquo;___ education he received in Finland&rdquo; and elicit the article for each. Part 2: ask students for two abstract nouns they might use in an essay about society (equality, freedom, trust) and confirm they take zero article in general."],
  ["8 min", "Presentation (I Do)", "Read the model (Exercise A) aloud. Stop at four points and give the rule + why: <i>Public education</i> &ndash; institution in general, zero article; <i>the government</i> / <i>the United Kingdom</i> &ndash; specific institution / fixed <i>the</i> country name; <i>many people</i>, <i>a little support</i>, <i>each individual</i> &ndash; determiners chosen for a non-specific number / a small amount / every one singly; <i>education</i> and <i>equality</i> &ndash; abstract nouns in general, zero article. Show how the phrases in Exercise C carry these rules."],
  ["10 min", "Guided Practice (We Do)", "As a class, answer Exercise A questions 1&ndash;2 in full sentences, then plan a shared paragraph on &ldquo;the role of public education&rdquo; using the Exercise B boxes on the board."],
  ["10 min", "Independent Practice (You Do)", "Students choose a topic, complete their Exercise B plan and draft the paragraph (Exercise E), aiming for 180&ndash;220 words with the required institution, place name and abstract noun."],
  ["7 min", "Assessment", "Students run the Exercise F self-check, then swap with a partner who circles every article and determiner and flags any that look wrong."],
  ["5 min", "Closure", "Two students read their opening two sentences; the class listens for one correct generic zero article and one correct <i>the</i>."]
 ],
 "followup": "Homework: redraft the paragraph after peer feedback, then write a two-sentence answer to a second topic from Exercise D using at least one determiner from Exercise C.",
 "support": "Give a half-built model with the articles/determiners gapped; students fill it, then adapt two sentences to their own topic before writing freely.",
 "challenge": "Students add a counter-argument sentence that uses <i>the</i> + an abstract noun made specific (&ldquo;the inequality that remains in large cities&rdquo;) and a concession linker.",
 "anticipated_problems": [
  ["Students add <i>the</i> to every abstract noun (&ldquo;the equality&rdquo;, &ldquo;the freedom&rdquo;), often from a first-language habit.", "Reuse the test question from Exercise A: general idea &rarr; zero article; specific instance (with <i>of&hellip;</i> or a relative clause) &rarr; <i>the</i>."],
  ["Students use &ldquo;most of people&rdquo; / &ldquo;each of student&rdquo;.", "Board the patterns: <i>most people</i> or <i>most of the people</i>; <i>each student</i> or <i>each of the students</i>. Never <i>most of people</i>."]
 ],
 "key_language": "<b>Grammar:</b> zero article for generic and abstract nouns; <i>the</i> for specific institutions and <i>the</i> + place names; determiners &ndash; many, most of, each, every, a little. <br><b>Board:</b> Public education is&hellip; &bull; In the United Kingdom,&hellip; &bull; Most of the population&hellip; &bull; A little progress&hellip;",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;The freedom is a basic right.&rdquo; &rarr; <i>Freedom is a basic right.</i></li><li><span class='n'>2.</span> Fix: &ldquo;most of people agree&rdquo; &rarr; <i>most people agree</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_articles_practice_b2.json",
 "ws_title": "Advanced Articles and Determiners " + BUL + " Practice " + BUL + " B2",
 "info_rows": info("Practice", "Articles and determiners in extended context: choice, gap-fill, error correction, rewriting", "A" + DASH + "F"),
 "answer_key_html": (
  "<div class='ex-title'>A. Choose the best option</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> A &ndash; a</div><div class='ans-item'><span class='n'>2.</span> C &ndash; a few</div>"
  "<div class='ans-item'><span class='n'>3.</span> C &ndash; The</div><div class='ans-item'><span class='n'>4.</span> A &ndash; &mdash;</div>"
  "<div class='ans-item'><span class='n'>5.</span> A &ndash; Most</div><div class='ans-item'><span class='n'>6.</span> A &ndash; &mdash; (institution)</div>"
  "<div class='ans-item'><span class='n'>7.</span> A &ndash; a (a little time)</div><div class='ans-item'><span class='n'>8.</span> B &ndash; The</div>"
  "<div class='ans-item'><span class='n'>9.</span> A &ndash; much (also accept C &ndash; a little)</div><div class='ans-item'><span class='n'>10.</span> C &ndash; The</div></div>"
  "<div class='ex-title'>B. Complete the text</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> an</div><div class='ans-item'><span class='n'>2.</span> &mdash;</div>"
  "<div class='ans-item'><span class='n'>3.</span> a</div><div class='ans-item'><span class='n'>4.</span> the</div>"
  "<div class='ans-item'><span class='n'>5.</span> the</div><div class='ans-item'><span class='n'>6.</span> &mdash;</div>"
  "<div class='ans-item'><span class='n'>7.</span> the</div><div class='ans-item'><span class='n'>8.</span> The</div>"
  "<div class='ans-item'><span class='n'>9.</span> most (many)</div><div class='ans-item'><span class='n'>10.</span> a</div>"
  "<div class='ans-item'><span class='n'>11.</span> the</div></div>"
  "<div class='ex-title'>C. Correct the mistake</div><ul class='ans'>"
  "<li><span class='n'>1.</span> She goes to <b>&mdash;</b> university in Manchester. (institution for its purpose)</li>"
  "<li><span class='n'>2.</span> <b>&mdash;</b> Education is important for a society. (abstract / general)</li>"
  "<li><span class='n'>3.</span> I have <b>many</b> friends who live abroad. (<i>much</i> &rarr; <i>many</i>, countable)</li>"
  "<li><span class='n'>4.</span> Mount Everest is <b>the</b> highest mountain in the world. (superlative &ndash; add <i>the</i>)</li>"
  "<li><span class='n'>5.</span> We need a little more time to complete <b>the</b> task. (specific &ndash; add <i>the</i>)</li>"
  "<li><span class='n'>6.</span> <b>The</b> Amazon is a major river in South America. (river name &ndash; add <i>The</i>)</li></ul>"
  "<div class='ex-title'>D. Rewrite the sentence (accept any paraphrase with the given word)</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> The environment should be protected by people.</div>"
  "<div class='ans-item'><span class='n'>2.</span> I know a few people who work for the charity.</div>"
  "<div class='ans-item'><span class='n'>3.</span> She has little experience in this area.</div>"
  "<div class='ans-item'><span class='n'>4.</span> France was the country they visited last year.</div>"
  "<div class='ans-item'><span class='n'>5.</span> Most of the people support the new policy.</div>"
  "<div class='ans-item'><span class='n'>6.</span> He spent two years in prison for the crime he had committed.</div></div>"
  "<div class='ex-title'>E. Extended context challenge &ndash; eight corrections</div><p>(1) a Japan &rarr; <b>Japan</b> &bull; (2) for first time &rarr; <b>for the first time</b> &bull; (3) few days &rarr; <b>a few days</b> &bull; (4) a Mount Fuji &rarr; <b>Mount Fuji</b> &bull; (5) the Japanese culture &rarr; <b>Japanese culture</b> &bull; (6) One of most memorable &rarr; <b>One of the most memorable</b> &bull; (7) an traditional temple &rarr; <b>a traditional temple</b> &bull; (8) more of country &rarr; <b>more of the country</b>.</p>"
  "<div class='ex-title'>F. Personal response</div><p>Model: <b>1.</b> The library in my town is free for everyone. <b>2.</b> The Andes run down the west of South America. <b>3.</b> Progress takes time and patience.</p>"
 ),
 "teacher_tip": "Exercise D items 1, 4 and 6 have more than one good rewrite &ndash; accept any version that keeps the meaning and uses the word in brackets naturally. Do one together before students work alone.",
 "mistakes": [
  ["I have much informations about the topic.", "I have much information about the topic."],
  ["He is the best student in a class.", "He is the best student in the class."],
  ["We spent a few money on the trip.", "We spent a little money on the trip."],
  ["The Everest is in the Himalayas.", "Everest is in the Himalayas."]
 ],
 "activity_title": "Fix or Keep (8 min)",
 "activity_body": "Read out twelve short sentences (half correct, half with an article/determiner error). Students hold up FIX or KEEP; for every FIX they must give the correction and the rule. Keep score by team.",
 "materials": MAT_G,
 "lesson_title": LT,
 "learning_objective": "Students will be able to apply article and determiner rules across extended text, correcting errors and rewriting sentences with a given word while keeping the meaning.",
 "success_criteria": "I can choose the right article or determiner in context. I can find and correct one article/determiner error per sentence. I can rewrite a sentence using a given quantifier or article without changing the meaning.",
 "prior_knowledge": "The four article systems and the main quantifiers (much/many, few/a few, little/a little, most of, each, every).",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;much friends&rdquo; and &ldquo;little cars&rdquo; and ask what is wrong (countable/uncountable mismatch). Part 2: write &ldquo;in ___ prison&rdquo; and &ldquo;___ Everest&rdquo; and elicit the article for each."],
  ["8 min", "Presentation (I Do)", "Quick review of the decision path: is the noun countable or uncountable? general or specific? an institution used for its purpose? a place name on the <i>the</i> list? For quantifiers: <i>much</i> + uncountable, <i>many</i> + countable; <i>a few/few</i> + countable, <i>a little/little</i> + uncountable; <i>most of</i> needs <i>the</i> + noun. Model Exercise C item 3 (<i>much friends</i> &rarr; <i>many friends</i>) and Exercise D item 2 (rewrite with <i>a few</i>)."],
  ["10 min", "Guided Practice (We Do)", "Exercise A items 1&ndash;5 as a class, naming the rule each time; then start Exercise C together (items 1&ndash;3)."],
  ["12 min", "Independent Practice (You Do)", "Students complete Exercise B, the rest of Exercise C, Exercise D and Exercise E individually."],
  ["6 min", "Assessment", "Review Exercise E on the board &ndash; students call out the eight errors and corrections. Then the Exit Ticket."],
  ["4 min", "Closure", "In pairs, students compare two Exercise D rewrites and agree which reads best."]
 ],
 "followup": "Homework: write five sentences about your country&rsquo;s public services, then swap with a partner who checks every article and determiner.",
 "support": "Give the countable/uncountable status of each key noun in Exercises B and C as a word list, so students focus only on the article choice.",
 "challenge": "Students write an eighth-error version of a short paragraph for a partner to correct, then mark it.",
 "anticipated_problems": [
  ["In Exercise D students change the meaning to force the given word in (e.g. turning a general statement into a specific one).", "Remind them the task is a paraphrase: the new sentence must be true in exactly the same situations as the original."],
  ["Students miss errors in Exercise E because they read for meaning, not form.", "Tell them there are exactly eight and they are all article/determiner errors &ndash; read once for meaning, then again word by word."]
 ],
 "key_language": "<b>Grammar:</b> article decision path (countable? general/specific? institution? place name?); quantifiers &ndash; much/many, few/a few, little/a little, most of + the. <br><b>Board:</b> much information / many friends &bull; a little time / a few cars &bull; most of the people &bull; the Amazon / Everest",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;I have much friends.&rdquo; &rarr; <i>many friends</i></li><li><span class='n'>2.</span> Fix: &ldquo;Everest is highest mountain.&rdquo; &rarr; <i>the highest mountain</i></li></ul>"
})
w(TES[-1])

print("--- articles set done ---")

# =====================================================================
# 2. ADVANCED QUANTIFIERS
# =====================================================================
TES.append({
 "_file": "te_quantifiers_grammar_b2.json",
 "ws_title": "Advanced Quantifiers " + BUL + " Grammar " + BUL + " B2",
 "info_rows": info("Grammar", "a great deal of, a large number of, little, few, hardly any, the majority of", "6 (A" + DASH + "F)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Grammar overview</div><p>Reference table &ndash; no written answers. Check students can match each quantifier to countable or uncountable and to its positive or negative meaning.</p>"
  "<div class='ex-title'>B. Choose the correct option</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> A large number of</div>"
  "<div class='ans-item'><span class='n'>2.</span> a little</div>"
  "<div class='ans-item'><span class='n'>3.</span> Hardly any (accept Few)</div>"
  "<div class='ans-item'><span class='n'>4.</span> a great deal of</div>"
  "<div class='ans-item'><span class='n'>5.</span> hardly any</div>"
  "<div class='ans-item'><span class='n'>6.</span> Little</div>"
  "<div class='ans-item'><span class='n'>7.</span> The majority of</div>"
  "<div class='ans-item'><span class='n'>8.</span> hardly any (accept a great deal of)</div>"
  "<div class='ans-item'><span class='n'>9.</span> The majority of</div>"
  "<div class='ans-item'><span class='n'>10.</span> few (accept a few)</div></div>"
  "<div class='ex-title'>C. Complete the sentences</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> little</div><div class='ans-item'><span class='n'>2.</span> large</div>"
  "<div class='ans-item'><span class='n'>3.</span> a little</div><div class='ans-item'><span class='n'>4.</span> Little</div>"
  "<div class='ans-item'><span class='n'>5.</span> a few</div><div class='ans-item'><span class='n'>6.</span> hardly any</div>"
  "<div class='ans-item'><span class='n'>7.</span> The majority</div><div class='ans-item'><span class='n'>8.</span> a large number of (accept a few)</div></div>"
  "<div class='ex-title'>D. Correct the mistake</div><ul class='ans'>"
  "<li><span class='n'>1.</span> <b>A great deal of</b> pollution is a serious problem. (uncountable)</li>"
  "<li><span class='n'>2.</span> There is <b>little</b> information on the website. (uncountable)</li>"
  "<li><span class='n'>3.</span> <b>A large number of</b> people are concerned about climate change. (countable)</li>"
  "<li><span class='n'>4.</span> She has <b>few</b> friends in her new school. (countable)</li>"
  "<li><span class='n'>5.</span> <b>Most of the</b> water in the area is contaminated. (the majority of + countable only &rarr; most of + uncountable)</li>"
  "<li><span class='n'>6.</span> There are <b>a few</b> cars parked outside. (countable)</li></ul>"
  "<div class='ex-title'>E. Complete the text &ndash; Changing consumer habits</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> a large number of</div><div class='ans-item'><span class='n'>2.</span> large number</div>"
  "<div class='ans-item'><span class='n'>3.</span> a great deal of</div><div class='ans-item'><span class='n'>4.</span> little</div>"
  "<div class='ans-item'><span class='n'>5.</span> The majority of</div><div class='ans-item'><span class='n'>6.</span> a great deal of</div>"
  "<div class='ans-item'><span class='n'>7.</span> Little</div><div class='ans-item'><span class='n'>8.</span> many (accept most)</div></div>"
  "<div class='ex-title'>F. Short production</div><p>Model: <b>1.</b> A large number of students take the bus to school. <b>2.</b> There is hardly any milk left in the fridge. <b>3.</b> The majority of my classmates study a second language.</p>"
  "<p class='flag'>Several Exercise B items accept a second quantifier of the same type (e.g. 3 <i>Hardly any / Few</i>, 10 <i>few / a few</i>) &ndash; accept any choice that fits the countable/uncountable noun and the positive or negative sense.</p>"
 ),
 "teacher_tip": "Two questions decide every answer: (1) is the noun countable or uncountable? (2) does the sentence mean &ldquo;not enough / almost none&rdquo; (little, few, hardly any) or &ldquo;some / a lot&rdquo; (a little, a few, a great deal of)? Have students say both answers aloud before choosing.",
 "mistakes": [
  ["There is few evidence for this claim.", "There is little evidence for this claim."],
  ["A great deal of students failed the exam.", "A large number of students failed the exam."],
  ["The majority of the information is out of date.", "Most of the information is out of date."],
  ["She has a little friends in this city.", "She has a few friends in this city."]
 ],
 "activity_title": "Countable Corners (8 min)",
 "activity_body": "Label two corners COUNTABLE and UNCOUNTABLE. Call out a noun + quantifier (&ldquo;a great deal of traffic&rdquo;, &ldquo;a large number of ideas&rdquo;, &ldquo;few water&rdquo;). Students move to the corner that matches and say whether the pairing is correct; if not, they fix it.",
 "materials": MAT_G,
 "lesson_title": LT,
 "learning_objective": "Students will be able to choose advanced quantifiers (a great deal of, a large number of, little/a little, few/a few, hardly any, the majority of) correctly for countable and uncountable nouns and for positive or negative meaning.",
 "success_criteria": "I can pair each quantifier with a countable or uncountable noun. I can tell <i>little</i> from <i>a little</i> and <i>few</i> from <i>a few</i> by meaning. I can correct a quantifier that does not match its noun.",
 "prior_knowledge": "Basic quantifiers (some, any, much, many, a lot of); countable vs uncountable nouns.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;I have ___ money&rdquo; and &ldquo;I have ___ friends&rdquo; and elicit which quantifiers fit each and why (uncountable vs countable). Part 2: write &ldquo;I have <b>little</b> time&rdquo; vs &ldquo;I have <b>a little</b> time&rdquo; and ask which sounds positive."],
  ["8 min", "Presentation (I Do)", "Explain the two-part choice with the &ldquo;why&rdquo;. <b>Countable / uncountable:</b> <i>a large number of</i>, <i>few</i>, <i>a few</i>, <i>the majority of</i> go with plural countable nouns (people, cars); <i>a great deal of</i>, <i>little</i>, <i>a little</i> go with uncountable nouns (money, information); <i>hardly any</i> works with both. <b>Positive vs negative:</b> without <i>a</i>, <i>little</i> and <i>few</i> mean &ldquo;not enough / almost none&rdquo; (a complaint); with <i>a</i>, <i>a little</i> and <i>a few</i> mean &ldquo;some, and that is fine&rdquo;. <i>The majority of</i> = more than half. Model Exercise D item 1 (<i>a large number of pollution</i> &rarr; <i>a great deal of pollution</i>) and item 5 (<i>the majority of water</i> &rarr; <i>most of the water</i>)."],
  ["10 min", "Guided Practice (We Do)", "Exercise B items 1&ndash;5 as a class, each time saying &ldquo;countable/uncountable&rdquo; and &ldquo;positive/negative&rdquo; first. Then start Exercise D together."],
  ["10 min", "Independent Practice (You Do)", "Students complete Exercise C, the rest of Exercise D and Exercise E individually, then compare Exercise E in pairs."],
  ["7 min", "Assessment", "Review Exercise E on the board; students justify each gap with the two-part test. Then the Exit Ticket."],
  ["5 min", "Closure", "Students write one Exercise F sentence and read it; the class says whether the quantifier matches the noun."]
 ],
 "followup": "Homework: write six sentences about your town (traffic, shops, green space, jobs, tourists, noise) using a different advanced quantifier in each.",
 "support": "Give a two-column card (UNCOUNTABLE: a great deal of / little / a little &bull; COUNTABLE: a large number of / few / a few / the majority of). Students pick the column first.",
 "challenge": "Students rewrite three Exercise C sentences twice &ndash; once with a negative quantifier, once with a positive one &ndash; and explain how the meaning changes.",
 "anticipated_problems": [
  ["Students use <i>the majority of</i> and <i>a large number of</i> with uncountable nouns (&ldquo;the majority of water&rdquo;).", "Rule: these need something you can count. For uncountable nouns use <i>most of the</i>, <i>a great deal of</i> or <i>a large amount of</i>."],
  ["Students treat <i>little/few</i> and <i>a little/a few</i> as the same.", "Board it: <i>few problems</i> = good news; <i>a few problems</i> = neutral. The little word <i>a</i> flips the meaning from negative to positive."]
 ],
 "key_language": "<b>Grammar:</b> a great deal of / little / a little + uncountable; a large number of / few / a few / the majority of + plural countable; hardly any + both; <i>little/few</i> (negative) vs <i>a little/a few</i> (positive). <br><b>Board:</b> a great deal of money &bull; a large number of cars &bull; little time / a little time",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;a large number of traffic&rdquo; &rarr; <i>a great deal of traffic</i></li><li><span class='n'>2.</span> Positive or negative: &ldquo;Few people came.&rdquo; &rarr; <i>negative (not many)</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_quantifiers_reading_b2.json",
 "ws_title": "Advanced Quantifiers " + BUL + " Reading " + BUL + " B2",
 "info_rows": info("Reading", "Consumer habits and statistics; precise quantifiers in context", "A" + DASH + "F (comprehension, language, summary)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Before you read</div><p>Discussion &ndash; answers vary. Encourage students to use quantifiers in their answers (&ldquo;most of my friends&rdquo;, &ldquo;a few things&rdquo;).</p>"
  "<div class='ex-title'>C. Reading comprehension</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> B</div><div class='ans-item'><span class='n'>2.</span> B</div>"
  "<div class='ans-item'><span class='n'>3.</span> C</div><div class='ans-item'><span class='n'>4.</span> B</div>"
  "<div class='ans-item'><span class='n'>5.</span> There is little confidence that prices will fall soon &ndash; consumers expect prices to stay high.</div>"
  "<div class='ans-item'><span class='n'>6.</span> Better planning (a great deal of food waste could be avoided that way, with a little more awareness).</div></div>"
  "<div class='ex-title'>D. Language in context</div><ul class='ans'>"
  "<li><span class='n'>1.</span> &ldquo;most people&rdquo; = <i>the majority of</i> (also &ldquo;Most of the people&rdquo;) &ndash; countable.</li>"
  "<li><span class='n'>2.</span> &ldquo;a small number of people&rdquo; = <i>a few</i> / <i>very few</i> &ndash; countable.</li>"
  "<li><span class='n'>3.</span> large amount + uncountable = <i>a great deal of</i> (this growth / this waste) &ndash; also <i>much</i>.</li>"
  "<li><span class='n'>4.</span> &ldquo;almost no people&rdquo; = <i>hardly any</i> (also <i>very few</i>).</li>"
  "<li><span class='n'>5.</span> small amount + uncountable = <i>a little</i> (a little more awareness) &ndash; also <i>a small amount of</i>.</li></ul>"
  "<div class='ex-title'>E. Complete the summary</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> a large</div><div class='ans-item'><span class='n'>2.</span> the majority</div>"
  "<div class='ans-item'><span class='n'>3.</span> a few (very few / a small number)</div><div class='ans-item'><span class='n'>4.</span> much (a great deal of)</div>"
  "<div class='ans-item'><span class='n'>5.</span> a great deal (much)</div><div class='ans-item'><span class='n'>6.</span> the majority (a large number)</div>"
  "<div class='ans-item'><span class='n'>7.</span> hardly any</div><div class='ans-item'><span class='n'>8.</span> much</div></div>"
  "<div class='ex-title'>F. Reflection</div><p>Opinion writing &ndash; look for at least two ideas, each supported, and quantifiers used precisely.</p>"
 ),
 "teacher_tip": "As students read, they underline every bold quantifier (Exercise B tells them to). Then Exercise D just asks them to sort what they already found by meaning &ndash; &ldquo;most people&rdquo;, &ldquo;a small number&rdquo;, &ldquo;a large amount&rdquo;, &ldquo;almost none&rdquo;, &ldquo;a small amount&rdquo;.",
 "mistakes": [
  ["The majority of shoppers is careful with food now.", "The majority of shoppers are careful with food now."],
  ["Very few of information is available on this.", "Very little information is available on this."],
  ["A great deal of consumers made a purchase online.", "A large number of consumers made a purchase online."],
  ["Hardly some people expect prices to fall.", "Hardly any people expect prices to fall."]
 ],
 "activity_title": "Statistic to Sentence (8 min)",
 "activity_body": "Give a figure (&ldquo;73% of shoppers&hellip;&rdquo;, &ldquo;only 8% would pay more&hellip;&rdquo;, &ldquo;almost no one&hellip;&rdquo;). Students turn each into a sentence with the best quantifier (the majority of, hardly any, a small number of) and say why it fits.",
 "materials": MAT_R,
 "lesson_title": LT,
 "learning_objective": "Students will be able to read a statistics-based article for detail and identify how advanced quantifiers express proportion and amount with countable and uncountable nouns.",
 "success_criteria": "I can find specific figures and claims in the text. I can match a quantifier from the text to a meaning (most / a few / a lot / almost none / a small amount). I can complete a summary with quantifiers that fit the noun.",
 "prior_knowledge": "The advanced quantifiers and the countable/uncountable + positive/negative distinctions (from the Grammar worksheet).",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: ask &ldquo;How have your shopping habits changed?&rdquo; and collect answers, writing any quantifier students use on the board. Part 2: sort those quantifiers into &ldquo;more than half / some / almost none&rdquo;."],
  ["8 min", "Presentation (I Do)", "Recap what each quantifier signals about proportion: <i>the majority of</i> = more than half; <i>a large number of</i> / <i>a great deal of</i> = a lot (countable / uncountable); <i>a few</i> / <i>a little</i> = some; <i>few</i> / <i>little</i> / <i>hardly any</i> = almost none, and usually a problem. Model paragraph 2 of the text aloud, naming the proportion each quantifier gives and whether the noun is countable."],
  ["10 min", "Guided Practice (We Do)", "Students read once for gist, then do Exercise C items 1&ndash;3 as a class, pointing to the sentence that proves each answer."],
  ["10 min", "Independent Practice (You Do)", "Students complete Exercise C 4&ndash;6, Exercise D and Exercise E individually; compare Exercise D in pairs."],
  ["7 min", "Assessment", "Review Exercise E; for each gap a student states the noun type and the proportion. Then the Exit Ticket."],
  ["5 min", "Closure", "Students share one Exercise F idea using a precise quantifier."]
 ],
 "followup": "Homework: find two real statistics about shopping or the environment and write a sentence for each using an advanced quantifier.",
 "support": "Give the meanings list (most / a lot / some / almost none) as a card; students label each bold quantifier in the text before Exercise D.",
 "challenge": "Students rewrite three sentences from the text, replacing the quantifier with one of the opposite proportion, and explain how the claim changes.",
 "anticipated_problems": [
  ["Students pick <i>the majority of</i> for uncountable nouns in Exercise E (&ldquo;the majority of food waste&rdquo;).", "For uncountable nouns use <i>a great deal of</i>, <i>much</i> or <i>most of the</i>; <i>the majority of</i> needs something countable."],
  ["Students confuse &ldquo;a few&rdquo; (some) with &ldquo;few&rdquo; (almost none) when choosing from the text.", "Point back to the sentence: does the writer sound positive (a few) or is it a problem (few / hardly any)?"]
 ],
 "key_language": "<b>Grammar:</b> the majority of = &gt;50%; a large number of / a great deal of = a lot; a few / a little = some; few / little / hardly any = almost none. <br><b>Board:</b> the majority of consumers &bull; a great deal of growth &bull; hardly any expect prices to fall",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> &ldquo;___ of consumers shop online&rdquo; (most) &rarr; <i>The majority</i></li><li><span class='n'>2.</span> Fix: &ldquo;a great deal of shoppers&rdquo; &rarr; <i>a large number of shoppers</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_quantifiers_writing_b2.json",
 "ws_title": "Advanced Quantifiers " + BUL + " Writing " + BUL + " B2",
 "info_rows": info("Writing", "Describe quantities and trends accurately with advanced quantifiers", "A" + DASH + "F (model, plan, 180" + DASH + "220-word paragraph)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Analyse the model</div><ul class='ans'>"
  "<li><span class='n'>1.</span> Quantifiers for a large amount / many people: <i>a large number of</i> (consumers), <i>The majority of</i> (young adults), <i>a great deal of</i> (their spending), <i>a large number of</i> (consumers&hellip; aware).</li>"
  "<li><span class='n'>2.</span> Quantifiers for a small amount / low number: <i>few</i> (people visit local shops), <i>little</i> (demand), <i>hardly any</i> (traditional shops left).</li>"
  "<li><span class='n'>3.</span> Trends: shift to online shopping; decline of small / local shops; rise in packaging waste; growing awareness of environmental costs; growing interest in sustainable shopping.</li>"
  "<li><span class='n'>4.</span> The writer links trends to a consequence with &ldquo;which has had a significant impact on&hellip;&rdquo;, &ldquo;it also leads to&hellip;&rdquo; and &ldquo;As a result, there is a growing interest in&hellip;&rdquo;.</li></ul>"
  "<div class='ex-title'>B. Organise your ideas / C. Useful language</div><p>Planning notes and phrase bank &ndash; not marked. Check the plan lists at least two quantities/trends and uses quantifiers, and that phrases from C appear in Exercise E.</p>"
  "<div class='ex-title'>D&ndash;E. Writing task</div><p>Model band (strong response): a clear focus (consumer habits / lifestyle changes / public services); a variety of advanced quantifiers used accurately with both countable and uncountable nouns; specific examples or figures; at least one cause&ndash;effect link between a trend and a result; 180&ndash;220 words; organised logically.</p>"
  "<div class='ex-title'>F. Self-check</div><p>Students tick each box; spot-check &ldquo;a variety of quantifiers&rdquo; and &ldquo;countable and uncountable nouns correctly&rdquo;.</p>"
 ),
 "teacher_tip": "Have students choose four quantifiers from the Exercise C list before drafting &ndash; two for &ldquo;a lot&rdquo; and two for &ldquo;almost none / a small amount&rdquo; &ndash; and mark which noun each will describe. This builds precision in from the plan.",
 "mistakes": [
  ["A large number of pollution comes from cars.", "A great deal of pollution comes from cars."],
  ["The majority of the traffic is caused by commuters.", "Most of the traffic is caused by commuters."],
  ["There is few evidence that habits are changing.", "There is little evidence that habits are changing."],
  ["Hardly any of information is available on this trend.", "Hardly any information is available on this trend."]
 ],
 "activity_title": "Trend Lines (8 min)",
 "activity_body": "Draw three simple graphs on the board (rising, falling, flat). Students describe each in one sentence using a quantifier + a trend verb (&ldquo;A large number of&hellip; now&hellip;&rdquo;, &ldquo;Hardly any&hellip; still&hellip;&rdquo;, &ldquo;The number of&hellip; has fallen&rdquo;).",
 "materials": MAT_W,
 "lesson_title": LT,
 "learning_objective": "Students will be able to plan and write a 180&ndash;220-word paragraph describing quantities and trends, using a range of advanced quantifiers accurately with countable and uncountable nouns.",
 "success_criteria": "I can use a variety of quantifiers (a great deal of, a large number of, few, little, hardly any, the majority of). I can match each to a countable or uncountable noun. I can link a trend to a cause or effect. I can stay within 180&ndash;220 words.",
 "prior_knowledge": "The advanced quantifiers and their noun types; basic cause&ndash;effect linkers (as a result, this leads to).",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: elicit three changes in how people shop or travel and write them on the board. Part 2: for each, ask &ldquo;a lot of people or hardly anyone?&rdquo; and add the quantifier."],
  ["8 min", "Presentation (I Do)", "Read the model paragraph. Point out, with the reason: <i>a large number of</i> / <i>The majority of</i> / <i>a great deal of</i> describe the big trends (many consumers, most young adults, a lot of spending); <i>few</i> / <i>little</i> / <i>hardly any</i> describe the decline (few visit local shops, little demand, hardly any shops left); the noun after each decides countable vs uncountable. Show the three linking phrases the model uses to connect a trend to a consequence."],
  ["10 min", "Guided Practice (We Do)", "As a class, answer Exercise A questions 1&ndash;2 in full sentences and plan a shared paragraph on &ldquo;how people travel to work&rdquo; using the Exercise B boxes."],
  ["10 min", "Independent Practice (You Do)", "Students choose an area, complete their Exercise B plan and draft the paragraph (Exercise E), 180&ndash;220 words, with at least four different quantifiers and one cause&ndash;effect link."],
  ["7 min", "Assessment", "Students run the Exercise F self-check, then a partner circles every quantifier and flags any noun mismatch."],
  ["5 min", "Closure", "Two students read their trend sentence; the class checks quantifier + noun agreement."]
 ],
 "followup": "Homework: redraft after feedback, then add two sentences describing the opposite trend using contrasting quantifiers.",
 "support": "Give a gapped version of the model paragraph; students fill the quantifiers, then swap two sentences for their own topic before writing freely.",
 "challenge": "Students include one sentence with &ldquo;The number of&hellip; has increased/decreased&rdquo; and one with &ldquo;a growing/declining number of&hellip;&rdquo; to vary how trends are expressed.",
 "anticipated_problems": [
  ["Students overuse &ldquo;a lot of&rdquo; instead of the advanced quantifiers.", "Set a target: at least four different quantifiers from Exercise C, and &ldquo;a lot of&rdquo; used no more than once."],
  ["Students write &ldquo;a large number of traffic&rdquo; / &ldquo;a great deal of cars&rdquo;.", "Quick check before drafting: is the noun countable (cars, shops, people) or uncountable (traffic, waste, demand)? Match the quantifier to that."]
 ],
 "key_language": "<b>Grammar:</b> a large number of + countable, a great deal of + uncountable; the majority of + countable; few/little/hardly any for decline. <b>Linking:</b> as a result, this leads to, which has had an impact on. <br><b>Board:</b> A large number of commuters&hellip; &bull; a great deal of packaging waste &bull; hardly any local shops",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Choose: &ldquo;___ of shoppers now buy online&rdquo; (most) &rarr; <i>The majority</i></li><li><span class='n'>2.</span> Fix: &ldquo;a great deal of shops closed&rdquo; &rarr; <i>a large number of shops</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_quantifiers_practice_b2.json",
 "ws_title": "Advanced Quantifiers " + BUL + " Practice " + BUL + " B2",
 "info_rows": info("Practice", "Precision with countable and uncountable nouns: choice, gap-fill, error correction, rewriting", "A" + DASH + "F"),
 "answer_key_html": (
  "<div class='ex-title'>A. Choose the best option</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> B &ndash; a little</div><div class='ans-item'><span class='n'>2.</span> C &ndash; The majority of</div>"
  "<div class='ans-item'><span class='n'>3.</span> A &ndash; much</div><div class='ans-item'><span class='n'>4.</span> A &ndash; a large number of</div>"
  "<div class='ans-item'><span class='n'>5.</span> B &ndash; few</div><div class='ans-item'><span class='n'>6.</span> A &ndash; a large number of</div>"
  "<div class='ans-item'><span class='n'>7.</span> A &ndash; little</div><div class='ans-item'><span class='n'>8.</span> A &ndash; a great deal of</div>"
  "<div class='ans-item'><span class='n'>9.</span> B &ndash; Much</div><div class='ans-item'><span class='n'>10.</span> B &ndash; few</div></div>"
  "<div class='ex-title'>B. Complete the text &ndash; A Greener City</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> a great deal of</div><div class='ans-item'><span class='n'>2.</span> a large amount of</div>"
  "<div class='ans-item'><span class='n'>3.</span> the majority of</div><div class='ans-item'><span class='n'>4.</span> a little</div>"
  "<div class='ans-item'><span class='n'>5.</span> a few</div><div class='ans-item'><span class='n'>6.</span> a large amount of</div>"
  "<div class='ans-item'><span class='n'>7.</span> large / significant *</div><div class='ans-item'><span class='n'>8.</span> a great deal of</div>"
  "<div class='ans-item'><span class='n'>9.</span> the majority of</div><div class='ans-item'><span class='n'>10.</span> a little</div></div>"
  "<p class='flag'>* Gap 7 (&ldquo;a ___ reduction&rdquo;) needs an adjective of degree, not a quantifier &ndash; accept <i>large / significant / considerable</i>. Flagged for regeneration.</p>"
  "<div class='ex-title'>C. Correct the mistake</div><ul class='ans'>"
  "<li><span class='n'>1.</span> I have <b>a little</b> time to finish the report. (uncountable)</li>"
  "<li><span class='n'>2.</span> There are <b>a lot of</b> / <b>many</b> cars parked near the station. (countable)</li>"
  "<li><span class='n'>3.</span> She gave me <b>a few</b> pieces of advice about the interview. (countable &ndash; pieces)</li>"
  "<li><span class='n'>4.</span> <b>Most of the</b> information is available online. (the majority of &rarr; most of the + uncountable)</li>"
  "<li><span class='n'>5.</span> We saw <b>a large number of</b> people at the concert. (countable)</li>"
  "<li><span class='n'>6.</span> There is <b>a little</b> water in the bottle. (uncountable)</li></ul>"
  "<div class='ex-title'>D. Rewrite the sentence</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> A large number of people attended the event.</div>"
  "<div class='ans-item'><span class='n'>2.</span> There is only a little coffee, so we should buy some.</div>"
  "<div class='ans-item'><span class='n'>3.</span> Few restaurants are open late in this town.</div>"
  "<div class='ans-item'><span class='n'>4.</span> She knows little about the plan.</div>"
  "<div class='ans-item'><span class='n'>5.</span> The majority of students prefer online learning.</div>"
  "<div class='ans-item'><span class='n'>6.</span> He has hardly any free time during the week.</div></div>"
  "<div class='ex-title'>E. Extended context challenge &ndash; eight corrections</div><p>(1) much advantages &rarr; <b>many advantages</b> &bull; (2) few information &rarr; <b>little information</b> &bull; (3) A large amount of respondents &rarr; <b>A large number of respondents</b> &bull; (4) a few interest &rarr; <b>a little interest</b> &bull; (5) isn&rsquo;t many information &rarr; <b>much information</b> &bull; (6) much participants &rarr; <b>many participants</b> &bull; (7) little people &rarr; <b>few people</b> &bull; (8) a little stores &rarr; <b>a few stores</b>.</p>"
  "<div class='ex-title'>F. Personal response</div><p>Model: <b>1.</b> A large number of students walk to school. <b>2.</b> There is little rain here in summer. <b>3.</b> The majority of my family live in the same city.</p>"
 ),
 "teacher_tip": "For every choice, students say the noun type first (&ldquo;cars &ndash; countable&rdquo;) and the sense (&ldquo;almost none&rdquo; / &ldquo;some&rdquo; / &ldquo;a lot&rdquo;). Exercise E has exactly eight errors, all quantifier&ndash;noun mismatches.",
 "mistakes": [
  ["There are much people waiting outside.", "There are many people waiting outside."],
  ["She has a little brothers and sisters.", "She has a few brothers and sisters."],
  ["The majority of the water is safe to drink.", "Most of the water is safe to drink."],
  ["I don't have many time today.", "I don't have much time today."]
 ],
 "activity_title": "Noun Type Sprint (8 min)",
 "activity_body": "Call out a noun (advice, cars, traffic, ideas, water, jobs). Students shout &ldquo;countable&rdquo; or &ldquo;uncountable&rdquo; and give one quantifier that fits it. Do fifteen fast.",
 "materials": MAT_G,
 "lesson_title": LT,
 "learning_objective": "Students will be able to choose and correct advanced quantifiers with precision across sentences and a longer text, matching each to countable or uncountable nouns and to positive or negative meaning.",
 "success_criteria": "I can choose the quantifier that fits the noun and the meaning. I can find and fix a quantifier&ndash;noun mismatch. I can rewrite a sentence with a given quantifier and keep the meaning.",
 "prior_knowledge": "The advanced quantifiers, countable/uncountable nouns, and the little/a little &ndash; few/a few contrast.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;much cars&rdquo; and &ldquo;many traffic&rdquo; and ask students to fix both. Part 2: write &ldquo;little / a little&rdquo; and &ldquo;few / a few&rdquo; and ask which of each pair is the bad-news one."],
  ["8 min", "Presentation (I Do)", "Review the decision: countable or uncountable noun? then &ldquo;almost none&rdquo; (little, few, hardly any), &ldquo;some&rdquo; (a little, a few) or &ldquo;a lot / more than half&rdquo; (a great deal of, a large number of, the majority of)? Note that <i>the majority of</i> and <i>a large number of</i> need countable nouns; for uncountable use <i>a great deal of</i>, <i>a large amount of</i> or <i>most of the</i>. Model Exercise C item 4 (<i>the majority of information</i> &rarr; <i>most of the information</i>)."],
  ["10 min", "Guided Practice (We Do)", "Exercise A items 1&ndash;5 together, saying noun type + sense each time; then start Exercise C."],
  ["12 min", "Independent Practice (You Do)", "Students complete Exercise B, the rest of Exercise C, Exercise D and Exercise E individually."],
  ["6 min", "Assessment", "Review Exercise E &ndash; students name the eight errors and corrections. Then the Exit Ticket."],
  ["4 min", "Closure", "In pairs, students compare two Exercise D rewrites and agree the meaning is unchanged."]
 ],
 "followup": "Homework: write eight sentences about your school or town, using each advanced quantifier once.",
 "support": "Give a card listing each key noun in Exercises A&ndash;C as C (countable) or U (uncountable); students choose the quantifier from that.",
 "challenge": "Students write a short paragraph with exactly six quantifier errors for a partner to find and correct.",
 "anticipated_problems": [
  ["Students use <i>much/little</i> with countable nouns and <i>many/few</i> with uncountable nouns.", "Fixed pairs on the board: much / a great deal of + uncountable; many / a large number of + countable. Check the noun before the quantifier."],
  ["Students keep <i>the majority of</i> + uncountable in Exercise C item 4.", "<i>The majority of</i> counts members of a group. For a mass noun like <i>information</i>, use <i>most of the information</i>."]
 ],
 "key_language": "<b>Grammar:</b> countable &ndash; many / a large number of / few / a few / the majority of; uncountable &ndash; much / a great deal of / a large amount of / little / a little; most of the + either. <br><b>Board:</b> a little water / a few bottles &bull; a great deal of advice &bull; most of the information",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;a large amount of people&rdquo; &rarr; <i>a large number of people</i></li><li><span class='n'>2.</span> Fix: &ldquo;the majority of water&rdquo; &rarr; <i>most of the water</i></li></ul>"
})
w(TES[-1])

print("--- quantifiers set done ---")

# =====================================================================
# 3. CONTRAST AND CONCESSION
# =====================================================================
TES.append({
 "_file": "te_contrast_grammar_b2.json",
 "ws_title": "Contrast and Concession " + BUL + " Grammar " + BUL + " B2",
 "info_rows": info("Grammar", "although, even though, despite, in spite of, whereas, while, nevertheless", "6 (A" + DASH + "F)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Grammar overview</div><p>Reference table &ndash; no written answers. Check students can say which connectors take a clause (although, even though, whereas, while) and which take a noun / pronoun / -ing (despite, in spite of).</p>"
  "<div class='ex-title'>B. Choose the best option</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> B &ndash; Despite (+ noun phrase)</div>"
  "<div class='ans-item'><span class='n'>2.</span> C &ndash; although (accept B whereas)</div>"
  "<div class='ans-item'><span class='n'>3.</span> C &ndash; whereas (accept A while)</div>"
  "<div class='ans-item'><span class='n'>4.</span> C &ndash; nevertheless</div>"
  "<div class='ans-item'><span class='n'>5.</span> B &ndash; Despite (+ -ing)</div>"
  "<div class='ans-item'><span class='n'>6.</span> C &ndash; even though (+ clause)</div>"
  "<div class='ans-item'><span class='n'>7.</span> A &ndash; while (accept although)</div>"
  "<div class='ans-item'><span class='n'>8.</span> D &ndash; nevertheless</div></div>"
  "<div class='ex-title'>C. Complete the sentences</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> Despite / In spite of</div><div class='ans-item'><span class='n'>2.</span> although / even though</div>"
  "<div class='ans-item'><span class='n'>3.</span> whereas / while</div><div class='ans-item'><span class='n'>4.</span> Despite / In spite of</div>"
  "<div class='ans-item'><span class='n'>5.</span> nevertheless</div><div class='ans-item'><span class='n'>6.</span> whereas / while (accept although)</div>"
  "<div class='ans-item'><span class='n'>7.</span> Although / Even though / While</div><div class='ans-item'><span class='n'>8.</span> but / although</div></div>"
  "<div class='ex-title'>D. Rewrite / combine</div><ul class='ans'>"
  "<li><span class='n'>1.</span> Although it was cold, we went for a swim.</li>"
  "<li><span class='n'>2.</span> Despite not having much experience, she got the job. / Despite her lack of experience, she got the job.</li>"
  "<li><span class='n'>3.</span> I like working in a team, whereas he prefers working alone.</li>"
  "<li><span class='n'>4.</span> The train was delayed; nevertheless, we arrived on time.</li>"
  "<li><span class='n'>5.</span> Even though he was exhausted, he finished the report.</li>"
  "<li><span class='n'>6.</span> She studies in the morning, while I study at night.</li></ul>"
  "<div class='ex-title'>E. Correct the mistakes</div><ul class='ans'>"
  "<li><span class='n'>1.</span> <b>Although it was late</b>, we continued working. / <b>Despite the late hour</b>, we continued working. (Despite + noun/-ing, not a clause)</li>"
  "<li><span class='n'>2.</span> <b>Although it was raining</b>, the match went ahead. / <b>Despite the rain</b>, the match went ahead.</li>"
  "<li><span class='n'>3.</span> He was tired<b>;</b> nevertheless<b>,</b> he went for a run. (semicolon + comma)</li>"
  "<li><span class='n'>4.</span> <b>In spite of trying</b> her best, she didn&rsquo;t pass the exam. / <b>Although she tried</b> her best&hellip; (In spite of + -ing/noun)</li>"
  "<li><span class='n'>5.</span> I like coffee, <b>whereas</b> she prefers tea. (one connector, not two; not sentence-initial here)</li>"
  "<li><span class='n'>6.</span> He didn&rsquo;t win the award<b>;</b> nevertheless<b>,</b> he was happy. (semicolon + comma joining two clauses)</li></ul>"
  "<div class='ex-title'>F. Short production</div><p>Model: <b>1.</b> Although technology saves time, it can be distracting. <b>2.</b> Despite studying every night, he found the exam hard. <b>3.</b> She likes reading fiction, whereas her brother only reads history.</p>"
 ),
 "teacher_tip": "The one rule that fixes most errors: <b>although / even though / whereas / while</b> are followed by a subject + verb; <b>despite / in spite of</b> are followed by a noun, pronoun or -ing form. Have students name &ldquo;clause&rdquo; or &ldquo;noun/-ing&rdquo; before every choice.",
 "mistakes": [
  ["Despite it was raining, we went out.", "Despite the rain, we went out. / Although it was raining, we went out."],
  ["Although of the traffic, he arrived on time.", "Despite the traffic, he arrived on time."],
  ["It was expensive, nevertheless we bought it.", "It was expensive; nevertheless, we bought it."],
  ["In spite she was tired, she kept working.", "In spite of being tired, she kept working."]
 ],
 "activity_title": "Clause or Noun (8 min)",
 "activity_body": "Hold up a card with a connector (although / despite / whereas / in spite of / nevertheless). Students say &ldquo;+ clause&rdquo; or &ldquo;+ noun/-ing&rdquo; and make one sentence about school. Go through all seven twice.",
 "materials": MAT_G,
 "lesson_title": LT,
 "learning_objective": "Students will be able to use although, even though, despite, in spite of, whereas, while and nevertheless correctly, choosing the right form (clause vs noun/-ing) and punctuation.",
 "success_criteria": "I can follow <i>although / even though</i> with a clause and <i>despite / in spite of</i> with a noun or -ing. I can use <i>whereas / while</i> to contrast two facts. I can punctuate <i>nevertheless</i> with a semicolon and a comma.",
 "prior_knowledge": "Basic contrast with <i>but</i> and <i>however</i>; the difference between a clause and a phrase.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;It was raining. We went out.&rdquo; and ask students to join them three ways (but, although, despite). Part 2: check what follows each &ndash; a clause after <i>although</i>, a noun/-ing after <i>despite</i>."],
  ["8 min", "Presentation (I Do)", "Explain the four groups with the &ldquo;why&rdquo;. (1) <b>although / even though</b> introduce a contrasting fact (a concession) and are followed by a full clause; <i>even though</i> is stronger. (2) <b>despite / in spite of</b> mean the same but are prepositions, so they are followed by a noun, a pronoun or an -ing form &ndash; use &ldquo;despite the fact that + clause&rdquo; if you need a clause. (3) <b>whereas / while</b> contrast two different facts or situations, one in each half of the sentence. (4) <b>nevertheless</b> is a linking adverb (= however, still); it joins two independent clauses and takes a semicolon before and a comma after. Model Exercise E item 1: &ldquo;Despite it was late&rdquo; &rarr; either &ldquo;Despite the late hour&rdquo; or &ldquo;Although it was late&rdquo;."],
  ["10 min", "Guided Practice (We Do)", "Exercise B items 1&ndash;4 as a class, naming &ldquo;clause&rdquo; or &ldquo;noun/-ing&rdquo; first; then Exercise C items 1&ndash;3 together."],
  ["10 min", "Independent Practice (You Do)", "Students complete the rest of Exercise C, Exercise D and Exercise E individually, then compare Exercise D in pairs, checking commas."],
  ["7 min", "Assessment", "Review Exercise E on the board; students name the error type (wrong form / punctuation / double connector). Then the Exit Ticket."],
  ["5 min", "Closure", "Students write one Exercise F sentence with <i>whereas</i> and read it; the class checks that two facts are contrasted."]
 ],
 "followup": "Homework: write six sentences about city life vs country life, using each of the seven connectors at least once across the set.",
 "support": "Give a desk card: CLAUSE &ndash; although / even though / whereas / while; NOUN or -ING &ndash; despite / in spite of; ADVERB (; &hellip; ,) &ndash; nevertheless.",
 "challenge": "Students rewrite three Exercise D answers, moving the concession clause to the end of the sentence and adjusting the comma.",
 "anticipated_problems": [
  ["Students write &ldquo;despite / in spite of&rdquo; + a full clause (&ldquo;despite it was late&rdquo;).", "Rule: after <i>despite / in spite of</i> use a noun or -ing, or say &ldquo;despite the fact that&rdquo; + clause."],
  ["Students use two contrast connectors in one sentence (&ldquo;Although&hellip; but&hellip;&rdquo;, &ldquo;Whereas&hellip; while&hellip;&rdquo;).", "One contrast per sentence. If the sentence starts with <i>although</i>, the second clause has no connector."]
 ],
 "key_language": "<b>Grammar:</b> although / even though / whereas / while + clause; despite / in spite of + noun / -ing; nevertheless as a linking adverb (; &hellip; ,). <br><b>Board:</b> Although it was late, we stayed. &bull; Despite the rain, we went out. &bull; It rained; nevertheless, we went out.",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;Despite it was cold&hellip;&rdquo; &rarr; <i>Despite the cold / Although it was cold</i></li><li><span class='n'>2.</span> Punctuate: &ldquo;It was hard nevertheless she finished.&rdquo; &rarr; <i>&hellip;hard; nevertheless, she finished.</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_contrast_reading_b2.json",
 "ws_title": "Contrast and Concession " + BUL + " Reading " + BUL + " B2",
 "info_rows": info("Reading", "&ldquo;Is technology improving our lives?&rdquo; &ndash; contrast and concession in context", "A" + DASH + "F (comprehension, language, summary)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Before you read</div><p>Discussion &ndash; answers vary. Encourage a balanced answer (one benefit, one problem).</p>"
  "<div class='ex-title'>C. Reading comprehension</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> B</div><div class='ans-item'><span class='n'>2.</span> B</div>"
  "<div class='ans-item'><span class='n'>3.</span> B</div><div class='ans-item'><span class='n'>4.</span> C</div>"
  "<div class='ans-item'><span class='n'>5.</span> It signals a contrast: after listing the benefits, the writer uses <i>nevertheless</i> to add the qualifying point that progress is uneven and carries risks.</div>"
  "<div class='ans-item'><span class='n'>6.</span> Generally positive but cautious: &ldquo;improving our lives in many important ways&rdquo; / &ldquo;real benefits to millions&rdquo;, with the warning that benefits must reach everyone &ldquo;not just a privileged few&rdquo;.</div></div>"
  "<div class='ex-title'>D. Language in context</div><ul class='ans'>"
  "<li><span class='n'>1.</span> &ldquo;<b>Although</b> some people worry that we are too dependent on our devices, it is clear that technology has brought real benefits&hellip;&rdquo; (or the <i>even though</i> traditional-schools sentence).</li>"
  "<li><span class='n'>2.</span> &ldquo;<b>Despite</b> the high costs of some medical technologies, they have improved the quality of life&hellip;&rdquo; &ndash; followed by a <b>noun phrase</b>.</li>"
  "<li><span class='n'>3.</span> &ldquo;&hellip;social media helps us stay connected, <b>whereas</b> it can also lead to distraction&hellip;&rdquo; (or &ldquo;While many enjoy&hellip;&rdquo;).</li>"
  "<li><span class='n'>4.</span> &ldquo;&hellip;improving our lives&hellip;; <b>nevertheless</b>, the progress is not equally shared&hellip;&rdquo; &ndash; a linking adverb (= however) adding a contrasting idea after a positive statement.</li>"
  "<li><span class='n'>5.</span> (model) &ldquo;Although some people worry&hellip;&rdquo; &rarr; &ldquo;<b>Even though</b> some people worry&hellip;&rdquo;.</li></ul>"
  "<div class='ex-title'>E. Complete the summary</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> tasks</div><div class='ans-item'><span class='n'>2.</span> diagnoses</div>"
  "<div class='ans-item'><span class='n'>3.</span> even though / although</div><div class='ans-item'><span class='n'>4.</span> However / Nevertheless</div>"
  "<div class='ans-item'><span class='n'>5.</span> but / whereas / although</div><div class='ans-item'><span class='n'>6.</span> nevertheless / but / however</div></div>"
  "<div class='ex-title'>F. Reflection</div><p>Opinion paragraph (3&ndash;4 sentences) &ndash; must use at least two contrast or concession structures. Check the position is clear.</p>"
 ),
 "teacher_tip": "Exercise B asks students to underline every contrast/concession connector as they read. Exercise D then just asks them to classify what they underlined by form (clause after <i>although</i>, noun after <i>despite</i>, adverb <i>nevertheless</i>).",
 "mistakes": [
  ["Despite technology has many benefits, it also has risks.", "Despite its many benefits, technology also has risks. / Although technology has many benefits, it also has risks."],
  ["Whereas the high costs, medical technology has improved lives.", "Despite the high costs, medical technology has improved lives."],
  ["Social media connects people, nevertheless it can isolate them too.", "Social media connects people; nevertheless, it can isolate them too."],
  ["Even though of the digital divide, more people can learn online.", "Despite the digital divide, more people can learn online."]
 ],
 "activity_title": "Two Sides (8 min)",
 "activity_body": "Give a topic from the text (online learning, social media, healthcare tech). Student A says a benefit, student B answers with a concession sentence (&ldquo;Even though&hellip;, &hellip;&rdquo; / &ldquo;Despite&hellip;, &hellip;&rdquo;). Swap roles for the next topic.",
 "materials": MAT_R,
 "lesson_title": LT,
 "learning_objective": "Students will be able to read a balanced argument text for gist and detail and identify how contrast and concession connectors are used, including their form and punctuation.",
 "success_criteria": "I can find the writer&rsquo;s overall position and specific reasons. I can name the form after each connector (clause / noun / adverb). I can complete a summary with a suitable contrast or concession word.",
 "prior_knowledge": "The seven connectors and their forms (from the Grammar worksheet); reading for gist and detail.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: ask &ldquo;How has technology improved your life?&rdquo; and collect answers. Part 2: for each, elicit a &ldquo;but&rdquo; &ndash; a problem it also creates &ndash; and write one as &ldquo;Although&hellip;, &hellip;&rdquo;."],
  ["8 min", "Presentation (I Do)", "Recap the forms the text uses: <b>although / even though</b> + clause (a concession); <b>despite / in spite of</b> + noun or -ing; <b>whereas / while</b> to set two facts against each other; <b>nevertheless</b> as a linking adverb after a semicolon. Read paragraph 2 aloud, stop at &ldquo;Despite the high costs&hellip;&rdquo; and show that a noun phrase, not a clause, follows."],
  ["10 min", "Guided Practice (We Do)", "Students read once for gist, then do Exercise C items 1&ndash;3 as a class, underlining the proof sentence for each."],
  ["10 min", "Independent Practice (You Do)", "Students complete Exercise C 4&ndash;6, Exercise D and Exercise E individually; compare Exercise D in pairs."],
  ["7 min", "Assessment", "Review Exercise E; for each gap a student says why that connector fits. Then the Exit Ticket."],
  ["5 min", "Closure", "Two students read their Exercise F opinion; the class checks that two contrast/concession structures are used correctly."]
 ],
 "followup": "Homework: write a balanced 100&ndash;120 word answer to &ldquo;Is technology improving our lives?&rdquo; using at least three different connectors from the text.",
 "support": "Give the text with the connectors already underlined; students only classify the form and answer Exercise C 1&ndash;3.",
 "challenge": "Students rewrite two sentences from the text, swapping <i>although</i> for <i>despite</i> (and vice versa) with the correct form change.",
 "anticipated_problems": [
  ["In Exercise D students quote a <i>despite</i> sentence but say a clause follows.", "Make them write out the exact words after <i>despite</i> &ndash; they will see it is a noun phrase (&ldquo;the high costs of some medical technologies&rdquo;)."],
  ["In Exercise E students put <i>despite</i> in a gap that is followed by a clause.", "Check the words after the gap: subject + verb &rarr; although / even though / whereas; noun &rarr; despite / in spite of."]
 ],
 "key_language": "<b>Grammar:</b> although / even though + clause; despite / in spite of + noun / -ing; whereas / while contrast two facts; nevertheless links two clauses. <br><b>Board:</b> Despite the high costs, &hellip; &bull; &hellip;connected, whereas it can also isolate &bull; &hellip;in many ways; nevertheless, &hellip;",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Clause or noun after &ldquo;despite&rdquo;? &rarr; <i>noun / -ing</i></li><li><span class='n'>2.</span> Fill: &ldquo;It is useful, ___ it has risks.&rdquo; &rarr; <i>but / although / nevertheless</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_contrast_writing_b2.json",
 "ws_title": "Contrast and Concession " + BUL + " Writing " + BUL + " B2",
 "info_rows": info("Writing", "Develop a balanced argument with contrast and concession structures", "A" + DASH + "F (model, plan, 180" + DASH + "220-word balanced paragraph)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Analyse the model</div><ul class='ans'>"
  "<li><span class='n'>1.</span> Advantages: instant access to information; helps us stay in touch with friends and family; makes work and study more flexible; brings people closer when distance makes contact hard; improved healthcare; created new job opportunities; made education more accessible; new forms of entertainment.</li>"
  "<li><span class='n'>2.</span> Disadvantages / concerns: it can be expensive; some argue technology isolates us; concerns about privacy and the constant flow of information; &ldquo;technology is not a perfect solution, and we must use it wisely&rdquo;.</li>"
  "<li><span class='n'>3.</span> Two concession connectors: <b>Although</b> and <b>Even though</b> (also <i>Despite</i> + noun, <i>Whereas</i> for contrast).</li>"
  "<li><span class='n'>4.</span> The writer ends in a balanced way by conceding the technology &ldquo;is not a perfect solution&rdquo; and giving a qualified conclusion: &ldquo;I believe technology improves our lives, but only if we are aware of the risks and make a conscious effort to maintain a healthy balance.&rdquo;</li></ul>"
  "<div class='ex-title'>B. Organise your ideas / C. Useful language</div><p>Planning notes and phrase bank &ndash; not marked. Check the plan has both sides and a final opinion, and that phrases from C appear in Exercise E.</p>"
  "<div class='ex-title'>D&ndash;E. Writing task</div><p>Model band (strong response): both sides of the argument presented; at least four contrast or concession structures used accurately with correct form and punctuation; ideas supported with examples; a clear, balanced final judgement; 180&ndash;220 words; logically organised.</p>"
  "<div class='ex-title'>F. Self-check</div><p>Students tick each box; spot-check &ldquo;at least four contrast or concession structures&rdquo; and &ldquo;presented both sides&rdquo;.</p>"
 ),
 "teacher_tip": "Insist on a balanced structure: one paragraph or half for advantages, one for concerns, then a qualified conclusion (&ldquo;Overall&hellip; but only if&hellip;&rdquo;). Students choose four phrases from Exercise C and mark where each will go before drafting.",
 "mistakes": [
  ["Although technology is expensive, but it is useful.", "Although technology is expensive, it is useful."],
  ["Despite it isolates some people, it also connects others.", "Despite isolating some people, it also connects others."],
  ["Technology has risks, nevertheless we should not stop using it.", "Technology has risks; nevertheless, we should not stop using it."],
  ["Whereas the benefits, there are also real concerns.", "Despite the benefits, there are also real concerns."]
 ],
 "activity_title": "Concede and Counter (8 min)",
 "activity_body": "Student A makes a one-sided claim (&ldquo;Social media is bad for young people.&rdquo;). Student B answers with a concession + counter (&ldquo;Although it can be bad, it also&hellip;&rdquo;). Do four rounds, swapping who claims.",
 "materials": MAT_W,
 "lesson_title": LT,
 "learning_objective": "Students will be able to plan and write a balanced 180&ndash;220-word argument paragraph, using contrast and concession structures accurately to present both sides and reach a qualified conclusion.",
 "success_criteria": "I can present advantages and disadvantages. I can use <i>although / even though</i> + clause and <i>despite / in spite of</i> + noun accurately. I can punctuate <i>nevertheless</i> and <i>however</i>. I can give a balanced final judgement in 180&ndash;220 words.",
 "prior_knowledge": "The seven connectors and their forms; paragraph structure and how to state an opinion.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;Technology is good / bad for us&rdquo; and take a quick class vote. Part 2: ask a &ldquo;yes&rdquo; voter for one drawback and a &ldquo;no&rdquo; voter for one benefit &ndash; write both as concession sentences."],
  ["8 min", "Presentation (I Do)", "Read the model. Show the balanced move each time: <b>Although</b> it can be expensive, it gives us&hellip; (concede a cost, then a benefit); <b>Even though</b> some people argue&hellip;, I believe&hellip; (concede an opinion, then counter it); <b>Despite</b> concerns about privacy, digital tools have&hellip; (noun after despite); <b>Whereas</b> older generations had limited resources, we can now&hellip; (contrast two situations); <b>Nevertheless</b>, technology is not a perfect solution (qualify the positive). End with the model&rsquo;s conclusion pattern: &ldquo;Overall, I believe&hellip;, but only if&hellip;&rdquo;."],
  ["10 min", "Guided Practice (We Do)", "As a class, answer Exercise A questions 1&ndash;3 in note form, then plan a shared balanced paragraph on &ldquo;smartphones in school&rdquo; using the Exercise B boxes."],
  ["10 min", "Independent Practice (You Do)", "Students complete their Exercise B plan and draft the paragraph (Exercise E), 180&ndash;220 words, with at least four contrast/concession structures and a qualified conclusion."],
  ["7 min", "Assessment", "Students run the Exercise F self-check, then a partner circles every connector and checks form and punctuation."],
  ["5 min", "Closure", "Two students read their concluding sentence; the class checks it is balanced, not one-sided."]
 ],
 "followup": "Homework: redraft after feedback, then write a two-sentence answer to a different question using <i>despite</i> + noun and <i>although</i> + clause.",
 "support": "Give a paragraph frame with the connectors and slots labelled (Concede&hellip;, but&hellip; / Despite&hellip;, &hellip; / Overall&hellip;). Students fill the ideas.",
 "challenge": "Students add one sentence using &ldquo;while it is true that&hellip;, &hellip;&rdquo; and one using &ldquo;despite the fact that&hellip;&rdquo; to widen the range of structures.",
 "anticipated_problems": [
  ["Students pair a connector with <i>but</i> (&ldquo;Although&hellip;, but&hellip;&rdquo;).", "One connector per contrast. If the sentence opens with <i>although / even though</i>, the main clause has no <i>but</i>."],
  ["The paragraph argues only one side and adds a connector for show.", "Require a real point on each side before the conclusion; the connector must join two genuinely opposing ideas."]
 ],
 "key_language": "<b>Grammar:</b> although / even though + clause; despite / in spite of + noun / -ing; whereas / while for contrast; nevertheless / however as linking adverbs. <b>Conclusion:</b> Overall&hellip;, but only if&hellip; <br><b>Board:</b> Although it is expensive, &hellip; &bull; Despite privacy concerns, &hellip; &bull; &hellip;; nevertheless, &hellip;",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;Although it is risky, but useful.&rdquo; &rarr; <i>Although it is risky, it is useful.</i></li><li><span class='n'>2.</span> Fix: &ldquo;Despite it costs a lot&hellip;&rdquo; &rarr; <i>Despite the cost / Although it costs a lot</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_contrast_practice_b2.json",
 "ws_title": "Contrast and Concession " + BUL + " Practice " + BUL + " B2",
 "info_rows": info("Practice", "Contrast and concession structures: connector choice, gap-fill, error correction, combining", "A" + DASH + "F"),
 "answer_key_html": (
  "<div class='ex-title'>A. Choose the best connector</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> A &ndash; Although</div><div class='ans-item'><span class='n'>2.</span> C &ndash; in spite of</div>"
  "<div class='ans-item'><span class='n'>3.</span> B &ndash; although (accept A whereas)</div><div class='ans-item'><span class='n'>4.</span> A &ndash; Despite (accept B In spite of)</div>"
  "<div class='ans-item'><span class='n'>5.</span> C &ndash; despite</div><div class='ans-item'><span class='n'>6.</span> A &ndash; while</div>"
  "<div class='ans-item'><span class='n'>7.</span> A &ndash; Although</div><div class='ans-item'><span class='n'>8.</span> C &ndash; even though</div>"
  "<div class='ans-item'><span class='n'>9.</span> B &ndash; Despite (+ -ing)</div><div class='ans-item'><span class='n'>10.</span> C &ndash; nevertheless</div></div>"
  "<div class='ex-title'>B. Complete the text</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> While / Although</div><div class='ans-item'><span class='n'>2.</span> even though</div>"
  "<div class='ans-item'><span class='n'>3.</span> Despite</div><div class='ans-item'><span class='n'>4.</span> Whereas</div>"
  "<div class='ans-item'><span class='n'>5.</span> In spite of</div><div class='ans-item'><span class='n'>6.</span> Despite</div>"
  "<div class='ans-item'><span class='n'>7.</span> nevertheless</div><div class='ans-item'><span class='n'>8.</span> Although</div></div>"
  "<div class='ex-title'>C. Correct the mistakes</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> <b>Despite / In spite of the rain</b>, we decided to go for a walk.</div>"
  "<div class='ans-item'><span class='n'>2.</span> <b>Despite the long journey</b>, she was still smiling. (no <i>of</i>)</div>"
  "<div class='ans-item'><span class='n'>3.</span> He was tired<b>;</b> nevertheless<b>,</b> he finished the project.</div>"
  "<div class='ans-item'><span class='n'>4.</span> <b>In spite of the fact that</b> it was expensive, they bought it.</div>"
  "<div class='ans-item'><span class='n'>5.</span> While she didn&rsquo;t like the idea, <b>she</b> agreed to try it. (add subject)</div>"
  "<div class='ans-item'><span class='n'>6.</span> He enjoys his job <b>despite the low salary</b>. / &hellip;<b>although the salary is low</b>.</div></div>"
  "<div class='ex-title'>D. Rewrite / combine</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> She passed the exam, although it was very difficult.</div>"
  "<div class='ans-item'><span class='n'>2.</span> He decided to take the job despite the low pay.</div>"
  "<div class='ans-item'><span class='n'>3.</span> I prefer reading books, whereas my sister prefers watching films.</div>"
  "<div class='ans-item'><span class='n'>4.</span> They continued the meeting even though they were very tired.</div>"
  "<div class='ans-item'><span class='n'>5.</span> The weather was terrible; nevertheless, we enjoyed the trip.</div>"
  "<div class='ans-item'><span class='n'>6.</span> She was working from home, while her colleague was in the office.</div></div>"
  "<div class='ex-title'>E. Extended context challenge &ndash; Remote work</div><p><b>1.</b> &ldquo;&hellip;popular in recent years, <b>although</b> it offers many advantages&rdquo; &rarr; no contrast; use <b>as / since</b>, or a full stop. <b>2.</b> &ldquo;&hellip;enjoy the flexibility, <b>nevertheless</b> they can organise their time better&rdquo; &rarr; this is a reason: <b>as / because</b>. <b>3.</b> &ldquo;<b>even though not it suits everyone</b>&rdquo; &rarr; word order: <b>even though it does not suit everyone</b>. (&ldquo;In spite of working from home&hellip; isolating&rdquo; is acceptable &ndash; treat as correct.)</p>"
  "<div class='ex-title'>F. Personal response</div><p>Model: <b>1.</b> Although online courses are cheaper, they need self-discipline. <b>2.</b> Despite living far from campus, she never misses a class. <b>3.</b> City life is fast, whereas village life is slow.</p>"
 ),
 "teacher_tip": "Before Exercise A, students name the form of the words after the gap &ndash; subject + verb, a noun, or an -ing. That alone rules out most options. Exercise E is about <i>meaning</i>: a connector must join two genuinely opposing ideas, not a reason.",
 "mistakes": [
  ["Despite of his age, he runs every day.", "Despite his age, he runs every day."],
  ["Although the noise, she kept studying.", "Despite the noise, she kept studying. / Although it was noisy, she kept studying."],
  ["He failed the test, nevertheless he tried hard.", "He failed the test; nevertheless, he tried hard."],
  ["Whereas I like tea while she likes coffee.", "I like tea, whereas she likes coffee."]
 ],
 "activity_title": "Form First (8 min)",
 "activity_body": "Read a half-sentence (&ldquo;___ it was raining&hellip;&rdquo;, &ldquo;___ the rain&hellip;&rdquo;, &ldquo;___ studying hard&hellip;&rdquo;). Students call out every connector that fits the form and one that does not, with the reason.",
 "materials": MAT_G,
 "lesson_title": LT,
 "learning_objective": "Students will be able to choose and correct contrast and concession connectors across sentences and a text, matching form (clause / noun / -ing / adverb) and meaning, and combine sentences with a given connector.",
 "success_criteria": "I can choose the connector that fits the form after it. I can correct wrong form, wrong punctuation and double connectors. I can combine two sentences with a given connector without changing the meaning.",
 "prior_knowledge": "The seven connectors and their forms and punctuation (from the Grammar worksheet).",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;___ it was late&rdquo; and &ldquo;___ the late hour&rdquo; and ask which connectors fit each. Part 2: write &ldquo;Although&hellip;, but&hellip;&rdquo; and ask what is wrong (two connectors)."],
  ["8 min", "Presentation (I Do)", "Quick review: <b>although / even though / whereas / while</b> take a clause (subject + verb); <b>despite / in spite of</b> take a noun, pronoun or -ing (add &ldquo;the fact that&rdquo; for a clause); <b>nevertheless</b> is an adverb needing a semicolon before and a comma after; never use two contrast connectors in one sentence. For Exercise E, add the meaning check: does the connector join two <i>opposing</i> ideas, or is one half a <i>reason</i>? Model Exercise C item 1 and Exercise E&rsquo;s &ldquo;although it offers many advantages&rdquo;."],
  ["10 min", "Guided Practice (We Do)", "Exercise A items 1&ndash;5 as a class (form first), then Exercise B items 1&ndash;3 together."],
  ["12 min", "Independent Practice (You Do)", "Students complete the rest of Exercise B, Exercise C, Exercise D and Exercise E individually."],
  ["6 min", "Assessment", "Review Exercise E &ndash; students explain why each flagged connector is wrong and give a fix. Then the Exit Ticket."],
  ["4 min", "Closure", "In pairs, students read two Exercise D combinations aloud, checking commas and that the meaning is unchanged."]
 ],
 "followup": "Homework: write six sentences contrasting two hobbies, using each connector at least once across the set.",
 "support": "Give the CLAUSE / NOUN-ING / ADVERB card; students label every gap with the form before choosing.",
 "challenge": "Students rewrite three Exercise A sentences with a different connector of the same meaning, changing the form as needed.",
 "anticipated_problems": [
  ["Students choose <i>despite / in spite of</i> before a clause in Exercise A/B.", "Check the next words: subject + verb &rarr; although / even though / whereas / while; noun or -ing &rarr; despite / in spite of."],
  ["In Exercise E students &ldquo;correct&rdquo; a connector that is actually fine, or miss one that joins a reason not a contrast.", "Ask for each: are the two ideas opposite? If one half explains <i>why</i>, the connector should be <i>as / because</i>, not a contrast word."]
 ],
 "key_language": "<b>Grammar:</b> clause &ndash; although / even though / whereas / while; noun / -ing &ndash; despite / in spite of; adverb &ndash; nevertheless (; &hellip; ,); one contrast connector per sentence. <br><b>Board:</b> Although it rained&hellip; / Despite the rain&hellip; &bull; &hellip;tired; nevertheless, &hellip; &bull; NOT &ldquo;Although&hellip; but&hellip;&rdquo;",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;Despite of the cost&hellip;&rdquo; &rarr; <i>Despite the cost</i></li><li><span class='n'>2.</span> Fix: &ldquo;Although he was tired, but he kept going.&rdquo; &rarr; <i>&hellip;tired, he kept going.</i></li></ul>"
})
w(TES[-1])

print("--- contrast set done ---")

# =====================================================================
# 4. CAUSE, REASON, PURPOSE AND RESULT
# =====================================================================
TES.append({
 "_file": "te_cause_grammar_b2.json",
 "ws_title": "Cause, Reason, Purpose and Result " + BUL + " Grammar " + BUL + " B2",
 "info_rows": info("Grammar", "due to, owing to, because of, so that, in order to, therefore, consequently", "6 (A" + DASH + "F)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Grammar overview</div><p>Reference table &ndash; no written answers. Check students can name the function (reason / purpose / result) and the form (+ noun phrase / + clause / + base verb) of each linker.</p>"
  "<div class='ex-title'>B. Choose the best option</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> B &ndash; due to</div><div class='ans-item'><span class='n'>2.</span> C &ndash; so that</div>"
  "<div class='ans-item'><span class='n'>3.</span> B &ndash; due to</div><div class='ans-item'><span class='n'>4.</span> A &ndash; in order to</div>"
  "<div class='ans-item'><span class='n'>5.</span> B &ndash; therefore</div><div class='ans-item'><span class='n'>6.</span> B &ndash; owing to</div>"
  "<div class='ans-item'><span class='n'>7.</span> B &ndash; therefore</div><div class='ans-item'><span class='n'>8.</span> A &ndash; in order to</div></div>"
  "<div class='ex-title'>C. Complete the sentences</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> because of / due to / owing to</div><div class='ans-item'><span class='n'>2.</span> in order to</div>"
  "<div class='ans-item'><span class='n'>3.</span> in order to</div><div class='ans-item'><span class='n'>4.</span> therefore / consequently</div>"
  "<div class='ans-item'><span class='n'>5.</span> because of / due to / owing to</div><div class='ans-item'><span class='n'>6.</span> in order to</div>"
  "<div class='ans-item'><span class='n'>7.</span> therefore / consequently</div><div class='ans-item'><span class='n'>8.</span> so that</div></div>"
  "<div class='ex-title'>D. Rewrite / combine</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> The traffic was terrible; therefore, we arrived late.</div>"
  "<div class='ans-item'><span class='n'>2.</span> She's learning French in order to work in an international company.</div>"
  "<div class='ans-item'><span class='n'>3.</span> The event was cancelled due to a security risk.</div>"
  "<div class='ans-item'><span class='n'>4.</span> He left a note so that we would know where he was.</div>"
  "<div class='ans-item'><span class='n'>5.</span> Many shops are closing owing to the popularity of online shopping.</div>"
  "<div class='ans-item'><span class='n'>6.</span> The weather improved; consequently, we decided to go for a walk.</div></div>"
  "<div class='ex-title'>E. Correct the mistakes</div><ul class='ans'>"
  "<li><span class='n'>1.</span> <b>Because of / Due to</b> the high demand, ticket prices increased. (<i>because to</i> is not a phrase)</li>"
  "<li><span class='n'>2.</span> He studies hard <b>so that he can</b> get a better job. / &hellip;<b>in order to</b> get a better job.</li>"
  "<li><span class='n'>3.</span> The event was cancelled <b>due to</b> bad organisation. (add <i>to</i>)</li>"
  "<li><span class='n'>4.</span> They moved house <b>in order to</b> be closer to their school. (purpose, not result)</li>"
  "<li><span class='n'>5.</span> <b>Owing to</b> the improvements, the service is running smoothly. (add <i>to</i>)</li>"
  "<li><span class='n'>6.</span> She left early <b>in order to attend</b> the meeting. / &hellip;<b>so that she could attend</b> the meeting.</li></ul>"
  "<div class='ex-title'>F. Short production</div><p>Model: <b>1.</b> The flight was delayed due to fog. <b>2.</b> I set an alarm so that I would not oversleep. <b>3.</b> Prices rose sharply; consequently, sales fell.</p>"
 ),
 "teacher_tip": "Two questions before every choice: (1) reason, purpose or result? (2) what follows the gap &ndash; a noun (because of / due to / owing to), a clause (so that / therefore / consequently) or a base verb (in order to)? Get both answers aloud first.",
 "mistakes": [
  ["Because of it was raining, the match was cancelled.", "Because it was raining, the match was cancelled. / Because of the rain, the match was cancelled."],
  ["He saved money for to buy a car.", "He saved money in order to buy a car."],
  ["Due to the strike, therefore many trains were cancelled.", "Due to the strike, many trains were cancelled."],
  ["She left early so that catch the bus.", "She left early so that she could catch the bus."]
 ],
 "activity_title": "Reason, Purpose or Result (8 min)",
 "activity_body": "Call out a sentence half (&ldquo;&hellip;because of the storm&rdquo;, &ldquo;&hellip;so that everyone could hear&rdquo;, &ldquo;&hellip;therefore the road was closed&rdquo;). Students shout the function and complete the sentence, then say what form followed the linker.",
 "materials": MAT_G,
 "lesson_title": LT,
 "learning_objective": "Students will be able to use because of, due to, owing to, so that, in order to, therefore and consequently correctly, choosing by function (reason / purpose / result) and by the form that follows (noun / clause / base verb).",
 "success_criteria": "I can follow <i>because of / due to / owing to</i> with a noun phrase. I can use <i>in order to</i> + base verb and <i>so that</i> + clause for purpose. I can use <i>therefore / consequently</i> + clause for a result, with the right punctuation.",
 "prior_knowledge": "Basic <i>because</i> and <i>so</i>; the difference between a noun phrase and a clause.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;The road was closed because ___&rdquo; and &ldquo;The road was closed because of ___&rdquo; and elicit what fits each (clause vs noun). Part 2: write &ldquo;She left early ___ catch the bus&rdquo; and elicit <i>in order to</i> vs <i>so that she could</i>."],
  ["8 min", "Presentation (I Do)", "Explain the three functions with the &ldquo;why&rdquo;. <b>Reason (cause):</b> <i>because of</i>, <i>due to</i>, <i>owing to</i> answer &ldquo;why did it happen?&rdquo; and are prepositions, so a noun phrase follows (&ldquo;due to <b>bad weather</b>&rdquo;); use plain <i>because</i> + clause if you need a subject and verb. <b>Purpose (intention):</b> <i>in order to</i> + base verb and <i>so that</i> + subject + modal answer &ldquo;what for?&rdquo; &ndash; <i>in order to</i> when the subject is the same, <i>so that</i> when it can change or you need <i>can/could/would</i>. <b>Result (consequence):</b> <i>therefore</i> and <i>consequently</i> introduce what happened next; they link two clauses and take a semicolon before and a comma after. Model Exercise E items 1 (<i>because to</i> &rarr; <i>because of</i>) and 5 (<i>owing</i> &rarr; <i>owing to</i>)."],
  ["10 min", "Guided Practice (We Do)", "Exercise B items 1&ndash;4 as a class (function + form first), then Exercise C items 1&ndash;3 together."],
  ["10 min", "Independent Practice (You Do)", "Students complete the rest of Exercise C, Exercise D and Exercise E individually, then compare Exercise D in pairs, checking punctuation."],
  ["7 min", "Assessment", "Review Exercise E on the board; students name the error (missing <i>to</i> / wrong function / <i>so that</i> without a modal). Then the Exit Ticket."],
  ["5 min", "Closure", "Students write one Exercise F sentence for &ldquo;result&rdquo; and read it; the class checks the semicolon and comma."]
 ],
 "followup": "Homework: write six sentences about a change in your town (a reason, a purpose and a result for each of two changes), using a different linker each time.",
 "support": "Give a desk card: NOUN &ndash; because of / due to / owing to; BASE VERB &ndash; in order to; CLAUSE (purpose) &ndash; so that + can/could; CLAUSE (result) &ndash; therefore / consequently (; &hellip; ,).",
 "challenge": "Students rewrite three Exercise C sentences, turning a reason into a result (or vice versa) and adjusting the linker and word order.",
 "anticipated_problems": [
  ["Students write &ldquo;because of&rdquo; / &ldquo;due to&rdquo; + a full clause (&ldquo;due to it was raining&rdquo;).", "Rule: <i>because of / due to / owing to</i> + noun phrase; <i>because</i> + subject + verb. Turn the clause into a noun (&ldquo;the rain&rdquo;)."],
  ["Students use <i>so that</i> with a bare verb (&ldquo;so that catch the bus&rdquo;).", "<i>So that</i> needs a subject and usually <i>can / could / would</i>. If you only have a verb, use <i>in order to</i>."]
 ],
 "key_language": "<b>Grammar:</b> because of / due to / owing to + noun; in order to + base verb; so that + subject + can/could; therefore / consequently + clause (; &hellip; ,). <br><b>Board:</b> due to bad weather &bull; in order to save time &bull; so that everyone could hear &bull; &hellip;late; therefore, &hellip;",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;due to it was foggy&rdquo; &rarr; <i>due to the fog / because it was foggy</i></li><li><span class='n'>2.</span> Fix: &ldquo;so that finish early&rdquo; &rarr; <i>in order to finish early / so that we could finish early</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_cause_reading_b2.json",
 "ws_title": "Cause, Reason, Purpose and Result " + BUL + " Reading " + BUL + " B2",
 "info_rows": info("Reading", "Causes and consequences of urban pollution; linking structures in context", "A" + DASH + "F (comprehension, table, summary)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Before you read</div><p>Discussion &ndash; answers vary. Encourage students to name a cause and rank it.</p>"
  "<div class='ex-title'>C. Reading comprehension</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> C &ndash; A combination of factors</div><div class='ans-item'><span class='n'>2.</span> B &ndash; Because of congestion</div>"
  "<div class='ans-item'><span class='n'>3.</span> B &ndash; Chemicals can leak into the soil and rivers</div><div class='ans-item'><span class='n'>4.</span> respiratory problems and heart disease</div>"
  "<div class='ans-item'><span class='n'>5.</span> B &ndash; In order to have a cleaner environment</div>"
  "<div class='ans-item'><span class='n'>6.</span> (1) invest in cleaner public transport / cycling infrastructure / green areas; (2) stricter rules for industry and better waste management.</div></div>"
  "<div class='ex-title'>D. Language in context &ndash; complete the table</div><ul class='ans'>"
  "<li><span class='n'>1.</span> <b>because of</b> &rarr; &ldquo;because of a combination of factors&rdquo; &rarr; reason (cause)</li>"
  "<li><span class='n'>2.</span> <b>due to</b> &rarr; &ldquo;due to the burning of fossil fuels&rdquo; &rarr; reason (cause)</li>"
  "<li><span class='n'>3.</span> <b>owing to</b> &rarr; &ldquo;owing to the lack of reliable and affordable public transport&rdquo; &rarr; reason (cause)</li>"
  "<li><span class='n'>4.</span> <b>so that / in order to</b> &rarr; &ldquo;so that people have greener&hellip; alternatives&rdquo; / &ldquo;in order to find a cleaner&hellip; environment&rdquo; &rarr; purpose (intention)</li>"
  "<li><span class='n'>5.</span> <b>therefore / consequently</b> &rarr; &ldquo;Therefore, harmful chemicals can leak&hellip;&rdquo; / &ldquo;Consequently, some families decide to move&hellip;&rdquo; (also &ldquo;As a result&hellip;&rdquo;) &rarr; result (consequence)</li></ul>"
  "<div class='ex-title'>E. Complete the summary</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> traffic</div><div class='ans-item'><span class='n'>2.</span> waste</div>"
  "<div class='ans-item'><span class='n'>3.</span> due to (because of / owing to)</div><div class='ans-item'><span class='n'>4.</span> as a result (therefore / consequently)</div>"
  "<div class='ans-item'><span class='n'>5.</span> public transport</div><div class='ans-item'><span class='n'>6.</span> future</div></div>"
  "<div class='ex-title'>F. Reflection</div><p>Short paragraph (80&ndash;120 words) &ndash; look for a clear priority and reasons expressed with cause/purpose/result linkers.</p>"
 ),
 "teacher_tip": "The text is organised by function: paragraph 2 = causes (because of / due to / owing to), paragraph 3&ndash;4 = results (therefore / as a result / consequently), paragraph 5 = purpose (so that / in order to). Point this out before Exercise D and the table fills itself.",
 "mistakes": [
  ["Pollution exists because a combination of factors.", "Pollution exists because of a combination of factors."],
  ["Cities are investing in transport so that reduce cars.", "Cities are investing in transport so that people use fewer cars. / ...in order to reduce cars."],
  ["Owing the fossil fuels, cars produce harmful gases.", "Owing to fossil fuels, cars produce harmful gases."],
  ["Recycling is inefficient, therefore of chemicals leak into rivers.", "Recycling is inefficient; therefore, chemicals leak into rivers."]
 ],
 "activity_title": "Cause and Effect Chain (8 min)",
 "activity_body": "Start a chain: &ldquo;There are more cars&hellip;&rdquo;. Each student adds a link with a linker (&ldquo;&hellip;therefore there is more traffic&hellip;&rdquo;, &ldquo;&hellip;consequently the air is worse&hellip;&rdquo;, &ldquo;&hellip;so families move away&hellip;&rdquo;). Keep it going for six links.",
 "materials": MAT_R,
 "lesson_title": LT,
 "learning_objective": "Students will be able to read an explanatory text for cause&ndash;effect relationships and identify how reason, purpose and result linkers connect ideas in context.",
 "success_criteria": "I can find the main causes, consequences and solutions in the text. I can match a linker from the text to its function (reason / purpose / result) and quote its example. I can complete a summary with a suitable linker.",
 "prior_knowledge": "The seven linkers and their functions and forms (from the Grammar worksheet); reading for detail.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: ask &ldquo;What are the main causes of pollution in cities?&rdquo; and list four on the board. Part 2: for one cause, build a chain &ndash; cause &rarr; effect &rarr; effect &ndash; using <i>therefore</i> and <i>as a result</i>."],
  ["8 min", "Presentation (I Do)", "Recap the three functions and their forms: <b>reason</b> &ndash; because of / due to / owing to + noun; <b>purpose</b> &ndash; so that + clause, in order to + base verb; <b>result</b> &ndash; therefore / consequently + clause. Read paragraph 2 aloud, stopping at each linker to name the function and the noun or clause that follows."],
  ["10 min", "Guided Practice (We Do)", "Students read once for gist, then do Exercise C items 1&ndash;3 as a class, underlining the sentence that proves each answer. Start the Exercise D table together (rows 1&ndash;2)."],
  ["10 min", "Independent Practice (You Do)", "Students complete Exercise C 4&ndash;6, the rest of the Exercise D table and Exercise E individually."],
  ["7 min", "Assessment", "Review the Exercise D table on the board; each row a student names the function and reads the example. Then the Exit Ticket."],
  ["5 min", "Closure", "Two students read one sentence of their Exercise F answer; the class identifies the linker and its function."]
 ],
 "followup": "Homework: write a 100-word paragraph about a local environmental problem, with at least one reason linker, one purpose linker and one result linker.",
 "support": "Give the text with the seven linkers highlighted; students only classify the function and fill the Exercise D table.",
 "challenge": "Students rewrite two result sentences from the text as purpose sentences (and vice versa), changing the linker and adjusting the verb.",
 "anticipated_problems": [
  ["Students fill the Exercise D table from memory of the rules, not from the text.", "Every row needs the exact quoted words from the text, then the function."],
  ["Students put <i>therefore</i> in an Exercise E gap that is followed by a noun.", "Check the words after the gap: noun &rarr; because of / due to / owing to; clause &rarr; therefore / consequently / as a result."]
 ],
 "key_language": "<b>Grammar:</b> reason &ndash; because of / due to / owing to + noun; purpose &ndash; so that / in order to; result &ndash; therefore / consequently / as a result. <br><b>Board:</b> due to fossil fuels &bull; so that people have cleaner options &bull; Therefore, chemicals leak into rivers.",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Function of &ldquo;in order to&rdquo;? &rarr; <i>purpose</i></li><li><span class='n'>2.</span> Fill: &ldquo;___ the traffic, journeys are slow.&rdquo; &rarr; <i>Because of / Due to / Owing to</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_cause_writing_b2.json",
 "ws_title": "Cause, Reason, Purpose and Result " + BUL + " Writing " + BUL + " B2",
 "info_rows": info("Writing", "Explain relationships between causes and effects with linking structures", "A" + DASH + "F (model, plan, 180" + DASH + "220-word paragraph)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Analyse the model</div><ul class='ans'>"
  "<li><span class='n'>1.</span> Causes: the large number of cars on the roads and the emissions from factories.</li>"
  "<li><span class='n'>2.</span> Solutions and their purposes: improve public transport and create more green spaces <b>so that</b> people can travel without cars and enjoy cleaner neighbourhoods; the community must support the changes <b>in order to</b> make them effective.</li>"
  "<li><span class='n'>3.</span> Consequences: air quality has deteriorated; many people suffer from breathing problems; more children are developing asthma; there is greater pressure on healthcare services (and the city could become a cleaner, more pleasant place if action is taken).</li>"
  "<li><span class='n'>4.</span> Linkers used: <i>Owing to</i>, <i>Because of</i>, <i>as a result</i>, <i>Therefore</i>, <i>so that</i>, <i>In order to</i>, <i>Consequently</i>.</li></ul>"
  "<div class='ex-title'>B. Organise your ideas / C. Useful language</div><p>Planning notes and phrase bank &ndash; not marked. Check the plan covers problem+causes, consequences, solutions+purposes and a final recommendation, and that phrases from C appear in Exercise E.</p>"
  "<div class='ex-title'>D&ndash;E. Writing task</div><p>Model band (strong response): a local environmental or urban problem explained with its causes, consequences and possible solutions; at least four target linkers used accurately (reason + purpose + result), with correct form and punctuation; a clear final recommendation; 180&ndash;220 words; logically organised.</p>"
  "<div class='ex-title'>F. Self-check</div><p>Students tick each box; spot-check &ldquo;at least four target linkers&rdquo; and that causes <i>and</i> consequences are both explained.</p>"
 ),
 "teacher_tip": "Before drafting, students choose one linker for each function (one reason, one purpose, one result) and one extra, and mark where each will go in the plan. This guarantees the range the task asks for.",
 "mistakes": [
  ["Because of the air quality has got worse, more children have asthma.", "Because the air quality has got worse, more children have asthma. / Because of the worse air quality, more children have asthma."],
  ["The city built cycle lanes for reduce traffic.", "The city built cycle lanes in order to reduce traffic."],
  ["Owing the emissions, the air is polluted.", "Owing to the emissions, the air is polluted."],
  ["Pollution rose, therefore of people got ill.", "Pollution rose; therefore, people got ill."]
 ],
 "activity_title": "Problem to Plan (8 min)",
 "activity_body": "Give a local problem (noise, litter, traffic). In pairs, students say one cause (because of&hellip;), one solution + purpose (in order to&hellip;) and one result (therefore&hellip;), then read their three sentences to another pair.",
 "materials": MAT_W,
 "lesson_title": LT,
 "learning_objective": "Students will be able to plan and write a 180&ndash;220-word paragraph about a local problem, explaining causes, consequences and solutions with accurate reason, purpose and result linkers, and giving a clear recommendation.",
 "success_criteria": "I can explain causes with <i>because of / due to / owing to</i> + noun. I can explain purposes with <i>so that / in order to</i>. I can explain results with <i>therefore / consequently / as a result</i>. I can end with a clear recommendation in 180&ndash;220 words.",
 "prior_knowledge": "The seven linkers, their functions and forms; paragraph structure and how to make a recommendation.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: name a local problem and list two causes on the board. Part 2: for one cause, add a consequence with <i>as a result</i> and a solution with <i>in order to</i>."],
  ["8 min", "Presentation (I Do)", "Read the model. Show the function of each linker with the reason: <b>Owing to / Because of</b> this &ndash; reason, + noun; <b>as a result / Therefore / Consequently</b> &ndash; the effects that follow, + clause; <b>so that / In order to</b> &ndash; the purpose of each solution. Point out how the paragraph moves problem &rarr; causes &rarr; consequences &rarr; solutions &rarr; recommendation, and that each linker takes a noun or a clause accordingly."],
  ["10 min", "Guided Practice (We Do)", "As a class, answer Exercise A questions 1&ndash;3 in note form, then plan a shared paragraph on &ldquo;traffic in our area&rdquo; using the Exercise B boxes."],
  ["10 min", "Independent Practice (You Do)", "Students complete their Exercise B plan and draft the paragraph (Exercise E), 180&ndash;220 words, with at least four target linkers and a recommendation."],
  ["7 min", "Assessment", "Students run the Exercise F self-check, then a partner labels each linker R (reason), P (purpose) or Res (result) and checks the form after it."],
  ["5 min", "Closure", "Two students read their recommendation sentence; the class checks it follows from the causes and effects given."]
 ],
 "followup": "Homework: redraft after feedback, then add one sentence using <i>the reason&hellip; is that&hellip;</i> and one using <i>with the aim of + -ing</i>.",
 "support": "Give a paragraph frame with the linkers and slots labelled (Problem&hellip; Because of&hellip; As a result&hellip; In order to&hellip; Therefore, I recommend&hellip;). Students fill the ideas.",
 "challenge": "Students add a short counter-point (a reason the problem is hard to solve) using <i>owing to</i> + noun, then still reach a recommendation.",
 "anticipated_problems": [
  ["Students use <i>because of / due to</i> before a clause (&ldquo;because of the air is dirty&rdquo;).", "Turn the clause into a noun phrase (&ldquo;because of the dirty air&rdquo;), or switch to plain <i>because</i> + clause."],
  ["Students use <i>for + to</i> or <i>for + -ing</i> for purpose (&ldquo;for to reduce traffic&rdquo;).", "Use <i>in order to</i> + base verb, or <i>so that</i> + subject + can/could."]
 ],
 "key_language": "<b>Grammar:</b> reason &ndash; because of / due to / owing to + noun; purpose &ndash; so that / in order to; result &ndash; therefore / consequently / as a result. <b>Structure:</b> problem &rarr; causes &rarr; consequences &rarr; solutions &rarr; recommendation. <br><b>Board:</b> due to the emissions &bull; in order to cut traffic &bull; As a result, air quality has fallen.",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;due to it is polluted&rdquo; &rarr; <i>due to the pollution / because it is polluted</i></li><li><span class='n'>2.</span> Fix: &ldquo;for reduce traffic&rdquo; &rarr; <i>in order to reduce traffic</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_cause_practice_b2.json",
 "ws_title": "Cause, Reason, Purpose and Result " + BUL + " Practice " + BUL + " B2",
 "info_rows": info("Practice", "Linking structures by function: connector choice, gap-fill, correction, rewriting, sorting", "A" + DASH + "G"),
 "answer_key_html": (
  "<div class='ex-title'>A. Choose the best connector</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> A &ndash; because of</div><div class='ans-item'><span class='n'>2.</span> B &ndash; in order to</div>"
  "<div class='ans-item'><span class='n'>3.</span> A &ndash; because of</div><div class='ans-item'><span class='n'>4.</span> B &ndash; consequently</div>"
  "<div class='ans-item'><span class='n'>5.</span> C &ndash; in order to</div><div class='ans-item'><span class='n'>6.</span> C &ndash; therefore</div>"
  "<div class='ans-item'><span class='n'>7.</span> B &ndash; because of</div><div class='ans-item'><span class='n'>8.</span> C &ndash; in order to</div></div>"
  "<div class='ex-title'>B. Complete the text &ndash; Life in a big city</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> Because of / Due to / Owing to</div><div class='ans-item'><span class='n'>2.</span> Therefore / Consequently / As a result</div>"
  "<div class='ans-item'><span class='n'>3.</span> in order to</div><div class='ans-item'><span class='n'>4.</span> so that</div>"
  "<div class='ans-item'><span class='n'>5.</span> Despite / In spite of *</div><div class='ans-item'><span class='n'>6.</span> because of / due to / owing to</div>"
  "<div class='ans-item'><span class='n'>7.</span> Therefore / Consequently / Ultimately</div></div>"
  "<p class='flag'>* Gap 5 (&ldquo;___ these improvements, many residents still choose to drive&rdquo;) needs a concession linker (despite / in spite of), which is outside this topic and not in a box &ndash; flagged for regeneration; accept <i>Despite / In spite of</i>.</p>"
  "<div class='ex-title'>C. Correct the mistakes</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> He was late <b>due to</b> the heavy traffic.</div>"
  "<div class='ans-item'><span class='n'>2.</span> They moved house <b>so that they could be</b> / <b>in order to be</b> closer to their school.</div>"
  "<div class='ans-item'><span class='n'>3.</span> The event was cancelled <b>because of</b> the bad organisation.</div>"
  "<div class='ans-item'><span class='n'>4.</span> We stayed at home <b>in order to</b> avoid the storm. (<i>too</i> &rarr; <i>to</i>)</div>"
  "<div class='ans-item'><span class='n'>5.</span> The roads were closed<b>;</b> therefore<b>,</b> many people worked from home.</div>"
  "<div class='ans-item'><span class='n'>6.</span> She studied hard <b>so that she could</b> get a better job.</div></div>"
  "<div class='ex-title'>D. Rewrite the sentence</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> The concert was cancelled due to a security risk.</div>"
  "<div class='ans-item'><span class='n'>2.</span> We left early so that we could avoid the rush-hour traffic.</div>"
  "<div class='ans-item'><span class='n'>3.</span> She's learning English in order to work abroad.</div>"
  "<div class='ans-item'><span class='n'>4.</span> Many people cycled to work owing to the disruption to the train service.</div>"
  "<div class='ans-item'><span class='n'>5.</span> The new policy will reduce pollution; therefore, the city will be a healthier place.</div>"
  "<div class='ans-item'><span class='n'>6.</span> They built a new park; consequently, people's well-being will improve.</div></div>"
  "<div class='ex-title'>E. Sort by function</div><div class='ans-grid-2'>"
  "<div class='ans-item'><b>Cause (reason):</b> 1, 5, 7</div>"
  "<div class='ans-item'><b>Purpose (intention):</b> 2, 4, 8</div>"
  "<div class='ans-item'><b>Result (consequence):</b> 3, 6</div><div class='ans-item'></div></div>"
  "<div class='ex-title'>F. Extended context challenge</div><p>Errors to find and correct: (1) owing <b>of</b> the increasing number &rarr; <b>owing to</b> &bull; (2) so that <b>to reduce</b> emissions &rarr; <b>so as to / in order to reduce</b> &bull; (3) <b>Therefore</b> the new rules &rarr; <b>Because of / Owing to / Due to</b> the new rules &bull; (4) in order <b>too it is cheaper</b> &rarr; <b>because it is cheaper</b> &bull; (5) because <b>to</b> these changes &rarr; <b>because of</b> these changes.</p>"
  "<div class='ex-title'>G. Personal response</div><p>Model: <b>1.</b> Rents here are high because of a housing shortage. <b>2.</b> I take notes in class in order to remember the key points. <b>3.</b> Our team practised every day; consequently, we won the league.</p>"
 ),
 "teacher_tip": "For every item, students say the function (reason / purpose / result) and then check the form after the gap (noun / clause / base verb). Exercise E is pure function sorting &ndash; a good quick check of understanding.",
 "mistakes": [
  ["He missed the train because of he woke up late.", "He missed the train because he woke up late."],
  ["She practises daily for to improve.", "She practises daily in order to improve."],
  ["Owing the rain, the game was postponed.", "Owing to the rain, the game was postponed."],
  ["Sales fell, therefore of the shop closed.", "Sales fell; therefore, the shop closed."]
 ],
 "activity_title": "Function Sort Relay (8 min)",
 "activity_body": "Put CAUSE / PURPOSE / RESULT in three corners. Read a phrase (&ldquo;due to the strike&rdquo;, &ldquo;so that everyone can hear&rdquo;, &ldquo;consequently prices rose&rdquo;). Students run to the right corner and say what form follows the linker.",
 "materials": MAT_G,
 "lesson_title": LT,
 "learning_objective": "Students will be able to choose, correct, rewrite and sort reason, purpose and result linkers across sentences and a text, matching each to its function and to the form that follows.",
 "success_criteria": "I can choose the linker that fits the function and the form. I can correct a wrong linker or form. I can rewrite a sentence with a given linker. I can sort linkers into cause, purpose and result.",
 "prior_knowledge": "The seven linkers, their functions and forms (from the Grammar worksheet).",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;because&rdquo; and &ldquo;because of&rdquo; and ask what follows each. Part 2: write &ldquo;so that&rdquo; and &ldquo;in order to&rdquo; and ask which needs a subject and modal."],
  ["8 min", "Presentation (I Do)", "Quick review: <b>reason</b> &ndash; because of / due to / owing to + noun (because + clause); <b>purpose</b> &ndash; in order to + base verb, so that + subject + can/could; <b>result</b> &ndash; therefore / consequently + clause (; &hellip; ,). Model Exercise C item 1 (<i>due of</i> &rarr; <i>due to</i>) and item 4 (<i>in order too</i> &rarr; <i>in order to</i>). Preview Exercise E: sort by function only."],
  ["10 min", "Guided Practice (We Do)", "Exercise A items 1&ndash;4 as a class (function + form), then Exercise B items 1&ndash;3 together."],
  ["12 min", "Independent Practice (You Do)", "Students complete the rest of Exercise B, Exercise C, Exercise D, Exercise E and Exercise F individually."],
  ["6 min", "Assessment", "Review Exercise E and Exercise F on the board; students name the function or the correction each time. Then the Exit Ticket."],
  ["4 min", "Closure", "In pairs, students read two Exercise D rewrites, checking the meaning matches the first sentence."]
 ],
 "followup": "Homework: write six sentences about a change in your school, using a reason, a purpose and a result linker twice each.",
 "support": "Give the CAUSE / PURPOSE / RESULT card with one linker and one form note each; students label every gap with the function before choosing.",
 "challenge": "Students rewrite three Exercise A items with a different linker of the same function, changing the form as needed.",
 "anticipated_problems": [
  ["Students choose a reason linker for an Exercise A item that needs purpose (or the reverse).", "Ask &ldquo;why did it happen?&rdquo; (reason) vs &ldquo;what for?&rdquo; (purpose) vs &ldquo;what happened next?&rdquo; (result) before looking at the options."],
  ["In Exercise F students miss &ldquo;in order too it is cheaper&rdquo; because the spelling error hides the structural one.", "Two checks: is <i>too</i> right here? and does <i>in order to</i> fit before a clause? (No &ndash; use <i>because</i>.)"]
 ],
 "key_language": "<b>Grammar:</b> reason &ndash; because of / due to / owing to + noun; purpose &ndash; in order to + verb, so that + clause; result &ndash; therefore / consequently + clause. <br><b>Board:</b> due to the strike &bull; in order to save time &bull; so that everyone can hear &bull; &hellip;; therefore, &hellip;",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Sort: &ldquo;so that we can reduce waste&rdquo; &rarr; <i>purpose</i></li><li><span class='n'>2.</span> Fix: &ldquo;because to the rain&rdquo; &rarr; <i>because of the rain</i></li></ul>"
})
w(TES[-1])

print("--- cause set done ---")

# =====================================================================
# 5. ADVANCED COMPARISON
# =====================================================================
TES.append({
 "_file": "te_comparison_grammar_b2.json",
 "ws_title": "Advanced Comparison " + BUL + " Grammar " + BUL + " B2",
 "info_rows": info("Grammar", "the more...the more, nowhere near as, considerably, slightly, by far", "6 (A" + DASH + "F)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Grammar overview</div><p>Reference table &ndash; no written answers. Check students can state each structure&rsquo;s use (linked change / big difference / degree of difference / clear choice or extreme / change over time).</p>"
  "<div class='ex-title'>B. Choose the best option</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> B &ndash; the more</div><div class='ans-item'><span class='n'>2.</span> A &ndash; fast</div>"
  "<div class='ans-item'><span class='n'>3.</span> B &ndash; more expensive</div><div class='ans-item'><span class='n'>4.</span> C &ndash; the better</div>"
  "<div class='ans-item'><span class='n'>5.</span> A &ndash; slightly (B/C also grammatical)</div><div class='ans-item'><span class='n'>6.</span> A &ndash; wider</div>"
  "<div class='ans-item'><span class='n'>7.</span> B &ndash; considerably (accept A)</div><div class='ans-item'><span class='n'>8.</span> A &ndash; convenient</div></div>"
  "<div class='ex-title'>C. Complete the sentences (use the words in the box)</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> the more</div><div class='ans-item'><span class='n'>2.</span> nowhere near as</div>"
  "<div class='ans-item'><span class='n'>3.</span> considerably</div><div class='ans-item'><span class='n'>4.</span> much</div>"
  "<div class='ans-item'><span class='n'>5.</span> by far</div><div class='ans-item'><span class='n'>6.</span> slightly</div>"
  "<div class='ans-item'><span class='n'>7.</span> increasingly</div><div class='ans-item'><span class='n'>8.</span> a little</div></div>"
  "<div class='ex-title'>D. Rewrite / combine</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> The more I study, the more I understand the subject.</div>"
  "<div class='ans-item'><span class='n'>2.</span> This hotel is nowhere near as modern as the one in the city centre.</div>"
  "<div class='ans-item'><span class='n'>3.</span> The new system is considerably cheaper than the old one.</div>"
  "<div class='ans-item'><span class='n'>4.</span> It's slightly more difficult than I expected.</div>"
  "<div class='ans-item'><span class='n'>5.</span> London is by far the best city for job opportunities.</div>"
  "<div class='ans-item'><span class='n'>6.</span> Taking the bus is by far the better option than driving.</div></div>"
  "<div class='ex-title'>E. Correct the mistakes</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> the <b>more</b> confident you will be (<i>the most</i> &rarr; <i>the more</i>)</div>"
  "<div class='ans-item'><span class='n'>2.</span> nowhere near as <b>cheap</b> as (base adjective after as&hellip;as)</div>"
  "<div class='ans-item'><span class='n'>3.</span> <b>much / far</b> more experienced (not <i>very more</i>)</div>"
  "<div class='ans-item'><span class='n'>4.</span> by far <b>the</b> better solution (by far needs <i>the</i>)</div>"
  "<div class='ans-item'><span class='n'>5.</span> becoming <b>increasingly</b> popular (adverb)</div>"
  "<div class='ans-item'><span class='n'>6.</span> a little <b>more</b> convenient (comparative needed)</div></div>"
  "<div class='ex-title'>F. Short production</div><p>Model: <b>1.</b> The more you read, the wider your vocabulary becomes. <b>2.</b> This route is nowhere near as fast as the motorway. <b>3.</b> Public transport is by far the cheapest way to travel here.</p>"
 ),
 "teacher_tip": "Two frequent slips: after <i>nowhere near as &hellip; as</i> use the plain adjective (as <b>cheap</b> as), not a comparative; and <i>by far</i> is followed by <i>the</i> + superlative or <i>the</i> + better/worse/more effective option. Drill both before Exercise E.",
 "mistakes": [
  ["This car is nowhere near as faster as that one.", "This car is nowhere near as fast as that one."],
  ["The exam was very more difficult than last year's.", "The exam was much more difficult than last year's."],
  ["It is by far better choice for beginners.", "It is by far the better choice for beginners."],
  ["The more you sleep the better you will feel it.", "The more you sleep, the better you will feel."]
 ],
 "activity_title": "Turn Up the Degree (8 min)",
 "activity_body": "Give a plain comparison (&ldquo;A is bigger than B&rdquo;). Students say it three ways: a small difference (slightly / a little bigger), a big difference (considerably / far bigger; or &ldquo;B is nowhere near as big as A&rdquo;), and a clear choice (A is by far the bigger option).",
 "materials": MAT_G,
 "lesson_title": LT,
 "learning_objective": "Students will be able to use advanced comparison structures &ndash; the more&hellip;the more, nowhere near as&hellip;as, considerably/slightly/far/a little + comparative, by far + the superlative, and increasingly &ndash; accurately.",
 "success_criteria": "I can link two changes with <i>the more&hellip;, the more&hellip;</i>. I can use <i>nowhere near as + adjective + as</i> for a big difference. I can put a modifier (slightly, considerably, far) before a comparative, and <i>by far</i> before <i>the</i> + superlative.",
 "prior_knowledge": "Regular comparatives and superlatives (-er/-est, more/most); the difference between an adjective and an adverb.",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;The more you practise&hellip;&rdquo; and ask students to finish it, then show the pattern <i>the</i> + comparative, <i>the</i> + comparative. Part 2: write &ldquo;A is not as fast as B&rdquo; and ask how to say the gap is <i>huge</i> (nowhere near as fast as)."],
  ["8 min", "Presentation (I Do)", "Explain each structure with the &ldquo;why&rdquo;. <b>the more&hellip;, the more&hellip;</b> &ndash; shows one thing changing <i>because</i> another changes; both halves use <i>the</i> + a comparative, and there is a comma between them. <b>nowhere near as + adjective + as</b> &ndash; emphasises a <i>big</i> difference (much less); the adjective stays in its base form because <i>as&hellip;as</i> already does the comparing. <b>considerably / far / much / slightly / a little + comparative</b> &ndash; these say <i>how big</i> the difference is; they go directly before the comparative (&ldquo;considerably more flexible&rdquo;). <b>by far + the superlative</b> (or <i>the</i> + better / worse / more effective option) &ndash; marks something as the clear extreme or choice; <i>the</i> is required. <b>increasingly + adjective/adverb</b> &ndash; a growing degree over time. Model Exercise E item 2 (<i>as cheaper as</i> &rarr; <i>as cheap as</i>) and item 4 (<i>by far better</i> &rarr; <i>by far the better</i>)."],
  ["10 min", "Guided Practice (We Do)", "Exercise B items 1&ndash;4 as a class, naming the structure each time; then Exercise C items 1&ndash;3 together."],
  ["10 min", "Independent Practice (You Do)", "Students complete the rest of Exercise C, Exercise D and Exercise E individually, then compare Exercise D in pairs, checking the comma in item 1."],
  ["7 min", "Assessment", "Review Exercise E on the board; students name the structure and the error type. Then the Exit Ticket."],
  ["5 min", "Closure", "Students write one Exercise F sentence with <i>by far</i> and read it; the class checks for <i>the</i> + superlative."]
 ],
 "followup": "Homework: write six sentences comparing two cities, using each advanced structure at least once across the set.",
 "support": "Give a card with one model sentence per structure. Students match each Exercise B/C item to a model before choosing.",
 "challenge": "Students rewrite three Exercise C sentences using a different advanced structure with the same meaning (e.g. &ldquo;considerably more expensive&rdquo; &rarr; &ldquo;nowhere near as cheap&rdquo;).",
 "anticipated_problems": [
  ["Students use a comparative after <i>as&hellip;as</i> (&ldquo;as cheaper as&rdquo;, &ldquo;nowhere near as faster as&rdquo;).", "The frame <i>as + adjective + as</i> already compares &ndash; keep the adjective in its base form."],
  ["Students drop <i>the</i> after <i>by far</i> (&ldquo;by far better solution&rdquo;) or the comma in <i>the more&hellip;, the more&hellip;</i>.", "Fixed patterns on the board: <i>by far <b>the</b> best / the better option</i>; <i>The + comparative<b>,</b> the + comparative</i>."]
 ],
 "key_language": "<b>Grammar:</b> the more&hellip;, the more&hellip;; nowhere near as + adj + as; slightly / considerably / far + comparative; by far + the superlative; increasingly + adj. <br><b>Board:</b> The more you read, the wider your vocabulary. &bull; nowhere near as reliable as &bull; by far the most popular",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;nowhere near as bigger as&rdquo; &rarr; <i>nowhere near as big as</i></li><li><span class='n'>2.</span> Fix: &ldquo;by far better option&rdquo; &rarr; <i>by far the better option</i></li></ul>"
})
w(TES[-1])

print("--- comparison grammar done ---")

TES.append({
 "_file": "te_comparison_reading_b2.json",
 "ws_title": "Advanced Comparison " + BUL + " Reading " + BUL + " B2",
 "info_rows": info("Reading", "Comparing education systems; advanced comparative structures in context", "A" + DASH + "F (comprehension, language, summary)"),
 "answer_key_html": (
  "<div class='ex-title'>A. Before you read</div><p>Discussion &ndash; answers vary. Push for a ranked, justified answer.</p>"
  "<div class='ex-title'>C. Reading comprehension</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> B</div><div class='ans-item'><span class='n'>2.</span> C</div>"
  "<div class='ans-item'><span class='n'>3.</span> C</div><div class='ans-item'><span class='n'>4.</span> B</div>"
  "<div class='ans-item'><span class='n'>5.</span> The text names adaptability, creativity and collaboration as &ldquo;by far the most important&rdquo; skills today.</div>"
  "<div class='ans-item'><span class='n'>6.</span> Because each approach has strengths and weaknesses &ndash; exam focus raises results but can limit creativity and raise stress; flexible systems build thinking skills but offer less structure.</div></div>"
  "<div class='ex-title'>D. Language in context &ndash; find the exact words</div><ul class='ans'>"
  "<li><span class='n'>1.</span> &ldquo;The more control students have&hellip;, the more motivated they tend to become, and the more developed their critical thinking skills are.&rdquo;</li>"
  "<li><span class='n'>2.</span> &ldquo;&hellip;nowhere near as much time for extracurricular activities as those in more flexible systems.&rdquo;</li>"
  "<li><span class='n'>3.</span> &ldquo;&hellip;typically score considerably more highly in international tests&hellip;&rdquo;</li>"
  "<li><span class='n'>4.</span> &ldquo;&hellip;gives students slightly less freedom than in the most flexible systems.&rdquo;</li>"
  "<li><span class='n'>5.</span> &ldquo;&hellip;qualities that are by far the most important in today&rsquo;s rapidly changing world.&rdquo;</li>"
  "<li><span class='n'>6.</span> &ldquo;&hellip;education is increasingly a global conversation.&rdquo;</li></ul>"
  "<div class='ex-title'>E. Complete the summary</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> independence (control / freedom)</div><div class='ans-item'><span class='n'>2.</span> structured (disciplined)</div>"
  "<div class='ans-item'><span class='n'>3.</span> considerably</div><div class='ans-item'><span class='n'>4.</span> nowhere near</div>"
  "<div class='ans-item'><span class='n'>5.</span> increasing</div><div class='ans-item'><span class='n'>6.</span> increasingly</div></div>"
  "<div class='ex-title'>F. Reflection</div><p>Short paragraph (80&ndash;120 words) &ndash; check at least one comparative structure from the text is used accurately.</p>"
 ),
 "teacher_tip": "Exercise D doubles as a grammar review: the meaning/function is already given, so students just have to locate the exact words &ndash; a good check that they can spot each structure in real text, not only in isolated sentences.",
 "mistakes": [
  ["Students in exam-focused systems have nowhere near much time for hobbies.", "Students in exam-focused systems have nowhere near as much time for hobbies."],
  ["This system scores more considerably highly in tests.", "This system scores considerably more highly in tests."],
  ["Adaptability is by far most important skill today.", "Adaptability is by far the most important skill today."],
  ["Education is becoming increase global.", "Education is becoming increasingly global."]
 ],
 "activity_title": "Find It Fast (8 min)",
 "activity_body": "Call out a function (&ldquo;a big difference&rdquo;, &ldquo;a small difference&rdquo;, &ldquo;a growing trend&rdquo;, &ldquo;the clear choice&rdquo;, &ldquo;linked change&rdquo;). Students race to find and read out the matching sentence from the text.",
 "materials": MAT_R,
 "lesson_title": LT,
 "learning_objective": "Students will be able to read a comparative text for gist and detail and locate how advanced comparative structures are used to show difference, degree and change over time.",
 "success_criteria": "I can find the main comparison the text makes between education systems. I can locate the exact words for each comparative structure. I can complete a summary with a suitable comparative word.",
 "prior_knowledge": "The advanced comparison structures and their functions (from the Grammar worksheet).",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: ask &ldquo;What are the most important goals of education?&rdquo; and list two or three. Part 2: compare two schools students know using one comparative structure each."],
  ["8 min", "Presentation (I Do)", "Recap each structure&rsquo;s function with an example from the text: <i>the more&hellip;the more</i> (linked change), <i>nowhere near as&hellip;as</i> (big difference), <i>considerably / slightly</i> + comparative (degree of difference), <i>by far</i> + superlative (clear choice), <i>increasingly</i> (growing trend). Read paragraph 1 aloud and find the first structure together."],
  ["10 min", "Guided Practice (We Do)", "Students read once for gist, then do Exercise C items 1&ndash;3 as a class, pointing to the proof sentence."],
  ["10 min", "Independent Practice (You Do)", "Students complete Exercise C 4&ndash;6, Exercise D and Exercise E individually; compare Exercise D in pairs."],
  ["7 min", "Assessment", "Review Exercise E; for each gap a student names the structure&rsquo;s function. Then the Exit Ticket."],
  ["5 min", "Closure", "Two students share their Exercise F sentence; the class checks the comparative structure is accurate."]
 ],
 "followup": "Homework: compare two subjects you study, using at least three different comparative structures from the text.",
 "support": "Give the Exercise D table with the first word of each quote already filled in as a starting point.",
 "challenge": "Students summarise the text in three sentences, each using a different comparative structure, without copying the original wording.",
 "anticipated_problems": [
  ["Students quote a sentence with the wrong structure for the function asked.", "Have them check the exact words match the pattern named (e.g. <i>the more&hellip;, the more&hellip;</i> needs two <i>the more</i> clauses, not one)."],
  ["Students use <i>considerably</i> and <i>slightly</i> interchangeably in Exercise E.", "Reread the sentence: does it describe a big change (considerably) or a small one (slightly / nowhere near)?"]
 ],
 "key_language": "<b>Grammar:</b> the more&hellip;the more (linked change); nowhere near as + adj + as (big difference); considerably/slightly + comparative (degree); by far + superlative (clear choice); increasingly (growing trend). <br><b>Board:</b> nowhere near as much time &bull; considerably more highly &bull; by far the most important",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Which shows a growing trend? &rarr; <i>increasingly</i></li><li><span class='n'>2.</span> Which shows the clear choice? &rarr; <i>by far</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_comparison_writing_b2.json",
 "ws_title": "Advanced Comparison " + BUL + " Writing " + BUL + " B2",
 "info_rows": info("Writing", "Make detailed comparisons using advanced comparative structures and modifiers", "A" + DASH + "G (model, plan, 180" + DASH + "220-word paragraph)"),
 "answer_key_html": (
  "<div class='ex-title'>B. Understand the model</div><ul class='ans'>"
  "<li><span class='n'>1.</span> Online learning is &ldquo;by far the more flexible option, allowing students to study whenever and wherever they want&rdquo; (also: more control over your schedule).</li>"
  "<li><span class='n'>2.</span> It is &ldquo;nowhere near as expensive as traditional classroom learning&rdquo; &ndash; much cheaper.</li>"
  "<li><span class='n'>3.</span> Classroom learning is &ldquo;considerably more interactive&rdquo;: you can ask questions immediately, meet people with similar interests, feel part of a community, and it suits subjects that need hands-on practice.</li>"
  "<li><span class='n'>4.</span> There is no single best option &ndash; &ldquo;the best option depends on your goals, learning style and personal circumstances&rdquo;, a balanced conclusion.</li></ul>"
  "<div class='ex-title'>C. Useful language / D. Organise your ideas</div><p>Phrase bank and planning notes &ndash; not marked. Check the plan names two clear subjects to compare and lists similarities/differences for each.</p>"
  "<div class='ex-title'>E&ndash;G. Writing task</div><p>Model band (strong response): two subjects compared in detail; a range of comparative structures used accurately (the more&hellip;the more, nowhere near as, considerably/slightly, by far, increasingly); reasons and examples for each point; a clear, balanced final judgement; 180&ndash;220 words; well organised.</p>"
  "<div class='ex-title'>F. Self-check</div><p>Students tick each box; spot-check &ldquo;a range of comparison structures&rdquo; and &ldquo;a clear final judgement&rdquo;.</p>"
 ),
 "teacher_tip": "Have students underline every comparative structure in the model before they plan &ndash; five different ones in one short paragraph shows how much range is expected in Exercise G.",
 "mistakes": [
  ["Online learning is by far more flexible option.", "Online learning is by far the more flexible option."],
  ["It is nowhere near expensive as classroom learning.", "It is nowhere near as expensive as classroom learning."],
  ["Classroom learning is considerable more interactive.", "Classroom learning is considerably more interactive."],
  ["The best option depend on your goals.", "The best option depends on your goals."]
 ],
 "activity_title": "Two Options (8 min)",
 "activity_body": "Give a pair (bus vs car, book vs film). In pairs, students produce one sentence with <i>nowhere near as&hellip;as</i>, one with <i>considerably/slightly</i>, and one with <i>by far</i>, comparing the two.",
 "materials": MAT_W,
 "lesson_title": LT,
 "learning_objective": "Students will be able to plan and write a 180&ndash;220-word paragraph comparing two subjects in detail, using a range of advanced comparative structures accurately and reaching a balanced judgement.",
 "success_criteria": "I can use nowhere near as&hellip;as, considerably/slightly + comparative, by far + superlative and increasingly accurately. I can support each comparison with a reason or example. I can give a clear, balanced final judgement in 180&ndash;220 words.",
 "prior_knowledge": "The advanced comparison structures and their functions (from the Grammar worksheet).",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: ask students to compare two ways of getting to school in one sentence. Part 2: upgrade it with a modifier (considerably / slightly / by far)."],
  ["8 min", "Presentation (I Do)", "Read the model. Point out each structure and why it was chosen: <i>by far</i> for the clearest advantage of online learning; <i>nowhere near as&hellip;as</i> for the big price gap; <i>considerably</i> for classroom learning&rsquo;s interactivity; and how the writer balances both before concluding with &ldquo;depends on&hellip;&rdquo;. Show that every comparison in the model has a reason or example attached."],
  ["10 min", "Guided Practice (We Do)", "As a class, answer Exercise B questions 1&ndash;2 in full sentences, then plan a shared paragraph on &ldquo;two forms of transport&rdquo; using the Exercise D boxes."],
  ["10 min", "Independent Practice (You Do)", "Students choose a pair from Exercise E, complete their Exercise D plan and draft the paragraph, 180&ndash;220 words, with a range of structures and a balanced conclusion."],
  ["7 min", "Assessment", "Students run the Exercise F self-check, then a partner circles every comparative structure and checks it is supported with a reason."],
  ["5 min", "Closure", "Two students read their final judgement sentence; the class checks it is balanced, not one-sided."]
 ],
 "followup": "Homework: redraft after feedback, then write two more sentences comparing a third option to one you already used.",
 "support": "Give a paragraph frame with the structures and slots labelled (X is by far&hellip; / X is nowhere near as&hellip;as Y / Overall, it depends on&hellip;). Students fill the ideas.",
 "challenge": "Students add one sentence using &ldquo;the more&hellip;, the more&hellip;&rdquo; linking a factor to an outcome for one of their two subjects.",
 "anticipated_problems": [
  ["Students write one-sided comparisons with no balance (&ldquo;X is better than Y in every way&rdquo;).", "Require at least one advantage for each subject before the final judgement, as the model does."],
  ["Students drop <i>the</i> after <i>by far</i> or <i>as</i> after <i>nowhere near</i>.", "Fixed patterns: <i>by far <b>the</b> more/most&hellip;</i>; <i>nowhere near <b>as</b> + adjective + as</i>."]
 ],
 "key_language": "<b>Grammar:</b> by far + the + comparative/superlative; nowhere near as + adj + as; considerably/slightly + comparative; increasingly + adj. <br><b>Board:</b> by far the more flexible option &bull; nowhere near as expensive as &bull; considerably more interactive",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;nowhere near expensive as&rdquo; &rarr; <i>nowhere near as expensive as</i></li><li><span class='n'>2.</span> Fix: &ldquo;by far more flexible option&rdquo; &rarr; <i>by far the more flexible option</i></li></ul>"
})
w(TES[-1])

TES.append({
 "_file": "te_comparison_practice_b2.json",
 "ws_title": "Advanced Comparison " + BUL + " Practice " + BUL + " B2",
 "info_rows": info("Practice", "Comparative structures and modifiers: option choice, gap-fill, correction, rewriting, sorting", "A" + DASH + "F"),
 "answer_key_html": (
  "<div class='ex-title'>A. Choose the best option</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> A &ndash; confident</div><div class='ans-item'><span class='n'>2.</span> A &ndash; expensive</div>"
  "<div class='ans-item'><span class='n'>3.</span> B &ndash; more popular</div><div class='ans-item'><span class='n'>4.</span> A &ndash; lighter</div>"
  "<div class='ans-item'><span class='n'>5.</span> C &ndash; best</div><div class='ans-item'><span class='n'>6.</span> A &ndash; challenging</div>"
  "<div class='ans-item'><span class='n'>7.</span> A &ndash; easy</div><div class='ans-item'><span class='n'>8.</span> B &ndash; cleaner</div></div>"
  "<div class='ex-title'>B. Complete the text (use each expression once)</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> much</div><div class='ans-item'><span class='n'>2.</span> nowhere near</div>"
  "<div class='ans-item'><span class='n'>3.</span> the more</div><div class='ans-item'><span class='n'>4.</span> the more</div>"
  "<div class='ans-item'><span class='n'>5.</span> considerably</div><div class='ans-item'><span class='n'>6.</span> slightly</div>"
  "<div class='ans-item'><span class='n'>7.</span> by far</div><div class='ans-item'></div></div>"
  "<div class='ex-title'>C. Rewrite the sentence</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> The more I travel, the more open-minded I feel.</div>"
  "<div class='ans-item'><span class='n'>2.</span> This option is nowhere near as good as the other one.</div>"
  "<div class='ans-item'><span class='n'>3.</span> The new school is considerably bigger than the old one.</div>"
  "<div class='ans-item'><span class='n'>4.</span> Living in the suburbs is slightly cheaper than in the city centre.</div>"
  "<div class='ans-item'><span class='n'>5.</span> She is by far the most experienced teacher in the department.</div>"
  "<div class='ans-item'><span class='n'>6.</span> The city is becoming increasingly polluted each year.</div></div>"
  "<div class='ex-title'>D. Correct the mistakes</div><div class='ans-grid-2'>"
  "<div class='ans-item'><span class='n'>1.</span> the <b>more</b> confident you will be</div>"
  "<div class='ans-item'><span class='n'>2.</span> nowhere near <b>as comfortable as</b> (word order)</div>"
  "<div class='ans-item'><span class='n'>3.</span> <b>considerably</b> more flexible</div>"
  "<div class='ans-item'><span class='n'>4.</span> slightly <b>cheaper</b> (not <i>more cheapest</i>)</div>"
  "<div class='ans-item'><span class='n'>5.</span> by far <b>better</b> at solving problems</div>"
  "<div class='ans-item'><span class='n'>6.</span> becoming <b>increasingly</b> crowded (drop &ldquo;more and more&rdquo;)</div></div>"
  "<div class='ex-title'>E. Sort by function</div><div class='ans-grid-2'>"
  "<div class='ans-item'><b>A</b> big difference: 2, 3</div><div class='ans-item'><b>B</b> small difference: 4</div>"
  "<div class='ans-item'><b>C</b> strongest option: 5</div><div class='ans-item'><b>D</b> growing change: 6</div>"
  "<div class='ans-item'><b>E</b> links two changes: 1</div><div class='ans-item'></div></div>"
  "<div class='ex-title'>F. Personal response</div><p>Model: <b>1.</b> The more I revise, the more confident I feel about the exam. <b>2.</b> This app is nowhere near as fast as the last one. <b>3.</b> Cycling to work is by far the healthiest option.</p>"
 ),
 "teacher_tip": "In Exercise B remind students the expressions are used <i>once each</i> &ndash; if they use one twice, another gap will be impossible. Encourage them to fill the &ldquo;forced&rdquo; gaps first (nowhere near as&hellip;as, the more&hellip;the more, by far the) before the flexible ones.",
 "mistakes": [
  ["This laptop is nowhere near as fastest as mine.", "This laptop is nowhere near as fast as mine."],
  ["She is by far good student in the class.", "She is by far the best student in the class."],
  ["The more you wait the worse it gets it.", "The more you wait, the worse it gets."],
  ["Prices are becoming increase high.", "Prices are becoming increasingly high."]
 ],
 "activity_title": "Category Cards (8 min)",
 "activity_body": "Give each pair five cards (the more&hellip;the more / nowhere near as / considerably / slightly / by far / increasingly). Read a sentence missing its modifier; pairs race to hold up the matching card and complete the sentence aloud.",
 "materials": MAT_G,
 "lesson_title": LT,
 "learning_objective": "Students will be able to choose, correct, rewrite and sort advanced comparative structures across sentences and a text, matching form and function.",
 "success_criteria": "I can choose the correct form after each comparative structure. I can find and fix a form or word-order error. I can rewrite a sentence with a given structure and sort structures by function.",
 "prior_knowledge": "The five advanced comparison structures and their functions (from the Grammar worksheet).",
 "lesson_rows": [
  ["5 min", "Warm-Up", "Part 1: write &ldquo;nowhere near as good as&rdquo; and ask what form follows (base adjective). Part 2: write &ldquo;by far ___ best&rdquo; and elicit <i>the</i>."],
  ["8 min", "Presentation (I Do)", "Quick review with the &ldquo;why&rdquo;: <i>the more&hellip;, the more&hellip;</i> links two changes (comma, comparative in both halves); <i>nowhere near as + adj + as</i> keeps the base adjective; <i>considerably/slightly/much/a little</i> sit directly before a comparative; <i>by far</i> needs <i>the</i> + superlative or <i>the</i> + better/worse. Model Exercise D items 1 and 2."],
  ["10 min", "Guided Practice (We Do)", "Exercise A items 1&ndash;4 as a class, then start Exercise B together (forced gaps first)."],
  ["12 min", "Independent Practice (You Do)", "Students complete the rest of Exercise B, Exercise C, Exercise D and Exercise E individually."],
  ["6 min", "Assessment", "Review Exercise D on the board; students name the fix. Then the Exit Ticket."],
  ["4 min", "Closure", "In pairs, students check two Exercise C rewrites keep the original meaning."]
 ],
 "followup": "Homework: write six sentences comparing your school now with five years ago, using each structure once.",
 "support": "Give a card with one correct model sentence per structure; students match each item to a model before answering.",
 "challenge": "Students rewrite three Exercise A sentences using a different structure with the same overall meaning.",
 "anticipated_problems": [
  ["Students use a comparative after <i>as&hellip;as</i> (Exercise A items 1, 2, 7, 8).", "The base adjective goes in <i>as&hellip;as</i>; the comparing is already done by <i>as&hellip;as</i> itself."],
  ["In Exercise B students use an expression twice and get stuck on a later gap.", "Cross off each expression in the box as it is used &ndash; there are exactly enough for one gap each."]
 ],
 "key_language": "<b>Grammar:</b> the more&hellip;, the more&hellip;; nowhere near as + adj + as; considerably/slightly/much + comparative; by far + the + superlative/better/worse; increasingly + adj. <br><b>Board:</b> nowhere near as good as &bull; considerably bigger &bull; by far the best",
 "exit_ticket": "<ul class='ans'><li><span class='n'>1.</span> Fix: &ldquo;nowhere near as bigger as&rdquo; &rarr; <i>nowhere near as big as</i></li><li><span class='n'>2.</span> Fix: &ldquo;by far good option&rdquo; &rarr; <i>by far the best option</i></li></ul>"
})
w(TES[-1])

print("--- comparison set done ---")
