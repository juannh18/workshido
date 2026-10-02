"""Estampa fechas en las guías (Workshido y Spanishido): datePublished /
dateModified / image en el JSON-LD Article + "Updated <fecha>" visible en
.article-meta. Google usa ambas señales para la frescura de un artículo y la
auditoría SEO del 27/09/2026 encontró que ninguna guía tenía fecha.

Idempotente: conserva el datePublished que ya exista; dateModified = fecha de
última escritura del archivo (los generadores reescriben al regenerar).
datePublished nuevo = primer commit del archivo en git, o su fecha de creación
si no está en git.

Uso:
  python tools/guide_dates.py <repo_root>        # todas las guías del sitio
Los generadores (gen_guides.py, gen_guides_spanishido.py) lo llaman al final.
"""
import datetime as dt
import glob
import os
import re
import subprocess
import sys

MONTHS = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()


def _git_first_date(path):
    try:
        out = subprocess.run(['git', 'log', '--diff-filter=A', '--follow', '--format=%as', '--', os.path.basename(path)],
                             cwd=os.path.dirname(path), capture_output=True, text=True, timeout=20).stdout.split()
        return out[-1] if out else None
    except Exception:
        return None


def _day(ts):
    return dt.date.fromtimestamp(ts).isoformat()


def _byline(s):
    """Firma "<Marca> Editorial Team" → /about/ (visible + author del Article).
    Auditoría 02/10/2026: las guías firmaban solo "Organization: Workshido", sin
    autoría editorial ni página que la respalde. Idempotente. Va dentro de
    stamp() a propósito: así no toca el mtime y no infla dateModified."""
    m = re.search(r'<meta property="og:site_name" content="([^"]+)">', s)
    brand = m.group(1) if m else 'Workshido'
    m = re.search(r'<link rel="canonical" href="(https://[^/]+)/', s)
    domain = m.group(1) if m else 'https://workshido.com'
    team = f'{brand} Editorial Team'
    s = re.sub(r'"author":\s*\{[^{}]*\}',
               f'"author":{{"@type":"Organization","name":"{team}","url":"{domain}/about/"}}', s, count=1)
    if 'class="article-byline"' not in s:
        s = re.sub(r'(<p class="article-desc">.*?</p>)',
                   lambda m: m.group(1) + f'\n  <p class="article-byline">By the <a href="/about/">{team}</a></p>',
                   s, count=1, flags=re.S)
    if '.article-byline' not in s.split('</style>')[0]:
        s = s.replace('</style>', '  .article-byline { font-size: 13px; color: var(--gray-600); margin-top: 10px; }\n'
                      '  .article-byline a { color: inherit; }\n</style>', 1)
    return s


def stamp(path):
    s = open(path, encoding='utf-8').read()
    m_art = re.search(r'"@type":\s*"Article",\s*', s)
    if not m_art:
        return False
    old_pub = re.search(r'"datePublished":\s*"(\d{4}-\d{2}-\d{2})"', s)
    pub = (old_pub.group(1) if old_pub else None) or _git_first_date(path) or _day(os.stat(path).st_ctime)
    mod = max(_day(os.stat(path).st_mtime), pub)
    og = re.search(r'<meta property="og:image" content="([^"]+)"', s)
    image = og.group(1) if og else None

    # Drop any previous stamp, then insert a fresh one right after "@type":"Article".
    s = re.sub(r'"(datePublished|dateModified)":\s*"[^"]*",\s*', '', s)
    if image:
        s = re.sub(r'"image":\s*"[^"]*",\s*(?="headline")', '', s)
    m_art = re.search(r'"@type":\s*"Article",\s*', s)
    ins = f'"datePublished":"{pub}","dateModified":"{mod}",' + (f'"image":"{image}",' if image and '"image"' not in s[m_art.end():m_art.end() + 2000].split('</script>')[0] else '')
    s = s[:m_art.end()] + ins + s[m_art.end():]

    d = dt.date.fromisoformat(mod)
    human = f'{MONTHS[d.month - 1]} {d.day}, {d.year}'
    s = re.sub(r'(<div class="article-meta">[^<]*?)(?:\s*(?:·|&middot;)\s*Updated <time[^>]*>[^<]*</time>)+', r'\1', s)
    s = re.sub(r'(<div class="article-meta">)([^<]*?)(</div>)',
               lambda m: f'{m.group(1)}{m.group(2)} &middot; Updated <time datetime="{mod}">{human}</time>{m.group(3)}', s, count=1)
    s = _byline(s)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(s)
    # Keep the file's mtime at "mod" so a re-run doesn't bump dateModified by itself.
    ts = dt.datetime.combine(d, dt.time(12)).timestamp()
    os.utime(path, (ts, ts))
    return True


def stamp_site(root):
    files = glob.glob(os.path.join(root, 'guides', '*', 'index.html')) + glob.glob(os.path.join(root, 'guides', '*', '*', 'index.html'))
    return sum(stamp(f) for f in files)


if __name__ == '__main__':
    for root in sys.argv[1:] or ['.']:
        print(root, stamp_site(root), 'guides stamped')
