const sb2 = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
const LEVEL_COLOR = { A1:'teal', A2:'blue', B1:'amber', B2:'purple', C1:'coral' };
const LEVEL_CLS   = { A1:'a1',   A2:'a2',  B1:'b1',   B2:'b2',    C1:'c1'    };
const LEVELS = ['A1','A2','B1','B2','C1'];
const WS_COLS = 'id,slug,title,level,category,thumbnail_url,downloads,rating,ratings_count,is_free,created_at';
const GRID_PAGE = 24;   // "My worksheets" cards per "Show more"
const GRID_PREVIEW = 8; // saved / downloads cards before "Show all"

async function logOut(){ await sb2.auth.signOut(); window.location.href='workshido-index.html'; }

function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
// Same ~440px _sm thumbnail derivative the catalog cards use.
function smThumb(u) { return u && /\.webp(\?|$)/i.test(u) ? u.replace(/\.webp(\?|$)/i, '_sm.webp$1') : u; }
function wsHref(w) { return w.slug ? `/worksheet/${w.slug}/` : `/workshido-worksheet.html?id=${w.id}`; }
function fmtNum(n) { return (n || 0).toLocaleString('en-US'); }
function _norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
function _topKey(counts) { return Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] || '—'; }
function _setText(id, v) { const el = document.getElementById(id); if (el) el.textContent = v; }

let _isJuan = false;

async function loadProfile() {
  const { data: { user } } = await sb2.auth.getUser();
  if (!user) { window.location.href = 'workshido-login.html'; return; }

  // The uploader dashboard (catalog stats + "my worksheets") is Juan-only —
  // uploading is admin-only. Everyone else gets their own activity + plan.
  _isJuan = user.email === 'juanda.5790@hotmail.com';
  ['my-worksheets', 'tabMyWs', 'levelMixSection'].forEach(id => { const el = document.getElementById(id); if (el) el.hidden = !_isJuan; });
  ['subscriberOverview', 'exploreSection'].forEach(id => { const el = document.getElementById(id); if (el) el.hidden = _isJuan; });

  const emailChip = document.querySelector('.profile-email');
  if (emailChip) { emailChip.textContent = user.email; emailChip.title = user.email; }

  const { data } = await sb2
    .from('profiles')
    .select('marketing_consent, is_premium, lemon_portal_url, avatar, display_name, bio, teaches, created_at, is_public, public_slug')
    .eq('id', user.id)
    .maybeSingle();
  // One shared object: the editor's save mutates it, so the public-profile
  // toggle always sees the current display name.
  const profile = data || {};

  setupProfileCustomization(user, profile);
  setupEditorToggle();
  paintPlan(profile);
  setupMarketingToggle(profile);
  setupPublicToggle(user, profile);
  setupTabs();

  const [saved, dl] = await Promise.all([loadSavedWorksheets(), loadDownloadHistory()]);
  if (_isJuan) loadMyWorksheets();
  else paintSubscriberStats(saved, dl, profile);
}

// --- Hero: teaches / bio / member since / profile completion ---------------
function paintHero(user, profile) {
  const p = profile || {};
  const teaches = (p.teaches || '').trim();
  const bio = (p.bio || '').trim();
  const t = document.getElementById('heroTeaches');
  const b = document.getElementById('heroBio');
  if (t) { t.textContent = teaches ? `Teaches ${teaches}` : ''; t.hidden = !teaches; }
  if (b) { b.textContent = bio; b.hidden = !bio; }
  const since = p.created_at || user.created_at;
  const sinceEl = document.getElementById('heroSince');
  if (sinceEl && since) {
    sinceEl.textContent = '📅 Member since ' + new Date(since).toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    sinceEl.hidden = false;
  }
  const first = (p.display_name || user.user_metadata?.full_name || '').trim().split(/\s+/)[0];
  _setText('heroHello', first ? `Hi, ${first}! 👋` : 'Welcome back 👋');

  // Profile completion — nudges teachers to finish the profile other
  // teachers see. Hidden once everything is filled in.
  const steps = [
    [!!(p.display_name || '').trim(), 'a display name'],
    [!!p.avatar, 'a custom avatar'],
    [!!teaches, 'what you teach'],
    [!!bio, 'a short bio'],
    [!!(p.is_public && p.public_slug), 'turn on your public profile'],
  ];
  const done = steps.filter(s => s[0]).length;
  const pct = Math.round(done / steps.length * 100);
  const box = document.getElementById('completion');
  if (!box) return;
  box.hidden = pct === 100;
  _setText('completionTitle', `Your profile is ${pct}% complete`);
  const bar = document.getElementById('completionBar');
  if (bar) bar.style.width = pct + '%';
  _setText('completionMissing', 'Add ' + steps.filter(s => !s[0]).map(s => s[1]).join(' · '));
}

