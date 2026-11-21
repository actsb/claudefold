#!/usr/bin/env python3
"""토큰 점검: refresh each stored token and show which channel / Drive account it reaches.
Usage: python3 yadam/tok_check.py            (quota: 1 unit per YouTube account)"""
import sys; sys.path.insert(0, __import__("os").path.dirname(__file__))
from ytlib import token, get, CHANNELS, TOKDIR

ok = True
for name in ("km", "gsb"):
    if not (TOKDIR / f"{name}.json").exists():
        print(f"{name}: MISSING"); ok = False; continue
    it = get("channels", token(name), part="snippet,statistics", mine="true")["items"][0]
    good = it["id"] == CHANNELS[name]
    ok &= good
    print(f"{name}: {'OK ' if good else 'WRONG CHANNEL'} {it['snippet']['title']} subs={it['statistics'].get('subscriberCount')} videos={it['statistics'].get('videoCount')}")
if (TOKDIR / "drive.json").exists():
    u = get("https://www.googleapis.com/drive/v3/about", token("drive"), fields="user(displayName)")
    print("drive: OK", u["user"]["displayName"])
else:
    print("drive: MISSING"); ok = False
sys.exit(0 if ok else 1)
