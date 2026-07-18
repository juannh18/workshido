// Workshido mascot — a little walking character that crosses the screen on
// special dates (or on demand via ?fiesta=1 / window.showMascot()). On
// holidays it wears a small accessory instead of a full new costume, so it
// stays festive without needing a redrawn character for every date.
(function () {
  const HOLIDAYS = [
    { m: 1, d: 1, label: '¡Feliz Año Nuevo! 🎉', accessory: 'newyear' },
    { m: 2, d: 14, label: '¡Feliz San Valentín! 💙', accessory: 'valentine' },
    { m: 5, d: 15, label: '¡Feliz Día del Maestro! 🍎', accessory: 'teacher' },
    { m: 10, d: 31, label: '¡Feliz Halloween! 🎃', accessory: 'halloween' },
    { m: 12, d: 24, label: '¡Feliz Navidad! 🎄', accessory: 'christmas' },
    { m: 12, d: 25, label: '¡Feliz Navidad! 🎄', accessory: 'christmas' },
  ];

  // Small SVG fragments layered on top of the base character — a hat or a
  // held prop, not a full outfit redraw, so quality stays consistent.
  const ACCESSORIES = {
    newyear: `
      <path d="M30 1 L20 17 L40 17 Z" fill="#e67e22"/>
      <path d="M30 1 L34.5 17 L25.5 17 Z" fill="#ffd166" opacity="0.85"/>
      <circle cx="30" cy="1" r="2.6" fill="#ffd166"/>`,
    valentine: `
      <path d="M30 6 C28 2 22 2 22 7 C22 11 26 14 30 18 C34 14 38 11 38 7 C38 2 32 2 30 6 Z" fill="#e0567a"/>`,
    teacher: `
      <circle cx="54" cy="30" r="4.5" fill="#c0392b"/>
      <rect x="53" y="24" width="2" height="4" fill="#6b4226"/>
      <path d="M55 25 Q58.5 23.5 57.5 27" fill="#2e7d32"/>`,
    halloween: `
      <ellipse cx="30" cy="18" rx="16" ry="3.2" fill="#1a1a2e"/>
      <path d="M30 -1 L22 18.5 L38 18.5 Z" fill="#1a1a2e"/>
      <rect x="24" y="11" width="12" height="3" fill="#6a4c93"/>`,
    christmas: `
      <path d="M14 18 Q30 -3 46 14 L44 20 L16 20 Z" fill="#c0392b"/>
      <rect x="13" y="17" width="34" height="5" rx="2.5" fill="#ffffff"/>
      <circle cx="45" cy="10" r="4" fill="#ffffff"/>`,
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
      .ws-mascot-legs { transform-origin: 30px 46px; animation: wsMascotStep 0.38s steps(2) infinite; }
      @keyframes wsMascotStep { 0% { transform: rotate(0deg); } 50% { transform: rotate(10deg); } 100% { transform: rotate(-10deg); } }
      .ws-mascot-arm { transform-origin: 42px 36px; animation: wsMascotWave 0.6s ease-in-out infinite alternate; }
      @keyframes wsMascotWave { from { transform: rotate(-10deg); } to { transform: rotate(18deg); } }
      .ws-mascot-bubble { position: absolute; bottom: 66px; left: 50%; transform: translateX(-50%) scale(0.6); background: #1a3a5c; color: #fff; padding: 6px 11px; border-radius: 10px; font: 700 12px Arial, sans-serif; white-space: nowrap; opacity: 0; transition: opacity .3s, transform .3s; }
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
        <ellipse cx="30" cy="66" rx="14" ry="3" fill="rgba(0,0,0,0.12)"/>
        <g class="ws-mascot-legs">
          <rect x="20" y="46" width="7" height="16" rx="3" fill="#1a3a5c"/>
          <rect x="33" y="46" width="7" height="16" rx="3" fill="#1a3a5c"/>
        </g>
        <circle cx="30" cy="30" r="20" fill="#e8f4f1" stroke="#0e7c66" stroke-width="2"/>
        <path d="M12 26 a18 12 0 0 1 36 0 z" fill="#0e7c66"/>
        <rect x="10" y="24" width="40" height="4" rx="2" fill="#e67e22"/>
        <circle cx="23" cy="31" r="1.8" fill="#1a3a5c"/>
        <circle cx="37" cy="31" r="1.8" fill="#1a3a5c"/>
        <g fill="none" stroke="#1a3a5c" stroke-width="1.6">
          <circle cx="23" cy="31" r="5"/>
          <circle cx="37" cy="31" r="5"/>
          <line x1="28" y1="31" x2="32" y2="31"/>
          <line x1="18" y1="30" x2="14.5" y2="28.5"/>
          <line x1="42" y1="30" x2="45.5" y2="28.5"/>
        </g>
        <path d="M22 39 Q30 45 38 39" stroke="#1a3a5c" stroke-width="2.2" fill="none" stroke-linecap="round"/>
        <g class="ws-mascot-arm">
          <rect x="42" y="34" width="12" height="5" rx="2.5" fill="#1a3a5c"/>
          <rect x="49" y="30" width="10" height="8" rx="1.2" fill="#e67e22"/>
          <line x1="54" y1="31.3" x2="54" y2="36.7" stroke="#fff" stroke-width="1"/>
        </g>
        ${accessorySvg}
      </svg>
    `;
    document.body.appendChild(wrap);
    const bubble = document.getElementById('wsMascotBubble');
    bubble.textContent = label || '¡Hola! 👋';
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
      setTimeout(() => spawnMascot(h ? h.label : '¡Hola! 👋', h && h.accessory), 1200);
    }
  });
})();
