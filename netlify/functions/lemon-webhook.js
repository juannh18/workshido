const crypto = require('crypto');
const { createClient } = require('@supabase/supabase-js');

const sb = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

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
