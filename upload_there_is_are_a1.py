import requests, json, os, uuid, io
from datetime import datetime
from PIL import Image

from env_secrets import SUPABASE_URL, SERVICE_KEY

HEADERS_AUTH = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
}

DL = r'C:\Users\juand\Downloads'

# ─── Worksheet definitions ──────────────────────────────────────────────────
WORKSHEETS = [
    {
        'slug': 'thereisthereagrammara1',
        'pdf':  'thereistherearegrammar.pdf',
        'thumb':'thereistherearegrammar.png',
        'title': 'There Is / There Are – Grammar Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, there is there are, grammar, a1, english',
        'description': 'A complete A1 grammar worksheet on "There Is / There Are". Includes a grammar box with singular and plural rules, plus exercises to complete sentences, describe pictures, and write negative sentences.',
        'is_free': True,
        'te_pdf': 'te_there_is_are_grammar_a1.pdf',
        'te_title': 'There Is / There Are – Grammar – Teacher Edition',
        'te_description': 'Teacher Edition for the There Is / There Are Grammar A1 worksheet. Includes full answer key, a complete lesson plan, common student mistakes, teacher tip, extra activity, and worksheet information.',
    },
    {
        'slug': 'thereisthereareadinga1',
        'pdf':  'thereistherearereading.pdf',
        'thumb':'thereistherearereading.png',
        'title': 'There Is / There Are – Reading Worksheet',
        'level': 'A1',
        'category': 'Reading',
        'tags': 'worksheet, there is there are, reading, a1, english',
        'description': 'An A1 reading worksheet based on "Emma\'s House" — a short descriptive text about rooms and furniture. Includes pre-reading, comprehension, true/false, vocabulary, and inference sections.',
        'is_free': True,
        'te_pdf': 'te_there_is_are_reading_a1.pdf',
        'te_title': 'There Is / There Are – Reading – Teacher Edition',
        'te_description': 'Teacher Edition for the There Is / There Are Reading A1 worksheet. Includes answer key for all exercises, true/false table, vocabulary answers, a complete lesson plan, teacher tip, common mistakes, and extra activity.',
    },
    {
        'slug': 'thereistherearevocabularya1',
        'pdf':  'thereistherearevocabulary.pdf',
        'thumb':'thereistherearevocabulary.png',
        'title': 'There Is / There Are – Vocabulary Worksheet',
        'level': 'A1',
        'category': 'Vocabulary',
        'tags': 'worksheet, there is there are, vocabulary, furniture, rooms, a1, english',
        'description': 'An A1 vocabulary worksheet focused on furniture and household objects. Includes matching, categorizing by room, sentence completion, quantity practice, and personal production exercises.',
        'is_free': True,
        'te_pdf': 'te_there_is_are_vocabulary_a1.pdf',
        'te_title': 'There Is / There Are – Vocabulary – Teacher Edition',
        'te_description': 'Teacher Edition for the There Is / There Are Vocabulary A1 worksheet. Includes full answer key, categorized word lists, a complete lesson plan, suggested production sentences, teacher tip, common mistakes, and extra activity.',
    },
    {
        'slug': 'thereistherearewritinga1',
        'pdf':  'thereistherearewriting.pdf',
        'thumb':'thereistherearewriting.png',
        'title': 'There Is / There Are – Writing Worksheet',
        'level': 'A1',
        'category': 'Writing',
        'tags': 'worksheet, there is there are, writing, a1, english',
        'description': 'An A1 writing worksheet on "There Is / There Are" for describing places. Students practice sentence building, guided writing from pictures, describing a room, and produce an independent paragraph about their favorite room.',
        'is_free': True,
        'te_pdf': 'te_there_is_are_writing_a1.pdf',
        'te_title': 'There Is / There Are – Writing – Teacher Edition',
        'te_description': 'Teacher Edition for the There Is / There Are Writing A1 worksheet. Includes model answers for guided writing, a complete lesson plan, teacher tip, common mistakes, and an extra describe-and-draw activity.',
    },
    {
        'slug': 'thereisthereareapracticea1',
        'pdf':  'thereisthereraepractice.pdf',
        'thumb':'thereisthereraepractice.png',
        'title': 'There Is / There Are – Practice Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, there is there are, practice, grammar, a1, english',
        'description': 'A comprehensive A1 practice worksheet on "There Is / There Are" with 10 exercises. Covers choosing correct options, completing sentences, negatives, short answers, reading, true/false, and free writing — ideal for consolidation.',
        'is_free': False,
        'te_pdf': 'te_there_is_are_practice_a1.pdf',
        'te_title': 'There Is / There Are – Practice – Teacher Edition',
        'te_description': 'Teacher Edition for the There Is / There Are Practice A1 worksheet. Includes complete answer key for all 10 exercises, a full lesson plan, suggested answers for open tasks, teacher tip, common mistakes, and an error-auction review activity.',
    },
]

