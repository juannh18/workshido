const sb = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
const LEVEL_CLASS = { A1:'a1', A2:'a2', B1:'b1', B2:'b2', C1:'c1' };
function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
// "Comparative Adjectives – Practice" -> "comparative adjectives". Titles
// with no " – "/" - " separator (standalone worksheets like "Articles",
// "Body Parts") return their own full lowercased title, which only matches
// another worksheet with the exact same title — i.e. effectively no match,
// same as having no related worksheets at all. Also strips a trailing
// "(A2)"-style level marker some titles carry before the dash (e.g.
// "Present Perfect Tense (A2) – Grammar") — left in, it made that title's
// base "present perfect tense (a2)", which never matches the A1 sibling's
// base "present perfect tense", silently hiding the cross-level match.
function titleBase(t) {
  return (t || '').split(/\s[–-]\s/)[0].replace(/\s*\((?:a1|a2|b1|b2|c1)\)\s*$/i, '').trim().toLowerCase();
}
// The "(Easy Version)" Word Searches are the older, simpler puzzles being
// phased out in favor of full diagonal/reversed-word versions — even when
// one's title-base collides with a real set sibling (e.g. "Feelings and
// Emotions – Word Search" vs. "Feelings and Emotions – Label and Learn"),
// it must never carry the "Complete the set" badge. Regular Word Searches
// (no "Easy Version" suffix) are unaffected and still count normally.
function isEasyWordSearch(t) {
  return /\(easy version\)/i.test(t || '');
}
// Vocabulary worksheets rarely share a title-base sibling ("Body Parts" has
// no "Body Parts – Reading" counterpart) but do share topic tags with other
// worksheets phrased differently ("Body Parts" / "Parts of the Face" both
// tagged "body parts") — strip generic tags (format/level/category words)
// so only real topic words are left to match on.
// Format/activity-type tags (how a worksheet is exercised, not what it's
// about) belong here too, or they masquerade as topic tags in byTag — e.g.
// "word search" sat outside the list and matched EVERY "* – Word Search"
// worksheet regardless of subject, drowning out the real same-topic matches
// (Body Parts / Parts of the Face) with unrelated ones (Colors, Weather...)
// that just happen to share the word-search format.
const TAG_STOPLIST = new Set(['worksheet','vocabulary','grammar','reading','writing','practice','listening','speaking','esl','english','a1','a2','b1','b2','c1','reading comprehension','comprehension','labeling','label and learn','language focus','word search','matching','fill-in-the-blank','review']);
function meaningfulTags(tagsStr) {
  return (tagsStr || '').split(',').map(t => t.trim().toLowerCase()).filter(t => t.length > 2 && !TAG_STOPLIST.has(t));
}
// Safety net beyond the static stoplist above: a tag shared by an unusually
// large slice of the WHOLE catalog (not one level) behaves like a category
// label in disguise ("language focus" sat on 61/176 A1 worksheets alone —
// now in the stoplist directly) rather than a real topic. The limit has to
// stay generous, though: a genuinely popular grammar topic spanning 3+
// levels at ~10-12 worksheets each (e.g. "present perfect": 32 across the
// catalog) is completely normal and must NOT be filtered out as generic —
// that silently broke A1↔A2 present-perfect matching until this was raised.
const TAG_FREQ_LIMIT = 45;
function specificTags(tags, freq) {
  return tags.filter(t => (freq.get(t) || 0) <= TAG_FREQ_LIMIT);
}
let _wsFileUrl = null;
let _answerKeyUrl = null;
let _isPremium = false;
let _wsId = null;
let _wsTitle = 'worksheet';
let _quizId = null;
let _quizTitle = 'quiz';

// Preview-then-paywall: instead of blurred skeleton bars (which read as
// "broken / still loading" and plant doubt right before the ask), show a
// concrete checklist of exactly what unlocking delivers, plus a full-width
// CTA. No real answer-key/quiz content is stored server-side for non-premium
// users, so the value has to be sold with specifics, not a fake mockup.
function lockedPreviewCard(kind, colorClass, icon, headLabel, items, ctaLabel) {
  const check = `<svg class="te-card-ic" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>`;
  const body = items.map(s => `
    <div class="te-card-feat">
      ${check}
      <div class="te-card-feat-txt"><span class="te-card-feat-t">${esc(s.t)}</span>${s.d ? `<span class="te-card-feat-d">${esc(s.d)}</span>` : ''}</div>
    </div>`).join('');
  const cta = ctaLabel || `Unlock ${headLabel}`;
  return `<div class="te-card ${colorClass}" onclick="openPremiumModal('${kind}')" role="button" tabindex="0" aria-label="Unlock ${esc(headLabel)}" onkeydown="if(event.key==='Enter'){openPremiumModal('${kind}')}">
    <div class="te-card-head">${icon} ${esc(headLabel)} <span class="te-card-tag">Preview</span></div>
    <div class="te-card-body">
      ${body}
      <button class="te-card-cta" onclick="event.stopPropagation();openPremiumModal('${kind}')">🔓 ${esc(cta)}</button>
    </div>
  </div>`;
}

