#!/usr/bin/env python3
"""Publish the Verdict Picks posts and the five static pages to Blogger through the Blogger API v3.

Auth, in order of preference:
  1. Unattended (for the daily Routine): BLOGGER_CLIENT_ID, BLOGGER_CLIENT_SECRET and BLOGGER_REFRESH_TOKEN in the
     environment (stored as environment secrets, never in the repo). The script mints a fresh access token itself.
     One-time setup by the blog owner: Google Cloud Console → new project → APIs & Services → Library → enable
     "Blogger API v3" → OAuth consent screen / Google Auth Platform (External; publishing status "In production",
     otherwise refresh tokens die after 7 days) → Credentials → OAuth client ID, type "Web application", with
     https://developers.google.com/oauthplayground as an authorized redirect URI (a Desktop client is refused by the
     Playground with redirect_uri_mismatch) → copy client ID + secret → https://developers.google.com/oauthplayground
     → gear icon → "Use your own OAuth credentials" → paste them → scope https://www.googleapis.com/auth/blogger →
     Authorize APIs (blog-owner account) → Exchange authorization code for tokens → copy the Refresh token.
     Store the three values as environment secrets of the cloud environment, never in the repo.
  2. Attended: an access token in BLOGGER_TOKEN (or --token-env NAME), minted at https://developers.google.com/oauthplayground
     → scope https://www.googleapis.com/auth/blogger → Authorize APIs → Exchange → Access token (valid ~1 hour).

Usage:
  BLOGGER_TOKEN=ya29... python3 scripts/publish_blogger.py                 # publish all posts + pages
  BLOGGER_TOKEN=ya29... python3 scripts/publish_blogger.py --posts-only    # skip the pages
  BLOGGER_TOKEN=ya29... python3 scripts/publish_blogger.py --only earbuds  # one post (key from POSTS)
  BLOGGER_TOKEN=ya29... python3 scripts/publish_blogger.py --draft         # create everything as drafts
  BLOGGER_TOKEN=ya29... python3 scripts/publish_blogger.py --check         # only verify token + blog access
Idempotent: a page or post whose title (or "slug title") already exists on the blog is updated, not duplicated.
New posts are created under the short slug title first (Blogger derives the URL from the title at first
publish), then immediately renamed to the full title so the URL stays short.
"""
import os, sys, json, re, base64, subprocess, pathlib, urllib.request, urllib.parse, urllib.error

