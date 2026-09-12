const sb2 = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');

// ── Auth state — updated instantly from localStorage via onAuthStateChange ──
let wsCurrentUser = null;

async function updateNav2(user) {
  const uploadLink = document.getElementById('navUploadLink');
  if (uploadLink) uploadLink.style.display = (user?.email === 'juanda.5790@hotmail.com') ? '' : 'none';
  const nav = document.getElementById('navActions');
  if (!nav) return;
  if (user) {
    let pa = {};
    try { pa = (await sb2.from('profiles').select('avatar, display_name').eq('id', user.id).maybeSingle()).data || {}; } catch (e) {}
    const name = (pa.display_name || user.user_metadata?.full_name || user.email || '').trim();
    const initials = name.split(/\s+/).filter(Boolean).map(n=>n[0]).join('').toUpperCase().slice(0,2);
    const pic = user.user_metadata?.avatar_url || user.user_metadata?.picture || '';
    // free text — never trust as HTML in innerHTML.
    const escNav = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    const inner = window.wsNavAvatar ? window.wsNavAvatar(pa.avatar, pic, initials) : escNav(initials);
    nav.innerHTML = '<a href="workshido-profile.html" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:#B5D4F4;font-size:13px;font-weight:500;"><div style="width:32px;height:32px;border-radius:50%;overflow:hidden;background:#E6F1FB;color:#185FA5;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;border:2px solid #85B7EB;flex-shrink:0;">'+inner+'</div>'+escNav(name.split(/\s+/)[0])+'</a><button onclick="logOut2()" style="background:transparent;border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:7px 14px;color:#B5D4F4;font-size:13px;cursor:pointer;font-family:inherit;">Log out</button>';
  }
}

sb2.auth.onAuthStateChange((_event, session) => {
  wsCurrentUser = session?.user || null;
  updateNav2(wsCurrentUser);
});

async function checkAuth2(){ /* nav now handled by onAuthStateChange */ }
async function logOut2(){await sb2.auth.signOut();window.location.reload();}

// ── Catalog ───────────────────────────────────────
const LEVEL_COLORS = { A1:'teal', A2:'blue', B1:'amber', B2:'purple', C1:'coral' };
const LEVEL_CLASS  = { A1:'a1',   A2:'a2',   B1:'b1',   B2:'b2',   C1:'c1'   };
const ACCENT       = { A1:'accent-teal', A2:'accent-blue', B1:'accent-amber', B2:'accent-purple', C1:'accent-amber' };

// Catalog cards render thumbnails at ~210-280px — use the ~440px _sm
// derivative (tools/make_thumb_sm.py), not the full 640px preview image.
// onerror on the <img> falls back to the original if an _sm is missing.
function smThumb(u) { return u && /\.webp(\?|$)/i.test(u) ? u.replace(/\.webp(\?|$)/i, '_sm.webp$1') : u; }

let allWorksheets = [];
const PAGE_SIZE = 24;
let currentPage = 1;
let _lastFiltered = [];
let activeLevel = 'all';
let activeCategory = 'all';
let activeTopic = 'all';      // 'all' | array of matcher terms
let activeTopicLabel = '';
let searchQuery = '';
// Set (to the level that was dropped) when a level-scoped search comes up
// empty and gets retried against the whole catalog — see filterAndRender().
let searchBroadenedFromLevel = '';

// ── "Latest worksheets" rows — the default (no filter/search) landing view.
//    One row per CEFR level plus a Vocabulary row, each showing the 5 most
//    recently uploaded worksheets in that group, instead of one flat
//    newest-first list mixing every level/category together. A row with 0
//    matches (e.g. C1 today) is simply skipped — it appears on its own once
//    that group has worksheets.
const LATEST_ROWS_DEF = [
  { label: 'Vocabulary', type: 'category', value: 'Vocabulary' },
  { label: 'A1', type: 'level', value: 'A1' },
  { label: 'A2', type: 'level', value: 'A2' },
  { label: 'B1', type: 'level', value: 'B1' },
  { label: 'B2', type: 'level', value: 'B2' },
  { label: 'C1', type: 'level', value: 'C1' },
];

function isDefaultView() {
  return activeLevel === 'all' && activeCategory === 'all' && activeTopic === 'all' && !searchQuery;
}

// Landed on a level with no other filter yet (e.g. the A1 chip, or
// ?level=A1) — same "curated rows" idea as the default view, but broken
// out by category within that one level instead of by level.
function isLevelOnlyView() {
  return activeLevel !== 'all' && activeCategory === 'all' && activeTopic === 'all' && !searchQuery;
}

// allWorksheets is already sorted newest-first (the initial query orders by
// created_at desc), so filtering it per group and taking the first 5 gives
// the latest 5 of that group without needing to re-sort — unless the sort
// dropdown is set to "Most downloaded", in which case each row re-sorts its
// own group by downloads instead, so the rows track the chosen sort just
// like the flat grid does.
function renderLatestRows() {
  const container = document.getElementById('latestRows');
  if (!container) return;
  const sort = document.getElementById('sortSelect')?.value || 'newest';
  const rowsHtml = LATEST_ROWS_DEF.map(row => {
    // Level rows exclude Vocabulary — otherwise whenever a level's most
    // recent/downloaded uploads happen to also be its most recent/downloaded
    // Vocabulary uploads (e.g. several new A1 word searches in a row), that
    // level's row is just a duplicate of the Vocabulary row above it.
    // The Vocabulary row itself uses cardCategory() (same "Practice" split as
    // the card badge) instead of the raw DB category — otherwise a "X –
    // Vocabulary Practice" worksheet shows a "Practice" badge on its card
    // while sitting inside a row header that says "Vocabulary".
    let items = allWorksheets
      .filter(w => row.type === 'level'
        ? w.level === row.value && (w.category || '').toLowerCase() !== 'vocabulary'
        : cardCategory(w) === row.value);
    if (sort === 'downloads') items = [...items].sort((a, b) => (b.downloads || 0) - (a.downloads || 0));
    items = items.slice(0, 5);
    if (!items.length) return '';
    return `<div class="latest-row">
      <div class="latest-row-header">
        <span class="latest-row-title">${row.label}</span>
        <button type="button" class="latest-row-seeall" onclick="latestRowSeeAll('${row.type}','${row.value}')">See all →</button>
      </div>
      <div class="card-grid">${items.map(buildCard).join('')}</div>
    </div>`;
  }).filter(Boolean).join('');
  container.innerHTML = rowsHtml;
}

