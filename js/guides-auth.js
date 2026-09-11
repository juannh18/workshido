// Auth-aware nav for the /guides pages and other pages that load this file.
// Swaps the "Log in / Sign up" actions for the signed-in user's avatar + name.
const sbGuides = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');

const _GB_DB = 'https://api.dicebear.com/9.x/avataaars/svg?';
const _GB_COLS = { blue:'#DCEBFB', teal:'#D3F0E6', amber:'#FBEAD0', pink:'#FBDDEC', purple:'#E7E5FB', coral:'#FADDD2', green:'#E4F1D3', slate:'#E6EBF1' };
function _gbEsc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' }[c])); }
function _gbAvatarInner(avatarStr, googlePic, initials) {
  if (avatarStr && avatarStr.indexOf('dicebear:') === 0)
    return '<img src="' + _GB_DB + _gbEsc(avatarStr.slice(9)) + '" alt="" style="width:100%;height:100%;border-radius:50%;display:block;">';
  if (avatarStr && avatarStr.indexOf('dicebear:') !== 0 && avatarStr.indexOf('|') > 0) {
    const i = avatarStr.lastIndexOf('|'), e = avatarStr.slice(0, i), c = avatarStr.slice(i + 1);
    if (_GB_COLS[c])
      return '<span style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:' + _GB_COLS[c] + ';border-radius:50%;font-size:16px;line-height:1;">' + _gbEsc(e) + '</span>';
  }
  if (googlePic)
    return '<img src="' + _gbEsc(googlePic) + '" referrerpolicy="no-referrer" alt="" style="width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;">';
  return _gbEsc(initials);
}

async function checkAuthGuides() {
  const { data: { user } } = await sbGuides.auth.getUser();
  const nav = document.getElementById('navActions');
  if (!user || !nav) return;
  let pa = {};
  try { pa = (await sbGuides.from('profiles').select('avatar, display_name').eq('id', user.id).maybeSingle()).data || {}; } catch (e) {}
  const name = (pa.display_name || user.user_metadata?.full_name || user.email || '').trim();
  const initials = name.split(/\s+/).filter(Boolean).map(n => n[0]).join('').toUpperCase().slice(0, 2);
  const pic = user.user_metadata?.avatar_url || user.user_metadata?.picture || '';
  const inner = _gbAvatarInner(pa.avatar, pic, initials);
  nav.innerHTML = '<a href="/workshido-profile.html" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:#B5D4F4;font-size:13px;font-weight:500;">'
    + '<div style="width:32px;height:32px;border-radius:50%;overflow:hidden;background:#E6F1FB;color:#185FA5;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;border:2px solid #85B7EB;flex-shrink:0;">' + inner + '</div>'
    + _gbEsc(name.split(/\s+/)[0]) + '</a>'
    + '<button onclick="logOutGuides()" style="background:transparent;border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:7px 14px;color:#B5D4F4;font-size:13px;cursor:pointer;font-family:inherit;">Log out</button>';
}
async function logOutGuides() { await sbGuides.auth.signOut(); window.location.reload(); }
document.addEventListener('DOMContentLoaded', checkAuthGuides);
