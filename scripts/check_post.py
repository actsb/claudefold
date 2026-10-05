#!/usr/bin/env python3
"""Audit a Blogger post: word/char counts, placeholders, tag balance, embeds, links.

Usage: python3 scripts/check_post.py posts/<slug>/post.html
Exit code 1 if a hard check fails.
"""
import re, sys, html, pathlib
from html.parser import HTMLParser

VOID = {"br","img","hr","input","meta","link","source","area","base","col","embed","param","track","wbr"}

# Amazon Associates Program Policies (see daily/README.md §0): Amazon customer reviews, star ratings and prices may be shown
# only through the Creators API / PA-API. FAIL = what the policy names; WARN = wording to look at, not a breach by itself.
AMAZON_FAIL = [
    ("Amazon star figure", r"\bAmazon\b[^.<]{0,60}?\b\d(?:\.\d)?\s*(?:stars?|out of 5)\b"),
    ("Amazon star figure", r"\b\d(?:\.\d)?\s*(?:stars?|out of 5)\b[^.<]{0,40}?\b(?:on|at|from)\s+Amazon\b"),
    ("Amazon rating or review count", r"\b\d[\d,.]*\+?\s*(?:global\s+)?(?:Amazon\s+)?(?:ratings?|reviews?|reviewers)\b[^.<]{0,40}?\b(?:on|at|from)\s+Amazon\b"),
    ("Amazon rating or review count", r"\b\d[\d,.]*\+?\s*(?:global\s+)?Amazon\s+(?:ratings?|reviews?|reviewers|shoppers have rated)\b"),
    ("Amazon rating or review count", r"\bAmazon(?:'s)?\s+(?:ratings?|reviews?)\b[^.<]{0,30}?\b\d[\d,.]{2,}"),
    ("five-star share", r"\b\d{1,3}\s?%\s+(?:of\s+[^.<]{0,30}?)?(?:five|5)[- ]stars?\b|\b(?:five|5)[- ]star\s+on\s+~?\d"),
    ("Amazon customer Q&A", r"\bAmazon(?:'s)?\s+(?:Q&A|questions and answers|customer questions)\b|questions and answers for the\b"),
    ("Amazon-review digest", r"\b(?:TheReviewIndex|ReviewMeta|Fakespot)\b"),
    ("Amazon price", r"\$\d[\d,.]*[^.<$]{0,40}?\b(?:on|at)\s+Amazon\b(?!\s+(?:button|link))"),
    ("Amazon price", r"\bAmazon(?:'s)?\s+(?:price|low|record low|sale price|deal price|list price)\b"),
    ("Amazon price tracker", r"\b(?:camelcamelcamel|Keepa)\b"),
]
AMAZON_WARN = [
    ("mentions Amazon reviews: paraphrase themes only, never quotes, counts or stars", r"\bAmazon(?:'s)?\s+(?:customer\s+)?(?:ratings?|reviews?|reviewers)\b"),
    ("Amazon rank or badge claim: prefer 'our top pick'", r"\bAmazon's\s+(?:#|No\.\s?)1\b|#1\s+(?:on|at)\s+Amazon\b|\bAmazon's\s+Choice\b|\bNo\.\s?1\s+(?:in|spot in)\s+Amazon|\bAmazon's\s+best[- ]selling\b"),
]

class Balance(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.errors=[]
    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in VOID: return
        if self.stack and self.stack[-1]==tag: self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1]!=tag: self.errors.append(f"unclosed <{self.stack.pop()}> before </{tag}>")
            self.stack.pop()
        else: self.errors.append(f"stray </{tag}>")

def main(path):
    raw = pathlib.Path(path).read_text(encoding="utf-8")
    body = re.sub(r"<svg.*?</svg>", " ", raw, flags=re.S)           # graphics text is not article text
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    text = html.unescape(re.sub(r"<[^>]+>", " ", body))
    words = re.findall(r"[A-Za-z0-9$][A-Za-z0-9$'’.,%/-]*", text)
    chars_no_space = len(re.sub(r"\s", "", text))
    p = Balance(); p.feed(raw)
    embeds = re.findall(r'youtube\.com/embed/([A-Za-z0-9_\-]{11})', raw)
    amazon = re.findall(r'https://www\.amazon\.com/[^"\s]+', raw)
    placeholders = re.findall(r"<!--SVG:[^>]+-->", raw)
    fails = []
    print(f"file: {path}")
    print(f"size: {len(raw):,} bytes | words: {len(words):,} | characters (no spaces): {chars_no_space:,} | characters (with spaces): {len(text.strip()):,}")
    print(f"headings: h2={raw.count('<h2')} h3={raw.count('<h3')} | tables: {raw.count('<table')} | inline SVGs: {raw.count('<svg')}")
    print(f"YouTube embeds ({len(embeds)}): {', '.join(dict.fromkeys(embeds))}")
    tagged = sum('tag=verdictpicks-20' in a for a in amazon)
    print(f"Amazon links: {len(amazon)} | with tag=verdictpicks-20: {tagged} | missing or placeholder tag: {len(amazon) - tagged}")
    if tagged != len(amazon): fails.append("Amazon link(s) without the live Associates tag")
    if placeholders: fails.append(f"unreplaced SVG placeholders: {placeholders}")
    if p.stack: fails.append(f"unclosed tags at end: {p.stack}")
    if p.errors: fails.append(f"tag balance errors: {p.errors[:5]}")
    min_words = int(sys.argv[sys.argv.index("--min-words") + 1]) if "--min-words" in sys.argv else 7000
    if len(words) < min_words: fails.append(f"word count {len(words)} < {min_words}")
    if re.search(r"<script(?![^>]*application/ld\+json)", raw, flags=re.I): fails.append("contains a non-JSON-LD <script> (Blogger may strip it)")
    # Amazon Associates Program Policies: no Amazon customer reviews or star ratings (or anything built from them) and no
    # Amazon prices unless they come from the Creators API / PA-API. Owner reviews from other retailers and forums are fine.
    seen = set()
    for label, pat in AMAZON_FAIL:
        for m in re.finditer(pat, text, flags=re.I):
            if m.start() in seen: continue
            seen.add(m.start()); fails.append(f"Amazon policy ({label}): …{text[max(0, m.start()-50):m.end()+30].strip()}…")
    warns = sorted({(label, text[max(0, m.start()-40):m.end()+25].strip()) for label, pat in AMAZON_WARN for m in re.finditer(pat, text, flags=re.I)})
    for label, ctx in warns[:12]:
        print(f"WARN: {label}: …{ctx}…")
    if re.search(r"raw\.githubusercontent\.com(/|%2F)", raw, flags=re.I): fails.append("hotlinks raw.githubusercontent.com (serve images from https://actsb.github.io/claudefold/ instead)")
    if re.search(r"/home/user/|home%2Fuser", raw): fails.append("an absolute container path leaked into a URL")
    for f in fails: print("FAIL:", f)
    print("RESULT:", "FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "posts/2026-09-best-robot-vacuums/post.html")
