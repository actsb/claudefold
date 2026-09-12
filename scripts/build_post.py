#!/usr/bin/env python3
"""Inline SVG graphics into a post.

Usage: python3 scripts/build_post.py posts/<slug>
Reads  posts/<slug>/post.src.html, replaces every <!--SVG:name--> with a
<figure> containing posts/<slug>/images/name.svg, writes posts/<slug>/post.html.
"""
import re, sys, pathlib

CAPTIONS_RE = re.compile(r"<!--SVG:([a-z0-9\-]+)(?:\|(.*?))?-->")

def main(post_dir: str) -> None:
    d = pathlib.Path(post_dir)
    src = (d / "post.src.html").read_text(encoding="utf-8")
    missing = []

    def repl(m):
        name, caption = m.group(1), m.group(2) or ""
        f = d / "images" / f"{name}.svg"
        if not f.exists():
            missing.append(name)
            return m.group(0)
        svg = f.read_text(encoding="utf-8").strip()
        svg = re.sub(r"^<\?xml[^>]*\?>\s*", "", svg)          # Blogger dislikes XML prologs
        cap = f'<div class="vp-source" style="font-size:13px;color:#555;margin-top:6px;">{caption}</div>' if caption else ""
        return (f'<div class="vp-figure" style="margin:1.4em 0;text-align:center;">'
                f'{svg}{cap}</div>')

    out = CAPTIONS_RE.sub(repl, src)
    (d / "post.html").write_text(out, encoding="utf-8")
    print(f"wrote {d/'post.html'} ({len(out):,} bytes)")
    if missing:
        print("MISSING SVGs:", ", ".join(missing)); sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "posts/2026-09-best-robot-vacuums")
