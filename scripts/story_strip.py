#!/usr/bin/env python3
"""Four-panel "in real life" comic strips (SVG) from posts/<slug>/strips.json.

Usage: python3 scripts/story_strip.py posts/<slug>
Each strip: {"id", "card" (optional product to render), "title", "panels": [{"glyph", "head", "text", "product": bool}]}
Writes posts/<slug>/images/strips/<id>.svg (1200x440).
"""
import json, sys, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from product_cards import render_product, FONT, NAVY, GREEN, AMBER
from host import draw_host

def esc(s): return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- glyphs (drawn in a 140x140 box, origin top-left)
def g_clock(c="#1B2A41"):
    return f'<circle cx="70" cy="70" r="52" fill="#fff" stroke="{c}" stroke-width="8"/><path d="M 70 70 L 70 36 M 70 70 L 94 82" stroke="{c}" stroke-width="8" stroke-linecap="round"/><circle cx="70" cy="70" r="5" fill="{c}"/>'
def g_phone(c="#1B2A41"):
    return f'<rect x="42" y="14" width="56" height="112" rx="12" fill="{c}"/><rect x="48" y="26" width="44" height="80" rx="4" fill="#DCE7F5"/><circle cx="70" cy="116" r="4" fill="#fff"/>'
def g_cable(c="#1B2A41"):
    return f'<path d="M 18 100 C 40 60, 60 130, 84 90 S 110 50, 124 74" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round"/><rect x="10" y="88" width="22" height="24" rx="4" fill="{c}"/><path d="M 96 42 q 18 -14 30 4 l -8 22 q -12 -6 -22 -2 z" fill="{AMBER}" opacity="0.9"/>'
def g_sofa(c="#1B2A41"):
    return f'<rect x="16" y="46" width="108" height="46" rx="12" fill="{c}"/><rect x="8" y="70" width="124" height="30" rx="10" fill="{c}"/><rect x="16" y="100" width="10" height="20" fill="{c}"/><rect x="114" y="100" width="10" height="20" fill="{c}"/><path d="M 30 116 L 110 116" stroke="{GREEN}" stroke-width="6" stroke-linecap="round" stroke-dasharray="4 8"/>'
def g_dock(c="#1B2A41"):
    return f'<rect x="40" y="18" width="60" height="100" rx="12" fill="#E4E2DC" stroke="{c}" stroke-width="5"/><rect x="40" y="18" width="60" height="18" rx="9" fill="{c}"/><rect x="50" y="46" width="18" height="40" rx="5" fill="#9fd3ff" opacity="0.8"/><rect x="72" y="46" width="18" height="40" rx="5" fill="#9fd3ff" opacity="0.8"/><path d="M 52 106 L 88 106" stroke="{c}" stroke-width="5" stroke-linecap="round"/>'
def g_fridge(c="#1B2A41"):
    return f'<rect x="38" y="10" width="64" height="120" rx="8" fill="#F1F1EE" stroke="{c}" stroke-width="6"/><path d="M 38 56 L 102 56" stroke="{c}" stroke-width="6"/><rect x="88" y="26" width="6" height="18" rx="3" fill="{c}"/><rect x="88" y="66" width="6" height="30" rx="3" fill="{c}"/>'
def g_moon(c="#1B2A41"):
    return f'<circle cx="70" cy="70" r="50" fill="#1B2A41"/><circle cx="90" cy="56" r="42" fill="#F7F5F0"/><circle cx="34" cy="40" r="4" fill="#F2C94C"/><circle cx="110" cy="112" r="3" fill="#F2C94C"/><circle cx="26" cy="104" r="3" fill="#F2C94C"/>'
def g_sun(c="#1B2A41"):
    rays = "".join(f'<line x1="70" y1="70" x2="{70 + 58 * __import__("math").cos(a)}" y2="{70 + 58 * __import__("math").sin(a)}" stroke="{AMBER}" stroke-width="7" stroke-linecap="round"/>' for a in [i * 3.14159 / 6 for i in range(12)])
    return rays + f'<circle cx="70" cy="70" r="30" fill="#F2C94C" stroke="{AMBER}" stroke-width="4"/>'
