#!/usr/bin/env python3
"""Cover / thumbnail (1200x630) with a hero render of the top pick.

Usage: python3 scripts/make_cover.py posts/<slug>
Reads posts/<slug>/cover.json {title:[..], subtitle:[..], footer:"", hero: <card id>} and cards.json.
Writes posts/<slug>/images/cover.svg (render to PNG with scripts/render_png.mjs).
"""
import json, sys, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from product_cards import render_product, FONT

def esc(s): return html.escape(str(s), quote=True)

def main(post_dir):
    d = pathlib.Path(post_dir)
    cfg = json.loads((d / "cover.json").read_text(encoding="utf-8"))
    spec = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    hero = next(c for c in spec["cards"] if c["id"] == cfg["hero"])
    prod = render_product(spec["category"], hero.get("art", {}), "hero", scale=cfg.get("scale", 1.0),
                          tx=cfg.get("tx", 600), ty=cfg.get("ty", 120), with_studio=False)
    title = "".join(f'<text x="70" y="{262 + i*92}" font-size="86" font-weight="800" fill="{"#8FD3AE" if line.startswith("of ") else "#fff"}">{esc(line)}</text>' for i, line in enumerate(cfg["title"]))
    sub = "".join(f'<text x="70" y="{500 + i*32}" font-size="25" fill="#E6E9EE">{esc(line)}</text>' for i, line in enumerate(cfg["subtitle"]))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" role="img" aria-label="{esc(cfg.get("alt", " ".join(cfg["title"])))}">
<defs>
<radialGradient id="cov-spot" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#3A4D6B"/><stop offset="0.6" stop-color="#24344D"/><stop offset="1" stop-color="#1B2A41" stop-opacity="0"/></radialGradient>
<radialGradient id="cov-halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffffff" stop-opacity="0.22"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
<linearGradient id="cov-floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.10"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
</defs>
<rect width="1200" height="630" fill="#1B2A41"/>
<ellipse cx="900" cy="330" rx="420" ry="300" fill="url(#cov-spot)"/>
<ellipse cx="900" cy="300" rx="300" ry="200" fill="url(#cov-halo)"/>
<ellipse cx="900" cy="520" rx="330" ry="40" fill="#ffffff" opacity="0.07"/>
<g font-family="{FONT}">
<rect x="70" y="72" width="330" height="36" rx="18" fill="#1E8E5A"/>
<text x="235" y="97" text-anchor="middle" font-size="16" font-weight="700" fill="#fff" letter-spacing="1.5">VERDICT PICKS · BUYING GUIDE</text>
{title}
{sub}
<text x="70" y="596" font-size="17" fill="#9FB0C7">{esc(cfg.get("footer", ""))}</text>
</g>
{prod}
<circle cx="1120" cy="90" r="42" fill="#1E8E5A"/><path d="M 1099 91 L 1113 105 L 1142 76" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
'''
    (d / "images" / "cover.svg").write_text(svg, encoding="utf-8")
    print(f"wrote {d/'images'/'cover.svg'}")

if __name__ == "__main__":
    main(sys.argv[1])
