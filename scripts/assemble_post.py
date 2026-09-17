#!/usr/bin/env python3
"""Assemble a post: the easy shopping-guide layer + the long deep-dive folded into <details>.

Usage: python3 scripts/assemble_post.py posts/<slug>
Reads  src/00-easy.html (placeholders: <!--TOPPICK-->, <!--CARDS-->, <!--CARD:id-->),
       cards.json, images/cards/<id>.svg, src/01..06 (the deep-dive parts)
Writes post.src.html (then run build_post.py to inline the remaining <!--SVG:...--> figures).
"""
import json, re, sys, pathlib, html, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from host import host_banner

BADGE = ('display:inline-block;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.02em;'
         'padding:4px 11px;border-radius:999px;background:{bg};color:#fff;')
BTN = ('display:inline-block;background:#1E8E5A;color:#fff;text-decoration:none;font-weight:700;'
       'font-size:18px;padding:12px 20px;border-radius:8px;')
VIDEO = ('<div class="vp-video" style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;background:#000;margin:14px 0 4px;">'
         '<iframe style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" src="https://www.youtube.com/embed/{vid}?rel=0" title="{title}" loading="lazy" '
         'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>')

def esc(s): return html.escape(s, quote=True)

STYLE = """<style>
.vp-post img{max-width:100%;height:auto}
.vp-post .vp-grid a{color:#1B2A41;font-weight:700}
.vp-post p a[href*="amazon.com"],.vp-post li a[href*="amazon.com"]{color:#1E8E5A;font-weight:700;text-decoration:underline dotted;text-underline-offset:3px}
@media (max-width:640px){
  .vp-post .vp-gridwrap{overflow:visible}
  .vp-post .vp-grid{min-width:0!important;display:block;border:0}
  .vp-post .vp-grid thead{display:none}
  .vp-post .vp-grid tbody,.vp-post .vp-grid tr{display:block}
  .vp-post .vp-grid tr{border:1px solid #ddd;border-radius:10px;margin:0 0 14px;overflow:hidden}
  .vp-post .vp-grid td{display:block;border:0!important;border-top:1px solid #eee!important;padding:9px 12px!important}
  .vp-post .vp-grid td:first-child{border-top:0!important;background:#1B2A41!important;color:#fff;font-size:1.05em}
  .vp-post .vp-moment>div:first-child{margin:0 auto}
  .vp-post .vp-host-text{display:block!important}
  .vp-post .vp-figure,.vp-post .vp-strip{overflow-x:auto;-webkit-overflow-scrolling:touch}
  .vp-post .vp-figure svg[viewBox^="0 0 1200"],.vp-post .vp-strip svg[viewBox^="0 0 1200"]{width:820px;max-width:none;display:block}
  .vp-post .vp-figure .vp-source,.vp-post .vp-strip .vp-source{position:sticky;left:0}
  .vp-post .vp-grid td[data-col]:not(:first-child)::before{content:attr(data-col);display:block;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;color:#1E8E5A;margin-bottom:2px}
}
</style>
"""

def responsive_grid(html_text):
    """Add class vp-grid + data-col labels to the picker table so the CSS can stack it on phones."""
    def fix_table(m):
        t = m.group(0)
        heads = re.findall(r"<th[^>]*>(.*?)</th>", t, flags=re.S)
        def fix_row(rm):
            row = rm.group(0); i = [0]
            def fix_td(tm):
                label = re.sub(r"<[^>]+>", "", heads[i[0]]) if i[0] < len(heads) else ""
                i[0] += 1
                return tm.group(1) + f' data-col="{esc(label)}"' + tm.group(2)
            return re.sub(r"(<td)([^>]*>)", fix_td, row)
        t = re.sub(r"<tr>.*?</tr>", fix_row, t, flags=re.S)
        t = t.replace("<table ", '<table class="vp-grid" ', 1)
        return t
    html_text = re.sub(r'<table style="border-collapse:collapse;width:100%;[^"]*min-width:\d+px[^"]*">.*?</table>', fix_table, html_text, count=0, flags=re.S)
    return html_text.replace('<div style="overflow-x:auto;margin:1em 0 1.4em;">', '<div class="vp-gridwrap" style="overflow-x:auto;margin:1em 0 1.4em;">')


