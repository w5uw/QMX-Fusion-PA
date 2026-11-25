"""QMX Fusion-PA local web server.

Serves the QMX Fusion-PA page at http://localhost:8737 so Chrome treats it as a
normal web address. That lets Chrome show every playback device (speakers,
virtual audio cables) and remember the audio and serial permissions.

Only this PC can reach it (it listens on 127.0.0.1). Close this window to stop.
"""
import http.server, os, re, socket, subprocess, sys, threading, time, urllib.request, webbrowser

PORT = 8737
HOST = "127.0.0.1"
HERE = os.path.dirname(os.path.abspath(__file__))
MARK = "QMX-Fusion-Local"

def versions():
    out = []
    for name in os.listdir(HERE):
        m = re.fullmatch(r"QMX-Fusion-Panadapter-v(\d+)\.(\d+)\.html", name)
        if m:
            out.append(((int(m.group(1)), int(m.group(2))), name))
    return [n for _, n in sorted(out)]

def newest():
    v = versions()
    return v[-1] if v else None

DEFAULT_FILE = "default-version.txt"

def pinned():
    """The version named in default-version.txt, if that file exists and names an app file in this folder."""
    try:
        with open(os.path.join(HERE, DEFAULT_FILE), encoding="utf-8-sig") as fh:
            for line in fh:
                name = line.strip()
                if name and not name.startswith("#"):
                    return name if name in versions() else None
    except OSError:
        pass
    return None

def default():
    """Pinned version if set, otherwise the newest version in the folder."""
    return pinned() or newest()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HERE, **k)
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Server", MARK)
        super().end_headers()
    def do_GET(self):
        if self.path in ("/", "/latest", "/index.html"):
            n = newest() if self.path == "/latest" else default()
            if not n:
                self.send_error(404, "No QMX-Fusion-Panadapter-vX.YY.html file in this folder")
                return
            self.send_response(302)
            self.send_header("Location", "/" + n)
            self.end_headers()
            return
        if self.path.startswith("/__ping"):
            self.send_response(200); self.end_headers()
            self.wfile.write((MARK + "|" + HERE).encode("utf-8")); return
        if self.path.startswith("/__quit"):
            self.send_response(200); self.end_headers(); self.wfile.write(b"bye")
            srv = self.server
            threading.Thread(target=lambda: (srv.shutdown(), srv.server_close()), daemon=True).start()
            STOP.set(); return
        return super().do_GET()
    def log_message(self, fmt, *args):
        pass

STOP = threading.Event()

def running_server():
    """None = no QMX Fusion-PA server. Otherwise the folder it serves
    ("" if it is an older server that doesn't report its folder)."""
    try:
        with urllib.request.urlopen(f"http://{HOST}:{PORT}/__ping", timeout=1) as r:
            txt = r.read().decode("utf-8", "replace")
    except Exception:
        return None
    if txt == MARK:
        return ""
    if txt.startswith(MARK + "|"):
        return txt.split("|", 1)[1]
    return None

def ask_old_to_quit():
    try:
        urllib.request.urlopen(f"http://{HOST}:{PORT}/__quit", timeout=2).read()
    except Exception:
        pass
    for _ in range(20):
        time.sleep(0.25)
        if not port_busy():
            return True
    return False

def port_busy():
    with socket.socket() as s:
        return s.connect_ex((HOST, PORT)) == 0

def open_chrome(url):
    cands = [os.path.join(os.environ.get(v, ""), r"Google\Chrome\Application\chrome.exe")
             for v in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")]
    for c in cands:
        if c and os.path.isfile(c):
            subprocess.Popen([c, "--new-window", url]); return "Chrome"
    webbrowser.open(url); return "your default browser"

def main():
    n = default()
    url = f"http://localhost:{PORT}/" + (n or "")
    print("QMX Fusion-PA local server (v3.31, with default-version pin)")
    print("==============================")
    if not n:
        print("No QMX-Fusion-Panadapter-vX.YY.html file found in", HERE)
        print("Put the app file in this folder and try again.")
        input("Press Enter to close..."); return
    other = running_server()
    if other is not None:
        same = other and os.path.normcase(os.path.abspath(other)) == os.path.normcase(HERE)
        if same:
            print("Already running from this folder. Opening", url)
            open_chrome(url); time.sleep(2); return
        print("Another QMX Fusion-PA server is already running" + (f" from:\n  {other}" if other else " (an older copy, from a different folder)."))
        print("Stopping it so this folder can be used...")
        if not ask_old_to_quit():
            print()
            print("The older server could not be stopped automatically.")
            print("Close its black 'QMX Fusion' or 'QMX Fusion-PA' local server window (from your old folder),")
            print("then double-click Start QMX Fusion.bat in this folder again.")
            input("Press Enter to close...")
            return
        print("Stopped.")
    if port_busy():
        print(f"Port {PORT} is used by another program. Close it, or change PORT in qmx_fusion_server.py.")
        input("Press Enter to close..."); return
    srv = http.server.ThreadingHTTPServer((HOST, PORT), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print("Serving folder:", HERE)
    if pinned():
        print("Default version:", n, "(pinned in " + DEFAULT_FILE + ")")
        if newest() != n:
            print("Newest in folder:", newest(), "- open it at", f"http://localhost:{PORT}/latest")
    else:
        print("Newest version:", n)
    print("Address:       ", url)
    print("Opened in      ", open_chrome(url))
    print()
    print("Leave this window open while you use QMX Fusion-PA.")
    print("Close it (or press Ctrl+C) to stop.")
    try:
        while not STOP.wait(1): pass
        print("Another QMX Fusion-PA folder took over. This window can be closed.")
        time.sleep(3)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            srv.shutdown(); srv.server_close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
