"""
Batch upload — Have Got / Has Got worksheets (A1)
"""
import requests, uuid, warnings
from datetime import datetime
warnings.filterwarnings('ignore')

from env_secrets import SUPABASE_URL, SERVICE_KEY

HEADERS = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
}

DL = r'C:\Users\juand\Downloads'
SCRATCH = r'C:\Users\juand\AppData\Local\Temp\claude\C--Users-juand-OneDrive-Desktop-Workshido\7acc255a-1c98-48a7-8053-710bcca8851f\scratchpad'

WORKSHEETS = [
    {
        'slug': 'havegothasgotgrammara1',
        'pdf': f'{DL}\\havegothasgotgrammara1.pdf',
        'thumb': f'{DL}\\havegothasgotgrammara1_thumb.webp',
        'title': 'Have Got / Has Got – Grammar Worksheet',
        'level': 'A1',
        'category': 'Grammar',
        'tags': 'worksheet, have got has got, grammar, a1, english',
        'description': 'A complete A1 grammar worksheet on "Have Got / Has Got". Includes a grammar box with affirmative, negative and question forms, a form summary table, and five practice exercises.',
        'is_free': True,
        'te_pdf': f'{SCRATCH}\\te_havegothasgot_grammar_a1.pdf',
        'te_title': 'Have Got / Has Got – Grammar – Teacher Edition',
        'te_description': 'Teacher Edition for the Have Got / Has Got Grammar A1 worksheet. Includes full answer key, a complete lesson plan, common student mistakes, teacher tip, extra activity, and worksheet information.',
    },
    {
        'slug': 'havegothasgotreadinga1',
        'pdf': f'{DL}\\havegothasgotreadinga1.pdf',
        'thumb': f'{DL}\\havegothasgotreadinga1_thumb.webp',
        'title': 'Have Got / Has Got – Reading Worksheet',
        'level': 'A1',
        'category': 'Reading',
        'tags': 'worksheet, have got has got, reading, a1, english',
        'description': 'An A1 reading worksheet based on "My Life, My Things" — a short personal text about possessions using have got / has got. Includes vocabulary matching, comprehension questions, and a speaking activity.',
        'is_free': True,
        'te_pdf': f'{SCRATCH}\\te_havegothasgot_reading_a1.pdf',
        'te_title': 'Have Got / Has Got – Reading – Teacher Edition',
        'te_description': 'Teacher Edition for the Have Got / Has Got Reading A1 worksheet. Includes full answer key, vocabulary matching answers, a complete lesson plan, teacher tip, common mistakes, and extra activity.',
    },
    {
        'slug': 'havegothasgotwritinga1',
        'pdf': f'{DL}\\havegothasgotwritinga1.pdf',
        'thumb': f'{DL}\\havegothasgotwritinga1_thumb.webp',
        'title': 'Have Got / Has Got – Writing Worksheet',
        'level': 'A1',
        'category': 'Writing',
        'tags': 'worksheet, have got has got, writing, a1, english',
        'description': 'An A1 writing worksheet on "Have Got / Has Got" for describing people and possessions. Students practice sentence building, picture description, question writing, and a guided paragraph about their family.',
        'is_free': True,
        'te_pdf': f'{SCRATCH}\\te_havegothasgot_writing_a1.pdf',
        'te_title': 'Have Got / Has Got – Writing – Teacher Edition',
        'te_description': 'Teacher Edition for the Have Got / Has Got Writing A1 worksheet. Includes full answer key, a complete lesson plan, common student mistakes, teacher tip, and extra activity.',
    },
]

def upload_pdf(local_path, storage_path):
    with open(local_path, 'rb') as f:
        res = requests.post(
            f'{SUPABASE_URL}/storage/v1/object/worksheets/{storage_path}',
            headers={**HEADERS, 'Content-Type': 'application/pdf', 'x-upsert': 'true'},
            data=f, verify=False
        )
    if res.status_code not in (200, 201):
        print(f'  ERROR PDF upload: {res.status_code} {res.text[:200]}')
        return None
    return f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{storage_path}'

def upload_thumb(local_path, storage_path):
    with open(local_path, 'rb') as f:
        res = requests.post(
            f'{SUPABASE_URL}/storage/v1/object/worksheets/{storage_path}',
            headers={**HEADERS, 'Content-Type': 'image/webp', 'x-upsert': 'true'},
            data=f, verify=False
        )
    if res.status_code not in (200, 201):
        print(f'  ERROR thumb upload: {res.status_code} {res.text[:200]}')
        return None
    return f'{SUPABASE_URL}/storage/v1/object/public/worksheets/{storage_path}'

def insert_worksheet(record):
    res = requests.post(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers={**HEADERS, 'Content-Type': 'application/json', 'Prefer': 'return=representation'},
        json=record, verify=False
    )
    return res.status_code, res.text[:300]

for ws in WORKSHEETS:
    ts = int(datetime.now().timestamp() * 1000)
    print(f'\n{"="*60}')
    print(f'Uploading: {ws["title"]}')

    pdf_path = f'a1/{ts}-{ws["slug"]}.pdf'
    pdf_url = upload_pdf(ws['pdf'], pdf_path)
    if not pdf_url:
        continue
    print('  OK: PDF uploaded')

    thumb_path = f'thumbnails/{ts}-{ws["slug"]}.webp'
    thumb_url = upload_thumb(ws['thumb'], thumb_path)
    if not thumb_url:
        continue
    print('  OK: Thumbnail uploaded')

    te_path = f'teacher-editions/a1/{ts}-te_{ws["slug"]}.pdf'
    te_url = upload_pdf(ws['te_pdf'], te_path)
    if not te_url:
        print('  WARNING: Teacher edition upload failed, continuing without it')
    else:
        print('  OK: Teacher Edition uploaded')

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
        'is_free': True,
        'downloads': 0,
    }
    status, text = insert_worksheet(record)
    if status in (200, 201):
        print('  OK: DB record inserted')
    else:
        print(f'  ERROR DB insert: {status} {text}')

print(f'\n{"="*60}')
print('Done! Have Got / Has Got A1 worksheets uploaded to Workshido.')