function openEditor() {
  const editor = document.getElementById('profileEdit');
  if (!editor) return;
  editor.hidden = false;
  editor.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
function setupEditorToggle() {
  const editor = document.getElementById('profileEdit');
  if (!editor) return;
  const open = openEditor;
  // /teacher/<slug>/ "Edit profile" links here with #edit.
  if (location.hash === '#edit') setTimeout(openEditor, 300);
  document.getElementById('editProfileBtn')?.addEventListener('click', open);
  document.getElementById('completionBtn')?.addEventListener('click', open);
  document.getElementById('peClose')?.addEventListener('click', () => { editor.hidden = true; });
}
function closeEditorSoon() {
  setTimeout(() => { const ed = document.getElementById('profileEdit'); if (ed) ed.hidden = true; }, 900);
}

// --- Public profile (/teacher/<slug>/, netlify/functions/teacher-page.js) ---
// Opt-in, private by default. set_profile_public() creates the slug the first
// time and keeps it, so a shared link survives later name changes.
function setupPublicToggle(user, profile) {
  const toggle = document.getElementById('publicToggle');
  if (!toggle) return;
  const box = document.getElementById('publicLinkBox');
  const link = document.getElementById('publicLink');
  const copy = document.getElementById('publicCopy');
  const err = document.getElementById('publicError');
  const viewBtn = document.getElementById('viewPublicBtn');
  const goBtn = document.getElementById('goPublicBtn');
  const showErr = (msg) => { err.textContent = msg; err.hidden = !msg; };
  const urlNow = () => `${location.origin}/teacher/${profile.public_slug}/`;

  const paint = () => {
    const on = !!(profile.is_public && profile.public_slug);
    toggle.checked = on;
    box.hidden = !on;
    const tip = document.getElementById('publicTip');
    if (tip) tip.hidden = !on;
    if (viewBtn) viewBtn.hidden = !on;
    if (goBtn) goBtn.hidden = on;
    if (on) {
      const url = urlNow();
      link.href = url; link.textContent = url.replace(/^https?:\/\//, '');
      if (viewBtn) viewBtn.href = url;
    }
  };
  paint();

  toggle.addEventListener('change', async () => {
    const desired = toggle.checked;
    showErr('');
    // Most accounts never saved a display name — the one on screen comes from
    // Google. Send it along; the RPC saves it when the profile has none.
    const shownName = (profile.display_name || user.user_metadata?.full_name || '').trim();
    if (desired && !shownName) {
      toggle.checked = false;
      showErr('Add a display name first — it’s the name shown on your public page.');
      openEditor();
      return;
    }
    toggle.disabled = true;
    const { data, error } = await sb2.rpc('set_profile_public', { p_public: desired, p_display_name: shownName });
    toggle.disabled = false;
    if (error) {
      console.error('set_profile_public failed', error);
      toggle.checked = !desired;
      showErr('Could not save right now. Please try again.');
      return;
    }
    profile.is_public = desired;
    if (data) profile.public_slug = data;
    if (desired && !(profile.display_name || '').trim()) profile.display_name = shownName.slice(0, 40);
    paint();
    paintHero(user, profile);
    window.wsTrack?.(desired ? 'profile_made_public' : 'profile_made_private', {});
    const saved = document.getElementById('publicSaved');
    saved.style.display = 'inline';
    setTimeout(() => { saved.style.display = 'none'; }, 2000);
  });

  copy?.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(urlNow()); copy.textContent = 'Copied ✓'; }
    catch (e) { prompt('Copy this link:', urlNow()); }
    setTimeout(() => { copy.textContent = 'Copy link'; }, 2000);
  });
}

// --- Plan / billing --------------------------------------------------------
function paintPlan(profile) {
  const premium = !!profile?.is_premium;
  const portal = profile?.lemon_portal_url || '';
  const planBadge = document.querySelector('.plan-badge');
  if (planBadge) { planBadge.textContent = premium ? '⭐ Premium' : '✓ Free'; planBadge.classList.toggle('premium', premium); }

  // "Billing & plan" only becomes a real "manage subscription" link once we
  // have this user's Lemon Squeezy portal URL (arrives on their first
  // webhook event after this field was added — see lemon-webhook.js). Until
  // then it falls back to the pricing page rather than a dead end.
  const setLink = (a, label) => {
    if (!a) return;
    a.removeAttribute('target'); a.removeAttribute('rel');
    if (premium && portal) { a.href = portal; a.target = '_blank'; a.rel = 'noopener'; }
    else a.href = 'workshido-pricing.html';
    if (label) label.textContent = premium && portal ? 'Manage subscription' : premium ? 'Billing & plan' : 'See plans';
  };
  setLink(document.getElementById('billingLink'), document.getElementById('billingLinkLabel'));
  _setText('billingDesc', premium ? 'Your Premium plan is active. Update payment details or cancel any time.' : 'You are on the Free plan. Upgrade any time to unlock everything.');

  const cta = document.getElementById('acctPlanCta');
  const card = document.getElementById('planCard');
  const perks = document.getElementById('planPerks');
  if (card) card.classList.toggle('free', !premium);
  if (perks) perks.hidden = premium;
  if (premium) {
    _setText('acctPlanTitle', '⭐ Premium plan — active');
    _setText('acctPlanDesc', 'You have full access to every Teacher Edition (860+ worksheets) and every graded Quiz.');
    setLink(cta);
    if (cta) cta.textContent = portal ? 'Manage subscription' : 'Billing & plan';
  } else {
    _setText('acctPlanTitle', 'Unlock everything with Premium');
    _setText('acctPlanDesc', 'Save hours of prep: 860+ worksheets come with a ready-to-teach Teacher Edition, plus graded Quizzes.');
    setLink(cta);
    if (cta) { cta.className = 'btn btn-primary'; cta.textContent = 'Upgrade to Premium →'; }
  }
}

