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
        'slug': 'goingtogrammara1',
        'pdf':  'goingtogrammara1.pdf',
        'thumb':'goingtogrammara1.png',
        'title': 'Going To – Grammar Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, going to, grammar, future plans, a1, english',
        'description': 'A complete A1 grammar worksheet on "Going To". Includes a grammar box with affirmative, negative, and question forms, plus exercises to complete sentences, write negatives, form questions, and use am/is/are correctly.',
        'is_free': True,
        'te_pdf': 'te_going_to_grammar_a1.pdf',
        'te_title': 'Going To – Grammar – Teacher Edition',
        'te_description': 'Teacher Edition for the Going To Grammar A1 worksheet. Includes full answer key, common student mistakes, teacher tip, extra activity, and worksheet information.',
    },
    {
        'slug': 'goingtoreadinga1',
        'pdf':  'goingtoreadinga1.pdf',
        'thumb':'goingtoreadinga1.png',
        'title': 'Going To – Reading Worksheet',
        'level': 'A1',
        'category': 'Reading',
        'tags': 'worksheet, going to, reading, future plans, a1, english',
        'description': 'An A1 reading worksheet based on "My Plans for the Summer" — a short personal text about Laura\'s future plans. Includes pre-reading, comprehension, vocabulary review, inference, and a reflection section.',
        'is_free': True,
        'te_pdf': 'te_going_to_reading_a1.pdf',
        'te_title': 'Going To – Reading – Teacher Edition',
        'te_description': 'Teacher Edition for the Going To Reading A1 worksheet. Includes answer key for all exercises, true/false table, vocabulary answers, suggested reflection answers, teacher tip, common mistakes, and extra activity.',
    },
    {
        'slug': 'goingtowritinga1',
        'pdf':  'goingtowritinga1.pdf',
        'thumb':'goingtowritinga1.png',
        'title': 'Going To – Writing Worksheet',
        'level': 'A1',
        'category': 'Writing',
        'tags': 'worksheet, going to, writing, future plans, a1, english',
        'description': 'An A1 writing worksheet on "Going To" for future plans. Students practice sentence building, guided writing, weekend and vacation plans, and produce an independent paragraph about their own future plans.',
        'is_free': True,
        'te_pdf': 'te_going_to_writing_a1.pdf',
        'te_title': 'Going To – Writing – Teacher Edition',
        'te_description': 'Teacher Edition for the Going To Writing A1 worksheet. Includes model answers for guided writing, sentence builder key, writing checklist guidance, teacher tip, common mistakes, and an extra class survey activity.',
    },
    {
        'slug': 'goingtovocabularya1',
        'pdf':  'goingtovocabularya1.pdf',
        'thumb':'goingtovocabularya1.png',
        'title': 'Going To – Vocabulary Worksheet',
        'level': 'A1',
        'category': 'Vocabulary',
        'tags': 'worksheet, going to, vocabulary, future plans, travel, activities, a1, english',
        'description': 'An A1 vocabulary worksheet focused on key words for talking about future plans: travel, activities, places, and time expressions. Includes matching, categorizing, sentence completion, and personal production exercises.',
        'is_free': True,
        'te_pdf': 'te_going_to_vocabulary_a1.pdf',
        'te_title': 'Going To – Vocabulary – Teacher Edition',
        'te_description': 'Teacher Edition for the Going To Vocabulary A1 worksheet. Includes full answer key for all exercises, categorized word lists, sentence completion answers, suggested production sentences, teacher tip, common mistakes, and vocabulary bingo activity.',
    },
    {
        'slug': 'goingtopracticea1',
        'pdf':  'goingtopracticea1.pdf',
        'thumb':'goingtopracticea1.png',
        'title': 'Going To – Practice Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, going to, practice, grammar, a1, english',
        'description': 'A comprehensive A1 practice worksheet on "Going To" with 10 exercises. Covers choosing correct options, completing sentences, reading comprehension, sentence construction, and a writing task — ideal for consolidation or exam preparation.',
        'is_free': False,
        'te_pdf': 'te_going_to_practice_a1.pdf',
        'te_title': 'Going To – Practice – Teacher Edition',
        'te_description': 'Teacher Edition for the Going To Practice A1 worksheet. Includes complete answer key for all 10 exercises, suggested answers for open tasks, teacher tip for peer correction, common mistakes, and a fast-finish challenge activity.',
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
print('Done! All Going To A1 worksheets uploaded to Workshido.')
