const sb2 = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
const LEVEL_COLOR = { A1:'teal', A2:'blue', B1:'amber', B2:'purple', C1:'coral' };
const LEVEL_CLS   = { A1:'a1',   A2:'a2',  B1:'b1',   B2:'b2',    C1:'c1'    };
const THUMB_ACCENT = { teal:'t', blue:'b', amber:'am', purple:'b', coral:'t' };

async function logOut(){ await sb2.auth.signOut(); window.location.href='workshido-index.html'; }

function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

async function loadProfile() {
  const { data: { user } } = await sb2.auth.getUser();
  if (!user) { window.location.href = 'workshido-login.html'; return; }

  const uploadSection = document.getElementById('uploadSection');
  if (uploadSection) uploadSection.style.display = (user.email === 'juanda.5790@hotmail.com') ? '' : 'none';

  const name = user.user_metadata?.full_name || user.email;
  const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  document.querySelector('.avatar-big').textContent    = initials;
  document.querySelector('.profile-name').textContent  = name;
  document.querySelector('.profile-email').textContent = user.email;
  document.querySelector('.nav-avatar').textContent    = initials;
  document.querySelector('.plan-badge').textContent    = '✓ Free';

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

document.addEventListener('DOMContentLoaded', loadProfile);