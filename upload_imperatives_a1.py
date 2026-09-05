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
        'slug': 'imperativesgrammara1',
        'pdf':  'imperativesgrammara1.pdf',
        'thumb':'imperativesgrammara1.png',
        'title': 'Imperatives – Grammar Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, imperatives, commands, instructions, grammar, a1, english',
        'description': 'A complete A1 grammar worksheet on imperatives. Includes rules and examples for giving orders, instructions and advice, plus exercises to choose, match, complete, reorder, rewrite and produce imperative sentences.',
        'is_free': True,
        'te_pdf': 'te_imperatives_grammar_a1.pdf',
        'te_title': 'Imperatives – Grammar – Teacher Edition',
        'te_description': 'Teacher Edition for the Imperatives Grammar A1 worksheet. Includes full answer key, a complete lesson plan, common student mistakes, teacher tip, extra activity, and worksheet information.',
    },
    {
        'slug': 'imperativesreadinga1',
        'pdf':  'imperativesreadinga1.pdf',
        'thumb':'imperativesreadinga1.png',
        'title': 'Imperatives – Reading Worksheet',
        'level': 'A1',
        'category': 'Reading',
        'tags': 'worksheet, imperatives, commands, instructions, reading, a1, english',
        'description': 'An A1 reading worksheet based on three short informational texts using imperatives: a park sign, a rules list, and tablet care instructions. Includes comprehension, true/false, vocabulary, and personal response sections.',
        'is_free': True,
        'te_pdf': 'te_imperatives_reading_a1.pdf',
        'te_title': 'Imperatives – Reading – Teacher Edition',
        'te_description': 'Teacher Edition for the Imperatives Reading A1 worksheet. Includes answer key for all exercises, true/false table, vocabulary answers, a complete lesson plan, teacher tip, common mistakes, and extra activity.',
    },
    {
        'slug': 'imperativesvocabularya1',
        'pdf':  'imperativesvocabularya1.pdf',
        'thumb':'imperativesvocabularya1.png',
        'title': 'Imperatives – Vocabulary Worksheet',
        'level': 'A1',
        'category': 'Vocabulary',
        'tags': 'worksheet, imperatives, commands, instructions, vocabulary, a1, english',
        'description': 'An A1 vocabulary worksheet practicing imperatives with everyday action verbs. Includes picture matching, categorizing, a word search, sentence completion, unscrambling, and picture-based production.',
        'is_free': True,
        'te_pdf': 'te_imperatives_vocabulary_a1.pdf',
        'te_title': 'Imperatives – Vocabulary – Teacher Edition',
        'te_description': 'Teacher Edition for the Imperatives Vocabulary A1 worksheet. Includes full answer key, a complete lesson plan, teacher tip, common mistakes, and an extra charades activity.',
    },
    {
        'slug': 'imperativeswritinga1',
        'pdf':  'imperativeswritinga1.pdf',
        'thumb':'imperativeswritinga1.png',
        'title': 'Imperatives – Writing Worksheet',
        'level': 'A1',
        'category': 'Writing',
        'tags': 'worksheet, imperatives, commands, instructions, writing, a1, english',
        'description': 'An A1 writing worksheet practicing imperatives for clear instructions and advice. Students build sentences, use picture prompts, complete guided writing, transform sentences, and write their own instructions with a self-check.',
        'is_free': True,
        'te_pdf': 'te_imperatives_writing_a1.pdf',
        'te_title': 'Imperatives – Writing – Teacher Edition',
        'te_description': 'Teacher Edition for the Imperatives Writing A1 worksheet. Includes model answers, a complete lesson plan, teacher tip, common mistakes, and an extra instruction-manual activity.',
    },
    {
        'slug': 'imperativespracticea1',
        'pdf':  'imperativespracticea1.pdf',
        'thumb':'imperativespracticea1.png',
        'title': 'Imperatives – Practice Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, imperatives, commands, instructions, practice, grammar, a1, english',
        'description': 'A comprehensive A1 practice worksheet on imperatives with 10 exercises. Covers choosing correct options, matching situations, sign reading, sentence transformation, error correction, and free writing — ideal for consolidation.',
        'is_free': True,
        'te_pdf': 'te_imperatives_practice_a1.pdf',
        'te_title': 'Imperatives – Practice – Teacher Edition',
        'te_description': 'Teacher Edition for the Imperatives Practice A1 worksheet. Includes complete answer key for all 10 exercises, a full lesson plan, teacher tip, common mistakes, and a classroom-rules-poster activity.',
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
print('Done! All Imperatives A1 worksheets uploaded to Workshido.')
