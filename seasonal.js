// Halloween bats — a swarm bursts out of the hero moon, crosses the screen
// and is gone in ~4 s. Once per visit (sessionStorage), so moving between the
// home page and the catalog doesn't replay it. Only while the <head> script
// has put theme-halloween on <html>; skipped for prefers-reduced-motion.
// Styles: .hw-swarm / .hw-flyer in /seasonal.css.
(function () {
  if (!document.documentElement.classList.contains('theme-halloween')) return;
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const replay = /[?&]bats=1\b/.test(location.search);   // ?bats=1 forces it, for previewing
  try {
    if (!replay && sessionStorage.getItem('hwBatsSeen')) return;
    sessionStorage.setItem('hwBatsSeen', '1');
  } catch (e) { /* storage blocked: just show it */ }

  const BAT = '<svg viewBox="0 0 64 28"><g class="hw-wings">'
    + '<path d="M29 13C24 5 14 1 2 4c3 4 5 8 4 13 4-3 8-2 10 2 3-3 7-3 9 1 2-3 3-4 4-3z"/>'
    + '<path d="M35 13c5-8 15-12 27-9-3 4-5 8-4 13-4-3-8-2-10 2-3-3-7-3-9 1-2-3-3-4-4-3z"/></g>'
    + '<ellipse cx="32" cy="16" rx="4" ry="7"/><circle cx="32" cy="11" r="3.6"/>'
    + '<path d="M29 10 28.5 4l3 5zM35 10l.5-6-3 5z"/></svg>';

  function launch() {
    const W = window.innerWidth, H = window.innerHeight;
    const moon = document.querySelector('.hero .hw-moon');
    const r = moon && moon.getBoundingClientRect();
    const ox = r && r.width ? r.left + r.width / 2 : W * 0.85;
    const oy = r && r.width ? r.top + r.height / 2 : 90;
    const rnd = (a, b) => a + Math.random() * (b - a);

    const layer = document.createElement('div');
    layer.className = 'hw-swarm';
    layer.setAttribute('aria-hidden', 'true');
    const n = W < 600 ? 6 : 9;
    let longest = 0;
    for (let i = 0; i < n; i++) {
      const s = rnd(W < 600 ? 38 : 50, W < 600 ? 58 : 86);
      // Exit off the left, top or bottom edge, spread so the bats fan out.
      const side = i % 3;
      const x1 = side === 0 ? -s - 40 : rnd(0, W * 0.75);
      const y1 = side === 0 ? rnd(0, H) : side === 1 ? -s - 40 : H + 40;
      const mx = (ox + x1) / 2 + rnd(-140, 140);
      const my = (oy + y1) / 2 + rnd(-110, 110);
      const d = i * 110 + rnd(0, 120);
      const t = rnd(2800, 3700);
      longest = Math.max(longest, d + t);
      const f = document.createElement('div');
      f.className = 'hw-flyer';
      f.style.cssText = `--s:${s.toFixed(0)}px;--x0:${(ox - s / 2).toFixed(0)}px;--y0:${(oy - s / 4).toFixed(0)}px;`
        + `--mx:${mx.toFixed(0)}px;--my:${my.toFixed(0)}px;--x1:${x1.toFixed(0)}px;--y1:${y1.toFixed(0)}px;`
        + `--d:${d.toFixed(0)}ms;--t:${t.toFixed(0)}ms;--flap:${rnd(0.16, 0.24).toFixed(2)}s`;
      f.innerHTML = BAT;
      layer.appendChild(f);
    }
    document.body.appendChild(layer);
    setTimeout(() => layer.remove(), longest + 300);
  }

  // Deferred script: the DOM is parsed. A short pause lets the hero paint first.
  setTimeout(launch, 700);
})();