def card_svg(d, cid):
    f = d / "images" / "cards" / f"{cid}.svg"
    svg = f.read_text(encoding="utf-8").strip()
    return re.sub(r"^<\?xml[^>]*\?>\s*", "", svg)

def is_paid(c):
    return "amazon.com" in c.get("cta", "") or c.get("paid", False)

def cta(c, label):
    rel = c.get("rel", "nofollow sponsored noopener" if is_paid(c) else "nofollow noopener")
    tag = ' <span style="font-size:13px;font-weight:600;color:#555;margin-left:6px;">(paid link)</span>' if is_paid(c) else ""
    return f'<a style="{BTN}" href="{esc(c["cta"]).replace("&amp;amp;","&amp;")}" rel="{rel}" target="_blank">{esc(c.get("cta_label", label))} →</a>' + tag

def top_pick(d, c):
    return f'''<div class="vp-top" id="top-pick" style="display:flex;flex-wrap:wrap;gap:22px;align-items:center;border:3px solid #1E8E5A;border-radius:16px;padding:20px;background:#fff;margin:1.2em 0 1.6em;">
<div style="flex:1 1 280px;min-width:0;">{card_svg(d, c["id"])}</div>
<div style="flex:1.2 1 300px;min-width:0;">
<span style="{BADGE.format(bg='#1E8E5A')}">{esc(c["badge"])}</span>
<h3 style="font-size:1.7em;line-height:1.2;margin:.35em 0 .2em;color:#1B2A41;">{esc(c["name"])}</h3>
<p style="font-size:1.25em;font-weight:700;color:#1E8E5A;margin:0 0 .6em;">{esc(c["price"])}</p>
<ul style="margin:0 0 1em;padding-left:20px;">
<li style="margin-bottom:.4em;"><strong>Buy it if</strong> {esc(c["buy_if"])}</li>
<li style="margin-bottom:.4em;"><strong>Skip it if</strong> {esc(c["skip_if"])}</li>
<li><strong>From the reviews:</strong> {esc(c["owners"])}</li>
</ul>
{cta(c, "See today's price on Amazon")}
</div>
</div>'''

WATCH = ('<div class="vp-watch" id="watch-{cid}" style="margin:18px -18px -18px;padding:14px 18px 18px;border-top:1px solid #e3e3e3;background:#F7F5F0;border-radius:0 0 13px 13px;">'
         '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-bottom:10px;">'
         '<span style="display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;background:#1E8E5A;color:#fff;font-size:12px;flex:0 0 auto;">&#9654;</span>'
         '<span style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#1E8E5A;">Watch &middot; video {n} of {total}</span>'
         '<span style="margin-left:auto;font-size:13px;color:#666;">{channel} &middot; <a href="https://www.youtube.com/watch?v={vid}" rel="noopener" target="_blank" style="color:#1B2A41;font-weight:700;">Watch on YouTube</a></span></div>'
         '<div class="vp-video" style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;background:#000;">'
         '<iframe style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;" src="https://www.youtube.com/embed/{vid}?rel=0" title="{title}" loading="lazy" '
         'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
         '<p style="margin:10px 0 0;font-size:15px;line-height:1.5;color:#333;"><strong style="color:#1B2A41;">Why this one:</strong> {why}</p></div>')

def card_video(d, c):
    """Plain embed by default; the framed, numbered Watch panel when the card explains why the video is worth it."""
    title = esc(c.get("video_title", c["name"] + " review"))
    if not c.get("video_why"):
        return VIDEO.format(vid=c["video"], title=title)
    with_video = [x["id"] for x in json.loads((d / "cards.json").read_text(encoding="utf-8"))["cards"] if x.get("video")]
    return WATCH.format(cid=c["id"], n=with_video.index(c["id"]) + 1, total=len(with_video), channel=esc(c.get("video_channel", "YouTube")),
                        vid=c["video"], title=title, why=esc(c["video_why"]))

