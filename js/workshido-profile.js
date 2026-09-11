const sb2 = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
const LEVEL_COLOR = { A1:'teal', A2:'blue', B1:'amber', B2:'purple', C1:'coral' };
const LEVEL_CLS   = { A1:'a1',   A2:'a2',  B1:'b1',   B2:'b2',    C1:'c1'    };
const THUMB_ACCENT = { teal:'t', blue:'b', amber:'am', purple:'b', coral:'t' };

async function logOut(){ await sb2.auth.signOut(); window.location.href='workshido-index.html'; }

function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

async function loadProfile() {
  const { data: { user } } = await sb2.auth.getUser();
  if (!user) { window.location.href = 'workshido-login.html'; return; }

  const isJuan = user.email === 'juanda.5790@hotmail.com';
  const uploadSection = document.getElementById('uploadSection');
  if (uploadSection) uploadSection.style.display = isJuan ? '' : 'none';

  // The uploader dashboard (stats + "my worksheets") only makes sense for
  // Juan — uploading is admin-only, so everyone else's would always be
  // empty. Regular subscribers get an account/plan overview instead.
  const statsOverview = document.getElementById('statsOverview');
  const myWsSection = document.getElementById('my-worksheets');
  const subscriberOverview = document.getElementById('subscriberOverview');
  const navMyWsLink = document.getElementById('navMyWsLink');
  const sidebarMyWsLink = document.getElementById('sidebarMyWsLink');
  if (statsOverview) statsOverview.style.display = isJuan ? '' : 'none';
  if (myWsSection) myWsSection.style.display = isJuan ? '' : 'none';
  if (subscriberOverview) subscriberOverview.style.display = isJuan ? 'none' : '';
  if (navMyWsLink) navMyWsLink.style.display = isJuan ? '' : 'none';
  if (sidebarMyWsLink) sidebarMyWsLink.style.display = isJuan ? '' : 'none';

  const name = user.user_metadata?.full_name || user.email;
  const initials0 = name.split(/\s+/).map(n => n[0]).join('').toUpperCase().slice(0, 2);
  document.querySelector('.avatar-big').textContent    = initials0;
  document.querySelector('.profile-name').textContent  = name;
  document.querySelector('.profile-email').textContent = user.email;
  document.querySelector('.nav-avatar').textContent    = initials0;

  const { data: profile } = await sb2
    .from('profiles')
    .select('marketing_consent, is_premium, lemon_portal_url, avatar, display_name')
    .eq('id', user.id)
    .maybeSingle();

  setupProfileCustomization(user, profile);
  loadSavedWorksheets();
  loadDownloadHistory();

  const planBadge = document.querySelector('.plan-badge');
  if (profile?.is_premium) {
    planBadge.textContent = '⭐ Premium';
    planBadge.classList.add('premium');
  } else {
    planBadge.textContent = '✓ Free';
  }

  // "Billing & plan" only becomes a real "manage subscription" link once we
  // have this user's Lemon Squeezy portal URL (arrives on their first
  // webhook event after this field was added — see lemon-webhook.js). Until
  // then it falls back to the pricing page rather than a dead end.
  const billingLink = document.getElementById('billingLink');
  const billingLabel = document.getElementById('billingLinkLabel');
  if (profile?.is_premium && profile?.lemon_portal_url) {
    billingLink.href = profile.lemon_portal_url;
    billingLink.target = '_blank';
    billingLink.rel = 'noopener';
    billingLabel.textContent = 'Manage subscription';
  } else if (profile?.is_premium) {
    billingLabel.textContent = 'Billing & plan';
  }

  // Same plan state, rendered as the main "Your account" card for regular
  // (non-Juan) subscribers — see subscriberOverview in the HTML.
  const acctPlanTitle = document.getElementById('acctPlanTitle');
  const acctPlanDesc = document.getElementById('acctPlanDesc');
  const acctPlanCta = document.getElementById('acctPlanCta');
  if (acctPlanTitle && acctPlanDesc && acctPlanCta) {
    if (profile?.is_premium) {
      acctPlanTitle.textContent = '⭐ Premium plan — active';
      acctPlanDesc.textContent = 'You have full access to the Teacher Edition and the graded Quiz for every worksheet.';
      acctPlanCta.removeAttribute('target');
      acctPlanCta.removeAttribute('rel');
      if (profile?.lemon_portal_url) {
        acctPlanCta.textContent = 'Manage subscription';
        acctPlanCta.href = profile.lemon_portal_url;
        acctPlanCta.target = '_blank';
        acctPlanCta.rel = 'noopener';
      } else {
        acctPlanCta.textContent = 'Billing & plan';
        acctPlanCta.href = 'workshido-pricing.html';
      }
    } else {
      acctPlanTitle.textContent = 'Free plan';
      acctPlanDesc.textContent = 'Upgrade to Premium to unlock the Teacher Edition and the full Quiz for every worksheet.';
      acctPlanCta.textContent = 'Upgrade to Premium';
      acctPlanCta.href = 'workshido-pricing.html';
      acctPlanCta.removeAttribute('target');
      acctPlanCta.removeAttribute('rel');
    }
  }

  const marketingToggle = document.getElementById('marketingToggle');
  if (marketingToggle) {
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

  // Uploading is Juan-only, so the "my worksheets" query/render below only
  // applies to his account — everyone else already saw subscriberOverview.
  if (!isJuan) return;

  const { data: worksheets } = await sb2
    .from('worksheets')
    .select('id, title, level, category, downloads, created_at')
    .eq('uploaded_by', user.id)
    .order('created_at', { ascending: false });

  const ws = worksheets || [];
  const totalDl = ws.reduce((s, w) => s + (w.downloads || 0), 0);

  const levelCount = {};
  const catCount   = {};
  ws.forEach(w => {
    levelCount[w.level]    = (levelCount[w.level]    || 0) + 1;
    catCount[w.category]   = (catCount[w.category]   || 0) + 1;
  });
  const topLevel = Object.entries(levelCount).sort((a,b) => b[1]-a[1])[0]?.[0] || '—';
  const topCat   = Object.entries(catCount).sort((a,b)   => b[1]-a[1])[0]?.[0] || '—';

  document.getElementById('statUploaded').textContent = ws.length;
  document.getElementById('statDownloads').textContent = totalDl.toLocaleString();
  document.getElementById('statLevel').textContent    = topLevel;
  document.getElementById('statCategory').textContent = topCat;
  document.getElementById('wsCount').textContent      = `${ws.length} published`;

  const container = document.getElementById('myWsRows');
  if (ws.length === 0) {
    container.innerHTML = `<div style="padding:40px;text-align:center;color:var(--gray-300);font-size:14px;">You haven't uploaded any worksheets yet. <a href="workshido-upload.html" style="color:var(--blue-600)">Upload your first one →</a></div>`;
    return;
  }

  container.innerHTML = ws.map(w => {
    const color   = LEVEL_COLOR[w.level]  || 'teal';
    const lvlCls  = LEVEL_CLS[w.level]   || 'a1';
    const accent  = THUMB_ACCENT[color]   || 't';
    const date    = w.created_at ? new Date(w.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' }) : '—';
    return `<div class="ws-row">
      <div class="ws-mini-thumb ${color}"><div class="wl a ${accent}"></div><div class="wl s"></div><div class="wb"></div><div class="wb"></div></div>
      <div class="ws-info">
        <div class="ws-title">${esc(w.title)}</div>
        <div class="ws-meta-row"><span class="ws-level ${lvlCls}">${w.level}</span><span class="ws-status">Published · ${date}</span></div>
      </div>
      <div class="ws-stats-mini"><div class="ws-stat">↓ <strong>${(w.downloads||0).toLocaleString()}</strong></div></div>
      <div class="ws-actions"><a href="workshido-worksheet.html?id=${w.id}" class="btn-sm edit">View</a></div>
    </div>`;
  }).join('');
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
  };
}

// --- Saved worksheets + download history ----------------------------------
function _wsRowHtml(w, opts) {
  const lvlCls = LEVEL_CLS[w.level] || 'a1';
  const cat = w.category || 'Worksheet';
  const rm = opts && opts.removeId
    ? `<button class="btn-sm delete" type="button" onclick="unsaveWs('${w.id}')">Remove</button>` : '';
  return `<div class="ws-row" data-id="${w.id}">
    <div class="ws-info">
      <div class="ws-title">${esc(w.title)}</div>
      <div class="ws-meta-row"><span class="ws-level ${lvlCls}">${esc(w.level || '')}</span><span class="ws-status">${esc(cat)}</span></div>
    </div>
    <div class="ws-actions">
      <a href="workshido-worksheet.html?id=${w.id}" class="btn-sm edit">Open</a>${rm}
    </div>
  </div>`;
}

async function _fetchWorksheetsByIds(ids) {
  if (!ids.length) return [];
  const { data } = await sb2.from('worksheets')
    .select('id,title,level,category')
    .in('id', ids);
  const byId = {};
  (data || []).forEach(w => { byId[w.id] = w; });
  return ids.map(id => byId[id]).filter(Boolean); // keep caller's order
}

async function loadSavedWorksheets() {
  const section = document.getElementById('savedSection');
  const rowsEl = document.getElementById('savedRows');
  const countEl = document.getElementById('savedCount');
  if (!section || !rowsEl) return;
  const { data: saved, error } = await sb2.from('saved_worksheets')
    .select('worksheet_id, created_at')
    .order('created_at', { ascending: false });
  if (error || !saved || !saved.length) return;   // hidden when empty
  const ws = await _fetchWorksheetsByIds(saved.map(s => s.worksheet_id));
  if (!ws.length) return;
  rowsEl.innerHTML = ws.map(w => _wsRowHtml(w, { removeId: true })).join('');
  if (countEl) countEl.textContent = `${ws.length} saved`;
  section.style.display = '';
}

async function unsaveWs(id) {
  const { error } = await sb2.from('saved_worksheets').delete().eq('worksheet_id', id);
  if (error) { console.error(error); return; }
  const row = document.querySelector(`#savedRows .ws-row[data-id="${id}"]`);
  if (row) row.remove();
  const rowsEl = document.getElementById('savedRows');
  const countEl = document.getElementById('savedCount');
  const n = rowsEl ? rowsEl.querySelectorAll('.ws-row').length : 0;
  if (countEl) countEl.textContent = n ? `${n} saved` : '';
  if (!n) { const s = document.getElementById('savedSection'); if (s) s.style.display = 'none'; }
}

async function loadDownloadHistory() {
  const section = document.getElementById('dlHistorySection');
  const rowsEl = document.getElementById('dlHistoryRows');
  if (!section || !rowsEl) return;
  const { data: dls, error } = await sb2.from('user_downloads')
    .select('worksheet_id, last_at')
    .order('last_at', { ascending: false })
    .limit(12);
  if (error || !dls || !dls.length) return;
  const ws = await _fetchWorksheetsByIds(dls.map(d => d.worksheet_id));
  if (!ws.length) return;
  rowsEl.innerHTML = ws.map(w => _wsRowHtml(w, {})).join('');
  section.style.display = '';
}

document.addEventListener('DOMContentLoaded', loadProfile);