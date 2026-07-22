const SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co';
const SUPABASE_KEY = 'sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo';
const { createClient } = supabase;
const sb = createClient(SUPABASE_URL, SUPABASE_KEY);

const GIS_CLIENT_ID = '402662121573-hjto2nl434h1qdgvtl21n58du49kl2bd.apps.googleusercontent.com';

window.addEventListener('load', () => {
  if (typeof google === 'undefined') return;
  google.accounts.id.initialize({
    client_id: GIS_CLIENT_ID,
    callback: handleCredentialResponse,
    auto_select: false,
    cancel_on_tap_outside: true,
  });
});

function handleGoogle() {
  if (typeof google === 'undefined') { showError('Google Sign-In not available. Please try again.'); return; }
  google.accounts.id.prompt((n) => {
    if (n.isNotDisplayed() || n.isSkippedMoment()) {
      google.accounts.id.renderButton(document.getElementById('gisFallbackBtn'), { theme: 'outline', size: 'large', width: 300 });
      setTimeout(() => document.querySelector('#gisFallbackBtn [role="button"]')?.click(), 100);
    }
  });
}

async function handleCredentialResponse(response) {
  try {
    const { error } = await sb.auth.signInWithIdToken({ provider: 'google', token: response.credential });
    if (error) throw error;
    window.wsTrack?.('login_success', { method: 'google' });
    const params = new URLSearchParams(window.location.search);
    window.location.href = safeRedirect(params.get('redirect'));
  } catch (e) {
    window.wsTrack?.('login_failure', { method: 'google' });
    showError('Google sign-in failed. Please try again.');
  }
}

function showError(msg) {
  const el = document.getElementById('errorBanner');
  el.textContent = msg;
  el.style.display = 'block';
  document.getElementById('email').setAttribute('aria-invalid', 'true');
  document.getElementById('password').setAttribute('aria-invalid', 'true');
}

// ?redirect= must stay same-site — otherwise a crafted link (workshido.com
// itself, so it looks trustworthy) could send a user who just logged in for
// real straight to an external phishing/malware page, or even run a
// javascript:/data: URI. Resolve it and compare the real origin rather than
// pattern-matching, since scheme tricks are easy to miss with a regex.
function safeRedirect(target) {
  if (!target) return 'workshido-index.html';
  try {
    const resolved = new URL(target, window.location.origin);
    return resolved.origin === window.location.origin ? target : 'workshido-index.html';
  } catch (e) {
    return 'workshido-index.html';
  }
}

document.getElementById('loginForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  if (!email || !password) return showError('Please enter your email and password.');
  const btn = document.getElementById('loginBtn');
  btn.disabled = true;
  btn.textContent = 'Logging in...';
  const { data, error } = await sb.auth.signInWithPassword({ email, password });
  if (error) {
    window.wsTrack?.('login_failure', { method: 'password' });
    showError('Incorrect email or password. Please try again.');
    btn.disabled = false;
    btn.textContent = 'Log in';
  } else {
    window.wsTrack?.('login_success', { method: 'password' });
    const params = new URLSearchParams(window.location.search);
    window.location.href = safeRedirect(params.get('redirect'));
  }
});

// Carry ?redirect= through to signup so a user going login -> signup ->
// back doesn't lose their way back to checkout (e.g. from the pricing page).
(function propagateRedirectToSignup() {
  const redirect = new URLSearchParams(window.location.search).get('redirect');
  if (!redirect) return;
  document.querySelectorAll('a[href="workshido-signup.html"]').forEach(a => {
    a.href = 'workshido-signup.html?redirect=' + encodeURIComponent(redirect);
  });
})();