async function checkAuth() {
  const { data: { user } } = await sb.auth.getUser();
  const uploadLink = document.getElementById('navUploadLink');
  if (uploadLink) uploadLink.style.display = (user?.email === 'juanda.5790@hotmail.com') ? '' : 'none';
  const nav = document.getElementById('navActions');
  // Not logged in: carry this worksheet's URL through Log in / Sign up so a
  // new user who registers via the nav (instead of the download modal's
  // Google button, which already does this) lands back here afterward
  // instead of the homepage.
  if (!user && nav) {
    // Match by substring, not the exact "workshido-login.html" filename —
    // the server-rendered version of this page (netlify/functions/worksheet-
    // page.js, used for SEO) links to the extensionless "/workshido-login"
    // clean URL instead, which an exact selector silently misses.
    const redirect = encodeURIComponent(window.location.href);
    nav.querySelectorAll('a[href*="workshido-login"]').forEach(a => a.href = a.getAttribute('href') + `?redirect=${redirect}`);
    nav.querySelectorAll('a[href*="workshido-signup"]').forEach(a => a.href = a.getAttribute('href') + `?redirect=${redirect}`);
  }
  if (user && nav) {
    const name = user.user_metadata?.full_name || user.email;
    const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0,2);
    // full_name is free text the user set at signup — never trust it as safe
    // HTML when it lands back in innerHTML.
    const escNav = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    nav.innerHTML = `<a href="workshido-profile.html" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:#B5D4F4;font-size:13px;font-weight:500;"><div style="width:32px;height:32px;border-radius:50%;background:#E6F1FB;color:#185FA5;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;border:2px solid #85B7EB;">${escNav(initials)}</div>${escNav(name.split(' ')[0])}</a><button onclick="logOut()" style="background:transparent;border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:7px 14px;color:#B5D4F4;font-size:13px;cursor:pointer;font-family:inherit;">Log out</button>`;
  }
}
async function logOut() { await sb.auth.signOut(); window.location.reload(); }

