#!/usr/bin/env python3
"""One-tap pinning page for the owner: pinterest/quick-pin.html (served by GitHub Pages at
https://actsb.github.io/claudefold/pinterest/quick-pin.html).

The Pinterest API path needs Standard access, which the app does not have yet, so no pin has gone out. This page lists every
pin drafted in pinterest/pins-*.md, newest first, with the image and two buttons: "Pin it" opens Pinterest's own Save dialog
with the image, link and description filled in (the owner picks the board and saves, so the owner chooses every pin), and
"Copy title" puts the title on the clipboard for the title field. Pins whose text names a sale that has ended are flagged.

  python3 scripts/quick_pins.py              # rebuild the page after adding pin entries
  python3 scripts/quick_pins.py --release 3  # also release up to 3 more pins into the RSS feed (the daily workflow does this)

The same entries feed pinterest/feed.xml (https://actsb.github.io/claudefold/pinterest/feed.xml), which Pinterest's own
"Auto-publish from RSS feed" turns into pins once the owner connects it (daily/pinterest-setup.md, "RSS auto-publish").
Pins are released a few a day, newest post first (pinterest/feed-state.json keeps each pin's release date), so a new
account does not drop 26 pins at once. Pins that name an ended sale stay out of the feed.
"""
import datetime, email.utils, html, json, pathlib, re, sys, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = "https://actsb.github.io/claudefold/"
OUT = ROOT / "pinterest" / "quick-pin.html"
FEED = ROOT / "pinterest" / "feed.xml"
STATE = ROOT / "pinterest" / "feed-state.json"
# sale dates already past: a pin that leans on them should be edited before it goes out
ENDED = [(re.compile(r"Prime Big Deal Days|October 6(?:–| to |-)7|Oct(?:ober)? 6", re.I), datetime.date(2026, 10, 7))]


def field(block, name):
    m = re.search(rf"\*\*{name}\*\*\n(.+?)(?:\n\n|\Z)", block, re.S)
    return m.group(1).strip() if m else ""


def entries():
    out = []
    for f in sorted(ROOT.glob("pinterest/pins-*.md"), reverse=True):
        for block in reversed(re.split(r"\n(?=## )", f.read_text(encoding="utf-8"))):
            m = re.match(r"## (.+?) — `([^`]+)`", block)
            if not m:
                continue
            e = {"name": m.group(1), "img": m.group(2), "title": field(block, "Title"), "desc": field(block, "Description"),
                 "link": field(block, "Link"), "alt": field(block, "Alt text")}
            if not e["link"].startswith("https://acts39.blogspot.com/") or "WRITE" in block:
                continue
            text = " ".join((e["title"], e["desc"]))
            e["stale"] = any(rx.search(text) and datetime.date.today() > end for rx, end in ENDED)
            out.append(e)
    seen, uniq = set(), []
    for e in out:                       # one pin per post link (the newest draft wins)
        if e["link"] not in seen:
            seen.add(e["link"]); uniq.append(e)
    return uniq


def main():
    es = entries()
    cards = []
    for i, e in enumerate(es):
        media = PAGES + e["img"]
        save = "https://www.pinterest.com/pin/create/button/?" + urllib.parse.urlencode({"url": e["link"], "media": media, "description": e["desc"]})
        warn = ('<p class="warn">This pin mentions a sale that has ended. Edit the text in Pinterest before saving, or skip it.</p>' if e["stale"] else "")
        cards.append(f'''<article>
<img src="{html.escape(media)}" alt="{html.escape(e["alt"])}" loading="lazy" width="1000" height="1500">
<div class="body">
<h2>{html.escape(e["title"])}</h2>
<p class="desc">{html.escape(e["desc"])}</p>{warn}
<div class="row"><a class="pin" href="{html.escape(save)}" target="_blank" rel="noopener">Pin it</a>
<button type="button" data-copy="t{i}">Copy title</button><button type="button" data-copy="a{i}">Copy alt text</button></div>
<textarea id="t{i}" hidden>{html.escape(e["title"])}</textarea><textarea id="a{i}" hidden>{html.escape(e["alt"])}</textarea>
<p class="link"><a href="{html.escape(e["link"])}" target="_blank" rel="noopener">{html.escape(e["link"].replace("https://acts39.blogspot.com", ""))}</a></p>
</div></article>''')
    page = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Quick pins · Verdict Picks</title>
