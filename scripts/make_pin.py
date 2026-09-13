#!/usr/bin/env python3
"""Pinterest pin (1000x1500, 2:3) with the hero render, from posts/<slug>/cover.json + cards.json.

cover.json keys used: hero, title[], pin[] (3 short bullets), url (live post URL, for the save button).
Writes posts/<slug>/images/pin.svg  (render with scripts/render_png.mjs -> pin.png at 2000x3000).
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
    prod = render_product(spec["category"], hero.get("art", {}), "pin", scale=1.3, tx=110, ty=560, with_studio=False)
    lines = cfg["title"]
    fs = 96 if max(len(l) for l in lines) <= 14 else 84
    title = "".join(f'<text x="500" y="{250 + i*(fs+10)}" text-anchor="middle" font-size="{fs}" font-weight="800" fill="{"#8FD3AE" if l.startswith("of ") else "#fff"}">{esc(l)}</text>' for i, l in enumerate(lines))
    bullets = "".join(f'<g transform="translate(0 {1190 + i*66})"><circle cx="110" cy="0" r="18" fill="#1E8E5A"/><path d="M 101 1 L 108 8 L 120 -7" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/><text x="148" y="10" font-size="34" fill="#F1F4F8">{esc(b)}</text></g>' for i, b in enumerate(cfg.get("pin", [])[:3]))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1500" role="img" aria-label="{esc(cfg.get("alt", " ".join(lines)))}">
<defs>
<radialGradient id="pin-spot" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#3A4D6B"/><stop offset="0.6" stop-color="#24344D"/><stop offset="1" stop-color="#1B2A41" stop-opacity="0"/></radialGradient>
<radialGradient id="pin-halo" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffffff" stop-opacity="0.22"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1000" height="1500" fill="#1B2A41"/>
<ellipse cx="500" cy="820" rx="520" ry="380" fill="url(#pin-spot)"/>
<ellipse cx="500" cy="800" rx="340" ry="240" fill="url(#pin-halo)"/>
<g font-family="{FONT}">
<rect x="310" y="96" width="380" height="44" rx="22" fill="#1E8E5A"/>
<text x="500" y="126" text-anchor="middle" font-size="19" font-weight="700" fill="#fff" letter-spacing="1.8">VERDICT PICKS · BUYING GUIDE</text>
{title}
{prod}
<rect x="60" y="1130" width="880" height="250" rx="24" fill="#ffffff" fill-opacity="0.06" stroke="#ffffff" stroke-opacity="0.12"/>
{bullets}
<text x="500" y="1448" text-anchor="middle" font-size="30" font-weight="700" fill="#8FD3AE" letter-spacing="1">acts39.blogspot.com</text>
</g>
<circle cx="900" cy="118" r="44" fill="#1E8E5A"/><path d="M 878 119 L 893 134 L 923 103" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
'''
    (d / "images" / "pin.svg").write_text(svg, encoding="utf-8")
    print(f"wrote {d/'images'/'pin.svg'}")

if __name__ == "__main__":
    main(sys.argv[1])
