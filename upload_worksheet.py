import requests, json, os, uuid
from datetime import datetime

from env_secrets import SUPABASE_URL, SERVICE_KEY

HEADERS_AUTH = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
}

PDF_PATH   = r'C:\Users\juand\Downloads\PastSimple_Writing_B1.pdf'
THUMB_PATH = r'C:\Users\juand\Downloads\preview_html_pdf.png'

# ── 1. Upload PDF ──────────────────────────────────────────
ts = int(datetime.now().timestamp() * 1000)
pdf_storage_path = f'b1/{ts}-PastSimple_Writing_B1.pdf'

with open(PDF_PATH, 'rb') as f:
    res = requests.post(
        f'{SUPABASE_URL}/storage/v1/object/worksheets/{pdf_storage_path}',
        headers={**HEADERS_AUTH, 'Content-Type': 'application/pdf', 'x-upsert': 'false'},
        data=f,
        verify=False
    )
print('PDF upload:', res.status_code, res.text[:200])

pdf_url = f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{pdf_storage_path}'

# ── 2. Upload thumbnail ────────────────────────────────────
thumb_path = f'thumbnails/{ts}-PastSimple_Writing_B1.webp'

# Convert PNG to WebP first
from PIL import Image
img = Image.open(THUMB_PATH)
import io
buf = io.BytesIO()
img.save(buf, 'WEBP', quality=88)
buf.seek(0)

res2 = requests.post(
    f'{SUPABASE_URL}/storage/v1/object/worksheets/{thumb_path}',
    headers={**HEADERS_AUTH, 'Content-Type': 'image/webp', 'x-upsert': 'false'},
    data=buf.read(),
    verify=False
)
print('Thumb upload:', res2.status_code, res2.text[:200])

thumb_url = f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{thumb_path}'

# ── 3. Insert DB record ────────────────────────────────────
record = {
    'id': str(uuid.uuid4()),
    'title': 'Past Simple – Writing Practice',
    'level': 'B1',
    'category': 'Grammar',
    'tags': 'worksheet, past simple, writing, grammar',
    'description': 'A complete writing worksheet for B1 students practising Past Simple. Includes picture-based sentences, paragraph writing, comprehension questions, and a challenge section.',
    'file_url': pdf_url,
    'thumbnail_url': thumb_url,
    'is_free': True,
    'downloads': 0,
}

res3 = requests.post(
    f'{SUPABASE_URL}/rest/v1/worksheets',
    headers={**HEADERS_AUTH, 'Content-Type': 'application/json', 'Prefer': 'return=representation'},
    json=record,
    verify=False
)
print('DB insert:', res3.status_code, res3.text[:300])

if res3.status_code in (200, 201):
    print('\nDone! Worksheet uploaded successfully to Workshido!')
    print('Title: Past Simple - Writing Practice')
    print('Level: B1 | Category: Grammar | Free: Yes')
else:
    print('\nDB insert failed')
