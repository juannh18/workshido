import requests, os, uuid, io
from datetime import datetime
from PIL import Image
import fitz

requests.packages.urllib3.disable_warnings()

SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co'
SERVICE_KEY  = 'REDACTED_SUPABASE_SERVICE_KEY'
HEADERS_AUTH = {'apikey': SERVICE_KEY, 'Authorization': f'Bearer {SERVICE_KEY}'}
DL = r'C:\Users\juand\Downloads'

WS = {
    'slug': 'dailyroutineverbsa1',
    'pdf':  'dailyroutineverbsa1_final.pdf',
    'title': 'Daily Routine Verbs – Vocabulary Worksheet',
    'level': 'A1',
    'category': 'Vocabulary',
    'tags': 'worksheet, daily routine, vocabulary, verbs, reading, a1, english',
    'description': 'An A1 vocabulary worksheet on daily routine verbs with 7 exercises: a reading about Emma’s day, schedule completion, true/false with corrections, third-person rewriting, error correction, a word search, and free writing. Includes free answer key.',
    'is_free': True,
}

ts = int(datetime.now().timestamp() * 1000)
print(f'Uploading: {WS["title"]}')

# 1. PDF
pdf_local = os.path.join(DL, WS['pdf'])
pdf_path = f'a1/{ts}-{WS["slug"]}.pdf'
with open(pdf_local, 'rb') as f:
    r = requests.post(f'{SUPABASE_URL}/storage/v1/object/worksheets/{pdf_path}',
        headers={**HEADERS_AUTH, 'Content-Type': 'application/pdf', 'x-upsert': 'true'},
        data=f, verify=False)
assert r.status_code in (200, 201), f'PDF upload: {r.status_code} {r.text[:200]}'
pdf_url = f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{pdf_path}'
print('  OK: PDF uploaded')

# 2. Thumbnail desde la pagina 1 del PDF
doc = fitz.open(pdf_local)
pix = doc[0].get_pixmap(dpi=100)
img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
buf = io.BytesIO()
img.save(buf, 'WEBP', quality=88)
buf.seek(0)
thumb_path = f'thumbnails/{ts}-{WS["slug"]}.webp'
r = requests.post(f'{SUPABASE_URL}/storage/v1/object/worksheets/{thumb_path}',
    headers={**HEADERS_AUTH, 'Content-Type': 'image/webp', 'x-upsert': 'true'},
    data=buf.read(), verify=False)
assert r.status_code in (200, 201), f'Thumb upload: {r.status_code} {r.text[:200]}'
thumb_url = f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{thumb_path}'
print('  OK: Thumbnail uploaded')

# 3. DB insert (sin teacher edition: la answer key va incluida en el PDF)
record = {
    'id': str(uuid.uuid4()),
    'title': WS['title'],
    'level': WS['level'],
    'category': WS['category'],
    'tags': WS['tags'],
    'description': WS['description'],
    'file_url': pdf_url,
    'thumbnail_url': thumb_url,
    'teacher_edition_url': None,
    'is_free': WS['is_free'],
    'downloads': 0,
}
r = requests.post(f'{SUPABASE_URL}/rest/v1/worksheets',
    headers={**HEADERS_AUTH, 'Content-Type': 'application/json', 'Prefer': 'return=representation'},
    json=record, verify=False)
print(f'  DB insert: {r.status_code}')
if r.status_code not in (200, 201):
    print('  ERROR:', r.text[:300])
else:
    print('Done! Daily Routine Verbs A1 uploaded (free, answer key included).')
