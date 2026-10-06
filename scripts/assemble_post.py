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
import link_cards as LC

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
""" + LC.CSS + """</style>
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


def teaser_first(html_text):
    """Blogger builds the home-page teaser and the feed summary from the first text in a post, and this blog's theme
    falls back to the blog-wide description for og:description, so the first words of the body are the only per-post
    preview we control. Order the top as cover → lead → jump break → style block → guide links → byline instead of
    style → guide links → byline → cover → lead. Idempotent: a post already in that order is returned unchanged."""
    m = re.match(r"\s*(<style>.*?</style>\s*)", html_text, flags=re.S)
    if not m:
        return html_text
    style, rest = m.group(1), html_text[m.end():]
    nav = re.search(r'<p class="vp-nav".*?</p>\s*', rest, flags=re.S)
    byline = re.search(r'<p style="font-size:15px;color:#555;"><em>(?:Published|Updated) .*?</em></p>\s*', rest, flags=re.S)
    lead = re.search(r'<p style="font-size:1\.25em;[^"]*">.*?</p>\s*<!--more-->\s*', rest, flags=re.S)
    if not (nav and byline and lead and nav.start() < lead.start() and byline.start() < lead.start()):
        return html_text
    moved = style + nav.group(0) + byline.group(0)
    out = rest[:lead.end()] + moved + rest[lead.end():]
    for block in (byline.group(0), nav.group(0)):          # drop the originals above the lead
        i = out.index(block)
        if i < out.index(moved):
            out = out[:i] + out[i + len(block):]
    return out

def with_more_guides(d, html_text):
    """Links to the closest live guides (scripts/site_index.py), just above the Pinterest box."""
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import site_index
    rel = d.resolve().relative_to(site_index.ROOT).as_posix()
    return site_index.inject(html_text, site_index.block(rel, site_index.build_index()))

def card_svg(d, cid):
    f = d / "images" / "cards" / f"{cid}.svg"
    svg = f.read_text(encoding="utf-8").strip()
    return re.sub(r"^<\?xml[^>]*\?>\s*", "", svg)

def is_paid(c):
    return "amazon.com" in c.get("cta", "") or c.get("paid", False)

def cta(c, label):
    rel = c.get("rel", "nofollow sponsored noopener" if is_paid(c) else "nofollow noopener")
    if c.get("cta_style") == "link":   # a quiet text link instead of a button, for roundups where only the top pick gets a button
        tag = ' <span style="font-size:13px;color:#555;white-space:nowrap;">(paid link)</span>' if is_paid(c) else ""
        return (f'<p style="margin:.2em 0 0;font-size:16px;"><a href="{esc(c["cta"]).replace("&amp;amp;","&amp;")}" rel="{rel}" target="_blank" '
                f'style="color:#1E8E5A;font-weight:700;text-decoration:underline;">{esc(c.get("cta_label", label))}</a>{tag}</p>')
    tag = ' <span style="font-size:13px;font-weight:600;color:#555;margin-left:6px;white-space:nowrap;display:inline-block;">(paid link)</span>' if is_paid(c) else ""
    return f'<a style="{BTN}" href="{esc(c["cta"]).replace("&amp;amp;","&amp;")}" rel="{rel}" target="_blank">{esc(c.get("cta_label", label))} →</a>' + tag

PAID_TAG = ' <span class="vp-paid" style="font-size:13px;color:#555;white-space:nowrap;">(paid link)</span>'
AMAZON_A = re.compile(r'<a\b[^>]*href="https://www\.amazon\.com/[^"]*"[^>]*>(.*?)</a>', re.S | re.I)


def label_paid_links(html_text):
    """Every Amazon link is marked "(paid link)" where the reader sees it (Amazon's link-disclosure rule and the FTC's
    "clear and conspicuous" test): add the label after any Amazon link with none inside it or in the next 160 characters."""
    out, last = [], 0
    for m in AMAZON_A.finditer(html_text):
        out.append(html_text[last:m.end()])
        if "paid link" not in m.group(1).lower() and "paid link" not in html_text[m.end(): m.end() + 160].lower():
            out.append(PAID_TAG)
        last = m.end()
    out.append(html_text[last:])
    return "".join(out)


