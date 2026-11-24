#!/usr/bin/env python3
"""Upload the comic videos to the Prof H Lab YouTube channel and finish them (11-language titles, descriptions, tags,
subtitles, thumbnail), or just check the channel.

  python3 scripts/youtube_upload.py --check                         # channel name, phone verification (longUploadsStatus), quota test
  python3 scripts/youtube_upload.py shorts/ep1-youtube.json [--private | --at 2026-11-26T09:00:00-05:00]
  (default: public; the video ID is saved in shorts/uploads.json and the run skips a video already uploaded)

Credentials, environment variables only, never in the repo or the chat:
  YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET  the OAuth client of a Google Cloud project whose uploads are not locked to private
                                            (YouTube locks videos.insert from projects that have not passed its API audit;
                                            the owner's other channels already upload publicly with such a client)
  YOUTUBE_REFRESH_TOKEN                     minted for the channel owner's Google account (choose the Prof H Lab channel) with the scopes
                                            youtube.upload and youtube.force-ssl
Falls back to BLOGGER_CLIENT_ID/SECRET when the YOUTUBE_ client is not set.
"""
import json, os, pathlib, sys, urllib.request, urllib.parse, urllib.error
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://www.googleapis.com/youtube/v3"
CATEGORY = {"Howto & Style": "26", "Education": "27", "Entertainment": "24"}

def token():
    cid = os.environ.get("YOUTUBE_CLIENT_ID") or os.environ.get("BLOGGER_CLIENT_ID")
    sec = os.environ.get("YOUTUBE_CLIENT_SECRET") or os.environ.get("BLOGGER_CLIENT_SECRET")
    rt = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    if not (cid and sec and rt): sys.exit("missing YOUTUBE_REFRESH_TOKEN (and YOUTUBE_CLIENT_ID/SECRET): see this script's docstring")
    d = urllib.parse.urlencode({"client_id": cid, "client_secret": sec, "refresh_token": rt, "grant_type": "refresh_token"}).encode()
    try: t = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", d))
    except urllib.error.HTTPError as e: sys.exit(f"token refresh failed: HTTP {e.code} {e.read().decode()[:200]}")
    if "youtube" not in t.get("scope", ""): sys.exit("the refresh token has no YouTube scope")
    return t["access_token"]

def call(tok, method, url, body=None, ctype="application/json", raw=False):
    req = urllib.request.Request(url, data=body, method=method, headers={"Authorization": f"Bearer {tok}", "Content-Type": ctype})
    try:
        r = urllib.request.urlopen(req, timeout=600)
        return r if raw else json.load(r)
    except urllib.error.HTTPError as e: sys.exit(f"{method} {url.split('?')[0]}: HTTP {e.code} {e.read().decode()[:400]}")

def check():
    tok = token()
    ch = call(tok, "GET", f"{API}/channels?part=snippet,status,brandingSettings&mine=true")["items"]
    for c in ch:
        st = c["status"]
        print(f"channel: {c['snippet']['title']} ({c['id']})")
        print(f"  phone verification / long uploads: {st.get('longUploadsStatus')}  (allowed = verified; eligible = not verified yet)")
        print(f"  made for kids default: {st.get('madeForKids')}, privacy: {st.get('privacyStatus')}")

def upload(meta_path, privacy="public", publish_at=None):
    meta_path = ROOT / meta_path; m = json.loads(meta_path.read_text(encoding="utf-8")); sid = meta_path.name.split("-youtube")[0]
    log_f = ROOT / "shorts" / "uploads.json"; log = json.loads(log_f.read_text(encoding="utf-8")) if log_f.exists() else {}
    tok = token()
    if sid in log: print(f"{sid}: already uploaded as {log[sid]}"); vid = log[sid]
    else:
        en = m["metadata"]["en"]
        tags, n = [], 0
        for lang in ["en"] + [l for l in m["metadata"] if l != "en"]:
            for tg in m["metadata"][lang].get("tags", [])[: (15 if lang == "en" else 3)]:
                if tg not in tags and n + len(tg) + 3 <= 480: tags.append(tg); n += len(tg) + 3
        status = {"privacyStatus": "private" if publish_at else privacy, "selfDeclaredMadeForKids": False, "containsSyntheticMedia": False}
        if publish_at: status["publishAt"] = publish_at
        body = {"snippet": {"title": en["title"][:100], "description": en["description"][:5000], "tags": tags, "categoryId": CATEGORY.get(m.get("category"), "26"),
                            "defaultLanguage": "en", "defaultAudioLanguage": "en"},
                "status": status,
                "localizations": {l: {"title": x["title"][:100], "description": x["description"][:5000]} for l, x in m["metadata"].items() if l != "en"}}
        video = meta_path.parent / m["video"]
        r = call(tok, "POST", "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status,localizations",
                 json.dumps(body).encode(), "application/json; charset=UTF-8", raw=True)
        loc = r.headers["Location"]
        req = urllib.request.Request(loc, data=video.read_bytes(), method="PUT", headers={"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"})
        try: v = json.load(urllib.request.urlopen(req, timeout=3600))
        except urllib.error.HTTPError as e: sys.exit(f"upload failed: HTTP {e.code} {e.read().decode()[:400]}")
        vid = v["id"]; log[sid] = vid; log_f.write_text(json.dumps(log, indent=1) + "\n", encoding="utf-8")
        print(f"{sid}: uploaded https://youtu.be/{vid} ({v['status'].get('uploadStatus')}, {v['status'].get('privacyStatus')})")
        if v["status"].get("privacyStatus") == "private" and privacy == "public" and not publish_at:
            print("  NOTE: YouTube kept it private: this OAuth client's project has not passed the YouTube API audit")
    import youtube_localize
    youtube_localize.main(vid, str(meta_path))   # subtitles, tags, localized metadata (idempotent) and the thumbnail

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "--check": check()
    else: upload(a[0], "private" if "--private" in a else "public", a[a.index("--at") + 1] if "--at" in a else None)
