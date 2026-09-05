// Asks logged-in users who never answered the marketing opt-in (Google
// sign-up skips the signup form, so they never saw the checkbox) — shown
// once per session, never blocking, and the decision (yes or no) is written
// via the set_marketing_consent RPC so we keep a timestamped consent record
// either way instead of nagging on every visit.
(function () {
  const SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co';
  const SUPABASE_KEY = 'sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo';
  const CONSENT_VERSION = 'v1';
  const sbConsent = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

  function showBanner() {
    if (document.getElementById('marketingConsentBanner')) return;
    const bar = document.createElement('div');
    bar.id = 'marketingConsentBanner';
    bar.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:9999;background:#042C53;color:#fff;padding:14px 20px;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:14px;font-family:Inter,sans-serif;font-size:13px;line-height:1.5;box-shadow:0 -2px 12px rgba(0,0,0,0.15);';
    bar.innerHTML =
      '<span style="max-width:520px;">Want new worksheets, teacher resources and offers from Workshido in your inbox? You can unsubscribe anytime.</span>' +
      '<span style="display:flex;gap:8px;flex-shrink:0;">' +
      '<button id="mcAccept" style="background:#1D9E75;color:#fff;border:none;border-radius:6px;padding:8px 16px;font-weight:600;cursor:pointer;font-family:inherit;font-size:13px;">Yes, sign me up</button>' +
      '<button id="mcDismiss" style="background:transparent;color:#B5D4F4;border:1px solid rgba(255,255,255,0.25);border-radius:6px;padding:8px 16px;cursor:pointer;font-family:inherit;font-size:13px;">No thanks</button>' +
      '</span>';
    document.body.appendChild(bar);

    async function answer(consent) {
      const buttons = bar.querySelectorAll('button');
      buttons.forEach(b => b.disabled = true);
      const { error } = await sbConsent.rpc('set_marketing_consent', { p_consent: consent, p_version: CONSENT_VERSION, p_source: 'post_login_banner' });
      if (error) {
        buttons.forEach(b => b.disabled = false);
        console.error('set_marketing_consent failed', error);
        return;
      }
      bar.remove();
    }
    document.getElementById('mcAccept').onclick = () => answer(true);
    document.getElementById('mcDismiss').onclick = () => answer(false);
  }

  sbConsent.auth.onAuthStateChange(async (_event, session) => {
    const user = session?.user;
    if (!user) return;
    const { data } = await sbConsent
      .from('profiles')
      .select('marketing_consent_at')
      .eq('id', user.id)
      .maybeSingle();
    if (data && data.marketing_consent_at == null) showBanner();
  });
})();
