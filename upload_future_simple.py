"""
Batch upload — Future Simple Tense worksheets (A2)
Converts PNG → PDF, generates WebP thumbnail, inserts DB record.
"""
import requests, json, uuid, io, warnings
from datetime import datetime
from PIL import Image

warnings.filterwarnings('ignore')  # suppress SSL warnings

from env_secrets import SUPABASE_URL, SERVICE_KEY

HEADERS = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
}

WORKSHEETS = [
    {
        'png':      r'C:\Users\juand\Downloads\FutureSimpleVocabulary.png',
        'slug':     'FutureSimpleVocabulary',
        'title':    'Future Simple Tense – Vocabulary',
        'level':    'A2',
        'category': 'Vocabulary',
        'tags':     'future simple, vocabulary, expressions, tense, A2',
        'desc':     'Vocabulary worksheet for A2 students exploring Future Simple Tense. Includes word-picture matching, fill-in-the-blank exercises, and a personal vocabulary challenge.',
    },
    {
        'png':      r'C:\Users\juand\Downloads\FutureSimpleReviewTopic.png',
        'slug':     'FutureSimpleReviewTopic',
        'title':    'Future Simple Tense – Review Practice',
        'level':    'A2',
        'category': 'Grammar',
        'tags':     'future simple, review, will, grammar, practice, A2',
        'desc':     'Review practice worksheet for A2 students covering will/won\'t, affirmative, negative, and question forms of Future Simple Tense.',
    },
    {
        'png':      r'C:\Users\juand\Downloads\FutureSimpleWriting.png',
        'slug':     'FutureSimpleWriting',
        'title':    'My Future Plans – Writing',
        'level':    'A2',
        'category': 'Writing',
        'tags':     'future simple, writing, plans, will, A2',
        'desc':     'Writing worksheet for A2 students practising Future Simple Tense to describe future plans. Includes sentence completion, picture-based writing, and a short paragraph challenge.',
    },
    {
        'png':      r'C:\Users\juand\Downloads\FutureSimpleReading.png',
        'slug':     'FutureSimpleReading',
        'title':    'The Future Awaits – Reading',
        'level':    'A2',
        'category': 'Reading',
        'tags':     'future simple, reading, comprehension, will, A2',
        'desc':     'Reading comprehension worksheet for A2 students based on a letter about future plans. Includes true/false, vocabulary matching, multiple choice, and discussion questions.',
    },
    {
        'png':      r'C:\Users\juand\Downloads\FutureSimpleTense.png',
        'slug':     'FutureSimpleTense',
        'title':    'Future Simple Tense – Grammar Practice',
        'level':    'A2',
        'category': 'Grammar',
        'tags':     'future simple, grammar, will, sentences, practice, A2',
        'desc':     'Grammar practice worksheet for A2 students on Future Simple Tense. Covers affirmative, negative, and question forms with fill-in-the-blank, sentence rewriting, and error correction.',
    },
]

def png_to_pdf_bytes(png_path):
    img = Image.open(png_path).convert('RGB')
    buf = io.BytesIO()
    # A4 at 150 dpi target
    img.save(buf, format='PDF', resolution=150)
    buf.seek(0)
    return buf.read()

def img_to_webp_bytes(png_path, max_w=800):
    img = Image.open(png_path).convert('RGB')
    ratio = max_w / img.width if img.width > max_w else 1
    if ratio < 1:
        img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'WEBP', quality=85)
    buf.seek(0)
    return buf.read()

for ws in WORKSHEETS:
    ts = int(datetime.now().timestamp() * 1000)
    print(f'\n--- {ws["title"]} ---')

    # 1. PNG → PDF bytes
    pdf_bytes = png_to_pdf_bytes(ws['png'])
    pdf_path  = f'a2/{ts}-{ws["slug"]}.pdf'

    res = requests.post(
        f'{SUPABASE_URL}/storage/v1/object/worksheets/{pdf_path}',
        headers={**HEADERS, 'Content-Type': 'application/pdf', 'x-upsert': 'false'},
        data=pdf_bytes,
        verify=False
    )
    if res.status_code not in (200, 201):
        print(f'  PDF FAIL {res.status_code}: {res.text[:200]}')
        continue
    print(f'  PDF OK')
    pdf_url = f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{pdf_path}'

    # 2. WebP thumbnail
    webp_bytes  = img_to_webp_bytes(ws['png'])
    thumb_path  = f'thumbnails/{ts}-{ws["slug"]}.webp'

    res2 = requests.post(
        f'{SUPABASE_URL}/storage/v1/object/worksheets/{thumb_path}',
        headers={**HEADERS, 'Content-Type': 'image/webp', 'x-upsert': 'false'},
        data=webp_bytes,
        verify=False
    )
    if res2.status_code not in (200, 201):
        print(f'  THUMB FAIL {res2.status_code}: {res2.text[:200]}')
        continue
    print(f'  Thumb OK')
    thumb_url = f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{thumb_path}'

    # 3. DB insert
    record = {
        'id':            str(uuid.uuid4()),
        'title':         ws['title'],
        'level':         ws['level'],
        'category':      ws['category'],
        'tags':          ws['tags'],
        'description':   ws['desc'],
        'file_url':      pdf_url,
        'thumbnail_url': thumb_url,
        'is_free':       True,
        'downloads':     0,
    }
    res3 = requests.post(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers={**HEADERS, 'Content-Type': 'application/json', 'Prefer': 'return=representation'},
        json=record,
        verify=False
    )
    if res3.status_code in (200, 201):
        data = res3.json()
        wid = data[0]['id'] if isinstance(data, list) else data.get('id', '?')
        print(f'  DB OK: id={wid}')
    else:
        print(f'  DB FAIL {res3.status_code}: {res3.text[:300]}')

print('\nTodo listo!')
