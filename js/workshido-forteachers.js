const sb = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
async function checkAuth() {
  const { data: { user } } = await sb.auth.getUser();
  const uploadLink = document.getElementById('navUploadLink');
  if (uploadLink) uploadLink.style.display = (user?.email === 'juanda.5790@hotmail.com') ? '' : 'none';
  const nav = document.getElementById('navActions');
  if (user && nav) {
    const name = user.user_metadata?.full_name || user.email;
    const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    // full_name is free text the user set at signup — never trust it as safe
    // HTML when it lands back in innerHTML.
    const escNav = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    nav.innerHTML = '<a href="workshido-profile.html" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:#B5D4F4;font-size:13px;font-weight:500;"><div style="width:32px;height:32px;border-radius:50%;background:#E6F1FB;color:#185FA5;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;border:2px solid #85B7EB;">' + escNav(initials) + '</div>' + escNav(name.split(' ')[0]) + '</a><button onclick="logOut()" style="background:transparent;border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:7px 14px;color:#B5D4F4;font-size:13px;cursor:pointer;font-family:inherit;">Log out</button>';
  }
}
async function logOut() { await sb.auth.signOut(); window.location.reload(); }

// Honest, live numbers from the real catalog
async function loadLiveStats() {
  const { data, error } = await sb.from('worksheets').select('level');
  if (error || !data || !data.length) return;
  // Count rounds down to marketing milestones (100+, 150+, 200+...),
  // so it is never overstated past 100
  const MILESTONES = [100, 150, 200, 300, 500, 750, 1000, 1500, 2000, 3000, 5000, 10000];
  let best = MILESTONES[0];
  for (const m of MILESTONES) if (data.length >= m) best = m;
  const rounded = best.toLocaleString('en-US') + '+';
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