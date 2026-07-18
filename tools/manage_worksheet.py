"""Utilidades puntuales de mantenimiento sobre la tabla `worksheets` en Supabase.

Reutiliza las credenciales ya presentes en tools/upload_batch.py (no las duplica).

Uso:
  python tools/manage_worksheet.py find "<texto del titulo>"
  python tools/manage_worksheet.py delete <id>
  python tools/manage_worksheet.py update <id> --pdf <ruta_o_url> --thumb <ruta_o_url> --slug <slug> --level_folder <lf>
"""
import sys, os, io, json, argparse
from datetime import datetime
import requests
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from upload_batch import SUPABASE_URL, HEADERS_AUTH, resolve, upload_pdf, upload_thumb


def find(title_substr):
    res = requests.get(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers=HEADERS_AUTH,
        params={'title': f'ilike.*{title_substr}*', 'select': 'id,title,file_url,thumbnail_url,teacher_edition_url'},
        verify=False,
    )
    rows = res.json()
    for r in rows:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    if not rows:
        print('Sin resultados.')
    return rows


def storage_path_from_url(url):
    marker = '/storage/v1/object/public/worksheets/'
    if not url or marker not in url:
        return None
    return url.split(marker, 1)[1]


def delete_storage_object(path):
    if not path:
        return
    res = requests.delete(
        f'{SUPABASE_URL}/storage/v1/object/worksheets/{path}',
        headers=HEADERS_AUTH, verify=False,
    )
    print(f'  storage delete {path}: {res.status_code}')


def delete_record(record_id):
    res = requests.get(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers=HEADERS_AUTH,
        params={'id': f'eq.{record_id}', 'select': 'id,title,file_url,thumbnail_url,teacher_edition_url'},
        verify=False,
    )
    rows = res.json()
    if not rows:
        print('No existe ese id.')
        return
    row = rows[0]
    print(f"Borrando: {row['title']} ({record_id})")
    for key in ('file_url', 'thumbnail_url', 'teacher_edition_url'):
        delete_storage_object(storage_path_from_url(row.get(key)))
    res = requests.delete(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers=HEADERS_AUTH,
        params={'id': f'eq.{record_id}'},
        verify=False,
    )
    print(f'  DB delete: {res.status_code}')


def update_record(record_id, pdf=None, thumb=None, te_pdf=None, slug=None, level_folder='a1'):
    ts = int(datetime.now().timestamp() * 1000)
    patch = {}
    if pdf:
        url = upload_pdf(resolve(pdf), f'{level_folder}/{ts}-{slug}.pdf')
        if url:
            patch['file_url'] = url
            print('  OK: nuevo PDF subido')
    if thumb:
        url = upload_thumb(resolve(thumb), f'thumbnails/{ts}-{slug}.webp')
        if url:
            patch['thumbnail_url'] = url
            print('  OK: nuevo thumbnail subido')
    if te_pdf:
        url = upload_pdf(resolve(te_pdf), f'teacher-editions/{level_folder}/{ts}-te_{slug}.pdf')
        if url:
            patch['teacher_edition_url'] = url
            print('  OK: nueva Teacher Edition subida')
    if not patch:
        print('Nada que actualizar.')
        return
    res = requests.patch(
        f'{SUPABASE_URL}/rest/v1/worksheets',
        headers={**HEADERS_AUTH, 'Content-Type': 'application/json', 'Prefer': 'return=representation'},
        params={'id': f'eq.{record_id}'},
        json=patch, verify=False,
    )
    print(f'  DB update: {res.status_code} {res.text[:300]}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)

    p_find = sub.add_parser('find')
    p_find.add_argument('title_substr')

    p_del = sub.add_parser('delete')
    p_del.add_argument('record_id')

    p_upd = sub.add_parser('update')
    p_upd.add_argument('record_id')
    p_upd.add_argument('--pdf')
    p_upd.add_argument('--thumb')
    p_upd.add_argument('--te_pdf')
    p_upd.add_argument('--slug', required=True)
    p_upd.add_argument('--level_folder', default='a1')

    args = ap.parse_args()
    if args.cmd == 'find':
        find(args.title_substr)
    elif args.cmd == 'delete':
        delete_record(args.record_id)
    elif args.cmd == 'update':
        update_record(args.record_id, pdf=args.pdf, thumb=args.thumb, te_pdf=args.te_pdf, slug=args.slug, level_folder=args.level_folder)
