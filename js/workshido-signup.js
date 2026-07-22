const SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co';
const SUPABASE_KEY = 'sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo';
const { createClient } = supabase;
const sb = createClient(SUPABASE_URL, SUPABASE_KEY);

let selectedRole = 'teacher';

function selectRole(btn, role) {
  document.querySelectorAll('.role-option').forEach(r => r.classList.remove('selected'));
  btn.classList.add('selected');
  selectedRole = role;
}

function togglePassword() {
  const input = document.getElementById('password');
  const show = input.type === 'password';
  input.type = show ? 'text' : 'password';
  const btn = document.getElementById('togglePwBtn');
  btn.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
  btn.setAttribute('aria-pressed', show);
}

document.getElementById('password').addEventListener('input', function() {
  const val = this.value;
  const fill = document.getElementById('strengthFill');
  const label = document.getElementById('strengthLabel');
  let strength = 0;
  if (val.length >= 8) strength++;
  if (/[A-Z]/.test(val)) strength++;
  if (/[0-9]/.test(val)) strength++;
  if (/[^A-Za-z0-9]/.test(val)) strength++;
  const levels = [
    { pct: '0%', color: '#D3D1C7', text: 'Enter a password' },
    { pct: '25%', color: '#C0392B', text: 'Weak' },
    { pct: '50%', color: '#BA7517', text: 'Fair' },
    { pct: '75%', color: '#378ADD', text: 'Good' },
    { pct: '100%', color: '#1D9E75', text: 'Strong ✓' },
  ];
  const lvl = val.length === 0 ? levels[0] : levels[strength] || levels[1];
  fill.style.width = lvl.pct;
  fill.style.background = lvl.color;
  label.textContent = lvl.text;
});

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

// ?redirect= must stay same-site — otherwise a crafted link could send a
// user who just signed up for real straight to an external phishing page.
function safeRedirect(target) {
  if (!target) return 'workshido-index.html';
  try {
    const url = new URL(target, window.location.origin);
    return url.origin === window.location.origin ? url.pathname + url.search : 'workshido-index.html';
  } catch (e) {
    return 'workshido-index.html';
  }
}

async function handleCredentialResponse(response) {
  try {
    const { error } = await sb.auth.signInWithIdToken({ provider: 'google', token: response.credential });
    if (error) throw error;
    window.wsTrack?.('signup_completed', { method: 'google' });
    const params = new URLSearchParams(window.location.search);
    window.location.href = safeRedirect(params.get('redirect'));
  } catch (e) {
    showError('Google sign-in failed. Please try again.');
  }
}

function showError(msg) {
  const el = document.getElementById('errorBanner');
  el.textContent = msg;
  el.style.display = 'block';
}

['firstName', 'lastName', 'email', 'password'].forEach(id => {
  document.getElementById(id)?.setAttribute('aria-describedby', 'errorBanner');
});

document.getElementById('signupForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const firstName = document.getElementById('firstName').value.trim();
  const lastName = document.getElementById('lastName').value.trim();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;
  const terms = document.getElementById('terms').checked;

  if (!firstName || !lastName) return showError('Please enter your full name.');
  if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) return showError('Please enter a valid email address.');
  if (password.length < 8) return showError('Password must be at least 8 characters.');
  if (!terms) return showError('Please accept the Terms of Service to continue.');

  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.textContent = 'Creating your account...';

  const redirectParam = new URLSearchParams(window.location.search).get('redirect');
  const emailRedirectTo = redirectParam
    ? `${window.location.origin}/workshido-login.html?redirect=${encodeURIComponent(redirectParam)}`
    : `${window.location.origin}/workshido-login.html`;

  const { data, error } = await sb.auth.signUp({
    email,
    password,
    options: { data: { full_name: `${firstName} ${lastName}`, role: selectedRole }, emailRedirectTo }
  });

  if (error) {
    window.wsTrack?.('validation_error', { form: 'signup', message: error.message });
    showError(error.message);
    btn.disabled = false;
    btn.textContent = 'Create free account';
  } else {
    window.wsTrack?.('signup_completed', { method: 'email', role: selectedRole });
    document.getElementById('formState').style.display = 'none';
    document.getElementById('successState').style.display = 'flex';
    if (redirectParam) document.getElementById('successGoLink').href = safeRedirect(redirectParam);
  }
});

// Carry ?redirect= to "Log in" too, in case the visitor already has an
// account — otherwise they'd lose their way back to checkout after logging in.
(function propagateRedirectToLogin() {
  const redirect = new URLSearchParams(window.location.search).get('redirect');
  if (!redirect) return;
  const link = document.getElementById('loginLink');
  if (link) link.href = 'workshido-login.html?redirect=' + encodeURIComponent(redirect);
})();