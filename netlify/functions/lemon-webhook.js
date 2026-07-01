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

  if (eventName === 'subscription_created' || eventName === 'subscription_updated') {
    const status = payload.data?.attributes?.status;
    const isPremium = status === 'active' || status === 'on_trial';

    if (userId) {
      await sb.from('profiles').update({ is_premium: isPremium }).eq('id', userId);
    } else if (userEmail) {
      await sb.from('profiles').update({ is_premium: isPremium }).eq('email', userEmail);
    }
  }

  if (eventName === 'subscription_cancelled' || eventName === 'subscription_expired') {
    if (userId) {
      await sb.from('profiles').update({ is_premium: false }).eq('id', userId);
    } else if (userEmail) {
      await sb.from('profiles').update({ is_premium: false }).eq('email', userEmail);
    }
  }

  return { statusCode: 200, body: JSON.stringify({ received: true }) };
};
