"""Convierte HTML a PDF con Chrome headless vía CDP (Page.printToPDF, sin header/footer).

Uso:
  python tools/html_to_pdf_cdp.py manifest.json           # convierte te_html -> te_pdf de todos
  python tools/html_to_pdf_cdp.py in.html out.pdf [...]   # pares explícitos

HTML relativos se resuelven contra la raíz del repo; PDFs relativos contra Downloads.
IMPORTANTE: Chrome exige --remote-allow-origins=* para aceptar el websocket (si no, 403).

Si corres esto en paralelo (varios procesos a la vez, ej. varios agentes generando
quizzes al mismo tiempo), cada invocación DEBE usar un puerto CDP distinto — de lo
contrario dos procesos comparten el mismo Chrome y sus PDFs pueden mezclarse entre
sí. Setea la variable de entorno CDP_PORT (ej. `CDP_PORT=9334 python tools/html_to_pdf_cdp.py ...`)
con un puerto distinto por invocación paralela; si no se define, usa 9333 por defecto.
"""
import subprocess, time, json, base64, os, tempfile, sys
import urllib.request
import websocket

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = r'C:\Users\juand\Downloads'
PORT = int(os.environ.get('CDP_PORT', 9333))


def resolve_html(p):
    return p if os.path.isabs(p) else os.path.join(REPO, p)


def resolve_pdf(p):
    return p if os.path.isabs(p) else os.path.join(DL, p)


def run(pairs):
    user_dir = tempfile.mkdtemp(prefix='chrome_cdp_')
    proc = subprocess.Popen([
        CHROME, '--headless=new', '--disable-gpu', '--no-first-run',
        '--remote-allow-origins=*',
        f'--remote-debugging-port={PORT}', f'--user-data-dir={user_dir}', 'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:
                tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json'))
                page = next(t for t in tabs if t['type'] == 'page')
                break
            except Exception:
                time.sleep(0.5)
        else:
            sys.exit('Chrome devtools endpoint never came up')

        ws = websocket.create_connection(page['webSocketDebuggerUrl'], timeout=60)
        state = {'mid': 0}

        def send(method, params=None):
            state['mid'] += 1
            ws.send(json.dumps({'id': state['mid'], 'method': method, 'params': params or {}}))
            while True:
                msg = json.loads(ws.recv())
                if msg.get('id') == state['mid']:
                    if 'error' in msg:
                        raise RuntimeError(f'{method}: {msg["error"]}')
                    return msg.get('result', {})

        send('Page.enable')
        for html, pdf in pairs:
            url = 'file:///' + resolve_html(html).replace('\\', '/')
            send('Page.navigate', {'url': url})
            deadline = time.time() + 15
            while time.time() < deadline:
                msg = json.loads(ws.recv())
                if msg.get('method') == 'Page.loadEventFired':
                    break
            time.sleep(0.4)
            res = send('Page.printToPDF', {
                'displayHeaderFooter': False,
                'printBackground': True,
                'paperWidth': 8.27, 'paperHeight': 11.69,  # A4
                'marginTop': 0, 'marginBottom': 0, 'marginLeft': 0, 'marginRight': 0,
            })
            out = resolve_pdf(pdf)
            with open(out, 'wb') as f:
                f.write(base64.b64decode(res['data']))
            print(pdf, os.path.getsize(out), 'bytes')
        ws.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 1 and args[0].endswith('.json'):
        manifest = json.load(open(args[0], encoding='utf-8'))
        pairs = [(w['te_html'], w['te_pdf']) for w in manifest['worksheets'] if w.get('te_html')]
    else:
        pairs = list(zip(args[::2], args[1::2]))
    if not pairs:
        sys.exit(__doc__)
    run(pairs)
    print('done')
