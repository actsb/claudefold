#!/usr/bin/env python3
"""Site index and "More guides" links between posts.

  python3 scripts/site_index.py            # rebuild brand/site-index.json from publish_blogger.py and daily/search-descriptions.md
  python3 scripts/site_index.py --inject   # also refresh the "More guides" block in every built post (post.html, post.src.html)
  python3 scripts/site_index.py --hub      # also re-render the guide cards on the Best Sellers hub (brand/pages/hub-best-sellers.html)

Only published posts are indexed: a post enters daily/search-descriptions.md (title, URL, description) when it goes live.
Related posts are the ones that share the most topic labels; ties go to the newest. Generic labels (Best Sellers, Review,
price bands…) do not count, so a pillow guide is not "related" to a jump starter just because both are under $50.
"""
import ast, html, json, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import link_cards as LC

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "brand" / "site-index.json"
HUB = ROOT / "brand" / "pages" / "hub-best-sellers.html"
GENERIC = {"amazon finds", "best sellers", "review", "product of the day", "buying guide", "gifts", "premium",
           "for creators", "workflow guide", "small business"}
GENERIC_RE = re.compile(r"^under \$\d", re.I)


def publisher_posts():
    src = (ROOT / "scripts" / "publish_blogger.py").read_text(encoding="utf-8")
    i = src.index("POSTS = {"); j = src.index("\n}\n", i)
    return ast.literal_eval(src[i + len("POSTS = "):j + 2])


HUB_CARD = re.compile(r'^<div class="vp-lc" data-guide="([^"]+)".*$', re.M)


def card_line(line):
    """(title, blurb) of one hub card line: the title as text, the blurb as the HTML it was written in."""
    name = re.search(r'<div class="vp-lc-name"[^>]*>(?:<span class="vp-pill"[^>]*>.*?</span>)?<a [^>]*>(.*?)</a></div>', line)
    hl = re.search(r'<div class="vp-lc-hl"[^>]*>(.*?)</div>', line)
    return (html.unescape(name.group(1)) if name else "", hl.group(1) if hl else "")


def hub_cards(text=None):
    """{key: (title, blurb)} from the Best Sellers hub: one card per line, written by daily_post.py and render_hub()."""
    text = HUB.read_text(encoding="utf-8") if text is None else text
    return {m.group(1): card_line(m.group(0)) for m in HUB_CARD.finditer(text)}


def build_index():
    """[{key, title, url, description, labels, dir, blurb, updated}] for every post that is live, newest first.
    blurb: the post's one line on the Best Sellers hub (more readable on a card than the search description)."""
    text = (ROOT / "daily" / "search-descriptions.md").read_text(encoding="utf-8")
    live = {}
    for m in re.finditer(r"^## ([^\n]+)\n+(https://\S+)\n+```text\n(.+?)\n```", text, re.M | re.S):
        live[m.group(1).strip()] = (m.group(2).strip(), m.group(3).strip())
    cfg = json.loads((ROOT / "brand" / "seo-configs.json").read_text(encoding="utf-8"))
    blurbs = hub_cards() if HUB.exists() else {}
    out = []
    for key, P in reversed(list(publisher_posts().items())):        # publisher order is oldest first
        if P["title"] in live:
            url, desc = live[P["title"]]
            e = {"key": key, "title": P["title"], "url": url, "description": desc, "labels": P["labels"], "dir": P["dir"]}
            blurb = html.unescape(blurbs.get(key, ("", ""))[1])
            if blurb and "WRITE" not in blurb:
                e["blurb"] = blurb
            upd = cfg.get(pathlib.Path(P["dir"]).name, {}).get("updated")
            if upd:
                e["updated"] = upd
            out.append(e)
    return out


def topics(labels):
    return {l.lower() for l in labels if l.lower() not in GENERIC and not GENERIC_RE.match(l)}


def related(post_dir, index, n=4):
    """The n live posts closest to the post in post_dir (by shared topic labels, then recency), excluding itself."""
    me = next((p for p in index if p["dir"] == post_dir), None)
    mine = topics(me["labels"]) if me else set()
    if not me:   # a post that is not live yet: use its publisher labels
        P = next((P for P in publisher_posts().values() if P["dir"] == post_dir), None)
        mine = topics(P["labels"]) if P else set()
    pool = [(len(mine & topics(p["labels"])), -i, p) for i, p in enumerate(index) if p["dir"] != post_dir]
    pool.sort(key=lambda t: (t[0], t[1]), reverse=True)
    return [p for _, _, p in pool[:n]]