async function loadWorksheet() {
  const id = new URLSearchParams(window.location.search).get('id');
  if (!id) { renderError('No worksheet ID provided.'); return; }

  const [{ data, error }, { data: { user: currentUser } }] = await Promise.all([
    sb.from('worksheets').select('*').eq('id', id).single(),
    sb.auth.getUser()
  ]);
  if (error || !data) { renderError('Worksheet not found.'); return; }

  if (currentUser) {
    const { data: prof } = await sb.from('profiles').select('is_premium').eq('id', currentUser.id).single();
    _isPremium = prof?.is_premium || false;
  }

  // Related worksheets: matched across ALL levels (not just this one), so a
  // learner on an A1 topic sees the same topic continue into A2/B1 as they
  // progress — combining three signals: (1) same topic_key (only set once a
  // quiz exists for that topic — exact, but covers a minority of worksheets);
  // (2) the title's "Topic – Type" convention (e.g. "Comparative Adjectives
  // – Practice" / "– Reading Practice" share the "comparative adjectives"
  // base, even across levels — "Daily Routines" at A1 and "Daily Routines –
  // Vocabulary (A2)" both reduce to "daily routines"); (3) shared specific
  // topic tags, for cases like Vocabulary worksheets that rarely have a
  // same-titled sibling ("Body Parts" has no "Body Parts – Reading") but do
  // share tags with worksheets on a similar theme phrased differently
  // ("Body Parts" / "Parts of the Face" both tagged "body parts").
  let quiz = null;
  let related = [];
  const quizPromise = data.topic_key
    ? sb.from('quizzes').select('*').eq('topic_key', data.topic_key).eq('level', data.level).maybeSingle()
    : Promise.resolve({ data: null });
  const base = titleBase(data.title);
  const myTags = meaningfulTags(data.tags);
  const [{ data: quizRow }, { data: allRows }] = await Promise.all([
    quizPromise,
    sb.from('worksheets').select('id,title,level,category,thumbnail_url,tags,topic_key').neq('id', data.id),
  ]);
  quiz = quizRow || null;
  const rows = allRows || [];

  const byTopicKey = data.topic_key ? rows.filter(r => r.topic_key === data.topic_key) : [];
  const byTitle = base ? rows.filter(r => titleBase(r.title) === base) : [];
  let byTag = [];
  if (myTags.length) {
    const freq = new Map();
    for (const r of rows) for (const t of meaningfulTags(r.tags)) freq.set(t, (freq.get(t) || 0) + 1);
    const myTagsSpecific = specificTags(myTags, freq);
    byTag = myTagsSpecific.length
      ? rows.filter(r => specificTags(meaningfulTags(r.tags), freq).some(t => myTagsSpecific.includes(t)))
      : [];
  }
  // byTopicKey/byTitle are the exact-same-topic "set" siblings (e.g. this
  // worksheet's Reading/Writing/Practice counterparts) — flagged so
  // renderRelated can list them first and style them as the featured set,
  // vs. byTag matches which are merely thematically related. Restricted to
  // the SAME level: the quiz itself is scoped per topic_key+level (a "set"
  // is Grammar+Reading+Writing+Practice at one level, same as the quiz
  // bundle), so a same-title worksheet at a different level is a topic
  // continuation to explore, not literally part of this set.
  const setMatchIds = isEasyWordSearch(data.title) ? new Set() : new Set(
    [...byTopicKey, ...byTitle].filter(r => r.level === data.level && !isEasyWordSearch(r.title)).map(r => r.id)
  );
  const seen = new Set();
  related = [...byTopicKey, ...byTitle, ...byTag]
    .filter(r => seen.has(r.id) ? false : (seen.add(r.id), true))
    .map(r => ({ ...r, _setMatch: setMatchIds.has(r.id) }));

  document.title = `${esc(data.title)} — Workshido`;
  const wsMetaDescription = data.description || `${data.level} ${data.category} worksheet. Free download.`;
  document.querySelector('meta[name="description"]')?.setAttribute('content', wsMetaDescription);
  document.querySelector('meta[property="og:title"]')?.setAttribute('content', `${data.title} — Workshido`);
  document.querySelector('meta[property="og:description"]')?.setAttribute('content', wsMetaDescription);
  document.querySelector('meta[name="twitter:title"]')?.setAttribute('content', `${data.title} — Workshido`);
  let twitterDesc = document.querySelector('meta[name="twitter:description"]');
  if (!twitterDesc) {
    twitterDesc = document.createElement('meta');
    twitterDesc.setAttribute('name', 'twitter:description');
    document.head.appendChild(twitterDesc);
  }
  twitterDesc.setAttribute('content', wsMetaDescription);
  if (data.thumbnail_url) document.querySelector('meta[property="og:image"]')?.setAttribute('content', data.thumbnail_url);
  const wsUrl = `https://workshido.com/workshido-worksheet.html?id=${data.id}`;
  document.querySelector('link[rel="canonical"]')?.setAttribute('href', wsUrl);
  document.querySelector('meta[property="og:url"]')?.setAttribute('content', wsUrl);
  const schema = document.getElementById('schemaLD');
  if (schema) schema.textContent = JSON.stringify({ "@context":"https://schema.org","@type":"LearningResource","name":data.title,"description":data.description||"","educationalLevel":data.level,"learningResourceType":"Worksheet","inLanguage":"en","isAccessibleForFree":data.is_free,"provider":{"@type":"Organization","name":"Workshido","url":"https://workshido.com"} });
  document.getElementById('bcCategory').textContent = data.category || 'Worksheet';
  document.getElementById('bcTitle').textContent = data.title;

  const lvlCls = LEVEL_CLASS[data.level] || 'a1';
  const tags = (data.tags || '').split(',').filter(t => t.trim()).map(t => `<span class="tag">${esc(t.trim())}</span>`).join('');
  const freeBadge = data.is_free ? '<span class="badge-free">Free</span>' : '<span class="badge-premium">⭐ Premium</span>';
  const desc = data.description ? `<p class="ws-desc">${esc(data.description)}</p>` : '';
  const ext = (data.file_url || '').split('.').pop().split('?')[0].toUpperCase();

  const preview = data.thumbnail_url
    ? `<img src="${data.thumbnail_url}" alt="${data.title}">`
    : `<div class="preview-placeholder">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        <span>No preview available</span>
      </div>`;

  _wsFileUrl = data.file_url || null;
  _answerKeyUrl = data.teacher_edition_url || null;
  _wsId = data.id;
  _wsTitle = data.title || 'worksheet';
  const _rating = data.rating || 0;
  const _ratingsCount = data.ratings_count || 0;

  const alreadyRated = localStorage.getItem('rated_' + data.id);

  function starsDisplay(avg, count) {
    const full = Math.floor(avg);
    const half = (avg - full) >= 0.5;
    let s = '';
    for (let i = 1; i <= 5; i++) {
      if (i <= full) s += '<span class="star-char filled">★</span>';
      else if (i === full + 1 && half) s += '<span class="star-char half">★</span>';
      else s += '<span class="star-char">★</span>';
    }
    const label = count > 0 ? `<span>${avg.toFixed(1)} (${count} rating${count !== 1 ? 's' : ''})</span>` : '<span>No ratings yet</span>';
    return `<div class="stars-display">${s}</div>${label}`;
  }

  const starInteractive = alreadyRated
    ? `<div class="star-done">✓ You rated ${alreadyRated}/5 — thanks!</div>`
    : `<div id="starInput">
         <div class="star-label">Rate this worksheet:</div>
         <div class="stars-interactive" id="starRow" onmouseleave="starsOut()">
           ${[1,2,3,4,5].map(n => `<span class="star-i" id="si${n}" onmouseover="starsHover(${n})" onclick="rateWS(${n})">★</span>`).join('')}
         </div>
       </div>`;

  const starSection = `
    <div class="star-section">
      <div class="star-avg-row" id="starAvgRow">${starsDisplay(_rating, _ratingsCount)}</div>
      ${starInteractive}
    </div>`;

  // data.is_free is always true by policy (upload scripts force it), but the
  // button still respects it instead of always rendering "Download free" —
  // a worksheet ever marked premium shouldn't silently stay downloadable.
  const downloadBtn = (data.is_free !== false || _isPremium)
    ? `<button class="btn-download-big" onclick="downloadWS('${data.id}',${data.downloads||0})">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
        Download free
      </button>`
    : `<button class="btn-download-big locked" onclick="openPremiumModal('worksheet_download')">🔒 Premium — Unlock to download</button>`;

  const answerKeyBtn = _answerKeyUrl
    ? (_isPremium
        ? `<button class="btn-answer-key unlocked" onclick="downloadAnswerKey()">
            <span class="ak-left">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              <span>Teacher Edition <span class="ak-sub">⭐ Premium — Download</span></span>
            </span>
          </button>`
        : `${lockedPreviewCard('teacher_edition', 'te-amber', '📘', 'Teacher Edition', [
            { t: 'Complete answer key', d: 'every exercise, fully worked' },
            { t: 'Learning objective & success criteria' },
            { t: 'Lesson plan', d: 'I Do / We Do / You Do, ready to teach' },
            { t: 'Common student mistakes', d: 'and how to correct them' },
          ], 'Unlock Teacher Edition')}
          ${!currentUser ? '<p class="premium-note">Already Premium? <a onclick="googleLoginDl()">Sign in</a></p>' : ''}`)
    : '';

  _quizId = quiz?.id || null;
  _quizTitle = quiz?.title || 'quiz';
  const quizBtn = quiz
    ? (_isPremium
        ? `<button class="btn-quiz unlocked" onclick="downloadQuiz()">
            <span class="ak-left">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              <span>Full Quiz <span class="ak-sub">⭐ Premium — Download</span></span>
            </span>
          </button>
          <p class="quiz-key-link">Covers ${esc(quiz.skills)} · <a onclick="downloadQuiz('key')">Download answer key</a></p>
          <div class="quiz-prep-tip">
            <div class="prep-label">Your prep checklist</div>
            <div class="prep-steps"><span class="prep-step"><span class="num">1</span>Grammar</span><span class="prep-arrow">→</span><span class="prep-step"><span class="num">2</span>Reading</span><span class="prep-arrow">→</span><span class="prep-step"><span class="num">3</span>Writing</span><span class="prep-extra">(+ Practice if you want extra reps)</span></div>
            <div class="prep-line">Done with those? You're ready. <a href="workshido-how-quiz-works.html">Why this order →</a></div>
          </div>`
        : `${lockedPreviewCard('quiz', 'te-pink', '📝', 'Full Quiz', [
            { t: 'Grammar, Reading & Writing', d: 'one graded evaluation' },
            { t: 'Score at the end', d: 'see exactly where the student stands' },
            { t: 'Full answer key', d: 'model answers for every section' },
          ], 'Unlock Full Quiz')}
          <p class="quiz-key-link">Covers ${esc(quiz.skills)}</p>
          <div class="quiz-prep-tip">
            <div class="prep-label">How to get there</div>
            <div class="prep-steps"><span class="prep-step"><span class="num">1</span>Grammar</span><span class="prep-arrow">→</span><span class="prep-step"><span class="num">2</span>Reading</span><span class="prep-arrow">→</span><span class="prep-step"><span class="num">3</span>Writing</span><span class="prep-extra">(all free)</span></div>
            <div class="prep-line">Then unlock the <b>only graded evaluation</b> on Workshido — full answer key included. <a href="workshido-how-quiz-works.html">Why this order →</a></div>
          </div>`)
    : '';

  document.getElementById('pageWrap').innerHTML = `
    <div class="preview-box">${preview}</div>
    <div class="detail-sidebar">
      <div class="detail-card">
        <h1 class="ws-title">${esc(data.title)}</h1>
        <div class="ws-badges">
          <span class="badge-level ${lvlCls}">${data.level}</span>
          ${data.category ? `<span class="badge-cat ${catClass(data.category)}">${esc(data.category)}</span>` : ''}
          ${freeBadge}
        </div>
        ${data.description ? `<p class="ws-desc">${esc(data.description)}</p>` : ''}
        ${tags ? `<div class="ws-tags">${tags}</div>` : ''}
        <div class="ws-meta">
          <div class="ws-meta-row"><span class="ws-meta-label">Format</span><span class="ws-meta-value">${ext || '—'}</span></div>
          <div class="ws-meta-row"><span class="ws-meta-label">Level</span><span class="ws-meta-value">${data.level || '—'}</span></div>
          <div class="ws-meta-row"><span class="ws-meta-label">Downloads</span><span class="ws-meta-value" id="dlCount">${data.downloads || 0}</span></div>
        </div>
        ${downloadBtn}
        <button class="btn-print" onclick="printWS()">🖨️ Print / Open PDF — Free</button>
        ${answerKeyBtn}
        ${quizBtn}
        ${starSection}
      </div>
    </div>`;

  renderRelated(related, lvlCls, data.category, data.level);
}

