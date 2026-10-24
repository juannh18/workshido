"""Loads Supabase/R2 credentials for local pipeline scripts from .env at the repo root.

.env is git-ignored — never hardcode these values directly in a script again.
If a value is missing this raises immediately with the variable name, so a
script fails loudly at import time instead of sending an empty Authorization
header.
"""
import os
import ssl
import sys
import tempfile


def _use_windows_ca_bundle():
    """TLS verification that is safe with threads, for requests and boto3.

    Avast's Web/Mail Shield re-signs every HTTPS connection with its own root,
    which lives only in the Windows certificate store, so certifi alone can't
    verify anything. pip_system_certs (loaded from a .pth at startup) fixes that
    by injecting truststore, but truststore loses verification under concurrent
    connections: with 8 boto3 threads a self-signed certificate was accepted 38
    times out of 40 (23/10/2026). Instead: undo the injection and give requests
    and boto3 a regular CA bundle built from the Windows ROOT/CA stores plus
    certifi — plain OpenSSL verification, which is thread-safe.
    """
    if sys.platform != 'win32':
        return
    try:
        from pip._vendor import truststore
        truststore.extract_from_ssl()
    except Exception:
        pass
    # Modules imported before this one (requests, boto3 — upload_batch.py imports
    # them first) captured truststore's class as their own `SSLContext` name;
    # extract_from_ssl() only restores the ssl module, so point them back too.
    for name, mod in list(sys.modules.items()):
        if name.startswith(('pip._vendor', 'truststore')):
            continue
        current = getattr(mod, 'SSLContext', None)
        if isinstance(current, type) and 'truststore' in getattr(current, '__module__', ''):
            setattr(mod, 'SSLContext', ssl.SSLContext)
    server_auth = '1.3.6.1.5.5.7.3.1'
    pems = []
    for store in ('ROOT', 'CA'):
        for cert, encoding, trust in ssl.enum_certificates(store):
            if encoding == 'x509_asn' and (trust is True or server_auth in trust):
                pems.append(ssl.DER_cert_to_PEM_cert(cert))
    try:
        import certifi
        with open(certifi.where(), encoding='utf-8') as f:
            pems.append(f.read())
    except ImportError:
        pass
    path = os.path.join(tempfile.gettempdir(), 'workshido-ca-bundle.pem')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(pems))
    os.environ['REQUESTS_CA_BUNDLE'] = path
    os.environ['AWS_CA_BUNDLE'] = path


_use_windows_ca_bundle()


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


def supabase_creds(lang):
    """(url, service_key) of the Supabase project for a site: 'en' = Workshido,
    'es' = Spanishido (its own project since 23/09/2026, no longer the `es` schema)."""
    if lang == 'es':
        return _require('ES_SUPABASE_URL'), _require('ES_SUPABASE_SERVICE_KEY')
    return SUPABASE_URL, SERVICE_KEY