def g_bolt(c="#1B2A41"):
    return f'<path d="M 82 10 L 40 78 h 28 l -12 52 l 44 -70 h -28 l 12 -50 z" fill="{GREEN}" stroke="{c}" stroke-width="5" stroke-linejoin="round"/>'
def g_wifi(c="#1B2A41"):
    return f'<path d="M 20 60 A 70 70 0 0 1 120 60" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round"/><path d="M 38 80 A 45 45 0 0 1 102 80" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round"/><path d="M 56 100 A 20 20 0 0 1 84 100" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round"/><circle cx="70" cy="118" r="7" fill="{GREEN}"/>'
def g_check(c="#1B2A41"):
    return f'<circle cx="70" cy="70" r="54" fill="{GREEN}"/><path d="M 42 72 L 62 92 L 100 50" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
def g_train(c="#1B2A41"):
    return f'<rect x="20" y="30" width="100" height="70" rx="16" fill="{c}"/><rect x="32" y="44" width="30" height="24" rx="4" fill="#DCE7F5"/><rect x="78" y="44" width="30" height="24" rx="4" fill="#DCE7F5"/><circle cx="44" cy="110" r="10" fill="{c}"/><circle cx="96" cy="110" r="10" fill="{c}"/><path d="M 8 20 q 10 -12 20 0 M 112 20 q 10 -12 20 0" stroke="{AMBER}" stroke-width="5" fill="none" stroke-linecap="round"/>'
def g_translate(c="#1B2A41"):
    return f'<path d="M 14 24 h 78 a 10 10 0 0 1 10 10 v 40 a 10 10 0 0 1 -10 10 h -40 l -18 16 v -16 h -20 a 10 10 0 0 1 -10 -10 v -40 a 10 10 0 0 1 10 -10 z" fill="#fff" stroke="{c}" stroke-width="6"/><text x="53" y="64" text-anchor="middle" font-family="{FONT}" font-size="26" font-weight="700" fill="{c}">A→文</text><path d="M 76 84 h 50 a 8 8 0 0 1 8 8 v 26 a 8 8 0 0 1 -8 8 h -20 l -10 10 v -10 h -20 a 8 8 0 0 1 -8 -8 v -26 a 8 8 0 0 1 8 -8 z" fill="{GREEN}"/>'
def g_camera(c="#1B2A41"):
    return f'<rect x="16" y="40" width="108" height="72" rx="14" fill="{c}"/><rect x="48" y="26" width="40" height="18" rx="6" fill="{c}"/><circle cx="70" cy="76" r="24" fill="#DCE7F5"/><circle cx="70" cy="76" r="14" fill="{c}"/><circle cx="64" cy="70" r="4" fill="#fff"/><circle cx="108" cy="54" r="5" fill="{GREEN}"/>'
def g_gym(c="#1B2A41"):
    return f'<rect x="10" y="50" width="20" height="40" rx="6" fill="{c}"/><rect x="110" y="50" width="20" height="40" rx="6" fill="{c}"/><rect x="26" y="60" width="14" height="20" rx="4" fill="{c}"/><rect x="100" y="60" width="14" height="20" rx="4" fill="{c}"/><rect x="38" y="64" width="64" height="12" rx="6" fill="{c}"/><path d="M 30 116 h 80" stroke="{AMBER}" stroke-width="6" stroke-linecap="round"/>'
def g_bed(c="#1B2A41"):
    return f'<rect x="12" y="70" width="116" height="30" rx="8" fill="{c}"/><rect x="20" y="52" width="40" height="22" rx="8" fill="#F1F1EE" stroke="{c}" stroke-width="4"/><rect x="12" y="98" width="10" height="24" fill="{c}"/><rect x="118" y="98" width="10" height="24" fill="{c}"/><rect x="96" y="30" width="30" height="22" rx="5" fill="{GREEN}"/><path d="M 100 30 q 12 -18 24 0" stroke="{c}" stroke-width="4" fill="none"/>'
