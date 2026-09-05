const sb2 = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
const LEVEL_COLOR = { A1:'teal', A2:'blue', B1:'amber', B2:'purple', C1:'coral' };
const LEVEL_CLS   = { A1:'a1',   A2:'a2',  B1:'b1',   B2:'b2',    C1:'c1'    };
const THUMB_ACCENT = { teal:'t', blue:'b', amber:'am', purple:'b', coral:'t' };

async function logOut(){ await sb2.auth.signOut(); window.location.href='workshido-index.html'; }

function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

async function loadProfile() {
  const { data: { user } } = await sb2.auth.getUser();
  if (!user) { window.location.href = 'workshido-login.html'; return; }

  const isJuan = user.email === 'juanda.5790@hotmail.com';
  const uploadSection = document.getElementById('uploadSection');
  if (uploadSection) uploadSection.style.display = isJuan ? '' : 'none';

  // The uploader dashboard (stats + "my worksheets") only makes sense for
  // Juan — uploading is admin-only, so everyone else's would always be
  // empty. Regular subscribers get an account/plan overview instead.
  const statsOverview = document.getElementById('statsOverview');
  const myWsSection = document.getElementById('my-worksheets');
  const subscriberOverview = document.getElementById('subscriberOverview');
  const navMyWsLink = document.getElementById('navMyWsLink');
  const sidebarMyWsLink = document.getElementById('sidebarMyWsLink');
  if (statsOverview) statsOverview.style.display = isJuan ? '' : 'none';
  if (myWsSection) myWsSection.style.display = isJuan ? '' : 'none';
  if (subscriberOverview) subscriberOverview.style.display = isJuan ? 'none' : '';
  if (navMyWsLink) navMyWsLink.style.display = isJuan ? '' : 'none';
  if (sidebarMyWsLink) sidebarMyWsLink.style.display = isJuan ? '' : 'none';

  const name = user.user_metadata?.full_name || user.email;
  const initials = name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
  document.querySelector('.avatar-big').textContent    = initials;
  document.querySelector('.profile-name').textContent  = name;
  document.querySelector('.profile-email').textContent = user.email;
  document.querySelector('.nav-avatar').textContent    = initials;

  const { data: profile } = await sb2
    .from('profiles')
    .select('marketing_consent, is_premium, lemon_portal_url')
    .eq('id', user.id)
    .maybeSingle();

  const planBadge = document.querySelector('.plan-badge');
  if (profile?.is_premium) {
    planBadge.textContent = '⭐ Premium';
    planBadge.classList.add('premium');
  } else {
    planBadge.textContent = '✓ Free';
  }

  // "Billing & plan" only becomes a real "manage subscription" link once we
  // have this user's Lemon Squeezy portal URL (arrives on their first
  // webhook event after this field was added — see lemon-webhook.js). Until
  // then it falls back to the pricing page rather than a dead end.
  const billingLink = document.getElementById('billingLink');
  const billingLabel = document.getElementById('billingLinkLabel');
  if (profile?.is_premium && profile?.lemon_portal_url) {
    billingLink.href = profile.lemon_portal_url;
    billingLink.target = '_blank';
    billingLink.rel = 'noopener';
    billingLabel.textContent = 'Manage subscription';
  } else if (profile?.is_premium) {
    billingLabel.textContent = 'Billing & plan';
  }

  // Same plan state, rendered as the main "Your account" card for regular
  // (non-Juan) subscribers — see subscriberOverview in the HTML.
  const acctPlanTitle = document.getElementById('acctPlanTitle');
  const acctPlanDesc = document.getElementById('acctPlanDesc');
  const acctPlanCta = document.getElementById('acctPlanCta');
  if (acctPlanTitle && acctPlanDesc && acctPlanCta) {
    if (profile?.is_premium) {
      acctPlanTitle.textContent = '⭐ Premium plan — active';
      acctPlanDesc.textContent = 'You have full access to the Teacher Edition and the graded Quiz for every worksheet.';
      acctPlanCta.removeAttribute('target');
      acctPlanCta.removeAttribute('rel');
      if (profile?.lemon_portal_url) {
        acctPlanCta.textContent = 'Manage subscription';
        acctPlanCta.href = profile.lemon_portal_url;
        acctPlanCta.target = '_blank';
        acctPlanCta.rel = 'noopener';
      } else {
        acctPlanCta.textContent = 'Billing & plan';
        acctPlanCta.href = 'workshido-pricing.html';
      }
    } else {
      acctPlanTitle.textContent = 'Free plan';
      acctPlanDesc.textContent = 'Upgrade to Premium to unlock the Teacher Edition and the full Quiz for every worksheet.';
      acctPlanCta.textContent = 'Upgrade to Premium';
      acctPlanCta.href = 'workshido-pricing.html';
      acctPlanCta.removeAttribute('target');
      acctPlanCta.removeAttribute('rel');
    }
  }

  const marketingToggle = document.getElementById('marketingToggle');
  if (marketingToggle) {
    marketingToggle.checked = !!profile?.marketing_consent;
    marketingToggle.addEventListener('change', async () => {
      const desired = marketingToggle.checked;
      marketingToggle.disabled = true;
      const { error } = await sb2.rpc('set_marketing_consent', {
        p_consent: desired,
        p_version: 'v1',
        p_source: 'profile_settings',
      });
      marketingToggle.disabled = false;
      if (error) {
        console.error('set_marketing_consent failed', error);
        marketingToggle.checked = !desired; // revert — the save didn't actually happen
        return;
      }
      const saved = document.getElementById('marketingSaved');
      saved.style.display = 'inline';
      setTimeout(() => { saved.style.display = 'none'; }, 2000);
    });
  }

  // Uploading is Juan-only, so the "my worksheets" query/render below only
  // applies to his account — everyone else already saw subscriberOverview.
  if (!isJuan) return;

  const { data: worksheets } = await sb2
    .from('worksheets')
    .select('id, title, level, category, downloads, created_at')
    .eq('uploaded_by', user.id)
    .order('created_at', { ascending: false });

  const ws = worksheets || [];
  const totalDl = ws.reduce((s, w) => s + (w.downloads || 0), 0);

  const levelCount = {};
  const catCount   = {};
  ws.forEach(w => {
    levelCount[w.level]    = (levelCount[w.level]    || 0) + 1;
    catCount[w.category]   = (catCount[w.category]   || 0) + 1;
  });
  const topLevel = Object.entries(levelCount).sort((a,b) => b[1]-a[1])[0]?.[0] || '—';
  const topCat   = Object.entries(catCount).sort((a,b)   => b[1]-a[1])[0]?.[0] || '—';

  document.getElementById('statUploaded').textContent = ws.length;
  document.getElementById('statDownloads').textContent = totalDl.toLocaleString();
  document.getElementById('statLevel').textContent    = topLevel;
  document.getElementById('statCategory').textContent = topCat;
  document.getElementById('wsCount').textContent      = `${ws.length} published`;

  const container = document.getElementById('myWsRows');
  if (ws.length === 0) {
    container.innerHTML = `<div style="padding:40px;text-align:center;color:var(--gray-300);font-size:14px;">You haven't uploaded any worksheets yet. <a href="workshido-upload.html" style="color:var(--blue-600)">Upload your first one →</a></div>`;
    return;
  }

  container.innerHTML = ws.map(w => {
    const color   = LEVEL_COLOR[w.level]  || 'teal';
    const lvlCls  = LEVEL_CLS[w.level]   || 'a1';
    const accent  = THUMB_ACCENT[color]   || 't';
    const date    = w.created_at ? new Date(w.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' }) : '—';
    return `<div class="ws-row">
      <div class="ws-mini-thumb ${color}"><div class="wl a ${accent}"></div><div class="wl s"></div><div class="wb"></div><div class="wb"></div></div>
      <div class="ws-info">
        <div class="ws-title">${esc(w.title)}</div>
        <div class="ws-meta-row"><span class="ws-level ${lvlCls}">${w.level}</span><span class="ws-status">Published · ${date}</span></div>
      </div>
      <div class="ws-stats-mini"><div class="ws-stat">↓ <strong>${(w.downloads||0).toLocaleString()}</strong></div></div>
      <div class="ws-actions"><a href="workshido-worksheet.html?id=${w.id}" class="btn-sm edit">View</a></div>
    </div>`;
  }).join('');
}

document.addEventListener('DOMContentLoaded', loadProfile);