function latestRowSeeAll(type, value) {
  if (type === 'level') { activeLevel = value; syncLevelChips(); }
  else { activeCategory = value; syncCategoryChips(); }
  resetSearch();
  syncUrl();
  filterAndRender();
  document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
}

// ── Level-only view: same 5-per-row idea as renderLatestRows(), scoped to
//    one CEFR level and split by category instead of by level. "Practice" is
//    matched by title/tag (like the "Practice worksheets" sidebar item) since
//    it isn't a real category value in the DB — drill-style worksheets are
//    stored as Grammar. Excluded from the Grammar row for the same reason
//    the worksheet detail page splits them out: otherwise a "X – Practice"
//    Grammar worksheet would show up in both rows.
const LEVEL_ROW_LABELS = ['Vocabulary', 'Grammar', 'Reading', 'Writing', 'Practice'];

function levelRowMatches(w, label) {
  const isPractice = wsMatchesTerms(w, ['practice']);
  if (label === 'Practice') return isPractice;
  return (w.category || '').toLowerCase() === label.toLowerCase() && !isPractice;
}

function renderLevelRows(level) {
  const container = document.getElementById('latestRows');
  if (!container) return;
  const sort = document.getElementById('sortSelect')?.value || 'newest';
  const rowsHtml = LEVEL_ROW_LABELS.map(label => {
    let items = allWorksheets.filter(w => w.level === level && levelRowMatches(w, label));
    if (sort === 'downloads') items = [...items].sort((a, b) => (b.downloads || 0) - (a.downloads || 0));
    items = items.slice(0, 5);
    if (!items.length) return '';
    return `<div class="latest-row">
      <div class="latest-row-header">
        <span class="latest-row-title">${label}</span>
        <button type="button" class="latest-row-seeall" onclick="levelRowSeeAll('${label}')">See all →</button>
      </div>
      <div class="card-grid">${items.map(buildCard).join('')}</div>
    </div>`;
  }).filter(Boolean).join('');
  container.innerHTML = rowsHtml;
}

function levelRowSeeAll(label) {
  // "Practice" filters via activeTopic (title/tag match), same mechanism as
  // the sidebar's "Practice worksheets" item — there's no real category to
  // filter on. Every other row is a real category. Level stays as-is.
  if (label === 'Practice') {
    activeCategory = 'all';
    activeTopic = ['practice'];
    activeTopicLabel = 'Practice worksheets';
  } else {
    activeCategory = label;
    activeTopic = 'all';
    activeTopicLabel = '';
  }
  syncCategoryChips();
  syncUrl();
  filterAndRender();
  document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
}

// ── Sidebar definition: label + matcher terms against real tags/titles.
//    Items with 0 matching worksheets are hidden automatically.
const SIDEBAR_SECTIONS = [
  // Grammar topics is curated by real popularity in buildSidebar() (top N by
  // downloads, rest behind a "See all topics" toggle) — this list only needs
  // to be COMPLETE, not pre-sorted, so it's fine to list every real topic in
  // the catalog even though most won't fit in the default view.
  { title: 'Grammar topics', items: [
    { label: 'Verb to be',            match: ['verb to be', 'am is are'] },
    { label: 'Present simple',        match: ['present simple', 'presentsimple'] },
    { label: 'Present continuous',    match: ['present continuous'] },
    { label: 'Present simple vs continuous', match: ['present simple vs'] },
    { label: 'Present perfect',       match: ['present perfect'] },
    { label: 'Present perfect continuous', match: ['present perfect continuous'] },
    { label: 'Present perfect vs past simple', match: ['present perfect vs'] },
    { label: 'Past simple',           match: ['past simple'] },
    { label: 'Past continuous',       match: ['past continuous'] },
    { label: 'Past perfect',          match: ['past perfect'] },
    { label: 'Future & going to',     match: ['going to', 'future simple', 'future plans', 'will'] },
    { label: 'Future time clauses',   match: ['future time clauses'] },
    { label: 'Zero conditional',      match: ['zero conditional'] },
    { label: 'First conditional',     match: ['first conditional'] },
    { label: 'Second conditional',    match: ['second conditional'] },
    { label: 'First vs second conditional', match: ['first vs. second conditional', 'first vs second conditional'] },
    { label: 'Passive voice',         match: ['passive voice'] },
    { label: 'Reported speech',       match: ['reported speech'] },
    { label: 'Imperatives',           match: ['imperatives', 'commands'] },
    { label: 'Demonstratives',        match: ['demonstratives', 'this that these those'] },
    { label: 'Articles a/an/the',     match: ['articles', 'a an the'] },
    { label: 'Possessive adjectives', match: ['possessive adjectives', 'possessiveadjectives', 'possessives'] },
    { label: 'Possessive pronouns',   match: ['possessive pronouns'] },
    { label: "Possessive 's (case)",  match: ['possessive s', 'possessive case'] },
    { label: 'Object pronouns',       match: ['object pronouns'] },
    { label: 'Pronouns',              match: ['pronouns'] },
    { label: 'There is / There are',  match: ['there is there are', 'there is/are'] },
    { label: 'Prepositions of place', match: ['prepositions of place'] },
    { label: 'Have got / Has got',    match: ['have got'] },
    { label: 'Modal verbs: can/could', match: ['can & can', 'can and could', 'modalcan'] },
    { label: 'Modal verbs: advice',   match: ['modal verbs of advice', 'ought to'] },
    { label: 'Modal verbs: deduction', match: ['modal verbs of deduction'] },
    { label: 'Modal verbs: obligation', match: ['modal verbs of obligation'] },
    { label: 'Modal verbs: possibility', match: ['modal verbs of possibility'] },
    { label: 'Must / Have to',        match: ['must / have to'] },
    { label: "Should / Shouldn't",    match: ["should / shouldn't"] },
    { label: 'Used to',               match: ['used to'] },
    { label: 'Verb patterns',         match: ['verb patterns'] },
    { label: 'Question words',        match: ['question words'] },
    { label: 'Question tags',         match: ['question tags'] },
    { label: 'Too & enough',          match: ['too and enough', 'too & enough'] },
    { label: 'Some & any',            match: ['some and any', 'some any'] },
    { label: 'Quantifiers',           match: ['quantifiers'] },
    { label: 'Adverbs of frequency',  match: ['adverbs of frequency'] },
  ]},
  { title: 'Skills', items: [
    { label: 'Reading',    cat: 'Reading' },
    { label: 'Writing',    cat: 'Writing' },
    { label: 'Vocabulary', cat: 'Vocabulary' },
    { label: 'Speaking',   cat: 'Speaking' },
    { label: 'Practice worksheets', match: ['practice'] },
  ]},
  { title: 'Topic', items: [
    { label: 'Travel',        match: ['travel'] },
    { label: 'Daily routine', match: ['daily routine'] },
    { label: 'Food & drink',  match: ['food'] },
  ]},
];

