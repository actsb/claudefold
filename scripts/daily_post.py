#!/usr/bin/env python3
"""Scaffold and build a product-of-the-day post (see daily/README.md).

  python3 scripts/daily_post.py new <key>          # daily/queue.json entry → posts/<date>-<slug>/ + publisher entry, SEO config, hub line, promo and pin drafts
  python3 scripts/daily_post.py build posts/<dir>  # cards, strips, cover, pin, infographics, assemble, SEO layer, build, check, PNGs

Queue entry (daily/queue.json → "queue": [...]):
  {"key": "lodge-skillet", "slug": "lodge-cast-iron-skillet-2026", "date": "2026-09-27", "status": "queued",
   "name": "Lodge 10.25-Inch Cast Iron Skillet", "short": "Lodge skillet", "category": "generic",
   "art": {"shape": "flat", "body": "#2F2F2F", "accent": "#C9781B"}, "search": "Lodge 10.25 inch cast iron skillet",
   "title": "Lodge Cast Iron Skillet Review 2026: ...", "slug_title": "Lodge Cast Iron Skillet Review 2026",
   "labels": ["Kitchen", "Best Sellers", "Review", "Under $50", "Amazon Finds"], "hook": "one-line seasonal hook", "beats": "the alternative it beats"}
"""
import datetime, json, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
QUEUE = ROOT / "daily" / "queue.json"
TAG = "verdictpicks-20"
CLUSTER_TITLES = {"cleaning": "Home cleaning", "comfort": "Sleep and home comfort", "kitchen": "Kitchen", "car": "Car",
                  "pets": "Pets", "bathroom": "Bathroom", "tech": "Tech and travel", "home": "Home and storage",
                  "gifts": "Gift guides", "deals": "Sales and deal guides", "more": "More picks"}

def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s

def run(*cmd, check=True):
    r = subprocess.run([str(c) for c in cmd], cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"FAILED: {' '.join(str(c) for c in cmd)}\n{r.stdout[-600:]}\n{r.stderr[-600:]}")
    return r

def cover_jpeg(src, dst):
    """cover.png → JPEG that fits 1200×630, white background, no metadata, quality 82: ImageMagick when present, else Pillow
    (installed on first use, since fresh containers may have neither)."""
    if shutil.which("convert"):
        run("convert", src, "-resize", "1200x630", "-background", "white", "-flatten", "-strip", "-quality", "82", dst); return
    try:
        from PIL import Image
    except ImportError:
        run(sys.executable, "-m", "pip", "install", "--quiet", "pillow")
        from PIL import Image
    im = Image.open(src).convert("RGBA"); im.thumbnail((1200, 630), Image.LANCZOS)
    bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.getchannel("A"))
    bg.save(dst, "JPEG", quality=82, optimize=True)