BLOG_ID = "9072207571822466986"
API = "https://www.googleapis.com/blogger/v3"
POSTS = {
    "robot-vacuums": {
        "dir": "posts/2026-09-best-robot-vacuums",
        "title": "Best Robot Vacuums of 2026: Every Brand Compared, One Clear Verdict",
        "slug_title": "Best Robot Vacuums of 2026: Every Brand Compared, One Clear Verdict",   # already live under this title
        "labels": ["Robot Vacuums", "Buying Guide", "Home Cleaning", "For Pet Owners", "Carpet", "Hardwood Floors", "Under $1000", "Roborock", "Dreame", "Roomba", "Smart Home", "Amazon Finds"],
    },
    "earbuds": {
        "dir": "posts/2026-09-best-wireless-earbuds",
        "title": "Best Wireless Earbuds of 2026: AirPods 5 & Pro 3 vs Sony, Bose, Galaxy Buds and Pixel Buds",
        "slug_title": "Best Wireless Earbuds 2026",
        "labels": ["Wireless Earbuds", "Buying Guide", "AirPods", "Sony", "Bose", "Noise Cancelling", "Under $300", "Under $100", "Tech Gifts", "Amazon Finds"],
    },
    "glasses": {
        "dir": "posts/2026-09-best-smart-glasses",
        "title": "Best Smart Glasses of 2026: Ray-Ban Meta vs Meta Display, Rokid, Xreal, Even Realities",
        "aliases": ["Best Smart Glasses of 2026: Meta Ray-Ban Display vs Ray-Ban Meta Gen 2, Rokid, Xreal, Even Realities — and the AI-Glasses Exam Scandal"],   # title it was first published under
        "slug_title": "Best Smart Glasses 2026",
        "labels": ["Smart Glasses", "AI Glasses", "Buying Guide", "Ray-Ban Meta", "XR Glasses", "Wearable Tech", "Premium", "Under $500", "Privacy", "Amazon Finds"],
    },
    "airtag": {
        "dir": "posts/2026-09-apple-airtag-2",
        "title": "Apple AirTag 2: Why Amazon Can't Keep the 4-Pack in Stock (and Whether You Need It)",
        "slug_title": "Apple AirTag 2 Review 2026",
        "labels": ["Best Sellers", "Review", "Under $100", "Amazon Finds", "Trackers", "Travel", "Apple", "Tech Gifts", "Find My", "Smart Home"],
    },
    "owala": {
        "dir": "posts/2026-09-owala-freesip",
        "title": "Owala FreeSip Review: How a Water Bottle Beat Stanley to #1 on Amazon",
        "aliases": ["Owala FreeSip: How a $30 Water Bottle Beat Stanley to #1 on Amazon"],   # title it was first published under
        "slug_title": "Owala FreeSip Review 2026",
        "labels": ["Best Sellers", "Review", "Under $100", "Amazon Finds", "Water Bottles", "Hydration", "Owala", "Stanley", "Fitness", "Gifts"],
    },
    "bissell": {
        "dir": "posts/2026-09-bissell-little-green",
        "title": "Bissell Little Green Review: Behind a Million Before-and-After Videos",
        "aliases": ["Bissell Little Green: The $95 Machine Behind a Million Before-and-After Videos"],   # title it was first published under
        "slug_title": "Bissell Little Green Review 2026",
        "labels": ["Best Sellers", "Review", "Under $100", "Amazon Finds", "Carpet Cleaners", "For Pet Owners", "Home Cleaning", "Carpet", "Bissell", "Stain Removal"],
    },
    "power-stations": {
        "dir": "posts/2026-09-best-portable-power-stations",
        "title": "Best Portable Power Stations of 2026: Anker SOLIX vs EcoFlow vs Jackery vs Bluetti",
        "aliases": ["Best Portable Power Stations of 2026: Anker SOLIX vs EcoFlow vs Jackery vs Bluetti — Sized for Outages, Camping, CPAP and Home Backup"],   # title it was first published under
        "slug_title": "Best Portable Power Stations 2026",
        "labels": ["Power Stations", "Buying Guide", "Home Backup", "Camping", "Emergency Prep", "Anker SOLIX", "EcoFlow", "Jackery", "Under $500", "Solar", "Amazon Finds"],
    },
    "prime-days": {
        "dir": "posts/2026-09-prime-big-deal-days-2026",
        "title": "Prime Big Deal Days 2026: The 12 Deals Worth Waiting For (and the Price That Makes Each One Real)",
        "slug_title": "Prime Big Deal Days 2026",
        "labels": ["Deals", "Prime Day", "Buying Guide", "Best Sellers", "Robot Vacuums", "Wireless Earbuds", "Power Stations", "Smart Glasses", "Price Tracking", "Amazon Finds"],
    },
    "pets": {
        "dir": "posts/2026-09-best-pet-products-on-amazon",
        "title": "Best Pet Products on Amazon 2026: Pet Hair Roller, Grooming Vacuum, Robot Litter Box (Good, Better, Best)",
        "slug_title": "Best Pet Products on Amazon 2026",
        "aliases": ["The 3 Best Pet Products on Amazon in 2026: a $25 Roller, an $85 Grooming Vacuum and the $699 Robot Litter Box (Good · Better · Best)"],
        "labels": ["Pets", "Pet Products", "Buying Guide", "Best Sellers", "For Pet Owners", "Cat Litter", "Robot Litter Box", "Pet Grooming", "Pet Hair Removal", "Cats", "Dogs", "Under $100", "Amazon Finds"],
    },
    "dogs": {
        "dir": "posts/2026-09-dog-essentials-on-amazon",
        "title": "Best-Value Dog Essentials on Amazon 2026: No-Pull Harness, KONG Classic, Poop Bags",
        "slug_title": "Best Value Dog Essentials on Amazon 2026",
        "labels": ["Dogs", "Dog Supplies", "Pets", "Pet Products", "Buying Guide", "Best Sellers", "For Pet Owners", "Dog Harness", "Dog Toys", "Poop Bags", "Under $30", "Amazon vs Chewy", "Amazon Finds"],
    },
    "aivideo": {
        "dir": "posts/2026-09-claude-higgsfield-mcp-ai-video",
        "title": "Claude + Higgsfield MCP: From One Photo to an AI Product Video (2026 Setup, Credits, 13 Uses, US Rules)",
        "slug_title": "Claude Higgsfield MCP Workflow 2026",
        "labels": ["AI Tools", "AI Video", "Higgsfield", "Claude", "Workflow Guide", "Creator Tools", "YouTube", "Small Business", "Buying Guide", "For Creators", "ElevenLabs", "Amazon Finds"],
    },
    "levoit300": {
        "dir": "posts/2026-09-levoit-core-300p-air-purifier",
        "title": "Levoit Core 300-P Review 2026: The Under-$100 Air Purifier That Makes the $500 Dyson Pointless",
        "slug_title": "Levoit Core 300P Review 2026",
        "labels": ["Air Purifiers", "Home Comfort", "Best Sellers", "Review", "Under $100", "Allergies", "Amazon Finds", "Product of the Day"],
    },
    "bedsure-throw": {
        "dir": "posts/2026-10-bedsure-heated-blanket-throw",
        "title": "Bedsure Heated Throw Review 2026: Amazon's Best-Selling Electric Blanket, Recall Check Included",
        "slug_title": "Bedsure Heated Throw Review 2026",
        "labels": ["Home Comfort", "Best Sellers", "Review", "Under $50", "Gifts", "Amazon Finds", "Product of the Day"],
    },
    "ocedar-mop": {
        "dir": "posts/2026-10-o-cedar-easywring-spin-mop",
        "title": "O-Cedar EasyWring Spin Mop Review 2026: 170,000 Reviews and No Refill Pads",
        "slug_title": "O-Cedar EasyWring Spin Mop Review 2026",
        "labels": ["Home Cleaning", "Best Sellers", "Review", "Under $50", "Amazon Finds", "Product of the Day"],
    },
    "noco-gb40": {
        "dir": "posts/2026-09-noco-boost-plus-gb40-jump-starter",
        "title": "NOCO GB40 Review 2026: The Glovebox Jump Starter With 110,000+ Amazon Ratings",
        "slug_title": "NOCO GB40 Jump Starter Review 2026",
        "labels": ["Car", "Tools", "Best Sellers", "Review", "Under $150", "Amazon Finds", "Product of the Day"],
    },
    "beckham-pillows": {
        "dir": "posts/2026-10-beckham-hotel-collection-pillows",
        "title": "Beckham Hotel Collection Pillows Review 2026: Amazon's #1 Pillow, Honestly",
        "slug_title": "Beckham Hotel Pillows Review 2026",
        "labels": ["Sleep", "Bedding", "Best Sellers", "Review", "Under $50", "Amazon Finds", "Product of the Day"],
    },
    "bidets2026": {
        "dir": "posts/2026-10-best-bidet-2026",
        "title": "Best Bidet of 2026: The $50 Attachment Owners Recommend (vs KOHLER PureWash, TUSHY, TOTO)",
        "slug_title": "Best Bidet 2026",
        "labels": ["Bathroom", "Bidets", "Buying Guide", "Best Sellers", "Under $50", "Amazon Finds"],
    },
}
PAGES = [
    ("About Verdict Picks", "brand/pages/about.html"),
    ("How We Rank Products", "brand/pages/how-we-rank.html"),
    ("Affiliate Disclosure", "brand/pages/affiliate-disclosure.html"),
    ("Privacy & Cookie Policy", "brand/pages/privacy-policy.html"),
    ("Contact Us", "brand/pages/contact.html"),
    ("Follow Verdict Picks", "brand/pages/follow.html"),
    # category hub pages — short titles so they read as nav tabs in the Pages gadget
    ("Robot Vacuums", "brand/pages/hub-robot-vacuums.html"),
    ("Wireless Earbuds", "brand/pages/hub-wireless-earbuds.html"),
    ("Smart Glasses", "brand/pages/hub-smart-glasses.html"),
    ("Power Stations", "brand/pages/hub-power-stations.html"),
    ("Best Sellers", "brand/pages/hub-best-sellers.html"),
]