function wsMatchesTerms(w, terms) {
  const hay = ((w.title || '') + ' ' + (w.tags || '') + ' ' + (w.category || '')).toLowerCase();
  return terms.some(t => hay.includes(t.toLowerCase()));
}

// Picking a topic/category from the sidebar, chips, or top nav is a fresh browse
// action — any leftover free-text search (especially one that matched nothing)
// must not keep silently filtering out the new selection.
function resetSearch() {
  searchQuery = '';
  const input = document.querySelector('.search-box input');
  if (input) input.value = '';
  const mini = document.getElementById('miniSearchInput');
  if (mini) mini.value = '';
}

// How many Grammar-topic items show by default before "See all topics"
// (the rest still render in the DOM, just hidden — so they stay real,
// crawlable <a href> links for SEO, not lost until a click reveals them).
const SIDEBAR_TOP_N = 14;
const SIDEBAR_SECTION_ICONS = { 'Grammar topics': '📘', 'Skills': '🎯', 'Topic': '🏷️' };
const CHEVRON_SVG = '<svg viewBox="0 0 24 24"><polyline points="6 9 12 15 18 9"/></svg>';

function buildSidebar() {
  const aside = document.getElementById('sidebar');
  if (!aside) return;
  let html = `<div class="sidebar-mobile-header"><span>Browse topics</span><button type="button" class="sidebar-mobile-close" aria-label="Close">✕</button></div>`;
  for (const section of SIDEBAR_SECTIONS) {
    // Score every item by real demand (total downloads across its matched
    // worksheets), not just whether it has any — a flat 40+ item list is
    // choice paralysis, so only "Grammar topics" (the section big enough to
    // need it) leads with what teachers actually download most and tucks
    // the long tail behind a toggle instead of dumping it all inline.
    let scored = section.items.map(item => {
      const matched = item.cat
        ? allWorksheets.filter(w => (w.category || '').toLowerCase() === item.cat.toLowerCase())
        : allWorksheets.filter(w => wsMatchesTerms(w, item.match));
      const downloads = matched.reduce((sum, w) => sum + (w.downloads || 0), 0);
      return { item, count: matched.length, downloads };
    }).filter(s => s.count > 0);

    const curate = section.title === 'Grammar topics' && scored.length > SIDEBAR_TOP_N;
    if (curate) scored = [...scored].sort((a, b) => b.downloads - a.downloads);
    const visible = curate ? scored.slice(0, SIDEBAR_TOP_N) : scored;
    const hidden  = curate ? scored.slice(SIDEBAR_TOP_N) : [];

    // Real crawlable href (same ?cat=/?topic= scheme as syncUrl) so search
    // engines can follow and index these filtered views, not just JS clicks.
    // The top 3 of a curated (popularity-sorted) list get a flame instead of
    // a plain count — makes the "sorted by real demand" idea visible at a
    // glance rather than only implied by list order.
    const renderItem = (s, i) => {
      const item = s.item;
      const payload = item.cat ? `data-cat="${item.cat}"` : `data-match="${item.match.join('|')}"`;
      const href = item.cat
        ? `workshido-index.html?cat=${encodeURIComponent(item.cat)}`
        : `workshido-index.html?topic=${encodeURIComponent(item.match.join('|'))}`;
      const popular = curate && i < 3;
      return `<a href="${href}" class="sidebar-item${popular ? ' is-popular' : ''}" ${payload} data-label="${item.label}">
        <span class="sidebar-item-label">${item.label}</span>
        ${popular ? '<span class="sidebar-popular-mark">🔥</span>' : ''}
        <span class="sidebar-count">${s.count}</span>
      </a>`;
    };

    let itemsHtml = visible.map(renderItem).join('');
    if (hidden.length) {
      itemsHtml += `<div class="sidebar-more" hidden>${hidden.map(renderItem).join('')}</div>
        <button type="button" class="sidebar-toggle-more"><span class="sidebar-toggle-label">See all topics (${scored.length})</span>${CHEVRON_SVG}</button>`;
    }
    const icon = SIDEBAR_SECTION_ICONS[section.title] || '';
    if (itemsHtml) html += `<div class="sidebar-section"><div class="sidebar-title">${icon ? `<span class="sidebar-title-icon">${icon}</span>` : ''}${section.title}</div>${itemsHtml}</div>`;
  }
  aside.innerHTML = html || '<div class="sidebar-section"><div class="sidebar-title">No topics yet</div></div>';

  aside.querySelector('.sidebar-mobile-close')?.addEventListener('click', closeTopicsMobile);

  aside.querySelectorAll('.sidebar-toggle-more').forEach(btn => {
    const label = btn.querySelector('.sidebar-toggle-label');
    const collapsedText = label.textContent;
    btn.addEventListener('click', () => {
      const more = btn.previousElementSibling;
      const nowHidden = more.hasAttribute('hidden');
      if (nowHidden) { more.removeAttribute('hidden'); label.textContent = 'Show fewer topics'; btn.classList.add('expanded'); }
      else { more.setAttribute('hidden', ''); label.textContent = collapsedText; btn.classList.remove('expanded'); }
    });
  });

  aside.querySelectorAll('.sidebar-item').forEach(item => {
    item.addEventListener('click', e => {
      e.preventDefault();
      const isActive = item.classList.contains('active');
      aside.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));
      if (isActive) {            // clicking the active topic clears it
        activeTopic = 'all'; activeTopicLabel = '';
        activeCategory = 'all';
        syncCategoryChips();
      } else {
        item.classList.add('active');
        if (item.dataset.cat) {  // skill items filter by category
          activeCategory = item.dataset.cat;
          activeTopic = 'all'; activeTopicLabel = item.dataset.label;
          syncCategoryChips();
        } else {
          activeTopic = item.dataset.match.split('|');
          activeTopicLabel = item.dataset.label;
          activeCategory = 'all';   // a topic is a cross-category view
          syncCategoryChips();
        }
      }
      resetSearch();
      syncUrl();
      filterAndRender();
      closeTopicsMobile();
      document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
    });
  });
}

