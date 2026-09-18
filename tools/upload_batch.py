"""Sube un lote de worksheets a R2 (archivos) + Supabase (metadata) desde un manifiesto JSON.

Uso:
  python tools/upload_batch.py manifest.json

Formato del manifiesto (rutas relativas: PDFs/PNGs contra Downloads):
{
  "worksheets": [
    {
      "slug": "pluralnounspracticea1",
      "pdf": "pluralnounspracticea1.pdf",
      "thumb": "Pluralnounspracticeworksheeta1.png",
      "te_pdf": "te_pluralnouns_practice_a1.pdf",     // opcional (null = sin TE)
      "te_html": "te_pluralnouns_practice_a1.html",   // solo lo usa html_to_pdf_cdp.py
      "title": "Plural Nouns – Practice Worksheet",
      "level": "A1",
      "category": "Grammar",                           // destreza (lo que ve el usuario)
      "piece_type": "practice",                        // pieza del set (gating + armado de sets)
      "is_free": true,                                 // solo lo lee language=es; en 'en' siempre True
      "tags": "worksheet, plural nouns, ...",          // 'worksheet' SIEMPRE primero
      "description": "..."
    }
  ]
}

Opcional en la raíz del manifiesto: "language": "en" (default) o "es". Con "es"
las filas se insertan en el esquema `es.worksheets` (Spanishido) vía el header
PostgREST `Content-Profile: es`, y los archivos van bajo el prefijo `es/` en R2
(mismo bucket workshido-files / files.workshido.com). Workshido = `en` = `public`.

`piece_type` es la PIEZA del set (grammar/reading/writing/practice/listening/
vocabulary/speaking), y es cosa distinta de `category`, que es la destreza. Hasta
el 13/09 la pieza vivia solo en el sufijo del titulo ("Tema - Practice"), asi que
filtrar por tipo obligaba a hacer ilike '%practice%' y eso agarra falsos positivos
("Earthquake Safety - Reading & Practice" es una pieza de reading). Obligatorio en
'es'; opcional en 'en' hasta que se backfilleen las 739 filas viejas.

Reglas fijas: tag 'worksheet' primero (se valida). is_free: en 'en' SIEMPRE True
(regla del negocio: la worksheet es el imán, se cobra la TE y el Quiz). En 'es' el
manifiesto puede ponerlo en false por pieza — pensado para listening premium.
Ojo antes de cerrar una pieza: en Workshido las de practice son el 22% del
catalogo pero el 33% de las 30 mas descargadas.
Después de subir, correr tools/verify_uploads.py N para confirmar desde las URLs
públicas (con --es para worksheets en español).

Requiere: pip install boto3
Nota: R2_PUBLIC_BASE asume que files.workshido.com ya está apuntando al bucket R2
(Fase 3 de la migración). Si el dominio custom todavía no está activo, las URLs
que este script genera no van a cargar hasta que se complete ese paso.
"""
import pip_system_certs.wrapt_requests  # noqa: usa el almacén de certificados de Windows en vez de desactivar la verificación TLS
import requests, boto3, os, uuid, io, json, sys, re, unicodedata
from datetime import datetime
from botocore.config import Config
from PIL import Image

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from env_secrets import SUPABASE_URL, SERVICE_KEY, R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY

HEADERS_AUTH = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
}

# Set from the manifest's "language" in main(). 'es' -> Spanishido: insert into
# the `es` schema and store files under the `es/` prefix in R2.
PROFILE_HEADERS = {}   # {'Content-Profile': 'es'} for Spanish
KEY_PREFIX = ''        # 'es/' for Spanish

# Debe coincidir con el CHECK de la columna piece_type en es.worksheets y
# public.worksheets (migracion add_piece_type_to_worksheets, 13/09).
PIECE_TYPES = {'grammar', 'reading', 'writing', 'practice',
               'listening', 'vocabulary', 'speaking'}

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

DL = r'C:\Users\juand\Downloads'

def resolve(p):
    return p if os.path.isabs(p) else os.path.join(DL, p)

