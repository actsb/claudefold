#!/usr/bin/env python3
"""Upload a finished yadam video to YouTube through the YouTube Data API v3 (resumable upload), then set the
thumbnail. Needs an OAuth2 access token in the env var YOUTUBE_TOKEN with the scopes
  https://www.googleapis.com/auth/youtube.upload   (upload)
  https://www.googleapis.com/auth/youtube          (thumbnail, playlist)
Mint one without a Cloud project at https://developers.google.com/oauthplayground : tick both scopes under
"YouTube Data API v3" -> Authorize APIs (choose the Google account / brand channel that owns the target channel)
-> Exchange authorization code for tokens -> copy the Access token (valid ~1 hour).

Usage:
  YOUTUBE_TOKEN=ya29... python3 scripts/publish_youtube.py video/2026-09-yadam-manbok/yadam_manbok_1080p.mp4 \
      --meta video/2026-09-yadam-manbok/youtube-meta.md [--thumb video/2026-09-yadam-manbok/thumbnail.png] \
      [--privacy private|unlisted|public] [--title-index 1] [--check]
Title/description/tags are read from youtube-meta.md (the numbered title list, the 설명 block, the 태그 line).
Uploads default to private so the owner can review in YouTube Studio and switch to public.
"""
import argparse, json, os, pathlib, re, sys, time, urllib.request, urllib.error

API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3/videos"
CHUNK = 32 * 1024 * 1024


def req(method, url, token, data=None, headers=None, raw=False):
    h = {"Authorization": f"Bearer {token}"}
    if headers: h.update(headers)
    if data is not None and not raw:
        data = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(r, timeout=600) as resp:
            body = resp.read(); return resp.status, dict(resp.headers), body
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def parse_meta(path, title_index):
    t = pathlib.Path(path).read_text(encoding="utf-8")
    titles = re.findall(r"^\d+\.\s+(.+)$", t.split("## 설명")[0], re.M)
    title = titles[title_index - 1].strip()
    desc = t.split("## 설명", 1)[1].split("## 태그", 1)[0]
    desc = re.sub(r"\(챕터는.*?\)\n", "", desc, flags=re.S).strip()
    tags_line = t.split("## 태그", 1)[1].split("## 설정", 1)[0].strip().replace("\n", " ")
    tags = [x.strip() for x in tags_line.split(",") if x.strip()]
    # YouTube: tags total <= 500 chars, each <= 100
    out, n = [], 0
    for tg in tags:
        if n + len(tg) + 1 > 480: break
        out.append(tg); n += len(tg) + 1
    return title[:100], desc[:5000], out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("--meta", required=True); ap.add_argument("--thumb", default="")
    ap.add_argument("--privacy", default="private"); ap.add_argument("--title-index", type=int, default=1); ap.add_argument("--check", action="store_true")
    ap.add_argument("--category", default="24", help="24 = Entertainment"); ap.add_argument("--playlist", default="")
    a = ap.parse_args()
    token = os.environ.get("YOUTUBE_TOKEN")
    if not token: sys.exit("set YOUTUBE_TOKEN (see docstring)")
    st, _, body = req("GET", f"{API}/channels?part=snippet&mine=true", token)
    if st != 200: sys.exit(f"token check failed: {st} {body[:300]}")
    ch = json.loads(body)["items"][0]; print("channel:", ch["snippet"]["title"], ch["id"])
    title, desc, tags = parse_meta(a.meta, a.title_index)
    print("title:", title); print("tags:", len(tags)); print("privacy:", a.privacy)
    if a.check: return
    video = pathlib.Path(a.video); size = video.stat().st_size
    meta = {"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": a.category, "defaultLanguage": "ko", "defaultAudioLanguage": "ko"},
            "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": False}}
    st, hdr, body = req("POST", f"{UPLOAD}?uploadType=resumable&part=snippet,status", token, meta,
                        headers={"X-Upload-Content-Length": str(size), "X-Upload-Content-Type": "video/mp4"})
    if st != 200: sys.exit(f"could not start upload: {st} {body[:400]}")
    loc = {k.lower(): v for k, v in hdr.items()}["location"]
    sent = 0
    with open(video, "rb") as f:
        while sent < size:
            chunk = f.read(CHUNK); end = sent + len(chunk) - 1
            for attempt in range(5):
                st, hdr, body = req("PUT", loc, token, chunk, headers={"Content-Type": "video/mp4", "Content-Length": str(len(chunk)),
                                                                        "Content-Range": f"bytes {sent}-{end}/{size}"}, raw=True)
                if st in (200, 201, 308): break
                time.sleep(2 ** attempt)
            else:
                sys.exit(f"upload failed at byte {sent}: {st} {body[:300]}")
            sent = end + 1; print(f"  uploaded {sent/1e6:.0f}/{size/1e6:.0f} MB", flush=True)
    vid = json.loads(body)["id"]; print("video id:", vid, "->", f"https://youtu.be/{vid}")
    if a.thumb:
        with open(a.thumb, "rb") as f: img = f.read()
        st, _, body = req("POST", f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}", token, img,
                          headers={"Content-Type": "image/png", "Content-Length": str(len(img))}, raw=True)
        print("thumbnail:", "ok" if st == 200 else f"{st} {body[:200]}")
    if a.playlist:
        st, _, body = req("POST", f"{API}/playlistItems?part=snippet", token,
                          {"snippet": {"playlistId": a.playlist, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
        print("playlist:", "ok" if st == 200 else f"{st} {body[:200]}")


if __name__ == "__main__":
    main()
