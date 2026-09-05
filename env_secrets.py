"""Loads Supabase/R2 credentials for local pipeline scripts from .env at the repo root.

.env is git-ignored — never hardcode these values directly in a script again.
If a value is missing this raises immediately with the variable name, so a
script fails loudly at import time instead of sending an empty Authorization
header.
"""
import os


def _load_dotenv():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.isfile(path):
        return
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, value = line.partition('=')
            os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


def _require(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f'Missing {name} — set it in .env at the repo root')
    return value


SUPABASE_URL = _require('SUPABASE_URL')
SERVICE_KEY = _require('SUPABASE_SERVICE_KEY')
R2_ACCOUNT_ID = _require('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = _require('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = _require('R2_SECRET_ACCESS_KEY')
R2_BUCKET = _require('R2_BUCKET')
R2_PUBLIC_BASE = _require('R2_PUBLIC_BASE')
