// Workshido mascot — a little walking character that crosses the screen on
// special dates (or on demand via ?fiesta=1 / window.showMascot()). On
// holidays it wears a small accessory instead of a full new costume, so it
// stays festive without needing a redrawn character for every date.
(function () {
  const HOLIDAYS = [
    { m: 1, d: 1, label: 'Happy New Year! 🎉', accessory: 'newyear' },
    { m: 2, d: 14, label: 'Happy Valentine\'s Day! 💙', accessory: 'valentine' },
    { m: 5, d: 15, label: 'Happy Teachers\' Day! 🍎', accessory: 'teacher' },
    { m: 10, d: 31, label: 'Happy Halloween! 🎃', accessory: 'halloween' },
    { m: 12, d: 24, label: 'Merry Christmas! 🎄', accessory: 'christmas' },
    { m: 12, d: 25, label: 'Merry Christmas! 🎄', accessory: 'christmas' },
  ];

  // Small SVG fragments layered on top of the base character — a hat or a
  // held prop, not a full outfit redraw, so quality stays consistent.
  // Positioned relative to the head (cx=30, cy=20, r=14) or the free hand (~10,42).
  const ACCESSORIES = {
    newyear: `
      <path d="M30 -6 L23 8 L37 8 Z" fill="#e67e22"/>
      <path d="M30 -6 L32.5 8 L27.5 8 Z" fill="#ffd166" opacity="0.85"/>
      <circle cx="30" cy="-6" r="2.2" fill="#ffd166"/>`,
    valentine: `
      <path d="M30 2 C28.5 -0.5 24 -0.5 24 2.5 C24 5 27 7 30 9.5 C33 7 36 5 36 2.5 C36 -0.5 31.5 -0.5 30 2 Z" fill="#e0567a"/>`,
    teacher: `
      <circle cx="10" cy="40" r="4" fill="#c0392b"/>
      <rect x="9" y="35" width="1.6" height="3.2" fill="#6b4226"/>
      <path d="M11 36 Q13.5 35 12.7 38" fill="#2e7d32"/>`,
    halloween: `
      <ellipse cx="30" cy="8" rx="11" ry="2.2" fill="#1a1a2e"/>
      <path d="M30 -7 L24 8.5 L36 8.5 Z" fill="#1a1a2e"/>
      <rect x="26" y="4" width="8" height="2" fill="#6a4c93"/>`,
    christmas: `
      <path d="M19 8 Q30 -6 41 6 L39 10 L21 10 Z" fill="#c0392b"/>
      <rect x="18" y="7" width="24" height="3.5" rx="1.7" fill="#ffffff"/>
      <circle cx="40" cy="1" r="2.8" fill="#ffffff"/>`,
  };

  function todayHoliday() {
    const now = new Date();
    return HOLIDAYS.find(h => h.m === now.getMonth() + 1 && h.d === now.getDate());
  }

  function injectStyles() {
    if (document.getElementById('wsMascotStyles')) return;
    const style = document.createElement('style');
    style.id = 'wsMascotStyles';
    style.textContent = `
      #wsMascot { position: fixed; bottom: 0; left: -80px; z-index: 9999; pointer-events: none; animation: wsMascotWalk 13s linear forwards; }
      @keyframes wsMascotWalk { from { left: -80px; } to { left: 105%; } }
      .ws-mascot-legs { transform-origin: 30px 54px; animation: wsMascotStep 0.38s steps(2) infinite; }
      @keyframes wsMascotStep { 0% { transform: rotate(0deg); } 50% { transform: rotate(10deg); } 100% { transform: rotate(-10deg); } }
      .ws-mascot-arm { transform-origin: 47px 42px; animation: wsMascotWave 0.6s ease-in-out infinite alternate; }
      @keyframes wsMascotWave { from { transform: rotate(-8deg); } to { transform: rotate(16deg); } }
      .ws-mascot-bubble { position: absolute; bottom: 72px; left: 50%; transform: translateX(-50%) scale(0.6); background: #1a3a5c; color: #fff; padding: 6px 11px; border-radius: 10px; font: 700 12px Arial, sans-serif; white-space: nowrap; opacity: 0; transition: opacity .3s, transform .3s; }
      .ws-mascot-bubble.show { opacity: 1; transform: translateX(-50%) scale(1); }
      .ws-mascot-bubble::after { content: ''; position: absolute; top: 100%; left: 50%; margin-left: -5px; border: 5px solid transparent; border-top-color: #1a3a5c; }
      @media (prefers-reduced-motion: reduce) { #wsMascot { animation-duration: 26s; } }
    `;
    document.head.appendChild(style);
  }

  function spawnMascot(label, accessoryKey) {
    if (document.getElementById('wsMascot')) return;
    injectStyles();
    const accessorySvg = ACCESSORIES[accessoryKey] || '';
    const wrap = document.createElement('div');
    wrap.id = 'wsMascot';
    wrap.innerHTML = `
      <div class="ws-mascot-bubble" id="wsMascotBubble"></div>
      <svg viewBox="0 0 60 70" width="52" height="60">
        <ellipse cx="30" cy="68" rx="14" ry="2.4" fill="rgba(0,0,0,0.12)"/>

        <!-- legs -->
        <g class="ws-mascot-legs">
          <rect x="20" y="54" width="7" height="13" rx="3" fill="#1a3a5c"/>
          <rect x="33" y="54" width="7" height="13" rx="3" fill="#1a3a5c"/>
        </g>

        <!-- torso (a body distinct from the head, so it doesn't read as a floating wheel) -->
        <rect x="15" y="34" width="30" height="22" rx="11" fill="#1a3a5c"/>
        <rect x="24" y="36" width="12" height="8" rx="2" fill="#e67e22"/>

        <!-- left arm, resting -->
        <rect x="6" y="39" width="12" height="6" rx="3" fill="#1a3a5c"/>

        <!-- right arm, waving, holding a small book -->
        <g class="ws-mascot-arm">
          <rect x="42" y="39" width="12" height="6" rx="3" fill="#1a3a5c"/>
          <rect x="50" y="34" width="9" height="7" rx="1" fill="#e67e22"/>
          <line x1="54.5" y1="35.2" x2="54.5" y2="39.8" stroke="#fff" stroke-width="0.9"/>
        </g>

        <!-- head -->
        <circle cx="30" cy="20" r="14" fill="#e8f4f1" stroke="#0e7c66" stroke-width="2"/>
        <path d="M17 16 a13 8 0 0 1 26 0 z" fill="#0e7c66"/>
        <rect x="15" y="14.5" width="30" height="3" rx="1.5" fill="#e67e22"/>

        <!-- face: glasses with visible pupils, not just empty rings -->
        <g fill="none" stroke="#1a3a5c" stroke-width="1.4">
          <circle cx="25" cy="21" r="3.6"/>
          <circle cx="35" cy="21" r="3.6"/>
          <line x1="28.6" y1="21" x2="31.4" y2="21"/>
          <line x1="21.4" y1="20.3" x2="19" y2="19.2"/>
          <line x1="38.6" y1="20.3" x2="41" y2="19.2"/>
        </g>
        <circle cx="25" cy="21" r="1.2" fill="#1a3a5c"/>
        <circle cx="35" cy="21" r="1.2" fill="#1a3a5c"/>
        <path d="M24 26.5 Q30 30 36 26.5" stroke="#1a3a5c" stroke-width="1.6" fill="none" stroke-linecap="round"/>

        ${accessorySvg}
      </svg>
    `;
    document.body.appendChild(wrap);
    const bubble = document.getElementById('wsMascotBubble');
    bubble.textContent = label || 'Thank you for using Workshido! 👋';
    setTimeout(() => bubble.classList.add('show'), 1600);
    setTimeout(() => bubble.classList.remove('show'), 5500);
    setTimeout(() => wrap.remove(), 13500);
  }

  // Manual trigger from the console/devtools, any time — pass an accessory
  // key ('newyear'|'valentine'|'teacher'|'halloween'|'christmas') to preview
  // a costume outside its real date.
  window.showMascot = (label, accessoryKey) => {
    const h = todayHoliday();
    spawnMascot(label || (h || {}).label, accessoryKey || (h || {}).accessory);
  };

  document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const holiday = todayHoliday();
    const forcedKey = params.get('fiesta');
    const forcedHoliday = forcedKey && HOLIDAYS.find(h => h.accessory === forcedKey);
    if (holiday || params.has('fiesta')) {
      const h = forcedHoliday || holiday;
      setTimeout(() => spawnMascot(h ? h.label : 'Thank you for using Workshido! 👋', h && h.accessory), 1200);
    }
  });
})();
