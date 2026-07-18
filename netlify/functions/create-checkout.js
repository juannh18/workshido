const { createClient } = require('@supabase/supabase-js');
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY);

const VARIANT_IDS = {
  monthly: '1852510',
  yearly: '1852478',
};

const STORE_URL = 'https://workshido.lemonsqueezy.com/checkout/buy';

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const token = (event.headers.authorization || event.headers.Authorization || '').replace('Bearer ', '');
  if (!token) return { statusCode: 401, body: JSON.stringify({ error: 'Not authenticated' }) };

  try {
    // The user paying for the subscription must be the one attached to the
    // session, not whatever id/email the client happens to send — otherwise
    // anyone could credit a purchase to (or bill) an arbitrary account.
    const { data: { user }, error: userErr } = await sb.auth.getUser(token);
    if (userErr || !user) return { statusCode: 401, body: JSON.stringify({ error: 'Invalid session' }) };

    const { plan } = JSON.parse(event.body);

    const variantId = plan === 'yearly' ? VARIANT_IDS.yearly : VARIANT_IDS.monthly;

    const params = new URLSearchParams({
      'checkout[email]': user.email,
      'checkout[custom][user_id]': user.id,
      'checkout[success_url]': `${process.env.SITE_URL}/workshido-pricing.html?success=1`,
      'checkout[cancel_url]': `${process.env.SITE_URL}/workshido-pricing.html?cancelled=1`,
    });

    const checkoutUrl = `${STORE_URL}/${variantId}?${params.toString()}`;

    return {
      statusCode: 200,
      body: JSON.stringify({ url: checkoutUrl }),
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};
