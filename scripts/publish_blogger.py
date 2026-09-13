#!/usr/bin/env python3
"""Publish the Verdict Picks posts and the five static pages to Blogger through the Blogger API v3.

Needs an OAuth2 access token with the scope https://www.googleapis.com/auth/blogger in the
environment variable BLOGGER_TOKEN (or pass --token-env NAME to read another variable).
The easiest way to mint one without a Cloud project: https://developers.google.com/oauthplayground
→ select "Blogger API v3 → https://www.googleapis.com/auth/blogger" → Authorize APIs →
Exchange authorization code for tokens → copy the Access token (valid ~1 hour).

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
import os, sys, json, re, pathlib, urllib.request, urllib.parse, urllib.error

BLOG_ID = "9072207571822466986"
API = "https://www.googleapis.com/blogger/v3"
POSTS = {
    "robot-vacuums": {
        "dir": "posts/2026-09-best-robot-vacuums",
        "title": "Best Robot Vacuums of 2026: Every Brand Compared, One Clear Verdict",
        "slug_title": "Best Robot Vacuums of 2026: Every Brand Compared, One Clear Verdict",   # already live under this title
        "labels": ["Robot Vacuums", "Buying Guide", "For Pet Owners", "Under $1000", "Carpet", "Hardwood Floors"],
    },
    "earbuds": {
        "dir": "posts/2026-09-best-wireless-earbuds",
        "title": "Best Wireless Earbuds of 2026: AirPods 5 & Pro 3 vs Sony, Bose, Galaxy Buds and Pixel Buds",
        "slug_title": "Best Wireless Earbuds 2026",
        "labels": ["Wireless Earbuds", "Buying Guide", "Under $300", "Under $100"],
    },
    "glasses": {
        "dir": "posts/2026-09-best-smart-glasses",
        "title": "Best Smart Glasses of 2026: Meta Ray-Ban Display vs Ray-Ban Meta Gen 2, Rokid, Xreal, Even Realities — and the AI-Glasses Exam Scandal",
        "slug_title": "Best Smart Glasses 2026",
        "labels": ["Smart Glasses", "Buying Guide", "Premium", "Under $500"],
    },
    "airtag": {
        "dir": "posts/2026-09-apple-airtag-2",
        "title": "Apple AirTag 2: Why Amazon Can't Keep the 4-Pack in Stock (and Whether You Need It)",
        "slug_title": "Apple AirTag 2 Review 2026",
        "labels": ["Best Sellers", "Review", "Under $100"],
    },
    "owala": {
        "dir": "posts/2026-09-owala-freesip",
        "title": "Owala FreeSip: How a $30 Water Bottle Beat Stanley to #1 on Amazon",
        "slug_title": "Owala FreeSip Review 2026",
        "labels": ["Best Sellers", "Review", "Under $100"],
    },
    "bissell": {
        "dir": "posts/2026-09-bissell-little-green",
        "title": "Bissell Little Green: The $95 Machine Behind a Million Before-and-After Videos",
        "slug_title": "Bissell Little Green Review 2026",
        "labels": ["Best Sellers", "Review", "Under $100", "For Pet Owners"],
    },
    "power-stations": {
        "dir": "posts/2026-09-best-portable-power-stations",
        "title": "Best Portable Power Stations of 2026: Anker SOLIX vs EcoFlow vs Jackery vs Bluetti — Sized for Outages, Camping, CPAP and Home Backup",
        "slug_title": "Best Portable Power Stations 2026",
        "labels": ["Power Stations", "Buying Guide", "Home Backup", "Under $500", "Camping"],
    },
    "prime-days": {
        "dir": "posts/2026-09-prime-big-deal-days-2026",
        "title": "Prime Big Deal Days 2026: The 12 Deals Worth Waiting For (and the Price That Makes Each One Real)",
        "slug_title": "Prime Big Deal Days 2026",
        "labels": ["Deals", "Buying Guide", "Best Sellers"],
    },
}
PAGES = [
    ("About Verdict Picks", "brand/pages/about.html"),
    ("How We Rank Products", "brand/pages/how-we-rank.html"),
    ("Affiliate Disclosure", "brand/pages/affiliate-disclosure.html"),
    ("Privacy & Cookie Policy", "brand/pages/privacy-policy.html"),
    ("Contact Us", "brand/pages/contact.html"),
    # category hub pages — short titles so they read as nav tabs in the Pages gadget
    ("Robot Vacuums", "brand/pages/hub-robot-vacuums.html"),
    ("Wireless Earbuds", "brand/pages/hub-wireless-earbuds.html"),
    ("Smart Glasses", "brand/pages/hub-smart-glasses.html"),
    ("Power Stations", "brand/pages/hub-power-stations.html"),
    ("Best Sellers", "brand/pages/hub-best-sellers.html"),
]

args = sys.argv[1:]
token_env = args[args.index("--token-env") + 1] if "--token-env" in args else "BLOGGER_TOKEN"
TOKEN = os.environ.get(token_env, "").strip()
DRAFT = "--draft" in args
CHECK_ONLY = "--check" in args
POSTS_ONLY = "--posts-only" in args
PAGES_ONLY = "--pages-only" in args
HUBS_ONLY = "--hubs-only" in args   # only the three category hub pages
ONLY = args[args.index("--only") + 1] if "--only" in args else None
if ONLY and ONLY not in POSTS:
    sys.exit(f"--only must be one of: {', '.join(POSTS)}")
if not TOKEN:
    sys.exit(f"no token in ${token_env} — see the docstring for how to mint one")

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
    content = strip_comments((pathlib.Path(P["dir"]) / "post.html").read_text(encoding="utf-8"))
    existing = posts_by_title.get(P["title"]) or posts_by_title.get(P["slug_title"])
    if existing:
        pid = existing["id"]
        body = {"kind": "blogger#post", "title": P["title"], "labels": P["labels"], "content": content}
        st, res = call("PUT", f"/blogs/{BLOG_ID}/posts/{pid}", body)
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
print("\nStill manual (the API cannot change blog settings or layout): Settings → Meta tags → search description per post"
      " (see each post-meta.md); Layout → Pages gadget → tick the hub pages.")