// Groups related worksheets first by level (A1 → C1, so a learner sees the
// same topic continue as they progress), then by category within each level
// — a visitor reading a Reading worksheet should see "try the Grammar/
// Writing version" as a distinct next step, not buried among more
// worksheets of the same type they already have. Within the CURRENT level,
// categories other than the one they're already reading lead; the current
// category trails last. Other levels use the plain topic order since
// there's no "already looking at this" bias for a level the visitor isn't on.
const LEVEL_ORDER = ['A1', 'A2', 'B1', 'B2', 'C1'];
const CATEGORY_ORDER = ['Grammar', 'Practice', 'Reading', 'Writing', 'Vocabulary', 'Listening', 'Speaking'];
// The DB only has 5 category values (Grammar/Reading/Writing/Vocabulary/
// Speaking) — "Practice" isn't one, so drill-style worksheets ("Possessive
// Adjectives – Practice", "Comparative Adjectives – Practice Time") sit
// under Grammar alongside explainer-style ones. Split them into their own
// group by title wording instead, so the two don't read as one bucket.
function displayCategory(r) {
  return (r.category === 'Grammar' && /\bpractice\b/i.test(r.title || '')) ? 'Practice' : (r.category || 'Other');
}
// Category → color class, so Grammar/Reading/Writing/Vocabulary/Speaking/
// Practice each get a distinct pastel pill (same pattern as the level badge)
// instead of sharing one flat gray — lets a learner scan a row of related
// cards by color instead of reading every label.
const CAT_CLASS = { Grammar: 'cat-grammar', Reading: 'cat-reading', Writing: 'cat-writing', Vocabulary: 'cat-vocabulary', Speaking: 'cat-speaking', Practice: 'cat-practice' };
function catClass(name) { return CAT_CLASS[name] || 'cat-other'; }
function renderRelated(related, lvlCls, currentCategory, currentLevel) {
  const section = document.getElementById('relatedSection');
  const grid = document.getElementById('relatedGrid');
  if (!section || !grid || !related.length) return;

  const levelGroups = new Map();
  for (const r of related) {
    const lvl = r.level || 'Other';
    if (!levelGroups.has(lvl)) levelGroups.set(lvl, []);
    levelGroups.get(lvl).push(r);
  }
  // Current level always leads. After that, other levels are ordered by how
  // close they are on the CEFR ladder (A2 view: B1 next, then A1 — not
  // always ascending A1→C1) since "what's the next step up" is more useful
  // than a fixed alphabetical march; ties (e.g. from A2, B1 and A1 are both
  // 1 step away) favor the higher level as the more natural "next step".
  const curIdx = LEVEL_ORDER.indexOf(currentLevel);
  const orderedLevels = [...levelGroups.keys()].sort((a, b) => {
    if (a === currentLevel) return -1;
    if (b === currentLevel) return 1;
    const ia = LEVEL_ORDER.indexOf(a), ib = LEVEL_ORDER.indexOf(b);
    const da = (ia === -1 || curIdx === -1) ? 99 : Math.abs(ia - curIdx);
    const db = (ib === -1 || curIdx === -1) ? 99 : Math.abs(ib - curIdx);
    if (da !== db) return da - db;
    return ib - ia; // tie: higher level first
  });

  const cardHtml = r => {
    const rLvlCls = LEVEL_CLASS[r.level] || lvlCls;
    const thumb = r.thumbnail_url
      ? `<img src="${r.thumbnail_url}" alt="${esc(r.title)}" loading="lazy">`
      : `<div class="related-thumb-placeholder">📄</div>`;
    // Same-topic "set" siblings (this worksheet's Reading/Writing/Practice
    // counterparts) get a distinct featured treatment so they read as "the
    // rest of this set" at a glance, not just another suggestion in the pile.
    // The strip sits above the thumbnail, never over it, so it never covers
    // the worksheet's own printed title in the preview image.
    const setBadge = r._setMatch ? `<div class="set-match-badge"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>Complete the set</div>` : '';
    return `<a href="workshido-worksheet.html?id=${r.id}" class="related-card${r._setMatch ? ' set-match' : ''}">
      ${setBadge}
      <div class="related-thumb">${thumb}</div>
      <div class="related-body">
        <div class="related-badges">
          <span class="badge-level ${rLvlCls}">${r.level}</span>
          <span class="badge-cat ${catClass(displayCategory(r))}">${esc(displayCategory(r))}</span>
        </div>
        <div class="related-name">${esc(r.title)}</div>
      </div>
    </a>`;
  };

  // One flowing row of cards per level (wrapping left-to-right, no per-
  // category sub-blocks/headers) — the category is still visible on each
  // card's own badge. Same-topic "set" siblings always lead within their
  // level group; after that, within the worksheet's own level, its own
  // category trails last, and other levels use the plain topic order.
  const sortForLevel = (items, biasCurrentCategory) => [...items].sort((a, b) => {
    if (a._setMatch !== b._setMatch) return a._setMatch ? -1 : 1;
    const ca = displayCategory(a), cb = displayCategory(b);
    if (biasCurrentCategory) {
      if (ca === currentCategory && cb !== currentCategory) return 1;
      if (cb === currentCategory && ca !== currentCategory) return -1;
    }
    const ia = CATEGORY_ORDER.indexOf(ca), ib = CATEGORY_ORDER.indexOf(cb);
    return (ia === -1 ? 99 : ia) - (ib === -1 ? 99 : ib);
  });

  grid.innerHTML = orderedLevels.map(lvl => `
    <div class="related-level-group">
      <h2 class="related-level-title"><span class="badge-level ${LEVEL_CLASS[lvl] || lvlCls}">${esc(lvl)}</span></h2>
      <div class="related-grid">${sortForLevel(levelGroups.get(lvl), lvl === currentLevel).map(cardHtml).join('')}</div>
    </div>`).join('');
  section.style.display = '';
}

