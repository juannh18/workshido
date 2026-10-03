// Supabase/PostgREST returns at most 1000 rows per request (API "max rows"),
// so whole-catalog reads page through with .range() instead of silently
// stopping at row 1000 (the catalog passes it ~Nov 2026). build() must return
// a fresh query ordered deterministically (id as tie-breaker).
async function fetchAllRows(build) {
  const rows = [];
  for (let from = 0; ; from += 1000) {
    const { data, error } = await build().range(from, from + 999);
    if (error) return { data: rows.length ? rows : null, error };
    rows.push(...(data || []));
    if (!data || data.length < 1000) return { data: rows, error: null };
  }
}

module.exports = { fetchAllRows };