def pick_card(d, c, n, with_video=True):
    vid = card_video(d, c) if (c.get("video") and with_video) else ""
    return f'''<div class="vp-card" id="card-{c["id"]}" style="border:1px solid #ddd;border-radius:14px;padding:18px;background:#fff;margin:1.2em 0;">
<div style="display:flex;flex-wrap:wrap;gap:20px;align-items:center;">
<div style="flex:1 1 240px;min-width:0;max-width:420px;">{card_svg(d, c["id"])}</div>
<div style="flex:1.4 1 280px;min-width:0;">
<span style="{BADGE.format(bg='#1B2A41')}">{n}. {esc(c["badge"])}</span>
<h3 style="font-size:1.45em;line-height:1.2;margin:.35em 0 .2em;color:#1B2A41;">{esc(c["name"])}</h3>
<p style="font-size:1.15em;font-weight:700;color:#1E8E5A;margin:0 0 .5em;">{esc(c["price"])}</p>
<ul style="margin:0 0 .9em;padding-left:20px;">
<li style="margin-bottom:.35em;"><strong>Buy it if</strong> {esc(c["buy_if"])}</li>
<li style="margin-bottom:.35em;"><strong>Skip it if</strong> {esc(c["skip_if"])}</li>
<li><strong>From the reviews:</strong> {esc(c["owners"])}</li>
</ul>
{cta(c, "Check the price on Amazon")}
</div>
</div>
{vid}
</div>'''

def buy_box(d, cards):
    """<!--BUYBOX--> : a framed 'buy box' with one row per card that carries a `buy` dict
    ({"pick": "which variant/size", "check": "what to confirm on the listing", "tier": "Good"}), a button each, and the total line from spec["buy_total"]."""
    spec = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    rows = []
    for i, c in enumerate([c for c in cards if c.get("buy")], 1):
        b = c["buy"]
        thumb = (d / "images" / "cards" / f'{c["id"]}.svg')
        svg = re.sub(r"<g font-family=.*?</g>\s*", "", thumb.read_text(encoding="utf-8"), flags=re.S) if thumb.exists() else ""   # render without the chip/name text
        svg = re.sub(r'<svg ', '<svg style="width:100%;height:100%;display:block;" ', svg, count=1)
        rows.append(
            f'<div style="display:flex;flex-wrap:wrap;align-items:center;gap:14px;padding:14px 18px;border-top:1px solid #e6e6e6;">'
            f'<div style="flex:0 0 96px;width:96px;height:64px;border-radius:10px;overflow:hidden;background:#F7F5F0;">{svg}</div>'
            f'<div style="flex:1 1 220px;min-width:0;">'
            f'<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#1E8E5A;">{i} &middot; {esc(b.get("tier", ""))}</div>'
            f'<div style="font-size:17px;font-weight:700;color:#1B2A41;line-height:1.3;">{esc(c["name"])}</div>'
            f'<div style="font-size:14px;color:#444;margin-top:2px;"><strong>Pick:</strong> {esc(b["pick"])}</div>'
            f'<div style="font-size:13px;color:#666;margin-top:2px;"><strong>Check:</strong> {esc(b["check"])}</div></div>'
            f'<div style="flex:0 0 auto;text-align:center;"><a href="{esc(c["cta"])}" rel="{c.get("rel", "nofollow sponsored noopener" if is_paid(c) else "nofollow noopener")}" target="_blank" style="display:inline-flex;align-items:center;gap:8px;background:#1E8E5A;color:#fff;font-weight:700;font-size:16px;padding:12px 18px;border-radius:10px;text-decoration:none;white-space:nowrap;">'
            f'<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.8a2 2 0 0 0 2-1.5L21 8H7"/><circle cx="10" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/></svg>'
            f'{esc(b.get("label", "See price on Amazon"))}</a>' + ('<div style="font-size:12px;color:#666;margin-top:4px;">paid link</div>' if is_paid(c) else '<div style="font-size:12px;color:#666;margin-top:4px;">plain link</div>') + '</div></div>')
    total = spec.get("buy_total", "")
    return (f'<div class="vp-buybox" id="buy-box" style="border:2px solid #1B2A41;border-radius:16px;overflow:hidden;background:#fff;margin:1.6em 0;">'
            f'<div style="display:flex;align-items:center;gap:12px;padding:14px 18px;background:#1B2A41;color:#fff;">'
            f'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#9fd9b9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.8a2 2 0 0 0 2-1.5L21 8H7"/><circle cx="10" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/></svg>'
            f'<div><div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#9fd9b9;">Buy box &middot; every pick on this page</div>'
            f'<div style="font-size:18px;font-weight:700;line-height:1.25;">{esc(spec.get("buy_title", "The exact version to order, one tap each"))}</div></div></div>'
            + "".join(rows) +
            (f'<div style="padding:12px 18px 14px;border-top:1px solid #e6e6e6;background:#F7F5F0;font-size:14px;color:#444;line-height:1.5;">{total}</div>' if total else "") +
            '</div>')