// Focus management for modals: remember what had focus before opening so
// keyboard/screen-reader users land back where they were after closing,
// and move focus into the dialog itself (its close button) on open.
let _lastFocusedBeforeModal = null;
function _openModal(el) {
  _lastFocusedBeforeModal = document.activeElement;
  el.classList.add('open');
  el.querySelector('.modal-close')?.focus();
}
function _closeModal(el) {
  el.classList.remove('open');
  _lastFocusedBeforeModal?.focus();
}
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  if (document.getElementById('premiumModal')?.classList.contains('open')) closePremiumModal();
  else if (document.getElementById('dlModal')?.classList.contains('open')) closeDlModal();
});

function openDlModal(action) {
  document.getElementById('dlModalTitle').textContent =
    action === 'print' ? 'Sign in to print for free' :
    action === 'rate'  ? 'Sign in to rate this worksheet' :
    'Sign in to download for free';
  _openModal(document.getElementById('dlModal'));
}

async function getSignedUrl(fileUrl) {
  // Worksheet files live in a PUBLIC storage bucket, so the URL already
  // works as-is — signing it added an extra ~0.5-1s network round-trip to
  // Supabase's sign endpoint before the actual PDF fetch could even start,
  // on every single download/print click, for no benefit (nothing about a
  // public file needs a signature to be readable).
  if (fileUrl.includes('/object/public/')) return fileUrl;
  const m = fileUrl.match(/\/object\/(?:public|sign)\/([^/]+)\/([^?]+)/);
  if (!m) return fileUrl;
  const { data } = await sb.storage.from(m[1]).createSignedUrl(m[2], 60);
  return data?.signedUrl || fileUrl;
}