args = sys.argv[1:]
token_env = args[args.index("--token-env") + 1] if "--token-env" in args else "BLOGGER_TOKEN"

def mint_token():
    """Access token from the environment, or minted from a stored refresh token (the unattended path)."""
    t = os.environ.get(token_env, "").strip()
    if t:
        return t
    cid, sec, rt = (os.environ.get(k, "").strip() for k in ("BLOGGER_CLIENT_ID", "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN"))
    if not (cid and sec and rt):
        return ""
    data = urllib.parse.urlencode({"client_id": cid, "client_secret": sec, "refresh_token": rt, "grant_type": "refresh_token"}).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            tok = json.loads(r.read()).get("access_token", "")
            if tok: print("access token minted from the stored refresh token")
            return tok
    except urllib.error.HTTPError as e:
        sys.exit(f"refresh-token exchange failed: HTTP {e.code} {e.read()[:200]!r} — re-issue BLOGGER_REFRESH_TOKEN (consent screen must be 'In production')")

TOKEN = mint_token()
DRAFT = "--draft" in args
CHECK_ONLY = "--check" in args
POSTS_ONLY = "--posts-only" in args
PAGES_ONLY = "--pages-only" in args
HUBS_ONLY = "--hubs-only" in args   # only the three category hub pages
ONLY = args[args.index("--only") + 1] if "--only" in args else None
if ONLY and ONLY not in POSTS:
    sys.exit(f"--only must be one of: {', '.join(POSTS)}")
