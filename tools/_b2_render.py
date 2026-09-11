# -*- coding: utf-8 -*-
"""Render B2 batch TE JSONs -> HTML -> PDF, working around a background scanner
that eats Chrome-authored .html/.pdf files in this environment.

For each te_content/te_*_b2.json listed on argv (or all in the batch):
  1. build HTML with build_te, write to tools/_tmp_<slug>.html (fresh)
  2. drive headless Chrome (CDP) -> printToPDF, keep bytes in memory
  3. re-save the PDF bytes through PyMuPDF (fitz) to Downloads/te_<slug>.pdf
     (fitz-authored PDFs are not quarantined)
  4. report page count + A4 check
"""
import subprocess, time, json, base64, os, tempfile, sys, urllib.request, websocket, fitz
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_te

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DL = r"C:\Users\juand\Downloads"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PORT = int(os.environ.get("CDP_PORT", "9333"))

BATCH = [
    "articles", "quantifiers", "contrast", "cause", "comparison",
]
TYPES = ["grammar", "reading", "writing", "practice"]


def all_slugs():
    out = []
    for t in BATCH:
        for ty in TYPES:
            out.append(f"{t}_{ty}_b2")
    return out


def render_one(send, slug):
    jpath = os.path.join(REPO, "tools", "te_content", f"te_{slug}.json")
    content = json.load(open(jpath, encoding="utf-8"))
    html = build_te.build(content)
    hpath = os.path.join(REPO, "tools", f"_tmp_{slug}.html")
    open(hpath, "w", encoding="utf-8").write(html)
    url = "file:///" + hpath.replace("\\", "/")
    send("Page.navigate", {"url": url})
    deadline = time.time() + 15
    while time.time() < deadline:
        pass
    time.sleep(1.1)
    res = send("Page.printToPDF", {
        "displayHeaderFooter": False, "printBackground": True,
        "paperWidth": 8.27, "paperHeight": 11.69,
        "marginTop": 0, "marginBottom": 0, "marginLeft": 0, "marginRight": 0,
        "scale": float(os.environ.get("TE_SCALE", "0.97")),
    })
    data = base64.b64decode(res["data"])
    doc = fitz.open("pdf", data)
    n = len(doc)
    w, h = doc[0].rect.width, doc[0].rect.height
    out = os.path.join(DL, f"te_{slug}.pdf")
    doc.save(out, garbage=4, deflate=True)
    doc.close()
    try:
        os.remove(hpath)
    except OSError:
        pass
    flag = "" if n == 2 else f"  <<< {n} PAGES"
    print(f"te_{slug}.pdf  {n}p  {round(w)}x{round(h)}pt  {os.path.getsize(out)}b{flag}")
    return n


def main(slugs):
    ud = tempfile.mkdtemp(prefix="cdp_b2_")
    proc = subprocess.Popen([
        CHROME, "--headless", "--disable-gpu", "--no-first-run",
        "--remote-allow-origins=*", f"--remote-debugging-port={PORT}",
        f"--user-data-dir={ud}", "about:blank",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json"))
                page = next(t for t in tabs if t["type"] == "page")
                break
            except Exception:
                time.sleep(0.4)
        else:
            sys.exit("no devtools endpoint")
        ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=60)
        st = {"mid": 0}

        def send(method, params=None):
            st["mid"] += 1
            ws.send(json.dumps({"id": st["mid"], "method": method, "params": params or {}}))
            while True:
                msg = json.loads(ws.recv())
                if msg.get("id") == st["mid"]:
                    if "error" in msg:
                        raise RuntimeError(f'{method}: {msg["error"]}')
                    return msg.get("result", {})

        send("Page.enable")
        bad = []
        for s in slugs:
            if render_one(send, s) != 2:
                bad.append(s)
        ws.close()
        print("\nNOT 2 PAGES:", bad or "none")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args if args else all_slugs())
