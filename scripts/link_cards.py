#!/usr/bin/env python3
"""Link cards: how a page shows a set of things to click through to (products to buy, guides to read).

The rule (daily/README.md, section 0): several product or guide links are cards in a grid, two or three to a row,
never a vertical stack of full-width boxes that each end in a text link. A phone too narrow for two product cards
shows one per row; guide cards stay two per row there. Each card has:

  a coloured bar on the left · a small pill · the picture on the left · the name in bold · one highlight sentence
  in colour · a grey detail line · a small "price · checked <month>" (or "Updated <date>") line · the call to action
  with a round arrow button at the bottom.

Used by assemble_post.py (buy box, lists marked <ul class="vp-linkcards">), site_index.py (the More guides block,
the Best Sellers hub) and daily_post.py (the hub card for a new guide).
"""
import html, pathlib, re

GREEN, NAVY, ORANGE, DEEP_GREEN = "#1E8E5A", "#1B2A41", "#C9781B", "#146C43"
PAGES = "https://actsb.github.io/claudefold"
SITE = "https://acts39.blogspot.com"
PAID = '<span class="vp-paid" style="font-size:13px;color:#555;white-space:nowrap;">(paid link)</span>'
ARROW = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true" style="display:block;"><path d="M5 12h13M13 6l6 6-6 6"/></svg>')
# palettes: bar and button colour, pill background and text, highlight colour
PRODUCT = {"bar": GREEN, "pill_bg": "#E6F4EC", "pill_fg": DEEP_GREEN, "hl": DEEP_GREEN}
GUIDE = {"bar": NAVY, "pill_bg": "#E9EDF3", "pill_fg": NAVY, "hl": "#2B4A6F"}
WARN = {"bar": ORANGE, "pill_bg": "#FBEFE2", "pill_fg": "#8A4B0C", "hl": "#8A4B0C"}

# phone layout; the grid itself works from inline styles alone (feed readers drop <style>)
CSS = """.vp-lc .vp-go{transition:transform .15s}
.vp-lc a:hover .vp-go{transform:translateX(2px)}
@media (max-width:560px){
  .vp-cards{gap:10px!important}
  .vp-lc{padding:12px 12px 10px 11px!important}
  .vp-lc-top{gap:10px!important}
  .vp-lc-img{flex-basis:90px!important;width:90px!important;height:60px!important}
  .vp-lc-name{font-size:16px!important}
  .vp-lc-hl{font-size:14.5px!important}
  .vp-guides{grid-template-columns:1fr 1fr!important}
  .vp-guides .vp-lc-top{flex-direction:column!important}
  .vp-guides .vp-lc-img{flex-basis:auto!important;width:100%!important;height:auto!important}
  .vp-guides .vp-lc-name{font-size:15px!important}
  .vp-guides .vp-lc-hl{font-size:13.5px!important;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
  .vp-guides .vp-lc-meta{display:none}
  .vp-guides .vp-lc-cta a{font-size:13.5px!important;gap:8px!important;white-space:nowrap}
  .vp-guides .vp-go{width:34px!important;height:34px!important}
}
"""


def esc(s):
    return html.escape(s, quote=True)


