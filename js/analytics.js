// Lightweight first-party analytics — no third-party script, no cookies,
// no consent banner needed (nothing is shared with an outside company).
// Events land in the analytics_events table (insert-only from the client;
// see the "anon can insert events" RLS policy) and are queried later via
// the Supabase dashboard or a service-role script, never read back here.
(function () {
  const ENDPOINT = 'https://mhbgxdsdaalvtgobnvbh.supabase.co/rest/v1/analytics_events';
  const ANON_KEY = 'sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo';

  function sessionId() {
    try {
      let id = sessionStorage.getItem('ws_sid');
      if (!id) {
        id = (crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).slice(2)}`);
        sessionStorage.setItem('ws_sid', id);
      }
      return id;
    } catch (e) {
      return null; // sessionStorage blocked (private mode, etc.) — event still sends, just without a session id
    }
  }

  // Country from Netlify's edge geo (netlify/edge-functions/geo.js) —
  // fetched once per session and cached, same lifetime as the session id.
  // Best-effort: if the fetch fails or is still pending, events just go
  // out with country: null rather than waiting on it.
  let country = null;
  try {
    const cached = sessionStorage.getItem('ws_country');
    if (cached) country = JSON.parse(cached);
  } catch (e) { /* private mode, etc. — fall through to fetching fresh */ }
  if (!country) {
    fetch('/api/geo').then((r) => r.json()).then((geo) => {
      country = geo;
      try { sessionStorage.setItem('ws_country', JSON.stringify(geo)); } catch (e) {}
    }).catch(() => {});
  }

  function track(eventName, properties) {
    try {
      const body = JSON.stringify({
        event_name: eventName,
        properties: { ...(properties || {}), country_code: country?.code || null, country_name: country?.name || null },
        session_id: sessionId(),
        path: location.pathname + location.search,
        referrer: document.referrer || null,
      });
      const url = `${ENDPOINT}`;
      const headers = { 'Content-Type': 'application/json', apikey: ANON_KEY, Authorization: `Bearer ${ANON_KEY}` };
      // sendBeacon can't set custom headers, so Supabase's REST insert (which
      // requires the apikey header) has to go through fetch with keepalive —
      // that still survives page unload/navigation like a beacon would.
      fetch(url, { method: 'POST', headers, body, keepalive: true }).catch(() => {});
    } catch (e) {
      // analytics must never break the page
    }
  }

  window.wsTrack = track;

  // Auto page view on load
  track('page_view', { title: document.title });

  // Web Vitals — LCP and CLS captured directly via PerformanceObserver
  // instead of pulling in the ~2KB web-vitals library, since we only need
  // two numbers, not the full attribution API.
  try {
    let lcp = null;
    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      lcp = entries[entries.length - 1];
    }).observe({ type: 'largest-contentful-paint', buffered: true });

    let cls = 0;
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) cls += entry.value;
      }
    }).observe({ type: 'layout-shift', buffered: true });

    const sendVitals = () => {
      const nav = performance.getEntriesByType('navigation')[0];
      track('web_vitals', {
        lcp_ms: lcp ? Math.round(lcp.startTime) : null,
        cls: Math.round(cls * 1000) / 1000,
        ttfb_ms: nav ? Math.round(nav.responseStart) : null,
        load_ms: nav ? Math.round(nav.loadEventEnd) : null,
      });
    };
    // Fire once the page is hidden (tab switch/close/navigate away) — that's
    // when LCP/CLS have their final values, not on load.
    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') sendVitals();
    }, { once: true });
  } catch (e) {
    // PerformanceObserver entry types not supported in this browser — skip vitals, page views still work
  }

  // 404 pages should self-report — the page id is set inline where used
  if (document.body?.dataset?.page === '404') {
    track('404_viewed', { path: location.pathname });
  }
})();
