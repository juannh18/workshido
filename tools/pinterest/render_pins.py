"""Pinta las imágenes de los pines (1000x1500 JPG) y las sube a R2.

Lee tools/pinterest/pins.json (lo genera tools/gen_pinterest_csv.js), abre
tools/pinterest/pin_template.html en un solo Chrome headless (CDP) con los
datos de cada pin en el hash, captura la pantalla y sube el resultado a
files.workshido.com/pins/<key>.jpg (la "Media URL" de los CSV de Pinterest).

Uso:
  python tools/pinterest/render_pins.py --out <carpeta> [--from 0 --to 811] [--no-upload] [--force]
Sin --force, se salta los pines que ya están en R2 (se puede relanzar sin repetir).
"""
import argparse, base64, json, os, subprocess, sys, tempfile, time, urllib.parse, urllib.request
import websocket

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, REPO)
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
PORT = int(os.environ.get('CDP_PORT', 9341))
TEMPLATE = 'file:///' + os.path.join(HERE, 'pin_template.html').replace('\\', '/')


class CDP:
    def __init__(self):
        self.proc = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars',
                                      '--remote-allow-origins=*', '--allow-file-access-from-files',
                                      f'--remote-debugging-port={PORT}', f'--user-data-dir={tempfile.mkdtemp(prefix="pins_")}',
                                      'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            try:
                tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json'))
                ws = next(t['webSocketDebuggerUrl'] for t in tabs if t['type'] == 'page')
                break
            except Exception:
                time.sleep(0.2)
        self.ws = websocket.create_connection(ws, timeout=60)
        self.n = 0
        self.call('Emulation.setDeviceMetricsOverride', width=1000, height=1500, deviceScaleFactor=1, mobile=False)

    def call(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({'id': self.n, 'method': method, 'params': params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get('id') == self.n:
                if 'error' in m:
                    raise RuntimeError(m['error'])
                return m.get('result', {})

    def render(self, creative):
        self.call('Page.navigate', url='about:blank')
        self.call('Page.navigate', url=TEMPLATE + '#' + urllib.parse.quote(json.dumps(creative)))
        for _ in range(150):  # up to 15 s for fonts + preview image
            r = self.call('Runtime.evaluate', expression='window.__ready === true', returnByValue=True)
            if r.get('result', {}).get('value'):
                break
            time.sleep(0.1)
        else:
            raise RuntimeError('timeout')
        shot = self.call('Page.captureScreenshot', format='jpeg', quality=86,
                         clip={'x': 0, 'y': 0, 'width': 1000, 'height': 1500, 'scale': 1})
        return base64.b64decode(shot['data'])

    def close(self):
        try:
            self.ws.close()
        finally:
            self.proc.kill()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--from', dest='start', type=int, default=0)
    ap.add_argument('--to', dest='end', type=int, default=10**6)
    ap.add_argument('--no-upload', action='store_true')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    pins = json.load(open(os.path.join(HERE, 'pins.json'), encoding='utf-8'))[a.start:a.end]
    os.makedirs(a.out, exist_ok=True)

    s3 = None
    if not a.no_upload:
        import boto3
        from env_secrets import R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY
        s3 = boto3.client('s3', endpoint_url=f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com',
                          aws_access_key_id=R2_ACCESS_KEY_ID, aws_secret_access_key=R2_SECRET_ACCESS_KEY, region_name='auto')

    def exists(key):
        try:
            s3.head_object(Bucket='workshido-files', Key=key)
            return True
        except Exception:
            return False

    cdp = CDP()
    done = skipped = failed = 0
    try:
        for i, p in enumerate(pins):
            key = f"pins/{p['key']}.jpg"
            if s3 and not a.force and exists(key):
                skipped += 1
                continue
            try:
                jpg = cdp.render(p['creative'])
            except Exception as e:
                failed += 1
                print('FAIL', p['key'], e, flush=True)
                continue
            path = os.path.join(a.out, p['key'] + '.jpg')
            open(path, 'wb').write(jpg)
            if s3:
                s3.put_object(Bucket='workshido-files', Key=key, Body=jpg, ContentType='image/jpeg',
                              CacheControl='public, max-age=31536000, immutable')
            done += 1
            if done % 25 == 0:
                print(f'{done} listos ({a.start + i + 1}/{a.start + len(pins)})', flush=True)
    finally:
        cdp.close()
    print(f'listos {done}, ya estaban {skipped}, fallidos {failed}')


if __name__ == '__main__':
    main()