def block(post_dir, index, n=4):
    """The "More guides" block: the n closest live guides as cards, two to a row (scripts/link_cards.py)."""
    picks = related(post_dir, index, n)
    if not picks:
        return ""
    return ('<div class="vp-related" id="more-guides" style="margin:1.6em 0;">'
            '<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#1E8E5A;margin:0 0 .5em;">More guides from Verdict Picks</div>'
            + LC.guide_grid(picks) + '</div><!--/more-guides-->\n')


# the block as written now (ends with its own marker) or as written before October 2026 (a list)
BLOCK_RE = re.compile(r'<div class="vp-related" id="more-guides".*?(?:<!--/more-guides-->|</ul></div>)\n?', re.S)
ANCHOR = '<div class="vp-pin"'


def inject(text, blk):
    """Replace the existing block, or put it just before the Pinterest box. Unchanged text when there is no anchor."""
    if BLOCK_RE.search(text):
        return BLOCK_RE.sub(lambda m: blk, text, count=1)
    i = text.find(ANCHOR)
    return text if i < 0 or not blk else text[:i] + blk + text[i:]


def grid_open():
    """The opening tag of a hub cluster's card grid (the cards follow its CLUSTER marker, one per line)."""
    return LC.grid([], guides=True, margin=".6em 0 1.2em").replace("</div>", "")


def hub_card(key, title, blurb, index=None):
    """One hub card, on one line. A guide that is not live yet (no index entry) uses its publisher entry."""
    index = build_index() if index is None else index
    p = next((p for p in index if p["key"] == key), None)
    if not p:
        P = publisher_posts()[key]
        cfg = json.loads((ROOT / "brand" / "seo-configs.json").read_text(encoding="utf-8")).get(pathlib.Path(P["dir"]).name, {})
        p = {"key": key, "title": P["title"], "url": P.get("url") or cfg.get("url", ""), "description": "", "labels": P["labels"],
             "dir": P["dir"], **({"updated": cfg["updated"]} if cfg.get("updated") else {})}
    return LC.guide_card(p, highlight=blurb, title=title, attrs=f' data-guide="{html.escape(key)}"')


def render_hub(text):
    """Best Sellers hub: guide cards two or three to a row in every cluster. Converts the lists the hub used before October
    2026 (<ul> + <li><a>Title</a> — blurb</li>) and re-renders existing cards from their title and blurb."""
    by_path = {P["url"].replace(LC.SITE, ""): k for k, P in publisher_posts().items() if P.get("url")}
    index = build_index()
    def legacy_list(m):
        lines = []
        for li in re.findall(r"<li\b[^>]*>(.*?)</li>", m.group(2), re.S):
            a = re.search(r'<a href="([^"]+)"[^>]*>(.*?)</a>\s*[—–-]\s*(.*)$', li.strip(), re.S)
            key = by_path.get(a.group(1)) if a else None
            if not key:
                raise SystemExit(f"hub: no publisher entry for {li[:80]}")
            lines.append(hub_card(key, html.unescape(a.group(2).strip()), LC.sentence(a.group(3).strip()), index))
        return grid_open() + "\n" + m.group(1) + "".join(l + "\n" for l in lines) + "</div>"
    text = re.sub(r'<ul style="padding-left:22px;">\n(<!--CLUSTER:[a-z]+-->\n)(.*?)</ul>', legacy_list, text, flags=re.S)
    text = HUB_CARD.sub(lambda m: hub_card(m.group(1), *card_line(m.group(0)), index), text)
    style = "<style>\n" + LC.CSS + "</style>\n"
    if "<style>" in text:
        text = re.sub(r"<style>\n.*?</style>\n", lambda m: style, text, count=1, flags=re.S)
    else:
        i = text.index("-->") + 4                                     # after the header comment
        text = text[:i] + style + text[i:]
    return text


def main():
    index = build_index()
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{INDEX.relative_to(ROOT)}: {len(index)} live posts")
    for P in publisher_posts().values():                              # the picture on every guide card
        if (ROOT / P["dir"] / "cards.json").exists():
            LC.write_thumb(ROOT / P["dir"])
    if "--hub" in sys.argv:
        new = render_hub(HUB.read_text(encoding="utf-8"))
        HUB.write_text(new, encoding="utf-8")
        print(f"{HUB.relative_to(ROOT)}: {len(HUB_CARD.findall(new))} guide cards")
    if "--inject" in sys.argv:
        changed = []
        for P in publisher_posts().values():
            blk = block(P["dir"], index)
            for name in ("post.html", "post.src.html"):
                f = ROOT / P["dir"] / name
                if f.exists():
                    t = f.read_text(encoding="utf-8"); new = inject(t, blk)
                    if new != t:
                        f.write_text(new, encoding="utf-8"); changed.append(f"{P['dir']}/{name}")
        print(f"More-guides block refreshed in {len(changed)} files")


if __name__ == "__main__":
    main()