function setupMarketingToggle(profile) {
  const marketingToggle = document.getElementById('marketingToggle');
  if (!marketingToggle) return;
  marketingToggle.checked = !!profile?.marketing_consent;
  marketingToggle.addEventListener('change', async () => {
    const desired = marketingToggle.checked;
    marketingToggle.disabled = true;
    const { error } = await sb2.rpc('set_marketing_consent', {
      p_consent: desired,
      p_version: 'v1',
      p_source: 'profile_settings',
    });
    marketingToggle.disabled = false;
    if (error) {
      console.error('set_marketing_consent failed', error);
      marketingToggle.checked = !desired; // revert — the save didn't actually happen
      return;
    }
    const saved = document.getElementById('marketingSaved');
    saved.style.display = 'inline';
    setTimeout(() => { saved.style.display = 'none'; }, 2000);
  });
}

// --- Tab bar: highlight the section in view --------------------------------
function setupTabs() {
  const tabs = [...document.querySelectorAll('#tabbar .tab')];
  const update = () => {
    let current = tabs[0];
    tabs.forEach(t => {
      if (t.hidden) return;
      const sec = document.querySelector(t.getAttribute('href'));
      if (sec && !sec.hidden && sec.getBoundingClientRect().top <= 140) current = t;
    });
    // Bottom of the page: the last section may be too short to reach the top.
    if (window.innerHeight + window.scrollY >= document.body.scrollHeight - 4) current = tabs.filter(t => !t.hidden).pop();
    tabs.forEach(t => {
      t.classList.toggle('active', t === current);
      if (t === current) t.setAttribute('aria-current', 'true'); else t.removeAttribute('aria-current');
    });
  };
  window.addEventListener('scroll', update, { passive: true });
  update();
}

// --- Worksheet card (real thumbnail) ---------------------------------------
function cardHtml(w, opts = {}) {
  const color = LEVEL_COLOR[w.level] || 'teal';
  const lvl = LEVEL_CLS[w.level] || 'a1';
  const thumb = w.thumbnail_url
    ? `<img src="${esc(smThumb(w.thumbnail_url))}" onerror="this.onerror=null;this.src='${esc(w.thumbnail_url)}'" alt="${esc(w.title)}" loading="lazy" decoding="async" width="440" height="622">`
    : '';
  const rank = opts.rank ? `<span class="pcard-rank">#${opts.rank}</span>` : '';
  const foot = [];
  if (opts.stats) {
    foot.push(`<span>↓ <strong>${fmtNum(w.downloads)}</strong></span>`);
    if (w.ratings_count) foot.push(`<span><span class="star">★</span> <strong>${Number(w.rating).toFixed(1)}</strong> (${w.ratings_count})</span>`);
  }
  if (opts.date) foot.push(`<span>${esc(opts.date)}</span>`);
  const free = opts.stats && w.is_free ? '<span class="ws-free">Free</span>' : '';
  const rm = opts.removable
    ? `<button class="pcard-remove" type="button" title="Remove from saved" aria-label="Remove from saved" onclick="unsaveWs('${w.id}')">♥</button>` : '';
  return `<div class="pcard" data-id="${w.id}">
    <a class="pcard-link" href="${wsHref(w)}">
      <div class="pcard-thumb ${color}">${thumb}${rank}</div>
      <div class="pcard-body">
        <div class="pcard-meta"><span class="ws-level ${lvl}">${esc(w.level || '')}</span>${free}${w.category ? `<span class="pcard-cat">${esc(w.category)}</span>` : ''}</div>
        <div class="pcard-title">${esc(w.title)}</div>
        ${foot.length ? `<div class="pcard-foot">${foot.join('')}</div>` : ''}
      </div>
    </a>${rm}
  </div>`;
}

function emptyHtml(icon, title, desc, ctaLabel, ctaHref) {
  return `<div class="empty" style="grid-column:1/-1">
    <div class="empty-icon">${icon}</div>
    <div class="empty-title">${title}</div>
    <div class="empty-desc">${desc}</div>
    <a href="${ctaHref}" class="btn btn-primary">${ctaLabel}</a>
  </div>`;
}

// --- My worksheets (Juan) --------------------------------------------------
// Juan is the only uploader, but the batch pipeline (tools/upload_batch.py)
// inserts rows without uploaded_by — filtering on it hid ~98% of the catalog.
// So the admin dashboard lists every worksheet.
async function fetchAllWorksheets() {
  const rows = [];
  for (let from = 0; ; from += 1000) {
    const { data, error } = await sb2.from('worksheets').select(WS_COLS)
      .order('created_at', { ascending: false, nullsFirst: false }).order('id')
      .range(from, from + 999);
    if (error) { console.error(error); break; }
    rows.push(...(data || []));
    if (!data || data.length < 1000) break;
  }
  return rows;
}

