// Grammar-topic map shared by worksheet-page.js (breadcrumb + "teaching guide"
// link on every worksheet) and topic-page.js (the /worksheets/topics/<slug>/
// hubs). One list so a worksheet, its guide and its hub can never disagree.
//
// Matching runs on `title + topic_key` (dashes → spaces). ORDER MATTERS: first
// match wins, so the specific patterns sit above the generic ones — "Third
// Conditional: If + Past Perfect" must land on conditionals, not past perfect;
// "Present Continuous for Future Arrangements" on future forms, not present
// continuous. Verified against all 809 titles (27/09/2026) — re-check with a
// dry run before adding a pattern, a loose regex silently mislinks dozens.
//
// `hub` is only set for topics with enough worksheets across levels to make a
// page worth indexing (~10+). Thin hubs are worse than none.

const TOPICS = [
  {
    re: /present perfect|\bever\b.*\bnever\b|already.{0,10}yet/i,
    guide: { slug: 'how-to-teach-present-perfect', label: 'How to Teach the Present Perfect' },
    hub: {
      slug: 'present-perfect', name: 'Present Perfect',
      desc: 'Free present perfect worksheets: ever/never, just/already/yet, for/since, present perfect vs. past simple and present perfect continuous, A2–B1.',
      intro: 'The present perfect is where learners first meet a tense that links past and present, so it needs more practice than any tense before it. These worksheets build it in the order it is usually taught: life experiences with <em>ever</em> and <em>never</em>, recent news with <em>just</em>, <em>already</em> and <em>yet</em>, duration with <em>for</em> and <em>since</em>, and finally the contrast with the past simple and the continuous form. Each step has grammar, reading, writing and practice sheets, so you can stay on one use until it sticks.',
    },
  },
  {
    re: /conditional|\bwish\b|if only/i,
    guide: { slug: 'how-to-teach-conditionals', label: 'How to Teach Conditionals' },
    hub: {
      slug: 'conditionals', name: 'Conditionals',
      desc: 'Free conditionals worksheets: zero, first, second and third conditional, mixed conditionals and wish / if only, from A2 to B2, with reading and writing.',
      intro: 'Conditionals are easiest to teach one at a time and only then side by side. Start with the zero and first conditional at A2 (real facts and likely results), move to the second conditional at B1 (unreal present), and leave the third conditional, mixed conditionals and <em>wish / if only</em> for B2, when learners can handle past hypotheticals. Every stage has its own grammar, reading, writing and practice sheet, plus comparison worksheets for the pairs students confuse most.',
    },
  },
  {
    re: /past perfect/i,
    guide: { slug: 'how-to-teach-past-perfect', label: 'How to Teach the Past Perfect' },
    hub: null,
  },
  {
    re: /report(ed|ing) (speech|questions|commands|verbs)|indirect speech/i,
    guide: { slug: 'how-to-teach-reported-speech', label: 'How to Teach Reported Speech' },
    hub: {
      slug: 'reported-speech', name: 'Reported Speech',
      desc: 'Free reported speech worksheets: tense backshift, reported questions and commands, reporting verbs and all tenses and modals, B1–B2, with practice.',
      intro: 'Reported speech has three moving parts: the tense backshift, the pronoun and time-word changes, and the reporting verb. These worksheets separate them. B1 sheets cover statements with present-to-past backshift, then reported questions and commands; B2 sheets add every tense and modal and the full range of reporting verbs (<em>suggest</em>, <em>deny</em>, <em>warn</em>…). Use the grammar sheet to present, the reading to notice the pattern in context and the writing sheet to produce it.',
    },
  },
  {
    re: /passive/i,
    guide: { slug: 'how-to-teach-passive-voice', label: 'How to Teach the Passive Voice' },
    hub: {
      slug: 'passive-voice', name: 'Passive Voice',
      desc: 'Free passive voice worksheets: present and past simple passive, future, modals, infinitives and gerunds, all tenses and the reporting passive, B1–B2.',
      intro: 'Learners understand the passive quickly; what takes time is forming it in every tense. These worksheets go tense by tense — present simple, past simple, future, <em>be going to</em>, modals, infinitives and gerunds — before the all-tenses review. At B2 they move on to advanced structures and the reporting passive (<em>It is said that…</em>, <em>He is believed to…</em>), the form students meet in news and academic texts.',
    },
  },
  {
    re: /\bused to\b/i,
    guide: { slug: 'how-to-teach-used-to', label: 'How to Teach Used To' },
    hub: null,
  },
  {
    re: /phrasal/i,
    guide: { slug: 'how-to-teach-phrasal-verbs', label: 'How to Teach Phrasal Verbs' },
    hub: null,
  },
  {
    re: /linking words|connectors/i,
    guide: { slug: 'how-to-teach-linking-words', label: 'How to Teach Linking Words' },
    hub: null,
  },
  {
    re: /comparative|superlative/i,
    guide: { slug: 'how-to-teach-comparatives-superlatives', label: 'How to Teach Comparatives & Superlatives' },
    hub: {
      slug: 'comparatives-superlatives', name: 'Comparatives & Superlatives',
      desc: 'Free comparative and superlative adjective worksheets: -er/-est and more/most, spelling rules, irregular forms and as…as equality structures, A1–B1.',
      intro: 'Comparatives and superlatives are best taught as two separate lessons before they are mixed. The A1 sheets introduce each form on its own with the spelling rules (<em>big → bigger</em>, <em>happy → happiest</em>) and the irregulars; A2 brings them together in review and practice; B1 adds equality and modifiers (<em>as tall as</em>, <em>much bigger</em>, <em>not nearly as…</em>). Reading and writing sheets give students real things to compare instead of isolated sentences.',
    },
  },
  {
    re: /modal|\bcan\b|can't|\bcould\b|\bmust\b|have to|should|\bmight\b/i,
    guide: { slug: 'how-to-teach-modal-verbs', label: 'How to Teach Modal Verbs' },
    hub: {
      slug: 'modal-verbs', name: 'Modal Verbs',
      desc: 'Free modal verbs worksheets: can/could, must/have to, should for advice, modals of possibility and deduction, and past modals (must have), A1–B2.',
      intro: 'Modal verbs are grouped here by meaning, which is how students actually need them: ability (<em>can</em>, <em>could</em>) at A1–A2, obligation and rules (<em>must</em>, <em>have to</em>, <em>don\'t have to</em>) and advice (<em>should</em>) at A2, possibility and deduction at B1, and past modals of deduction and regret (<em>must have</em>, <em>should have</em>) at B2. Pick the function you are teaching and you will find a grammar, reading, writing and practice sheet for it.',
    },
  },
  {
    re: /going to|future|\bwill\b/i,
    guide: { slug: 'how-to-teach-going-to-future-forms', label: 'How to Teach Future Forms' },
    hub: {
      slug: 'future-forms', name: 'Future Forms',
      desc: 'Free future tense worksheets: going to, will, present continuous for arrangements, future time clauses, future continuous and future perfect, A1–B2.',
      intro: 'English has no single future tense, which is exactly why students struggle with it. These worksheets introduce <em>going to</em> for plans at A1, <em>will</em> and the will-vs-going-to contrast at A2, the present continuous for arrangements and future time clauses (<em>when</em>, <em>before</em>, <em>after</em>) at B1, and the future continuous and future perfect at B2. Review sheets at each level make students choose between forms, which is the real skill.',
    },
  },
  {
    re: /irregular verb/i,
    guide: { slug: 'how-to-learn-irregular-verbs', label: 'How to Learn Irregular Verbs' },
    hub: null,
  },
  {
    re: /past simple|simple past|\bwas\b.{0,6}\bwere\b/i,
    guide: { slug: 'how-to-teach-past-simple', label: 'How to Teach the Past Simple' },
    hub: {
      slug: 'past-simple', name: 'Past Simple',
      desc: 'Free past simple worksheets: was/were, regular -ed verbs and spelling, irregular verbs, time expressions and past simple vs. past continuous, A1–B1.',
      intro: 'Most courses teach the past simple in three steps, and these worksheets follow them: <em>was</em> and <em>were</em> first, then regular <em>-ed</em> verbs with their spelling and pronunciation, then the most common irregular verbs. A2 sheets add time expressions (<em>yesterday</em>, <em>last weekend</em>, <em>ago</em>) and storytelling, and the B1 review contrasts the past simple with the past continuous. Readings are short personal stories, so students have a model before they write their own.',
    },
  },
  {
    re: /present continuous|present progressive/i,
    guide: { slug: 'how-to-teach-present-continuous', label: 'How to Teach the Present Continuous' },
    hub: {
      slug: 'present-continuous', name: 'Present Continuous',
      desc: 'Free present continuous worksheets: am/is/are + -ing, spelling rules, actions happening now and present simple vs. present continuous, A2–B1.',
      intro: 'The present continuous is simple to form and hard to use correctly, because students have just learned the present simple and now need to choose. These worksheets cover the form and <em>-ing</em> spelling rules first, then actions happening now with picture-based reading and speaking tasks, and finally the present simple vs. present continuous contrast (<em>usually</em> vs. <em>right now</em>), with a B1 review for classes that need to revisit it.',
    },
  },
  {
    re: /verb (to )?be\b/i,
    guide: { slug: 'how-to-teach-verb-to-be', label: 'How to Teach the Verb To Be' },
    hub: {
      slug: 'verb-to-be', name: 'Verb To Be',
      desc: 'Free verb to be worksheets for A1: am/is/are for name, age, nationality and jobs, negatives and questions, was/were, with reading, writing and speaking.',
      intro: 'The verb <em>to be</em> is the first grammar point of almost every beginner course, and it carries the whole first unit: introducing yourself, age, nationality, jobs and feelings. These A1 worksheets cover <em>am / is / are</em> in affirmative, negative and question form, with reading texts built around personal information, guided writing, a speaking sheet and a past form (<em>was / were</em>) sheet for when you move on.',
    },
  },
  {
    re: /present simple|simple present|daily routine/i,
    guide: { slug: 'how-to-teach-present-simple', label: 'How to Teach the Present Simple' },
    hub: {
      slug: 'present-simple', name: 'Present Simple',
      desc: 'Free present simple worksheets: daily routines, third person -s, do/does questions and negatives, with reading, writing and speaking practice, A1–A2.',
      intro: 'The present simple is taught through routines because routines are what it describes. These worksheets start with the third person <em>-s</em> at A1 and build to full daily-routine lessons at A2: the grammar sheet presents <em>do / does</em> questions and negatives, the reading gives a model routine, the writing sheet has students describe their own day and the speaking sheet turns it into pair work. A B1 practice sheet is there for classes that need a deeper review.',
    },
  },
  {
    re: /possessive adjective/i,
    guide: { slug: 'how-to-teach-possessive-adjectives', label: 'How to Teach Possessive Adjectives' },
    hub: null,
  },
];

