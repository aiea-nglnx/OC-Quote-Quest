#!/usr/bin/env python3
"""OC Quote Quest local server: serves the page and relays requests to public map services.

Why: some networks or browser extensions block CDNs (Leaflet), and some government map
servers don't allow requests straight from a web page (CORS). This server fetches those for
the page and caches the answers so public servers aren't asked twice.

Run:  python3 server.py      then open  http://localhost:8000
Python 3.8+ standard library only. No API keys.
"""
import hashlib, json, os, time, urllib.parse, urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", 8000))
ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, ".cache")
TTL = 24 * 3600  # cache answers for a day
# OFFLINE=1: answer only from the cache (rehearse once online, then demo with no Wi-Fi).
OFFLINE = os.environ.get("OFFLINE") == "1"
UA = "OCQuoteQuest-hackathon-prototype/1.0 (educational; local use)"

# Only these public hosts can be relayed (keeps this from being an open proxy).
ALLOWED = {
    "www.ocgis.com", "ocgis.com", "maps.scag.ca.gov", "hazards.fema.gov", "services.gis.ca.gov",
    "services1.arcgis.com", "services2.arcgis.com", "caltrans-gis.dot.ca.gov",
    "nominatim.openstreetmap.org", "gis.conservation.ca.gov", "fwspublicservices.wim.usgs.gov",
}
LEAFLET = {  # tried in order
    "leaflet.js": ["https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
                   "https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js",
                   "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"],
    "leaflet.css": ["https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
                    "https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css",
                    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css"],
}
os.makedirs(CACHE, exist_ok=True)


def fetch(url, timeout=25):
    path = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest())
    if os.path.exists(path) and (OFFLINE or time.time() - os.path.getmtime(path) < TTL):
        with open(path, "rb") as f:
            return f.read()
    if OFFLINE:
        raise RuntimeError("offline mode: not rehearsed (no cached answer)")
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = r.read()
    with open(path, "wb") as f:
        f.write(body)
    return body


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path in ("/", ""):
            self.path = "/oc-quote-quest.html"
            return super().do_GET()
        if u.path == "/proxy/health":
            return self.send(200, b'{"ok":true}', "application/json")
        if u.path.startswith("/vendor/"):
            name = u.path.rsplit("/", 1)[-1]
            for src in LEAFLET.get(name, []):
                try:
                    body = fetch(src)
                    return self.send(200, body, "text/css" if name.endswith(".css") else "application/javascript")
                except Exception:
                    continue
            return self.send(502, b"/* could not download Leaflet from any CDN */", "text/plain")
        if u.path == "/proxy":
            target = urllib.parse.parse_qs(u.query).get("url", [""])[0]
            host = urllib.parse.urlparse(target).hostname or ""
            if not target.startswith("https://") or host not in ALLOWED:
                return self.send(403, json.dumps({"error": {"message": "host not allowed: " + host}}).encode(), "application/json")
            try:
                return self.send(200, fetch(target), "application/json")
            except Exception as e:
                return self.send(502, json.dumps({"error": {"message": f"{host}: {e}"}}).encode(), "application/json")
        return super().do_GET()


if __name__ == "__main__":
    print(f"OC Quote Quest running at http://localhost:{PORT}  (Ctrl+C to stop)" + ("  [OFFLINE: cache only]" if OFFLINE else ""))
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()