# ─── Helper functions ────────────────────────────────────────────────────────

def upload_pdf(local_path, storage_path):
    with open(local_path, 'rb') as f:
        res = requests.post(
            f'{SUPABASE_URL}/storage/v1/object/worksheets/{storage_path}',
            headers={**HEADERS_AUTH, 'Content-Type': 'application/pdf', 'x-upsert': 'true'},
            data=f, verify=False
        )
    if res.status_code not in (200, 201):
        print(f'  ERROR PDF upload: {res.status_code} {res.text[:200]}')
        return None
    return f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{storage_path}'

def upload_thumb(local_path, storage_path):
    img = Image.open(local_path)
    buf = io.BytesIO()
    img.save(buf, 'WEBP', quality=88)
    buf.seek(0)
    res = requests.post(
        f'{SUPABASE_URL}/storage/v1/object/worksheets/{storage_path}',
        headers={**HEADERS_AUTH, 'Content-Type': 'image/webp', 'x-upsert': 'true'},
        data=buf.read(), verify=False
    )
    if res.status_code not in (200, 201):
        print(f'  ERROR thumb upload: {res.status_code} {res.text[:200]}')
        return None
    return f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{storage_path}'

def insert_worksheet(record):
    res = requests.post(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers={**HEADERS_AUTH, 'Content-Type': 'application/json', 'Prefer': 'return=representation'},
        json=record, verify=False
    )
    return res.status_code, res.text[:300]

# ─── Main upload loop ────────────────────────────────────────────────────────

for ws in WORKSHEETS:
    ts = int(datetime.now().timestamp() * 1000)
    print(f'\n{"="*60}')
    print(f'Uploading: {ws["title"]}')

    # 1. Worksheet PDF
    pdf_path = f'a1/{ts}-{ws["slug"]}.pdf'
    pdf_url = upload_pdf(os.path.join(DL, ws['pdf']), pdf_path)
    if not pdf_url:
        continue
    print(f'  OK: PDF uploaded')

    # 2. Thumbnail
    thumb_path = f'thumbnails/{ts}-{ws["slug"]}.webp'
    thumb_url = upload_thumb(os.path.join(DL, ws['thumb']), thumb_path)
    if not thumb_url:
        continue
    print(f'  OK: Thumbnail uploaded')

    # 3. Teacher Edition PDF
    te_path = f'teacher-editions/a1/{ts}-te_{ws["slug"]}.pdf'
    te_url = upload_pdf(os.path.join(DL, ws['te_pdf']), te_path)
    if not te_url:
        print(f'  WARNING: Teacher edition upload failed, continuing without it')
        te_url = None
    else:
        print(f'  OK: Teacher Edition uploaded')

    # 4. DB Insert
    record = {
        'id': str(uuid.uuid4()),
        'title': ws['title'],
        'level': ws['level'],
        'category': ws['category'],
        'tags': ws['tags'],
        'description': ws['description'],
        'file_url': pdf_url,
        'thumbnail_url': thumb_url,
        'teacher_edition_url': te_url,
        'is_free': ws['is_free'],
        'downloads': 0,
    }
    status, text = insert_worksheet(record)
    if status in (200, 201):
        print(f'  OK: DB record inserted — Free: {ws["is_free"]}')
    else:
        print(f'  ERROR DB insert: {status} {text}')

print(f'\n{"="*60}')
print('Done! All There Is / There Are A1 worksheets uploaded to Workshido.')
