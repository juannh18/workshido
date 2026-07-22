"""Genera las landing pages SEO por tema/nivel (/worksheets/<slug>/index.html).

Uso:
  python tools/gen_landing_pages.py

Reusa el <style> completo de workshido-index.html (mismo look, cero CSS nuevo
que mantener por separado) y una versión simplificada del catalog JS (fetch
filtrado por categoria/nivel en vez de las 1000 filas completas, mismo
buildCard/paginacion que el catalogo principal). Cada pagina es un archivo
estatico independiente con su propio <title>/meta description/canonical/H1 +
parrafo de introduccion unico, indexable sin depender de query strings.
"""
import os, re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Reusar el CSS completo del catálogo (mismo <style>...</style>) ---
catalog_html = open(os.path.join(REPO, 'workshido-index.html'), encoding='utf-8').read()
STYLE = catalog_html[catalog_html.index('<style>'):catalog_html.index('</style>') + len('</style>')]

PAGES = [
    {
        'slug': 'worksheets/grammar',
        'title': 'Free Grammar Worksheets for English Teachers | Workshido',
        'description': 'Free printable English grammar worksheets: present and past tenses, articles, prepositions, modal verbs and more. CEFR-levelled PDFs with answer keys.',
        'h1': 'Free English Grammar Worksheets',
        'intro': '''<p>Grammar is where most ESL lesson planning time goes — finding a worksheet that drills the exact point you just taught, at the right level, without turning into busywork. This collection covers the grammar points that come up most in general English courses: present and past tenses, articles, prepositions, modal verbs, comparatives, conditionals and more, organized by CEFR level from A1 through B1.</p>
<p>Every worksheet is free to download as a print-ready PDF, with a complete answer key included with many downloads (the rest are available in the worksheet's Teacher Edition). Most grammar worksheets follow the same shape — a short grammar focus box, several practice exercises building in difficulty, and a final freer-production task — so students get controlled practice before they're asked to produce the structure on their own.</p>''',
        'filter_field': 'category',
        'filter_value': 'Grammar',
        'breadcrumb': 'Grammar',
    },
    {
        'slug': 'worksheets/vocabulary',
        'title': 'Free Vocabulary Worksheets for English Teachers | Workshido',
        'description': 'Free printable English vocabulary worksheets: everyday topics, label-and-learn sheets and themed word lists. CEFR-levelled PDFs with answer keys.',
        'h1': 'Free English Vocabulary Worksheets',
        'intro': '''<p>Vocabulary worksheets work best when they're tied to a real topic a student can picture — the kitchen, a job interview, a weekend routine — rather than a random word list. This collection is organized around everyday themes: food, jobs, the home, travel, feelings, and more, each with clear visuals and CEFR-appropriate target vocabulary.</p>
<p>Most worksheets combine a label-and-learn or matching exercise to introduce the words with a short practice section that puts them into real sentences, so students leave with more than just a list they'll forget by next class. All PDFs are free to download and print, with answer keys included on many of them.</p>''',
        'filter_field': 'category',
        'filter_value': 'Vocabulary',
        'breadcrumb': 'Vocabulary',
    },
    {
        'slug': 'worksheets/reading',
        'title': 'Free Reading Comprehension Worksheets for English Teachers | Workshido',
        'description': 'Free printable English reading comprehension worksheets with short stories, true/false questions and vocabulary practice. CEFR-levelled PDFs with answer keys.',
        'h1': 'Free English Reading Worksheets',
        'intro': '''<p>Reading worksheets here pair a short, level-appropriate story or text with a set of comprehension tasks — multiple choice, true/false with correction, vocabulary-in-context, and short-answer questions — so a single text does double duty as both a reading and a grammar or vocabulary review.</p>
<p>Texts are written specifically for each CEFR level rather than adapted from adult content, so the language stays natural without outrunning what an A1 or A2 student can handle. Every worksheet is a free, print-ready PDF, and most include a full answer key.</p>''',
        'filter_field': 'category',
        'filter_value': 'Reading',
        'breadcrumb': 'Reading',
    },
    {
        'slug': 'worksheets/writing',
        'title': 'Free Writing Worksheets for English Teachers | Workshido',
        'description': 'Free printable English writing worksheets with guided prompts, planning boxes and model sentences. CEFR-levelled PDFs with answer keys.',
        'h1': 'Free English Writing Worksheets',
        'intro': '''<p>Blank-page writing tasks are hard for lower-level students to start cold, so these worksheets build in scaffolding: a short model text or example sentences, a planning box to organize ideas before drafting, and a target structure or vocabulary set the paragraph needs to use. Topics range from simple personal writing (daily routines, descriptions) to short opinion and narrative paragraphs at higher levels.</p>
<p>Each worksheet ends with a self-check list so students can review their own writing against the task requirements before handing it in. All PDFs are free to download and print.</p>''',
        'filter_field': 'category',
        'filter_value': 'Writing',
        'breadcrumb': 'Writing',
    },
    {
        'slug': 'worksheets/levels/a1',
        'title': 'Free A1 English Worksheets (Beginner) | Workshido',
        'description': 'Free printable A1 English worksheets for beginners: grammar, vocabulary, reading and writing PDFs with answer keys, aligned to the CEFR A1 level.',
        'h1': 'Free A1 English Worksheets',
        'intro': '''<p>A1 is the true beginner level — simple present and past tenses, basic vocabulary sets (family, food, numbers, colors), and short, highly-scaffolded reading and writing tasks. Every worksheet on this page is written and levelled specifically for A1 learners, not simplified from higher-level material, so the language stays within reach without feeling babyish.</p>
<p>The collection spans grammar, vocabulary, reading and writing, so you can build a full lesson — or a full unit — around a single topic at the same level. All worksheets are free, print-ready PDFs, and most include a complete answer key.</p>''',
        'filter_field': 'level',
        'filter_value': 'A1',
        'breadcrumb': 'A1 Beginner',
    },
    {
        'slug': 'worksheets/levels/a2',
        'title': 'Free A2 English Worksheets (Elementary) | Workshido',
        'description': 'Free printable A2 English worksheets for elementary learners: grammar, vocabulary, reading and writing PDFs with answer keys, aligned to the CEFR A2 level.',
        'h1': 'Free A2 English Worksheets',
        'intro': '''<p>A2 learners are past the true-beginner stage and ready for past continuous, comparatives, modal verbs, and longer reading and writing tasks — but still need clear models and controlled practice before freer production. This page collects every A2-level worksheet in the catalog: grammar, vocabulary, reading and writing, all written and levelled specifically for A2.</p>
<p>Use the level and skill filters on the full catalog to combine A2 with a specific grammar point or topic, or browse everything here to plan a full unit at this level. All worksheets are free to download as print-ready PDFs, with answer keys included on many of them.</p>''',
        'filter_field': 'level',
        'filter_value': 'A2',
        'breadcrumb': 'A2 Elementary',
    },
]