// Functional English sets (Reading / Practice / Writing, no Grammar sheet —
// see the guide) are matched by their tag BEFORE the grammar regexes: titles
// like "Health Problems – … Advice" or "Making Complaints – … Could you…?"
// would otherwise land on the modal-verbs guide.
const FUNCTIONAL = { guide: { slug: 'how-to-teach-functional-english', label: 'How to Teach Functional English' }, hub: null };
const isFunctional = (ws) => /functional english/i.test((ws && ws.tags) || '');

function topicFor(ws) {
  if (!ws) return null;
  if (isFunctional(ws)) return FUNCTIONAL;
  const text = `${ws.title || ''} ${(ws.topic_key || '').replace(/-/g, ' ')}`;
  return TOPICS.find((t) => t.re.test(text)) || null;
}

// Hubs listed in teaching order (index page, "Explore more", sitemap) — not
// in match order, which is tuned for regex precedence.
const HUB_ORDER = ['verb-to-be', 'present-simple', 'present-continuous', 'past-simple', 'future-forms',
  'comparatives-superlatives', 'modal-verbs', 'present-perfect', 'conditionals', 'passive-voice', 'reported-speech'];
const HUBS = TOPICS.filter((t) => t.hub)
  .sort((x, y) => (HUB_ORDER.indexOf(x.hub.slug) + 99) % 99 - (HUB_ORDER.indexOf(y.hub.slug) + 99) % 99);
