#!/usr/bin/env python3
"""공개 조회수: public view/like/comment counts for the channel's videos (newest first).
Usage: python3 yadam/views.py [--channel km|gsb] [--limit 50] [--ids id1,id2]   (quota: ~2-3 units)"""
import argparse, sys; sys.path.insert(0, __import__("os").path.dirname(__file__))
from ytlib import token, get, chunks, CHANNELS

ap = argparse.ArgumentParser(); ap.add_argument("--channel", default="km"); ap.add_argument("--limit", type=int, default=50); ap.add_argument("--ids", default="")
a = ap.parse_args(); tok = token(a.channel)
if a.ids:
    ids = a.ids.split(",")
else:
    up = "UU" + CHANNELS[a.channel][2:]
    ids, page = [], None
    while len(ids) < a.limit:
        kw = {"part": "contentDetails", "playlistId": up, "maxResults": 50}
        if page: kw["pageToken"] = page
        r = get("playlistItems", tok, **kw); ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        page = r.get("nextPageToken")
        if not page: break
    ids = ids[:a.limit]
total = 0
for c in chunks(ids):
    for v in get("videos", tok, part="snippet,statistics,status", id=",".join(c))["items"]:
        s = v["statistics"]; total += int(s.get("viewCount", 0))
        print(f"{v['id']}  {v['snippet']['publishedAt'][:10]}  {v['status']['privacyStatus'][:3]}  views={s.get('viewCount',0):>6}  likes={s.get('likeCount',0):>4}  comments={s.get('commentCount',0):>3}  {v['snippet']['title'][:60]}")
print("total views:", total)
