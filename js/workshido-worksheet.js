const sb = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
const LEVEL_CLASS = { A1:'a1', A2:'a2', B1:'b1', B2:'b2', C1:'c1' };
function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
let _wsFileUrl = null;
let _answerKeyUrl = null;
let _isPremium = false;
let _wsId = null;
let _wsTitle = 'worksheet';

async function checkAuth() {
  const { data: { user } } = await sb.auth.getUser();
  const uploadLink = document.getElementById('navUploadLink');
  if (uploadLink) uploadLink.style.display = (user?.email === 'juanda.5790@hotmail.com') ? '' : 'none';
  const nav = document.getElementById('navActions');
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
    : `<button class="btn-download-big locked" onclick="openPremiumModal()">🔒 Premium — Unlock to download</button>`;

  const answerKeyBtn = _answerKeyUrl
    ? (_isPremium
        ? `<button class="btn-answer-key unlocked" onclick="downloadAnswerKey()">
            <span class="ak-left">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              <span>Teacher Edition <span class="ak-sub">⭐ Premium — Download</span></span>
            </span>
          </button>`
        : `<button class="btn-answer-key" onclick="openPremiumModal()">
            <span class="ak-left">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              <span>Teacher Edition <span class="ak-sub">⭐ Premium only</span></span>
            </span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color:var(--gray-300)"><polyline points="9 18 15 12 9 6"/></svg>
          </button>
          ${!currentUser ? '<p class="premium-note">Already Premium? <a onclick="googleLoginDl()">Sign in</a></p>' : ''}`)
    : '';

  document.getElementById('pageWrap').innerHTML = `
    <div class="preview-box">${preview}</div>
    <div class="detail-sidebar">
      <div class="detail-card">
        <h1 class="ws-title">${esc(data.title)}</h1>
        <div class="ws-badges">
          <span class="badge-level ${lvlCls}">${data.level}</span>
          ${data.category ? `<span class="badge-cat">${esc(data.category)}</span>` : ''}
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
        ${answerKeyBtn}
        <button class="btn-print" onclick="printWS()">🖨️ Print / Open PDF — Free</button>
        ${starSection}
      </div>
    </div>`;
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
  if (!_wsFileUrl) return;
  const url = await getSignedUrl(_wsFileUrl);
  await forceDownload(url, _wsTitle);
  window.wsTrack?.('download_completed', { worksheet_id: id });
  try {
    const res = await fetch('/.netlify/functions/increment-downloads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${session.access_token}` },
      body: JSON.stringify({ worksheetId: id }),
    });
    const { downloads } = await res.json();
    const el = document.getElementById('dlCount');
    if (el && downloads) el.textContent = downloads;
  } catch(e) {}
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
    if (res.status === 403) { openPremiumModal(); return; }
    if (!res.ok) return;
    const { url } = await res.json();
    if (url) window.open(url, '_blank');
  } catch (e) {}
}

async function openPremiumModal() {
  const { data: { user } } = await sb.auth.getUser();
  if (!user) {
    document.getElementById('dlModalTitle').textContent = 'Sign in to access Premium';
    _openModal(document.getElementById('dlModal'));
  } else {
    _openModal(document.getElementById('premiumModal'));
  }
}
function closePremiumModal() { _closeModal(document.getElementById('premiumModal')); }

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