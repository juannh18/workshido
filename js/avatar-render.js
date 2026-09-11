// Shared avatar renderer. profiles.avatar is one of:
//   "dicebear:<query-string>"   Avataaars character  -> <img> to api.dicebear.com
//   "<emoji>|<colourkey>"       quick icon           -> coloured <span>
//   null / anything else        -> Google photo, then initials
// Returns the INNER html for a round avatar container (the container itself
// must be sized, round and overflow:hidden by the caller).
(function () {
  var DB = 'https://api.dicebear.com/9.x/avataaars/svg?';
  var COLS = { blue:'#DCEBFB', teal:'#D3F0E6', amber:'#FBEAD0', pink:'#FBDDEC', purple:'#E7E5FB', coral:'#FADDD2', green:'#E4F1D3', slate:'#E6EBF1' };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;' })[c]; }); }
  window.wsNavAvatar = function (avatarStr, googlePic, initials) {
    if (avatarStr && avatarStr.indexOf('dicebear:') === 0) {
      return '<img src="' + DB + esc(avatarStr.slice(9)) + '" alt="" style="width:100%;height:100%;border-radius:50%;display:block;">';
    }
    if (avatarStr && avatarStr.indexOf('dicebear:') !== 0 && avatarStr.indexOf('|') > 0) {
      var i = avatarStr.lastIndexOf('|'), e = avatarStr.slice(0, i), c = avatarStr.slice(i + 1);
      if (COLS[c]) {
        return '<span style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:' + COLS[c] + ';border-radius:50%;font-size:16px;line-height:1;">' + esc(e) + '</span>';
      }
    }
    if (googlePic) {
      return '<img src="' + esc(googlePic) + '" referrerpolicy="no-referrer" alt="" style="width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;">';
    }
    return esc(initials);
  };
})();
