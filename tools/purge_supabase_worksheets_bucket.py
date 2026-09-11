"""One-off cleanup: delete every object in the Supabase Storage `worksheets`
bucket.

Context: worksheet/quiz files were migrated to Cloudflare R2 on 2026-08-20
(see memory/project_r2_migration.md) but the originals were never removed from
Supabase Storage. By 2026-09-10 that bucket held ~1.19 GB across 2,146 objects,
pushing the project over the 1 GB free-tier limit. Verified before running:
- all 716 `worksheets` rows and all 75 `quizzes` rows reference
  files.workshido.com (R2); zero rows reference Supabase Storage
- no public table has any 'supabase' URL in any text column
- no Netlify function signs/serves from a Supabase bucket
- sampled files exist byte-identical on R2

Reads the authoritative object list from a text file (one key per line) and
deletes in batches via the Storage REST API. Safe to re-run (missing keys are
simply ignored by the API).
"""
import json
import sys
import time
import urllib.request

sys.path.insert(0, __file__.rsplit('\\', 2)[0])
from env_secrets import SUPABASE_URL, SERVICE_KEY

BUCKET = 'worksheets'
LIST_FILE = (
    r'C:\Users\juand\AppData\Local\Temp\claude'
    r'\C--Users-juand-OneDrive-Desktop-Workshido'
    r'\fd0fe0cb-308a-462b-86a4-6bdd9f6fd09e\scratchpad\ws_bucket_objects.txt'
)
BATCH = 100
ENDPOINT = f'{SUPABASE_URL}/storage/v1/object/{BUCKET}'


def _delete(prefixes):
    body = json.dumps({'prefixes': prefixes}).encode('utf-8')
    req = urllib.request.Request(ENDPOINT, data=body, method='DELETE')
    req.add_header('Authorization', f'Bearer {SERVICE_KEY}')
    req.add_header('apikey', SERVICE_KEY)
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main():
    with open(LIST_FILE, encoding='utf-8') as f:
        keys = [ln.strip() for ln in f if ln.strip()]
    print(f'{len(keys)} objects to delete from bucket "{BUCKET}"')

    deleted = 0
    for i in range(0, len(keys), BATCH):
        chunk = keys[i:i + BATCH]
        for attempt in range(3):
            try:
                res = _delete(chunk)
                deleted += len(res) if isinstance(res, list) else len(chunk)
                print(f'  batch {i // BATCH + 1}: removed {len(chunk)} '
                      f'({deleted}/{len(keys)})')
                break
            except Exception as e:  # noqa: BLE001
                print(f'  batch {i // BATCH + 1} attempt {attempt + 1} failed: {e}')
                time.sleep(2 + attempt * 3)
        else:
            print(f'  !! batch {i // BATCH + 1} gave up, continuing')
        time.sleep(0.3)

    print(f'done. API acknowledged {deleted} deletions.')


if __name__ == '__main__':
    main()
