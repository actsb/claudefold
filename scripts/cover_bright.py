"""Bright, photo-led cover (1200x630) and pin (1000x1500): warm gradient, a circular photo of the owner's dog
(or the hero render when there is no photo), the related products as white chips, navy title.
Used by make_cover.py / make_pin.py when cover.json has "style": "bright"; optional keys: photo (path under the post
folder), products (card ids, up to 3), title_size.
"""
import base64, html, mimetypes, pathlib
from product_cards import render_product, FONT

NAVY, GREEN = "#1B2A41", "#1E8E5A"
def esc(s): return html.escape(str(s), quote=True)

def photo_uri(d, rel):
    p = pathlib.Path(d) / rel; mime = mimetypes.guess_type(str(p))[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

def chip(spec, cid, x, y, w=168, h=112, uid="chip"):
    c = next(c for c in spec["cards"] if c["id"] == cid)
    g = render_product(c.get("category", spec["category"]), c.get("art", {}), f"{uid}{cid}", scale=1.0, tx=0, ty=0, with_studio=False)
    return (f'<g transform="translate({x} {y})"><rect x="6" y="10" width="{w}" height="{h}" rx="18" fill="{NAVY}" opacity="0.12"/>'
            f'<rect width="{w}" height="{h}" rx="18" fill="#fff"/><rect width="{w}" height="{h}" rx="18" fill="none" stroke="#E3E1DB"/>'
            f'<svg x="8" y="6" width="{w-16}" height="{h-12}" viewBox="60 40 480 320" preserveAspectRatio="xMidYMid meet">{g}</svg></g>')

def picture(d, cfg, spec, cx, cy, r, uid):
    ring = f'<circle cx="{cx}" cy="{cy}" r="{r+12}" fill="#fff"/><circle cx="{cx}" cy="{cy}" r="{r+12}" fill="none" stroke="{GREEN}" stroke-width="6"/>'
    if cfg.get("photo"):
        return (f'<clipPath id="{uid}-pc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>' + ring +
                f'<image href="{photo_uri(d, cfg["photo"])}" x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{uid}-pc)"/>')
    hero = next(c for c in spec["cards"] if c["id"] == cfg["hero"]); s = r / 285
    return ring + render_product(hero.get("category", spec["category"]), hero.get("art", {}), uid + "hero", scale=s, tx=cx - 300 * s, ty=cy - 195 * s, with_studio=False)

DEFS = '''<defs>
<linearGradient id="{u}-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFF6E3"/><stop offset="0.55" stop-color="#F7F5F0"/><stop offset="1" stop-color="#DDF2E5"/></linearGradient>
<radialGradient id="{u}-sun" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#FFD27A" stop-opacity="0.85"/><stop offset="1" stop-color="#FFD27A" stop-opacity="0"/></radialGradient>
<radialGradient id="{u}-leaf" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#8FD3AE" stop-opacity="0.7"/><stop offset="1" stop-color="#8FD3AE" stop-opacity="0"/></radialGradient>
</defs>'''

def wrap_sub(lines, width=46, max_lines=3):
    """Re-wrap a subtitle written for the wide dark layout into the narrower bright column, keeping the author's line breaks."""
    import textwrap
    out = [w for l in lines for w in (textwrap.wrap(l, width=width) or [""])]
    if len(out) > max_lines: out = out[:max_lines - 1] + [textwrap.shorten(" ".join(out[max_lines - 1:]), width=width, placeholder="…")]
    return out

def cover(d, cfg, spec):
    W, H = 1200, 630; u = "bc"
    fs = min(cfg.get("title_size", 78), int(690 / (max(len(l) for l in cfg["title"]) * 0.56)))
    title = "".join(f'<text x="64" y="{236 + i*(fs+14)}" font-size="{fs}" font-weight="800" fill="{NAVY}">{esc(l)}</text>' for i, l in enumerate(cfg["title"]))
    sub = "".join(f'<text x="64" y="{468 + i*30}" font-size="23" fill="#3A4453">{esc(l)}</text>' for i, l in enumerate(wrap_sub(cfg["subtitle"])))
    chips = "".join(chip(spec, cid, 700 + i * 164, 478, w=150, h=104, uid="c") for i, cid in enumerate(cfg.get("products", [])[:3]))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(cfg.get("alt", " ".join(cfg["title"])))}">' + DEFS.format(u=u) +
            f'<rect width="{W}" height="{H}" fill="url(#{u}-bg)"/><circle cx="1010" cy="120" r="300" fill="url(#{u}-sun)"/><circle cx="760" cy="560" r="260" fill="url(#{u}-leaf)"/>'
            f'<g font-family="{FONT}"><rect x="64" y="70" width="330" height="36" rx="18" fill="{GREEN}"/>'
            f'<text x="229" y="95" text-anchor="middle" font-size="16" font-weight="700" fill="#fff" letter-spacing="1.5">VERDICT PICKS · BUYING GUIDE</text>{title}{sub}'
            f'<text x="64" y="612" font-size="17" fill="#6B7684">{esc(cfg.get("footer", ""))}</text></g>'
            + picture(d, cfg, spec, 960, 265, 200, u) + chips +
            f'<circle cx="1120" cy="80" r="40" fill="{GREEN}"/><path d="M 1100 81 L 1113 94 L 1141 67" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>\n')

