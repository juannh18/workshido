// Lightweight first-party analytics — no third-party script, no cookies,
// no consent banner needed (nothing is shared with an outside company).
// Events land in the analytics_events table (insert-only from the client;
// see the "anon can insert events" RLS policy) and are queried later via
// the Supabase dashboard or a service-role script, never read back here.
(function () {
  // Known crawlers/bots/uptime monitors — without this, Googlebot rendering
  // JS pages (and similar) inflates session/page-view counts. wsTrack still
  // exists as a no-op so callers elsewhere on the site don't need a guard.
  const UA = navigator.userAgent || '';
  if (/bot|crawl|spider|slurp|facebookexternalhit|whatsapp|telegrambot|slackbot|discordbot|skypeuripreview|applebot|google-inspectiontool|adsbot|mediapartners|headlesschrome|phantomjs|pingdom|uptimerobot|gtmetrix|lighthouse|ahrefsbot|semrushbot|mj12bot|dotbot|petalbot|bingpreview/i.test(UA)) {
    window.wsTrack = function () {};
    return;
  }

  const ENDPOINT = 'https://mhbgxdsdaalvtgobnvbh.supabase.co/rest/v1/analytics_events';
  const ANON_KEY = 'sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo';

  // Own-testing flag — set once per browser/device via the console
  // (localStorage.setItem('ws_internal','1')) so Juan's manual QA sessions
  // can be filtered out of real-user analytics instead of skewing them.
  let isInternal = false;
  try { isInternal = localStorage.getItem('ws_internal') === '1'; } catch (e) {}

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

  // Coarse channel bucket for traffic that arrives with no UTM tag at all —
  // mirrors the CASE in the channel_funnel SQL view, so a session and the
  // signup it eventually produces land in the same bucket.
  function classifyReferrerChannel(referrer) {
    if (!referrer) return 'direct';
    let host;
    try { host = new URL(referrer).hostname.replace(/^www\./, '').toLowerCase(); } catch (e) { return 'direct'; }
    // Exact host / suffix match only — a substring test would match "t.co"
    // (Twitter's shortener) inside "chatgpt.com" and misclassify it.
    const is = (d) => host === d || host.endsWith('.' + d);
    if (host === location.hostname || is('workshido.com')) return 'direct';
    if (/(^|\.)google\.[a-z.]+$/.test(host) || is('bing.com') || is('duckduckgo.com') || /(^|\.)yahoo\.[a-z.]+$/.test(host)) return 'search_organic';
    if (is('facebook.com') || is('instagram.com')) return 'facebook_instagram_referral';
    if (/(^|\.)pinterest\.[a-z.]+$/.test(host)) return 'pinterest_referral';
    if (is('tiktok.com')) return 'tiktok_referral';
    if (is('youtube.com') || is('youtu.be')) return 'youtube_referral';
    if (is('chatgpt.com') || is('chat.openai.com') || is('perplexity.ai') || is('claude.ai') || is('copilot.microsoft.com') || is('gemini.google.com')) return 'ai_assistant_referral';
    if (is('twitter.com') || is('x.com') || is('t.co')) return 'twitter_referral';
    return 'other_referral';
  }
  const CHANNEL_ALIASES = { ig: 'instagram', fb: 'facebook' };

  // First-touch attribution — captured once per browser (localStorage, not
  // sessionStorage) and never overwritten: ws_utm holds the raw utm_* tags
  // when present; ws_channel is always set (utm_source when tagged, else the
  // referrer guess above), so every signup gets credited to a channel even
  // without a tagged link.
  try {
    if (!localStorage.getItem('ws_channel')) {
      const params = new URLSearchParams(location.search);
      const source = params.get('utm_source');
      if (source) {
        localStorage.setItem('ws_utm', JSON.stringify({
          source,
          medium: params.get('utm_medium') || null,
          campaign: params.get('utm_campaign') || null,
        }));
        const norm = source.toLowerCase();
        localStorage.setItem('ws_channel', CHANNEL_ALIASES[norm] || norm);
      } else {
        localStorage.setItem('ws_channel', classifyReferrerChannel(document.referrer));
      }
    }
  } catch (e) { /* private mode, etc. — attribution just won't be captured */ }

  // Persistent visitor id — survives across sessions (localStorage, not
  // sessionStorage) so repeat visits from the same browser can be told apart
  // from genuinely new traffic before someone registers.
  function visitorId() {
    try {
      let id = localStorage.getItem('ws_vid');
      if (!id) {
        id = (crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).slice(2)}`);
        localStorage.setItem('ws_vid', id);
      }
      return id;
    } catch (e) {
      return null;
    }
  }

  function track(eventName, properties) {
    try {
      const body = JSON.stringify({
        event_name: eventName,
        properties: { ...(properties || {}), country_code: country?.code || null, country_name: country?.name || null, is_internal: isInternal || undefined },
        session_id: sessionId(),
        visitor_id: visitorId(),
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