async function downloadWS(id, currentDl) {
  let session;
  try {
    const { data } = await sb.auth.getSession();
    session = data.session;
    if (!session) { openDlModal('download'); return; }
  } catch(e) { openDlModal('download'); return; }
  // Preferred path: a SAME-ORIGIN call to our own function, which hands back a
  // short-lived R2 URL with Content-Disposition: attachment. Navigating to it
  // downloads the file directly — no cross-origin fetch that ad blockers /
  // tracking protection / stale-CDN-CORS can silently break into an "open in
  // new tab". Works on iOS too. Falls back to the old blob method on failure.
  let directUrl = null;
  try {
    const r = await fetch(`/.netlify/functions/download-worksheet?id=${encodeURIComponent(id)}`, {
      headers: { 'Authorization': `Bearer ${session.access_token}` },
    });
    if (r.ok) directUrl = (await r.json()).url || null;
  } catch (e) {}

  // Fire analytics + the download-count bump BEFORE triggering the download, so
  // a stripped-down in-app webview that treats the attachment URL as a plain
  // navigation can't cancel them mid-flight.
  window.wsTrack?.('download_completed', { worksheet_id: id });
  fetch('/.netlify/functions/increment-downloads', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${session.access_token}` },
    body: JSON.stringify({ worksheetId: id }),
  })
    .then((res) => res.json())
    .then(({ downloads }) => {
      const el = document.getElementById('dlCount');
      if (el && downloads) el.textContent = downloads;
    })
    .catch(() => {});

  if (directUrl) {
    window.location.href = directUrl;
  } else if (_wsFileUrl) {
    await forceDownload(await getSignedUrl(_wsFileUrl), _wsTitle);
  }
}

async function forceDownload(url, filename) {
  // iOS Safari doesn't reliably honor <a download> on a blob: URL created via
  // fetch — the file can end up saved in a broken/partial state that share
  // sheets (e.g. WhatsApp) refuse to attach. Let Safari handle the PDF via a
  // real navigation instead, which uses its native download/share flow.
  const isIOS = /iP(hone|ad|od)/.test(navigator.userAgent) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  if (isIOS) {
    window.open(url, '_blank');
    return;
  }
  const safeName = (filename || 'worksheet').replace(/[\\/:*?"<>|]+/g, '').trim() || 'worksheet';
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error('fetch failed');
    const blob = await res.blob();
    const blobUrl = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = blobUrl;
    a.download = `${safeName}.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(blobUrl), 4000);
  } catch (e) {
    // Cross-origin fetch blocked or network error — fall back to opening the file directly.
    window.open(url, '_blank');
  }
}

