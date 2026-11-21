"""Shared helpers for the yadam scripts. No secrets live here.

Tokens: one JSON file per account in $YADAM_TOKDIR (km.json, gsb.json, drive.json), each holding a
"refresh_token" from the OAuth Playground consent. The OAuth client ID/secret are NOT needed here:
the cloud environment's network secret for oauth2.googleapis.com adds them (HTTP Basic) to every
token request. Never commit token files.
"""
import json, os, pathlib, sys, time, urllib.error, urllib.parse, urllib.request

TOKDIR = pathlib.Path(os.environ.get("YADAM_TOKDIR", os.path.expanduser("~/.yadam/tok")))
API = "https://www.googleapis.com/youtube/v3"
ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
CHANNELS = {"km": "UCNDIUDE7FVc29dLcxl_ueEQ", "gsb": "UCd6mIDo7MFVfzoJs3Tg6VUA"}


def token(name):
    """Return a fresh access token for km / gsb / drive, refreshing with the stored refresh token."""
    p = TOKDIR / f"{name}.json"
    if not p.exists():
        sys.exit(f"missing {p} - redo the OAuth Playground consent for '{name}'")
    t = json.loads(p.read_text())
    if t.get("access_token") and time.time() < t.get("obtained", 0) + t.get("expires_in", 0) - 120:
        return t["access_token"]
    body = urllib.parse.urlencode({"grant_type": "refresh_token", "refresh_token": t["refresh_token"]}).encode()
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=body)))
    except urllib.error.HTTPError as e:
        sys.exit(f"refresh failed for {name}: {e.code} {e.read()[:200]!r}")
    t.update(access_token=r["access_token"], expires_in=r["expires_in"], obtained=int(time.time()))
    p.write_text(json.dumps(t)); os.chmod(p, 0o600)
    return t["access_token"]


def call(method, url, tok, data=None, headers=None, raw=False, retries=5):
    """HTTP call with Bearer token. Returns (status, headers, body bytes). Retries rate limits briefly."""
    h = {"Authorization": f"Bearer {tok}"}
    h.update(headers or {})
    if data is not None and not raw:
        data = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method, headers=h), timeout=600) as r:
                return r.status, dict(r.headers), r.read()
        except urllib.error.HTTPError as e:
            b = e.read()
            if e.code == 403 and b"rateLimitExceeded" in b and i < retries - 1:
                time.sleep(5 * (i + 1)); continue
            return e.code, dict(e.headers), b


def get(path, tok, **params):
    """GET a YouTube Data API path ("videos", "channels", ...) and return parsed JSON or exit."""
    url = path if path.startswith("http") else f"{API}/{path}"
    st, _, b = call("GET", url + "?" + urllib.parse.urlencode(params), tok)
    if st != 200:
        sys.exit(f"GET {path} -> {st} {b[:300]!r}")
    return json.loads(b)


def chunks(xs, n=50):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]
