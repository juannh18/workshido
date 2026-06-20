// ============================================
// WORKSHIDO — Supabase Auth Config
// ============================================
const SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co';
const SUPABASE_KEY = 'sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo';

// Load Supabase client
const { createClient } = supabase;
const sb = createClient(SUPABASE_URL, SUPABASE_KEY);

// ============================================
// AUTH FUNCTIONS
// ============================================

// Sign up with email
async function signUp(email, password, fullName, role) {
  const { data, error } = await sb.auth.signUp({
    email,
    password,
    options: {
      data: { full_name: fullName, role: role }
    }
  });
  return { data, error };
}

// Login with email
async function logIn(email, password) {
  const { data, error } = await sb.auth.signInWithPassword({ email, password });
  return { data, error };
}

// Login with Google
async function logInWithGoogle() {
  const { data, error } = await sb.auth.signInWithOAuth({
    provider: 'google',
    options: { redirectTo: window.location.origin + '/workshido-index.html' }
  });
  return { data, error };
}

// Logout
async function logOut() {
  const { error } = await sb.auth.signOut();
  if (!error) window.location.href = 'workshido-index.html';
}

// Get current user
async function getUser() {
  const { data: { user } } = await sb.auth.getUser();
  return user;
}

// Check auth and update nav
async function checkAuth() {
  const user = await getUser();
  const navActions = document.querySelector('.nav-actions');
  if (!navActions) return;

  if (user) {
    const name = user.user_metadata?.full_name || user.email;
    const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    navActions.innerHTML = `
      <a href="workshido-profile.html" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:var(--blue-100);font-size:13px;">
        <div style="width:32px;height:32px;border-radius:50%;background:var(--blue-50);color:var(--blue-600);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:12px;border:2px solid var(--blue-200);">${initials}</div>
        ${name.split(' ')[0]}
      </a>
      <button onclick="logOut()" style="background:transparent;border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:7px 14px;color:var(--blue-100);font-size:13px;cursor:pointer;">Log out</button>
    `;
  }
}

// Run on every page
document.addEventListener('DOMContentLoaded', checkAuth);
