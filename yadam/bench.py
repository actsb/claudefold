#!/usr/bin/env python3
"""bench 명당 조사: which publish slots (KST weekday x hour) and lengths work best, from public data.
Looks at recent uploads of benchmark channels (and our own), computes views per day since publish,
and ranks slots and Shorts-vs-long. Public data only; costs ~3 units per channel.
Usage: python3 yadam/bench.py [--channels UC...,UC...] [--per 50] [--token km]
Default channels: our two channels. Add benchmark channel ids with --channels."""
import argparse, collections, datetime as dt, re, statistics, sys; sys.path.insert(0, __import__("os").path.dirname(__file__))
from ytlib import token, get, chunks, CHANNELS

def secs(iso):
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0

ap = argparse.ArgumentParser(); ap.add_argument("--channels", default=",".join(CHANNELS.values()))
ap.add_argument("--per", type=int, default=50); ap.add_argument("--token", default="km")
a = ap.parse_args(); tok = token(a.token)
now = dt.datetime.now(dt.timezone.utc); KST = dt.timezone(dt.timedelta(hours=9))
rows = []
for ch in a.channels.split(","):
    up = "UU" + ch[2:]
    ids = [i["contentDetails"]["videoId"] for i in get("playlistItems", tok, part="contentDetails", playlistId=up, maxResults=min(a.per, 50))["items"]]
    for c in chunks(ids):
        for v in get("videos", tok, part="snippet,statistics,contentDetails", id=",".join(c))["items"]:
            pub = dt.datetime.fromisoformat(v["snippet"]["publishedAt"].replace("Z", "+00:00"))
            age = max((now - pub).total_seconds() / 86400, 1)
            if age < 3: continue  # too fresh to judge
            rows.append(dict(ch=v["snippet"]["channelTitle"], kst=pub.astimezone(KST), vpd=int(v["statistics"].get("viewCount", 0)) / age,
                             short=secs(v["contentDetails"]["duration"]) <= 180, title=v["snippet"]["title"]))
if not rows: sys.exit("no data")
def table(key, label):
    g = collections.defaultdict(list)
    for r in rows: g[key(r)].append(r["vpd"])
    print(f"\n== {label} (median views/day, n)")
    for k, xs in sorted(g.items(), key=lambda kv: -statistics.median(kv[1])):
        print(f"  {k:<14} {statistics.median(xs):8.1f}  n={len(xs)}")
DOW = "월화수목금토일"
table(lambda r: r["ch"][:14], "channel")
table(lambda r: "Shorts" if r["short"] else "long", "format")
table(lambda r: DOW[r["kst"].weekday()] + "요일", "weekday (KST)")
table(lambda r: f"{r['kst'].hour // 3 * 3:02d}-{r['kst'].hour // 3 * 3 + 3:02d}시", "hour block (KST)")
print("\n== top 10 by views/day")
for r in sorted(rows, key=lambda r: -r["vpd"])[:10]:
    print(f"  {r['vpd']:8.1f}  {r['kst']:%m-%d %a %H:%M}  {'S' if r['short'] else 'L'}  {r['ch'][:12]}  {r['title'][:50]}")
print("\nNote: few samples per slot -> treat as a hint, not proof. For US viewers, KST 22-02시 = US morning/afternoon.")