const hubBySlug = (slug) => HUBS.find((t) => t.hub.slug === slug) || null;

// SERP title for a worksheet page: add "Worksheet" and the level when they fit.
// The stored title stays the visible <h1>; only <title> changes. Brand suffix
// stays off on purpose (dropped 09/09 — pushed titles past the ~60-char cutoff).
function seoTitle(ws) {
  const MAX = 65;
  let core = String(ws.title || '').trim();
  const groups = [];
  let m;
  while ((m = core.match(/\s*\(([^()]*)\)\s*$/))) { groups.unshift(m[1]); core = core.slice(0, m.index).trim(); }
  const level = ws.level || '';
  const extras = groups.filter((g) => g !== level).map((g) => ` (${g})`).join('');
  const hasWs = /worksheet/i.test(core);
  // Level already inside the title ("Present Perfect Tense (A2) – Grammar",
  // "… (A1) – Variant 2") — don't repeat it.
  const lvl = level && !core.includes(`(${level})`) ? ` (${level})` : '';
  const candidates = [
    `${core}${hasWs ? '' : ' Worksheet'}${lvl}${extras}`,
    `${core}${lvl}${extras}`,
  ];
  return candidates.find((c) => c.length <= MAX) || String(ws.title || '');
}

module.exports = { TOPICS, HUBS, topicFor, hubBySlug, seoTitle, isFunctional };