// Mobile: the sidebar renders as a slide-in drawer instead of the sticky
// desktop column (see the @media (max-width:768px) rules), opened from the
// "Browse topics" button that replaces it in that breakpoint.
function openTopicsMobile() {
  document.getElementById('sidebar')?.classList.add('mobile-open');
  document.getElementById('sidebarBackdrop')?.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeTopicsMobile() {
  document.getElementById('sidebar')?.classList.remove('mobile-open');
  document.getElementById('sidebarBackdrop')?.classList.remove('open');
  document.body.style.overflow = '';
}

function syncLevelChips() {
  document.querySelectorAll('.chip[data-level]').forEach(c =>
    c.classList.toggle('active', c.dataset.level === activeLevel || (activeLevel === 'all' && c.dataset.level === 'all')));
}
function syncCategoryChips() {
  document.querySelectorAll('.chip[data-cat]').forEach(c =>
    c.classList.toggle('active', !Array.isArray(activeCategory) && c.dataset.cat.toLowerCase() === String(activeCategory).toLowerCase()));
}

// Reflect the current filters in the URL (replaceState — no new history entries,
// no reload) so the Back button from a worksheet page returns to this same filtered view.
function syncUrl() {
  const params = new URLSearchParams();
  if (activeCategory !== 'all' && !Array.isArray(activeCategory)) params.set('cat', activeCategory);
  if (activeLevel !== 'all') params.set('level', activeLevel);
  if (activeTopic !== 'all') {
    const terms = Array.isArray(activeTopic) ? activeTopic : [activeTopic];
    params.set('topic', terms.join('|'));
  }
  if (searchQuery) params.set('q', searchQuery);
  const sort = document.getElementById('sortSelect')?.value;
  if (sort && sort !== 'newest') params.set('sort', sort);
  if (currentPage > 1) params.set('page', currentPage);
  const qs = params.toString();
  history.replaceState(null, '', window.location.pathname + (qs ? '?' + qs : ''));
}

function composeTitle() {
  const parts = [];
  if (activeTopicLabel) parts.push(activeTopicLabel);
  else if (activeCategory !== 'all') parts.push(Array.isArray(activeCategory) ? 'Skills' : activeCategory);
  if (activeLevel !== 'all') parts.push(activeLevel);
  if (searchQuery) parts.push(`"${searchQuery}"`);
  const title = document.getElementById('contentTitle');
  if (title) {
    const sort = document.getElementById('sortSelect')?.value;
    title.textContent = parts.length ? parts.join(' · ') : (sort === 'downloads' ? 'Most downloaded worksheets' : 'Latest worksheets');
  }
}

function clearFilters() {
  activeLevel = 'all'; activeCategory = 'all'; activeTopic = 'all'; activeTopicLabel = ''; searchQuery = '';
  const input = document.querySelector('.search-box input');
  if (input) input.value = '';
  const mini = document.getElementById('miniSearchInput');
  if (mini) mini.value = '';
  document.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));
  syncLevelChips(); syncCategoryChips();
  syncUrl();
  filterAndRender();
}

// Catalog cards show downloads, not star ratings — most worksheets have no
// ratings yet, so stars would mostly read as a generic "New" badge across
// the whole grid. Downloads are populated for nearly every worksheet and
// give a faster trust signal when scanning many cards at once. The detailed
// star rating still lives on the individual worksheet page.
function catalogRatingHtml(ws) {
  if (!ws.downloads) return `<span class="badge-new">🆕 New</span>`;
  return `<span class="reviews">↓ ${ws.downloads} download${ws.downloads === 1 ? '' : 's'}</span>`;
}

// Worksheet title/tags/category are free text set at upload time — never trust
// them as safe HTML when building cards from the catalog.
function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

// Category badge for a card — same "Practice" split used for the level rows
// above (drill-style worksheets are stored as Grammar in the DB, so a title
// match takes them out of the Grammar bucket and into their own), and the
// same color-per-category the worksheet detail page's related cards use.
const CARD_CAT_CLASS = { Grammar: 'cat-grammar', Reading: 'cat-reading', Writing: 'cat-writing', Vocabulary: 'cat-vocabulary', Speaking: 'cat-speaking', Practice: 'cat-practice' };
function cardCategory(ws) {
  if (wsMatchesTerms(ws, ['practice'])) return 'Practice';
  return ws.category || '';
}

function buildCard(ws) {
  const color  = LEVEL_COLORS[ws.level] || 'teal';
  const lvlCls = LEVEL_CLASS[ws.level]  || 'a1';
  const accent = ACCENT[ws.level]        || 'accent-teal';
  const badge  = ws.is_free ? '<span class="badge-type free">Free</span>' : '<span class="badge-type premium">Premium</span>';
  const cat    = cardCategory(ws);
  const catBadge = cat ? `<span class="badge-cat ${CARD_CAT_CLASS[cat] || ''}">${esc(cat)}</span>` : '';
  const btn    = ws.is_free
    ? `<a href="workshido-worksheet.html?id=${ws.id}" class="btn-download" style="text-decoration:none;">↓ Download</a>`
    : `<a href="workshido-worksheet.html?id=${ws.id}" class="btn-download locked" style="text-decoration:none;">🔒 Unlock</a>`;
  const tags   = (ws.tags || ws.category || '').split(',').slice(0,2).map(t=>`<span class="tag">${esc(t.trim())}</span>`).join('');
  const thumb = ws.thumbnail_url
    ? `<img src="${smThumb(ws.thumbnail_url)}" onerror="this.onerror=null;this.src='${ws.thumbnail_url}'" alt="${esc(ws.title)}" loading="lazy" decoding="async" width="440" height="622">`
    : `<div class="ws-preview"><div class="wl ${accent}"></div><div class="wl"></div><div class="wl short"></div><div class="wb"></div><div class="wb"></div><div class="wl short"></div></div>`;
  const overlay = !ws.thumbnail_url ? `<div class="card-thumb-overlay"><span class="overlay-logo">Work<span>shido</span></span><span class="overlay-level ${lvlCls}">${ws.level}</span></div>` : '';
  return `<div class="ws-card">
    <a href="workshido-worksheet.html?id=${ws.id}" class="card-thumb ${color}" style="display:block;text-decoration:none;">${thumb}${overlay}</a>
    <div class="card-body">
      <div class="card-meta"><span class="badge-level ${lvlCls}">${ws.level}</span>${badge}${catBadge}</div>
      <a href="workshido-worksheet.html?id=${ws.id}" class="card-title" style="text-decoration:none;color:inherit;">${esc(ws.title)}</a>
      <div class="card-tags">${tags}</div>
      <div class="card-footer">
        <div class="card-rating">${catalogRatingHtml(ws)}</div>
        ${btn}
      </div>
    </div>
  </div>`;
}