if not TOKEN:
    sys.exit(f"no credentials: set BLOGGER_CLIENT_ID/BLOGGER_CLIENT_SECRET/BLOGGER_REFRESH_TOKEN (unattended) or ${token_env} (attended) — see the docstring")

def call(method, path, body=None, params=None):
    url = f"{API}{path}" + (("?" + urllib.parse.urlencode(params)) if params else "")
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")

def strip_comments(html):
    """Drop HTML comments except Blogger's jump break <!--more-->."""
    html = html.replace("<!--more-->", "\x00MORE\x00")
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    return html.replace("\x00MORE\x00", "<!--more-->").strip()


PAGES_BASE = "https://actsb.github.io/claudefold/"
EMBED_WIDTH = {"pin.png": 440}   # px of the embedded JPEG (shown at 220 px wide, so 2x). The cover is NOT embedded: it must stay a real URL (cover.jpg) so Google can crawl it, index it and use it as og:image.
EMBED_LIMIT = 700_000                               # chars of post HTML; above this keep the GitHub Pages URLs instead

def inline_images(html):
    """Blogger has no image-upload API, so decorative .png images that live on GitHub Pages (the pin thumbnail) are embedded as
    compressed JPEG data: URIs (ImageMagick `convert`). The post then renders even if Pages is down. Anything that
    fails (no convert, missing file, post too large) keeps its Pages URL. Pinterest's media= parameter is left alone:
    Pinterest needs a public URL, which is what Pages still serves."""
    def one(m):
        rel = m.group(2)
        f = pathlib.Path(__file__).resolve().parent.parent / rel
        if not f.exists():
            return m.group(0)
        w = EMBED_WIDTH.get(f.name, 1200)
        try:
            jpg = subprocess.run(["convert", str(f), "-resize", f"{w}x>", "-background", "white", "-flatten", "-strip", "-quality", "82", "jpg:-"],
                                 capture_output=True, check=True, timeout=60).stdout
        except Exception as e:
            print(f"  image kept as URL ({f.name}): {e}")
            return m.group(0)
        return f'{m.group(1)}data:image/jpeg;base64,{base64.b64encode(jpg).decode()}"'
    out = re.sub(r'(<img\b[^>]*?\bsrc=")' + re.escape(PAGES_BASE) + r'([^"]+?\.png)"', one, html)
    if len(out) > EMBED_LIMIT:
        print(f"  post too large with embedded images ({len(out)} chars): keeping Pages URLs")
        return html
    return out

# 1. token + blog access
st, info = call("GET", "/users/self/blogs")
if st != 200:
    sys.exit(f"token check failed: HTTP {st} {json.dumps(info)[:300]}")