def g_plane(c="#1B2A41"):
    return f'<path d="M 30 96 h 72 a 12 12 0 0 1 12 12 v 12 h -96 v -12 a 12 12 0 0 1 12 -12 z" fill="{c}"/><rect x="34" y="40" width="48" height="60" rx="10" fill="{c}"/><rect x="88" y="36" width="34" height="24" rx="4" fill="#DCE7F5" stroke="{c}" stroke-width="4"/><path d="M 96 48 l 8 -6 l 8 6 l -8 6 z" fill="{GREEN}"/>'
def g_battery(c="#1B2A41"):
    return f'<rect x="16" y="46" width="100" height="50" rx="10" fill="#fff" stroke="{c}" stroke-width="7"/><rect x="116" y="60" width="12" height="22" rx="4" fill="{c}"/><rect x="24" y="54" width="84" height="34" rx="6" fill="{GREEN}"/><path d="M 74 50 L 60 74 h 12 l -6 22 l 20 -30 h -12 l 6 -16 z" fill="#fff"/>'
def g_dog(c="#1B2A41"):
    return f'<ellipse cx="66" cy="84" rx="40" ry="26" fill="{c}"/><circle cx="104" cy="66" r="20" fill="{c}"/><path d="M 92 50 l -8 -18 l 16 8 z M 116 50 l 8 -18 l -16 8 z" fill="{c}"/><circle cx="110" cy="64" r="3" fill="#fff"/><path d="M 30 96 q -14 -6 -10 -22" stroke="{c}" stroke-width="8" fill="none" stroke-linecap="round"/><rect x="44" y="104" width="10" height="20" fill="{c}"/><rect x="80" y="104" width="10" height="20" fill="{c}"/><path d="M 20 40 q 8 -12 16 0 q 8 -12 16 0" stroke="{AMBER}" stroke-width="4" fill="none"/>'
def g_music(c="#1B2A41"):
    return f'<path d="M 54 30 v 66 M 54 30 q 30 -6 44 12 q -10 20 -44 12" stroke="{c}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/><ellipse cx="42" cy="100" rx="16" ry="12" fill="{c}"/><path d="M 100 60 q 14 14 0 30 M 112 46 q 26 26 0 58" stroke="{GREEN}" stroke-width="6" fill="none" stroke-linecap="round"/>'
def g_map(c="#1B2A41"):
    return f'<path d="M 70 126 C 40 90, 26 72, 26 54 a 44 44 0 0 1 88 0 c 0 18 -14 36 -44 72 z" fill="{GREEN}" stroke="{c}" stroke-width="5"/><circle cx="70" cy="54" r="16" fill="#fff"/><path d="M 62 54 l 6 6 l 12 -12" stroke="{c}" stroke-width="5" fill="none" stroke-linecap="round"/>'
def g_warning(c="#1B2A41"):
    return f'<path d="M 70 14 L 128 118 H 12 Z" fill="{AMBER}" stroke="{c}" stroke-width="5" stroke-linejoin="round"/><rect x="64" y="48" width="12" height="38" rx="5" fill="#fff"/><circle cx="70" cy="100" r="7" fill="#fff"/>'
def g_home(c="#1B2A41"):
    return f'<path d="M 16 70 L 70 22 L 124 70" fill="none" stroke="{c}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><rect x="32" y="66" width="76" height="56" rx="6" fill="{c}"/><rect x="60" y="88" width="20" height="34" rx="3" fill="#F2C94C"/>'

GLYPHS = {"clock": g_clock, "phone": g_phone, "cable": g_cable, "sofa": g_sofa, "dock": g_dock, "fridge": g_fridge, "moon": g_moon, "sun": g_sun,
          "bolt": g_bolt, "wifi": g_wifi, "check": g_check, "train": g_train, "translate": g_translate, "camera": g_camera, "gym": g_gym,
          "bed": g_bed, "plane": g_plane, "battery": g_battery, "dog": g_dog, "music": g_music, "map": g_map, "warning": g_warning, "home": g_home}

