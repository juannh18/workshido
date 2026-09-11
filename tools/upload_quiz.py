"""Sube un Quiz (PDF del estudiante + Answer Key) a Supabase y crea/actualiza
su fila en la tabla `quizzes`, más el `topic_key` en las worksheets que cubre.

Uso:
  python tools/upload_quiz.py manifest_quiz.json

Formato del manifiesto (rutas relativas al repo, ver tools/te_output/):
{
  "topic_key": "present-simple-a2",
  "level": "A2",
  "title": "Present Simple Tense",
  "skills": "Grammar, Reading, Writing",
  "quiz_pdf": "tools/te_output/quiz_present-simple-tense-a2.html",   // PDF ya generado, no el HTML
  "key_pdf": "tools/te_output/quiz_key_present-simple-tense-a2.html",
  "worksheet_ids": ["4c739616-...", "af1d60b9-...", ...]   // filas de `worksheets` que reciben este topic_key
}

Opcional en la raíz del manifiesto: "language": "en" (default) o "es". Con "es"
la fila va a `es.quizzes` (header PostgREST Content-Profile: es), los PDFs van
bajo `es/` en R2, y el PATCH de topic_key va contra `es.worksheets`.

Nota: is_free no aplica a quizzes (siempre son premium, gateados por
get-quiz-url.js). Después de subir, verificar visualmente igual que un
worksheet normal (render_pdf_pages.py) antes de correr esto.
"""
import pip_system_certs.wrapt_requests  # noqa: usa el almacén de certificados de Windows en vez de desactivar la verificación TLS
import requests, boto3, os, json, sys
from botocore.config import Config

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from env_secrets import SUPABASE_URL, SERVICE_KEY, R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY

HEADERS_AUTH = {'apikey': SERVICE_KEY, 'Authorization': f'Bearer {SERVICE_KEY}'}

R2_BUCKET = 'workshido-files'
R2_PUBLIC_BASE = 'https://files.workshido.com'

s3 = boto3.client(
    's3',
    endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name='auto',
    config=Config(signature_version='s3v4'),
)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = r'C:\Users\juand\Downloads'

def resolve(p):
    return p if os.path.isabs(p) else os.path.join(DL, p)

def check_r2_domain():
    try:
        requests.head(R2_PUBLIC_BASE, timeout=5)
    except requests.RequestException:
        sys.exit(
            f'ERROR: {R2_PUBLIC_BASE} no responde todavia.\n'
            'El dominio custom de R2 (files.workshido.com) todavia no esta activo.\n'
            'No subas quizzes nuevos hasta completar ese paso, o quedaran con links rotos.'
        )

def upload_pdf(local_path, storage_path):
    try:
        s3.upload_file(local_path, R2_BUCKET, storage_path, ExtraArgs={
            'ContentType': 'application/pdf',
            'CacheControl': 'public, max-age=31536000, immutable',
        })
    except Exception as e:
        sys.exit(f'ERROR subiendo {storage_path}: {e}')
    return f'{R2_PUBLIC_BASE}/{storage_path}'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    check_r2_domain()
    manifest = json.load(open(sys.argv[1], encoding='utf-8'))

    lang = manifest.get('language', 'en')
    assert lang in ('en', 'es'), f"language debe ser 'en' o 'es', no {lang!r}"
    profile_headers = {'Content-Profile': 'es'} if lang == 'es' else {}
    key_prefix = 'es/' if lang == 'es' else ''
    if lang == 'es':
        print('>> language=es -> esquema es.quizzes + prefijo es/ en R2')

    level_folder = manifest['level'].lower()
    quiz_pdf_url = upload_pdf(resolve(manifest['quiz_pdf']), f'{key_prefix}quizzes/{level_folder}/{manifest["topic_key"]}.pdf')
    key_pdf_url = upload_pdf(resolve(manifest['key_pdf']), f'{key_prefix}quizzes/teacher-editions/{level_folder}/{manifest["topic_key"]}.pdf')
    print('quiz_pdf_url:', quiz_pdf_url)
    print('key_pdf_url:', key_pdf_url)

    row = {
        'topic_key': manifest['topic_key'],
        'level': manifest['level'],
        'title': manifest['title'],
        'skills': manifest['skills'],
        'quiz_pdf_url': quiz_pdf_url,
        'key_pdf_url': key_pdf_url,
    }
    res = requests.post(
        f'{SUPABASE_URL}/rest/v1/quizzes',
        headers={**HEADERS_AUTH, **profile_headers, 'Content-Type': 'application/json', 'Prefer': 'resolution=merge-duplicates,return=representation'},
        json=row
    )
    if res.status_code not in (200, 201):
        sys.exit(f'ERROR creando fila quizzes: {res.status_code} {res.text[:300]}')
    quiz_id = res.json()[0]['id']
    print('quiz row id:', quiz_id)

    for wid in manifest.get('worksheet_ids', []):
        r = requests.patch(
            f'{SUPABASE_URL}/rest/v1/worksheets?id=eq.{wid}',
            headers={**HEADERS_AUTH, **profile_headers, 'Content-Type': 'application/json', 'Prefer': 'return=minimal'},
            json={'topic_key': manifest['topic_key']}
        )
        print(f'  worksheet {wid}: topic_key set ->', r.status_code)

    print('done')
