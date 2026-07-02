import requests, json, os, uuid, io
from datetime import datetime
from PIL import Image

SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co'
SERVICE_KEY  = 'REDACTED_SUPABASE_SERVICE_KEY'

HEADERS_AUTH = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
}

DL = r'C:\Users\juand\Downloads'

# ─── Worksheet definitions ──────────────────────────────────────────────────
WORKSHEETS = [
    {
        'slug': 'possessiveadjectivesgrammara1',
        'pdf':  'possessiveadjectivesgrammara1.pdf',
        'thumb':'possessiveadjectivesgrammara1.png',
        'title': 'Possessive Adjectives – Grammar Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, possessive adjectives, my your his her, grammar, a1, english',
        'description': 'A complete A1 grammar worksheet on possessive adjectives (my, your, his, her, its, our, their). Includes a reference table with examples plus exercises to choose, complete and rewrite sentences.',
        'is_free': True,
        'te_pdf': 'te_possessiveadjectives_grammar_a1.pdf',
        'te_title': 'Possessive Adjectives – Grammar – Teacher Edition',
        'te_description': 'Teacher Edition for the Possessive Adjectives Grammar A1 worksheet. Includes full answer key for all 38 items, a complete lesson plan, common student mistakes, teacher tip, and extra activity.',
    },
    {
        'slug': 'possessiveadjectivesreadinga1',
        'pdf':  'possessiveadjectivesreadinga1.pdf',
        'thumb':'possessiveadjectivesreadinga1.png',
        'title': 'Possessive Adjectives – Reading Worksheet',
        'level': 'A1',
        'category': 'Reading',
        'tags': 'worksheet, possessive adjectives, reading comprehension, family, a1, english',
        'description': 'An A1 reading worksheet based on a blog post ("A Day in Our Lives") about a typical family Saturday, full of possessive adjectives in context. Includes vocabulary matching, comprehension questions, true/false, and personal response.',
        'is_free': True,
        'te_pdf': 'te_possessiveadjectives_reading_a1.pdf',
        'te_title': 'Possessive Adjectives – Reading – Teacher Edition',
        'te_description': 'Teacher Edition for the Possessive Adjectives Reading A1 worksheet. Includes answer key for all exercises, true/false table with corrections, a complete lesson plan, teacher tip, common mistakes, and extra activity.',
    },
    {
        'slug': 'possessiveadjectiveswritinga1',
        'pdf':  'possessiveadjectiveswritinga1.pdf',
        'thumb':'possessiveadjectiveswritinga1.png',
        'title': 'Possessive Adjectives – Writing Worksheet',
        'level': 'A1',
        'category': 'Writing',
        'tags': 'worksheet, possessive adjectives, writing, guided writing, a1, english',
        'description': 'An A1 writing worksheet on possessive adjectives. Students build sentences from prompts, complete a guided text using a word bank and pictures, and write their own paragraph with a self-check checklist.',
        'is_free': True,
        'te_pdf': 'te_possessiveadjectives_writing_a1.pdf',
        'te_title': 'Possessive Adjectives – Writing – Teacher Edition',
        'te_description': 'Teacher Edition for the Possessive Adjectives Writing A1 worksheet. Includes model answers for all exercises, a complete lesson plan, teacher tip, common mistakes, and a picture dictation activity.',
    },
    {
        'slug': 'articlesgrammar1a1',
        'pdf':  'articlesgrammar1a1.pdf',
        'thumb':'articles,a,an,the,grammar01.png',
        'title': 'Articles A, An, The – Grammar Worksheet 1',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, articles, a an the, grammar, a1, english',
        'description': 'An A1 grammar worksheet on articles a, an and the. Students complete a 15-blank story ("A Day in the City"), circle the correct article in 10 sentences, and answer comprehension questions.',
        'is_free': True,
        'te_pdf': 'te_articles_grammar1_a1.pdf',
        'te_title': 'Articles A, An, The – Grammar 1 – Teacher Edition',
        'te_description': 'Teacher Edition for the Articles Grammar 1 A1 worksheet. Includes full answer key with teaching notes, a complete lesson plan, common student mistakes, teacher tip, and extra activity.',
    },
    {
        'slug': 'articlesgrammar2a1',
        'pdf':  'articlesgrammar2a1.pdf',
        'thumb':'articles a,an,the,grammar02.png',
        'title': 'Articles A, An, The – Grammar Worksheet 2',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, articles, a an the, grammar, a1, english',
        'description': 'An A1 grammar worksheet practicing articles a, an and the with the sound rule. Includes picture-based sentence writing, 10 fill-in items featuring tricky cases (a university, an honest person), and a free paragraph.',
        'is_free': True,
        'te_pdf': 'te_articles_grammar2_a1.pdf',
        'te_title': 'Articles A, An, The – Grammar 2 – Teacher Edition',
        'te_description': 'Teacher Edition for the Articles Grammar 2 A1 worksheet. Includes full answer key, model paragraph, a complete lesson plan, common student mistakes, teacher tip, and a sound-sort activity.',
    },
    {
        'slug': 'articlesgrammar3a1',
        'pdf':  'articlesgrammar3a1.pdf',
        'thumb':'articles,a,an,the grammar03.png',
        'title': 'Articles A, An, The – Grammar Worksheet 3',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, articles, a an the, grammar, a1, english',
        'description': 'An A1 grammar worksheet on articles a, an and the focused on first vs. second mention. Includes picture-based sentences, a 10-blank story paragraph, and a guided writing task about a favorite place.',
        'is_free': True,
        'te_pdf': 'te_articles_grammar3_a1.pdf',
        'te_title': 'Articles A, An, The – Grammar 3 – Teacher Edition',
        'te_description': 'Teacher Edition for the Articles Grammar 3 A1 worksheet. Includes full answer key with teaching notes, model answer, a complete lesson plan, common student mistakes, teacher tip, and a story chain activity.',
    },
    {
        'slug': 'articlesreadinga1',
        'pdf':  'articlesreadinga1.pdf',
        'thumb':'articlesa,an,thereading.png',
        'title': 'Articles A, An, The – Reading Worksheet',
        'level': 'A1',
        'category': 'Reading',
        'tags': 'worksheet, articles, a an the, reading comprehension, travel, a1, english',
        'description': 'An A1 reading worksheet based on a travel blog post ("A Weekend in Paris") with 16 article blanks. Includes a parallel circle-the-article exercise, comprehension questions, vocabulary in context, and a reflection prompt.',
        'is_free': True,
        'te_pdf': 'te_articles_reading_a1.pdf',
        'te_title': 'Articles A, An, The – Reading – Teacher Edition',
        'te_description': 'Teacher Edition for the Articles Reading A1 worksheet. Includes answer key for all 16 blanks with teaching notes, comprehension and vocabulary answers, a complete lesson plan, teacher tip, common mistakes, and extra activity.',
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
print('Done! Possessive Adjectives + Articles A1 worksheets uploaded to Workshido.')
