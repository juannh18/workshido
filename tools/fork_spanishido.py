"""Fork the Workshido site into the Spanishido repo, applying every systematic
transform in one pass.

Why a script: Workshido -> Spanishido differs only by (1) brand theme, (2) the
Supabase schema it reads (`es` instead of `public`), (3) domain/OAuth config.
Hand-editing ~40 files is slow and drift-prone. This runs the mechanical 90%;
a human reviews FORK_NOTES.md for the rest (nuanced copy, favicon, OG image).
Re-runnable: to pull later Workshido changes, re-run and diff.

Backend is SHARED (same Supabase project mhbgxdsdaalvtgobnvbh, same anon key):
  * es.worksheets / es.quizzes         -> real isolated tables
  * es.profiles / es.saved_worksheets / es.user_downloads / es.email_leads /
    es.analytics_events                -> security_invoker views onto public.*
  * es.increment_downloads / es.submit_rating -> RPC clones
So a blanket { db: { schema: 'es' } } on every createClient is all the code needs.

Usage:  python tools/fork_spanishido.py
"""
import os, re, shutil, sys

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = r'C:\Users\juand\OneDrive\Desktop\Spanishido'

# Files/dirs to carry into the fork (everything else is skipped).
COPY_FILES = [
    'index.html', '404.html', 'robots.txt', 'llms.txt',
    'workshido-index.html', 'workshido-worksheet-app.html',
    'workshido-forteachers.html', 'workshido-how-quiz-works.html',
    'workshido-login.html', 'workshido-signup.html', 'workshido-reset.html',
    'workshido-profile.html', 'workshido-pricing.html',
    'workshido-privacy.html', 'workshido-terms.html', 'workshido-upload.html',
    'workshido-auth.js', 'mascot.js', 'netlify.toml',
    'favicon.ico', 'favicon.svg', 'favicon-16x16.png', 'favicon-32x32.png',
    'favicon-192.png', 'apple-touch-icon.png', 'og-image.png',
]
COPY_DIRS = [
    'fonts',
    'js',
    os.path.join('netlify', 'functions'),
    os.path.join('netlify', 'edge-functions'),
    os.path.join('worksheets', 'grammar'),
    os.path.join('worksheets', 'reading'),
    os.path.join('worksheets', 'writing'),
    os.path.join('worksheets', 'vocabulary'),
    os.path.join('worksheets', 'levels', 'a1'),
    os.path.join('worksheets', 'levels', 'a2'),
]
# js/ files that are Workshido-only utilities or belong to sections we don't fork yet
JS_SKIP = set()  # keep all js/*; guides-auth.js harmless even w/o guides
# dir copy: skip these names anywhere
DIR_SKIP = {'node_modules', '__pycache__'}

TEXT_EXT = {'.html', '.js', '.css', '.txt', '.toml', '.json', '.xml', '.svg'}

# ---- brand palette: Workshido blue -> Spanishido terracota (same lightness ramp) ----
# Only BLUE-family colors are remapped. Category accents (teal/amber/purple/
# pink/red/green/coral), greys, and Google sign-in brand colors are left as-is.
COLOR = {
    '#042C53': '#3B160A', '#0C447C': '#64230E', '#185FA5': '#A6401D',
    '#378ADD': '#CE6538', '#85B7EB': '#EFAD86', '#B5D4F4': '#F6CBB0',
    '#E6F1FB': '#FBEDE5',
    '#E8ECF1': '#F0E4DA', '#D8E6F5': '#F0D9CA',   # cool borders -> warm
    '#0E3D6E': '#5C2A12',                          # hero gradient mid-stop
    '#1A4FA0': '#8A3518', '#0369A1': '#8A3518',    # mid-dark blues
    '#2563EB': '#A6401D',                          # bright link/button blue
    '#DCEBFB': '#F8E1D3', '#E8F0FB': '#FBEDE5', '#E0F2FE': '#FBEDE5',
    '#F0F4FF': '#FDF6F1', '#D1DAF0': '#F0DFD2', '#E6EBF1': '#F0E4DA',
    '#7EC8F0': '#EFAD86', '#6B7FB5': '#A8836E',
    '#1A3A5C': '#3B160A', '#6EA8DC': '#CE6538',    # TE hexes if any HTML carries them
}
# blue-family rgb/rgba -> terracota equivalents (alpha preserved by regex)
RGBA = {
    (181, 212, 244): (246, 203, 176),   # #B5D4F4
    (133, 183, 235): (239, 173, 134),   # #85B7EB
    (24, 95, 165):   (166, 64, 29),     # #185FA5
    (55, 138, 221):  (206, 101, 56),    # #378ADD
    (4, 44, 83):     (59, 22, 10),      # #042C53
}

