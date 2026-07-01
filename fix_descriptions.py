import requests, warnings
warnings.filterwarnings('ignore')

SUPABASE_URL = 'https://mhbgxdsdaalvtgobnvbh.supabase.co'
SERVICE_KEY  = 'REDACTED_SUPABASE_SERVICE_KEY'
HEADERS = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal',
}

UPDATES = [
    {
        'id': '9a0f24e3-73bc-4e61-a0e1-8e61297224ef',
        'description': 'Explore words and expressions used with Future Simple Tense. Includes word-picture matching, fill-in-the-blank exercises, column sorting, and a personal vocabulary challenge.',
    },
    {
        'id': '11e8909b-c3d9-4fa2-a7d5-f975ba43f992',
        'description': 'Practice will/won\'t in affirmative, negative, and question forms. Includes sentence ordering, rewriting, error correction, and a guided writing activity.',
    },
    {
        'id': '840a590c-bf6d-4329-963d-602837e367b0',
        'description': 'Write sentences and short paragraphs about future plans using Future Simple. Includes guided sentence completion, picture-based writing, question formation, and a creative writing challenge.',
    },
    {
        'id': '3860590c-9035-41ec-b7f6-a8633b7cb3d5',
        'description': 'Read a letter about future plans and complete a set of comprehension tasks. Includes true/false statements, vocabulary matching, multiple choice, and a short personal writing activity.',
    },
    {
        'id': 'b1b7277f-3353-4422-a5e9-4ab502880b5a',
        'description': 'Practice Future Simple Tense through fill-in-the-blank, sentence transformation, affirmative/negative/question forms, and error correction exercises.',
    },
]

for u in UPDATES:
    wid = u['id']
    res = requests.patch(
        f'{SUPABASE_URL}/rest/v1/worksheets?id=eq.{wid}',
        headers=HEADERS,
        json={'description': u['description']},
        verify=False
    )
    status = 'OK' if res.status_code in (200, 201, 204) else f'FAIL {res.status_code}: {res.text[:100]}'
    print(f'{wid[:8]}... {status}')

print('\nListo!')