<style>
:root{{--ink:#1B2A41;--green:#1E8E5A;--red:#E60023;--bg:#F7F5F0}}
body{{margin:0;background:var(--bg);color:#222;font:16px/1.5 -apple-system,Segoe UI,Roboto,Arial,sans-serif}}
header{{max-width:1100px;margin:0 auto;padding:20px 16px 4px}} h1{{color:var(--ink);font-size:24px;margin:0 0 6px}}
header p{{margin:4px 0;color:#444}} main{{max-width:1100px;margin:0 auto;padding:12px 16px 40px;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:16px}}
article{{background:#fff;border:1px solid #DDE3EA;border-left:5px solid var(--red);border-radius:14px;overflow:hidden;display:flex;gap:12px;padding:12px}}
article img{{width:110px;height:165px;object-fit:cover;border-radius:8px;flex:0 0 110px;background:#eee}}
.body{{min-width:0;display:flex;flex-direction:column;gap:6px}} h2{{font-size:16px;margin:0;color:var(--ink);line-height:1.3}}
.desc{{font-size:13.5px;color:#555;margin:0;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}}
.warn{{margin:0;font-size:13px;color:#8A4B0C;background:#FBEFE2;border-radius:8px;padding:4px 8px}}
.row{{display:flex;flex-wrap:wrap;gap:6px;margin-top:auto}} .pin{{background:var(--red);color:#fff;font-weight:700;text-decoration:none;padding:8px 14px;border-radius:999px}}
button{{border:1px solid #ccd;background:#fff;border-radius:999px;padding:7px 11px;font:inherit;font-size:13px;cursor:pointer}}
.link{{margin:0;font-size:12px;word-break:break-all}} .link a{{color:#678}}
</style></head><body>
<header><h1>Quick pins ({len(es)})</h1>
<p><strong>Pin it</strong>을 누르면 핀터레스트 저장 창이 이미지·링크·설명이 채워진 채로 열립니다. 보드를 고르고 저장하세요. 제목 칸은 <strong>Copy title</strong>로 복사해 붙여 넣으면 됩니다.</p>
<p>하루 5~10개씩, 위에서부터(최신 글 먼저). 같은 핀을 여러 보드에 한꺼번에 올리지 마세요. 주황 경고가 붙은 핀은 끝난 세일을 언급하니 문구를 고치거나 건너뛰세요.</p></header>
<main>
{chr(10).join(cards)}
</main>
<script>document.addEventListener('click',e=>{{const b=e.target.closest('button[data-copy]');if(!b)return;const t=document.getElementById(b.dataset.copy).value;navigator.clipboard.writeText(t).then(()=>{{const o=b.textContent;b.textContent='Copied';setTimeout(()=>b.textContent=o,1200)}})}});</script>
</body></html>
'''
    OUT.write_text(page, encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: {len(es)} pins, {sum(e['stale'] for e in es)} flagged as naming an ended sale")


def feed(es, release):
    """RSS 2.0 for Pinterest auto-publish: one item per released pin, the tall pin image as the enclosure and media:content."""
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    today = datetime.date.today().isoformat()
    for e in [e for e in es if not e["stale"] and e["link"] not in state][:release]:
        state[e["link"]] = today
    STATE.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    items = []
    for e in sorted([e for e in es if e["link"] in state and not e["stale"]], key=lambda e: state[e["link"]], reverse=True):
        img = PAGES + e["img"]
        f = ROOT / e["img"]
        when = email.utils.format_datetime(datetime.datetime.fromisoformat(state[e["link"]] + "T12:00:00+00:00"))
        items.append(f"""<item>
<title>{html.escape(e["title"])}</title>
<link>{html.escape(e["link"])}</link>
<guid isPermaLink="false">{html.escape(e["link"])}#pin</guid>
<pubDate>{when}</pubDate>
<description>{html.escape(e["desc"])}</description>
<enclosure url="{html.escape(img)}" type="image/png" length="{f.stat().st_size if f.exists() else 0}"/>
<media:content url="{html.escape(img)}" medium="image" type="image/png" width="1000" height="1500"/>
</item>""")
    FEED.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>Verdict Picks: buying guides</title>
<link>https://acts39.blogspot.com/</link>
<atom:link href="{PAGES}pinterest/feed.xml" rel="self" type="application/rss+xml"/>
<description>New Verdict Picks buying guides for Pinterest. Guides contain paid Amazon links.</description>
<language>en-us</language>
{chr(10).join(items)}
</channel>
</rss>
""", encoding="utf-8")
    print(f"{FEED.relative_to(ROOT)}: {len(items)} pins released, {sum(1 for e in es if e['link'] not in state and not e['stale'])} waiting")


if __name__ == "__main__":
    main()
    feed(entries(), int(sys.argv[sys.argv.index("--release") + 1]) if "--release" in sys.argv else 0)