# ---- safe copy swaps (English-for-ESL -> Spanish-for-ELE). Nuanced marketing
#      copy is left for human review; these are the unambiguous ones. ----
COPY = [
    ('Free English Worksheets', 'Free Spanish Worksheets'),
    ('free English worksheets', 'free Spanish worksheets'),
    ('English worksheets', 'Spanish worksheets'),
    ('English Worksheets', 'Spanish Worksheets'),
    ('printable English', 'printable Spanish'),
    ('English classes', 'Spanish classes'),
    ('English class', 'Spanish class'),
    ('real English classes', 'real Spanish classes'),
    ('English teachers', 'Spanish teachers'),
    ('English teacher', 'Spanish teacher'),
    ('teach English', 'teach Spanish'),
    ('teaching English', 'teaching Spanish'),
    ('learn English', 'learn Spanish'),
    ('learning English', 'learning Spanish'),
    ('for English learners', 'for Spanish learners'),
    ('English learners', 'Spanish learners'),
    ('English grammar', 'Spanish grammar'),
    ('English language', 'Spanish language'),
    ('ESL worksheets', 'Spanish worksheets'),
    ('ESL classes', 'Spanish classes'),
    ('ESL teachers', 'Spanish teachers'),
    ('ESL classroom', 'Spanish classroom'),
]


def transform(text, path):
    t = text

    # 1. domain (before the Workshido->Spanishido text swap). The R2 asset host
    # `files.workshido.com` is SHARED (Spanish files just live under /es/), so
    # protect it from the rename.
    t = t.replace('files.workshido.com', '\x00R2HOST\x00')
    t = t.replace('https://workshido.com', 'https://spanishido.com')
    t = t.replace('workshido.com', 'spanishido.com')
    t = t.replace('\x00R2HOST\x00', 'files.workshido.com')

    # 2. wordmark HTML (before the plain-text swap)
    t = t.replace('Work<span class="brand-accent">shido</span>',
                  'Spanish<span class="brand-accent">ido</span>')
    t = t.replace('Work<span>shido</span>', 'Spanish<span>ido</span>')

    # 3. plain brand name (leaves lowercase workshido-*.html / js/workshido-*.js paths alone)
    t = t.replace('Workshido', 'Spanishido')

    # 4. brand palette (hex, case-insensitive)
    for a, b in COLOR.items():
        t = re.sub(re.escape(a), b, t, flags=re.IGNORECASE)
    # blue-family rgb/rgba with any alpha -> terracota
    def _rgba(m):
        r, g, bl = int(m.group(1)), int(m.group(2)), int(m.group(3))
        rep = RGBA.get((r, g, bl))
        if not rep:
            return m.group(0)
        tail = m.group(4) or ''
        return f'rgba({rep[0]},{rep[1]},{rep[2]}{tail})' if tail else f'rgb({rep[0]},{rep[1]},{rep[2]})'
    t = re.sub(r'rgba?\((\d+), ?(\d+), ?(\d+)(, ?[0-9.]+)?\)', _rgba, t)

    # 5. Supabase client -> default to schema `es` (shared tables are es views)
    t = t.replace(
        "supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo')",
        "supabase.createClient('https://mhbgxdsdaalvtgobnvbh.supabase.co','sb_publishable_SnvJUMzhWFsSBHJZyCAjTA_nH0-F9jo',{db:{schema:'es'}})")
    t = re.sub(
        r"createClient\(\s*process\.env\.SUPABASE_URL\s*,\s*process\.env\.SUPABASE_SERVICE_KEY\s*\)",
        "createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SERVICE_KEY, { db: { schema: 'es' } })",
        t)
    t = re.sub(
        r"createClient\(\s*SUPABASE_URL\s*,\s*SUPABASE_KEY\s*\)",
        "createClient(SUPABASE_URL, SUPABASE_KEY, { db: { schema: 'es' } })",
        t)
    # marketing-consent.js pattern
    t = t.replace("supabase.createClient(SUPABASE_URL, SUPABASE_KEY)",
                  "supabase.createClient(SUPABASE_URL, SUPABASE_KEY, { db: { schema: 'es' } })")
    # analytics.js writes analytics_events via raw fetch -> keep it on `es`
    # (es.analytics_events is a view onto public); tag the site for later split.
    t = t.replace("/rest/v1/analytics_events',",
                  "/rest/v1/analytics_events',  // es view -> public.analytics_events")

    # 6. safe copy swaps
    for a, b in COPY:
        t = t.replace(a, b)

    # 7. Spanishido premium is its own entitlement (higher price) — every
    # is_premium check reads/writes is_premium_es instead. \b won't match
    # inside an existing is_premium_es.
    t = re.sub(r'\bis_premium\b', 'is_premium_es', t)

    # 8. Bookend: footer + browse-cta get the EXACT hero gradient (Juan's rule
    # — same terracota top and bottom). Copy the hero's gradient verbatim,
    # don't invent a colour.
    _grad = 'linear-gradient(160deg, var(--blue-900) 0%, var(--blue-800) 60%, #5C2A12 100%)'
    t = re.sub(r'(\bfooter\s*\{\s*\n\s*)background:\s*var\(--blue-900\);', r'\1background: ' + _grad + ';', t)
    t = t.replace('footer { background: var(--blue-900);', 'footer { background: ' + _grad + ';')
    t = t.replace('.browse-cta { background: var(--blue-900);', '.browse-cta { background: ' + _grad + ';')

    return t


