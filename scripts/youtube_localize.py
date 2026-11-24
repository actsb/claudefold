#!/usr/bin/env python3
"""Add the 11-language titles, descriptions, tags, subtitle tracks and the custom thumbnail to a YouTube video the owner uploaded.

  python3 scripts/youtube_localize.py VIDEO_ID shorts/ep1-youtube.json [--check]

Credentials (environment secrets, never in the repo, never printed): BLOGGER_CLIENT_ID and BLOGGER_CLIENT_SECRET (the same
Google Cloud OAuth client as the Blogger publisher) and YOUTUBE_REFRESH_TOKEN, minted once by the channel owner at
https://developers.google.com/oauthplayground with "Use your own OAuth credentials" and the scope
https://www.googleapis.com/auth/youtube.force-ssl, after enabling "YouTube Data API v3" in that Cloud project.

Why the owner uploads the video by hand: YouTube locks every video uploaded through videos.insert by an API project that
has not passed YouTube's API audit to private. Updating an existing video's localizations and adding caption tracks is not
restricted, so the owner uploads in YouTube Studio (public, English title and description) and this script does the rest.
--check only reads the video and lists its current localizations and captions.
"""
import json, os, pathlib, sys, urllib.request, urllib.parse, urllib.error, uuid

API = "https://www.googleapis.com/youtube/v3"

def token():
    cid = os.environ.get("YOUTUBE_CLIENT_ID") or os.environ.get("BLOGGER_CLIENT_ID"); sec = os.environ.get("YOUTUBE_CLIENT_SECRET") or os.environ.get("BLOGGER_CLIENT_SECRET")
    if not (cid and sec and os.environ.get("YOUTUBE_REFRESH_TOKEN")): sys.exit("missing YOUTUBE_REFRESH_TOKEN (and YOUTUBE_CLIENT_ID/SECRET): see youtube_upload.py's docstring")
    d = urllib.parse.urlencode({"client_id": cid, "client_secret": sec,
                                "refresh_token": os.environ["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    t = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", d))
    if "youtube" not in t.get("scope", ""): sys.exit("the refresh token has no YouTube scope; mint it with youtube.force-ssl")
    return t["access_token"]

def call(tok, method, url, body=None, ctype="application/json"):
    req = urllib.request.Request(url, data=body, method=method, headers={"Authorization": f"Bearer {tok}", "Content-Type": ctype})
    try: return json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e: sys.exit(f"{method} {url.split('?')[0]}: HTTP {e.code} {e.read().decode()[:400]}")

def main(vid, meta_path, check=False):
    meta_path = pathlib.Path(meta_path); m = json.loads(meta_path.read_text(encoding="utf-8")); sid = meta_path.name.split("-youtube")[0]
    tok = token()
    v = call(tok, "GET", f"{API}/videos?part=snippet,localizations,status&id={vid}")["items"]
    if not v: sys.exit(f"video {vid} not found on this channel")
    v = v[0]; caps = call(tok, "GET", f"{API}/captions?part=snippet&videoId={vid}")["items"]
    have = {c["snippet"]["language"] for c in caps}
    print(f"{vid}: {v['snippet']['title']!r} ({v['status']['privacyStatus']}); localizations: {sorted(v.get('localizations', {}))}; captions: {sorted(have)}")
    if check: return
    sn = v["snippet"]; sn["defaultLanguage"] = "en"
    tags, n = [], 0      # YouTube keeps one tag list per video (max 500 characters): English first, then each language's top terms
    for lang in ["en"] + [l for l in m["metadata"] if l != "en"]:
        for tg in m["metadata"][lang].get("tags", [])[: (15 if lang == "en" else 3)]:
            if tg not in tags and n + len(tg) + 3 <= 480: tags.append(tg); n += len(tg) + 3
    sn["tags"] = tags; sn["title"] = m["metadata"]["en"]["title"]; sn["description"] = m["metadata"]["en"]["description"]
    loc = {lang: {"title": x["title"][:100], "description": x["description"][:5000]} for lang, x in m["metadata"].items() if lang != "en"}
    call(tok, "PUT", f"{API}/videos?part=snippet,localizations", json.dumps({"id": vid, "snippet": {k: sn[k] for k in ("title", "description", "categoryId", "tags", "defaultLanguage") if k in sn}, "localizations": loc}).encode())
    print(f"localized title and description: {', '.join(sorted(loc))}")
    for lang in m["languages"]:
        if lang in have: continue
        srt = meta_path.parent / f"{sid}.{lang}.srt"
        b = uuid.uuid4().hex
        body = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n" + json.dumps({"snippet": {"videoId": vid, "language": lang, "name": "", "isDraft": False}})
                + f"\r\n--{b}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + srt.read_bytes() + f"\r\n--{b}--\r\n".encode()
        call(tok, "POST", "https://www.googleapis.com/upload/youtube/v3/captions?uploadType=multipart&part=snippet", body, f"multipart/related; boundary={b}")
        print(f"captions: {lang} added")
    th = meta_path.parent / m.get("thumbnail", "")
    if m.get("thumbnail") and th.exists():   # custom thumbnails need a verified channel (phone verification in YouTube Studio)
        req = urllib.request.Request(f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}", data=th.read_bytes(), method="POST",
                                     headers={"Authorization": f"Bearer {tok}", "Content-Type": "image/jpeg"})
        try: urllib.request.urlopen(req, timeout=120); print("thumbnail set")
        except urllib.error.HTTPError as e: print(f"thumbnail not set: HTTP {e.code} {e.read().decode()[:200]}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    main(a[0], a[1], "--check" in a)
