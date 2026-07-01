const VARIANT_IDS = {
  monthly: '1852510',
  yearly: '1852478',
};

const STORE_URL = 'https://workshido.lemonsqueezy.com/checkout/buy';

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { plan, userId, userEmail } = JSON.parse(event.body);

    const variantId = plan === 'yearly' ? VARIANT_IDS.yearly : VARIANT_IDS.monthly;

    const params = new URLSearchParams({
      'checkout[email]': userEmail,
      'checkout[custom][user_id]': userId,
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
