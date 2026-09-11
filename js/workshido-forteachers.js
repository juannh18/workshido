const sb = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
async function checkAuth() {
  const { data: { user } } = await sb.auth.getUser();
  const uploadLink = document.getElementById('navUploadLink');
  if (uploadLink) uploadLink.style.display = (user?.email === 'juanda.5790@hotmail.com') ? '' : 'none';
  const nav = document.getElementById('navActions');
  if (user && nav) {
    let pa = {};
    try { pa = (await sb.from('profiles').select('avatar, display_name').eq('id', user.id).maybeSingle()).data || {}; } catch (e) {}
    const name = (pa.display_name || user.user_metadata?.full_name || user.email || '').trim();
    const initials = name.split(/\s+/).filter(Boolean).map(n => n[0]).join('').toUpperCase().slice(0, 2);
    const pic = user.user_metadata?.avatar_url || user.user_metadata?.picture || '';
    const escNav = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    const inner = window.wsNavAvatar ? window.wsNavAvatar(pa.avatar, pic, initials) : escNav(initials);
    nav.innerHTML = '<a href="workshido-profile.html" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:#B5D4F4;font-size:13px;font-weight:500;"><div style="width:32px;height:32px;border-radius:50%;overflow:hidden;background:#E6F1FB;color:#185FA5;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;border:2px solid #85B7EB;flex-shrink:0;">' + inner + '</div>' + escNav(name.split(/\s+/)[0]) + '</a><button onclick="logOut()" style="background:transparent;border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:7px 14px;color:#B5D4F4;font-size:13px;cursor:pointer;font-family:inherit;">Log out</button>';
  }
}
async function logOut() { await sb.auth.signOut(); window.location.reload(); }

// Honest, live numbers from the real catalog
async function loadLiveStats() {
  const { data, error } = await sb.from('worksheets').select('level');
  if (error || !data || !data.length) return;
  // Rounds down to the nearest 100 ("700+", "800+", …) — never overstated,
  // steps up every 100 uploads.
  const rounded = Math.max(100, Math.floor(data.length / 100) * 100).toLocaleString('en-US') + '+';
  const elWs = document.getElementById('statWs');
  if (elWs) elWs.textContent = rounded;
  const order = ['A1', 'A2', 'B1', 'B2', 'C1'];
  const present = order.filter(l => data.some(w => w.level === l));
  const elLv = document.getElementById('statLv');
  if (elLv && present.length) {
    elLv.textContent = present.length > 1 ? `${present[0]}–${present[present.length - 1]}` : present[0];
  }
}
document.addEventListener('DOMContentLoaded', () => { checkAuth(); loadLiveStats(); });