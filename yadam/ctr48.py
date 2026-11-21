#!/usr/bin/env python3
"""ctr48: first-48-hour report for recent uploads (YouTube Analytics API, owner-only data).
Shows views, watch minutes, average view %, likes, subscribers gained per video published in the
last --days days, plus traffic sources. Note: impressions / impressions CTR are only in YouTube
Studio (Analytics API does not expose them) - copy them from Studio > Reach if needed.
Usage: python3 yadam/ctr48.py [--channel km] [--days 3]"""
import argparse, datetime as dt, sys; sys.path.insert(0, __import__("os").path.dirname(__file__))
from ytlib import token, get, ANALYTICS, CHANNELS

ap = argparse.ArgumentParser(); ap.add_argument("--channel", default="km"); ap.add_argument("--days", type=int, default=3)
a = ap.parse_args(); tok = token(a.channel)
up = "UU" + CHANNELS[a.channel][2:]
cut = (dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) - dt.timedelta(days=a.days)).isoformat() + "Z"
vids = [(i["contentDetails"]["videoId"], i["contentDetails"].get("videoPublishedAt", ""), i["snippet"]["title"])
        for i in get("playlistItems", tok, part="snippet,contentDetails", playlistId=up, maxResults=20)["items"]]
vids = [v for v in vids if v[1] >= cut]
if not vids: sys.exit(f"no uploads in the last {a.days} days")
today = dt.date.today().isoformat()
for vid, pub, title in vids:
    start = pub[:10]
    r = get(ANALYTICS, tok, ids="channel==MINE", startDate=start, endDate=today, filters=f"video=={vid}",
            metrics="views,estimatedMinutesWatched,averageViewPercentage,likes,subscribersGained")
    row = (r.get("rows") or [[0] * 5])[0]
    print(f"{vid} {pub[:16]} {title[:50]}\n  views={row[0]} watchMin={row[1]} avgView%={row[2]} likes={row[3]} subs+={row[4]}")
    s = get(ANALYTICS, tok, ids="channel==MINE", startDate=start, endDate=today, filters=f"video=={vid}",
            dimensions="insightTrafficSourceType", metrics="views", sort="-views")
    print("  sources:", ", ".join(f"{x[0]}={x[1]}" for x in (s.get("rows") or [])[:6]))
print("(Analytics data lags 24-48 h; impressions CTR: YouTube Studio only)")