function renderCards(pageData, total) {
  const grid  = document.getElementById('cardGrid');
  const label = document.getElementById('catalogLabel');
  const count = document.getElementById('contentCount');
  if (!pageData || pageData.length === 0) {
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:60px 0;color:var(--gray-300);font-size:14px;">No worksheets match your filters.<br><br><button onclick="clearFilters()" style="background:var(--blue-600);color:#fff;border:none;border-radius:6px;padding:9px 20px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;">Clear all filters</button></div>';
    label.textContent = 'No worksheets found';
    if (count) count.textContent = '';
    renderPagination(0);
    return;
  }
  const txt = `${total} worksheet${total !== 1 ? 's' : ''}`;
  label.textContent = searchBroadenedFromLevel
    ? `No ${searchBroadenedFromLevel} results for "${searchQuery}" — showing ${txt} from all levels`
    : txt + ' available';
  if (count) count.textContent = txt;
  grid.innerHTML = pageData.map(buildCard).join('');
  renderPagination(total);
}

// Renders only PAGE_SIZE cards at a time instead of the full filtered set —
// with 252+ worksheets, building every card/image up front bloated the DOM
// to 4,000+ nodes and loaded far more thumbnails than a visitor ever sees.
function renderPage() {
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageData = _lastFiltered.slice(start, start + PAGE_SIZE);
  renderCards(pageData, _lastFiltered.length);
}

function renderPagination(total) {
  const el = document.getElementById('pagination');
  if (!el) return;
  const pageCount = Math.ceil(total / PAGE_SIZE);
  if (pageCount <= 1) { el.style.display = 'none'; el.innerHTML = ''; return; }
  el.style.display = 'flex';
  const btn = (label, page, opts = {}) =>
    `<button class="page-btn${opts.active ? ' active' : ''}" ${opts.disabled ? 'disabled' : ''} onclick="goToPage(${page})" aria-label="${opts.ariaLabel || `Page ${label}`}" ${opts.active ? 'aria-current="page"' : ''}>${label}</button>`;
  let html = btn('‹', currentPage - 1, { disabled: currentPage === 1, ariaLabel: 'Previous page' });
  const windowSize = 2;
  for (let p = 1; p <= pageCount; p++) {
    if (p === 1 || p === pageCount || (p >= currentPage - windowSize && p <= currentPage + windowSize)) {
      html += btn(p, p, { active: p === currentPage });
    } else if (p === currentPage - windowSize - 1 || p === currentPage + windowSize + 1) {
      html += '<span class="page-ellipsis">…</span>';
    }
  }
  html += btn('›', currentPage + 1, { disabled: currentPage === pageCount, ariaLabel: 'Next page' });
  el.innerHTML = html;
}

