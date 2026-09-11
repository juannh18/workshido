const crypto = require('crypto');
const { createClient } = require('@supabase/supabase-js');

const sb = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

// The Lemon Squeezy store is shared with Spanishido, which registers its own
// webhook on the same store — so this endpoint also receives Spanishido's
// subscription events. Restrict this handler to Workshido's own subscription
// variants; without it, a Spanishido purchase would flip is_premium here too.
// Set LEMONSQUEEZY_VARIANT_IDS to the comma-separated Workshido Premium
// monthly+yearly numeric variant ids. Unset => act on every variant (legacy).
const WS_VARIANT_IDS = (process.env.LEMONSQUEEZY_VARIANT_IDS || '')
  .split(',').map(s => s.trim()).filter(Boolean);

function verifySignature(rawBody, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(rawBody);
  const digest = hmac.digest('hex');
  return crypto.timingSafeEqual(Buffer.from(digest), Buffer.from(signature));
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const signature = event.headers['x-signature'];
  if (!signature) {
    return { statusCode: 400, body: 'Missing signature' };
  }

  try {
    const validSignature = verifySignature(event.body, signature, process.env.LEMONSQUEEZY_WEBHOOK_SECRET);
    if (!validSignature) {
      return { statusCode: 400, body: 'Invalid signature' };
    }
  } catch {
    return { statusCode: 400, body: 'Invalid signature' };
  }

  const payload = JSON.parse(event.body);
  const eventName = payload.meta?.event_name;
  const userId = payload.meta?.custom_data?.user_id;
  const userEmail = payload.data?.attributes?.user_email;

  const SUBSCRIPTION_EVENTS = ['subscription_created', 'subscription_updated', 'subscription_cancelled', 'subscription_expired'];
  if (SUBSCRIPTION_EVENTS.includes(eventName)) {
    // Ignore Spanishido (or any other) product events on this shared store.
    const variantId = payload.data?.attributes?.variant_id != null ? String(payload.data.attributes.variant_id) : null;
    if (WS_VARIANT_IDS.length && !WS_VARIANT_IDS.includes(variantId)) {
      return { statusCode: 200, body: JSON.stringify({ received: true, ignored: 'not a Workshido variant' }) };
    }
    const status = payload.data?.attributes?.status;
    const endsAt = payload.data?.attributes?.ends_at;
    // Lemon Squeezy sets status='cancelled' the INSTANT the customer cancels —
    // that only means "won't renew", not "access revoked now". The customer
    // already paid for the current period and keeps access until `ends_at`.
    // Only 'expired' (or a cancelled sub whose ends_at has passed) should
    // actually revoke Premium.
    const isPremium = status === 'active' || status === 'on_trial'
      || (status === 'cancelled' && !!endsAt && new Date(endsAt) > new Date());
    // LS returns the customer's self-service portal link directly on the
    // subscription resource — no separate API call needed to fetch it.
    const customerId = payload.data?.attributes?.customer_id != null ? String(payload.data.attributes.customer_id) : null;
    const portalUrl = payload.data?.attributes?.urls?.customer_portal || null;
    const extra = {};
    if (customerId) extra.lemon_customer_id = customerId;
    if (portalUrl) extra.lemon_portal_url = portalUrl;

    if (userId) {
      // upsert so premium activates even if the profile row is somehow missing
      await sb.from('profiles').upsert(
        { id: userId, email: userEmail, is_premium: isPremium, ...extra },
        { onConflict: 'id' }
      );
    } else if (userEmail) {
      await sb.from('profiles').update({ is_premium: isPremium, ...extra }).eq('email', userEmail);
    }
  }

  return { statusCode: 200, body: JSON.stringify({ received: true }) };
};
