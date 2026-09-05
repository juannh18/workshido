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
        'slug': 'demonstrativesgrammara1',
        'pdf':  'demonstrativesgrammara1.pdf',
        'thumb':'demonstrativesgrammara1.png',
        'title': 'Demonstratives – Grammar Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, demonstratives, this that these those, grammar, a1, english',
        'description': 'A complete A1 grammar worksheet on demonstratives (this, that, these, those). Includes a grammar box with near/far and singular/plural rules, plus exercises to choose, complete, describe pictures, and rewrite sentences.',
        'is_free': True,
        'te_pdf': 'te_demonstratives_grammar_a1.pdf',
        'te_title': 'Demonstratives – Grammar – Teacher Edition',
        'te_description': 'Teacher Edition for the Demonstratives Grammar A1 worksheet. Includes full answer key, a complete lesson plan, common student mistakes, teacher tip, extra activity, and worksheet information.',
    },
    {
        'slug': 'demonstrativesreadinga1',
        'pdf':  'demonstrativesreadinga1.pdf',
        'thumb':'demonstrativesreadinga1.png',
        'title': 'Demonstratives – Reading Worksheet',
        'level': 'A1',
        'category': 'Reading',
        'tags': 'worksheet, demonstratives, this that these those, reading, a1, english',
        'description': 'An A1 reading worksheet based on "Tom\'s Room" — a short descriptive text using this, that, these and those. Includes comprehension, true/false, vocabulary, and short answer sections.',
        'is_free': True,
        'te_pdf': 'te_demonstratives_reading_a1.pdf',
        'te_title': 'Demonstratives – Reading – Teacher Edition',
        'te_description': 'Teacher Edition for the Demonstratives Reading A1 worksheet. Includes answer key for all exercises, true/false table, vocabulary answers, a complete lesson plan, teacher tip, common mistakes, and extra activity.',
    },
    {
        'slug': 'demonstrativesvocabularya1',
        'pdf':  'demonstrativesvocabularya1.pdf',
        'thumb':'demonstrativesvocabularya1.png',
        'title': 'Demonstratives – Vocabulary Worksheet',
        'level': 'A1',
        'category': 'Vocabulary',
        'tags': 'worksheet, demonstratives, this that these those, vocabulary, a1, english',
        'description': 'An A1 vocabulary worksheet practicing this, that, these and those with everyday objects. Includes matching, categorizing, sentence completion, odd-one-out, and pair work speaking practice.',
        'is_free': True,
        'te_pdf': 'te_demonstratives_vocabulary_a1.pdf',
        'te_title': 'Demonstratives – Vocabulary – Teacher Edition',
        'te_description': 'Teacher Edition for the Demonstratives Vocabulary A1 worksheet. Includes full answer key, a complete lesson plan, suggested pair-work dialogues, teacher tip, common mistakes, and extra activity.',
    },
    {
        'slug': 'demonstrativeswritinga1',
        'pdf':  'demonstrativeswritinga1.pdf',
        'thumb':'demonstrativeswritinga1.png',
        'title': 'Demonstratives – Writing Worksheet',
        'level': 'A1',
        'category': 'Writing',
        'tags': 'worksheet, demonstratives, this that these those, writing, a1, english',
        'description': 'An A1 writing worksheet practicing this, that, these and those. Students practice picture-based sentence writing, describing their classroom, and produce a short paragraph about their own room.',
        'is_free': True,
        'te_pdf': 'te_demonstratives_writing_a1.pdf',
        'te_title': 'Demonstratives – Writing – Teacher Edition',
        'te_description': 'Teacher Edition for the Demonstratives Writing A1 worksheet. Includes model answers for guided writing, a complete lesson plan, teacher tip, common mistakes, and an extra describe-and-guess activity.',
    },
    {
        'slug': 'demonstrativespracticea1',
        'pdf':  'demonstrativespracticea1.pdf',
        'thumb':'demonstrativespracticea1.png',
        'title': 'Demonstratives – Practice Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, demonstratives, this that these those, practice, grammar, a1, english',
        'description': 'A comprehensive A1 practice worksheet on demonstratives with 10 exercises. Covers choosing the correct word, completing sentences, matching, ordering, mini dialogues, and free writing — ideal for consolidation.',
        'is_free': True,
        'te_pdf': 'te_demonstratives_practice_a1.pdf',
        'te_title': 'Demonstratives – Practice – Teacher Edition',
        'te_description': 'Teacher Edition for the Demonstratives Practice A1 worksheet. Includes complete answer key for all 10 exercises, a full lesson plan, suggested answers for open tasks, teacher tip, common mistakes, and an error-auction review activity.',
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
print('Done! All Demonstratives A1 worksheets uploaded to Workshido.')
