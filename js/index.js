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

const LEVEL_CLASS = { A1:'a1', A2:'a2', B1:'b1', B2:'b2', C1:'c1' };

// Worksheet title is free text set at upload time — never trust it as safe
// HTML when it lands back in innerHTML (used by the trending cards below).
function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

// Fire-and-forget — a slow/failed trending fetch must never delay or block
// the rest of the homepage.
async function loadTrending() {
  try {
    const res = await fetch('/.netlify/functions/trending');
    if (!res.ok) return;
    const { items } = await res.json();
    if (!items || !items.length) return;
    const grid = document.getElementById('trendingGrid');
    const section = document.getElementById('trendingSection');
    if (!grid || !section) return;
    grid.innerHTML = items.map((ws, i) => {
      const lvlCls = LEVEL_CLASS[ws.level] || 'a1';
      const thumb = ws.thumbnail_url
        ? `<img src="${ws.thumbnail_url}" alt="${esc(ws.title)}" loading="lazy">`
        : '';
      return `<a href="workshido-worksheet.html?id=${ws.id}" class="trending-card">
        <span class="trending-rank">${i + 1}</span>
        <div class="trending-thumb">${thumb}</div>
        <span class="badge-level ${lvlCls}">${ws.level}</span>
        <div class="trending-card-title">${esc(ws.title)}</div>
        <div class="trending-downloads">↓ ${ws.weekly_downloads} this week</div>
      </a>`;
    }).join('');
    section.style.display = '';
  } catch { /* trending is a nice-to-have — fail silently */ }
}

// ── Live numbers for the hero/stats-bar. The full catalog (browse, filter,
//    search) lives only on workshido-index.html now — this page only needs
//    the count and which levels exist, not every worksheet's full row. ──
const COUNT_MILESTONES = [100, 150, 200, 300, 500, 750, 1000, 1500, 2000, 3000, 5000, 10000];
function milestoneCount(n) {
  let best = COUNT_MILESTONES[0];
  for (const m of COUNT_MILESTONES) if (n >= m) best = m;
  return best.toLocaleString('en-US') + '+';
}
async function loadStats() {
  const { data, count, error } = await sb2.from('worksheets').select('level', { count: 'exact' });
  if (error || !data) return;
  const n = count ?? data.length;
  if (!n) return;
  const rounded = milestoneCount(n);
  const elCount = document.getElementById('statWorksheets');
  if (elCount) elCount.textContent = rounded;
  const eyebrow = document.getElementById('heroEyebrowText');
  if (eyebrow) eyebrow.textContent = `${rounded} free worksheets · Print-ready PDFs · New resources every week`;
  const ctaCount = document.getElementById('browseCtaCount');
  if (ctaCount) ctaCount.textContent = `${n} worksheets and growing — filter by grammar topic, CEFR level, or skill.`;
  // CEFR range actually covered by the catalog
  const order = ['A1', 'A2', 'B1', 'B2', 'C1'];
  const present = order.filter(l => data.some(w => w.level === l));
  const elLevels = document.getElementById('statLevels');
  if (elLevels && present.length) {
    elLevels.textContent = present.length > 1 ? `${present[0]}–${present[present.length - 1]}` : present[0];
  }
  // Hide level chips that have no worksheets yet — they reappear as the catalog grows
  document.querySelectorAll('.chip[data-level]').forEach(chip => {
    if (chip.dataset.level === 'all') return;
    chip.style.display = data.some(w => w.level === chip.dataset.level) ? '' : 'none';
  });
}

// ── Hero search + level/category chips — this page no longer has its own
//    catalog to filter in place, so every one of these just hands the query
//    off to the real catalog page instead. ──
document.querySelectorAll('.chip[data-level]').forEach(chip => {
  chip.addEventListener('click', () => {
    if (chip.dataset.level === 'all') { window.location.href = 'workshido-index.html'; return; }
    window.location.href = `workshido-index.html?level=${encodeURIComponent(chip.dataset.level)}`;
  });
});
document.querySelectorAll('.chip[data-cat]').forEach(chip => {
  chip.addEventListener('click', () => {
    window.location.href = `workshido-index.html?cat=${encodeURIComponent(chip.dataset.cat)}`;
  });
});

const searchInput = document.querySelector('.search-box input');
function goToSearch() {
  const q = searchInput.value.trim();
  window.location.href = q
    ? `workshido-index.html?q=${encodeURIComponent(q)}`
    : 'workshido-index.html';
}
document.querySelector('.search-box button').addEventListener('click', goToSearch);
searchInput.addEventListener('keydown', e => { if (e.key === 'Enter') goToSearch(); });

// Reload on back/forward navigation to avoid stale auth state from bfcache
window.addEventListener('pageshow', (e) => { if (e.persisted) window.location.reload(); });

document.getElementById('yr').textContent = new Date().getFullYear();
function openMobileMenu()  { document.getElementById('mobileMenu').classList.add('open'); document.body.style.overflow = 'hidden'; }
function closeMobileMenu() { document.getElementById('mobileMenu').classList.remove('open'); document.body.style.overflow = ''; }

document.addEventListener('DOMContentLoaded', () => {
  checkAuth2();
  loadTrending();
  loadStats();
});
