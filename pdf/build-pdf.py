# Baut die Spendenbestätigung neu: Seite 1 aus seite1.html (Chrome-Druck), Seiten 2+3 unverändert aus original-3-seiten.pdf
# (dort liegt der ausfüllbare Rückmeldebogen). Aufruf: uv run -q --with websocket-client --with pypdf python3 -I build-pdf.py
import os, json, subprocess, time, urllib.request, base64, socket, tempfile, shutil, io
import websocket
from pypdf import PdfReader, PdfWriter

D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, 'Hopetize_Spendenbestaetigung_Weihnachtsaktion_2026.pdf')
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
prof = tempfile.mkdtemp(prefix="pdfprof-")
p = subprocess.Popen([CH, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", f"--remote-debugging-port={port}", f"--user-data-dir={prof}", "about:blank"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try: tabs = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json")); break
        except Exception: time.sleep(0.2)
    ws = websocket.create_connection([t for t in tabs if t["type"] == "page"][0]["webSocketDebuggerUrl"], timeout=60)
    n = [0]
    def cmd(m, **pa):
        n[0] += 1; ws.send(json.dumps({"id": n[0], "method": m, "params": pa}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n[0]: return r.get("result", r)
    cmd("Page.navigate", url="file://" + os.path.join(D, "seite1.html")); time.sleep(3)
    cmd("Runtime.evaluate", expression="document.fonts.ready.then(()=>1)", awaitPromise=True)
    pdf = base64.b64decode(cmd("Page.printToPDF", printBackground=True, preferCSSPageSize=True, marginTop=0, marginBottom=0, marginLeft=0, marginRight=0)["data"])
finally:
    p.kill(); shutil.rmtree(prof, ignore_errors=True)

p1 = PdfReader(io.BytesIO(pdf))
assert len(p1.pages) == 1, "Seite 1 läuft über: %d Seiten" % len(p1.pages)
w = PdfWriter(clone_from=os.path.join(D, "original-3-seiten.pdf"))  # behält Formularfelder (AcroForm) der Seite 3
w.insert_page(p1.pages[0], 0)
w.remove_page(1)  # alte Seite 1
w.add_metadata({"/Title": "Hopetize · Spendenbestätigung Weihnachtsaktion 2026", "/Author": "Hopetize Kinderkrebshilfe e. V."})
with open(OUT, "wb") as f: w.write(f)
r = PdfReader(OUT)
print(OUT, "Seiten", len(r.pages), "Felder", len(r.get_fields() or {}))
