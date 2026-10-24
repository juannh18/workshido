# -*- coding: utf-8 -*-
"""Copia los PDFs de pago (Teacher Editions, quizzes y sus claves) del bucket público
workshido-files al bucket privado workshido-premium, con la misma key y el mismo ContentType.

Uso:
  python tools/copy_premium_to_private.py              # copia (salta los que ya están iguales) y verifica
  python tools/copy_premium_to_private.py --verify     # solo verifica
  python tools/copy_premium_to_private.py --delete-public
      # borra los 4 prefijos de workshido-files, pero SOLO si la verificación da 0 faltantes
      # y cada objeto existe en workshido-premium con el mismo tamaño. Pide escribir BORRAR.

Prefijos: teacher-editions/, quizzes/, es/teacher-editions/, es/quizzes/
Verificación: cada teacher_edition_url (worksheets) y quiz_pdf_url / key_pdf_url (quizzes) de las
bases de Workshido y Spanishido debe existir en workshido-premium (head_object).
La URL guardada en Supabase no cambia (https://files.workshido.com/<key>): las funciones
get-teacher-edition-url / get-quiz-url sacan la key de ahí y firman contra el bucket privado.
"""
import os, sys
import pip_system_certs.wrapt_requests  # noqa: almacén de certificados de Windows
import requests
from botocore.exceptions import ClientError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from upload_batch import s3, R2_BUCKET, R2_PREMIUM_BUCKET, R2_PUBLIC_BASE
from env_secrets import supabase_creds

PREFIXES = ('teacher-editions/', 'quizzes/', 'es/teacher-editions/', 'es/quizzes/')


def list_objects(bucket, prefix):
    out = {}
    for page in s3.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=prefix):
        for o in page.get('Contents', []):
            out[o['Key']] = o['Size']
    return out


def head(bucket, key):
    try:
        return s3.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        if e.response['ResponseMetadata'].get('HTTPStatusCode') == 404:
            return None
        raise


def copy_all():
    copied = skipped = 0
    for prefix in PREFIXES:
        src = list_objects(R2_BUCKET, prefix)
        dst = list_objects(R2_PREMIUM_BUCKET, prefix)
        print(f'{prefix}: {len(src)} en {R2_BUCKET}, {len(dst)} ya en {R2_PREMIUM_BUCKET}')
        for key, size in src.items():
            if dst.get(key) == size:
                skipped += 1
                continue
            # CopyObject conserva ContentType y CacheControl del original (MetadataDirective=COPY).
            s3.copy_object(Bucket=R2_PREMIUM_BUCKET, Key=key,
                           CopySource={'Bucket': R2_BUCKET, 'Key': key},
                           MetadataDirective='COPY')
            copied += 1
            if copied % 100 == 0:
                print(f'  ... {copied} copiados')
    print(f'Copiados: {copied}  ya estaban: {skipped}')


def stored_urls(lang):
    url, key = supabase_creds(lang)
    h = {'apikey': key, 'Authorization': f'Bearer {key}'}
    def fetch_all(table, cols):
        rows, start = [], 0
        while True:
            r = requests.get(f'{url}/rest/v1/{table}', headers={**h, 'Range': f'{start}-{start + 999}'},
                             params={'select': cols})
            r.raise_for_status()
            batch = r.json()
            rows += batch
            if len(batch) < 1000:
                return rows
            start += 1000
    te = [w['teacher_edition_url'] for w in fetch_all('worksheets', 'teacher_edition_url') if w['teacher_edition_url']]
    qz = []
    for q in fetch_all('quizzes', 'quiz_pdf_url,key_pdf_url'):
        qz += [u for u in (q['quiz_pdf_url'], q['key_pdf_url']) if u]
    return te, qz


def verify():
    missing, not_r2 = [], []
    for lang, site in (('en', 'Workshido'), ('es', 'Spanishido')):
        te, qz = stored_urls(lang)
        site_missing = 0
        for u in te + qz:
            if not u.startswith(R2_PUBLIC_BASE + '/'):
                not_r2.append((site, u))
                continue
            key = u[len(R2_PUBLIC_BASE) + 1:]
            if head(R2_PREMIUM_BUCKET, key) is None:
                missing.append((site, u))
                site_missing += 1
        print(f'{site}: {len(te)} Teacher Editions + {len(qz)} PDFs de quiz/clave -> faltan {site_missing}')
    for site, u in not_r2:
        print(f'  NO ES R2 ({site}): {u}')
    for site, u in missing:
        print(f'  FALTA ({site}): {u}')
    print('VERIFICACION OK' if not missing and not not_r2 else 'VERIFICACION CON PROBLEMAS')
    return not missing and not not_r2


def delete_public():
    if not verify():
        sys.exit('No se borra nada: la verificación no está limpia.')
    to_delete = []
    for prefix in PREFIXES:
        src = list_objects(R2_BUCKET, prefix)
        dst = list_objects(R2_PREMIUM_BUCKET, prefix)
        bad = [k for k, size in src.items() if dst.get(k) != size]
        if bad:
            sys.exit(f'No se borra nada: {len(bad)} objetos de {prefix} no están iguales en el bucket privado (ej. {bad[0]}).')
        to_delete += list(src)
    print(f'Se van a borrar {len(to_delete)} objetos de {R2_BUCKET} (todos tienen copia idéntica en {R2_PREMIUM_BUCKET}).')
    if input('Escribe BORRAR para confirmar: ').strip() != 'BORRAR':
        sys.exit('Cancelado.')
    for i in range(0, len(to_delete), 1000):
        chunk = to_delete[i:i + 1000]
        s3.delete_objects(Bucket=R2_BUCKET, Delete={'Objects': [{'Key': k} for k in chunk], 'Quiet': True})
    print(f'Borrados {len(to_delete)} objetos de {R2_BUCKET}.')


if __name__ == '__main__':
    if '--delete-public' in sys.argv:
        delete_public()
    elif '--verify' in sys.argv:
        sys.exit(0 if verify() else 1)
    else:
        copy_all()
        sys.exit(0 if verify() else 1)
