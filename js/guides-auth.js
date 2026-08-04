const sbGuides = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
async function checkAuthGuides() {
  const { data: { user } } = await sbGuides.auth.getUser();
  const nav = document.getElementById('navActions');
  if (user && nav) {
    const name = user.user_metadata?.full_name || user.email;
    const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    // full_name is free text the user set at signup — never trust it as safe
    // HTML when it lands back in innerHTML.
    const escNav = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    nav.innerHTML = '<a href="/workshido-profile.html" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:#B5D4F4;font-size:13px;font-weight:500;"><div style="width:32px;height:32px;border-radius:50%;background:#E6F1FB;color:#185FA5;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;border:2px solid #85B7EB;">' + escNav(initials) + '</div>' + escNav(name.split(' ')[0]) + '</a><button onclick="logOutGuides()" style="background:transparent;border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:7px 14px;color:#B5D4F4;font-size:13px;cursor:pointer;font-family:inherit;">Log out</button>';
  }
}
async function logOutGuides() { await sbGuides.auth.signOut(); window.location.reload(); }
document.addEventListener('DOMContentLoaded', checkAuthGuides);
