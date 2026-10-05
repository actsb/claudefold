#!/usr/bin/env python3
"""Pin Verdict Picks posts to Pinterest through the API (v5), using the copy sheets pinterest/pins-*.md.

Where it runs: the GitHub Actions workflow .github/workflows/pinterest.yml. GitHub's runners reach
api.pinterest.com, and the workflow can store the rotating refresh token back as a repository secret.
(The Claude cloud environment's network policy blocks pinterest.com, so the daily Routine does not call it;
the Routine only completes the pin entry in the sheet, and its push triggers the workflow.)

Credentials come from the environment and are never printed or written into the repository:
  PINTEREST_APP_ID, PINTEREST_APP_SECRET  the developer app (developers.pinterest.com -> My apps)
  PINTEREST_REFRESH_TOKEN                 continuous refresh token: valid 60 days and ROTATED on every refresh
                                          (the one sent is spent), so every run must save the new one
  PINTEREST_TOKEN_OUT                     file the new refresh token is written to; the workflow stores it back
                                          as the PINTEREST_REFRESH_TOKEN secret. Required before any refresh.
  PINTEREST_ACCESS_TOKEN                  alternative: a 30-day token from My apps -> Generate access token
  PINTEREST_API                           API base, default https://api.pinterest.com/v5
                                          (https://api-sandbox.pinterest.com/v5 for sandbox testing)

Commands:
  check                                  who is connected, and the boards
  auth-url                               the one-time authorization link (tools/pinterest-connect.html builds the same)
  connect --code CODE                    exchange the one-time code for tokens; saves the refresh token to PINTEREST_TOKEN_OUT
  list                                   every pin the sheets describe, and whether it is ready
  sync [--limit N] [--board NAME]        pin the ready entries that are not on the board yet (matched by link), newest post first
  pin SLUG|URL [--board NAME]            one entry
  fix SLUG|URL [--replace] [--board NAME]
                                         bring an existing pin's title, description, alt text and link in line with the sheet.
                                         Pinterest's update endpoint is in beta and not open to every app, so with --replace
                                         the pin is deleted and created again when the update is refused.
Common flags: --dry-run (no writes), --no-online-check (skip the check that the post and image URLs answer 200).
"""
import argparse, base64, json, os, pathlib, re, secrets, sys, urllib.error, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = os.environ.get("PINTEREST_API", "https://api.pinterest.com/v5").rstrip("/")
PAGES = "https://actsb.github.io/claudefold/"
REDIRECT_URI = os.environ.get("PINTEREST_REDIRECT_URI", PAGES + "tools/pinterest-connect.html")
SCOPES = "boards:read,boards:write,pins:read,pins:write,user_accounts:read"
DEFAULT_BOARD = "Best of Amazon 2026"
BOARD_DESCRIPTIONS = {
    DEFAULT_BOARD: "Honest buying guides to the most-wanted products on Amazon US: the best pick first, real owner "
                   "reviews, what to check before you buy, and when the price is right. From Verdict Picks.",
}
IN_ACTIONS = os.environ.get("GITHUB_ACTIONS") == "true"
_token = None


def env(name):
    return os.environ.get(name, "").strip()


