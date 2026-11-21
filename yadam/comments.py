#!/usr/bin/env python3
"""댓글 점검: recent comment threads on the channel; marks threads with no reply from the channel.
Read-only - drafts replies are written by Claude for the user to approve; this script never posts.
Usage: python3 yadam/comments.py [--channel km|gsb] [--days 7]   (quota: 1 unit per 100 threads)"""
import argparse, datetime as dt, sys; sys.path.insert(0, __import__("os").path.dirname(__file__))
from ytlib import token, get, CHANNELS

ap = argparse.ArgumentParser(); ap.add_argument("--channel", default="km"); ap.add_argument("--days", type=int, default=7)
a = ap.parse_args(); tok = token(a.channel); me = CHANNELS[a.channel]
since = (dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) - dt.timedelta(days=a.days)).isoformat() + "Z"
page, n = None, 0
while True:
    kw = {"part": "snippet,replies", "allThreadsRelatedToChannelId": me, "maxResults": 100, "order": "time", "textFormat": "plainText"}
    if page: kw["pageToken"] = page
    r = get("commentThreads", tok, **kw)
    for th in r["items"]:
        top = th["snippet"]["topLevelComment"]["snippet"]
        if top["publishedAt"] < since: page = None; break
        if top.get("authorChannelId", {}).get("value") == me: continue
        replied = any(x["snippet"].get("authorChannelId", {}).get("value") == me for x in th.get("replies", {}).get("comments", []))
        n += 1
        print(f"[{'답변함' if replied else '미답변'}] {top['publishedAt'][:10]} video={th['snippet'].get('videoId')} {top['authorDisplayName']}: {top['textDisplay'][:150]!r}")
    else:
        page = r.get("nextPageToken")
    if not page: break
print("threads:", n)