const _grid = { all: [], q: '', level: 'all', sort: 'new', shown: GRID_PAGE };

async function loadMyWorksheets() {
  const ws = await fetchAllWorksheets();
  _grid.all = ws;
  const totalDl = ws.reduce((s, w) => s + (w.downloads || 0), 0);
  const rated = ws.filter(w => w.ratings_count > 0);
  const nRatings = rated.reduce((s, w) => s + w.ratings_count, 0);
  const avgRating = nRatings ? rated.reduce((s, w) => s + Number(w.rating) * w.ratings_count, 0) / nRatings : 0;

  _setText('stat1Icon', '📚'); _setText('stat1', fmtNum(ws.length)); _setText('stat1Label', 'Worksheets published');
  _setText('stat2Icon', '📥'); _setText('stat2', fmtNum(totalDl)); _setText('stat2Label', 'Total downloads');
  _setText('stat3Icon', '⭐'); _setText('stat3', nRatings ? avgRating.toFixed(1) + ' ★' : '—'); _setText('stat3Label', nRatings ? `Average rating · ${fmtNum(nRatings)} reviews` : 'Average rating');
  _setText('stat4Icon', '📈'); _setText('stat4', ws.length ? (totalDl / ws.length).toFixed(1) : '—'); _setText('stat4Label', 'Downloads per worksheet');
  _setText('wsCount', `${fmtNum(ws.length)} published · ${fmtNum(totalDl)} downloads`);
  _setText('tabMyWsCount', fmtNum(ws.length));

  // Level mix bar
  const byLevel = {};
  ws.forEach(w => { byLevel[w.level] = (byLevel[w.level] || 0) + 1; });
  const present = LEVELS.filter(l => byLevel[l]);
  const bar = document.getElementById('levelBar');
  const legend = document.getElementById('levelLegend');
  if (bar && ws.length) {
    bar.innerHTML = present.map(l => `<span class="lv-${l}" style="width:${byLevel[l] / ws.length * 100}%" title="${l}: ${byLevel[l]}"></span>`).join('');
    legend.innerHTML = present.map(l => `<span><i class="lv-${l}"></i><strong>${l}</strong> · ${fmtNum(byLevel[l])} (${Math.round(byLevel[l] / ws.length * 100)}%)</span>`).join('');
    _setText('levelMixSub', `Most of your catalog is ${_topKey(byLevel)} — ${fmtNum(ws.length)} worksheets in total`);
  }

  // Toolbar
  const filters = document.getElementById('wsLevelFilters');
  if (filters) {
    filters.innerHTML = [`<button class="lvl-chip sel" type="button" data-level="all">All</button>`]
      .concat(present.map(l => `<button class="lvl-chip" type="button" data-level="${l}">${l}</button>`)).join('');
    filters.addEventListener('click', e => {
      const b = e.target.closest('.lvl-chip'); if (!b) return;
      _grid.level = b.dataset.level; _grid.shown = GRID_PAGE;
      filters.querySelectorAll('.lvl-chip').forEach(x => x.classList.toggle('sel', x === b));
      renderMyWs();
    });
  }
  let t;
  document.getElementById('wsSearch')?.addEventListener('input', e => {
    clearTimeout(t);
    t = setTimeout(() => { _grid.q = _norm(e.target.value.trim()); _grid.shown = GRID_PAGE; renderMyWs(); }, 150);
  });
  document.getElementById('wsSort')?.addEventListener('change', e => { _grid.sort = e.target.value; _grid.shown = GRID_PAGE; renderMyWs(); });
  document.getElementById('myWsMoreBtn')?.addEventListener('click', () => { _grid.shown += GRID_PAGE; renderMyWs(); });

  renderMyWs();
}

function renderMyWs() {
  const container = document.getElementById('myWsRows');
  if (!container) return;
  if (!_grid.all.length) {
    container.innerHTML = emptyHtml('📄', 'No worksheets yet', 'Upload your first worksheet and it will appear here with its downloads and ratings.', 'Upload a worksheet', 'workshido-upload.html');
    document.getElementById('myWsMore').hidden = true;
    return;
  }
  let list = _grid.all.filter(w =>
    (_grid.level === 'all' || w.level === _grid.level) &&
    (!_grid.q || _norm(w.title + ' ' + (w.category || '')).includes(_grid.q)));
  const sorters = {
    new: null, // already newest-first from the query
    dl: (a, b) => (b.downloads || 0) - (a.downloads || 0),
    rating: (a, b) => (Number(b.rating) || 0) - (Number(a.rating) || 0) || (b.ratings_count || 0) - (a.ratings_count || 0),
    az: (a, b) => a.title.localeCompare(b.title),
  };
  if (sorters[_grid.sort]) list = list.slice().sort(sorters[_grid.sort]);
  const ranked = _grid.sort === 'dl' || _grid.sort === 'rating';
  const page = list.slice(0, _grid.shown);
  container.innerHTML = page.length
    ? page.map((w, i) => cardHtml(w, { stats: true, rank: ranked && i < 3 ? i + 1 : 0 })).join('')
    : `<div class="empty" style="grid-column:1/-1"><div class="empty-icon">🔍</div><div class="empty-title">No matches</div><div class="empty-desc">Try another word or level.</div></div>`;
  const more = document.getElementById('myWsMore');
  more.hidden = !list.length;
  document.getElementById('myWsMoreBtn').hidden = page.length >= list.length;
  _setText('myWsMoreInfo', `Showing ${fmtNum(page.length)} of ${fmtNum(list.length)}`);
}