function goToPage(page) {
  const pageCount = Math.ceil(_lastFiltered.length / PAGE_SIZE);
  if (page < 1 || page > pageCount || page === currentPage) return;
  currentPage = page;
  // Keep ?page= in sync so the Back button from a worksheet opened on page 4
  // returns to page 4, not page 1 — filters were already preserved this way,
  // the page number was the one thing missing.
  syncUrl();
  renderPage();
  document.getElementById('cardGrid')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Edit distance between two short words, capped so a couple of typos (one
// swapped/missing/extra letter) still counts as a match without turning
// unrelated words into false positives.
function levenshtein(a, b) {
  const m = a.length, n = b.length;
  if (Math.abs(m - n) > 2) return 3; // early out, lengths too far apart to matter
  const prev = new Array(n + 1);
  for (let j = 0; j <= n; j++) prev[j] = j;
  for (let i = 1; i <= m; i++) {
    let cur = [i];
    for (let j = 1; j <= n; j++) {
      cur[j] = a[i - 1] === b[j - 1]
        ? prev[j - 1]
        : 1 + Math.min(prev[j - 1], prev[j], cur[j - 1]);
    }
    prev.splice(0, prev.length, ...cur);
  }
  return prev[n];
}

// Whether a single catalog word (from a title/tag) should count as matching
// a single search token — covers exact match, shared root ("transport" /
// "transportation" — one word starting with the other), and small typos
// ("trasportation" for "transportation") via edit distance.
function wsWordMatches(word, token) {
  if (!word || !token) return false;
  if (word === token) return true;
  if (token.length >= 3 && (word.startsWith(token) || token.startsWith(word))) return true;
  if (token.length >= 4) {
    const maxDist = token.length >= 8 ? 2 : 1;
    if (levenshtein(word, token) <= maxDist) return true;
  }
  return false;
}

// Whether a search token appears (exactly, by root, or with a small typo)
// anywhere among the words of a haystack string.
function wsFuzzyIncludes(hay, token) {
  return hay.split(/[\s,/–—-]+/).some(w => wsWordMatches(w, token));
}

// Every filter except level — factored out so a level-scoped search that
// comes up empty (see filterAndRender) can be retried against the whole
// catalog with the same category/topic/search logic, level just dropped.
function applyNonLevelFilters(base) {
  let filtered = base;
  if (activeCategory !== 'all') {
    const cats = Array.isArray(activeCategory) ? activeCategory.map(c => c.toLowerCase()) : [activeCategory.toLowerCase()];
    filtered = filtered.filter(w => cats.includes((w.category || '').toLowerCase()));
  }
  if (activeTopic !== 'all') {
    const terms = Array.isArray(activeTopic) ? activeTopic : [activeTopic];
    filtered = filtered.filter(w => wsMatchesTerms(w, terms));
  }
  if (searchQuery) {
    // Match on WORDS, not the query as one glued-together phrase — "past
    // simple tense" used to require that exact 3-word string verbatim, so it
    // only matched a worksheet literally titled "Past Simple Tense" and
    // dropped "Past Simple Grammar", "Past Simple Vocabulary", etc.
    const tokens = searchQuery.toLowerCase().split(/\s+/).filter(Boolean);
    // For short queries (1-2 words — the common case for a specific grammar
    // term) require EVERY word to fuzzy-match (root or small typo) somewhere
    // in title/tags/category, not the free-text description. Matching tokens
    // independently against a blob that includes descriptions let unrelated
    // topics sneak in — e.g. "present" (from "Present Perfect") + "simple"
    // (from "Past Simple") both appearing somewhere on "Present Perfect vs.
    // Past Simple", or a Conditional worksheet's description that explains
    // "if + present simple" in passing. Longer queries keep the looser
    // per-token majority match below, since an extra descriptive word (like
    // "tense") shouldn't silently exclude the whole topic.
    if (tokens.length <= 2) {
      filtered = filtered.filter(w => {
        const hay = [w.title, w.tags, w.category].filter(Boolean).join(' ').toLowerCase();
        return tokens.every(t => wsFuzzyIncludes(hay, t));
      });
    } else {
      const threshold = Math.floor(tokens.length / 2) + 1;
      filtered = filtered.filter(w => {
        const hay = [w.title, w.tags, w.category, w.description].filter(Boolean).join(' ').toLowerCase();
        return tokens.filter(t => wsFuzzyIncludes(hay, t)).length >= threshold;
      });
    }
  }
  return filtered;
}

function filterAndRender() {
  let filtered = activeLevel !== 'all' ? allWorksheets.filter(w => w.level === activeLevel) : allWorksheets;
  filtered = applyNonLevelFilters(filtered);

  // A level filter should scope results, never make a real topic look like
  // it doesn't exist just because it hasn't reached that level yet — e.g.
  // searching "reported speech"/"passive voice" while browsing A1 used to
  // say "No worksheets match your filters" even though those topics exist
  // (just starting at a higher level), which reads as "this doesn't exist
  // on the site" rather than "not at A1". If a level-scoped search comes up
  // empty, drop the level and search the whole catalog instead — each
  // result card still shows its own level badge, so it's clear where it's
  // actually found (e.g. B2).
  searchBroadenedFromLevel = '';
  if (searchQuery && filtered.length === 0 && activeLevel !== 'all') {
    searchBroadenedFromLevel = activeLevel;
    activeLevel = 'all';
    syncLevelChips();
    syncUrl();
    filtered = applyNonLevelFilters(allWorksheets);
  }

  const sort = document.getElementById('sortSelect')?.value || 'newest';
  const sortSecondary = (a, b) => {
    if (sort === 'newest') {
      const da = a.created_at ? new Date(a.created_at).getTime() : 0;
      const db = b.created_at ? new Date(b.created_at).getTime() : 0;
      return db - da;
    }
    return (b.downloads || 0) - (a.downloads || 0);
  };
  if (searchQuery) {
    const q = searchQuery.toLowerCase();
    filtered = [...filtered].sort((a, b) => {
      const diff = wsRelevanceScore(b, q) - wsRelevanceScore(a, q);
      return diff !== 0 ? diff : sortSecondary(a, b);
    });
  } else if (activeTopic !== 'all') {
    // Same relevance ranking as free-text search, keyed off the topic's own
    // match terms — otherwise a worksheet whose core topic IS "Present
    // continuous" ties on sortSecondary (newest/downloads) with one that only
    // carries "present continuous" as a cross-reference tag (e.g. a Future
    // Forms worksheet comparing it to "will"/"going to"), and a newer tag-only
    // match buries the actually-on-topic worksheet.
    const terms = (Array.isArray(activeTopic) ? activeTopic : [activeTopic]).map(t => t.toLowerCase());
    const topicScore = w => Math.max(...terms.map(t => wsRelevanceScore(w, t)));
    filtered = [...filtered].sort((a, b) => {
      const diff = topicScore(b) - topicScore(a);
      return diff !== 0 ? diff : sortSecondary(a, b);
    });
  } else {
    filtered = [...filtered].sort(sortSecondary);
  }
  composeTitle();
  _lastFiltered = filtered;
  currentPage = 1;
  const latestRows   = document.getElementById('latestRows');
  const cardGrid      = document.getElementById('cardGrid');
  const catalogLabel  = document.getElementById('catalogLabel');
  const pagination    = document.getElementById('pagination');
  const contentCount  = document.getElementById('contentCount');
  if (isDefaultView()) {
    // Landing with no filter/search active: show curated "latest per group"
    // rows instead of one flat newest-first list of the whole catalog.
    if (latestRows)  latestRows.style.display = '';
    if (cardGrid)     cardGrid.style.display = 'none';
    if (catalogLabel) catalogLabel.style.display = 'none';
    if (pagination)   pagination.style.display = 'none';
    if (contentCount) contentCount.textContent = `${filtered.length} worksheet${filtered.length !== 1 ? 's' : ''}`;
    renderLatestRows();
  } else if (isLevelOnlyView()) {
    // Same idea, one level deep: a level with no category/topic/search yet
    // shows its own "latest 5 per category" rows instead of jumping
    // straight to one flat paginated list of every category mixed together.
    if (latestRows)  latestRows.style.display = '';
    if (cardGrid)     cardGrid.style.display = 'none';
    if (catalogLabel) catalogLabel.style.display = 'none';
    if (pagination)   pagination.style.display = 'none';
    if (contentCount) contentCount.textContent = `${filtered.length} worksheet${filtered.length !== 1 ? 's' : ''}`;
    renderLevelRows(activeLevel);
  } else {
    if (latestRows)  latestRows.style.display = 'none';
    if (cardGrid)     cardGrid.style.display = '';
    if (catalogLabel) catalogLabel.style.display = '';
    renderPage();
  }
}

// Titles follow "{Topic} – {Type}" (e.g. "Present Perfect Tense – Grammar",
// "Present Perfect vs. Past Simple – Writing"). The part after the dash is
// the worksheet type (already scored separately via category), not the
// topic, and a couple of generic descriptor words add no topic information
// of their own ("Present Perfect Tense" IS "Present Perfect"). Stripped here
// so the relevance score below can tell "this worksheet's topic almost
// exactly IS the query" apart from "this worksheet's topic merely starts
// with the query's words before continuing into a different one" — e.g. a
// "present perfect" search used to give "Present Perfect Continuous" and
// "Present Perfect vs. Past Simple" the exact same flat title bonus as the
// actual "Present Perfect" worksheet (both are literal string prefixes of
// "present perfect"), leaving only recency to break the tie and burying the
// one worksheet that IS the query's topic under newer, more specific ones.
const TOPIC_FILLER_WORDS = new Set(['tense']);
function wsCoreTopic(title) {
  const dash = title.search(/[–—-]/);
  const topic = dash >= 0 ? title.slice(0, dash) : title;
  return topic.replace(/[():,.&]/g, ' ').split(/\s+/).filter(w => w && !TOPIC_FILLER_WORDS.has(w)).join(' ').trim();
}

// Ranks a worksheet's relevance to a search query: exact title match scores
// highest so a worksheet's core topic always outranks one that merely
// mentions the term in a secondary tag (e.g. "past simple" as a cross-
// reference tag on a Past Continuous worksheet).
function wsRelevanceScore(w, q) {
  const title = (w.title || '').toLowerCase();
  const tags = (w.tags || '').toLowerCase();
  const category = (w.category || '').toLowerCase();
  const description = (w.description || '').toLowerCase();
  let score = 0;
  const topic = wsCoreTopic(title);
  if (title === q || topic === q) {
    score += 200;
  } else if (title.startsWith(q) || topic.startsWith(q)) {
    // Dilute by how much real topic content trails the match — "present
    // perfect" fully covers the "Present Perfect" worksheet's topic (no
    // leftover, full 140) but only partially covers "Present Perfect
    // Continuous" (1 leftover word) or "Present Perfect vs. Past Simple" (3
    // leftover words), so those score progressively lower instead of tying.
    const base = topic.startsWith(q) ? topic : title;
    const extraWords = base.slice(q.length).trim().split(/\s+/).filter(Boolean).length;
    score += Math.max(20, 140 - extraWords * 40);
  } else {
    // Weight by position: a match right at the start of the title ("Present
    // Simple – Grammar") should outrank one buried inside a differently-named
    // topic ("Passive Voice in Present Simple", "Reported Speech: Present
    // Simple to Past Simple") — those are legitimate related results, but the
    // worksheet's own topic isn't the query, so they shouldn't outrank
    // worksheets whose core topic actually is.
    const idx = title.indexOf(q);
    if (idx >= 0) score += Math.max(20, 100 - idx * 3);
  }
  if (tags.includes(q)) {
    const idx = tags.indexOf(q);
    score += Math.max(10, 45 - Math.floor(idx / 4));
  }
  if (category.includes(q)) score += 15;
  if (description.includes(q)) score += 5;
  // Per-word credit: rewards how many of the query's individual words show up
  // and where, so "past simple tense" still ranks "Past Simple Grammar" (2/3
  // words in the title) above something that only matches in the description.
  // Uses fuzzy (root/typo-tolerant) matching so a single-word query like
  // "transportation" still gets scored against a "transport" tag, or a typo
  // like "trasportation" against results found only via wsFuzzyIncludes.
  const tokens = q.split(/\s+/).filter(Boolean);
  {
    tokens.forEach(t => {
      if (wsFuzzyIncludes(title, t)) score += 8;
      if (wsFuzzyIncludes(tags, t)) score += 4;
      if (wsFuzzyIncludes(category, t)) score += 2;
      if (wsFuzzyIncludes(description, t)) score += 1;
    });
  }
  // Recency nudge: among worksheets that match the topic about equally well,
  // surface newer ones first. Decays linearly to 0 over a year so it can't
  // outweigh a real relevance gap (e.g. an exact title match vs. a tag-only
  // mention), it only breaks near-ties in favor of the newest worksheet.
  if (w.created_at) {
    const daysOld = (Date.now() - new Date(w.created_at).getTime()) / 86400000;
    score += Math.max(0, 20 * (1 - daysOld / 365));
  }
  return score;
}

function setCategory(cat) {
  activeCategory = cat;
  activeTopic = 'all'; activeTopicLabel = '';
  document.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));
  syncCategoryChips();
  resetSearch();
  syncUrl();
  document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
  filterAndRender();
}