def pin(d, cfg, spec):
    W, H = 1000, 1500; u = "bp"; lines = cfg["title"]; fs = 92 if max(len(l) for l in lines) <= 14 else 78
    title = "".join(f'<text x="500" y="{250 + i*(fs+8)}" text-anchor="middle" font-size="{fs}" font-weight="800" fill="{NAVY}">{esc(l)}</text>' for i, l in enumerate(lines))
    prods = cfg.get("products", [])[:3]; cw = 250; x0 = 500 - (len(prods) * cw + (len(prods) - 1) * 24) / 2
    chips = "".join(chip(spec, cid, x0 + i * (cw + 24), 1052, w=cw, h=150, uid="p") for i, cid in enumerate(prods))
    bullets = "".join(f'<g transform="translate(0 {1262 + i*58})"><circle cx="100" cy="0" r="17" fill="{GREEN}"/><path d="M 92 1 L 98 7 L 109 -6" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
                      f'<text x="136" y="10" font-size="30" font-weight="600" fill="{NAVY}">{esc(b)}</text></g>' for i, b in enumerate(cfg.get("pin", [])[:3]))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(cfg.get("alt", " ".join(lines)))}">' + DEFS.format(u=u) +
            f'<rect width="{W}" height="{H}" fill="url(#{u}-bg)"/><circle cx="860" cy="120" r="320" fill="url(#{u}-sun)"/><circle cx="160" cy="1380" r="320" fill="url(#{u}-leaf)"/>'
            f'<g font-family="{FONT}"><rect x="310" y="96" width="380" height="44" rx="22" fill="{GREEN}"/>'
            f'<text x="500" y="126" text-anchor="middle" font-size="19" font-weight="700" fill="#fff" letter-spacing="1.8">VERDICT PICKS · BUYING GUIDE</text>{title}</g>'
            + picture(d, cfg, spec, 500, 760, 260, u) + chips +
            f'<g font-family="{FONT}"><rect x="60" y="1225" width="880" height="190" rx="24" fill="#fff" fill-opacity="0.75" stroke="#E3E1DB"/>{bullets}'
            f'<text x="500" y="1462" text-anchor="middle" font-size="30" font-weight="700" fill="{GREEN}" letter-spacing="1">acts39.blogspot.com</text></g>'
            f'<circle cx="900" cy="118" r="44" fill="{GREEN}"/><path d="M 878 119 L 893 134 L 923 103" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>\n')