def main():
    copied, transformed, skipped_bin = [], [], []

    def handle(rel):
        s = os.path.join(SRC, rel)
        d = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        ext = os.path.splitext(s)[1].lower()
        if ext in TEXT_EXT:
            try:
                txt = open(s, encoding='utf-8').read()
            except UnicodeDecodeError:
                shutil.copy2(s, d); skipped_bin.append(rel); return
            new = transform(txt, rel)
            open(d, 'w', encoding='utf-8', newline='\n').write(new)
            (transformed if new != txt else copied).append(rel)
        else:
            shutil.copy2(s, d); copied.append(rel)

    for f in COPY_FILES:
        if os.path.isfile(os.path.join(SRC, f)):
            handle(f)
        else:
            print('  (missing, skipped):', f)

    for dpath in COPY_DIRS:
        base = os.path.join(SRC, dpath)
        if not os.path.isdir(base):
            print('  (missing dir, skipped):', dpath); continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [x for x in dirs if x not in DIR_SKIP]
            for fn in files:
                rel = os.path.relpath(os.path.join(root, fn), SRC)
                if os.path.basename(rel) in JS_SKIP:
                    continue
                handle(rel)

    notes = f"""# Spanishido fork — generated by tools/fork_spanishido.py

Source: Workshido repo. Backend SHARED (Supabase project mhbgxdsdaalvtgobnvbh):
worksheets/quizzes -> real `es` tables; profiles/analytics/retention -> `es`
security_invoker views onto public.*; RPCs cloned. Every createClient now
defaults to {{ db: {{ schema: 'es' }} }}.

## Auto-applied
- Files copied:        {len(copied)}
- Files transformed:   {len(transformed)}
- Binary copied as-is: {len(skipped_bin)}
- Domain workshido.com -> spanishido.com
- Wordmark Work<span>shido</span> -> Spanish<span>ido</span>
- "Workshido" -> "Spanishido" (JSON-LD, meta, titles, copy)
- Blue palette -> terracota (7-step ramp + warm borders)
- Supabase client -> schema `es` (all forms)
- Safe copy swaps (English worksheets -> Spanish worksheets, etc.)

## MANUAL — still to do
- [ ] Favicon: Juan wants an "Sp" mark (S + p), same style as Workshido's "Ws".
      Replace favicon.ico / .svg / -16 / -32 / -192 / apple-touch-icon.png.
- [ ] og-image.png: make a Spanishido version.
- [ ] Review ALL user-facing copy per page — the regex only caught unambiguous
      phrases. Hero headlines, "why" cards, forteachers page, pricing copy,
      privacy/terms body all need a human pass for Spanish-teaching context.
- [ ] Social links (Pinterest/TikTok/YouTube) now point at .../Spanishido/ —
      broken; point to real accounts or remove until they exist.
- [ ] Google OAuth: add https://spanishido.com to the client's Authorized
      JavaScript origins (client id 402662121573-hjto2nl434h1qdgvtl21n58du49kl2bd,
      same client kept in code).
- [ ] Lemon Squeezy: decide same store/products or separate for Spanishido
      premium; check create-checkout.js / lemon-webhook.js variant IDs + the
      LEMON_* env vars on the spanishido Netlify project.
- [ ] Netlify env vars on project "spanishido": SUPABASE_URL,
      SUPABASE_SERVICE_KEY, R2_* , LEMON_* , GOOGLE_* — copy from workshido.
- [ ] guides/ NOT forked (English ESL content). Nav links to /guides/ are
      "soon" — leave or hide.
- [ ] Internal routes still read /workshido-pricing etc. (filenames kept for
      clean Workshido->Spanishido syncing). Rename user-facing ones later.
- [ ] googleXXXX.html search-console verification not copied — Spanishido gets
      its own once the domain is in Search Console.
- [ ] Deploy: from THIS folder (not the Workshido repo) so netlify.toml +
      functions resolve correctly:  netlify deploy --prod --dir "{DST}" --site <spanishido-site-id>

## Transformed files
""" + '\n'.join('- ' + f for f in sorted(transformed))

    open(os.path.join(DST, 'FORK_NOTES.md'), 'w', encoding='utf-8').write(notes)

    print(f'\n{"="*60}')
    print(f'Fork written to: {DST}')
    print(f'  copied:      {len(copied)}')
    print(f'  transformed: {len(transformed)}')
    print(f'  binary:      {len(skipped_bin)}')
    print(f'See {os.path.join(DST, "FORK_NOTES.md")} for the manual checklist.')


if __name__ == '__main__':
    main()