function starsHover(v) {
  for (let i = 1; i <= 5; i++)
    document.getElementById('si' + i)?.classList.toggle('active', i <= v);
}
function starsOut() {
  for (let i = 1; i <= 5; i++)
    document.getElementById('si' + i)?.classList.remove('active');
}
async function rateWS(v) {
  const input = document.getElementById('starInput');
  if (!input) return;

  let session;
  try {
    const { data } = await sb.auth.getSession();
    session = data.session;
    if (!session) { openDlModal('rate'); return; }
  } catch(e) { openDlModal('rate'); return; }

  // Feedback inmediato — no esperar la red
  localStorage.setItem('rated_' + _wsId, v);
  input.innerHTML = `<div class="star-done">✓ You rated ${v}/5 — thanks!</div>`;
  window.wsTrack?.('rating_submitted', { worksheet_id: _wsId, rating: v });

  // Guardar en DB en segundo plano
  try {
    const res = await fetch('/.netlify/functions/submit-rating', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${session.access_token}` },
      body: JSON.stringify({ worksheetId: _wsId, rating: v }),
    });
    if (res.ok) {
      const json = await res.json();
      if (json.rating != null) {
        const avgRow = document.getElementById('starAvgRow');
        if (avgRow) {
          const r = json.rating, c = json.ratings_count;
          const full = Math.floor(r), half = (r - full) >= 0.5;
          let s = '';
          for (let i = 1; i <= 5; i++) {
            if (i <= full) s += '<span class="star-char filled">★</span>';
            else if (i === full + 1 && half) s += '<span class="star-char half">★</span>';
            else s += '<span class="star-char">★</span>';
          }
          avgRow.innerHTML = `<div class="stars-display">${s}</div><span>${r.toFixed(1)} (${c} rating${c !== 1 ? 's' : ''})</span>`;
        }
      }
    }
  } catch(e) {}
}

async function printWS() {
  try {
    const { data: { user } } = await sb.auth.getUser();
    if (!user) { openDlModal('print'); return; }
  } catch(e) { openDlModal('print'); return; }
  if (!_wsFileUrl) return;
  const url = await getSignedUrl(_wsFileUrl);
  window.open(url, '_blank');
}

function closeDlModal() { _closeModal(document.getElementById('dlModal')); }

async function downloadAnswerKey() {
  if (!_answerKeyUrl || !_wsId) return;
  // Premium is verified server-side here (not just the button being hidden) —
  // the signed URL for the paid Teacher Edition is only ever issued after that check.
  try {
    const { data: { session } } = await sb.auth.getSession();
    if (!session) { openDlModal('download'); return; }
    const res = await fetch('/.netlify/functions/get-teacher-edition-url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${session.access_token}` },
      body: JSON.stringify({ worksheetId: _wsId }),
    });
    if (res.status === 403) { openPremiumModal('teacher_edition'); return; }
    if (!res.ok) return;
    const { url } = await res.json();
    if (url) window.open(url, '_blank');
  } catch (e) {}
}

