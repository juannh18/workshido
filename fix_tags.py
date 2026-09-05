import requests, warnings
warnings.filterwarnings('ignore')

from env_secrets import SUPABASE_URL, SERVICE_KEY

HEADERS = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal',
}

UPDATES = [
    # Future Simple
    {'id': '9a0f24e3-73bc-4e61-a0e1-8e61297224ef', 'tags': 'worksheet, future simple, vocabulary, expressions, tense, A2'},
    {'id': '11e8909b-c3d9-4fa2-a7d5-f975ba43f992', 'tags': 'worksheet, future simple, review, will, grammar, practice, A2'},
    {'id': '840a590c-bf6d-4329-963d-602837e367b0', 'tags': 'worksheet, future simple, writing, plans, will, A2'},
    {'id': '3860590c-9035-41ec-b7f6-a8633b7cb3d5', 'tags': 'worksheet, future simple, reading, comprehension, will, A2'},
    {'id': 'b1b7277f-3353-4422-a5e9-4ab502880b5a', 'tags': 'worksheet, future simple, grammar, sentences, practice, A2'},
    # Past Simple
    {'id': '281649bd-aede-423f-ab26-ea952bb9fbbc', 'tags': 'worksheet, past simple, vocabulary, grammar, A2'},
    {'id': '0919786b-f335-443b-88a4-917f34891d0f', 'tags': 'worksheet, past simple, grammar, practice, A2'},
]

for u in UPDATES:
    res = requests.patch(
        f'{SUPABASE_URL}/rest/v1/worksheets?id=eq.{u["id"]}',
        headers=HEADERS,
        json={'tags': u['tags']},
        verify=False
    )
    status = 'OK' if res.status_code in (200, 201, 204) else f'FAIL {res.status_code}: {res.text[:100]}'
    print(f'{u["id"][:8]}... {status}')

print('\nListo!')