def die(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


def mask(value):
    """Hide a secret from GitHub Actions logs from this point on (a no-op anywhere else)."""
    if IN_ACTIONS and value:
        print(f"::add-mask::{value}", flush=True)


def summary(line):
    """Append a line to the workflow run's summary page when running in GitHub Actions."""
    path = env("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def reason(res):
    """The human part of an error payload, never the payload itself (it could echo credentials)."""
    if not isinstance(res, dict):
        return str(res)[:200]
    for key in ("message", "error_description", "error"):
        if res.get(key):
            return str(res[key])[:300]
    return "no message"


def http(method, url, body=None, headers=None, form=False, timeout=90):
    headers = dict(headers or {})
    data = None
    if body is not None:
        if form:
            data = urllib.parse.urlencode(body).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            data = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw)
        except ValueError:
            return e.code, {"message": raw.decode("utf-8", "replace")[:300]}
    except urllib.error.URLError as e:
        return 0, {"message": f"network error: {e.reason}"}


# ---------------------------------------------------------------- credentials

def token_request(fields):
    cid, secret = env("PINTEREST_APP_ID"), env("PINTEREST_APP_SECRET")
    if not (cid and secret):
        die("PINTEREST_APP_ID and PINTEREST_APP_SECRET are required (repository secrets; see daily/pinterest-setup.md)")
    basic = base64.b64encode(f"{cid}:{secret}".encode()).decode()
    st, res = http("POST", f"{API}/oauth/token", fields, {"Authorization": f"Basic {basic}"}, form=True)
    if st != 200 or not res.get("access_token"):
        die(f"Pinterest refused the token request (HTTP {st}): {reason(res)}")
    mask(res.get("access_token"))
    mask(res.get("refresh_token"))
    return res


def save_refresh_token(res):
    new = res.get("refresh_token")
    if not new:
        return
    out = pathlib.Path(env("PINTEREST_TOKEN_OUT"))
    out.write_text(new, encoding="utf-8")
    out.chmod(0o600)
    print("refresh token rotated; the new one is ready to be saved by the workflow")


def access_token():
    global _token
    if _token:
        return _token
    if env("PINTEREST_ACCESS_TOKEN"):
        _token = env("PINTEREST_ACCESS_TOKEN")
        mask(_token)
        return _token
    if not env("PINTEREST_REFRESH_TOKEN"):
        die("no Pinterest credentials: connect once (daily/pinterest-setup.md, step 5) or set PINTEREST_ACCESS_TOKEN")
    if not env("PINTEREST_TOKEN_OUT"):
        die("refusing to refresh without PINTEREST_TOKEN_OUT: Pinterest rotates the refresh token on every use, "
            "so the new one must be saved or the connection breaks")
    res = token_request({"grant_type": "refresh_token", "refresh_token": env("PINTEREST_REFRESH_TOKEN")})
    save_refresh_token(res)
    _token = res["access_token"]
    return _token


def api(method, path, body=None, params=None):
    url = f"{API}{path}" + ("?" + urllib.parse.urlencode(params) if params else "")
    return http(method, url, body, {"Authorization": f"Bearer {access_token()}"})


def paged(path, params=None):
    params = dict(params or {}, page_size=100)
    items = []
    while True:
        st, res = api("GET", path, params=params)
        if st != 200:
            die(f"GET {path} failed (HTTP {st}): {reason(res)}")
        items += res.get("items", [])
        if not res.get("bookmark"):
            return items
        params["bookmark"] = res["bookmark"]


# ---------------------------------------------------------------- the copy sheets

ENTRY = re.compile(r"^## (?:\d+ · )?(?P<name>.+?) — `(?P<image>posts/[^`]+?/images/pin\.png)`[ \t]*$", re.M)
FIELD = re.compile(r"^\*\*(Title|Description|Link|Alt text|Board)\*\*[ \t]*\n(.+?)(?=\n[ \t]*\n|\n\*\*|\Z)", re.M | re.S)
KEYS = {"Title": "title", "Description": "description", "Link": "link", "Alt text": "alt", "Board": "board"}


def load_entries():
    """Every pin entry in pinterest/pins-*.md, in sheet order."""
    entries = []
    for sheet in sorted((ROOT / "pinterest").glob("pins-*.md")):
        text = sheet.read_text(encoding="utf-8")
        heads = list(ENTRY.finditer(text))
        for i, m in enumerate(heads):
            block = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
            other = re.search(r"^## ", block, re.M)          # a non-entry section (e.g. "Suggested order") ends the block
            if other:
                block = block[: other.start()]
            fields = {KEYS[k]: " ".join(v.split()) for k, v in FIELD.findall(block)}
            image = m.group("image")
            entries.append({"name": m.group("name").strip(), "image": image, "dir": image.rsplit("/images/", 1)[0],
                            "sheet": sheet.name, **fields})
    return entries


def queue_by_dir():
    q = ROOT / "daily" / "queue.json"
    if not q.exists():
        return {}
    # the folder the entry recorded when it was scaffolded; the date-slug path only for entries that have none
    # (a post's folder month can differ from its date, e.g. posts/2026-09-noco-… dated 2026-10-03)
    return {e.get("dir") or f"posts/{e['date'][:7]}-{e['slug']}": e for e in json.loads(q.read_text(encoding="utf-8"))["queue"]}


def problems(e, queue):
    """Why an entry cannot be pinned yet (an empty list means it is ready)."""
    out = [f"no {k}" for k in ("title", "description", "link", "alt") if not e.get(k)]
    if any("WRITE" in str(e.get(k, "")) for k in ("title", "description", "link", "alt")):
        out.append("unfinished (WRITE marker)")
    if not (ROOT / e["image"]).exists():
        out.append("pin image missing")
    q = queue.get(e["dir"])
    if q and q.get("status") != "published":
        out.append(f"post not published yet (queue status {q.get('status')})")
    return out


def online(url):
    st, _ = http("GET", url, headers={"User-Agent": "VerdictPicks-pinner/1.0"}, timeout=30)
    return st == 200


def norm(link):
    p = urllib.parse.urlsplit((link or "").strip())
    return f"{p.netloc.lower()}{p.path.rstrip('/')}"


def clip(text, n):
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def find_entry(target, entries):
    t = target.strip()
    for e in entries:
        if t in (e["dir"], e["dir"].split("/", 1)[-1], e.get("link")) or (t.startswith("http") and norm(t) == norm(e.get("link"))):
            return e
    matches = [e for e in entries if t.lower() in e["dir"].lower()]
    if len(matches) == 1:
        return matches[0]
    die(f"no single sheet entry matches {target!r}" + (f" (candidates: {', '.join(m['dir'] for m in matches)})" if matches else ""))


# ---------------------------------------------------------------- boards and pins

def board_id(name, dry):
    for b in paged("/boards"):
        if b.get("name", "").strip().lower() == name.strip().lower():
            return b["id"]
    if dry:
        print(f"would create board {name!r}")
        return None
    st, res = api("POST", "/boards", {"name": name, "description": BOARD_DESCRIPTIONS.get(name, ""), "privacy": "PUBLIC"})
    if st not in (200, 201):
        die(f"could not create board {name!r} (HTTP {st}): {reason(res)}")
    print(f"created board {name!r}")
    return res["id"]


def pins_by_link(bid):
    found = {}
    if bid:
        for p in paged(f"/boards/{bid}/pins"):
            found.setdefault(norm(p.get("link")), []).append(p)
    return found


def fields(e):
    return {"title": clip(e["title"], 100), "description": clip(e["description"], 500),
            "link": e["link"], "alt_text": clip(e["alt"], 500)}


def create_pin(e, bid):
    body = dict(fields(e), board_id=bid, media_source={"source_type": "image_url", "url": PAGES + e["image"]})
    st, res = api("POST", "/pins", body)
    if st == 400:
        print(f"  Pinterest could not use the image URL ({reason(res)}); uploading the file instead")
        body["media_source"] = {"source_type": "image_base64", "content_type": "image/png",
                                "data": base64.b64encode((ROOT / e["image"]).read_bytes()).decode()}
        st, res = api("POST", "/pins", body)
    if st not in (200, 201):
        return None, f"HTTP {st}: {reason(res)}"
    return res.get("id"), None


def announce(e, pin_id):
    url = f"https://www.pinterest.com/pin/{pin_id}/"
    print(f"  pinned: {e['name']} -> {url}")
    summary(f"- Pinned **{e['name']}** → {url}")


# ---------------------------------------------------------------- commands

def cmd_check(_):
    st, me = api("GET", "/user_account")
    if st != 200:
        die(f"GET /user_account failed (HTTP {st}): {reason(me)}")
    print(f"connected as @{me.get('username')} ({me.get('account_type', 'account type unknown')}) via {API}")
    for b in paged("/boards"):
        print(f"  board: {b.get('name')} ({b.get('privacy', '?').lower()}, {b.get('pin_count', '?')} pins)")
    summary(f"Connected as **@{me.get('username')}** ({me.get('account_type', '?')}).")


def cmd_auth_url(_):
    cid = env("PINTEREST_APP_ID") or die("PINTEREST_APP_ID is required")
    print("https://www.pinterest.com/oauth/?" + urllib.parse.urlencode(
        {"client_id": cid, "redirect_uri": REDIRECT_URI, "response_type": "code", "scope": SCOPES, "state": secrets.token_urlsafe(12)}))


def cmd_connect(a):
    code = (a.code or "").strip()
    if not code:
        die("the one-time code is required (from tools/pinterest-connect.html)")
    mask(code)
    if not env("PINTEREST_TOKEN_OUT"):
        die("PINTEREST_TOKEN_OUT is required so the refresh token can be saved")
    res = token_request({"grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI})
    save_refresh_token(res)
    global _token
    _token = res["access_token"]
    cmd_check(a)
    print("connected: the workflow now saves the refresh token as the PINTEREST_REFRESH_TOKEN secret")


def cmd_list(_):
    queue = queue_by_dir()
    for e in load_entries():
        issues = problems(e, queue)
        print(f"{'ready  ' if not issues else 'waiting'}  {e['dir']}  {e.get('link', '(no link)')}" + (f"  [{'; '.join(issues)}]" if issues else ""))


def ordered_ready(a):
    queue = queue_by_dir()
    entries = [e for e in load_entries() if not problems(e, queue)]
    daily = sorted((e for e in entries if e["dir"] in queue), key=lambda e: queue[e["dir"]]["date"], reverse=True)
    return daily + [e for e in entries if e["dir"] not in queue]


def pin_one(e, board_name, dry, check_online, existing_cache):
    name = e.get("board") or board_name
    if name not in existing_cache:
        bid = board_id(name, dry)
        existing_cache[name] = (bid, pins_by_link(bid))
    bid, existing = existing_cache[name]
    if norm(e["link"]) in existing:
        print(f"  already on {name!r}: {e['name']}")
        return "skipped"
    if check_online and not (online(e["link"]) and online(PAGES + e["image"])):
        print(f"  not online yet (post or image does not answer 200), will retry next run: {e['name']}")
        return "waiting"
    if dry:
        print(f"  would pin to {name!r}: {e['name']} | {fields(e)['title']}")
        return "dry"
    pin_id, err = create_pin(e, bid)
    if err:
        print(f"  FAILED {e['name']}: {err}")
        summary(f"- Failed **{e['name']}**: {err}")
        return "failed"
    existing.setdefault(norm(e["link"]), []).append({"id": pin_id, "link": e["link"]})
    announce(e, pin_id)
    return "created"


def cmd_sync(a):
    cache, created, failed = {}, 0, 0
    for e in ordered_ready(a):
        if created >= a.limit:
            print(f"limit of {a.limit} new pins reached; the rest wait for the next run")
            break
        r = pin_one(e, a.board, a.dry_run, not a.no_online_check, cache)
        created += r in ("created", "dry")
        failed += r == "failed"
    print(f"done: {created} {'would be ' if a.dry_run else ''}created, {failed} failed")
    if failed:
        sys.exit(1)


def cmd_pin(a):
    e = find_entry(a.target, load_entries())
    issues = problems(e, queue_by_dir())
    if issues:
        die(f"{e['dir']} is not ready: {'; '.join(issues)}")
    if pin_one(e, a.board, a.dry_run, not a.no_online_check, {}) == "failed":
        sys.exit(1)


def cmd_fix(a):
    e = find_entry(a.target, load_entries())
    issues = problems(e, queue_by_dir())
    if issues:
        die(f"{e['dir']} is not ready: {'; '.join(issues)}")
    name = e.get("board") or a.board
    bid = board_id(name, a.dry_run)
    pins = pins_by_link(bid).get(norm(e["link"]), [])
    want = fields(e)
    if not pins:
        print(f"no pin for this link on {name!r}; creating one")
        return cmd_pin(a)
    if a.dry_run:
        print(f"would update {len(pins)} pin(s) on {name!r} to: {want['title']}")
        return
    refused = []
    for p in pins:
        st, res = api("PATCH", f"/pins/{p['id']}", want)
        if st == 200:
            print(f"  updated pin {p['id']}")
            summary(f"- Updated pin {p['id']} for **{e['name']}**")
        else:
            refused.append(p)
            print(f"  Pinterest refused the update of pin {p['id']} (HTTP {st}: {reason(res)})")
    if not refused:
        return
    if not a.replace:
        die("the update endpoint is not open to this app; run again with --replace to delete and recreate the pin")
    for p in refused:
        st, res = api("DELETE", f"/pins/{p['id']}")
        if st not in (200, 204):
            die(f"could not delete pin {p['id']} (HTTP {st}): {reason(res)}")
        print(f"  deleted pin {p['id']}")
    pin_id, err = create_pin(e, bid)
    if err:
        die(f"deleted the old pin but could not create the new one: {err}")
    announce(e, pin_id)


def main():
    ap = argparse.ArgumentParser(description="Pin Verdict Picks posts to Pinterest (API v5).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--board", default=DEFAULT_BOARD)
    common.add_argument("--dry-run", action="store_true")
    common.add_argument("--no-online-check", action="store_true")
    sub.add_parser("check")
    sub.add_parser("auth-url")
    c = sub.add_parser("connect"); c.add_argument("--code", required=True)
    sub.add_parser("list")
    s = sub.add_parser("sync", parents=[common]); s.add_argument("--limit", type=int, default=2)
    p = sub.add_parser("pin", parents=[common]); p.add_argument("target")
    f = sub.add_parser("fix", parents=[common]); f.add_argument("target"); f.add_argument("--replace", action="store_true")
    a = ap.parse_args()
    {"check": cmd_check, "auth-url": cmd_auth_url, "connect": cmd_connect, "list": cmd_list,
     "sync": cmd_sync, "pin": cmd_pin, "fix": cmd_fix}[a.cmd](a)


if __name__ == "__main__":
    main()