// --- Subscriber KPI tiles --------------------------------------------------
function paintSubscriberStats(saved, dl, profile) {
  const byLevel = {};
  (dl?.ws || []).forEach(w => { byLevel[w.level] = (byLevel[w.level] || 0) + 1; });
  _setText('stat1', fmtNum(dl?.ws?.length || 0));
  _setText('stat2', fmtNum(saved?.length || 0));
  _setText('stat3', _topKey(byLevel));
  _setText('stat4', profile?.is_premium ? 'Premium' : 'Free');
}

// --- Profile customization -------------------------------------------------
// profiles.avatar stores ONE of:
//   null
//   "<emoji>|<colourkey>"        quick icon (rendered as a coloured circle)
//   "dicebear:<query-string>"    Avataaars character (rendered via an <img> to
//                                api.dicebear.com — sandboxed, $0 storage)
// Falls back to the Google photo, then to initials.
const AV_COLORS = { blue:'#DCEBFB', teal:'#D3F0E6', amber:'#FBEAD0', pink:'#FBDDEC', purple:'#E7E5FB', coral:'#FADDD2', green:'#E4F1D3', slate:'#E6EBF1' };
const AV_COLOR_KEYS = Object.keys(AV_COLORS);
const AV_EMOJI = ['📚','✏️','📝','🍎','🌟','🚀','🌍','💡','🧠','🎨','🧩','🎓','🔍','📖','✨','🌈','🦉','🦊','🐱','🐧','🐢','🌱','☕','🎵'];

const DICEBEAR = 'https://api.dicebear.com/9.x/avataaars/svg?';
// One list per studio category. Order = display order. 'none' handled specially.
const DB_OPTS = {
  top:        ['shortFlat','shortCurly','shortRound','theCaesar','bob','bun','curly','dreads','longButNotTooLong','frizzle','hat','turban','hijab','winterHat02'],
  hairColor:  ['2c1b18','4a312c','724133','a55728','b58143','c93305','d6b370','e8e1e1','f59797','ecdcbf'],
  skinColor:  ['f2d3b1','edb98a','d08b5b','ae5d29','614335','ffdbb4'],
  accessories:['none','prescription01','prescription02','round','sunglasses','wayfarers','kurt','eyepatch'],
  facialHair: ['none','beardLight','beardMedium','beardMajestic','moustacheFancy','moustacheMagnum'],
  eyes:       ['default','happy','wink','hearts','squint','surprised','closed','side','cry'],
  eyebrows:   ['default','raisedExcited','angry','sadConcerned','upDown','flatNatural'],
  mouth:      ['default','smile','twinkle','serious','tongue','grimace','disbelief','eating'],
  clothing:   ['blazerAndShirt','hoodie','graphicShirt','collarAndSweater','overall','shirtCrewNeck','shirtVNeck','blazerAndSweater'],
  backgroundColor: ['b6e3f4','c0aede','d1d4f9','ffd5dc','ffdfbf','transparent'],
};
const DB_CATS = [
  { key:'top',        label:'Hair / hat',   type:'chips' },
  { key:'hairColor',  label:'Hair colour',  type:'sw' },
  { key:'skinColor',  label:'Skin',         type:'sw' },
  { key:'accessories',label:'Glasses',      type:'chips' },
  { key:'facialHair', label:'Facial hair',  type:'chips' },
  { key:'eyes',       label:'Eyes',         type:'chips' },
  { key:'eyebrows',   label:'Eyebrows',     type:'chips' },
  { key:'mouth',      label:'Mouth',        type:'chips' },
  { key:'clothing',   label:'Clothes',      type:'chips' },
  { key:'backgroundColor', label:'Background', type:'sw' },
];
const DB_LABELS = {
  shortFlat:'Short', shortCurly:'Curly', shortRound:'Round', theCaesar:'Caesar', bob:'Bob', bun:'Bun',
  curly:'Big curly', dreads:'Dreads', longButNotTooLong:'Long', frizzle:'Frizzle', hat:'Sun hat',
  turban:'Turban', hijab:'Hijab', winterHat02:'Beanie',
  none:'None', prescription01:'Thin', prescription02:'Bold', round:'Round', sunglasses:'Shades',
  wayfarers:'Wayfarer', kurt:'Kurt', eyepatch:'Eyepatch',
  beardLight:'Stubble', beardMedium:'Beard', beardMajestic:'Full beard', moustacheFancy:'Moustache', moustacheMagnum:'Magnum',
  raisedExcited:'Excited', sadConcerned:'Concerned', upDown:'Up-down', flatNatural:'Natural',
  blazerAndShirt:'Blazer', hoodie:'Hoodie', graphicShirt:'Graphic tee', collarAndSweater:'Collar+jumper',
  overall:'Overalls', shirtCrewNeck:'Crew neck', shirtVNeck:'V-neck', blazerAndSweater:'Blazer+jumper',
};
const dbLabel = v => DB_LABELS[v] || (v.charAt(0).toUpperCase() + v.slice(1).replace(/([A-Z])/g, ' $1'));