def check_r2_domain():
    """Aborta si files.workshido.com todavía no resuelve (dominio custom de R2, Fase 3
    de la migración) — evita subir worksheets nuevas con links rotos."""
    try:
        requests.head(R2_PUBLIC_BASE, timeout=5)
    except requests.RequestException:
        sys.exit(
            f'ERROR: {R2_PUBLIC_BASE} no responde todavia.\n'
            'El dominio custom de R2 (files.workshido.com) todavia no esta activo.\n'
            'No subas worksheets nuevas hasta completar ese paso, o quedaran con links rotos.'
        )

def upload_pdf(local_path, storage_path):
    try:
        s3.upload_file(local_path, R2_BUCKET, storage_path, ExtraArgs={
            'ContentType': 'application/pdf',
            'CacheControl': 'public, max-age=31536000, immutable',
        })
    except Exception as e:
        print(f'  ERROR PDF upload: {e}')
        return None
    return f'{R2_PUBLIC_BASE}/{storage_path}'

THUMB_MAX_WIDTH = 640  # big preview (top of the worksheet page) — shown at
                        # ~700px, so 640 without shipping full A4 resolution.
THUMB_SM_WIDTH = 440   # catalog/home/related CARDS render at ~150-280px; the
THUMB_SM_Q = 74        # JS points cards at this "<key>_sm.webp" derivative.

def _put_webp(img, key, quality):
    buf = io.BytesIO()
    img.save(buf, 'WEBP', quality=quality, method=6)
    s3.put_object(Bucket=R2_BUCKET, Key=key, Body=buf.getvalue(),
                  ContentType='image/webp', CacheControl='public, max-age=31536000, immutable')

def upload_thumb(local_path, storage_path):
    img = Image.open(local_path).convert('RGB')
    if img.width > THUMB_MAX_WIDTH:
        img = img.resize((THUMB_MAX_WIDTH, round(img.height * THUMB_MAX_WIDTH / img.width)), Image.LANCZOS)
    try:
        _put_webp(img, storage_path, 88)
        # Small card variant at "<name>_sm.webp" — see tools/make_thumb_sm.py
        # (the one-off backfill) and smThumb() in the card-rendering JS.
        sm = img if img.width <= THUMB_SM_WIDTH else img.resize(
            (THUMB_SM_WIDTH, round(img.height * THUMB_SM_WIDTH / img.width)), Image.LANCZOS)
        _put_webp(sm, storage_path[:-5] + '_sm.webp', THUMB_SM_Q)
    except Exception as e:
        print(f'  ERROR thumb upload: {e}')
        return None
    return f'{R2_PUBLIC_BASE}/{storage_path}'

def make_slug(title, level=None):
    """Slug para la URL publica /worksheet/<slug>/.

    Debe ser identico al backfill del 13/09 (NFKD -> ascii, minusculas, todo
    lo que no sea [a-z0-9] pasa a guion). El slug es INMUTABLE una vez
    publicado: si despues cambia el titulo, NO se regenera, o la URL viva
    cambia y se rompe el 301 que sostiene el posicionamiento.

    Si el slug base ya existe en la BD se desempata con el nivel y luego con
    un contador, igual que el backfill. La columna tiene indice unico, asi
    que una colision no detectada aqui falla ruidosamente en el insert en vez
    de servir la ficha equivocada.
    """
    base = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode().lower()
    base = re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', base)).strip('-')
    if not base:
        sys.exit(f'ERROR: no se pudo derivar slug del titulo {title!r}')

    def taken(s):
        # PostgREST usa Accept-Profile para LEER y Content-Profile para ESCRIBIR.
        # Con solo Content-Profile este GET consultaria public.worksheets aunque
        # estemos subiendo a es.worksheets, y el desempate de slug miraria el
        # catalogo equivocado.
        read_profile = {'Accept-Profile': PROFILE_HEADERS['Content-Profile']} if PROFILE_HEADERS else {}
        r = requests.get(f'{SUPABASE_URL}/rest/v1/worksheets',
                         headers={**HEADERS_AUTH, **read_profile},
                         params={'select': 'id', 'slug': f'eq.{s}', 'limit': '1'})
        return bool(r.json())

    cand = base
    if taken(cand) and level:
        cand = f'{base}-{level.lower()}'
    n = 2
    while taken(cand):
        cand = f'{base}-{n}'
        n += 1
    return cand


