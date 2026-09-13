#!/usr/bin/env python3
"""Audit a Blogger post: word/char counts, placeholders, tag balance, embeds, links.

Usage: python3 scripts/check_post.py posts/<slug>/post.html
Exit code 1 if a hard check fails.
"""
import re, sys, html, pathlib
from html.parser import HTMLParser

VOID = {"br","img","hr","input","meta","link","source","area","base","col","embed","param","track","wbr"}

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
    if "<script" in raw.lower(): fails.append("contains <script> (Blogger may strip it)")
    for f in fails: print("FAIL:", f)
    print("RESULT:", "FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "posts/2026-09-best-robot-vacuums/post.html")