blogs = {b["id"]: b for b in info.get("items", [])}
print("token OK — blogs on this account:", ", ".join(f"{b['name']} ({i}, {b['url']})" for i, b in blogs.items()) or "none")
if BLOG_ID not in blogs:
    sys.exit(f"blog {BLOG_ID} is not on this account; refusing to publish elsewhere")
blog_url = blogs[BLOG_ID]["url"]
if CHECK_ONLY:
    sys.exit(0)

# 2. pages (update if a page with the same title exists)
if POSTS_ONLY or ONLY:
    print("skipping pages")
st, existing = call("GET", f"/blogs/{BLOG_ID}/pages", params={"status": "live", "fetchBodies": "false", "maxResults": 50})
st2, drafts = call("GET", f"/blogs/{BLOG_ID}/pages", params={"status": "draft", "fetchBodies": "false", "maxResults": 50})
by_title = {p["title"]: p for p in (existing.get("items", []) + drafts.get("items", []))}
for title, f in ([] if (POSTS_ONLY or ONLY) else (PAGES[-5:] if HUBS_ONLY else PAGES)):
    body = {"title": title, "content": strip_comments(pathlib.Path(f).read_text(encoding="utf-8"))}
    if title in by_title:
        st, res = call("PUT", f"/blogs/{BLOG_ID}/pages/{by_title[title]['id']}", body)
        verb = "updated"
    else:
        st, res = call("POST", f"/blogs/{BLOG_ID}/pages", body, params={"isDraft": str(DRAFT).lower()})
        verb = "created"
    print(f"page {verb}: {title} → HTTP {st} {res.get('url', res.get('error', {}).get('message', ''))}")

# 3. the posts (update if the full title or the slug title already exists)
if PAGES_ONLY or HUBS_ONLY:
    print("skipping posts"); sys.exit(0)
st, live = call("GET", f"/blogs/{BLOG_ID}/posts", params={"status": "live", "fetchBodies": "false", "maxResults": 100})
st2, pdrafts = call("GET", f"/blogs/{BLOG_ID}/posts", params={"status": "draft", "fetchBodies": "false", "maxResults": 100})
posts_by_title = {p["title"]: p for p in (live.get("items", []) + pdrafts.get("items", []))}
for key, P in POSTS.items():
    if ONLY and key != ONLY:
        continue
    content = inline_images(strip_comments((pathlib.Path(P["dir"]) / "post.html").read_text(encoding="utf-8")))
    existing = posts_by_title.get(P["title"]) or posts_by_title.get(P["slug_title"]) or next((posts_by_title[a] for a in P.get("aliases", []) if a in posts_by_title), None)
    if existing:
        pid = existing["id"]
        # PATCH, not PUT: change only title, labels and content, and leave what the API cannot see untouched
        # (above all the search description, which can be entered only in the Blogger editor)
        body = {"title": P["title"], "labels": P["labels"], "content": content}
        st, res = call("PATCH", f"/blogs/{BLOG_ID}/posts/{pid}", body)
        verb = "updated"
        if not DRAFT and st == 200 and res.get("status") == "DRAFT":
            st, res = call("POST", f"/blogs/{BLOG_ID}/posts/{pid}/publish"); verb = "updated + published"
    else:
        # create under the short slug title so the URL is short, then rename to the full title
        body = {"kind": "blogger#post", "title": P["slug_title"], "labels": P["labels"], "content": content}
        st, res = call("POST", f"/blogs/{BLOG_ID}/posts", body, params={"isDraft": str(DRAFT).lower()})
        verb = "created"
        if st == 200 and P["slug_title"] != P["title"]:
            pid = res["id"]
            st, res = call("PUT", f"/blogs/{BLOG_ID}/posts/{pid}", {"kind": "blogger#post", "title": P["title"], "labels": P["labels"], "content": content})
            verb = "created (short URL) + renamed to full title"
    print(f"post {key} {verb}: HTTP {st} status={res.get('status')} url={res.get('url', res.get('error', {}).get('message', ''))}")
print("\nStill manual (the API cannot change these): each post's search description, entered in the Blogger editor"
      " (the texts are in daily/search-descriptions.md); Layout → Pages gadget → tick the hub pages.")