def cmd_new(key):
    q = json.loads(QUEUE.read_text(encoding="utf-8"))
    e = next((x for x in q["queue"] if x["key"] == key), None)
    if not e: sys.exit(f"{key} not in daily/queue.json")
    # a post is dated the day it is written: the queue date is only the plan
    date = e["date"] = datetime.date.today().isoformat()
    y, m = date[:4], date[5:7]
    roundup = e.get("format") == "roundup"
    d = ROOT / "posts" / f"{date[:7]}-{e['slug']}"
    if d.exists(): sys.exit(f"{d} exists")
    (d / "src").mkdir(parents=True); (d / "images").mkdir()
    url = f"https://acts39.blogspot.com/{y}/{m}/{slugify(e['slug_title'])}.html"
    e["url"] = url; e["dir"] = str(d.relative_to(ROOT))
    cta = f"https://www.amazon.com/s?k={'+'.join(e['search'].split())}&tag={TAG}"
    cards = {"category": e.get("category", "generic"),
             "buy_title": f"The exact {e['short']} to order, and what to check on the listing",
             "buy_total": "The button shows today's price; as an Amazon Associate we earn from qualifying purchases, and it never changes what you pay.",
             "cards": [{"id": key, "category": e.get("category", "generic"), "name": e["name"], "short": e["short"],
                        "badge": "WRITE: category · why it is the value pick", "chip": "WRITE: three spec words",
                        "art": e.get("art", {"shape": "box", "body": "#2F3A48", "accent": "#1E8E5A"}),
                        "price": "WRITE: a price band, or a non-Amazon price with source and date (never an Amazon price)",
                        "buy_if": "WRITE: who it is for", "skip_if": "WRITE: who should skip it and what to buy instead",
                        "owners": "WRITE: praise / complaints from owner reviews at non-Amazon retailers or forums, with source and date (never Amazon stars, counts or quotes)",
                        "cta": cta, "video": "", "video_title": "", "video_channel": "", "video_why": "",
                        "buy": {"tier": "The pick", "pick": "WRITE: exact variant/size/colour", "check": "WRITE: sold-by line, model number, what marks a counterfeit", "label": "See today's price"}}]}
    (d / "cards.json").write_text(json.dumps(cards, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cover = {"hero": key, "title_size": 66, "title": [e["short"] + ":", "WRITE: line two", "WRITE: line three"],
             "subtitle": ["WRITE: one sentence of what the guide answers,", "wrapped at about fifty characters per line,", "three lines at most."],
             "footer": f"Product of the day · {e['name']} · Verdict Picks", "alt": f"{e['name']}: is it worth it, how to use it, and why Amazon is the place to buy it (Verdict Picks)",
             "pin": ["WRITE: bullet one", "WRITE: bullet two", "WRITE: bullet three"], "url": url, "style": "bright", "products": [key]}
    (d / "cover.json").write_text(json.dumps(cover, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    strips = {"strips": [{"id": "in-real-life", "card": key, "title": f"A day with the {e['short']} — in real life",
                          "panels": [{"glyph": "clock", "head": "WRITE", "text": "WRITE", "host": {"pose": "present"}},
                                     {"glyph": "check", "product": True, "head": "WRITE", "text": "WRITE"},
                                     {"glyph": "warning", "head": "WRITE", "text": "WRITE"},
                                     {"glyph": "sun", "head": "WRITE", "text": "WRITE", "host": {"pose": "thumbsup"}}]}]}
    (d / "strips.json").write_text(json.dumps(strips, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    infos = [{"type": "steps", "name": "howto", "title": f"The {e['short']} in five minutes", "sub": "WRITE: what the steps get you", "footer": "WRITE: source (the manual, the brand's page)",
              "items": [{"head": "WRITE", "body": "WRITE"} for _ in range(6)]},
             {"type": "stores", "name": "stores", "title": "Where to buy it, and why Amazon usually wins", "sub": "WRITE: month, what was compared", "footer": "Prices and policies as seen in the month of writing; the buttons show today's.",
              "rows": [{"store": "Amazon", "price": "WRITE", "ship": "WRITE", "returns": "WRITE", "note": "WRITE", "verdict": "win"},
                       {"store": "Walmart", "price": "WRITE", "ship": "WRITE", "returns": "WRITE", "note": "WRITE", "verdict": "ok"},
                       {"store": "Target", "price": "WRITE", "ship": "WRITE", "returns": "WRITE", "note": "WRITE", "verdict": "ok"},
                       {"store": "Brand store", "price": "WRITE", "ship": "WRITE", "returns": "WRITE", "note": "WRITE", "verdict": "ok"},
                       {"store": "Temu / look-alikes", "price": "WRITE", "ship": "WRITE", "returns": "WRITE", "note": "WRITE", "verdict": "no"}]}]
    (d / "infographics.json").write_text(json.dumps(infos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    long_date = datetime.date.fromisoformat(date).strftime("%B %-d, %Y")
    tpl = (ROOT / "daily" / "template-00-easy.html").read_text(encoding="utf-8")
    for k, v in {"{{NAME}}": e["name"], "{{SHORT}}": e["short"], "{{DATE}}": long_date, "{{URL}}": url, "{{KEY}}": key, "{{DIR}}": d.name, "{{SEARCH}}": e["search"]}.items():
        tpl = tpl.replace(k, v)
    (d / "src" / "00-easy.html").write_text(tpl, encoding="utf-8")
    model = e.get("model", "posts/2026-10-best-bidet-2026")
    fmt = f"roundup (daily/README.md section 11; model: {model})" if roundup else "product of the day (daily/README.md)"
    (d / "post-meta.md").write_text(f"# Post metadata — {e['title']}\n\n* **Title:** {e['title']}\n* **Slug title (first publish):** {e['slug_title']} → {url}\n* **Labels:** {', '.join(e['labels'])}\n* **Search description (≤150 chars):** WRITE\n* **Format:** {fmt}\n* **Research:** research/daily-{date}-{e['slug']}.md\n* **Status:** scaffolded {date}\n", encoding="utf-8")
    # publisher entry
    pb = ROOT / "scripts" / "publish_blogger.py"; t = pb.read_text(encoding="utf-8")
    entry = f'''    "{key}": {{
        "dir": "{d.relative_to(ROOT).as_posix()}",
        "title": {json.dumps(e['title'])},
        "slug_title": {json.dumps(e['slug_title'])},
        "labels": {json.dumps(e['labels'])},
    }},
'''
    i = t.index("POSTS = {"); j = t.index("\n}\n", i)          # the first line that closes the POSTS dict
    assert key not in t[i:j], f"{key} already in publish_blogger.py"
    t = t[:j] + "\n" + entry.rstrip("\n") + t[j:]; pb.write_text(t, encoding="utf-8")
    # seo config
    sc = ROOT / "brand" / "seo-configs.json"; c = json.loads(sc.read_text(encoding="utf-8"))
    c[d.name] = {"updated": long_date, "url": url, "list_name": e["name"], "takeaways": [], "korean": "", "h2": []}
    sc.write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    # hub line (draft), promo and pin drafts
    # the hub page groups guides by cluster: the line goes into the entry's cluster list, else under "More picks"
    hub = ROOT / "brand" / "pages" / "hub-best-sellers.html"; h = hub.read_text(encoding="utf-8")
    text = e["name"] if roundup else f'{e["name"]} review'
    line = f'<li style="margin-bottom:.6em;"><a href="{url.replace("https://acts39.blogspot.com", "")}" style="color:#1B2A41;font-weight:700;">{text}</a> — WRITE: one line on who it is for and the verdict (no Amazon ratings, counts or prices).</li>\n'
    cluster = e.get("cluster") or "more"
    anchor = f"<!--CLUSTER:{cluster}-->\n"
    if anchor not in h:   # first guide of a new cluster: open its section
        title = CLUSTER_TITLES.get(cluster, cluster.capitalize())
        section = (f'<h3 style="color:#1B2A41;font-size:1.25em;margin:1.3em 0 .3em;">{title}</h3>\n'
                   f'<p>WRITE: one or two sentences on what this section covers and how we choose.</p>\n'
                   f'<ul style="padding-left:22px;">\n{anchor}</ul>\n')
        assert "<!--NEW-SECTIONS-->" in h, "hub anchor not found"
        h = h.replace("<!--NEW-SECTIONS-->", section + "<!--NEW-SECTIONS-->", 1)
    hub.write_text(h.replace(anchor, anchor + line, 1), encoding="utf-8")
    kind = "buying guide" if roundup else "product of the day"
    (ROOT / "promo").mkdir(exist_ok=True)
    (ROOT / "promo" / f"{date}-{e['slug']}.md").write_text(f"# Promotion kit — {e['name']} ({kind}, {long_date})\n\nPost: {url}\nCover: `{d.relative_to(ROOT)}/images/cover.png` · Pin: `images/pin.png` · Share: `images/howto.png`, `images/stores.png`, `images/strips/in-real-life.png`\n\nDisclosure on every social post: \"Amazon links in the guide are paid links.\"\n\n## Pinterest (day 1)\nWRITE\n\n## X / Threads (day 1)\n1. WRITE\n2. WRITE\n\n## Facebook groups (day 2)\nWRITE\n\n## Reddit (comments only, day 3)\nWRITE\n\n## Search and indexing\nSearch Console → URL inspection → Request indexing; set the search description from post-meta.md.\n", encoding="utf-8")
    pins = ROOT / "pinterest" / f"pins-{date[:7]}.md"
    if not pins.exists(): pins.write_text(f"# Pinterest pins — {date[:7]}\n\nBoard: Best of Amazon 2026 (plus the category board named per pin).\n\n"
                                         "**Approval:** a pin goes live only after the owner chooses it (Pinterest's Developer Guidelines). The owner adds "
                                         "`**Approved**` with `yes` on the next line under an entry's Alt text, or runs the Pinterest workflow in mode "
                                         "`pin` with the post link (daily/pinterest-setup.md, step 8). Claude sessions never add the Approved field on their own.\n\n", encoding="utf-8")
    pins.write_text(pins.read_text(encoding="utf-8") + f"## {e['name']} — `{d.relative_to(ROOT)}/images/pin.png`\n\n**Title**\nWRITE\n\n**Description**\nWRITE #amazonfinds\n\n**Link**\n{url}\n\n**Alt text**\nWRITE\n\n---\n\n", encoding="utf-8")
    e["status"] = "writing"; QUEUE.write_text(json.dumps(q, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"scaffolded {d.relative_to(ROOT)} → {url}\nnext: edit cards.json, cover.json, strips.json, infographics.json, src/00-easy.html; then: python3 scripts/daily_post.py build {d.relative_to(ROOT)}")
    if roundup:
        print(f"roundup: write src/00-easy.html on the structure of {model}/src/00-easy.html "
              f"(daily/README.md section 11); research candidates: {e.get('picks', 'see the queue entry')}")

def cmd_build(post_dir):
    d = ROOT / post_dir
    for s in ("product_cards.py", "story_strip.py", "make_cover.py", "make_pin.py", "daily_infographic.py"):
        run("python3", ROOT / "scripts" / s, d)
    run("python3", ROOT / "scripts" / "assemble_post.py", d)
    cfg = json.loads((ROOT / "brand" / "seo-configs.json").read_text(encoding="utf-8"))
    if d.name in cfg:
        run("python3", ROOT / "scripts" / "seo_layer.py", d, ROOT / "brand" / "seo-configs.json")
        run("python3", ROOT / "scripts" / "assemble_post.py", d)
    run("python3", ROOT / "scripts" / "build_post.py", d)
    r = run("python3", ROOT / "scripts" / "check_post.py", d / "post.html", "--min-words", "1500", check=False)
    print(r.stdout.strip().splitlines()[-4:] and "\n".join(r.stdout.strip().splitlines()[-4:]))
    for sub in ("images", "images/cards", "images/strips"):
        if (d / sub).exists(): run("node", ROOT / "scripts" / "render_png.mjs", d / sub)
    if (d / "images" / "cover.png").exists():   # the post's <img> uses cover.jpg: small, crawlable, usable as og:image / image-search source
        cover_jpeg(d / "images" / "cover.png", d / "images" / "cover.jpg")
    left = re.findall(r"WRITE[^<\"]{0,40}", (d / "post.html").read_text(encoding="utf-8"))
    print(f"PNGs rendered; unfilled WRITE markers in post.html: {len(left)}")
    if r.returncode: sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3: sys.exit(__doc__)
    {"new": cmd_new, "build": cmd_build}[sys.argv[1]](sys.argv[2])