def checked_month(d):
    """The month the post's prices were last checked: its "prices_checked" month in brand/seo-configs.json when set (a post
    can be updated without new price research), else the month of its "updated" date, else this month."""
    import datetime
    try:
        cfg = json.loads((pathlib.Path(__file__).resolve().parent.parent / "brand" / "seo-configs.json").read_text(encoding="utf-8"))
        if cfg[d.name].get("prices_checked"):
            return cfg[d.name]["prices_checked"]
        return datetime.datetime.strptime(cfg[d.name]["updated"], "%B %d, %Y").strftime("%B %Y")
    except (OSError, KeyError, ValueError):
        return datetime.date.today().strftime("%B %Y")


OWN_LABEL = re.compile(r"([^:.;]{3,48}):\s+(.+)", re.S)


def owners_line(text):
    """A card's owner-themes line. A field that opens with its own label ("Our own analysis, not owner reviews: …",
    "Praise in 2026 reviews: …") keeps it; any other is labelled "What owners and testers say". Never "From the reviews":
    on a card with an Amazon button that reads as Amazon customer reviews, which the Associates rules keep off the page."""
    m = OWN_LABEL.match(text)
    if m:
        return f"<strong>{esc(m.group(1))}:</strong> {esc(m.group(2))}"
    return f"<strong>What owners and testers say:</strong> {esc(text)}"


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
<li>{owners_line(c["owners"])}</li>
</ul>
{cta(c, "See today's price on Amazon")}
</div>
</div>'''

WATCH = ('<div class="vp-watch" id="watch-{cid}" style="margin:16px -18px -18px;padding:14px 18px 18px;border-top:1px solid #e3e3e3;background:#F7F5F0;border-radius:0 0 9px 9px;">'
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

def pick_cta(c, label):
    """The round-arrow call to action every pick card ends with (the big button is the top pick's alone)."""
    rel = c.get("rel", "nofollow sponsored noopener" if is_paid(c) else "nofollow noopener")
    return ('<div class="vp-lc-cta" style="display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;">'
            f'<a href="{esc(c["cta"]).replace("&amp;amp;","&amp;")}" rel="{rel}" target="_blank" style="display:inline-flex;align-items:center;gap:10px;'
            f'color:#1B2A41;font-weight:700;font-size:16px;line-height:1.25;text-decoration:none;">{esc(c.get("cta_label", label))}'
            '<span class="vp-go" style="display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto;width:40px;height:40px;'
            f'border-radius:50%;background:#1E8E5A;box-shadow:0 2px 6px rgba(16,24,40,.22);">{LC.ARROW}</span></a>'
            + (LC.PAID if is_paid(c) else "") + '</div>')

def pick_card(d, c, n, with_video=True, in_grid=False):
    """One pick: the render, a light pill, the name, the price line in colour, who should buy or skip it, what owners say,
    then the round-arrow call to action and the video panel, both held at the bottom of the card so cards side by side line
    up. The call to action follows the owners line, never the video note: a price there would read as Amazon's. Cards that
    follow each other share a grid (pick_grid), where the text runs a size smaller."""
    vid = card_video(d, c) if (c.get("video") and with_video) else ""
    size = "font-size:17px;" if in_grid else ""
    return f'''<div class="vp-card" id="card-{c["id"]}" style="display:flex;flex-direction:column;min-width:0;box-sizing:border-box;{size}border:1px solid #DDE3EA;border-left:5px solid #1E8E5A;border-radius:14px;padding:18px;background:#fff;margin:{"0" if in_grid else "1.2em 0"};box-shadow:0 1px 3px rgba(16,24,40,.05);">
