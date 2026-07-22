const sb2 = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');

// ── Auth state — updated instantly from localStorage via onAuthStateChange ──
let wsCurrentUser = null;

function updateNav2(user) {
  const uploadLink = document.getElementById('navUploadLink');
  if (uploadLink) uploadLink.style.display = (user?.email === 'juanda.5790@hotmail.com') ? '' : 'none';
  const nav = document.getElementById('navActions');
  if (!nav) return;
  if (user) {
    const name = user.user_metadata?.full_name || user.email;
    const initials = name.split(' ').map(n=>n[0]).join('').toUpperCase().slice(0,2);
    // full_name is free text the user set at signup — never trust it as safe
    // HTML when it lands back in innerHTML.
    const escNav = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    nav.innerHTML = '<a href="workshido-profile.html" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:#B5D4F4;font-size:13px;font-weight:500;"><div style="width:32px;height:32px;border-radius:50%;background:#E6F1FB;color:#185FA5;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;border:2px solid #85B7EB;">'+escNav(initials)+'</div>'+escNav(name.split(' ')[0])+'</a><button onclick="logOut2()" style="background:transparent;border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:7px 14px;color:#B5D4F4;font-size:13px;cursor:pointer;font-family:inherit;">Log out</button>';
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

let allWorksheets = [];
const PAGE_SIZE = 24;
let currentPage = 1;
let _lastFiltered = [];
let activeLevel = 'all';
let activeCategory = 'all';
let activeTopic = 'all';      // 'all' | array of matcher terms
let activeTopicLabel = '';
let searchQuery = '';

// ── Sidebar definition: label + matcher terms against real tags/titles.
//    Items with 0 matching worksheets are hidden automatically.
const SIDEBAR_SECTIONS = [
  { title: 'Grammar topics', items: [
    { label: 'Verb to be',            match: ['verb to be', 'am is are'] },
    { label: 'Present simple',        match: ['present simple', 'presentsimple'] },
    { label: 'Present continuous',    match: ['present continuous'] },
    { label: 'Past simple',           match: ['past simple'] },
    { label: 'Future & going to',     match: ['going to', 'future simple', 'future plans', 'will'] },
    { label: 'Imperatives',           match: ['imperatives', 'commands'] },
    { label: 'Demonstratives',        match: ['demonstratives', 'this that these those'] },
    { label: 'Articles a/an/the',     match: ['articles', 'a an the'] },
    { label: 'Possessive adjectives', match: ['possessive adjectives', 'possessiveadjectives', 'possessives'] },
    { label: 'There is / There are',  match: ['there is there are', 'there is/are'] },
    { label: 'Prepositions of place', match: ['prepositions of place'] },
    { label: 'Have got / Has got',    match: ['have got'] },
    { label: 'Modal verbs (can)',     match: ['modal', 'can and can', "can & can"] },
    { label: 'Some & any',            match: ['some and any', 'some any'] },
    { label: 'Pronouns',              match: ['pronouns'] },
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

function buildSidebar() {
  const aside = document.getElementById('sidebar');
  if (!aside) return;
  let html = '';
  for (const section of SIDEBAR_SECTIONS) {
    let itemsHtml = '';
    for (const item of section.items) {
      const count = item.cat
        ? allWorksheets.filter(w => (w.category || '').toLowerCase() === item.cat.toLowerCase()).length
        : allWorksheets.filter(w => wsMatchesTerms(w, item.match)).length;
      if (count === 0) continue;
      const payload = item.cat ? `data-cat="${item.cat}"` : `data-match="${item.match.join('|')}"`;
      // Real crawlable href (same ?cat=/?topic= scheme as syncUrl) so search
      // engines can follow and index these filtered views, not just JS clicks.
      const href = item.cat
        ? `workshido-index.html?cat=${encodeURIComponent(item.cat)}`
        : `workshido-index.html?topic=${encodeURIComponent(item.match.join('|'))}`;
      itemsHtml += `<a href="${href}" class="sidebar-item" ${payload} data-label="${item.label}">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/></svg>
        ${item.label}<span class="sidebar-count">${count}</span>
      </a>`;
    }
    if (itemsHtml) html += `<div class="sidebar-section"><div class="sidebar-title">${section.title}</div>${itemsHtml}</div>`;
  }
  aside.innerHTML = html || '<div class="sidebar-section"><div class="sidebar-title">No topics yet</div></div>';

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
      syncUrl();
      filterAndRender();
      document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
    });
  });
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
  if (title) title.textContent = parts.length ? parts.join(' · ') : 'All worksheets';
}

function clearFilters() {
  activeLevel = 'all'; activeCategory = 'all'; activeTopic = 'all'; activeTopicLabel = ''; searchQuery = '';
  const input = document.querySelector('.search-box input');
  if (input) input.value = '';
  document.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));
  syncLevelChips(); syncCategoryChips();
  syncUrl();
  filterAndRender();
}