def text_of(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def art_thumb(svg):
    """A product render as a thumbnail: no chip or name text, scaled to fill its box."""
    svg = re.sub(r"^<\?xml[^>]*\?>\s*", "", svg.strip())
    svg = re.sub(r"<g font-family=.*?</g>\s*", "", svg, flags=re.S)
    return re.sub(r"<svg ", '<svg style="width:100%;height:100%;display:block;" ', svg, count=1)


def write_thumb(d):
    """posts/<dir>/images/thumb.svg: the cover's hero render without text, for guide cards on other pages (~5 KB)."""
    import json
    d = pathlib.Path(d)
    cov = json.loads((d / "cover.json").read_text(encoding="utf-8")) if (d / "cover.json").exists() else {}
    cards = json.loads((d / "cards.json").read_text(encoding="utf-8"))["cards"] if (d / "cards.json").exists() else []
    for cid in [cov.get("hero")] + [c["id"] for c in cards]:
        f = d / "images" / "cards" / f"{cid}.svg"
        if cid and f.exists():
            svg = re.sub(r"<g font-family=.*?</g>\s*", "", f.read_text(encoding="utf-8"), flags=re.S)
            out = d / "images" / "thumb.svg"
            if not out.exists() or out.read_text(encoding="utf-8") != svg:
                out.write_text(svg, encoding="utf-8")
            return out
    return None


def img_box(inner, w=120, h=80, href=None):
    style = (f'flex:0 0 {w}px;width:{w}px;height:{h}px;border-radius:10px;overflow:hidden;background:#F4F2EC;')
    if href:   # the picture repeats the title link: keep it out of the tab order and the screen-reader list
        return f'<a class="vp-lc-img" href="{esc(href)}" tabindex="-1" aria-hidden="true" style="display:block;{style}">{inner}</a>'
    return f'<div class="vp-lc-img" style="{style}">{inner}</div>'


def card(name, href=None, *, img="", pill="", highlight="", detail="", meta="", cta="See today's price", paid=None,
         rel=None, palette=PRODUCT, name_href=None, attrs="", thumb=(120, 80)):
    """One link card. `img` is inline SVG or an <img>; `href` None makes a note card without a call to action."""
    bar, pill_bg, pill_fg = palette["bar"], palette["pill_bg"], palette["pill_fg"]
    paid = ("amazon." in (href or "")) if paid is None else paid
    if rel is None:
        rel = "nofollow sponsored noopener" if paid else ("" if (href or "").startswith(("/", SITE)) else "nofollow noopener")
    out_attrs = (f' rel="{rel}"' if rel else "") + (' target="_blank"' if rel else "")
    pill_html = (f'<span class="vp-pill" style="display:inline-block;vertical-align:2px;margin:0 7px 3px 0;font-size:12px;font-weight:700;'
                 f'line-height:1.45;letter-spacing:.01em;padding:2px 9px;border-radius:999px;background:{pill_bg};color:{pill_fg};">{pill}</span>') if pill else ""
    name_html = (f'<a href="{esc(name_href)}" style="color:{NAVY};text-decoration:none;">{name}</a>' if name_href else name)
    body = (f'<div class="vp-lc-name" style="font-size:17px;font-weight:700;line-height:1.35;color:{NAVY};">{pill_html}{name_html}</div>'
            + (f'<div class="vp-lc-hl" style="margin-top:5px;font-size:15px;font-weight:700;line-height:1.5;color:{palette["hl"]};">{highlight}</div>' if highlight else "")
            + (f'<div class="vp-lc-detail" style="margin-top:4px;font-size:14px;line-height:1.5;color:#555;">{detail}</div>' if detail else "")
            + (f'<div class="vp-lc-meta" style="margin-top:4px;font-size:13px;line-height:1.45;color:#8A8F98;">{meta}</div>' if meta else ""))
    top = ('<div class="vp-lc-top" style="display:flex;gap:14px;align-items:flex-start;">'
           + (img_box(img, *thumb, href=name_href) if img else "")
           + f'<div class="vp-lc-body" style="flex:1 1 auto;min-width:0;">{body}</div></div>')
    action = ""
    if href:
        action = ('<div class="vp-lc-cta" style="margin-top:auto;display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;">'
                  f'<a href="{esc(href)}"{out_attrs} style="display:inline-flex;align-items:center;gap:10px;color:{NAVY};font-weight:700;'
                  f'font-size:15px;line-height:1.2;text-decoration:none;">{cta}<span class="vp-go" style="display:inline-flex;align-items:center;'
                  f'justify-content:center;flex:0 0 auto;width:38px;height:38px;border-radius:50%;background:{bar};'
                  f'box-shadow:0 2px 6px rgba(16,24,40,.22);">{ARROW}</span></a>' + (PAID if paid else "") + '</div>')
    return (f'<div class="vp-lc"{attrs} style="display:flex;flex-direction:column;gap:12px;min-width:0;box-sizing:border-box;'
            f'background:#fff;border:1px solid #DDE3EA;border-left:5px solid {bar};border-radius:14px;padding:14px 16px 12px 14px;'
            f'box-shadow:0 1px 3px rgba(16,24,40,.05);">{top}{action}</div>')


def grid(cards, guides=False, min_px=300, margin="1em 0 1.4em"):
    """Two or three to a row where they fit (min_px each); one to a row below that. Guide grids stay two to a row on phones."""
    cls = "vp-cards vp-guides" if guides else "vp-cards"
    return (f'<div class="{cls}" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,{min_px}px),1fr));'
            f'gap:14px;margin:{margin};">' + "".join(cards) + '</div>')


# --- guides ------------------------------------------------------------------------------------------------------------

def short_title(t):
    """The part of a post title before the colon reads better on a card."""
    return t.split(":")[0].strip() if ":" in t and len(t.split(":")[0]) >= 18 else t


def guide_kind(labels):
    ls = {l.lower() for l in labels}
    if "deals" in ls or "prime day" in ls:
        return "Deal guide"
    if "workflow guide" in ls:
        return "How-to"
    if "review" in ls:
        return "Review"
    return "Buying guide" if "buying guide" in ls else "Guide"


def sentence(s):
    s = (s or "").strip()
    return s[:1].upper() + s[1:] if s else s


def guide_card(p, highlight=None, title=None, attrs=""):
    """A card for one live guide from brand/site-index.json (key, title, url, description, labels, dir, blurb, updated)."""
    href = p["url"].replace(SITE, "") or "/"
    img = (f'<img src="{PAGES}/{p["dir"]}/images/thumb.svg" alt="" width="600" height="400" loading="lazy" '
           'style="display:block;width:100%;height:100%;object-fit:cover;border:0;margin:0;padding:0;box-shadow:none;border-radius:0;background:none;">')
    hl = highlight if highlight is not None else esc(sentence(p.get("blurb") or p["description"]))
    return card(esc(title or short_title(p["title"])), href, img=img, pill=guide_kind(p.get("labels", [])), highlight=hl,
                meta=f'Updated {esc(p["updated"])}' if p.get("updated") else "", cta="Read the guide", palette=GUIDE,
                name_href=href, attrs=attrs)


def guide_grid(entries, **kw):
    return grid([guide_card(p, **kw) for p in entries], guides=True)


# --- lists in post sources: <ul class="vp-linkcards"> ------------------------------------------------------------------

PILL_SPAN = re.compile(r'^\s*<span\b[^>]*border-radius:999px[^>]*>(.*?)</span>\s*', re.S)
PILL_STRONG = re.compile(r'^\s*<strong>([^<]{1,40}?):</strong>\s*', re.S)
A_TAG = re.compile(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S)
GENERIC = re.compile(r"^(see|check|shop|view|compare|get)\b.*\b(amazon|price|deal|deals|it)\b", re.I)
WARN_PILL = re.compile(r"^(skip|avoid|wait)", re.I)


def split_highlight(text, limit=150):
    """First clause as the highlight, the rest as the detail line. `text` may hold inline HTML (a second link, <em>): the
    split never falls inside a tag, and `limit` counts visible characters."""
    t = text.strip()
    for m in re.finditer(r"(?<=[^\s])(:|;|\.)\s+(?=\S)|\s+—\s+", t):
        before = t[:m.start()]
        if before.count("<") != before.count(">"):          # inside a tag's attributes
            continue
        if len(text_of(before)) < 14:
            continue
        if len(text_of(before)) > limit:
            break
        return before + ("." if m.group(0).strip() == "." else ""), t[m.end():].strip()
    return t, ""


def parse_item(li):
    """<li> → dict(pill, name, spec, text, href, label) from the house list style:
    [pill span or <strong>Label:</strong>] <strong>Name</strong> (spec) — text <a href>See on Amazon</a>
    or [<strong>Label:</strong>] the <a href>Name</a> (spec) — text."""
    item = {"pill": "", "name": "", "spec": "", "text": "", "href": "", "label": ""}
    m = PILL_SPAN.match(li) or PILL_STRONG.match(li)
    if m:
        item["pill"], li = text_of(m.group(1)), li[m.end():]
    links = list(A_TAG.finditer(li))
    if links:
        item["href"] = html.unescape(links[0].group(1))
    m = re.match(r"\s*<strong>(.*?)</strong>\s*", li, re.S)
    if m and not m.group(1).rstrip().endswith(":"):
        item["name"], rest = m.group(1).strip(), li[m.end():]
    elif links and not GENERIC.match(text_of(links[0].group(2))):
        a = links[0]
        lead = li[:a.start()]
        if text_of(lead).lower() in ("", "the", "a", "an", "our"):
            item["name"], rest = a.group(2).strip(), li[a.end():]
        else:   # the link sits inside a sentence: the whole sentence is the text, the link text the name
            item["name"], rest = a.group(2).strip(), re.sub(A_TAG, lambda x: x.group(2), li)
            item["href"] = html.unescape(a.group(1))
    else:
        rest = li
    if links and GENERIC.match(text_of(links[0].group(2))):
        item["label"] = text_of(links[0].group(2))
        rest = rest.replace(links[0].group(0), "")
    m = re.match(r"\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)\s*", rest)
    if m:
        item["spec"], rest = m.group(1).strip(), rest[m.end():]
    m = re.search(r"\s*\(([^()]*\$[^()]*)\)\s*$", item["name"])   # "Name ($799 list; $399–$599 on sale)"
    if m and not item["spec"]:
        item["spec"], item["name"] = m.group(1).strip(), item["name"][:m.start()].strip()
    rest = re.sub(r"^\s*[—–-]\s*", "", rest).strip()
    item["text"] = re.sub(r"\s+", " ", rest).strip()
    return item
