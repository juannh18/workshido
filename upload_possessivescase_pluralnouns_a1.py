import requests, os, uuid, io
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
        'slug': 'possessivescasegrammara1',
        'pdf':  'possessivescasegrammara1.pdf',
        'thumb':'possessivescasegrammara1.png',
        'title': "Possessive 's (Possessive Case) – Grammar Worksheet",
        'level': 'A1',
        'category': 'Grammar',
        'tags': "worksheet, possessive s, possessive case, apostrophe, grammar, a1, english",
        'description': "A complete A1 grammar worksheet on the possessive 's (possessive case), including plural nouns ending in -s and irregular plurals. Students add 's to nouns, rewrite of-phrases, identify possessives, choose the correct form, and build their own sentences.",
        'is_free': True,
        'te_pdf': 'te_possessivescase_grammar_a1.pdf',
        'te_title': "Possessive 's – Grammar – Teacher Edition",
        'te_description': "Teacher Edition for the Possessive 's Grammar A1 worksheet. Includes full answer key for all 5 exercises, a complete lesson plan, common student mistakes, teacher tip, and extra activity.",
    },
    {
        'slug': 'possessivescasereadinga1',
        'pdf':  'possessivescasereadinga1.pdf',
        'thumb':'possessivescasereadinga1.png',
        'title': "Possessive 's (Possessive Case) – Reading Worksheet",
        'level': 'A1',
        'category': 'Reading',
        'tags': "worksheet, possessive s, possessive case, reading comprehension, family, a1, english",
        'description': "An A1 reading worksheet based on the text \"Mia's Weekend\", full of possessive 's forms in context. Includes before-reading predictions, vocabulary in context, comprehension questions, thinking-more questions, and a personal response.",
        'is_free': True,
        'te_pdf': 'te_possessivescase_reading_a1.pdf',
        'te_title': "Possessive 's – Reading – Teacher Edition",
        'te_description': "Teacher Edition for the Possessive 's Reading A1 worksheet. Includes answer key for all exercises, suggested vocabulary meanings, model personal responses, a complete lesson plan, teacher tip, common mistakes, and extra activity.",
    },
    {
        'slug': 'possessivescasewritinga1',
        'pdf':  'possessivescasewritinga1.pdf',
        'thumb':'possessivescasewritinga1.png',
        'title': "Possessive 's (Possessive Case) – Writing Worksheet",
        'level': 'A1',
        'category': 'Writing',
        'tags': "worksheet, possessive s, possessive case, writing, guided writing, a1, english",
        'description': "An A1 writing worksheet on the possessive 's. Students complete a sentence builder (including plural and joint possession), write 5 sentences about a picture, and produce their own 6–8 sentence paragraph with a self-check checklist.",
        'is_free': True,
        'te_pdf': 'te_possessivescase_writing_a1.pdf',
        'te_title': "Possessive 's – Writing – Teacher Edition",
        'te_description': "Teacher Edition for the Possessive 's Writing A1 worksheet. Includes answer key and model paragraph, a complete lesson plan, common student mistakes, teacher tip, and a guessing-game extra activity.",
    },
    {
        'slug': 'pluralnounsgrammar1a1',
        'pdf':  'pluralnounsgrammar1a1.pdf',
        'thumb':'PluralNounsGrammarworksheet1a1.png',
        'title': 'Plural Nouns – Grammar Worksheet 1',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, plural nouns, plurals, grammar, a1, english',
        'description': 'An A1 grammar worksheet on regular plural noun rules (-s, -es, -ies, vowel + y) plus basic irregulars. Includes a rule chart to complete, plural writing practice, choose-the-option sentences, a paragraph noun sort, and a classroom writing challenge.',
        'is_free': True,
        'te_pdf': 'te_pluralnouns_grammar1_a1.pdf',
        'te_title': 'Plural Nouns – Grammar 1 – Teacher Edition',
        'te_description': 'Teacher Edition for the Plural Nouns Grammar 1 A1 worksheet. Includes full answer key with teaching notes, a complete lesson plan, common student mistakes, pronunciation teacher tip, and a plural corners activity.',
    },
    {
        'slug': 'irregularpluralnounsgrammar2a1',
        'pdf':  'irregularpluralnounsgrammar2a1.pdf',
        'thumb':'Irregularpluralnounsgrammarworksheet2a1.png',
        'title': 'Irregular Plural Nouns – Grammar Worksheet 2',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, irregular plural nouns, plurals, grammar, a1, english',
        'description': 'An A1 grammar worksheet on irregular plural nouns (men, teeth, mice, sheep, geese, oxen and more). Includes a study table, plural writing with no-change and Latin/Greek forms, choose-the-option sentences, a paragraph hunt, and a sentence challenge.',
        'is_free': True,
        'te_pdf': 'te_irregularpluralnouns_grammar2_a1.pdf',
        'te_title': 'Irregular Plural Nouns – Grammar 2 – Teacher Edition',
        'te_description': 'Teacher Edition for the Irregular Plural Nouns Grammar 2 A1 worksheet. Includes full answer key with accepted alternatives, a complete lesson plan, common student mistakes, pattern-grouping teacher tip, and a flashcard matching game.',
    },
    {
        'slug': 'pluralnounspracticea1',
        'pdf':  'pluralnounspracticea1.pdf',
        'thumb':'Pluralnounspracticeworksheeta1.png',
        'title': 'Plural Nouns – Practice Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, plural nouns, plurals, practice, grammar, a1, english',
        'description': 'A complete A1 practice worksheet reviewing all plural noun rules: -s, -es, -ies, o → oes, f → ves and irregulars. Includes plural writing, choose-the-option, a three-column noun sort, sentence rewriting, gap completion, a paragraph sort, and a writing challenge.',
        'is_free': True,
        'te_pdf': 'te_pluralnouns_practice_a1.pdf',
        'te_title': 'Plural Nouns – Practice – Teacher Edition',
        'te_description': 'Teacher Edition for the Plural Nouns Practice A1 worksheet. Includes full answer key for all 7 sections with teaching notes, a complete lesson plan, common student mistakes, diagnostic teacher tip, and a plural auction game.',
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
print("Done! Possessive 's + Plural Nouns A1 worksheets uploaded to Workshido.")
