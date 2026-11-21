#!/usr/bin/env python3
"""yt_up: upload a finished yadam video to YouTube (resumable upload), then set thumbnail, captions, playlist.
Tokens come from yadam/ytlib.py (refresh tokens in $YADAM_TOKDIR; the OAuth client secret is added by the
environment network secret). Uploads default to PRIVATE so the owner reviews in Studio. Titles starting
with "[OLD" are refused (house rule). Mind the 10,000 units/day quota per project.

Usage:
  python3 yadam/yt_up.py VIDEO.mp4 --meta youtube-meta-en.md [--channel km|gsb] [--thumb t.png]
      [--srt subs.srt --srt-lang en] [--privacy private|unlisted|public] [--publish-at 2026-11-25T10:00:00Z]
      [--playlist PL...] [--title-index 1] [--check] [--video-id ID]
Title/description/tags are read from the meta file (## Titles / ## Description / ## Tags, or the Korean
설명/태그 layout).
"""
import argparse, json, os, pathlib, re, sys, time, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(__file__))
from ytlib import token as get_token

API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3/videos"
CHUNK = 32 * 1024 * 1024


def req(method, url, token, data=None, headers=None, raw=False):
    """Retries when the shared API project hits a transient quota/rate limit (OAuth Playground tokens share one quota)."""
    for attempt in range(40):
        st, hd, body = _req(method, url, token, data, headers, raw)
        if st == 403 and (b"quotaExceeded" in body or b"rateLimitExceeded" in body):
            print(f"  quota busy, retry {attempt + 1}", flush=True); time.sleep(10 + attempt * 2); continue
        return st, hd, body
    return st, hd, body


def _req(method, url, token, data=None, headers=None, raw=False):
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


def parse_meta_en(t, title_index):
    """English meta (youtube-meta-en.md): ## Titles (numbered), ## Description (one ``` block), ## Tags, ## Settings."""
    sec = lambda name: t.split("## " + name, 1)[1].split("\n## ", 1)[0]
    titles = re.findall(r"^\d+\.\s+(.+)$", sec("Titles"), re.M)
    title = re.sub(r"\s*\*\*\(.*?\)\*\*\s*", "", titles[title_index - 1]).strip().strip("*").strip()
    d = sec("Description"); desc = d.split("```", 2)[1].strip("\n") if "```" in d else d.strip()
    tl = sec("Tags").strip(); tl = tl.split("```", 2)[1] if "```" in tl else tl.split("\n\n")[0]
    tags = [x.strip() for x in tl.replace("\n", " ").split(",") if x.strip()]
    out, n = [], 0
    for tg in tags:
        c = len(tg) + (2 if " " in tg else 0) + 1
        if n + c > 495: break
        out.append(tg); n += c
    return title[:100], desc[:5000], out


def parse_meta(path, title_index):
    t = pathlib.Path(path).read_text(encoding="utf-8")
    if "## Titles" in t: return parse_meta_en(t, title_index)
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
    ap.add_argument("--srt", default="", help="caption file to attach as a Korean caption track (needs youtube.force-ssl scope)")
    ap.add_argument("--video-id", default="", help="skip the upload and only set thumbnail/captions/playlist on this existing video")
    ap.add_argument("--channel", default="km", choices=["km", "gsb"])
    ap.add_argument("--srt-lang", default="", help="caption language (default: video language)")
    ap.add_argument("--publish-at", default="", help="RFC3339 UTC time; uploads private and auto-publishes then")
    ap.add_argument("--lang", default="", help="video language (default: en for youtube-meta-en.md, else ko)")
    a = ap.parse_args()
    if not a.lang: a.lang = "en" if "## Titles" in pathlib.Path(a.meta).read_text(encoding="utf-8") else "ko"
    token = get_token(a.channel)
    st, _, body = req("GET", f"{API}/channels?part=snippet&mine=true", token)
    if st != 200: sys.exit(f"token check failed: {st} {body[:300]}")
    ch = json.loads(body)["items"][0]; print("channel:", ch["snippet"]["title"], ch["id"])
    title, desc, tags = parse_meta(a.meta, a.title_index)
    if title.lstrip().upper().startswith("[OLD"): sys.exit("refused: titles starting with [OLD are never published")
    print("title:", title); print("tags:", len(tags)); print("privacy:", a.privacy)
    if a.check: return
    if a.video_id:
        vid = a.video_id
    else:
        vid = upload(a, token, title, desc, tags)
    finish(a, token, vid)


def upload(a, token, title, desc, tags):
    video = pathlib.Path(a.video); size = video.stat().st_size
    meta = {"snippet": {"title": title, "description": desc, "tags": tags, "categoryId": a.category, "defaultLanguage": a.lang, "defaultAudioLanguage": a.lang},
            "status": {"privacyStatus": "private" if a.publish_at else a.privacy, "selfDeclaredMadeForKids": False}}
    if a.publish_at: meta["status"]["publishAt"] = a.publish_at
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
    return vid


def finish(a, token, vid):
    if a.thumb:
        with open(a.thumb, "rb") as f: img = f.read()
        st, _, body = req("POST", f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}", token, img,
                          headers={"Content-Type": "image/png", "Content-Length": str(len(img))}, raw=True)
        print("thumbnail:", "ok" if st == 200 else f"{st} {body[:200]}")
    if a.srt:
        srt = open(a.srt, "rb").read()
        meta_c = json.dumps({"snippet": {"videoId": vid, "language": a.srt_lang or a.lang, "name": "English" if (a.srt_lang or a.lang) == "en" else "한국어 자막", "isDraft": False}}).encode()
        boundary = b"yadam_caption_boundary"
        body = (b"--" + boundary + b"\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n" + meta_c + b"\r\n--" + boundary +
                b"\r\nContent-Type: application/octet-stream\r\n\r\n" + srt + b"\r\n--" + boundary + b"--")
        st, _, resp = req("POST", "https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart", token, body,
                          headers={"Content-Type": "multipart/related; boundary=" + boundary.decode(), "Content-Length": str(len(body))}, raw=True)
        print("captions:", "ok" if st == 200 else f"{st} {resp[:200]}")
    if a.playlist:
        st, _, body = req("POST", f"{API}/playlistItems?part=snippet", token,
                          {"snippet": {"playlistId": a.playlist, "resourceId": {"kind": "youtube#video", "videoId": vid}}})
        print("playlist:", "ok" if st == 200 else f"{st} {body[:200]}")


if __name__ == "__main__":
    main()
