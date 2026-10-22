// Shared by teacher-page.js (robots meta) and sitemap.js (which profiles to
// list): a public teacher profile is only worth indexing once it has real
// content — a bio or "teaches" line AND a few favourite worksheets. Thinner
// profiles still render for visitors, with noindex.
const INDEX_MIN_FAVS = 3;
const isIndexable = (p, favCount) => !!((p.bio || p.teaches) && favCount >= INDEX_MIN_FAVS);

module.exports = { INDEX_MIN_FAVS, isIndexable };