function _randSeed() { return Math.random().toString(36).slice(2, 10); }
function _pick(a) { return a[Math.floor(Math.random() * a.length)]; }

function dbDefaultCfg(seed) {
  return { seed: seed || _randSeed(), top:'shortFlat', hairColor:'4a312c', skinColor:'edb98a',
    accessories:'none', facialHair:'none', eyes:'default', eyebrows:'default', mouth:'smile',
    clothing:'shirtCrewNeck', backgroundColor:'b6e3f4' };
}
function dbRandomCfg() {
  const c = { seed: _randSeed() };
  for (const k in DB_OPTS) c[k] = _pick(DB_OPTS[k]);
  return c;
}
function dbToQS(cfg) {
  const p = new URLSearchParams();
  p.set('seed', cfg.seed || 'ws');
  ['top','hairColor','skinColor','eyes','eyebrows','mouth','clothing','backgroundColor'].forEach(k => {
    if (cfg[k]) p.set(k, cfg[k]);
  });
  if (cfg.accessories && cfg.accessories !== 'none') { p.set('accessories', cfg.accessories); p.set('accessoriesProbability', '100'); }
  else p.set('accessoriesProbability', '0');
  if (cfg.facialHair && cfg.facialHair !== 'none') { p.set('facialHair', cfg.facialHair); p.set('facialHairProbability', '100'); }
  else p.set('facialHairProbability', '0');
  return p.toString();
}
function dbFromStored(stored) {
  if (!stored || stored.indexOf('dicebear:') !== 0) return null;
  const p = new URLSearchParams(stored.slice(9));
  const cfg = dbDefaultCfg(p.get('seed') || _randSeed());
  ['top','hairColor','skinColor','eyes','eyebrows','mouth','clothing','backgroundColor'].forEach(k => {
    if (p.get(k)) cfg[k] = p.get(k);
  });
  cfg.accessories = (p.get('accessoriesProbability') === '0') ? 'none' : (p.get('accessories') || 'none');
  cfg.facialHair  = (p.get('facialHairProbability') === '0')  ? 'none' : (p.get('facialHair')  || 'none');
  return cfg;
}
function dbSrc(stored) { return stored && stored.indexOf('dicebear:') === 0 ? DICEBEAR + stored.slice(9) : ''; }

function _parseEmoji(v) {
  if (!v || v.indexOf('|') < 0 || v.indexOf('dicebear:') === 0) return null;
  const i = v.lastIndexOf('|');
  const e = v.slice(0, i), c = v.slice(i + 1);
  return AV_COLORS[c] && e ? { e, c } : null;
}
function _toInitials(s) {
  return (s || '').split(/\s+/).filter(Boolean).map(n => n[0]).join('').toUpperCase().slice(0, 2) || '?';
}
function _paintAvatar(el, stored, googlePic, fallbackInitials) {
  if (!el) return;
  el.classList.remove('has-emoji');
  el.innerHTML = '';
  el.style.background = '';
  el.style.color = '';
  const dbs = dbSrc(stored);
  const emoji = _parseEmoji(stored);
  if (dbs) {
    const img = document.createElement('img');
    img.src = dbs; img.alt = 'avatar';
    img.onerror = () => { el.innerHTML = ''; el.textContent = fallbackInitials; };
    el.appendChild(img);
  } else if (emoji) {
    el.classList.add('has-emoji');
    el.style.background = AV_COLORS[emoji.c];
    el.textContent = emoji.e;
  } else if (googlePic) {
    const img = document.createElement('img');
    img.src = googlePic; img.alt = ''; img.referrerPolicy = 'no-referrer';
    img.onerror = () => { el.innerHTML = ''; el.textContent = fallbackInitials; };
    el.appendChild(img);
  } else {
    el.textContent = fallbackInitials;
  }
}

