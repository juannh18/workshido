const sb = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');

async function sendReset() {
  const email = document.getElementById('email').value.trim();
  const btn = document.getElementById('submitBtn');
  const msg = document.getElementById('msg');
  msg.className = 'msg';
  msg.style.display = 'none';

  if (!email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
    msg.textContent = 'Please enter a valid email address.';
    msg.className = 'msg error';
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Sending...';

  const { error } = await sb.auth.resetPasswordForEmail(email, {
    redirectTo: window.location.origin + '/workshido-index.html'
  });

  btn.disabled = false;
  btn.textContent = 'Send reset link';

  if (error) {
    msg.textContent = 'Something went wrong. Please try again.';
    msg.className = 'msg error';
  } else {
    msg.textContent = 'Check your email — we sent a reset link!';
    msg.className = 'msg success';
    document.getElementById('email').value = '';
  }
}

document.getElementById('email').addEventListener('keydown', e => {
  if (e.key === 'Enter') sendReset();
});