async function loadWorksheets() {
  // Only the columns the catalog list/cards/search actually use — not select('*').
  // Drops file_url, teacher_edition_url, topic_key, rating, uploader_* … which
  // cut the payload for ~700 rows from ~690 KB to ~450 KB.
  const COLS = 'id,title,level,category,tags,thumbnail_url,is_free,downloads,description,created_at';
  const { data, error } = await sb2.from('worksheets').select(COLS).order('created_at', { ascending: false, nullsFirst: false }).limit(1000);
  if (error) {
    document.getElementById('cardGrid').innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:60px 0;color:var(--gray-300);font-size:14px;">Could not load worksheets.</div>';
    return;
  }
  allWorksheets = data || [];
  updateLiveStats();
  buildSidebar();
  filterAndRender();
}

// ── Live numbers from the catalog. Rounds down to the nearest 100 ("700+",
//    "800+", …) — never overstated, steps up every 100 uploads. ──
function milestoneCount(n) {
  return Math.max(100, Math.floor(n / 100) * 100).toLocaleString('en-US') + '+';
}
function updateLiveStats() {
  const n = allWorksheets.length;
  if (!n) return;
  const rounded = milestoneCount(n);
  const elCount = document.getElementById('statWorksheets');
  if (elCount) elCount.textContent = rounded;
  const eyebrow = document.getElementById('heroEyebrowText');
  if (eyebrow) eyebrow.textContent = `${rounded} free worksheets · Print-ready PDFs · New resources every week`;
  // CEFR range actually covered by the catalog
  const order = ['A1', 'A2', 'B1', 'B2', 'C1'];
  const present = order.filter(l => allWorksheets.some(w => w.level === l));
  const elLevels = document.getElementById('statLevels');
  if (elLevels && present.length) {
    elLevels.textContent = present.length > 1 ? `${present[0]}–${present[present.length - 1]}` : present[0];
  }
  // Hide level chips that have no worksheets yet — they reappear as the catalog grows
  document.querySelectorAll('.chip[data-level]').forEach(chip => {
    if (chip.dataset.level === 'all') return;
    chip.style.display = allWorksheets.some(w => w.level === chip.dataset.level) ? '' : 'none';
  });
}

// ── Chip filters (level and category combine, they don't reset each other) ──
document.querySelectorAll('.chip[data-level]').forEach(chip => {
  chip.addEventListener('click', () => {
    activeLevel = (chip.dataset.level === activeLevel) ? 'all' : chip.dataset.level;
    syncLevelChips();
    resetSearch();
    syncUrl();
    filterAndRender();
    document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
  });
});
document.querySelectorAll('.chip[data-cat]').forEach(chip => {
  chip.addEventListener('click', () => {
    const isSame = String(activeCategory).toLowerCase() === chip.dataset.cat.toLowerCase();
    activeCategory = isSame ? 'all' : chip.dataset.cat;
    activeTopic = 'all'; activeTopicLabel = '';
    document.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));
    syncCategoryChips();
    resetSearch();
    syncUrl();
    filterAndRender();
    document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
  });
});