// Same source of truth as workshido-worksheet.html's star display: real
// ws.rating/ws.ratings_count, rounded to whole stars for the compact card
// (no ratings yet -> all empty, never a fake perfect score).
function catalogStars(ws) {
  const avg = ws.ratings_count ? (ws.rating || 0) : 0;
  const full = Math.round(avg);
  return '★'.repeat(full) + '☆'.repeat(5 - full);
}

// No ratings yet -> a neutral "New" badge instead of empty stars, which
// otherwise reads as "0/5, badly rated" rather than "not rated yet".
function catalogRatingHtml(ws) {
  if (!ws.ratings_count) return `<span class="badge-new">🆕 New</span>`;
  return `<span class="stars">${catalogStars(ws)}</span><span class="reviews">(${ws.downloads||0})</span>`;
}

// Worksheet title/tags/category are free text set at upload time — never trust
// them as safe HTML when building cards from the catalog.
function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

function buildCard(ws) {
  const color  = LEVEL_COLORS[ws.level] || 'teal';
  const lvlCls = LEVEL_CLASS[ws.level]  || 'a1';
  const accent = ACCENT[ws.level]        || 'accent-teal';
  const badge  = ws.is_free ? '<span class="badge-type free">Free</span>' : '<span class="badge-type premium">Premium</span>';
  const btn    = ws.is_free
    ? `<a href="workshido-worksheet.html?id=${ws.id}" class="btn-download" style="text-decoration:none;">↓ Download</a>`
    : `<a href="workshido-worksheet.html?id=${ws.id}" class="btn-download locked" style="text-decoration:none;">🔒 Unlock</a>`;
  const tags   = (ws.tags || ws.category || '').split(',').slice(0,2).map(t=>`<span class="tag">${esc(t.trim())}</span>`).join('');
  const thumb = ws.thumbnail_url
    ? `<img src="${ws.thumbnail_url}" alt="${esc(ws.title)}" loading="lazy">`
    : `<div class="ws-preview"><div class="wl ${accent}"></div><div class="wl"></div><div class="wl short"></div><div class="wb"></div><div class="wb"></div><div class="wl short"></div></div>`;
  const overlay = !ws.thumbnail_url ? `<div class="card-thumb-overlay"><span class="overlay-logo">Work<span>shido</span></span><span class="overlay-level ${lvlCls}">${ws.level}</span></div>` : '';
  return `<div class="ws-card">
    <a href="workshido-worksheet.html?id=${ws.id}" class="card-thumb ${color}" style="display:block;text-decoration:none;">${thumb}${overlay}</a>
    <div class="card-body">
      <div class="card-meta"><span class="badge-level ${lvlCls}">${ws.level}</span>${badge}</div>
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
  label.textContent = txt + ' available';
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
  renderPage();
  document.getElementById('cardGrid')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function filterAndRender() {
  let filtered = allWorksheets;
  if (activeLevel !== 'all') filtered = filtered.filter(w => w.level === activeLevel);
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
    // Requiring every token (strict AND) was still too narrow: those
    // worksheets have "past" and "simple" but nowhere say "tense", so they
    // still failed. Require a majority of tokens instead — for 1-2 words
    // (the common case, e.g. "past simple") every word must still match, but
    // 3+ word queries only need most of them, so an extra/descriptive word
    // like "tense" doesn't silently exclude the whole topic.
    const tokens = searchQuery.toLowerCase().split(/\s+/).filter(Boolean);
    const threshold = tokens.length <= 2 ? tokens.length : Math.floor(tokens.length / 2) + 1;
    filtered = filtered.filter(w => {
      const hay = [w.title, w.tags, w.category, w.description].filter(Boolean).join(' ').toLowerCase();
      return tokens.filter(t => hay.includes(t)).length >= threshold;
    });
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
  } else {
    filtered = [...filtered].sort(sortSecondary);
  }
  composeTitle();
  _lastFiltered = filtered;
  currentPage = 1;
  renderPage();
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
  if (title === q) score += 200;
  else if (title.startsWith(q)) score += 140;
  else if (title.includes(q)) score += 100;
  if (tags.includes(q)) {
    const idx = tags.indexOf(q);
    score += Math.max(10, 45 - Math.floor(idx / 4));
  }
  if (category.includes(q)) score += 15;
  if (description.includes(q)) score += 5;
  // Per-word credit: rewards how many of the query's individual words show up
  // and where, so "past simple tense" still ranks "Past Simple Grammar" (2/3
  // words in the title) above something that only matches in the description.
  const tokens = q.split(/\s+/).filter(Boolean);
  if (tokens.length > 1) {
    tokens.forEach(t => {
      if (title.includes(t)) score += 8;
      if (tags.includes(t)) score += 4;
      if (category.includes(t)) score += 2;
      if (description.includes(t)) score += 1;
    });
  }
  return score;
}

function setCategory(cat) {
  activeCategory = cat;
  activeTopic = 'all'; activeTopicLabel = '';
  document.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));
  syncCategoryChips();
  syncUrl();
  document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
  filterAndRender();
}

async function loadWorksheets() {
  const { data, error } = await sb2.from('worksheets').select('*').order('created_at', { ascending: false, nullsFirst: false }).limit(1000);
  if (error) {
    document.getElementById('cardGrid').innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:60px 0;color:var(--gray-300);font-size:14px;">Could not load worksheets.</div>';
    return;
  }
  allWorksheets = data || [];
  updateLiveStats();
  buildSidebar();
  filterAndRender();
}

// ── Live numbers from the catalog. The count rounds down to marketing
//    milestones (100+, 150+, 200+...), so it is never overstated past 100. ──
const COUNT_MILESTONES = [100, 150, 200, 300, 500, 750, 1000, 1500, 2000, 3000, 5000, 10000];
function milestoneCount(n) {
  let best = COUNT_MILESTONES[0];
  for (const m of COUNT_MILESTONES) if (n >= m) best = m;
  return best.toLocaleString('en-US') + '+';
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
    syncUrl();
    filterAndRender();
  });
});
document.querySelectorAll('.chip[data-cat]').forEach(chip => {
  chip.addEventListener('click', () => {
    const isSame = String(activeCategory).toLowerCase() === chip.dataset.cat.toLowerCase();
    activeCategory = isSame ? 'all' : chip.dataset.cat;
    activeTopic = 'all'; activeTopicLabel = '';
    document.querySelectorAll('.sidebar-item').forEach(s => s.classList.remove('active'));
    syncCategoryChips();
    syncUrl();
    filterAndRender();
  });
});

// ── Search (client-side over the full catalog, loaded up to 1000 rows) ──
let searchTimer;
const searchInput = document.querySelector('.search-box input');

function trackSearch() {
  if (searchQuery) window.wsTrack?.('search_submitted', { query: searchQuery, results: _lastFiltered.length });
}

searchInput.addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    searchQuery = searchInput.value.trim();
    syncUrl();
    filterAndRender();
    trackSearch();
  }, 400);
});

document.querySelector('.search-box button').addEventListener('click', () => {
  searchQuery = searchInput.value.trim();
  syncUrl();
  filterAndRender();
  trackSearch();
  document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
});
document.querySelector('.search-box input').addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    searchQuery = e.target.value.trim();
    syncUrl();
    filterAndRender();
    trackSearch();
    document.querySelector('.main-layout').scrollIntoView({ behavior: 'smooth' });
  }
});

document.getElementById('sortSelect').addEventListener('change', filterAndRender);

// Reload on back/forward navigation to avoid stale auth state from bfcache
window.addEventListener('pageshow', (e) => { if (e.persisted) window.location.reload(); });

document.getElementById('yr').textContent = new Date().getFullYear();
function openMobileMenu()  { document.getElementById('mobileMenu').classList.add('open'); document.body.style.overflow = 'hidden'; }
function closeMobileMenu() { document.getElementById('mobileMenu').classList.remove('open'); document.body.style.overflow = ''; }

document.addEventListener('DOMContentLoaded', () => {
  checkAuth2();
  loadWorksheets().then(() => {
    const params = new URLSearchParams(window.location.search);
    const cat   = params.get('cat');
    const level = params.get('level');
    const topic = params.get('topic');
    const q     = params.get('q');
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
    }
    if (cat || level || topic || q) filterAndRender();
  });
});