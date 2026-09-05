  let currentBilling = 'monthly';
  let userIsPremium = false;
  let portalUrl = null;

  function renderPremiumCta() {
    const premiumCta = document.getElementById('premiumCta');
    const microcopy = document.querySelector('.cta-microcopy');
    if (!premiumCta) return;
    if (userIsPremium) {
      premiumCta.textContent = "You're Premium ✓ — Manage subscription";
      premiumCta.onclick = () => {
        if (portalUrl) window.open(portalUrl, '_blank', 'noopener');
        else window.location.href = 'workshido-profile.html';
      };
      if (microcopy) microcopy.textContent = 'You already have full access to the Teacher Edition';
    } else {
      premiumCta.onclick = () => startCheckout(currentBilling);
      premiumCta.textContent = currentBilling === 'monthly'
        ? 'Unlock Teacher Edition — $2.99/mo'
        : 'Unlock Teacher Edition — $24.99/yr';
      if (microcopy) microcopy.textContent = '🔒 Secure checkout · Cancel anytime · Instant access';
    }
  }

  function setBilling(type) {
    currentBilling = type;
    const monthlyBtn = document.getElementById('monthlyBtn');
    const yearlyBtn = document.getElementById('yearlyBtn');
    const premiumPrice = document.getElementById('premiumPrice');
    const premiumNote = document.getElementById('premiumNote');

    if (type === 'monthly') {
      monthlyBtn.classList.add('active');
      yearlyBtn.classList.remove('active');
      premiumPrice.textContent = '$2.99';
      premiumNote.innerHTML = 'Billed monthly · Cancel anytime';
    } else {
      yearlyBtn.classList.add('active');
      monthlyBtn.classList.remove('active');
      premiumPrice.textContent = '$2.08';
      premiumNote.innerHTML = '<strong style="color:var(--teal-400)">Save $10.89/year</strong> · Billed as $24.99/yr';
    }
    renderPremiumCta();
  }

  function toggleFaq(el) {
    const answer = el.nextElementSibling;
    const chevron = el.querySelector('.faq-chevron');
    answer.classList.toggle('open');
    chevron.classList.toggle('open');
  }

const sb2 = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
async function checkAuth2(){
  const {data:{user}} = await sb2.auth.getUser();
  const uploadLink = document.getElementById('navUploadLink');
  if (uploadLink) uploadLink.style.display = (user?.email === 'juanda.5790@hotmail.com') ? '' : 'none';
  const nav = document.getElementById('navActions');
  if(user && nav){
    const name = user.user_metadata?.full_name || user.email;
    const initials = name.split(' ').map(n=>n[0]).join('').toUpperCase().slice(0,2);
    // full_name is free text the user set at signup — never trust it as safe
    // HTML when it lands back in innerHTML.
    const escNav = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    nav.innerHTML = '<a href="workshido-profile.html" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:#B5D4F4;font-size:13px;font-weight:500;"><div style="width:32px;height:32px;border-radius:50%;background:#E6F1FB;color:#185FA5;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;border:2px solid #85B7EB;">'+escNav(initials)+'</div>'+escNav(name.split(' ')[0])+'</a><button onclick="logOut2()" style="background:transparent;border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:7px 14px;color:#B5D4F4;font-size:13px;cursor:pointer;font-family:inherit;">Log out</button>';
  }
  if (user) {
    const { data: profile } = await sb2.from('profiles').select('is_premium, lemon_portal_url').eq('id', user.id).maybeSingle();
    userIsPremium = !!profile?.is_premium;
    portalUrl = profile?.lemon_portal_url || null;
    renderPremiumCta();
  }
  handleCheckoutReturn(user);
}

// Lemon Squeezy redirects back here with ?success=1 right after payment, but
// the webhook that flips profiles.is_premium runs async — it's usually
// already there, but can lag a few seconds. Poll briefly instead of leaving
// the payer looking at the same "Unlock" button they just paid to get rid of.
async function handleCheckoutReturn(user) {
  if (new URLSearchParams(window.location.search).get('success') !== '1') return;
  history.replaceState(null, '', window.location.pathname);
  const banner = document.getElementById('successBanner');
  if (!banner || !user) return;
  banner.style.display = 'block';
  if (userIsPremium) {
    banner.textContent = "🎉 Payment received — you're Premium! Full Teacher Edition access is unlocked.";
    return;
  }
  banner.textContent = '🎉 Payment received — activating your Premium access…';
  for (let i = 0; i < 6; i++) {
    await new Promise((r) => setTimeout(r, 2000));
    const { data: profile } = await sb2.from('profiles').select('is_premium, lemon_portal_url').eq('id', user.id).maybeSingle();
    if (profile?.is_premium) {
      userIsPremium = true;
      portalUrl = profile?.lemon_portal_url || null;
      renderPremiumCta();
      banner.textContent = "🎉 Payment received — you're Premium! Full Teacher Edition access is unlocked.";
      return;
    }
  }
  banner.textContent = "🎉 Payment received! It's taking a little longer than usual to activate — refresh this page in a minute.";
}
async function logOut2(){await sb2.auth.signOut();window.location.reload();}

// Reflect the CEFR range actually in the catalog (same source of truth as
// workshido-index.html's live stats) instead of a hand-typed range that can
// drift from reality and overclaim levels that don't exist yet.
async function updateLevelRange(){
  const { data, error } = await sb2.from('worksheets').select('level');
  if (error || !data || !data.length) return;
  const order = ['A1','A2','B1','B2','C1'];
  const present = order.filter(l => data.some(w => w.level === l));
  const el = document.getElementById('pricingLevelRange');
  if (el && present.length) el.textContent = present.length > 1 ? `all levels ${present[0]}–${present[present.length-1]}` : `all ${present[0]} worksheets`;
}
updateLevelRange();

async function startCheckout(plan) {
  const { data: { session } } = await sb2.auth.getSession();
  if (!session) {
    window.location.href = 'workshido-login.html?redirect=' + encodeURIComponent(window.location.href);
    return;
  }
  window.wsTrack?.('checkout_started', { plan });
  try {
    const res = await fetch('/.netlify/functions/create-checkout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${session.access_token}` },
      body: JSON.stringify({ plan }),
    });
    const { url } = await res.json();
    if (url) window.location.href = url;
  } catch (e) {
    alert('Something went wrong. Please try again.');
  }
}

document.addEventListener('DOMContentLoaded',checkAuth2);