def strip_svg(strip, category, art):
    W, H = 1200, 440
    n = len(strip["panels"]); gap = 18; pw = (W - 40 - gap * (n - 1)) / n
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(strip["title"])}">',
           f'<rect width="{W}" height="{H}" rx="18" fill="#F7F5F0"/>',
           f'<text x="24" y="40" font-family="{FONT}" font-size="24" font-weight="800" fill="{NAVY}">{esc(strip["title"])}</text>',
           f'<text x="{W-24}" y="40" text-anchor="end" font-family="{FONT}" font-size="14" fill="#888">in real life · 4 panels</text>']
    tones = ["#DCE7F5", "#E4F3EA", "#FBEBD2", "#EDE9F7"]
    for i, p in enumerate(strip["panels"]):
        x = 20 + i * (pw + gap); y = 62; ph = H - 62 - 20
        out.append(f'<rect x="{x}" y="{y}" width="{pw}" height="{ph}" rx="16" fill="#fff" stroke="{NAVY}" stroke-width="4"/>')
        out.append(f'<rect x="{x+4}" y="{y+4}" width="{pw-8}" height="{ph*0.56}" rx="12" fill="{tones[i % 4]}"/>')
        # step number
        out.append(f'<circle cx="{x+30}" cy="{y+30}" r="18" fill="{NAVY}"/><text x="{x+30}" y="{y+37}" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="800" fill="#fff">{i+1}</text>')
        # art: host, product render and/or glyph
        host = p.get("host")
        if host:
            hp = host if isinstance(host, dict) else {"pose": host}
            gl_art = {"frame": art.get("frame", "#111"), "style": "round" if art.get("style") == "round" else "wayfarer"} if hp.get("glasses") else None
            eb = art.get("bud", "#222") if hp.get("earbud") else None
            out.append(draw_host(f"h{i}", hp.get("pose", "present"), tx=x + 8, ty=y + 10, scale=0.5, glasses=gl_art, earbud=eb, flip=hp.get("flip", False)))
        if p.get("product"):
            px = x + pw/2 - 108 if not host else x + pw - 178
            py = y + 22 if not host else y + 60
            out.append(render_product(category, art, f"s{i}", scale=0.36 if not host else 0.28, tx=px, ty=py, with_studio=False))
        gl = p.get("glyph")
        if gl and gl in GLYPHS:
            if host: gx, gy, sc = x + pw - 74, y + 14, 0.42
            elif p.get("product"): gx, gy, sc = x + pw - 96, y + 20, 0.55
            else: gx, gy, sc = x + pw/2 - 70, y + 44, 1.0
            out.append(f'<g transform="translate({gx} {gy}) scale({sc})">{GLYPHS[gl]()}</g>')
        # captions
        cy = y + ph*0.56 + 34
        out.append(f'<text x="{x+16}" y="{cy}" font-family="{FONT}" font-size="17" font-weight="800" fill="{NAVY}">{esc(p["head"])}</text>')
        lines = p.get("text", "")
        if isinstance(lines, str):
            # naive wrap at ~34 chars
            words = lines.split(); lines = []; cur = ""
            for w in words:
                if len(cur) + len(w) + 1 > 31: lines.append(cur); cur = w
                else: cur = (cur + " " + w).strip()
            if cur: lines.append(cur)
        for k, ln in enumerate(lines[:4]):
            out.append(f'<text x="{x+16}" y="{cy + 26 + k*21}" font-family="{FONT}" font-size="15.5" fill="#333">{esc(ln)}</text>')
    out.append('</svg>')
    return "\n".join(out)

def main(post_dir):
    d = pathlib.Path(post_dir)
    spec = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    strips = json.loads((d / "strips.json").read_text(encoding="utf-8"))["strips"]
    outdir = d / "images" / "strips"; outdir.mkdir(parents=True, exist_ok=True)
    cards = {c["id"]: c for c in spec["cards"]}
    for s in strips:
        art = cards[s["card"]].get("art", {}) if s.get("card") else {}
        (outdir / f"{s['id']}.svg").write_text(strip_svg(s, spec["category"], art), encoding="utf-8")
    print(f"wrote {len(strips)} strips to {outdir}")

if __name__ == "__main__":
    main(sys.argv[1])