// ── Search (client-side over the full catalog, loaded up to 1000 rows) ──
// Two inputs share one query: the hero search box and the compact sticky
// one in the results toolbar (visible once the hero scrolls out of view).
let searchTimer;
const searchInput = document.querySelector('.search-box input');
const miniSearchInput = document.getElementById('miniSearchInput');

// `source` = el input donde el usuario está escribiendo, si lo hay. Nunca se le
// reasigna el .value: hacerlo manda el cursor al final y, como aquí se guarda la
// versión con trim(), se comía el espacio recién tecleado — escribir
// "present simple" terminaba como "presentsimple". El otro input sí se sincroniza.
function runSearch(value, source) {
  searchQuery = value.trim();
  if (source !== searchInput && searchInput.value !== searchQuery) searchInput.value = searchQuery;
  if (source !== miniSearchInput && miniSearchInput.value !== searchQuery) miniSearchInput.value = searchQuery;
  // A search is an intent to look across the whole catalog — a leftover topic/category
  // filter from wherever the user was browsing (e.g. a "Present Simple" topic view) would
  // otherwise silently AND with the query and could hide every result (searching "present
  // perfect" while still scoped to "Present Simple" matches nothing, with no clue why).
  if (searchQuery && (activeTopic !== 'all' || activeCategory !== 'all')) {
    activeTopic = 'all'; activeTopicLabel = '';
    activeCategory = 'all';
    document.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));
    syncCategoryChips();
  }
  syncUrl();
  filterAndRender();
  if (searchQuery) window.wsTrack?.('search_submitted', { query: searchQuery, results: _lastFiltered.length });
}

searchInput.addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => runSearch(searchInput.value, searchInput), 400);
});
miniSearchInput.addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => runSearch(miniSearchInput.value, miniSearchInput), 400);
});

document.querySelector('.search-box button').addEventListener('click', () => {
  runSearch(searchInput.value);
  document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
});
searchInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    runSearch(searchInput.value);
    document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
  }
});
miniSearchInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') runSearch(miniSearchInput.value);
});

document.getElementById('sortSelect').addEventListener('change', () => { syncUrl(); filterAndRender(); });

// Reload on back/forward navigation to avoid stale auth state from bfcache
window.addEventListener('pageshow', (e) => { if (e.persisted) window.location.reload(); });

document.getElementById('yr').textContent = new Date().getFullYear();
function openMobileMenu()  { document.getElementById('mobileMenu').classList.add('open'); document.body.style.overflow = 'hidden'; }
function closeMobileMenu() { document.getElementById('mobileMenu').classList.remove('open'); document.body.style.overflow = ''; }

// Anonymous homepage lead capture — separate from the logged-in marketing
// consent banner (marketing-consent.js, which only fires for existing
// accounts). Public insert-only table (email_leads), no auth required.
const EMAIL_CAPTURE_CONSENT_VERSION = 'v1';
function initEmailCapture() {
  const form = document.getElementById('ecForm');
  if (!form) return;
  const status = document.getElementById('ecStatus');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('ecEmail').value.trim();
    const consent = document.getElementById('ecConsent').checked;
    if (!consent) {
      status.textContent = 'Please check the box to agree to receive emails.';
      status.className = 'email-capture-status err';
      return;
    }
    const btn = document.getElementById('ecBtn');
    btn.disabled = true;
    btn.textContent = 'Subscribing…';
    const { error } = await sb2.from('email_leads').insert({
      email, source: 'catalog', consent_version: EMAIL_CAPTURE_CONSENT_VERSION,
    });
    btn.disabled = false;
    btn.textContent = 'Subscribe free';
    if (error) {
      // Unique index on lower(email) — a repeat signup is not a real error.
      if (error.code === '23505') {
        status.textContent = "You're already on the list!";
        status.className = 'email-capture-status ok';
        form.reset();
        return;
      }
      status.textContent = 'Something went wrong — please try again.';
      status.className = 'email-capture-status err';
      return;
    }
    status.textContent = "You're in! Watch your inbox for new worksheets.";
    status.className = 'email-capture-status ok';
    form.reset();
  });
}

document.addEventListener('DOMContentLoaded', () => {
  checkAuth2();
  initEmailCapture();
  loadWorksheets().then(() => {
    const params = new URLSearchParams(window.location.search);
    const cat   = params.get('cat');
    const level = params.get('level');
    const topic = params.get('topic');
    const q     = params.get('q');
    const sort  = params.get('sort');
    const page  = parseInt(params.get('page'), 10);
    if (sort) { const sel = document.getElementById('sortSelect'); if (sel) sel.value = sort; }
    if (cat) { activeCategory = cat; syncCategoryChips(); }
    if (level) { activeLevel = level.toUpperCase(); syncLevelChips(); }
    if (topic) {
      activeTopic = topic.split('|');
      activeTopicLabel = activeTopic[0].charAt(0).toUpperCase() + activeTopic[0].slice(1);
      // highlight the matching sidebar item if one exists (also picks up its full label/match list)
      document.querySelectorAll('.sidebar-item[data-match]').forEach(s => {
        const itemTerms = s.dataset.match.toLowerCase().split('|');
        if (activeTopic.some(t => itemTerms.includes(t.toLowerCase()))) {
          s.classList.add('active');
          activeTopicLabel = s.dataset.label;
        }
      });
    }
    if (q) {
      searchQuery = q;
      const input = document.querySelector('.search-box input');
      if (input) input.value = q;
      const mini = document.getElementById('miniSearchInput');
      if (mini) mini.value = q;
    }
    if (cat || level || topic || q || sort) {
      filterAndRender();
      // Arriving here via a nav button/chip/search from another page (or a
      // shared/bookmarked filtered link) means the user already expressed
      // intent — land them on the results instead of the hero, which on
      // mobile pushes results below several screens of marketing content.
      document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
    }
    // filterAndRender() always resets to page 1, so restore the saved page
    // afterward (e.g. returning via Back from a worksheet opened on page 4).
    if (page > 1) {
      const pageCount = Math.ceil(_lastFiltered.length / PAGE_SIZE);
      if (page <= pageCount) { currentPage = page; renderPage(); }
    }
  });
});