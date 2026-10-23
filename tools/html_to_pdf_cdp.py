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
import subprocess, time, json, base64, os, shutil, tempfile, sys
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


# Ajuste de la pág. 1 de las Teacher Editions (son PREMIUM: un hueco les quita autoridad).
# Se mide en un viewport A4 (794 px de ancho, sin escala = lo mismo que imprime printToPDF):
#  1) si la pág. 1 se desborda, quita filas del final de la tabla .p1-ref (Quick Reference);
#  2) si sobra espacio, estira el padding de las filas que quedan hasta llenarla.
# Devuelve las medidas para el reporte; no hace nada en HTML sin .support-grid (quizzes, etc.).
FIT_JS = r"""
(() => {
  if (!document.querySelector('.support-grid')) return null;
  const PAGE = 11.69 * 96, SAFE = 6;
  const feet = document.querySelectorAll('.footer');
  const f1 = feet[0], fN = feet[feet.length - 1];
  const p2 = document.querySelector('.page2');
  const y = el => el.getBoundingClientRect().bottom + window.scrollY;
  const p1 = () => y(f1);                       // fondo del pie de la pág. 1 (incluye el padding superior)
  const rows = [...document.querySelectorAll('.p1-ref tbody tr')];
  let removed = 0;
  while (p1() > PAGE - SAFE && rows.length) { rows.pop().remove(); removed++; }
  if (!rows.length) { const b = document.querySelector('.p1-ref-block'); if (b) b.remove(); }
  let stretch = 0;
  if (rows.length) {
    const tds = rows.map(r => [...r.children]);
    const base = parseFloat(getComputedStyle(tds[0][0]).paddingTop);
    for (let add = 0.5; add <= 9; add += 0.5) {   // máx. +9 px arriba y abajo por fila
      tds.flat().forEach(td => { td.style.paddingTop = td.style.paddingBottom = (base + add) + 'px'; });
      if (p1() > PAGE - SAFE) { tds.flat().forEach(td => { td.style.paddingTop = td.style.paddingBottom = (base + add - 0.5) + 'px'; }); break; }
      stretch = add;
    }
  }
  const p2h = p2 ? y(fN) - p2.getBoundingClientRect().top - window.scrollY + 16 : 0;
  return {gap1: Math.round(PAGE - p1()), over1: p1() > PAGE, kept: rows.length, removed, stretch,
          gap2: p2 ? Math.round(PAGE - p2h) : null};
})()
"""
GAP_MAX = 0.06  # >6 % de página en blanco = advertencia


def _report(pdf_path, m):
    """Imprime el estado de la TE: páginas y hueco de cada página."""
    if not m:
        return
    try:
        import fitz
        pages = len(fitz.open(pdf_path))
    except Exception:
        pages = None
    page = 11.69 * 96
    msg = (f'   pág.1 hueco {m["gap1"]}px ({100*m["gap1"]/page:.0f}%) · Quick Reference {m["kept"]} filas'
           f' (-{m["removed"]}, +{m["stretch"]}px) · pág.2 hueco {m["gap2"]}px')
    print(msg)
    if pages is not None and pages != 2:
        print(f'   ⚠⚠ LA TE TIENE {pages} PÁGINAS (deben ser 2)')
    if m['gap1'] > page * GAP_MAX:
        print('   ⚠⚠ PÁG. 1 CON HUECO: agregar filas a p1_reference (TE premium, no se sube así)')
    if m['gap2'] is not None and m['gap2'] > page * GAP_MAX:
        print('   ⚠ pág. 2 con hueco: agregar extension/key_language/exit_ticket')


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
        send('Emulation.setDeviceMetricsOverride', {'width': 794, 'height': 1123, 'deviceScaleFactor': 1, 'mobile': False})
        for html, pdf in pairs:
            url = 'file:///' + resolve_html(html).replace('\\', '/')
            send('Page.navigate', {'url': url})
            deadline = time.time() + 15
            while time.time() < deadline:
                msg = json.loads(ws.recv())
                if msg.get('method') == 'Page.loadEventFired':
                    break
            time.sleep(0.4)
            fit = send('Runtime.evaluate', {'expression': FIT_JS, 'returnByValue': True})
            fit = fit.get('result', {}).get('value')
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
            _report(out, fit)
        # Cierre ordenado: matar el proceso dejaba sus scoped_dir*/*.tmp en Temp
        # (4,3 GB acumulados al 15/10/2026).
        ws.send(json.dumps({'id': state['mid'] + 1, 'method': 'Browser.close'}))
        ws.close()
    finally:
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except Exception:
                proc.kill()
        # El perfil de Chrome pesa ~35 MB; sin esto cada conversión lo dejaba en Temp
        # (la calibración de quizzes hace decenas y llenó el disco el 11/10/2026).
        for _ in range(10):
            shutil.rmtree(user_dir, ignore_errors=True)
            if not os.path.exists(user_dir):
                break
            time.sleep(0.5)  # Windows suelta los archivos del perfil unos ms después de cerrar Chrome


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