ALL_SLUGS = {p['slug']: p for p in PAGES}
CATEGORY_LINKS = [p for p in PAGES if p['filter_field'] == 'category']
LEVEL_LINKS = [p for p in PAGES if p['filter_field'] == 'level']


def related_links_html(current_slug):
    other_cats = [p for p in CATEGORY_LINKS if p['slug'] != current_slug]
    other_levels = [p for p in LEVEL_LINKS if p['slug'] != current_slug]
    items = []
    for p in other_cats + other_levels:
        items.append(f'<a href="/{p["slug"]}/" class="related-link">{p["breadcrumb"]}</a>')
    return '\n      '.join(items)


def breadcrumb_ld(page):
    parts = page['slug'].split('/')
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'Browse', 'item': 'https://workshido.com/workshido-index.html'}]
    if parts[0] == 'worksheets' and len(parts) == 2:
        items.append({'@type': 'ListItem', 'position': 2, 'name': page['breadcrumb'], 'item': f'https://workshido.com/{page["slug"]}/'})
    else:
        items.append({'@type': 'ListItem', 'position': 2, 'name': 'Levels', 'item': 'https://workshido.com/workshido-index.html'})
        items.append({'@type': 'ListItem', 'position': 3, 'name': page['breadcrumb'], 'item': f'https://workshido.com/{page["slug"]}/'})
    import json
    return json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items})


PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>__TITLE__</title>
<meta name="description" content="__DESCRIPTION__">
<link rel="canonical" href="https://workshido.com/__SLUG__/">
<meta property="og:site_name" content="Workshido">
<meta property="og:type" content="website">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESCRIPTION__">
<meta property="og:image" content="https://workshido.com/og-image.png">
<meta property="og:url" content="https://workshido.com/__SLUG__/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="__TITLE__">
<meta name="twitter:description" content="__DESCRIPTION__">
<meta name="twitter:image" content="https://workshido.com/og-image.png">
<meta name="theme-color" content="#042C53">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage","name":"__H1__","url":"https://workshido.com/__SLUG__/","isPartOf":{"@type":"WebSite","name":"Workshido","url":"https://workshido.com/"}}</script>
<script type="application/ld+json">__BREADCRUMB_LD__</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://mhbgxdsdaalvtgobnvbh.supabase.co" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">
__STYLE__
<style>
  .hero-lite { padding: 56px 32px 40px; }
  .hero-lite .intro { max-width: 720px; margin: 0 auto; text-align: left; color: var(--blue-100); font-size: 15px; line-height: 1.7; }
  .hero-lite .intro p { margin-bottom: 14px; }
  .hero-lite .browse-all { display: inline-block; margin-top: 6px; color: var(--white); font-size: 13px; text-decoration: underline; }
  .related-section { max-width: 1100px; margin: 0 auto; padding: 8px 32px 40px; }
  .related-section h2 { font-family: var(--font-display); font-size: 15px; font-weight: 700; color: var(--gray-900); margin-bottom: 12px; }
  .related-links { display: flex; flex-wrap: wrap; gap: 8px; }
  .related-link { display: inline-block; padding: 7px 16px; border: 1px solid var(--gray-100); border-radius: 20px; font-size: 13px; color: var(--blue-600); text-decoration: none; }
  .related-link:hover { background: var(--blue-50); border-color: var(--blue-200); }
  .content { padding: 32px; max-width: 1100px; margin: 0 auto; }
  @media (max-width: 480px) { .hero-lite { padding: 40px 16px 32px; } .related-section { padding: 8px 16px 32px; } }
</style>
</head>
<body>

<!-- NAV -->
<nav>
  <a href="/index.html" class="nav-logo">work<span>shido</span></a>
  <ul class="nav-links">
    <li><a href="/workshido-index.html">Browse</a></li>
    <li><a href="/workshido-index.html?cat=Grammar">Grammar</a></li>
    <li><a href="/workshido-index.html?cat=Vocabulary">Vocabulary</a></li>
    <li><a href="/workshido-index.html?cat=Reading">Skills</a></li>
    <li><a href="/workshido-forteachers.html">For teachers</a></li>
  </ul>
  <div class="nav-actions" id="navActions">
    <a href="/workshido-login.html" class="btn-ghost">Log in</a>
    <a href="/workshido-signup.html" class="btn-primary">Sign up free</a>
  </div>
  <button class="hamburger" onclick="openMobileMenu()" aria-label="Open menu">
    <span></span><span></span><span></span>
  </button>
</nav>

