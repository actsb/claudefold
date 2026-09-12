#!/usr/bin/env python3
"""Build a Blogger import file (Atom XML) containing the launch post and the five static pages.

Usage: python3 scripts/make_blogger_import.py [--draft]
Writes posts/2026-09-best-robot-vacuums/blogger-import.xml

Import it in Blogger: Settings → Manage blog → Import content → choose this file.
Tick "Automatically publish all imported posts and pages" unless you passed --draft.
"""
import sys, pathlib, datetime, re
from xml.sax.saxutils import escape

BLOG_ID = "9072207571822466986"
AUTHOR = "Verdict Picks"
POST_DIR = pathlib.Path("posts/2026-09-best-robot-vacuums")
PAGES_DIR = pathlib.Path("brand/pages")
DRAFT = "yes" if "--draft" in sys.argv else "no"
NOW = datetime.datetime(2026, 9, 12, 14, 0, 0).strftime("%Y-%m-%dT%H:%M:%S.000Z")

POST = {
    "title": "Best Robot Vacuums of 2026: Every Brand Compared, One Clear Verdict",
    "labels": ["Robot Vacuums", "Buying Guide", "For Pet Owners", "Under $1000", "Carpet", "Hardwood Floors"],
    "file": POST_DIR / "post.html",
}
PAGES = [
    ("About Verdict Picks", PAGES_DIR / "about.html"),
    ("How We Rank Products", PAGES_DIR / "how-we-rank.html"),
    ("Affiliate Disclosure", PAGES_DIR / "affiliate-disclosure.html"),
    ("Privacy & Cookie Policy", PAGES_DIR / "privacy-policy.html"),
    ("Contact", PAGES_DIR / "contact.html"),
]

def strip_comments(html: str) -> str:
    return re.sub(r"<!--.*?-->", "", html, flags=re.S).strip()

def entry(kind: str, n: int, title: str, html: str, labels=()):
    cats = "".join(f"\n    <category scheme='http://www.blogger.com/atom/ns#' term='{escape(l, {chr(39): '&#39;'})}'/>" for l in labels)
    return f"""  <entry>
    <id>tag:blogger.com,1999:blog-{BLOG_ID}.{kind}-verdictpicks-{n}</id>
    <published>{NOW}</published>
    <updated>{NOW}</updated>
    <category scheme='http://schemas.google.com/g/2005#kind' term='http://schemas.google.com/blogger/2008/kind#{kind}'/>{cats}
    <title type='text'>{escape(title)}</title>
    <content type='html'>{escape(html)}</content>
    <author><name>{AUTHOR}</name></author>
    <app:control xmlns:app='http://purl.org/atom/app#'><app:draft>{DRAFT}</app:draft></app:control>
  </entry>
"""

entries = [entry("post", 1, POST["title"], strip_comments(POST["file"].read_text(encoding="utf-8")), POST["labels"])]
entries += [entry("page", i + 1, t, strip_comments(f.read_text(encoding="utf-8"))) for i, (t, f) in enumerate(PAGES)]

xml = f"""<?xml version='1.0' encoding='UTF-8'?>
<?xml-stylesheet href="http://www.blogger.com/styles/atom.css" type="text/css"?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/' xmlns:blogger='http://schemas.google.com/blogger/2008' xmlns:georss='http://www.georss.org/georss' xmlns:gd='http://schemas.google.com/g/2005' xmlns:thr='http://purl.org/syndication/thread/1.0'>
  <id>tag:blogger.com,1999:blog-{BLOG_ID}.archive</id>
  <updated>{NOW}</updated>
  <title type='text'>Verdict Picks</title>
  <author><name>{AUTHOR}</name></author>
  <generator version='7.00' uri='http://www.blogger.com'>Blogger</generator>
{''.join(entries)}</feed>
"""
out = POST_DIR / "blogger-import.xml"
out.write_text(xml, encoding="utf-8")
import xml.dom.minidom as m; m.parseString(xml.encode("utf-8"))   # well-formedness check
print(f"wrote {out} ({len(xml):,} bytes): 1 post + {len(PAGES)} pages, draft={DRAFT}")
