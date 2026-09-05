"""
Batch upload — Prepositions of Place worksheets (A1)
Se insertan con created_at ANTERIOR al worksheet mas antiguo existente
para que aparezcan de ultimas en el home (orden: created_at desc).
"""
import requests, uuid, warnings
warnings.filterwarnings('ignore')

from env_secrets import SUPABASE_URL, SERVICE_KEY

HEADERS = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
}

DL = r'C:\Users\juand\Downloads'

# created_at mas antiguo actual en la tabla: 2026-06-18T16:28:48.929467+00:00
# Se usan timestamps anteriores a esa fecha, en orden grammar > reading > writing
WORKSHEETS = [
    {
        'slug': 'prepositionsofplacereadinga1',
        'pdf': 'prepositionsofplacereadinga1.pdf',
        'thumb': 'prepositionsofplacereadinga1_thumb.webp',
        'title': 'Prepositions of Place – Reading Worksheet',
        'level': 'A1',
        'category': 'Reading',
        'tags': 'worksheet, prepositions of place, reading, a1, english',
        'description': 'An A1 reading worksheet describing a bedroom using prepositions of place. Includes pre-reading questions, vocabulary in context, comprehension questions, true/false, and a personal response task.',
        'is_free': True,
        'te_pdf': 'te_prepositions_place_reading_a1.pdf',
        'te_title': 'Prepositions of Place – Reading – Teacher Edition',
        'te_description': 'Teacher Edition for the Prepositions of Place Reading A1 worksheet. Includes full answer key, vocabulary matching answers, a complete lesson plan, teacher tip, common mistakes, and extra activity.',
        'created_at': '2026-06-17T23:56:00+00:00',
    },
    {
        'slug': 'prepositionsofplacewritinga1',
        'pdf': 'prepositionsofplacewritinga1.pdf',
        'thumb': 'prepositionsofplacewritinga1_thumb.webp',
        'title': 'Prepositions of Place – Writing Worksheet',
        'level': 'A1',
        'category': 'Writing',
        'tags': 'worksheet, prepositions of place, writing, a1, english',
        'description': 'An A1 writing worksheet on Prepositions of Place for describing rooms. Students practice sentence building, guided picture writing, completing a description, and writing their own paragraph about a room.',
        'is_free': True,
        'te_pdf': 'te_prepositions_place_writing_a1.pdf',
        'te_title': 'Prepositions of Place – Writing – Teacher Edition',
        'te_description': 'Teacher Edition for the Prepositions of Place Writing A1 worksheet. Includes full answer key, a complete lesson plan, common student mistakes, teacher tip, and extra activity.',
        'created_at': '2026-06-17T23:55:00+00:00',
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
    print(f'\n{"="*60}')
    print(f'Uploading: {ws["title"]}')

    # ts en el nombre de archivo (solo para no chocar nombres, no afecta el orden del home)
    ts = int(__import__('datetime').datetime.now().timestamp() * 1000)

    pdf_path = f'a1/{ts}-{ws["slug"]}.pdf'
    pdf_url = upload_pdf(f'{DL}\\{ws["pdf"]}', pdf_path)
    if not pdf_url:
        continue
    print('  OK: PDF uploaded')

    thumb_path = f'thumbnails/{ts}-{ws["slug"]}.webp'
    thumb_url = upload_thumb(f'{DL}\\{ws["thumb"]}', thumb_path)
    if not thumb_url:
        continue
    print('  OK: Thumbnail uploaded')

    te_path = f'teacher-editions/a1/{ts}-te_{ws["slug"]}.pdf'
    te_url = upload_pdf(f'{DL}\\{ws["te_pdf"]}', te_path)
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
        'created_at': ws['created_at'],
    }
    status, text = insert_worksheet(record)
    if status in (200, 201):
        print(f'  OK: DB record inserted — created_at: {ws["created_at"]}')
    else:
        print(f'  ERROR DB insert: {status} {text}')

print(f'\n{"="*60}')
print('Done! Prepositions of Place A1 worksheets uploaded to Workshido.')