<!-- MOBILE MENU -->
<div class="mobile-menu" id="mobileMenu">
  <div class="mobile-menu-backdrop" onclick="closeMobileMenu()"></div>
  <div class="mobile-menu-panel">
    <div class="mobile-menu-header">
      <a href="/index.html" class="mobile-menu-logo">work<span>shido</span></a>
      <button class="mobile-menu-close" onclick="closeMobileMenu()" aria-label="Close menu">✕</button>
    </div>
    <div class="mobile-menu-links">
      <a href="/workshido-index.html">Browse all</a>
      <a href="/workshido-index.html?cat=Grammar">Grammar</a>
      <a href="/workshido-index.html?cat=Vocabulary">Vocabulary</a>
      <a href="/workshido-index.html?cat=Reading">Reading</a>
      <a href="/workshido-index.html?cat=Writing">Writing</a>
      <a href="/workshido-forteachers.html">For teachers</a>
    </div>
    <div class="mobile-menu-footer">
      <a href="/workshido-login.html" class="m-login">Log in</a>
      <a href="/workshido-signup.html" class="m-signup">Sign up free</a>
    </div>
  </div>
</div>

<div class="breadcrumb" role="navigation" aria-label="Breadcrumb">
  <a href="/workshido-index.html">Browse</a>
  <span>›</span>
  <span>__BREADCRUMB__</span>
</div>

<!-- HERO -->
<section class="hero hero-lite">
  <div class="hero-eyebrow" style="margin-left:auto;margin-right:auto;">
    <span class="dot"></span>
    <span>Free · Print-ready PDFs · Answer keys included</span>
  </div>
  <h1 style="max-width:720px;margin-left:auto;margin-right:auto;">__H1__</h1>
  <div class="intro">
    __INTRO__
    <a href="/workshido-index.html?__FILTER_QUERY__" class="browse-all">Browse and filter the full catalog →</a>
  </div>
</section>

<!-- CONTENT -->
<main class="content">
  <div class="content-header">
    <div>
      <span class="content-title" id="contentTitle">__H1__</span>
      <span class="content-count" id="contentCount"></span>
    </div>
    <select class="sort-select" id="sortSelect">
      <option value="newest">Newest first</option>
      <option value="downloads">Most downloaded</option>
    </select>
  </div>

  <div class="card-grid" id="cardGrid">
    <div style="grid-column:1/-1;text-align:center;padding:60px 0;color:var(--gray-300);font-size:14px;">Loading worksheets...</div>
  </div>

  <nav class="pagination" id="pagination" style="display:none;" aria-label="Worksheet results pages"></nav>
</main>

<section class="related-section">
  <h2>Explore more</h2>
  <div class="related-links">
    __RELATED_LINKS__
    <a href="/workshido-index.html" class="related-link">Full catalog →</a>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-grid">
    <div>
      <div class="footer-logo">work<span>shido</span></div>
      <p class="footer-desc">Free, high-quality English worksheets for teachers and students worldwide. Download, print, and teach.</p>
    </div>
    <div class="footer-col">
      <h4>Browse</h4>
      <a href="/worksheets/grammar/">Grammar</a>
      <a href="/worksheets/vocabulary/">Vocabulary</a>
      <a href="/worksheets/reading/">Reading</a>
      <a href="/worksheets/writing/">Writing</a>
    </div>
    <div class="footer-col">
      <h4>Levels</h4>
      <a href="/worksheets/levels/a1/">A1 Beginner</a>
      <a href="/worksheets/levels/a2/">A2 Elementary</a>
      <a href="/workshido-index.html?level=B1">B1 Intermediate</a>
    </div>
    <div class="footer-col">
      <h4>Company</h4>
      <a href="/workshido-forteachers.html">For teachers</a>
      <a href="/workshido-pricing.html">Premium</a>
      <a href="mailto:hello@workshido.com">Contact</a>
      <a href="/workshido-privacy.html">Privacy</a>
      <a href="/workshido-terms.html">Terms</a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© <span id="yr"></span> Workshido. All rights reserved.</span>
    <span>Made with ♥ for teachers worldwide</span>
  </div>