function setupProfileCustomization(user, profile) {
  const googlePic = user.user_metadata?.avatar_url || user.user_metadata?.picture || '';
  const bigEl = document.querySelector('.avatar-big');
  const navEl = document.querySelector('.nav-avatar');
  const nameEl = document.querySelector('.profile-name');

  const applied = () => {
    const dn = (profile?.display_name || user.user_metadata?.full_name || user.email || '').trim();
    if (nameEl) nameEl.textContent = dn;
    const ini = _toInitials(dn);
    _paintAvatar(bigEl, profile?.avatar, googlePic, ini);
    _paintAvatar(navEl, profile?.avatar, googlePic, ini);
    paintHero(user, profile);
  };
  applied();

  const preview     = document.getElementById('pePreview');
  const nameInput   = document.getElementById('peName');
  const teachesInput= document.getElementById('peTeaches');
  const bioInput    = document.getElementById('peBio');
  const saveBtn     = document.getElementById('peSave');
  const savedMsg    = document.getElementById('peSaved');
  const studioRows  = document.getElementById('peStudioRows');
  const studioWrap  = document.getElementById('peStudio');
  const quickWrap   = document.getElementById('peQuick');
  const quickToggle = document.getElementById('peQuickToggle');
  const shuffleBtn  = document.getElementById('peShuffle');
  const emojiGrid   = document.getElementById('peEmojiGrid');
  const emojiColors = document.getElementById('peColors');
  if (!preview || !nameInput || !saveBtn || !studioRows) return;

  nameInput.value    = profile?.display_name || user.user_metadata?.full_name || '';
  teachesInput.value = profile?.teaches || '';
  bioInput.value     = profile?.bio || '';

  // ---- state ----
  const emojiCur = _parseEmoji(profile?.avatar);
  let mode = emojiCur ? 'emoji' : 'studio';               // which picker is active
  let cfg  = dbFromStored(profile?.avatar) || dbDefaultCfg();
  let selE = emojiCur ? emojiCur.e : '';
  let selC = emojiCur ? emojiCur.c : 'blue';

  const previewImg = document.createElement('img');
  previewImg.alt = 'avatar preview';

  function renderPreview() {
    if (mode === 'studio') {
      preview.style.background = '#DCEBFB';
      preview.textContent = '';
      previewImg.src = DICEBEAR + dbToQS(cfg);
      if (previewImg.parentNode !== preview) preview.appendChild(previewImg);
    } else {
      if (previewImg.parentNode) previewImg.remove();
      preview.style.background = AV_COLORS[selC];
      preview.textContent = selE || _toInitials(nameInput.value.trim() || 'You');
      preview.style.fontSize = selE ? '44px' : '32px';
    }
  }

  // ---- studio rows ----
  function buildStudio() {
    studioRows.innerHTML = '';
    DB_CATS.forEach(cat => {
      const wrap = document.createElement('div'); wrap.className = 'pe-cat';
      const lab = document.createElement('div'); lab.className = 'pe-cat-label'; lab.textContent = cat.label;
      const row = document.createElement('div'); row.className = 'pe-chips';
      DB_OPTS[cat.key].forEach(val => {
        const b = document.createElement('button'); b.type = 'button';
        if (cat.type === 'sw') {
          b.className = 'pe-sw' + (cfg[cat.key] === val ? ' sel' : '');
          b.style.background = (val === 'transparent') ? 'repeating-conic-gradient(#ccc 0% 25%, #fff 0% 50%) 50% / 10px 10px' : '#' + val;
          b.title = (val === 'transparent') ? 'None' : ('#' + val);
        } else {
          b.className = 'pe-chip' + (cfg[cat.key] === val ? ' sel' : '');
          b.textContent = dbLabel(val);
        }
        b.onclick = () => {
          cfg[cat.key] = val;
          row.querySelectorAll('button').forEach(x => x.classList.toggle('sel', false));
          b.classList.add('sel');
          renderPreview();
        };
        row.appendChild(b);
      });
      wrap.appendChild(lab); wrap.appendChild(row); studioRows.appendChild(wrap);
    });
  }
  buildStudio();

  // ---- emoji quick-pick ----
  AV_EMOJI.forEach(e => {
    const b = document.createElement('button'); b.type = 'button';
    b.className = 'pe-emoji' + (e === selE ? ' sel' : '');
    b.textContent = e;
    b.onclick = () => {
      selE = (selE === e) ? '' : e;
      emojiGrid.querySelectorAll('.pe-emoji').forEach(x => x.classList.toggle('sel', x.textContent === selE && selE !== ''));
      renderPreview();
    };
    emojiGrid.appendChild(b);
  });
  AV_COLOR_KEYS.forEach(c => {
    const s = document.createElement('button'); s.type = 'button';
    s.className = 'pe-color' + (c === selC ? ' sel' : '');
    s.style.background = AV_COLORS[c];
    s.onclick = () => {
      selC = c;
      emojiColors.querySelectorAll('.pe-color').forEach((x, i) => x.classList.toggle('sel', AV_COLOR_KEYS[i] === selC));
      renderPreview();
    };
    emojiColors.appendChild(s);
  });

  function setMode(m) {
    mode = m;
    studioWrap.hidden = (m !== 'studio');
    quickWrap.hidden  = (m === 'studio');
    quickToggle.textContent = (m === 'studio') ? 'Use a simple icon instead' : 'Back to the character builder';
    shuffleBtn.hidden = (m !== 'studio');
    renderPreview();
  }
  quickToggle.onclick = () => setMode(mode === 'studio' ? 'emoji' : 'studio');
  shuffleBtn.onclick = () => { cfg = dbRandomCfg(); buildStudio(); renderPreview(); };
  nameInput.addEventListener('input', () => { if (mode === 'emoji') renderPreview(); });

  setMode(mode);

  saveBtn.onclick = async () => {
    saveBtn.disabled = true;
    const p_avatar = (mode === 'studio')
      ? 'dicebear:' + dbToQS(cfg)
      : (selE ? (selE + '|' + selC) : null);
    const p_display_name = nameInput.value.trim();
    const p_teaches = teachesInput.value.trim();
    const p_bio = bioInput.value.trim();
    const { error } = await sb2.rpc('set_profile_customization', { p_avatar, p_display_name, p_bio, p_teaches });
    saveBtn.disabled = false;
    if (error) { console.error('set_profile_customization failed', error); alert('Could not save right now. Please try again.'); return; }
    profile = profile || {};
    profile.avatar = p_avatar; profile.display_name = p_display_name;
    profile.bio = p_bio; profile.teaches = p_teaches;
    applied();
    if (savedMsg) { savedMsg.style.display = 'inline'; setTimeout(() => { savedMsg.style.display = 'none'; }, 2000); }
    closeEditorSoon();
  };
}