<div style="display:flex;flex-wrap:wrap;gap:18px;align-items:center;">
<div style="flex:1 1 240px;min-width:0;max-width:420px;">{card_svg(d, c["id"])}</div>
<div style="flex:1.4 1 280px;min-width:0;">
<span style="display:inline-block;font-size:13px;font-weight:700;line-height:1.45;padding:3px 11px;border-radius:999px;background:#E6F4EC;color:#146C43;">{n}. {esc(c["badge"])}</span>
<h3 style="font-size:{"1.3em" if in_grid else "1.45em"};line-height:1.22;margin:.35em 0 .2em;color:#1B2A41;">{esc(c["name"])}</h3>
<p style="font-size:1.05em;font-weight:700;line-height:1.45;color:#146C43;margin:0 0 .5em;">{esc(c["price"])}</p>
<ul style="margin:0;padding-left:20px;font-size:.95em;">
<li style="margin-bottom:.35em;"><strong>Buy it if</strong> {esc(c["buy_if"])}</li>
<li style="margin-bottom:.35em;"><strong>Skip it if</strong> {esc(c["skip_if"])}</li>
<li>{owners_line(c["owners"])}</li>
</ul>
</div>
</div>
<div style="margin-top:auto;padding-top:14px;">{pick_cta(c, "Check the price on Amazon")}{vid}</div>
</div>'''

def pick_grid(d, items):
    """Picks that follow each other: two to a row where they fit, one on a phone. items = [(card, number, with_video)]."""
    if len(items) == 1:
        c, n, v = items[0]
        return pick_card(d, c, n, with_video=v)
    return LC.grid([pick_card(d, c, n, with_video=v, in_grid=True) for c, n, v in items], min_px=300, margin="1.2em 0 1.4em")

BAND = re.compile(r"(?:(?:about|under|roughly|usually|around|from|often|list(?: price)?)\s+)?\$[\d,.]+(?:\s*(?:–|-|to)\s*\$[\d,.]+)?"
                  r"(?:\s+(?:on sale|list|a month|for the pair|for four|for one))?", re.I)

QUALIFIED = re.compile(r"\b(?:about|under|roughly|usually|around|from|often|list|on sale|real deal|tier|free|mid-range)\b|\$[\d,.]+\s*(?:–|-|to)\s*\$", re.I)

def price_band(price):
    """The short price on a link card: the price line's first part ("About $50 ($49.99 at LUXE…)" → "About $50"), or just
    its leading band when that part is a sentence ("About $14–$18 at Target and Walmart for…" → "About $14–$18").
    A bare figure keeps its source ("$699 direct at litter-robot.com…"): next to an Amazon button, an unqualified number
    would read as Amazon's price."""
    first = re.split(r" · |; ", price.strip())[0].strip().rstrip(",.")
    s = re.split(r" \(", first)[0].strip()
    if len(s) > 40:
        m = BAND.search(s)
        if m:
            s = m.group(0)
    if not QUALIFIED.search(s):
        s = first
    return s[:1].upper() + s[1:]

def price_meta(d, c):
    """The small line on a product link card: price band · where · when ("About $50 · US retailers, Oct 2026"). It never
    sits next to the word Amazon: the band is what US retailers charged, and the button shows Amazon's price of the day."""
    band = price_band(c["price"])
    where = "" if re.search(r"\b(at|direct|from)\b .*\b[A-Z]|\.com\b", band) else "US retailers, "
    return f"{esc(band)} · {where}{esc(card_month(d))}"

def card_month(d):
    """"Oct 2026" for the small line on a link card."""
    import datetime
    try:
        return datetime.datetime.strptime(checked_month(d), "%B %Y").strftime("%b %Y")
    except ValueError:
        return checked_month(d)

def thumb(d, cid):
    f = d / "images" / "cards" / f"{cid}.svg"
    return LC.art_thumb(f.read_text(encoding="utf-8")) if f.exists() else ""

def product_link_card(d, c, *, pill="", highlight="", detail="", label=None, size=(120, 80)):
    """A card from cards.json as a link card: the render, the price band and the month the prices were checked."""
    return LC.card(esc(c["name"]), html.unescape(html.unescape(c["cta"])), img=thumb(d, c["id"]), pill=esc(pill),
                   highlight=highlight, detail=detail, meta=price_meta(d, c),
                   cta=esc(label or "See today's price"), paid=is_paid(c),
                   rel=c.get("rel", "nofollow sponsored noopener" if is_paid(c) else "nofollow noopener"), thumb=size)

def buy_box(d, cards):
    """<!--BUYBOX--> : the exact version to order of every card that carries a `buy` dict
    ({"pick": "which variant/size", "check": "what to confirm on the listing", "tier": "Good", "label": "button text"}), as link
    cards two to a row, under a heading line and above the total line from spec["buy_total"].
    spec["buy_kicker"] replaces the small heading line when the box holds one pick rather than every pick."""
    spec = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    picks = [c for c in cards if c.get("buy")]
    size = (168, 112) if len(picks) == 1 else (120, 80)
    items = [product_link_card(d, c, pill=c["buy"].get("tier", ""), highlight=f'Pick: {esc(c["buy"]["pick"])}',
                               detail=f'<strong>Check:</strong> {esc(c["buy"]["check"])}', label=c["buy"].get("label", "See today's price"), size=size)
             for c in picks]
    total = spec.get("buy_total", "")
    return (f'<div class="vp-buybox" id="buy-box" style="border:2px solid #1B2A41;border-radius:16px;overflow:hidden;background:#fff;margin:1.6em 0;">'
            f'<div style="display:flex;align-items:center;gap:12px;padding:14px 18px;background:#1B2A41;color:#fff;">'
            f'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#9fd9b9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.8a2 2 0 0 0 2-1.5L21 8H7"/><circle cx="10" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/></svg>'
            f'<div><div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#9fd9b9;">{esc(spec["buy_kicker"]) if spec.get("buy_kicker") else "Buy box &middot; every pick on this page"}</div>'
            f'<div style="font-size:18px;font-weight:700;line-height:1.25;">{esc(spec.get("buy_title", "The exact version to order, one tap each"))}</div></div></div>'
            f'<div style="padding:14px;background:#F7F5F0;">{LC.grid(items, margin="0")}</div>'
            + (f'<div style="padding:12px 18px 14px;border-top:1px solid #e6e6e6;background:#fff;font-size:14px;color:#444;line-height:1.5;">{total}</div>' if total else "") +
            '</div>')

LIST_RE = re.compile(r'<(ul|ol)\b[^>]*class="vp-linkcards"[^>]*>(.*?)</\1>', re.S)

def match_card(cards, item):
    """The cards.json entry a list item points at: the same link, else the same product name."""
    href = html.unescape(item["href"])
    for c in cards:
        if href and html.unescape(html.unescape(c.get("cta", ""))) == href:
            return c
    name = LC.text_of(item["name"]).lower()
    for c in cards:
        if name and (name == c["name"].lower() or name == c.get("short", "").lower() or c["name"].lower().startswith(name)):
            return c
    return None

def linkcard_lists(d, cards, text):
    """Lists the writer marked <ul class="vp-linkcards"> become link cards, two or three to a row: product links (with the
    render when the product has a card), links to our own guides (from the site index), and link-less notes ("Skip", "Wait")."""
    def convert(m):
        items = []
        index = None
        for li in re.findall(r"<li\b[^>]*>(.*?)</li>", m.group(2), re.S):
            it = LC.parse_item(li)
            href = it["href"]
            internal = href.startswith("/") or href.startswith(LC.SITE)
            if internal:
                if index is None:
                    import site_index
                    index = site_index.build_index()
                path = href.replace(LC.SITE, "").split("#")[0]
                p = next((p for p in index if p["url"].replace(LC.SITE, "") == path), None)
                sentence = esc(LC.sentence(LC.text_of(re.sub(LC.A_TAG, lambda x: x.group(2), li))))
                if p:
                    items.append(LC.guide_card(p, highlight=sentence))
                else:   # not live yet: a card without the picture
                    items.append(LC.card(esc(LC.text_of(it["name"])), path, highlight=sentence, cta="Read the guide", palette=LC.GUIDE, name_href=path))
                continue
            if not href:   # "Skip", "Avoid", "Wait": a note card without a call to action
                body = (PILL_RE.sub("", li, count=1)).strip()
                items.append(LC.card("", None, pill=esc(it["pill"]), highlight=body, palette=LC.WARN if LC.WARN_PILL.match(it["pill"]) else LC.PRODUCT))
                continue
            c = match_card(cards, it)
            hl, det = LC.split_highlight(it["text"])
            spec = esc(it["spec"]) if it["spec"] else ""
            detail = " · ".join(x for x in (spec, det) if x)
            items.append(LC.card(it["name"], href, img=thumb(d, c["id"]) if c else "", pill=esc(it["pill"]), highlight=LC.sentence(hl), detail=LC.sentence(det) if not spec else detail,
                                 meta=price_meta(d, c) if c else "",
                                 cta="See today's price" if "amazon." in href else esc(it["label"] or "See it"), paid="amazon." in href))
        guides = all('class="vp-lc"' in x and "Read the guide" in x for x in items)
        return LC.grid(items, guides=guides)
    parts = re.split(r"(<!--.*?-->)", text, flags=re.S)          # a list inside a comment (a template example) stays as written
    return "".join(x if x.startswith("<!--") else LIST_RE.sub(convert, x) for x in parts)

PILL_RE = re.compile(r'^\s*<span\b[^>]*border-radius:999px[^>]*>.*?</span>\s*', re.S)

# Ways to follow the blog. "email" stays empty until the newsletter list exists; the button is then added everywhere on rebuild.
FOLLOW = {"email": "", "blogger": "https://www.blogger.com/follow.g?blogID=9072207571822466986",
          "rss": "https://acts39.blogspot.com/feeds/posts/default", "youtube": "https://www.youtube.com/@ubuntu29", "page": "/p/follow-verdict-picks.html"}

def follow_block():
    """The follow box that closes every post: email (when the list exists), Blogger's native follow, the feed, YouTube."""
    btn = 'display:inline-block;text-decoration:none;font-weight:700;font-size:15px;padding:10px 16px;border-radius:9px;'
    buttons = []
    if FOLLOW["email"]:
        buttons.append(f'<a href="{FOLLOW["email"]}" rel="noopener" target="_blank" style="{btn}background:#1E8E5A;color:#fff;">Email me new guides</a>')
    buttons.append(f'<a href="{FOLLOW["blogger"]}" rel="noopener" target="_blank" style="{btn}background:#1B2A41;color:#fff;">Follow on Blogger</a>')
    buttons.append(f'<a href="{FOLLOW["rss"]}" rel="noopener" target="_blank" style="{btn}background:#fff;color:#1B2A41;border:2px solid #1B2A41;">RSS feed</a>')
    buttons.append(f'<a href="{FOLLOW["youtube"]}" rel="noopener" target="_blank" style="{btn}background:#fff;color:#1B2A41;border:2px solid #1B2A41;">YouTube</a>')
    return ('<div class="vp-follow" id="follow" style="border:2px solid #1B2A41;border-radius:16px;padding:18px 20px;background:#F7F5F0;margin:1.6em 0;">'
            '<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#1E8E5A;">Follow Verdict Picks</div>'
            '<h3 style="margin:.3em 0 .4em;color:#1B2A41;font-size:1.3em;">Get the next guide when it lands</h3>'
            '<p style="margin:0 0 .9em;font-size:16px;color:#333;">A new guide most days: researched picks only, no sale pitches. Pick the way you like to follow:</p>'
            '<div style="display:flex;flex-wrap:wrap;gap:10px;">' + "".join(buttons) + '</div>'
            f'<p style="margin:.8em 0 0;font-size:13px;color:#666;">Every option explained, and what we will never send: <a href="{FOLLOW["page"]}" style="color:#1B2A41;font-weight:700;">the follow page</a>.</p></div>\n')

def main(post_dir):
    d = pathlib.Path(post_dir)
    spec = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    cards = spec["cards"]; by_id = {c["id"]: c for c in cards}
    easy = (d / "src" / "00-easy.html").read_text(encoding="utf-8")
    easy = responsive_grid(easy)
    easy = easy.replace('<div class="vp-post"', STYLE + '<div class="vp-post"', 1)
    strip = ('<p class="vp-nav" style="font-size:15px;margin:0 0 .8em;color:#555;"><strong style="color:#1B2A41;">Guides:</strong> '
             '<a href="/p/robot-vacuums.html" style="color:#1B2A41;">Robot Vacuums</a> · <a href="/p/wireless-earbuds.html" style="color:#1B2A41;">Wireless Earbuds</a> · '
             '<a href="/p/smart-glasses.html" style="color:#1B2A41;">Smart Glasses</a> · <a href="/p/power-stations.html" style="color:#1B2A41;">Power Stations</a> · <a href="/p/best-sellers.html" style="color:#1B2A41;">Best Sellers</a> · <a href="/p/follow-verdict-picks.html" style="color:#1E8E5A;font-weight:700;">Follow</a></p>\n')
    easy = easy.replace('<div class="vp-post" style="font-size:19px;line-height:1.6;color:#222;">', '<div class="vp-post" style="font-size:19px;line-height:1.6;color:#222;">\n' + strip, 1)
    notice = ('<p class="vp-notice" style="font-size:16px;background:#F7F5F0;border-left:5px solid #1B2A41;padding:10px 14px;margin:0 0 1.2em;">'
              '<strong>Two ways to read this.</strong> In a hurry: the quick guide starts right here — one pick, a 10-second picker, every product in 30 seconds. '
              'Have twenty minutes: the <a href="#deep" style="color:#1B2A41;font-weight:700;">complete deep-dive</a> follows on this same page — how we researched, every brand, every pick in detail, what long-term owners report, and when to buy.</p>\n')
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
        rel = d.resolve().relative_to(pathlib.Path(__file__).resolve().parent.parent).as_posix()   # repo-relative even when called with an absolute path
        url = cov.get("url", ""); img = f"https://actsb.github.io/claudefold/{rel}/images/pin.png"
        desc = cov.get("alt", " ".join(cov.get("title", [])))
        save = "https://pinterest.com/pin/create/button/?" + urllib.parse.urlencode({"url": url, "media": img, "description": desc})
        return (f'<div class="vp-pin" style="display:flex;flex-wrap:wrap;gap:20px;align-items:center;border:1px solid #ddd;border-radius:14px;padding:18px;background:#fff;margin:1.6em 0;">'
                f'<a href="{save}" rel="noopener nofollow" target="_blank" style="flex:0 1 220px;"><img src="{img}" alt="{html.escape(desc)}" width="1000" height="1500" style="width:100%;max-width:220px;height:auto;border-radius:10px;display:block;" loading="lazy"></a>'
                f'<div style="flex:1 1 260px;min-width:0;"><h3 style="margin:0 0 .3em;color:#1B2A41;font-size:1.25em;">Save this guide for later</h3>'
                f'<p style="margin:0 0 .8em;font-size:17px;">Pin it to your Pinterest board and it will be there when the sale hits.</p>'
                f'<a href="{save}" rel="noopener nofollow" target="_blank" style="display:inline-block;background:#E60023;color:#fff;text-decoration:none;font-weight:700;font-size:17px;padding:11px 18px;border-radius:8px;">Save to Pinterest</a></div></div>')
    easy = re.sub(r"<!--PIN-->", lambda m: pin_block(m) + follow_block(), easy)
    def strip_fig(m):
        sid, cap = m.group(1), m.group(2) or ""
        f = d / "images" / "strips" / f"{sid}.svg"
        if not f.exists(): return ""
        svg = re.sub(r"^<\?xml[^>]*\?>\s*", "", f.read_text(encoding="utf-8").strip())
        capt = f'<div style="font-size:14px;color:#555;margin-top:6px;">{cap}</div>' if cap else ""
        return f'<div class="vp-strip" style="margin:1.2em 0;">{svg}{capt}</div>'
    easy = re.sub(r"<!--STRIP:([a-z0-9\-]+)(?:\|(.*?))?-->", strip_fig, easy)
    easy = easy.replace("<!--CARDS-->", pick_grid(d, [(c, i + 1, i > 0) for i, c in enumerate(cards)]))
    # card markers that follow each other share one grid; a marker on its own stays a full-width card
    easy = re.sub(r"(?:<!--CARD:[a-z0-9\-]+-->\s*)+", lambda m: pick_grid(d, [(by_id[k], cards.index(by_id[k]) + 1, True) for k in re.findall(r"<!--CARD:([a-z0-9\-]+)-->", m.group(0))]) + "\n", easy)
    easy = linkcard_lists(d, cards, easy)
    parts = sorted(p for p in (d / "src").glob("0[1-9]-*.html"))
    if not parts:
        # short story post: no deep-dive, just close the wrapper
        out = (easy + f'<p style="font-size:15px;color:#555;"><em>As an Amazon Associate I earn from qualifying purchases. Prices and availability are those seen at US retailers at the time of writing ({checked_month(d)}), are subject to change, and the price shown on Amazon at checkout is the one that applies. We do not accept products or payment from manufacturers. <a href="/p/how-we-rank-products.html">How we rank</a> · <a href="/p/affiliate-disclosure.html">Disclosure</a></em></p>\n</div>\n')
        out = with_more_guides(d, teaser_first(label_paid_links(out)))
        (d / "post.src.html").write_text(out, encoding="utf-8")
        print(f"assembled {d/'post.src.html'} ({len(out):,} bytes, {len(cards)} cards, no deep-dive)"); return
    deep = "\n".join(p.read_text(encoding="utf-8") for p in parts)
    # strip the wrapper, byline and cover the deep-dive parts open with, and the wrapper close at the end
    deep = re.sub(r'^\s*<div class="vp-post"[^>]*>\s*<p[^>]*><em>.*?</em></p>\s*<p[^>]*><img[^>]*></p>', "", deep, count=1, flags=re.S)
    deep = re.sub(r"</div>\s*$", "", deep.rstrip(), count=1)
    deep = linkcard_lists(d, cards, deep)
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
           + '<p>The quick guide above is enough to buy well. If you want to know <em>why</em> — how we researched, what every brand does well and badly, every pick in detail, what owners report after months of use, and when to buy — the complete analysis follows. Read it in one go, or one section at a time when you have a few minutes. Each section stands on its own.</p>\n'
           + '<div class="vp-roadmap" style="border:2px solid #1B2A41;border-radius:12px;padding:14px 20px;background:#F7F5F0;margin:1em 0 1.6em;">\n<strong style="color:#1B2A41;">Reading plan</strong>\n<ol style="margin:8px 0 0;padding-left:22px;">\n' + "\n".join(items) + '\n</ol>\n</div>\n'
           + '<div class="vp-deep" style="border-top:3px solid #1B2A41;margin-top:1.4em;padding-top:1.2em;font-size:0.94em;">\n' + deep + '\n</div>\n'
           + '<p style="margin:1.6em 0 1em;"><a href="#top-pick" style="display:inline-block;background:#1B2A41;color:#fff;text-decoration:none;font-weight:700;padding:10px 16px;border-radius:8px;">↑ Back to the quick guide and the top pick</a></p>\n'
           + f'<p style="font-size:15px;color:#555;"><em>As an Amazon Associate I earn from qualifying purchases. Prices and availability are those seen at US retailers at the time of writing ({checked_month(d)}), are subject to change, and the price shown on Amazon at checkout is the one that applies. We do not accept products or payment from manufacturers. <a href="/p/how-we-rank-products.html">How we rank</a> · <a href="/p/affiliate-disclosure.html">Disclosure</a></em></p>\n'
           + '</div>\n')
    out = with_more_guides(d, teaser_first(label_paid_links(out)))
    (d / "post.src.html").write_text(out, encoding="utf-8")
    print(f"assembled {d/'post.src.html'} ({len(out):,} bytes, {len(cards)} cards)")

if __name__ == "__main__":
    main(sys.argv[1])
