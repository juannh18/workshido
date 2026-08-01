// Returns the visitor's country using Netlify's own edge geolocation —
// no third-party IP-lookup service, no API key, stays consistent with
// analytics.js's "first-party, no external service" design.
export default async (request, context) => {
  const country = context.geo?.country || {};
  return new Response(
    JSON.stringify({ code: country.code || null, name: country.name || null }),
    { headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } }
  );
};

export const config = { path: '/api/geo' };
