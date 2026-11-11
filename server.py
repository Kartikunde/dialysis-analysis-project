"""Live dashboard server. Python standard library only.
  GET /api/data  -> all records as JSON
  GET /stream    -> Server-Sent Events: a new patient record every INTERVAL seconds
Run: python server.py   then open http://localhost:8000
"""
import csv, json, os, queue, random, threading, time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import datagen

BASE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(BASE, "data", "patients.csv")
PORT = int(os.environ.get("PORT", 8000))
INTERVAL = float(os.environ.get("INTERVAL", 2))

if not os.path.exists(CSV):
    os.makedirs(os.path.dirname(CSV), exist_ok=True)
    datagen.write_csv(CSV)
rows, clients, lock = datagen.read_csv(CSV), [], threading.Lock()

def producer():
    rng = random.Random()
    while True:
        time.sleep(INTERVAL)
        with lock:
            rec = datagen.make(rng, len(rows) + 1, mo=11)
            rows.append(rec)
            with open(CSV, "a", newline="") as fh:
                csv.DictWriter(fh, datagen.FIELDS).writerow(rec)
            for q in list(clients):
                q.put(rec)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=os.path.join(BASE, "static"), **k)

    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path.startswith("/api/data"):
            with lock:
                body = json.dumps(rows).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path.startswith("/stream"):
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            q = queue.Queue()
            with lock:
                clients.append(q)
            try:
                while True:
                    try:
                        msg = "data: %s\n\n" % json.dumps(q.get(timeout=15))
                    except queue.Empty:
                        msg = ": ping\n\n"
                    self.wfile.write(msg.encode()); self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                with lock:
                    clients.remove(q)
        else:
            super().do_GET()

if __name__ == "__main__":
    threading.Thread(target=producer, daemon=True).start()
    print("Dashboard running at http://localhost:%d  (Ctrl+C to stop)" % PORT)
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()
