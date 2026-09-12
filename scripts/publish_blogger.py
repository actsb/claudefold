#!/usr/bin/env python3
"""Publish the launch post and the five static pages to Blogger through the Blogger API v3.

Needs an OAuth2 access token with the scope https://www.googleapis.com/auth/blogger in the
environment variable BLOGGER_TOKEN (or pass --token-env NAME to read another variable).
The easiest way to mint one without a Cloud project: https://developers.google.com/oauthplayground
→ select "Blogger API v3 → https://www.googleapis.com/auth/blogger" → Authorize APIs →
Exchange authorization code for tokens → copy the Access token (valid ~1 hour).

Usage:
  BLOGGER_TOKEN=ya29... python3 scripts/publish_blogger.py            # publish post + pages
  BLOGGER_TOKEN=ya29... python3 scripts/publish_blogger.py --draft    # create everything as drafts
  BLOGGER_TOKEN=ya29... python3 scripts/publish_blogger.py --check    # only verify token + blog access
Idempotent: a page or post whose title already exists on the blog is updated, not duplicated.
"""
import os, sys, json, re, pathlib, urllib.request, urllib.parse, urllib.error

BLOG_ID = "9072207571822466986"
API = "https://www.googleapis.com/blogger/v3"
POST_DIR = pathlib.Path("posts/2026-09-best-robot-vacuums")
POST = {
    "title": "Best Robot Vacuums of 2026: Every Brand Compared, One Clear Verdict",
    "labels": ["Robot Vacuums", "Buying Guide", "For Pet Owners", "Under $1000", "Carpet", "Hardwood Floors"],
    "file": POST_DIR / "post.html",
}
PAGES = [
    ("About Verdict Picks", "brand/pages/about.html"),
    ("How We Rank Products", "brand/pages/how-we-rank.html"),
    ("Affiliate Disclosure", "brand/pages/affiliate-disclosure.html"),
    ("Privacy & Cookie Policy", "brand/pages/privacy-policy.html"),
    ("Contact", "brand/pages/contact.html"),
]

args = sys.argv[1:]
token_env = args[args.index("--token-env") + 1] if "--token-env" in args else "BLOGGER_TOKEN"
TOKEN = os.environ.get(token_env, "").strip()
DRAFT = "--draft" in args
CHECK_ONLY = "--check" in args
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

def strip_comments(html): return re.sub(r"<!--.*?-->", "", html, flags=re.S).strip()

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
st, existing = call("GET", f"/blogs/{BLOG_ID}/pages", params={"status": "live", "fetchBodies": "false", "maxResults": 50})
st2, drafts = call("GET", f"/blogs/{BLOG_ID}/pages", params={"status": "draft", "fetchBodies": "false", "maxResults": 50})
by_title = {p["title"]: p for p in (existing.get("items", []) + drafts.get("items", []))}
for title, f in PAGES:
    body = {"title": title, "content": strip_comments(pathlib.Path(f).read_text(encoding="utf-8"))}
    if title in by_title:
        st, res = call("PUT", f"/blogs/{BLOG_ID}/pages/{by_title[title]['id']}", body)
        verb = "updated"
    else:
        st, res = call("POST", f"/blogs/{BLOG_ID}/pages", body, params={"isDraft": str(DRAFT).lower()})
        verb = "created"
    print(f"page {verb}: {title} → HTTP {st} {res.get('url', res.get('error', {}).get('message', ''))}")

# 3. the post (update if same title exists)
st, live = call("GET", f"/blogs/{BLOG_ID}/posts", params={"status": "live", "fetchBodies": "false", "maxResults": 50})
st2, pdrafts = call("GET", f"/blogs/{BLOG_ID}/posts", params={"status": "draft", "fetchBodies": "false", "maxResults": 50})
posts_by_title = {p["title"]: p for p in (live.get("items", []) + pdrafts.get("items", []))}
body = {"kind": "blogger#post", "title": POST["title"], "labels": POST["labels"],
        "content": strip_comments(POST["file"].read_text(encoding="utf-8"))}
if POST["title"] in posts_by_title:
    pid = posts_by_title[POST["title"]]["id"]
    st, res = call("PUT", f"/blogs/{BLOG_ID}/posts/{pid}", body)
    verb = "updated"
    if not DRAFT and st == 200 and res.get("status") == "DRAFT":
        st, res = call("POST", f"/blogs/{BLOG_ID}/posts/{pid}/publish"); verb = "updated + published"
else:
    st, res = call("POST", f"/blogs/{BLOG_ID}/posts", body, params={"isDraft": str(DRAFT).lower()})
    verb = "created"
print(f"post {verb}: HTTP {st} status={res.get('status')} url={res.get('url', res.get('error', {}).get('message', ''))}")
print("\nStill manual (the API cannot change blog settings): Settings → Permissions → Reader access = Public;"
      " Settings → Meta tags → enable search description and paste it from post-meta.md; blog title/description.")
