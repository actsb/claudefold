#!/usr/bin/env python3
"""Site index and "More guides" links between posts.

  python3 scripts/site_index.py            # rebuild brand/site-index.json from publish_blogger.py and daily/search-descriptions.md
  python3 scripts/site_index.py --inject   # also refresh the "More guides" block in every built post (post.html, post.src.html)

Only published posts are indexed: a post enters daily/search-descriptions.md (title, URL, description) when it goes live.
Related posts are the ones that share the most topic labels; ties go to the newest. Generic labels (Best Sellers, Review,
price bands…) do not count, so a pillow guide is not "related" to a jump starter just because both are under $50.
"""
import ast, html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "brand" / "site-index.json"
GENERIC = {"amazon finds", "best sellers", "review", "product of the day", "buying guide", "gifts", "premium",
           "for creators", "workflow guide", "small business"}
GENERIC_RE = re.compile(r"^under \$\d", re.I)


def publisher_posts():
    src = (ROOT / "scripts" / "publish_blogger.py").read_text(encoding="utf-8")
    i = src.index("POSTS = {"); j = src.index("\n}\n", i)
    return ast.literal_eval(src[i + len("POSTS = "):j + 2])


def build_index():
    """[{key, title, url, description, labels, dir}] for every post that is live, newest first."""
    text = (ROOT / "daily" / "search-descriptions.md").read_text(encoding="utf-8")
    live = {}
    for m in re.finditer(r"^## (.+?)\n\n(https://\S+)\n\n```text\n(.+?)\n```", text, re.M | re.S):
        live[m.group(1).strip()] = (m.group(2).strip(), m.group(3).strip())
    out = []
    for key, P in reversed(list(publisher_posts().items())):        # publisher order is oldest first
        if P["title"] in live:
            url, desc = live[P["title"]]
            out.append({"key": key, "title": P["title"], "url": url, "description": desc, "labels": P["labels"], "dir": P["dir"]})
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
    picks = related(post_dir, index, n)
    if not picks:
        return ""
    def short(t):   # the part of the title before the colon reads better as a link
        return t.split(":")[0].strip() if ":" in t and len(t.split(":")[0]) >= 18 else t
    items = "".join(
        f'<li style="margin:0 0 .7em;"><a href="{html.escape(p["url"].replace("https://acts39.blogspot.com", ""))}" style="color:#1B2A41;font-weight:700;">{html.escape(short(p["title"]))}</a>'
        f'<br><span style="font-size:15px;color:#555;">{html.escape(p["description"])}</span></li>' for p in picks)
    return ('<div class="vp-related" id="more-guides" style="border:1px solid #ddd;border-radius:14px;padding:16px 20px;background:#fff;margin:1.6em 0;">'
            '<div style="font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#1E8E5A;">More guides from Verdict Picks</div>'
            f'<ul style="margin:.6em 0 0;padding-left:20px;font-size:17px;">{items}</ul></div>\n')


BLOCK_RE = re.compile(r'<div class="vp-related" id="more-guides".*?</ul></div>\n?', re.S)
ANCHOR = '<div class="vp-pin"'


def inject(text, blk):
    """Replace the existing block, or put it just before the Pinterest box. Unchanged text when there is no anchor."""
    if BLOCK_RE.search(text):
        return BLOCK_RE.sub(lambda m: blk, text, count=1)
    i = text.find(ANCHOR)
    return text if i < 0 or not blk else text[:i] + blk + text[i:]


def main():
    index = build_index()
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{INDEX.relative_to(ROOT)}: {len(index)} live posts")
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