def insert_worksheet(record):
    res = requests.post(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers={**HEADERS_AUTH, **PROFILE_HEADERS, 'Content-Type': 'application/json', 'Prefer': 'return=representation'},
        json=record
    )
    return res.status_code, res.text[:300]

def main(manifest_path):
    global PROFILE_HEADERS, KEY_PREFIX
    check_r2_domain()
    manifest = json.load(open(manifest_path, encoding='utf-8'))

    lang = manifest.get('language', 'en')
    assert lang in ('en', 'es'), f"language debe ser 'en' o 'es', no {lang!r}"
    if lang == 'es':
        PROFILE_HEADERS = {'Content-Profile': 'es'}
        KEY_PREFIX = 'es/'
        print('>> language=es -> esquema es.worksheets + prefijo es/ en R2')

    for ws in manifest['worksheets']:
        assert ws['tags'].startswith('worksheet'), f"{ws['slug']}: el tag 'worksheet' debe ir primero"
        pt = ws.get('piece_type')
        if lang == 'es':
            assert pt in PIECE_TYPES, (
                f"{ws['slug']}: piece_type es obligatorio en espanol y debe ser uno de "
                f"{sorted(PIECE_TYPES)} (recibido: {pt!r})")
        else:
            assert pt is None or pt in PIECE_TYPES, f"{ws['slug']}: piece_type invalido: {pt!r}"
        if lang == 'en':
            assert ws.get('is_free', True) is True, (
                f"{ws['slug']}: en ingles is_free es siempre True (la worksheet es el iman; "
                "se cobra la Teacher Edition y el Quiz)")

    level_folder_default = manifest.get('level_folder', 'a1')
    for ws in manifest['worksheets']:
        ts = int(datetime.now().timestamp() * 1000)
        lf = ws.get('level_folder', level_folder_default)
        print(f'\n{"="*60}')
        print(f'Uploading: {ws["title"]}')

        pdf_url = upload_pdf(resolve(ws['pdf']), f'{KEY_PREFIX}{lf}/{ts}-{ws["slug"]}.pdf')
        if not pdf_url:
            continue
        print('  OK: PDF uploaded')

        thumb_url = upload_thumb(resolve(ws['thumb']), f'{KEY_PREFIX}thumbnails/{ts}-{ws["slug"]}.webp')
        if not thumb_url:
            continue
        print('  OK: Thumbnail uploaded')

        te_url = None
        if ws.get('te_pdf'):
            te_url = upload_pdf(resolve(ws['te_pdf']), f'{KEY_PREFIX}teacher-editions/{lf}/{ts}-te_{ws["slug"]}.pdf')
            print('  OK: Teacher Edition uploaded' if te_url else '  WARNING: TE upload failed, continuing without it')

        record = {
            'id': str(uuid.uuid4()),
            'slug': make_slug(ws['title'], ws.get('level')),
            'title': ws['title'],
            'level': ws['level'],
            'category': ws['category'],
            'piece_type': ws.get('piece_type'),
            'topic_key': ws.get('topic_key'),
            'tags': ws['tags'],
            'description': ws['description'],
            'file_url': pdf_url,
            'thumbnail_url': thumb_url,
            'teacher_edition_url': te_url,
            # En ingles la regla es dura (ya validada arriba). En espanol el
            # manifiesto decide, con True por defecto.
            'is_free': True if lang == 'en' else bool(ws.get('is_free', True)),
            'downloads': 0,
        }
        status, text = insert_worksheet(record)
        if status in (200, 201):
            print('  OK: DB record inserted')
        else:
            print(f'  ERROR DB insert: {status} {text}')

    print(f'\n{"="*60}')
    print('Done!')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
