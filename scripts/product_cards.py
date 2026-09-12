#!/usr/bin/env python3
"""Generate flat-style product illustration cards (SVG) from posts/<slug>/cards.json.

Usage: python3 scripts/product_cards.py posts/<slug>
Writes posts/<slug>/images/cards/<id>.svg for every card. Illustrations are original
drawings (no logos, no photos) so they can be hosted and inlined freely.
"""
import json, sys, pathlib, html

W, H = 600, 400
FONT = "-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
NAVY, GREEN, AMBER, PAPER = "#1B2A41", "#1E8E5A", "#C9781B", "#F7F5F0"

def esc(s): return html.escape(str(s), quote=True)

def frame(title, chip, inner, label):
    """Common card frame: paper background, floor shadow, top-left chip, bottom label."""
    chip_w = 16 + int(len(chip) * 7.2)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)} (illustration)">
<rect width="{W}" height="{H}" rx="18" fill="{PAPER}"/>
<ellipse cx="300" cy="318" rx="190" ry="16" fill="#000" opacity="0.07"/>
{inner}
<g font-family="{FONT}">
<rect x="18" y="18" width="{chip_w}" height="28" rx="14" fill="{NAVY}"/>
<text x="{18 + chip_w/2}" y="37" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">{esc(chip)}</text>
<text x="22" y="378" font-size="22" font-weight="700" fill="{NAVY}">{esc(label)}</text>
<text x="578" y="380" text-anchor="end" font-size="11" fill="#999">Illustration</text>
</g>
</svg>
'''

# ---------------------------------------------------------------- robot vacuum (top view)
def draw_robot(a):
    body = a.get("body", "#F2F2F0"); rim = a.get("rim", "#C8C8C3"); accent = a.get("accent", NAVY)
    cx, cy, r = 260, 200, 112
    out = []
    dock = a.get("dock")
    if dock:
        dw, dh = (150, 190) if dock == "omni" else (120, 150)
        dx, dy = 400, 300 - dh
        dcol = a.get("dock_color", "#E4E2DC"); ddark = a.get("dock_dark", "#B9B6AE")
        out.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="18" fill="{dcol}" stroke="{ddark}" stroke-width="3"/>')
        out.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="30" rx="14" fill="{ddark}"/>')
        if dock == "omni":
            out.append(f'<rect x="{dx+18}" y="{dy+50}" width="48" height="70" rx="8" fill="#fff" opacity="0.7"/><rect x="{dx+84}" y="{dy+50}" width="48" height="70" rx="8" fill="#fff" opacity="0.7"/>')
            out.append(f'<text x="{dx+dw/2}" y="{dy+dh-16}" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#666">wash · dry · empty</text>')
        else:
            out.append(f'<rect x="{dx+30}" y="{dy+50}" width="60" height="60" rx="10" fill="#fff" opacity="0.7"/>')
            out.append(f'<text x="{dx+dw/2}" y="{dy+dh-16}" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#666">auto-empty</text>')
    # body
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{body}" stroke="{rim}" stroke-width="6"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r-22}" fill="none" stroke="{rim}" stroke-width="2" opacity="0.6"/>')
    # bumper (front = top)
    out.append(f'<path d="M {cx-95} {cy-58} A {r} {r} 0 0 1 {cx+95} {cy-58}" fill="none" stroke="{rim}" stroke-width="12" stroke-linecap="round" opacity="0.9"/>')
    # turret or flat sensor
    if a.get("turret", True):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="{accent}"/><circle cx="{cx}" cy="{cy}" r="16" fill="#fff" opacity="0.25"/><circle cx="{cx}" cy="{cy}" r="7" fill="#fff" opacity="0.6"/>')
    else:
        out.append(f'<rect x="{cx-40}" y="{cy-r+18}" width="80" height="14" rx="7" fill="{accent}"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{accent}" stroke-width="3" opacity="0.35"/>')
    if a.get("camera"):
        out.append(f'<circle cx="{cx+52}" cy="{cy-r+34}" r="7" fill="#111"/><circle cx="{cx+54}" cy="{cy-r+32}" r="2" fill="#fff"/>')
    # side brush (front-left)
    bx, by = cx-78, cy-70
    out.append(f'<g stroke="{accent}" stroke-width="4" stroke-linecap="round" opacity="0.8"><line x1="{bx}" y1="{by}" x2="{bx-26}" y2="{by-20}"/><line x1="{bx}" y1="{by}" x2="{bx-32}" y2="{by+10}"/><line x1="{bx}" y1="{by}" x2="{bx-8}" y2="{by-32}"/></g><circle cx="{bx}" cy="{by}" r="5" fill="{accent}"/>')
    # mop hint
    if a.get("mop") == "roller":
        out.append(f'<rect x="{cx-60}" y="{cy+62}" width="120" height="14" rx="7" fill="{accent}" opacity="0.35"/>')
    elif a.get("mop") == "pads":
        out.append(f'<circle cx="{cx-34}" cy="{cy+70}" r="16" fill="{accent}" opacity="0.3"/><circle cx="{cx+34}" cy="{cy+70}" r="16" fill="{accent}" opacity="0.3"/>')
    return "\n".join(out)

# ---------------------------------------------------------------- earbuds (open case)
def draw_earbuds(a):
    case = a.get("case", "#111"); lid = a.get("lid", "#2a2a2a"); bud = a.get("bud", "#111"); accent = a.get("accent", "#888")
    style = a.get("style", "stemless")
    out = []
    # lid (open, behind)
    out.append(f'<rect x="150" y="70" width="300" height="120" rx="40" fill="{lid}" opacity="0.92"/>')
    out.append(f'<rect x="150" y="150" width="300" height="140" rx="40" fill="{case}"/>')
    out.append(f'<rect x="170" y="165" width="260" height="110" rx="30" fill="#000" opacity="0.18"/>')
    out.append(f'<circle cx="300" cy="228" r="6" fill="{accent}" opacity="0.8"/>')
    def one(x, flip):
        s = -1 if flip else 1
        if style == "stem":
            return (f'<ellipse cx="{x}" cy="205" rx="26" ry="24" fill="{bud}" stroke="#fff" stroke-width="1" stroke-opacity="0.3"/>'
                    f'<rect x="{x-8 + s*6}" y="218" width="16" height="58" rx="8" fill="{bud}" transform="rotate({-8*s} {x} 240)"/>'
                    f'<circle cx="{x - s*10}" cy="200" r="7" fill="{accent}" opacity="0.7"/>')
        if style == "hook":
            return (f'<ellipse cx="{x}" cy="215" rx="30" ry="26" fill="{bud}"/>'
                    f'<path d="M {x - s*18} 195 C {x - s*40} 170, {x - s*64} 195, {x - s*46} 240" fill="none" stroke="{bud}" stroke-width="10" stroke-linecap="round"/>'
                    f'<circle cx="{x + s*8}" cy="216" r="7" fill="{accent}"/>')
        if style == "openear":
            return (f'<rect x="{x-30}" y="196" width="60" height="30" rx="15" fill="{bud}"/>'
                    f'<path d="M {x - s*18} 200 C {x - s*46} 168, {x - s*70} 200, {x - s*44} 250" fill="none" stroke="{bud}" stroke-width="9" stroke-linecap="round"/>'
                    f'<circle cx="{x + s*10}" cy="211" r="6" fill="{accent}"/>')
        # stemless
        return (f'<ellipse cx="{x}" cy="212" rx="34" ry="30" fill="{bud}"/>'
                f'<circle cx="{x - s*16}" cy="228" r="12" fill="{bud}" stroke="#fff" stroke-opacity="0.35" stroke-width="2"/>'
                f'<circle cx="{x + s*8}" cy="206" r="9" fill="{accent}" opacity="0.85"/>')
    out.append(one(248, False)); out.append(one(352, True))
    return "\n".join(out)

# ---------------------------------------------------------------- glasses (front view)
def draw_glasses(a):
    fr = a.get("frame", "#111"); lens = a.get("lens", "#3a3a3a"); style = a.get("style", "wayfarer")
    disp = a.get("display", "none"); accent = a.get("accent", GREEN)
    out = []
    cy = 205
    if style == "wrap":
        out.append(f'<path d="M 90 175 Q 300 150 510 175 L 500 235 Q 300 265 100 235 Z" fill="{lens}" stroke="{fr}" stroke-width="8" stroke-linejoin="round"/>')
        out.append(f'<path d="M 92 178 L 60 150 M 508 178 L 540 150" stroke="{fr}" stroke-width="10" stroke-linecap="round"/>')
        out.append(f'<rect x="284" y="222" width="32" height="10" rx="5" fill="{fr}"/>')
        lens_boxes = [(110, 170, 180, 60), (310, 170, 180, 60)]
    else:
        if style == "round":
            shapes = [f'<circle cx="{x}" cy="{cy}" r="62" fill="{lens}" stroke="{fr}" stroke-width="9"/>' for x in (205, 395)]
            lens_boxes = [(150, 150, 110, 110), (340, 150, 110, 110)]
        elif style == "xr":
            shapes = [f'<rect x="{x}" y="160" width="165" height="95" rx="26" fill="{lens}" stroke="{fr}" stroke-width="10"/>' for x in (108, 327)]
            lens_boxes = [(108, 160, 165, 95), (327, 160, 165, 95)]
        elif style == "thin":
            shapes = [f'<rect x="{x}" y="165" width="150" height="88" rx="22" fill="{lens}" fill-opacity="0.25" stroke="{fr}" stroke-width="4"/>' for x in (120, 330)]
            lens_boxes = [(120, 165, 150, 88), (330, 165, 150, 88)]
        else:  # wayfarer
            shapes = [f'<path d="M {x} 160 L {x+165} 160 Q {x+178} 160 {x+176} 175 L {x+160} 245 Q {x+156} 258 {x+142} 258 L {x+34} 258 Q {x+18} 258 {x+14} 244 L {x+2} 176 Q 0 160 {x+12} 160 Z" fill="{lens}" stroke="{fr}" stroke-width="10" stroke-linejoin="round"/>' for x in (112, 322)]
            lens_boxes = [(112, 160, 176, 98), (322, 160, 176, 98)]
        out += shapes
        out.append(f'<path d="M 288 178 Q 300 168 312 178" fill="none" stroke="{fr}" stroke-width="9" stroke-linecap="round"/>')
        out.append(f'<path d="M 110 176 L 70 150 M 490 176 L 530 150" stroke="{fr}" stroke-width="10" stroke-linecap="round"/>')
    if a.get("camera"):
        x, y, w, h = lens_boxes[0]
        out.append(f'<circle cx="{x+16}" cy="{y+16}" r="9" fill="#0d0d0d" stroke="#888" stroke-width="2"/><circle cx="{x+19}" cy="{y+13}" r="2.5" fill="#fff"/>')
    if disp in ("right", "both"):
        boxes = lens_boxes if disp == "both" else lens_boxes[1:]
        for (x, y, w, h) in boxes:
            gx, gy = x + w*0.30, y + h*0.30
            out.append(f'<rect x="{gx}" y="{gy}" width="{w*0.42}" height="{h*0.38}" rx="4" fill="{accent}" opacity="0.85"/>')
            out.append(f'<rect x="{gx+6}" y="{gy+6}" width="{w*0.28}" height="4" rx="2" fill="#fff" opacity="0.8"/><rect x="{gx+6}" y="{gy+14}" width="{w*0.2}" height="4" rx="2" fill="#fff" opacity="0.6"/>')
    if style == "xr":
        for (x, y, w, h) in lens_boxes:
            out.append(f'<path d="M {x+20} {y+70} L {x+60} {y+20}" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.25"/>')
    return "\n".join(out)

# ---------------------------------------------------------------- power station (front view)
def draw_power(a):
    size = a.get("size", "mid"); body = a.get("body", "#2E2E2E"); accent = a.get("accent", "#F2A900")
    screen_text = a.get("screen_text", "1,024 Wh"); handle = a.get("handle", "bar")
    dims = {"small": (220, 150), "mid": (300, 190), "large": (340, 220), "xl": (380, 250)}
    w, h = dims.get(size, dims["mid"])
    x, y = 300 - w/2, 315 - h - (26 if size == "xl" else 0)
    out = []
    if handle == "bar":
        out.append(f'<rect x="{x + w*0.2}" y="{y-26}" width="{w*0.6}" height="30" rx="14" fill="{a.get("handle_color", "#C9C9C4")}"/>')
    elif handle == "fold":
        out.append(f'<rect x="{x + w*0.15}" y="{y-22}" width="{w*0.7}" height="34" rx="16" fill="none" stroke="{a.get("handle_color", "#C9C9C4")}" stroke-width="12"/>')
    elif handle == "side":
        out.append(f'<rect x="{x+w-24}" y="{y-60}" width="14" height="70" rx="6" fill="{a.get("handle_color", "#C9C9C4")}"/><rect x="{x+w-64}" y="{y-66}" width="60" height="14" rx="7" fill="{a.get("handle_color", "#C9C9C4")}"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{body}"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="18" rx="9" fill="{accent}"/>')
    # screen
    sw, sh = w*0.36, h*0.36
    sx, sy = x + w*0.08, y + h*0.2
    out.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="10" fill="{NAVY}" stroke="#000" stroke-width="2"/>')
    out.append(f'<text x="{sx+sw/2}" y="{sy+sh/2+8}" text-anchor="middle" font-family="{FONT}" font-size="{max(14, int(sw/6.2))}" font-weight="700" fill="#8FD3AE">{esc(screen_text)}</text>')
    # outlets 2x2 (or a USB-C panel for DC-only units)
    ox, oy = x + w*0.52, y + h*0.2
    cell = min(w*0.19, h*0.3)
    if a.get("no_ac"):
        for i in range(2):
            for j in range(2):
                cx0 = ox + j*(cell+10); cy0 = oy + i*(cell+8)
                out.append(f'<rect x="{cx0}" y="{cy0+cell*0.3}" width="{cell}" height="{cell*0.4}" rx="{cell*0.2}" fill="#F1F1EE"/>')
                out.append(f'<rect x="{cx0+cell*0.2}" y="{cy0+cell*0.42}" width="{cell*0.6}" height="{cell*0.16}" rx="{cell*0.08}" fill="{body}"/>')
        out.append(f'<text x="{ox+cell+5}" y="{oy+2*cell+22}" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#F1F1EE" opacity="0.8">USB-C only</text>')
    for i in range(2 if not a.get("no_ac") else 0):
        for j in range(2):
            cx0 = ox + j*(cell+10); cy0 = oy + i*(cell+8)
            out.append(f'<rect x="{cx0}" y="{cy0}" width="{cell}" height="{cell}" rx="8" fill="#F1F1EE"/>')
            out.append(f'<rect x="{cx0+cell*0.28}" y="{cy0+cell*0.3}" width="{cell*0.12}" height="{cell*0.32}" rx="2" fill="{body}"/><rect x="{cx0+cell*0.6}" y="{cy0+cell*0.3}" width="{cell*0.12}" height="{cell*0.32}" rx="2" fill="{body}"/>')
    # usb row under screen
    uy = sy + sh + 14
    for k in range(3):
        out.append(f'<rect x="{sx + k*(sw/3)}" y="{uy}" width="{sw/3 - 8}" height="12" rx="4" fill="#F1F1EE" opacity="0.85"/>')
    if a.get("wheels") or size == "xl":
        out.append(f'<circle cx="{x+40}" cy="{y+h+14}" r="18" fill="#222" stroke="#555" stroke-width="4"/><circle cx="{x+w-40}" cy="{y+h+14}" r="18" fill="#222" stroke="#555" stroke-width="4"/>')
    if a.get("bolt", True):
        out.append(f'<path d="M {x+w-46} {y+h-52} l -12 24 h 12 l -6 22 l 20 -30 h -12 l 8 -16 z" fill="{accent}"/>')
    return "\n".join(out)

DRAW = {"robot": draw_robot, "earbuds": draw_earbuds, "glasses": draw_glasses, "power": draw_power}

def card_svg(category, c):
    inner = DRAW[category](c.get("art", {}))
    return frame(c["name"], c.get("chip", ""), inner, c.get("short", c["name"]))

def main(post_dir):
    d = pathlib.Path(post_dir)
    spec = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    outdir = d / "images" / "cards"; outdir.mkdir(parents=True, exist_ok=True)
    for c in spec["cards"]:
        (outdir / f"{c['id']}.svg").write_text(card_svg(spec["category"], c), encoding="utf-8")
    print(f"wrote {len(spec['cards'])} cards to {outdir}")

if __name__ == "__main__":
    main(sys.argv[1])