// --- Saved worksheets + download history ----------------------------------
async function _fetchWorksheetsByIds(ids) {
  if (!ids.length) return [];
  const byId = {};
  // Chunked so the .in() filter never builds an oversized request URL.
  for (let i = 0; i < ids.length; i += 100) {
    const { data } = await sb2.from('worksheets').select(WS_COLS).in('id', ids.slice(i, i + 100));
    (data || []).forEach(w => { byId[w.id] = w; });
  }
  return ids.map(id => byId[id]).filter(Boolean); // keep caller's order
}

// Renders the first GRID_PREVIEW cards; the "Show all" button reveals the rest.
function _renderPreviewGrid(rowsEl, moreEl, btnEl, cards) {
  rowsEl.innerHTML = cards.slice(0, GRID_PREVIEW).join('');
  if (!moreEl) return;
  moreEl.hidden = cards.length <= GRID_PREVIEW;
  btnEl.onclick = () => { rowsEl.innerHTML = cards.join(''); moreEl.hidden = true; };
}

function _savedEmpty() {
  return emptyHtml('♡', 'No saved worksheets yet', 'Tap <strong>♡ Save</strong> on any worksheet to build a shortlist for your next lesson.', 'Browse worksheets', 'workshido-index.html');
}

async function loadSavedWorksheets() {
  const rowsEl = document.getElementById('savedRows');
  if (!rowsEl) return [];
  const { data: saved, error } = await sb2.from('saved_worksheets')
    .select('worksheet_id, created_at')
    .order('created_at', { ascending: false });
  const ws = error || !saved ? [] : await _fetchWorksheetsByIds(saved.map(s => s.worksheet_id));
  if (!ws.length) { rowsEl.innerHTML = _savedEmpty(); _setText('tabSavedCount', ''); return []; }
  _renderPreviewGrid(rowsEl, document.getElementById('savedMore'), document.getElementById('savedMoreBtn'),
    ws.map(w => cardHtml(w, { removable: true })));
  _setText('savedCount', `${ws.length} saved · your shortlist for upcoming lessons`);
  _setText('tabSavedCount', ws.length);
  return ws;
}

async function unsaveWs(id) {
  const { error } = await sb2.from('saved_worksheets').delete().eq('worksheet_id', id);
  if (error) { console.error(error); return; }
  const card = document.querySelector(`#savedRows .pcard[data-id="${id}"]`);
  if (card) card.remove();
  const rowsEl = document.getElementById('savedRows');
  const n = rowsEl ? rowsEl.querySelectorAll('.pcard').length : 0;
  _setText('savedCount', n ? `${n} saved · your shortlist for upcoming lessons` : 'Your shortlist for upcoming lessons');
  _setText('tabSavedCount', n || '');
  if (!_isJuan) _setText('stat2', fmtNum(n));
  if (!n && rowsEl) rowsEl.innerHTML = _savedEmpty();
}

async function loadDownloadHistory() {
  const rowsEl = document.getElementById('dlHistoryRows');
  if (!rowsEl) return { ws: [] };
  const { data: dls, error } = await sb2.from('user_downloads')
    .select('worksheet_id, last_at, times')
    .order('last_at', { ascending: false })
    .limit(300);
  const ws = error || !dls ? [] : await _fetchWorksheetsByIds(dls.map(d => d.worksheet_id));
  if (!ws.length) {
    rowsEl.innerHTML = emptyHtml('📥', 'Nothing downloaded yet', 'Every worksheet you download shows up here, so you can grab it again in one click.', 'Find your first worksheet', 'workshido-index.html');
    return { ws: [] };
  }
  const lastAt = {};
  (dls || []).forEach(d => { lastAt[d.worksheet_id] = d.last_at; });
  _renderPreviewGrid(rowsEl, document.getElementById('dlMore'), document.getElementById('dlMoreBtn'),
    ws.map(w => cardHtml(w, { date: lastAt[w.id] ? 'Downloaded ' + new Date(lastAt[w.id]).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '' })));
  _setText('dlCount', `${ws.length} worksheet${ws.length === 1 ? '' : 's'} · grab them again in one click`);
  _setText('tabDlCount', ws.length);
  return { ws };
}

document.addEventListener('DOMContentLoaded', loadProfile);