</footer>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.110.7"></script>
<script>
const sb2 = supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo');
const LEVEL_COLORS = { A1:'teal', A2:'blue', B1:'amber', B2:'purple', C1:'coral' };
const LEVEL_CLASS  = { A1:'a1',   A2:'a2',   B1:'b1',   B2:'b2',   C1:'c1'   };
const ACCENT       = { A1:'accent-teal', A2:'accent-blue', B1:'accent-amber', B2:'accent-purple', C1:'accent-amber' };
const PAGE_SIZE = 24;
let currentPage = 1;
let _lastFiltered = [];

function esc(s) { return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

function catalogStars(ws) {
  const avg = ws.rating || 0;
  const full = Math.round(avg);
  let s = '';
  for (let i = 1; i <= 5; i++) s += i <= full ? '★' : '☆';
  return s;
}
function catalogRatingHtml(ws) {
  if (!ws.ratings_count) return `<span class="badge-new">🆕 New</span>`;
  return `<span class="stars">${catalogStars(ws)}</span><span class="reviews">(${ws.downloads||0})</span>`;
}

function buildCard(ws) {
  const color  = LEVEL_COLORS[ws.level] || 'teal';
  const lvlCls = LEVEL_CLASS[ws.level]  || 'a1';
  const accent = ACCENT[ws.level]        || 'accent-teal';
  const badge  = ws.is_free ? '<span class="badge-type free">Free</span>' : '<span class="badge-type premium">Premium</span>';
  const btn    = ws.is_free
    ? `<a href="/workshido-worksheet.html?id=${ws.id}" class="btn-download" style="text-decoration:none;">↓ Download</a>`
    : `<a href="/workshido-worksheet.html?id=${ws.id}" class="btn-download locked" style="text-decoration:none;">🔒 Unlock</a>`;
  const tags   = (ws.tags || ws.category || '').split(',').slice(0,2).map(t=>`<span class="tag">${esc(t.trim())}</span>`).join('');
  const thumb = ws.thumbnail_url
    ? `<img src="${ws.thumbnail_url}" alt="${esc(ws.title)}" loading="lazy">`
    : `<div class="ws-preview"><div class="wl ${accent}"></div><div class="wl"></div><div class="wl short"></div><div class="wb"></div><div class="wb"></div><div class="wl short"></div></div>`;
  const overlay = !ws.thumbnail_url ? `<div class="card-thumb-overlay"><span class="overlay-logo">Work<span>shido</span></span><span class="overlay-level ${lvlCls}">${ws.level}</span></div>` : '';
  return `<div class="ws-card">
    <a href="/workshido-worksheet.html?id=${ws.id}" class="card-thumb ${color}" style="display:block;text-decoration:none;">${thumb}${overlay}</a>
    <div class="card-body">
      <div class="card-meta"><span class="badge-level ${lvlCls}">${ws.level}</span>${badge}</div>
      <a href="/workshido-worksheet.html?id=${ws.id}" class="card-title" style="text-decoration:none;color:inherit;">${esc(ws.title)}</a>
      <div class="card-tags">${tags}</div>
      <div class="card-footer">
        <div class="card-rating">${catalogRatingHtml(ws)}</div>
        ${btn}
      </div>
    </div>
  </div>`;
}

function renderCards(pageData, total) {
  const grid  = document.getElementById('cardGrid');
  const count = document.getElementById('contentCount');
  if (!pageData || pageData.length === 0) {
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:60px 0;color:var(--gray-300);font-size:14px;">No worksheets found yet — check back soon.</div>';
    if (count) count.textContent = '';
    renderPagination(0);
    return;
  }
  const txt = `${total} worksheet${total !== 1 ? 's' : ''}`;
  if (count) count.textContent = txt;
  grid.innerHTML = pageData.map(buildCard).join('');
  renderPagination(total);
}

function renderPage() {
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageData = _lastFiltered.slice(start, start + PAGE_SIZE);
  renderCards(pageData, _lastFiltered.length);
}

function renderPagination(total) {
  const el = document.getElementById('pagination');
  if (!el) return;
  const pageCount = Math.ceil(total / PAGE_SIZE);
  if (pageCount <= 1) { el.style.display = 'none'; el.innerHTML = ''; return; }
  el.style.display = 'flex';
  const btn = (label, page, opts = {}) =>
    `<button class="page-btn${opts.active ? ' active' : ''}" ${opts.disabled ? 'disabled' : ''} onclick="goToPage(${page})" aria-label="${opts.ariaLabel || `Page ${label}`}" ${opts.active ? 'aria-current="page"' : ''}>${label}</button>`;
  let html = btn('‹', currentPage - 1, { disabled: currentPage === 1, ariaLabel: 'Previous page' });
  const windowSize = 2;
  for (let p = 1; p <= pageCount; p++) {
    if (p === 1 || p === pageCount || (p >= currentPage - windowSize && p <= currentPage + windowSize)) {
      html += btn(p, p, { active: p === currentPage });
    } else if (p === currentPage - windowSize - 1 || p === currentPage + windowSize + 1) {
      html += '<span class="page-ellipsis">…</span>';
    }
  }
  html += btn('›', currentPage + 1, { disabled: currentPage === pageCount, ariaLabel: 'Next page' });
  el.innerHTML = html;
}

function goToPage(page) {
  const pageCount = Math.ceil(_lastFiltered.length / PAGE_SIZE);
  if (page < 1 || page > pageCount || page === currentPage) return;
  currentPage = page;
  renderPage();
  document.getElementById('cardGrid')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function applySort() {
  const sort = document.getElementById('sortSelect')?.value || 'newest';
  _lastFiltered = [..._lastFiltered].sort((a, b) => {
    if (sort === 'newest') {
      const da = a.created_at ? new Date(a.created_at).getTime() : 0;
      const db = b.created_at ? new Date(b.created_at).getTime() : 0;
      return db - da;
    }
    return (b.downloads || 0) - (a.downloads || 0);
  });
  currentPage = 1;
  renderPage();
}

document.getElementById('sortSelect').addEventListener('change', applySort);
document.getElementById('yr').textContent = new Date().getFullYear();
function openMobileMenu()  { document.getElementById('mobileMenu').classList.add('open'); document.body.style.overflow = 'hidden'; }
function closeMobileMenu() { document.getElementById('mobileMenu').classList.remove('open'); document.body.style.overflow = ''; }

async function loadWorksheets() {
  const { data, error } = await sb2.from('worksheets').select('*').eq('__FILTER_FIELD__', '__FILTER_VALUE__').order('created_at', { ascending: false, nullsFirst: false }).limit(500);
  if (error) {
    document.getElementById('cardGrid').innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:60px 0;color:var(--gray-300);font-size:14px;">Could not load worksheets.</div>';
    return;
  }
  _lastFiltered = data || [];
  renderPage();
}
loadWorksheets();
</script>
</body>
</html>
'''


def main():
    for page in PAGES:
        html = PAGE_TEMPLATE
        html = html.replace('__STYLE__', STYLE)
        html = html.replace('__TITLE__', page['title'])
        html = html.replace('__DESCRIPTION__', page['description'])
        html = html.replace('__SLUG__', page['slug'])
        html = html.replace('__H1__', page['h1'])
        html = html.replace('__INTRO__', page['intro'])
        html = html.replace('__BREADCRUMB__', page['breadcrumb'])
        html = html.replace('__BREADCRUMB_LD__', breadcrumb_ld(page))
        html = html.replace('__FILTER_FIELD__', page['filter_field'])
        html = html.replace('__FILTER_VALUE__', page['filter_value'])
        html = html.replace('__FILTER_QUERY__', f"{page['filter_field']}={page['filter_value']}")
        html = html.replace('__RELATED_LINKS__', related_links_html(page['slug']))

        out_dir = os.path.join(REPO, page['slug'])
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'index.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"OK: {page['slug']}/index.html ({len(html)} chars)")


if __name__ == '__main__':
    main()