def main(post_dir):
    d = pathlib.Path(post_dir)
    spec = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    cards = spec["cards"]; by_id = {c["id"]: c for c in cards}
    easy = (d / "src" / "00-easy.html").read_text(encoding="utf-8")
    easy = responsive_grid(easy)
    easy = easy.replace('<div class="vp-post"', STYLE + '<div class="vp-post"', 1)
    strip = ('<p class="vp-nav" style="font-size:15px;margin:0 0 .8em;color:#555;"><strong style="color:#1B2A41;">Guides:</strong> '
             '<a href="/p/robot-vacuums.html" style="color:#1B2A41;">Robot Vacuums</a> · <a href="/p/wireless-earbuds.html" style="color:#1B2A41;">Wireless Earbuds</a> · '
             '<a href="/p/smart-glasses.html" style="color:#1B2A41;">Smart Glasses</a> · <a href="/p/power-stations.html" style="color:#1B2A41;">Power Stations</a> · <a href="/p/best-sellers.html" style="color:#1B2A41;">Best Sellers</a></p>\n')
    easy = easy.replace('<div class="vp-post" style="font-size:19px;line-height:1.6;color:#222;">', '<div class="vp-post" style="font-size:19px;line-height:1.6;color:#222;">\n' + strip, 1)
    notice = ('<p class="vp-notice" style="font-size:16px;background:#F7F5F0;border-left:5px solid #1B2A41;padding:10px 14px;margin:0 0 1.2em;">'
              '<strong>Two ways to read this.</strong> In a hurry: the quick guide starts right here — one pick, a 10-second picker, every product in 30 seconds. '
              'Have twenty minutes: the <a href="#deep" style="color:#1B2A41;font-weight:700;">complete deep-dive</a> follows on this same page — how we tested, every brand, every pick in detail, thousands of owner reviews, and when to buy.</p>\n')
    if sorted((d / "src").glob("0[1-9]-*.html")):   # only guides with a deep-dive get the two-ways notice
        easy = easy.replace("<h2 style=", notice + "<h2 style=", 1)
    # Blogger jump break after the lead paragraph: index pages show only the lead, and
    # auto-pagination stops hiding posts because of the page size
    easy = re.sub(r'(<p style="font-size:1\.25em;[^"]*">.*?</p>)', r'\1\n<!--more-->', easy, count=1, flags=re.S)
    easy = easy.replace("<!--TOPPICK-->", top_pick(d, cards[0]))
    easy = easy.replace("<!--BUYBOX-->", buy_box(d, cards))
    def host_fig(m):
        pose, lines = m.group(1), [html.escape(x) for x in m.group(2).split("|") if x.strip()]
        art = cards[0].get("art", {})
        gl = {"frame": art.get("frame", "#111"), "style": "round" if art.get("style") == "round" else "wayfarer"} if spec["category"] == "glasses" else None
        eb = art.get("bud", "#222") if spec["category"] == "earbuds" else None
        # phones shrink the banner until the speech bubble is unreadable, so the same lines follow as text (shown by the phone CSS only)
        text = ('<div class="vp-host-text" style="display:none;background:#F7F5F0;border-left:5px solid #1E8E5A;padding:12px 14px;margin:-.4em 0 1.2em;font-size:16px;line-height:1.45;color:#222;">'
                + "<br>".join(f"<strong>{l}</strong>" if i == 0 else l for i, l in enumerate(lines)) + '</div>')
        return '<div class="vp-host" style="margin:1em 0 1.2em;">' + host_banner("hb", lines, pose=pose, glasses=gl, earbud=eb) + '</div>' + text
    easy = re.sub(r"<!--HOST:([a-z]+)\|(.*?)-->", host_fig, easy)
    def pin_block(m):
        cov = json.loads((d / "cover.json").read_text(encoding="utf-8")) if (d / "cover.json").exists() else {}
        url = cov.get("url", ""); img = f"https://raw.githubusercontent.com/actsb/claudefold/claude/sharp-lovelace-n7vhzq/{d.as_posix()}/images/pin.png"
        desc = cov.get("alt", " ".join(cov.get("title", [])))
        save = "https://pinterest.com/pin/create/button/?" + urllib.parse.urlencode({"url": url, "media": img, "description": desc})
        return (f'<div class="vp-pin" style="display:flex;flex-wrap:wrap;gap:20px;align-items:center;border:1px solid #ddd;border-radius:14px;padding:18px;background:#fff;margin:1.6em 0;">'
                f'<a href="{save}" rel="noopener nofollow" target="_blank" style="flex:0 1 220px;"><img src="{img}" alt="{html.escape(desc)}" width="1000" height="1500" style="width:100%;max-width:220px;height:auto;border-radius:10px;display:block;" loading="lazy"></a>'
                f'<div style="flex:1 1 260px;min-width:0;"><h3 style="margin:0 0 .3em;color:#1B2A41;font-size:1.25em;">Save this guide for later</h3>'
                f'<p style="margin:0 0 .8em;font-size:17px;">Pin it to your Pinterest board and it will be there when the sale hits.</p>'
                f'<a href="{save}" rel="noopener nofollow" target="_blank" style="display:inline-block;background:#E60023;color:#fff;text-decoration:none;font-weight:700;font-size:17px;padding:11px 18px;border-radius:8px;">Save to Pinterest</a></div></div>')
    easy = re.sub(r"<!--PIN-->", pin_block, easy)
    def strip_fig(m):
        sid, cap = m.group(1), m.group(2) or ""
        f = d / "images" / "strips" / f"{sid}.svg"
        if not f.exists(): return ""
        svg = re.sub(r"^<\?xml[^>]*\?>\s*", "", f.read_text(encoding="utf-8").strip())
        capt = f'<div style="font-size:14px;color:#555;margin-top:6px;">{cap}</div>' if cap else ""
        return f'<div class="vp-strip" style="margin:1.2em 0;">{svg}{capt}</div>'
    easy = re.sub(r"<!--STRIP:([a-z0-9\-]+)(?:\|(.*?))?-->", strip_fig, easy)
    easy = easy.replace("<!--CARDS-->", "\n".join(pick_card(d, c, i + 1, with_video=(i > 0)) for i, c in enumerate(cards)))
    easy = re.sub(r"<!--CARD:([a-z0-9\-]+)-->", lambda m: pick_card(d, by_id[m.group(1)], cards.index(by_id[m.group(1)]) + 1), easy)
    parts = sorted(p for p in (d / "src").glob("0[1-9]-*.html"))
    if not parts:
        # short story post: no deep-dive, just close the wrapper
        out = (easy + '<p style="font-size:15px;color:#555;"><em>As an Amazon Associate I earn from qualifying purchases. Prices and availability are those seen at US retailers at the time of writing (September 2026), are subject to change, and the price shown on Amazon at checkout is the one that applies. We do not accept products or payment from manufacturers. <a href="/p/how-we-rank-products.html">How we rank</a> · <a href="/p/affiliate-disclosure.html">Disclosure</a></em></p>\n</div>\n')
        (d / "post.src.html").write_text(out, encoding="utf-8")
        print(f"assembled {d/'post.src.html'} ({len(out):,} bytes, {len(cards)} cards, no deep-dive)"); return
    deep = "\n".join(p.read_text(encoding="utf-8") for p in parts)
    # strip the wrapper, byline and cover the deep-dive parts open with, and the wrapper close at the end
    deep = re.sub(r'^\s*<div class="vp-post"[^>]*>\s*<p[^>]*><em>.*?</em></p>\s*<p[^>]*><img[^>]*></p>', "", deep, count=1, flags=re.S)
    deep = re.sub(r"</div>\s*$", "", deep.rstrip(), count=1)
    # reading guide for the deep-dive: one line per section with a minutes estimate
    secs = [(m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip(), m.start()) for m in re.finditer(r'<h2 id="([a-z0-9\-]+)"[^>]*>(.*?)</h2>', deep, flags=re.S)]
    items = []
    for i, (sid, title, pos) in enumerate(secs):
        nxt = secs[i + 1][2] if i + 1 < len(secs) else len(deep)
        words = len(re.findall(r"[A-Za-z0-9$][A-Za-z0-9$'’.,%/-]*", re.sub(r"<[^>]+>", " ", deep[pos:nxt])))
        mins = max(1, round(words / 230))
        items.append(f'<li style="margin-bottom:.3em;"><a href="#{sid}" style="color:#1B2A41;font-weight:700;">{esc(title)}</a> <span style="color:#777;font-size:.9em;">· about {mins} min</span></li>')
    out = (easy
           + '\n<h2 id="deep" style="color:#1B2A41;font-size:1.6em;line-height:1.25;margin:1.6em 0 .5em;">Have more time? The full deep-dive, section by section</h2>\n'
           + '<p>The quick guide above is enough to buy well. If you want to know <em>why</em> — how we tested, what every brand does well and badly, every pick in detail, what thousands of owners said, and when to buy — the complete analysis follows. Read it in one go, or one section at a time when you have a few minutes. Each section stands on its own.</p>\n'
           + '<div class="vp-roadmap" style="border:2px solid #1B2A41;border-radius:12px;padding:14px 20px;background:#F7F5F0;margin:1em 0 1.6em;">\n<strong style="color:#1B2A41;">Reading plan</strong>\n<ol style="margin:8px 0 0;padding-left:22px;">\n' + "\n".join(items) + '\n</ol>\n</div>\n'
           + '<div class="vp-deep" style="border-top:3px solid #1B2A41;margin-top:1.4em;padding-top:1.2em;font-size:0.94em;">\n' + deep + '\n</div>\n'
           + '<p style="margin:1.6em 0 1em;"><a href="#top-pick" style="display:inline-block;background:#1B2A41;color:#fff;text-decoration:none;font-weight:700;padding:10px 16px;border-radius:8px;">↑ Back to the quick guide and the top pick</a></p>\n'
           + '<p style="font-size:15px;color:#555;"><em>As an Amazon Associate I earn from qualifying purchases. Prices and availability are those seen at US retailers at the time of writing (September 2026), are subject to change, and the price shown on Amazon at checkout is the one that applies. We do not accept products or payment from manufacturers. <a href="/p/how-we-rank-products.html">How we rank</a> · <a href="/p/affiliate-disclosure.html">Disclosure</a></em></p>\n'
           + '</div>\n')
    (d / "post.src.html").write_text(out, encoding="utf-8")
    print(f"assembled {d/'post.src.html'} ({len(out):,} bytes, {len(cards)} cards)")

if __name__ == "__main__":
    main(sys.argv[1])