async function downloadQuiz(kind) {
  if (!_quizId) return;
  // Same server-side premium check as downloadAnswerKey — the signed URL is
  // only ever issued after that check, never derived from the button state.
  try {
    const { data: { session } } = await sb.auth.getSession();
    if (!session) { openDlModal('download'); return; }
    const res = await fetch('/.netlify/functions/get-quiz-url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${session.access_token}` },
      body: JSON.stringify({ quizId: _quizId, kind: kind || 'quiz' }),
    });
    if (res.status === 403) { openPremiumModal('quiz'); return; }
    if (!res.ok) return;
    const { url } = await res.json();
    if (url) window.open(url, '_blank');
  } catch (e) {}
}

async function openPremiumModal(source) {
  const { data: { user } } = await sb.auth.getUser();
  window.wsTrack?.('premium_modal_opened', { worksheet_id: _wsId, source: source || 'other', signed_in: !!user });
  if (!user) {
    document.getElementById('dlModalTitle').textContent = 'Sign in to access Premium';
    _openModal(document.getElementById('dlModal'));
  } else {
    _openModal(document.getElementById('premiumModal'));
  }
}
function closePremiumModal() {
  if (document.getElementById('premiumModal').classList.contains('open')) {
    window.wsTrack?.('premium_modal_dismissed', { worksheet_id: _wsId });
  }
  _closeModal(document.getElementById('premiumModal'));
}

async function startCheckout(plan) {
  const { data: { session } } = await sb.auth.getSession();
  if (!session) {
    document.getElementById('premiumModal').classList.remove('open');
    document.getElementById('dlModalTitle').textContent = 'Sign in to access Premium';
    _openModal(document.getElementById('dlModal'));
    return;
  }
  window.wsTrack?.('checkout_started', { plan });
  try {
    const res = await fetch('/.netlify/functions/create-checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${session.access_token}` },
      body: JSON.stringify({ plan }),
    });
    const { url } = await res.json();
    if (url) window.location.href = url;
  } catch (e) {
    alert('Something went wrong. Please try again.');
  }
}

function googleLoginDl() {
  window.location.href = 'workshido-login.html?redirect=' + encodeURIComponent(window.location.href);
}

function renderError(msg) {
  document.getElementById('pageWrap').innerHTML = `<div class="loading">${msg} <a href="workshido-index.html" style="color:var(--blue-600)">← Back to catalog</a></div>`;
}

document.addEventListener('DOMContentLoaded', () => { checkAuth(); loadWorksheet(); });