#!/usr/bin/env python3
"""Studio-photo style product renders (SVG) from posts/<slug>/cards.json.

Usage: python3 scripts/product_cards.py posts/<slug>
Writes posts/<slug>/images/cards/<id>.svg. Every render is an original drawing
(three-quarter view, gradients, soft shadows, no logos, no photos), so it can be
hosted and inlined freely. Gradient/filter ids are prefixed with the card id so
many cards can be inlined on one page.

Also exposes render_product(category, art, uid, scale, tx, ty) for covers and strips.
"""
import json, sys, pathlib, html, colorsys

W, H = 600, 400
FONT = "-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
NAVY, GREEN, AMBER, PAPER = "#1B2A41", "#1E8E5A", "#C9781B", "#F7F5F0"

def esc(s): return html.escape(str(s), quote=True)

# ---------------------------------------------------------------- colour helpers
def _rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(ch * 2 for ch in h)
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
def _hex(r, g, b): return '#%02x%02x%02x' % tuple(max(0, min(255, round(v * 255))) for v in (r, g, b))
def shade(h, dl):
    """lighten (dl>0) or darken (dl<0) a hex colour by dl in HLS lightness."""
    r, g, b = _rgb(h); hh, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0, min(1, l + dl)); return _hex(*colorsys.hls_to_rgb(hh, l, s))

# ---------------------------------------------------------------- shared defs
def defs(uid, body, accent):
    return f'''<defs>
<radialGradient id="{uid}-bg" cx="50%" cy="38%" r="72%"><stop offset="0" stop-color="#ffffff"/><stop offset="0.7" stop-color="#f3f3f1"/><stop offset="1" stop-color="#e4e4e1"/></radialGradient>
<filter id="{uid}-blur" x="-30%" y="-80%" width="160%" height="300%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="{uid}-soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="{uid}-glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
<linearGradient id="{uid}-front" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="{shade(body, .10)}"/><stop offset="0.55" stop-color="{body}"/><stop offset="1" stop-color="{shade(body, -.09)}"/></linearGradient>
<linearGradient id="{uid}-side" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shade(body, -.06)}"/><stop offset="1" stop-color="{shade(body, -.20)}"/></linearGradient>
<linearGradient id="{uid}-top" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shade(body, .24)}"/><stop offset="1" stop-color="{shade(body, .06)}"/></linearGradient>
<radialGradient id="{uid}-dome" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="{shade(body, .22)}"/><stop offset="0.6" stop-color="{body}"/><stop offset="1" stop-color="{shade(body, -.14)}"/></radialGradient>
<linearGradient id="{uid}-gloss" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity="0.55"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.05"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
<linearGradient id="{uid}-screen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1d2a3a"/><stop offset="1" stop-color="#060a10"/></linearGradient>
<linearGradient id="{uid}-metal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#d9d9d6"/><stop offset="0.35" stop-color="#f4f4f2"/><stop offset="0.65" stop-color="#bdbdb9"/><stop offset="1" stop-color="#e6e6e3"/></linearGradient>
<linearGradient id="{uid}-accent" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shade(accent, .15)}"/><stop offset="1" stop-color="{shade(accent, -.12)}"/></linearGradient>
<linearGradient id="{uid}-lens" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5a6470"/><stop offset="0.45" stop-color="#1c2129"/><stop offset="0.55" stop-color="#2b323c"/><stop offset="1" stop-color="#0c0f14"/></linearGradient>
</defs>'''

def studio(uid, cx=300, cy=326, rx=170, ry=18):
    return (f'<rect width="{W}" height="{H}" rx="18" fill="url(#{uid}-bg)"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity="0.28" filter="url(#{uid}-blur)"/>')

def box3d(uid, x, y, w, h, depth, body, rx=16, skew=0.55):
    """A rounded box in three-quarter view: front face at (x,y,w,h); side & top faces to the right/up."""
    d = depth; dx, dy = d * skew, d * 0.45
    side = f'<path d="M {x+w} {y+rx*0.4} L {x+w+dx} {y-dy+rx*0.4} L {x+w+dx} {y+h-dy-rx*0.4} Q {x+w+dx} {y+h-dy} {x+w+dx-rx*0.3} {y+h-dy} L {x+w} {y+h-rx*0.15} Z" fill="url(#{uid}-side)"/>'
    top = f'<path d="M {x+rx*0.5} {y} L {x+dx+rx*0.5} {y-dy} L {x+w+dx-rx*0.3} {y-dy} Q {x+w+dx} {y-dy} {x+w+dx} {y-dy+rx*0.4} L {x+w} {y+rx*0.4} Q {x+w} {y} {x+w-rx*0.5} {y} Z" fill="url(#{uid}-top)"/>'
    front = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{uid}-front)"/>'
    edge = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="{shade(body, -.25)}" stroke-width="1.2" opacity="0.6"/>'
    gloss = f'<path d="M {x+rx} {y+3} L {x+w-rx} {y+3}" stroke="#fff" stroke-opacity="0.35" stroke-width="2" stroke-linecap="round"/>'
    return side + top + front + edge + gloss

def outlet(uid, x, y, s, body):
    """A US AC outlet face."""
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s*0.16}" fill="#efefec"/>'
            f'<rect x="{x+1.5}" y="{y+1.5}" width="{s-3}" height="{s-3}" rx="{s*0.14}" fill="none" stroke="#c9c9c4" stroke-width="1"/>'
            f'<rect x="{x+s*0.27}" y="{y+s*0.24}" width="{s*0.11}" height="{s*0.30}" rx="1.5" fill="#333"/>'
            f'<rect x="{x+s*0.62}" y="{y+s*0.24}" width="{s*0.11}" height="{s*0.30}" rx="1.5" fill="#333"/>'
            f'<circle cx="{x+s*0.5}" cy="{y+s*0.72}" r="{s*0.08}" fill="#333"/>')

# ---------------------------------------------------------------- robot vacuum (three-quarter top view)
def draw_robot(uid, a):
    body = a.get("body", "#F4F4F1"); accent = a.get("accent", NAVY)
    out = [defs(uid, body, accent), studio(uid, 270, 322, 170, 16)]
    cx, cy, rx, ry, hh = 270, 218, 158, 86, 40
    dock = a.get("dock")
    if dock:
        dw, dh, dd = (120, 175, 52) if dock == "omni" else (96, 132, 42)
        dx, dy = 430, 305 - dh
        dcol = a.get("dock_color", "#ECEAE4")
        out.append(f'<ellipse cx="{dx+dw/2+10}" cy="{dy+dh+6}" rx="{dw*0.75}" ry="10" fill="#000" opacity="0.22" filter="url(#{uid}-blur)"/>')
        out.append(box3d(uid + "d", dx, dy, dw, dh, dd, dcol, rx=14))
        out.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="26" rx="14" fill="{shade(dcol, -.28)}"/><rect x="{dx}" y="{dy+14}" width="{dw}" height="12" fill="{shade(dcol, -.28)}"/>')
        if dock == "omni":
            for k in (0, 1):
                tx = dx + 14 + k * (dw/2 - 10)
                out.append(f'<rect x="{tx}" y="{dy+46}" width="{dw/2-22}" height="72" rx="8" fill="#ffffff" opacity="0.55"/><rect x="{tx+6}" y="{dy+70}" width="{dw/2-34}" height="40" rx="5" fill="#9fd3ff" opacity="0.35"/>')
            out.append(f'<rect x="{dx+12}" y="{dy+dh-40}" width="{dw-24}" height="22" rx="4" fill="{shade(dcol, -.12)}"/>')
        else:
            out.append(f'<rect x="{dx+14}" y="{dy+44}" width="{dw-28}" height="54" rx="8" fill="{shade(dcol, -.10)}"/><rect x="{dx+18}" y="{dy+48}" width="{dw-36}" height="46" rx="6" fill="#ffffff" opacity="0.5"/>')
        out.append(f'<rect x="{dx+dw/2-10}" y="{dy+dh-14}" width="20" height="4" rx="2" fill="{accent}" opacity="0.8"/>')
    # side wall (lower half of ellipse extruded)
    out.append(f'<path d="M {cx-rx} {cy} A {rx} {ry} 0 0 0 {cx+rx} {cy} L {cx+rx} {cy+hh} A {rx} {ry} 0 0 1 {cx-rx} {cy+hh} Z" fill="url(#{uid}-side)"/>')
    # bumper seam on the wall
    out.append(f'<path d="M {cx-rx+2} {cy+14} A {rx} {ry} 0 0 0 {cx+rx-2} {cy+14}" fill="none" stroke="{shade(body, -.30)}" stroke-width="1.5" opacity="0.7"/>')
    # front sensor window on the wall
    out.append(f'<path d="M {cx-58} {cy+ry-2} Q {cx} {cy+ry+8} {cx+58} {cy+ry-2} L {cx+58} {cy+ry+18} Q {cx} {cy+ry+28} {cx-58} {cy+ry+18} Z" fill="#141414"/>')
    out.append(f'<path d="M {cx-40} {cy+ry+4} Q {cx} {cy+ry+11} {cx+40} {cy+ry+4}" stroke="#fff" stroke-opacity="0.25" stroke-width="2" fill="none"/>')
    # top face
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{uid}-dome)"/>')
    out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx-14}" ry="{ry-8}" fill="none" stroke="{shade(body, -.16)}" stroke-width="1.2" opacity="0.7"/>')
    # lid gloss
    out.append(f'<ellipse cx="{cx-40}" cy="{cy-30}" rx="86" ry="26" fill="url(#{uid}-gloss)"/>')
    if a.get("turret", True):
        tcol = a.get("turret_color", "#2B2B2B")
        out.append(f'<path d="M {cx-34} {cy-4} A 34 19 0 0 0 {cx+34} {cy-4} L {cx+34} {cy+12} A 34 19 0 0 1 {cx-34} {cy+12} Z" fill="{shade(tcol, -.12)}"/>')
        out.append(f'<ellipse cx="{cx}" cy="{cy-4}" rx="34" ry="19" fill="{tcol}"/><ellipse cx="{cx}" cy="{cy-4}" rx="24" ry="13" fill="{shade(tcol, .10)}"/>')
        out.append(f'<rect x="{cx-22}" y="{cy+1}" width="44" height="6" rx="3" fill="#0d0d0d" opacity="0.8"/>')
        out.append(f'<ellipse cx="{cx-10}" cy="{cy-10}" rx="12" ry="5" fill="#fff" opacity="0.28"/>')
    else:
        out.append(f'<rect x="{cx-48}" y="{cy+ry-30}" width="96" height="14" rx="7" fill="#101418"/><rect x="{cx-36}" y="{cy+ry-27}" width="40" height="4" rx="2" fill="#fff" opacity="0.25"/>')
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="46" ry="24" fill="none" stroke="{shade(body, -.12)}" stroke-width="1.5" opacity="0.8"/>')
    if a.get("camera"):
        out.append(f'<circle cx="{cx+64}" cy="{cy+ry-20}" r="7" fill="#0a0a0a"/><circle cx="{cx+62}" cy="{cy+ry-22}" r="2.2" fill="#fff" opacity="0.8"/>')
    # buttons
    out.append(f'<rect x="{cx-26}" y="{cy-ry+22}" width="20" height="6" rx="3" fill="{shade(body, -.22)}"/><rect x="{cx+6}" y="{cy-ry+22}" width="20" height="6" rx="3" fill="{shade(body, -.22)}"/>')
    # side brush at front-left of the wall
    bx, by = cx - rx + 26, cy + hh - 4
    out.append(f'<g stroke="{accent}" stroke-width="3.5" stroke-linecap="round" opacity="0.9"><line x1="{bx}" y1="{by}" x2="{bx-28}" y2="{by+10}"/><line x1="{bx}" y1="{by}" x2="{bx-20}" y2="{by+24}"/><line x1="{bx}" y1="{by}" x2="{bx-2}" y2="{by+28}"/></g><circle cx="{bx}" cy="{by}" r="4.5" fill="{shade(accent, -.1)}"/>')
    if a.get("mop") == "roller":
        out.append(f'<rect x="{cx-80}" y="{cy+hh+2}" width="160" height="10" rx="5" fill="{shade(accent, .1)}" opacity="0.55"/>')
    elif a.get("mop") == "pads":
        out.append(f'<ellipse cx="{cx-60}" cy="{cy+hh+6}" rx="22" ry="7" fill="{shade(accent, .1)}" opacity="0.5"/><ellipse cx="{cx+60}" cy="{cy+hh+6}" rx="22" ry="7" fill="{shade(accent, .1)}" opacity="0.5"/>')
    return "\n".join(out)

# ---------------------------------------------------------------- earbuds (open case, three-quarter)
def draw_earbuds(uid, a):
    case = a.get("case", "#111"); bud = a.get("bud", "#111"); accent = a.get("accent", "#888"); style = a.get("style", "stemless")
    out = [defs(uid, case, accent), studio(uid, 300, 322, 150, 16)]
    # lid: open, tilted back
    lid_in = shade(case, .14)
    out.append(f'<g transform="translate(300 175) skewX(-6)"><rect x="-118" y="-92" width="236" height="104" rx="42" fill="url(#{uid}-side)"/><rect x="-106" y="-80" width="212" height="82" rx="34" fill="{lid_in}"/><rect x="-96" y="-74" width="190" height="30" rx="15" fill="#fff" opacity="0.10"/></g>')
    # case body (front + top faces)
    out.append(box3d(uid, 180, 185, 240, 118, 26, case, rx=44, skew=0.5))
    # cavity
    out.append(f'<ellipse cx="300" cy="196" rx="112" ry="26" fill="{shade(case, -.35)}"/><ellipse cx="300" cy="194" rx="104" ry="20" fill="{shade(case, -.22)}"/>')
    out.append(f'<circle cx="300" cy="262" r="5" fill="{accent}" opacity="0.9"/><circle cx="300" cy="262" r="2" fill="#fff" opacity="0.6"/>')
    def one(x, flip):
        s = -1 if flip else 1
        g = f'''<radialGradient id="{uid}-b{int(x)}" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="{shade(bud, .30)}"/><stop offset="0.55" stop-color="{bud}"/><stop offset="1" stop-color="{shade(bud, -.22)}"/></radialGradient>'''
        parts = [g, f'<ellipse cx="{x}" cy="{212}" rx="30" ry="9" fill="#000" opacity="0.35" filter="url(#{uid}-soft)"/>']
        if style == "stem":
            parts.append(f'<rect x="{x-9 + s*8}" y="186" width="18" height="66" rx="9" fill="url(#{uid}-b{int(x)})" transform="rotate({-9*s} {x} 200)"/>')
            parts.append(f'<ellipse cx="{x}" cy="176" rx="24" ry="22" fill="url(#{uid}-b{int(x)})"/>')
            parts.append(f'<ellipse cx="{x - s*9}" cy="168" rx="8" ry="6" fill="#fff" opacity="0.45"/>')
            parts.append(f'<rect x="{x-3 + s*8}" y="228" width="6" height="14" rx="3" fill="{shade(bud, -.25)}" transform="rotate({-9*s} {x} 200)"/>')
        elif style == "hook":
            parts.append(f'<path d="M {x - s*16} 176 C {x - s*40} 150, {x - s*66} 178, {x - s*46} 222" fill="none" stroke="{bud}" stroke-width="11" stroke-linecap="round"/>')
            parts.append(f'<path d="M {x - s*18} 173 C {x - s*40} 150, {x - s*62} 176, {x - s*46} 216" fill="none" stroke="#fff" stroke-opacity="0.18" stroke-width="3" stroke-linecap="round"/>')
            parts.append(f'<ellipse cx="{x}" cy="192" rx="30" ry="26" fill="url(#{uid}-b{int(x)})"/><circle cx="{x + s*8}" cy="190" r="8" fill="{accent}"/><ellipse cx="{x - s*8}" cy="180" rx="9" ry="6" fill="#fff" opacity="0.4"/>')
        elif style == "openear":
            parts.append(f'<path d="M {x - s*16} 178 C {x - s*46} 146, {x - s*72} 182, {x - s*44} 228" fill="none" stroke="{bud}" stroke-width="10" stroke-linecap="round"/>')
            parts.append(f'<rect x="{x-32}" y="176" width="64" height="30" rx="15" fill="url(#{uid}-b{int(x)})"/><circle cx="{x + s*10}" cy="191" r="6" fill="{accent}"/><rect x="{x-20}" y="181" width="26" height="5" rx="2.5" fill="#fff" opacity="0.35"/>')
        else:  # stemless pebble
            parts.append(f'<ellipse cx="{x}" cy="190" rx="36" ry="31" fill="url(#{uid}-b{int(x)})"/>')
            parts.append(f'<circle cx="{x - s*17}" cy="205" r="13" fill="{shade(bud, -.05)}"/><circle cx="{x - s*17}" cy="205" r="9" fill="{shade(bud, -.3)}"/>')
            parts.append(f'<circle cx="{x + s*9}" cy="184" r="12" fill="none" stroke="{accent}" stroke-width="3" opacity="0.9"/><circle cx="{x + s*9}" cy="184" r="5" fill="{accent}" opacity="0.8"/>')
            parts.append(f'<ellipse cx="{x - s*10}" cy="172" rx="14" ry="8" fill="#fff" opacity="0.38"/>')
        return "\n".join(parts)
    out.append(one(250, False)); out.append(one(350, True))
    return "\n".join(out)

# ---------------------------------------------------------------- glasses (front, slight perspective)
def draw_glasses(uid, a):
    fr = a.get("frame", "#111"); style = a.get("style", "wayfarer"); disp = a.get("display", "none"); accent = a.get("accent", "#7FE0A8")
    out = [defs(uid, fr, accent), studio(uid, 300, 300, 200, 14)]
    fdef = f'<linearGradient id="{uid}-fr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shade(fr, .30)}"/><stop offset="0.45" stop-color="{fr}"/><stop offset="1" stop-color="{shade(fr, -.20)}"/></linearGradient>'
    out.append(fdef)
    lens_fill = f"url(#{uid}-lens)" if a.get("lens", "dark") != "clear" else "#dfe6ec"
    lens_op = "0.96" if a.get("lens", "dark") != "clear" else "0.55"
    if style == "wrap":
        out.append(f'<path d="M 74 190 Q 300 152 526 190 L 512 250 Q 300 292 88 250 Z" fill="{lens_fill}" opacity="{lens_op}"/>')
        out.append(f'<path d="M 74 190 Q 300 152 526 190 L 512 250 Q 300 292 88 250 Z" fill="none" stroke="url(#{uid}-fr)" stroke-width="12" stroke-linejoin="round"/>')
        out.append(f'<path d="M 120 205 Q 300 175 480 205" stroke="#fff" stroke-opacity="0.35" stroke-width="10" fill="none" filter="url(#{uid}-soft)"/>')
        out.append(f'<rect x="282" y="238" width="36" height="12" rx="6" fill="{fr}"/>')
        out.append(f'<path d="M 76 194 L 40 160 M 524 194 L 560 160" stroke="url(#{uid}-fr)" stroke-width="12" stroke-linecap="round"/>')
        boxes = [(90, 178, 190, 76), (320, 178, 190, 76)]
    else:
        if style == "round":
            shapes = [(f'<circle cx="{x}" cy="212" r="66"', x-66, 146, 132, 132) for x in (205, 395)]
        elif style == "xr":
            shapes = [(f'<rect x="{x}" y="168" width="170" height="98" rx="28"', x, 168, 170, 98) for x in (105, 325)]
        elif style == "thin":
            shapes = [(f'<rect x="{x}" y="172" width="152" height="92" rx="24"', x, 172, 152, 92) for x in (118, 330)]
        else:  # wayfarer
            shapes = [(f'<path d="M {x} 168 L {x+168} 168 Q {x+182} 168 {x+180} 184 L {x+162} 254 Q {x+158} 268 {x+144} 268 L {x+34} 268 Q {x+18} 268 {x+14} 254 L {x+2} 184 Q {x-2} 168 {x+12} 168 Z"', x, 168, 182, 100) for x in (108, 322)]
        boxes = [s[1:] for s in shapes]
        sw = 6 if style == "thin" else (13 if style == "xr" else 11)
        for shp, x, y, w, h in shapes:
            out.append(shp + f' fill="{lens_fill}" opacity="{lens_op}"/>')
            out.append(shp + f' fill="none" stroke="url(#{uid}-fr)" stroke-width="{sw}" stroke-linejoin="round"/>')
            # reflection streak
            out.append(f'<path d="M {x+w*0.22} {y+h*0.78} L {x+w*0.55} {y+h*0.18}" stroke="#fff" stroke-opacity="0.32" stroke-width="{h*0.16}" stroke-linecap="round" filter="url(#{uid}-soft)"/>')
        out.append(f'<path d="M 288 190 Q 300 178 312 190" fill="none" stroke="url(#{uid}-fr)" stroke-width="{sw}" stroke-linecap="round"/>')
        out.append(f'<path d="M 110 186 L 66 156 M 490 186 L 534 156" stroke="url(#{uid}-fr)" stroke-width="{sw+1}" stroke-linecap="round"/>')
        out.append(f'<path d="M 66 156 L 62 150 M 534 156 L 538 150" stroke="{shade(fr, -.2)}" stroke-width="{sw+1}" stroke-linecap="round"/>')
    if a.get("camera"):
        x, y, w, h = boxes[0]
        out.append(f'<circle cx="{x+14}" cy="{y+14}" r="10" fill="#0b0b0b" stroke="#9a9a9a" stroke-width="2.5"/><circle cx="{x+14}" cy="{y+14}" r="5" fill="#1a2430"/><circle cx="{x+11}" cy="{y+11}" r="2" fill="#fff" opacity="0.9"/>')
        x2, y2, w2, h2 = boxes[1]
        out.append(f'<circle cx="{x2+w2-14}" cy="{y2+14}" r="3.5" fill="#fff" opacity="0.7"/>')
    if disp in ("right", "both"):
        for (x, y, w, h) in (boxes if disp == "both" else boxes[1:]):
            gx, gy, gw, gh = x + w*0.30, y + h*0.30, w*0.42, h*0.36
            out.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="4" fill="{accent}" opacity="0.55" filter="url(#{uid}-glow)"/>')
            out.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="4" fill="{accent}" opacity="0.85"/>')
            out.append(f'<rect x="{gx+7}" y="{gy+7}" width="{gw*0.6}" height="4" rx="2" fill="#fff" opacity="0.85"/><rect x="{gx+7}" y="{gy+16}" width="{gw*0.42}" height="4" rx="2" fill="#fff" opacity="0.6"/><rect x="{gx+7}" y="{gy+25}" width="{gw*0.5}" height="4" rx="2" fill="#fff" opacity="0.45"/>')
    return "\n".join(out)

# ---------------------------------------------------------------- power station (three-quarter box)
def draw_power(uid, a):
    size = a.get("size", "mid"); body = a.get("body", "#2E2E2E"); accent = a.get("accent", "#F2A900")
    screen_text = a.get("screen_text", "1,024 Wh"); handle = a.get("handle", "bar"); hcol = a.get("handle_color", "#C9C9C4")
    dims = {"small": (230, 150, 60), "mid": (300, 190, 74), "large": (330, 214, 82), "xl": (340, 222, 86)}
    w, h, d = dims.get(size, dims["mid"])
    x = 300 - w/2 - d*0.25; y = 318 - h - (22 if size == "xl" else 0)
    out = [defs(uid, body, accent), studio(uid, 300, 326, w*0.62, 16)]
    hdef = f'<linearGradient id="{uid}-h" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shade(hcol, .18)}"/><stop offset="0.5" stop-color="{hcol}"/><stop offset="1" stop-color="{shade(hcol, -.22)}"/></linearGradient>'
    out.append(hdef)
    out.append(box3d(uid, x, y, w, h, d, body, rx=20, skew=0.55))
    dx, dy = d * 0.55, d * 0.45           # top-face offsets used by box3d
    tcx, tcy = x + w/2 + dx*0.5, y - dy*0.5   # centre of the top face
    if handle == "bar":
        bw = w * 0.58
        out.append(f'<rect x="{tcx-bw/2-6}" y="{tcy-6}" width="12" height="16" rx="4" fill="{shade(hcol, -.25)}"/><rect x="{tcx+bw/2-6}" y="{tcy-6}" width="12" height="16" rx="4" fill="{shade(hcol, -.25)}"/>')
        out.append(f'<rect x="{tcx-bw/2}" y="{tcy-22}" width="{bw}" height="24" rx="12" fill="url(#{uid}-h)"/><rect x="{tcx-bw/2+10}" y="{tcy-18}" width="{bw-20}" height="5" rx="2.5" fill="#fff" opacity="0.4"/>')
    elif handle == "fold":
        bw = w * 0.66
        out.append(f'<path d="M {tcx-bw/2} {tcy+2} L {tcx-bw/2} {tcy-28} Q {tcx-bw/2} {tcy-40} {tcx-bw/2+12} {tcy-40} L {tcx+bw/2-12} {tcy-40} Q {tcx+bw/2} {tcy-40} {tcx+bw/2} {tcy-28} L {tcx+bw/2} {tcy+2}" fill="none" stroke="url(#{uid}-h)" stroke-width="14" stroke-linecap="round"/>')
        out.append(f'<path d="M {tcx-bw/2+14} {tcy-41} L {tcx+bw/2-14} {tcy-41}" stroke="#fff" stroke-opacity="0.35" stroke-width="3" stroke-linecap="round"/>')
    elif handle == "side":
        hx = x + w + dx*0.55
        out.append(f'<rect x="{hx-8}" y="{y-dy-58}" width="14" height="70" rx="6" fill="url(#{uid}-h)"/><rect x="{hx-58}" y="{y-dy-66}" width="64" height="14" rx="7" fill="url(#{uid}-h)"/>')
    # accent stripe along the top of the front face
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="14" rx="7" fill="url(#{uid}-accent)"/><rect x="{x}" y="{y+8}" width="{w}" height="6" fill="url(#{uid}-accent)"/>')
    # screen
    sw, sh = w*0.36, h*0.34; sx, sy = x + w*0.07, y + h*0.2
    out.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="9" fill="url(#{uid}-screen)" stroke="#000" stroke-width="2"/>')
    out.append(f'<rect x="{sx+4}" y="{sy+4}" width="{sw-8}" height="{sh*0.4}" rx="6" fill="#fff" opacity="0.05"/>')
    fs = max(13, int(sw/6.4))
    out.append(f'<text x="{sx+sw/2}" y="{sy+sh*0.52}" text-anchor="middle" font-family="{FONT}" font-size="{fs}" font-weight="700" fill="#8FE3B2">{esc(screen_text)}</text>')
    # battery bar
    bx, by, bw = sx + sw*0.12, sy + sh*0.66, sw*0.76
    out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{sh*0.14}" rx="3" fill="#0f2a1c"/><rect x="{bx}" y="{by}" width="{bw*0.92}" height="{sh*0.14}" rx="3" fill="#2ecc71"/>')
    # outlets or USB-C panel
    ox, oy = x + w*0.52, y + h*0.2; cell = min(w*0.19, h*0.3)
    if a.get("no_ac"):
        for i in range(2):
            for j in range(2):
                cx0 = ox + j*(cell+10); cy0 = oy + i*(cell+8)
                out.append(f'<rect x="{cx0}" y="{cy0+cell*0.3}" width="{cell}" height="{cell*0.4}" rx="{cell*0.2}" fill="#efefec"/><rect x="{cx0+cell*0.22}" y="{cy0+cell*0.43}" width="{cell*0.56}" height="{cell*0.14}" rx="{cell*0.07}" fill="#222"/>')
    else:
        for i in range(2):
            for j in range(2):
                out.append(outlet(uid, ox + j*(cell+10), oy + i*(cell+8), cell, body))
    # usb row under the screen
    uy = sy + sh + 12
    for k in range(3):
        ux = sx + k*(sw/3)
        out.append(f'<rect x="{ux}" y="{uy}" width="{sw/3 - 8}" height="11" rx="4" fill="#efefec" opacity="0.9"/><rect x="{ux+4}" y="{uy+3.5}" width="{sw/3 - 16}" height="4" rx="2" fill="#333"/>')
    # power button + LED
    out.append(f'<circle cx="{x+w-26}" cy="{y+h-26}" r="9" fill="{shade(body, .12)}" stroke="{shade(body, -.3)}" stroke-width="1.5"/><circle cx="{x+w-26}" cy="{y+h-26}" r="3" fill="{accent}"/>')
    if a.get("wheels") or size == "xl":
        for wx in (x+44, x+w-44):
            out.append(f'<circle cx="{wx}" cy="{y+h+14}" r="20" fill="#1a1a1a"/><circle cx="{wx}" cy="{y+h+14}" r="12" fill="#3a3a3a"/><circle cx="{wx}" cy="{y+h+14}" r="4" fill="#777"/>')
    return "\n".join(out)


# ---------------------------------------------------------------- bluetooth tracker (coin or tag)
def draw_tracker(uid, a):
    body = a.get("body", "#F7F7F5"); back = a.get("back", "#C9CACB"); style = a.get("style", "coin"); pack = int(a.get("pack", 1))
    out = [defs(uid, body, back), studio(uid, 300, 322, 150, 14)]
    out.append(f'<radialGradient id="{uid}-coin" cx="40%" cy="32%" r="70%"><stop offset="0" stop-color="#ffffff"/><stop offset="0.7" stop-color="{body}"/><stop offset="1" stop-color="{shade(body, -.10)}"/></radialGradient>')
    def coin(cx, cy, r, face=True, sc=1.0):
        ry = r * 0.92
        if face:
            return (f'<path d="M {cx-r} {cy} A {r} {ry} 0 0 0 {cx+r} {cy} L {cx+r} {cy+12*sc} A {r} {ry} 0 0 1 {cx-r} {cy+12*sc} Z" fill="url(#{uid}-metal)"/>'
                    f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry}" fill="url(#{uid}-coin)" stroke="{shade(body, -.12)}" stroke-width="1.5"/>'
                    f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.62}" ry="{ry*0.62}" fill="none" stroke="{shade(body, -.08)}" stroke-width="1.2" opacity="0.8"/>'
                    f'<ellipse cx="{cx-r*0.28}" cy="{cy-ry*0.36}" rx="{r*0.36}" ry="{ry*0.16}" fill="#fff" opacity="0.55"/>')
        return (f'<path d="M {cx-r} {cy} A {r} {ry} 0 0 0 {cx+r} {cy} L {cx+r} {cy+12*sc} A {r} {ry} 0 0 1 {cx-r} {cy+12*sc} Z" fill="{shade(back, -.2)}"/>'
                f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry}" fill="url(#{uid}-metal)" stroke="{shade(back, -.25)}" stroke-width="1.5"/>'
                f'<ellipse cx="{cx}" cy="{cy}" rx="{r*0.5}" ry="{ry*0.5}" fill="none" stroke="{shade(back, -.15)}" stroke-width="1.2"/>'
                f'<ellipse cx="{cx-r*0.3}" cy="{cy-ry*0.3}" rx="{r*0.3}" ry="{ry*0.12}" fill="#fff" opacity="0.5"/>')
    def tag(cx, cy, w, h, col):
        return (f'<rect x="{cx-w/2+6}" y="{cy-h/2+8}" width="{w}" height="{h}" rx="{w*0.28}" fill="{shade(col, -.3)}"/>'
                f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{w*0.28}" fill="{col}"/>'
                f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{w*0.28}" fill="url(#{uid}-gloss)"/>'
                f'<circle cx="{cx}" cy="{cy-h/2+w*0.16}" r="{w*0.085}" fill="{PAPER}" stroke="{shade(col, -.3)}" stroke-width="3"/>'
                f'<circle cx="{cx}" cy="{cy+h*0.12}" r="{w*0.16}" fill="none" stroke="{shade(col, -.18)}" stroke-width="2"/>')
    if style == "coin":
        if pack >= 4:
            out.append(coin(190, 250, 62, face=False, sc=0.9)); out.append(coin(410, 250, 62, face=False, sc=0.9))
            out.append(coin(250, 205, 74, face=True)); out.append(coin(350, 205, 74, face=True))
            out.append(f'<text x="300" y="322" text-anchor="middle" font-family="{FONT}" font-size="14" fill="#666">4-pack</text>')
        else:
            out.append(coin(300, 212, 104, face=True))
    else:
        out.append(tag(300, 215, 150, 172, body))
    return "\n".join(out)

# ---------------------------------------------------------------- insulated bottle / tumbler
def draw_bottle(uid, a):
    body = a.get("body", "#3D6FA8"); lid = a.get("lid", "#1B2A41"); accent = a.get("accent", "#8FD3AE"); style = a.get("style", "freesip")
    out = [defs(uid, body, accent), studio(uid, 300, 330, 90, 12)]
    out.append(f'<linearGradient id="{uid}-cyl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{shade(body, -.18)}"/><stop offset="0.28" stop-color="{shade(body, .16)}"/><stop offset="0.55" stop-color="{body}"/><stop offset="1" stop-color="{shade(body, -.24)}"/></linearGradient>')
    out.append(f'<linearGradient id="{uid}-lidg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{shade(lid, -.12)}"/><stop offset="0.35" stop-color="{shade(lid, .18)}"/><stop offset="1" stop-color="{shade(lid, -.22)}"/></linearGradient>')
    if style == "tumbler":
        out.append(f'<path d="M 236 120 L 364 120 L 348 316 Q 300 330 252 316 Z" fill="url(#{uid}-cyl)"/>')
        out.append(f'<ellipse cx="300" cy="120" rx="64" ry="12" fill="{shade(body, .1)}"/>')
        out.append(f'<rect x="232" y="96" width="136" height="30" rx="10" fill="url(#{uid}-lidg)"/><ellipse cx="300" cy="96" rx="68" ry="12" fill="{shade(lid, .25)}"/><rect x="300" y="84" width="14" height="24" rx="5" fill="{accent}" transform="rotate(12 300 84)"/>')
        out.append(f'<path d="M 366 150 Q 430 150 430 210 Q 430 270 356 270" fill="none" stroke="{shade(body, -.05)}" stroke-width="20" stroke-linecap="round"/><path d="M 366 150 Q 430 150 430 210 Q 430 270 356 270" fill="none" stroke="#fff" stroke-opacity="0.25" stroke-width="5"/>')
    else:
        out.append(f'<rect x="238" y="118" width="124" height="204" rx="22" fill="url(#{uid}-cyl)"/>')
        out.append(f'<ellipse cx="300" cy="322" rx="62" ry="10" fill="{shade(body, -.3)}"/>')
        out.append(f'<path d="M 238 140 Q 238 100 262 96 L 338 96 Q 362 100 362 140" fill="url(#{uid}-cyl)"/>')
        out.append(f'<rect x="254" y="72" width="92" height="30" rx="10" fill="url(#{uid}-lidg)"/>')
        if style == "freesip":
            out.append(f'<path d="M 262 72 Q 262 50 284 50 L 318 50 Q 340 50 340 72 Z" fill="{shade(lid, .10)}"/><rect x="286" y="46" width="40" height="10" rx="5" fill="{accent}"/>')
            out.append(f'<path d="M 330 60 Q 372 40 380 84 Q 384 110 350 104" fill="none" stroke="{shade(lid, .05)}" stroke-width="9" stroke-linecap="round"/>')
            out.append(f'<circle cx="300" cy="88" r="7" fill="{accent}"/>')
        else:  # straw bottle
            out.append(f'<rect x="270" y="52" width="60" height="26" rx="8" fill="{shade(lid, .10)}"/><rect x="296" y="14" width="10" height="44" rx="4" fill="{accent}" transform="rotate(-14 300 40)"/>')
            out.append(f'<path d="M 262 66 Q 226 40 236 90" fill="none" stroke="{shade(lid, .05)}" stroke-width="8" stroke-linecap="round"/>')
        out.append(f'<rect x="258" y="150" width="14" height="140" rx="7" fill="#fff" opacity="0.28"/>')
    return "\n".join(out)

# ---------------------------------------------------------------- portable spot / carpet cleaner
def draw_cleaner(uid, a):
    body = a.get("body", "#3E8E5A"); tank = a.get("tank", "#9FD3FF"); accent = a.get("accent", "#1B2A41"); style = a.get("style", "classic")
    sc = 0.78 if style == "mini" else 1.0
    out = [defs(uid, body, accent), studio(uid, 300, 328, 190, 16)]
    out.append(f'<g transform="translate({300 - 300*sc} {330 - 330*sc}) scale({sc})">')
    # base body (three-quarter)
    out.append(box3d(uid, 170, 214, 230, 104, 60, body, rx=24))
    # tank on top (translucent)
    out.append(f'<rect x="196" y="126" width="180" height="96" rx="20" fill="{tank}" opacity="0.85"/><rect x="196" y="126" width="180" height="96" rx="20" fill="url(#{uid}-gloss)"/>')
    out.append(f'<rect x="196" y="170" width="180" height="52" rx="14" fill="#5FA8E6" opacity="0.55"/><rect x="204" y="134" width="18" height="70" rx="9" fill="#fff" opacity="0.35"/>')
    out.append(f'<rect x="188" y="118" width="196" height="16" rx="8" fill="{shade(body, -.15)}"/>')
    # handle
    out.append(f'<path d="M 236 118 L 236 84 Q 236 68 252 68 L 320 68 Q 336 68 336 84 L 336 118" fill="none" stroke="{shade(accent, .1)}" stroke-width="16" stroke-linecap="round"/><path d="M 250 66 L 322 66" stroke="#fff" stroke-opacity="0.3" stroke-width="3" stroke-linecap="round"/>')
    # front panel: switch + logo-less badge
    out.append(f'<rect x="196" y="236" width="70" height="26" rx="8" fill="{shade(body, -.25)}"/><circle cx="214" cy="249" r="7" fill="{accent}"/><rect x="230" y="244" width="28" height="10" rx="5" fill="#F1F1EE" opacity="0.8"/>')
    out.append(f'<rect x="300" y="232" width="86" height="60" rx="10" fill="{shade(body, -.1)}"/><circle cx="343" cy="262" r="16" fill="{shade(body, -.35)}"/>')
    # hose from the right side, looping to the front with a tool
    out.append(f'<path d="M 400 250 Q 470 240 468 300 Q 464 350 400 342 Q 330 336 300 356" fill="none" stroke="#2A2A2A" stroke-width="13" stroke-linecap="round"/><path d="M 400 250 Q 470 240 468 300 Q 464 350 400 342 Q 330 336 300 356" fill="none" stroke="#fff" stroke-opacity="0.15" stroke-width="4" stroke-linecap="round"/>')
    out.append(f'<rect x="262" y="344" width="52" height="22" rx="8" fill="{shade(accent, .05)}" transform="rotate(-12 288 355)"/><rect x="252" y="352" width="22" height="12" rx="4" fill="#DDE3EA" transform="rotate(-12 263 358)"/>')
    out.append('</g>')
    return "\n".join(out)


def draw_groomvac(uid, a):
    """Pet grooming vacuum kit: rounded canister with a dust-cup window, top handle, hose to a brush head, two spare tools."""
    body = a.get("body", "#F1F1EE"); accent = a.get("accent", "#3C8DAD"); cup = a.get("cup", "#9FD3FF"); tool = a.get("tool", "#2A2A2A")
    out = [defs(uid, body, accent), studio(uid, 300, 334, 220, 16)]
    # spare tools at the front-left: clipper and de-shedding comb
    out.append(f'<g transform="rotate(-8 130 300)"><rect x="76" y="290" width="100" height="26" rx="12" fill="{tool}"/><rect x="80" y="288" width="42" height="9" rx="4.5" fill="{shade(tool, .35)}"/>'
               f'<path d="M 128 303 h 40" stroke="{accent}" stroke-width="6" stroke-linecap="round"/></g>')
    out.append(f'<g transform="rotate(5 140 344)"><rect x="86" y="336" width="108" height="18" rx="9" fill="{shade(tool, .15)}"/>'
               + "".join(f'<rect x="{94 + i*9.5}" y="328" width="3" height="10" rx="1.5" fill="{shade(tool, .15)}"/>' for i in range(11)) + '</g>')
    # canister: rounded body with a darker right edge for roundness, cap on top
    out.append(f'<rect x="212" y="168" width="182" height="154" rx="30" fill="url(#{uid}-front)"/>'
               f'<path d="M 364 168 h 0 a 30 30 0 0 1 30 30 v 94 a 30 30 0 0 1 -30 30 z" fill="url(#{uid}-side)" opacity="0.55"/>'
               f'<rect x="212" y="168" width="182" height="154" rx="30" fill="none" stroke="{shade(body, -.25)}" stroke-width="1.2" opacity="0.6"/>')
    out.append(f'<rect x="222" y="148" width="162" height="36" rx="18" fill="{shade(body, -.08)}"/><rect x="222" y="148" width="162" height="36" rx="18" fill="url(#{uid}-gloss)"/>')
    # translucent dust cup window
    out.append(f'<rect x="232" y="212" width="142" height="94" rx="18" fill="{cup}" opacity="0.8"/><rect x="232" y="212" width="142" height="94" rx="18" fill="url(#{uid}-gloss)"/>'
               f'<rect x="232" y="266" width="142" height="40" rx="12" fill="#5FA8E6" opacity="0.5"/><rect x="240" y="220" width="16" height="70" rx="8" fill="#fff" opacity="0.35"/>')
    # accent band with power button and mode dial
    out.append(f'<rect x="212" y="188" width="182" height="14" fill="{accent}" opacity="0.9"/><circle cx="362" cy="195" r="9" fill="#fff"/><circle cx="362" cy="195" r="4" fill="{accent}"/>'
               f'<circle cx="250" cy="195" r="6" fill="{shade(accent, -.3)}"/>')
    # carry handle
    out.append(f'<path d="M 262 150 L 262 122 Q 262 106 278 106 L 328 106 Q 344 106 344 122 L 344 150" fill="none" stroke="{shade(body, -.35)}" stroke-width="15" stroke-linecap="round"/>'
               f'<path d="M 276 104 L 330 104" stroke="#fff" stroke-opacity="0.3" stroke-width="3" stroke-linecap="round"/>')
    # hose from the right port, looping out and down to the brush head at the front-right
    hose = "M 392 246 Q 470 228 500 272 Q 528 314 486 336 Q 452 352 448 336"
    out.append(f'<circle cx="392" cy="246" r="16" fill="{shade(body, -.3)}"/><circle cx="392" cy="246" r="9" fill="{tool}"/>')
    out.append(f'<path d="{hose}" fill="none" stroke="{tool}" stroke-width="14" stroke-linecap="round"/><path d="{hose}" fill="none" stroke="#fff" stroke-opacity="0.15" stroke-width="4" stroke-linecap="round"/>')
    # brush head (angled, bristles down) with a few captured hairs
    out.append(f'<g transform="rotate(-22 452 344)"><rect x="410" y="334" width="92" height="26" rx="12" fill="{shade(accent, -.05)}"/>'
               + "".join(f'<rect x="{418 + i*8}" y="358" width="3" height="9" rx="1.5" fill="{tool}"/>' for i in range(10)) + '</g>')
    out.append(f'<path d="M 404 372 q 6 -8 12 0 M 424 380 q 6 -8 12 0 M 388 360 q 6 -8 12 0" stroke="{AMBER}" stroke-width="2.5" fill="none" stroke-linecap="round" opacity="0.85"/>')
    return "\n".join(out)

def draw_roller(uid, a):
    """Reusable pet-hair roller (ChomChom style): rounded handle body, roller face with bristle strips, release button, fur wad."""
    body = a.get("body", "#F4F4F1"); accent = a.get("accent", "#1B2A41"); strip = a.get("strip", "#2A2A2A")
    out = [defs(uid, body, accent), studio(uid, 300, 330, 200, 16)]
    out.append(f'<g transform="rotate(-14 300 250)">')
    # roller head: a wide capsule seen from the front-top, with two bristle strips and the chamber
    out.append(f'<rect x="150" y="196" width="300" height="120" rx="56" fill="url(#{uid}-front)"/><rect x="150" y="196" width="300" height="120" rx="56" fill="none" stroke="{shade(body, -.25)}" stroke-width="1.2" opacity="0.6"/>')
    out.append(f'<rect x="150" y="256" width="300" height="60" rx="30" fill="{shade(body, -.12)}" opacity="0.9"/>')
    # bristle strips on the underside face
    for y in (272, 296):
        out.append(f'<rect x="176" y="{y}" width="248" height="10" rx="5" fill="{strip}"/>' + "".join(f'<rect x="{182 + i*10}" y="{y-3}" width="2.5" height="6" rx="1.2" fill="{shade(strip, .35)}"/>' for i in range(24)))
    # chamber door seam and release button
    out.append(f'<path d="M 176 236 H 424" stroke="{shade(body, -.3)}" stroke-width="2" stroke-linecap="round" opacity="0.7"/>')
    out.append(f'<rect x="286" y="206" width="28" height="18" rx="6" fill="{accent}"/><rect x="290" y="208" width="20" height="6" rx="3" fill="#fff" opacity="0.35"/>')
    # handle rising from the back
    out.append(f'<path d="M 300 196 L 300 150 Q 300 118 334 118 L 372 118" fill="none" stroke="{shade(body, -.18)}" stroke-width="34" stroke-linecap="round"/>'
               f'<path d="M 300 196 L 300 150 Q 300 118 334 118 L 372 118" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="6" stroke-linecap="round"/>'
               f'<circle cx="372" cy="118" r="17" fill="{accent}"/><circle cx="372" cy="118" r="7" fill="#fff" opacity="0.5"/>')
    out.append('</g>')
    # a wad of collected fur next to the roller
    out.append(f'<ellipse cx="470" cy="350" rx="46" ry="16" fill="{AMBER}" opacity="0.55"/><ellipse cx="462" cy="344" rx="30" ry="10" fill="{shade(AMBER, .25)}" opacity="0.7"/>'
               f'<path d="M 436 342 q 8 -10 16 0 M 468 336 q 8 -10 16 0 M 484 348 q 8 -10 16 0" stroke="{shade(AMBER, -.2)}" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
    return "\n".join(out)

def draw_litterbot(uid, a):
    """Self-cleaning litter box (rotating globe on a base with a waste drawer), three-quarter view."""
    body = a.get("body", "#F2F2EF"); accent = a.get("accent", "#1B2A41"); trim = a.get("trim", "#8A8F98")
    out = [defs(uid, body, accent), studio(uid, 300, 350, 200, 16)]
    # base with the waste drawer (front) and a step in front of it
    out.append(box3d(uid, 168, 262, 250, 92, 70, body, rx=18))
    out.append(f'<rect x="184" y="290" width="218" height="50" rx="10" fill="{shade(body, -.12)}"/><rect x="270" y="310" width="46" height="8" rx="4" fill="{shade(body, -.4)}"/>')
    out.append(f'<rect x="176" y="352" width="120" height="14" rx="6" fill="{shade(body, -.2)}" opacity="0.9"/>')
    # globe: big sphere with a dark bezel opening facing front-left
    out.append(f'<circle cx="300" cy="176" r="112" fill="url(#{uid}-front)"/><circle cx="300" cy="176" r="112" fill="none" stroke="{shade(body, -.25)}" stroke-width="1.2" opacity="0.6"/>')
    out.append(f'<ellipse cx="262" cy="176" rx="34" ry="72" transform="rotate(-8 262 176)" fill="{shade(body, -.5)}"/><ellipse cx="256" cy="176" rx="26" ry="62" transform="rotate(-8 256 176)" fill="#111"/>')
    out.append(f'<ellipse cx="262" cy="176" rx="34" ry="72" transform="rotate(-8 262 176)" fill="none" stroke="{trim}" stroke-width="5"/>')
    # seam and sensor bar on the globe, gloss highlight
    out.append(f'<path d="M 300 66 Q 372 96 380 176" fill="none" stroke="{shade(body, -.2)}" stroke-width="2" opacity="0.7"/>'
               f'<path d="M 330 84 Q 362 104 368 140" fill="none" stroke="#fff" stroke-opacity="0.55" stroke-width="6" stroke-linecap="round"/>')
    out.append(f'<rect x="318" y="228" width="60" height="10" rx="5" fill="{accent}" opacity="0.85"/><circle cx="392" cy="248" r="5" fill="{GREEN}"/>')
    # a sitting cat silhouette peeking from the opening for scale
    out.append(f'<g fill="{shade(body, -.55)}"><circle cx="238" cy="186" r="14"/><path d="M 228 176 l -4 -14 l 12 8 z M 248 176 l 4 -14 l -12 8 z"/></g>')
    return "\n".join(out)

def draw_harness(uid, a):
    """No-pull dog harness (Rabbitgoo style) laid out three-quarter: padded chest plate, back plate with a D-ring, side straps with buckles, reflective piping."""
    body = a.get("body", "#2F3A48"); accent = a.get("accent", "#F08A24"); ring = a.get("ring", "#B9BEC6")
    out = [defs(uid, body, accent), studio(uid, 300, 336, 210, 16)]
    dark = shade(body, -.35); lite = shade(body, .18)
    # back plate (top) and chest plate (bottom), joined by two shoulder straps forming the neck loop
    out.append(f'<path d="M 214 118 Q 300 78 386 118 L 372 178 Q 300 150 228 178 Z" fill="url(#{uid}-front)" stroke="{dark}" stroke-width="2"/>')
    out.append(f'<path d="M 190 262 Q 300 226 410 262 L 392 318 Q 300 292 208 318 Z" fill="url(#{uid}-front)" stroke="{dark}" stroke-width="2"/>')
    for x1, x2 in ((228, 208), (372, 392)):
        out.append(f'<path d="M {x1} 178 Q {x1 + (x2 - x1) * .5} 222 {x2} 262" fill="none" stroke="{body}" stroke-width="30" stroke-linecap="round"/>'
                   f'<path d="M {x1} 178 Q {x1 + (x2 - x1) * .5} 222 {x2} 262" fill="none" stroke="{lite}" stroke-width="3" stroke-dasharray="6 5" opacity="0.9"/>')
    # girth straps going out to the sides with side-release buckles
    for sx, dirn in ((208, -1), (392, 1)):
        ex = sx + dirn * 88
        out.append(f'<path d="M {sx} 290 L {ex} 290" stroke="{body}" stroke-width="22" stroke-linecap="round"/>'
                   f'<path d="M {sx} 290 L {ex} 290" stroke="{lite}" stroke-width="2.5" stroke-dasharray="6 5" opacity="0.9"/>'
                   f'<rect x="{ex - 20 if dirn < 0 else ex - 12}" y="276" width="32" height="28" rx="7" fill="{dark}"/>'
                   f'<rect x="{ex - 14 if dirn < 0 else ex - 6}" y="282" width="20" height="16" rx="4" fill="{shade(body, -.1)}"/>')
    # stitching and padding lines on the plates
    out.append(f'<path d="M 232 128 Q 300 96 368 128 M 240 168 Q 300 146 360 168" fill="none" stroke="{lite}" stroke-width="2" stroke-dasharray="6 5" opacity="0.8"/>'
               f'<path d="M 210 270 Q 300 240 390 270 M 220 306 Q 300 282 380 306" fill="none" stroke="{lite}" stroke-width="2" stroke-dasharray="6 5" opacity="0.8"/>')
    # handle on the back plate, metal D-ring, front leash ring on the chest
    out.append(f'<path d="M 268 108 Q 300 84 332 108" fill="none" stroke="{dark}" stroke-width="12" stroke-linecap="round"/>')
    out.append(f'<path d="M 282 128 a 18 18 0 1 0 36 0" fill="none" stroke="url(#{uid}-metal)" stroke-width="7"/><path d="M 282 128 H 318" stroke="{dark}" stroke-width="9" stroke-linecap="round"/>')
    out.append(f'<circle cx="300" cy="270" r="15" fill="none" stroke="url(#{uid}-metal)" stroke-width="7"/><circle cx="300" cy="270" r="15" fill="none" stroke="{ring}" stroke-width="1" opacity="0.5"/>')
    # orange accent tab (brand-style) and a leash clip resting on the plate
    out.append(f'<rect x="318" y="236" width="44" height="14" rx="5" fill="{accent}"/><rect x="322" y="239" width="24" height="4" rx="2" fill="#fff" opacity="0.5"/>')
    out.append(f'<path d="M 300 118 l 0 -22 q 0 -16 16 -16 l 6 0" fill="none" stroke="url(#{uid}-metal)" stroke-width="8" stroke-linecap="round"/><circle cx="326" cy="80" r="6" fill="url(#{uid}-metal)"/>')
    return "\n".join(out)

def draw_kong(uid, a):
    """The classic KONG: three stacked rubber lobes, hollow top with a swirl of peanut butter, slightly tilted, glossy."""
    body = a.get("body", "#C8102E"); accent = a.get("accent", "#F4B942")
    out = [defs(uid, body, accent), studio(uid, 300, 340, 150, 16)]
    out.append(f'<g transform="rotate(-9 300 240)">')
    for cx, cy, rx, ry in ((300, 300, 88, 66), (300, 214, 68, 54), (300, 148, 48, 40)):
        out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#{uid}-dome)"/>'
                   f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{shade(body, -.28)}" stroke-width="1.5" opacity="0.7"/>')
    # waist blends between lobes
    out.append(f'<ellipse cx="300" cy="256" rx="58" ry="20" fill="{body}"/><ellipse cx="300" cy="182" rx="44" ry="16" fill="{body}"/>')
    # hollow opening at the top with peanut butter
    out.append(f'<ellipse cx="300" cy="112" rx="22" ry="11" fill="{shade(body, -.6)}"/><ellipse cx="300" cy="111" rx="16" ry="7" fill="{accent}"/>'
               f'<path d="M 291 110 q 6 -6 12 0 q 4 4 8 -1" fill="none" stroke="{shade(accent, -.3)}" stroke-width="2" stroke-linecap="round"/>')
    # gloss highlights and the small bottom hole
    out.append(f'<path d="M 246 292 q -8 -40 20 -62" fill="none" stroke="#fff" stroke-opacity="0.45" stroke-width="10" stroke-linecap="round"/>'
               f'<path d="M 262 206 q -6 -26 12 -40" fill="none" stroke="#fff" stroke-opacity="0.4" stroke-width="7" stroke-linecap="round"/>'
               f'<path d="M 280 140 q -4 -14 8 -22" fill="none" stroke="#fff" stroke-opacity="0.4" stroke-width="5" stroke-linecap="round"/>')
    out.append(f'<ellipse cx="300" cy="364" rx="6" ry="3" fill="{shade(body, -.55)}"/>')
    out.append('</g>')
    # a few kibble pieces spilled at the base
    out.append(f'<g fill="{shade(accent, -.35)}"><circle cx="404" cy="350" r="6"/><circle cx="420" cy="342" r="5"/><circle cx="392" cy="362" r="5"/><circle cx="184" cy="354" r="6"/></g>')
    return "\n".join(out)

def draw_bags(uid, a):
    """Dog waste bags: a roll with one bag peeling off, next to a dispenser on a strap; leaf pattern on the roll."""
    body = a.get("body", "#2E8B57"); accent = a.get("accent", "#1B2A41"); bag = a.get("bag", "#7BC47F")
    out = [defs(uid, body, accent), studio(uid, 300, 336, 210, 16)]
    # the roll: a cylinder lying at an angle (front ellipse face + body)
    out.append(f'<g transform="rotate(-18 250 250)">')
    out.append(f'<rect x="150" y="196" width="200" height="104" fill="url(#{uid}-front)"/>')
    out.append(f'<ellipse cx="350" cy="248" rx="30" ry="52" fill="{shade(body, .12)}"/><ellipse cx="350" cy="248" rx="14" ry="26" fill="{shade(body, -.45)}"/><ellipse cx="350" cy="248" rx="7" ry="13" fill="#111"/>')
    out.append(f'<ellipse cx="150" cy="248" rx="30" ry="52" fill="{shade(body, -.12)}"/>')
    # leaf pattern along the roll
    for i in range(5):
        x = 176 + i * 34
        out.append(f'<path d="M {x} 232 q 10 -14 22 0 q -10 14 -22 0 Z" fill="{shade(body, .35)}" opacity="0.8"/><path d="M {x} 268 q 10 -14 22 0 q -10 14 -22 0 Z" fill="{shade(body, .35)}" opacity="0.6"/>')
    # a bag peeling off the roll with a perforation line
    out.append(f'<path d="M 150 300 L 150 196 L 92 176 Q 62 220 92 292 Z" fill="{bag}" opacity="0.92"/><path d="M 150 196 L 150 300" stroke="{shade(body, -.3)}" stroke-width="2" stroke-dasharray="3 4"/>'
               f'<path d="M 100 190 q -22 40 0 92" fill="none" stroke="#fff" stroke-opacity="0.5" stroke-width="4" stroke-linecap="round"/>')
    out.append('</g>')
    # dispenser: a rounded capsule with a slot, hanging from a short strap and clip
    out.append(f'<rect x="392" y="222" width="96" height="60" rx="26" fill="url(#{uid}-accent)"/><rect x="392" y="222" width="96" height="60" rx="26" fill="none" stroke="{shade(accent, -.3)}" stroke-width="1.5"/>')
    out.append(f'<rect x="424" y="248" width="34" height="8" rx="4" fill="{shade(accent, -.55)}"/><path d="M 418 246 q 12 -10 24 0" fill="none" stroke="{bag}" stroke-width="5" stroke-linecap="round"/>')
    out.append(f'<path d="M 440 222 l 0 -26 q 0 -18 18 -18 l 22 0" fill="none" stroke="{shade(accent, -.2)}" stroke-width="10" stroke-linecap="round"/>'
               f'<path d="M 480 178 a 12 12 0 1 1 0.1 0" fill="none" stroke="url(#{uid}-metal)" stroke-width="6"/>')
    out.append(f'<path d="M 404 244 q 10 -14 24 -10" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="5" stroke-linecap="round"/>')
    # a tied bag on the floor for scale (knot on top)
    out.append(f'<ellipse cx="520" cy="338" rx="26" ry="18" fill="{bag}"/><path d="M 512 322 q 8 -14 16 0 q -4 -8 8 -6" fill="none" stroke="{shade(bag, -.35)}" stroke-width="4" stroke-linecap="round"/>')
    return "\n".join(out)

def _tile(uid, a, glyph):
    """A software 'product': a rounded app tile on the studio floor with a big white glyph and a small window frame behind it."""
    body = a.get("body", "#1B2A41"); accent = a.get("accent", "#1E8E5A")
    out = [defs(uid, body, accent), studio(uid, 300, 336, 190, 16)]
    dark = shade(body, -.3); lite = shade(body, .25)
    # window frame behind the tile (a browser/app window)
    out.append(f'<rect x="120" y="70" width="360" height="236" rx="16" fill="#fff" stroke="#D9D6CF" stroke-width="2"/>'
               f'<rect x="120" y="70" width="360" height="30" rx="16" fill="#ECEAE4"/><rect x="120" y="86" width="360" height="14" fill="#ECEAE4"/>'
               f'<circle cx="142" cy="85" r="5" fill="#F26D5B"/><circle cx="160" cy="85" r="5" fill="#F4B942"/><circle cx="178" cy="85" r="5" fill="#5AC26A"/>'
               f'<rect x="150" y="122" width="150" height="10" rx="5" fill="#E8E6E0"/><rect x="150" y="142" width="220" height="10" rx="5" fill="#E8E6E0"/><rect x="150" y="162" width="110" height="10" rx="5" fill="#E8E6E0"/>')
    # the tile
    out.append(f'<rect x="222" y="152" width="176" height="176" rx="40" fill="{dark}" opacity="0.25" transform="translate(6 10)"/>'
               f'<rect x="222" y="152" width="176" height="176" rx="40" fill="url(#{uid}-front)"/>'
               f'<rect x="222" y="152" width="176" height="176" rx="40" fill="none" stroke="{lite}" stroke-width="2" opacity="0.6"/>')
    out.append(glyph(accent))
    return "\n".join(out)

def draw_chat(uid, a):
    """Assistant / chat app: a speech bubble with a sparkle."""
    def glyph(acc):
        return (f'<path d="M 262 200 h 96 a 14 14 0 0 1 14 14 v 46 a 14 14 0 0 1 -14 14 h -52 l -26 22 v -22 h -18 a 14 14 0 0 1 -14 -14 v -46 a 14 14 0 0 1 14 -14 z" fill="#fff"/>'
                f'<circle cx="286" cy="240" r="6" fill="{acc}"/><circle cx="310" cy="240" r="6" fill="{acc}"/><circle cx="334" cy="240" r="6" fill="{acc}"/>'
                f'<path d="M 372 178 l 5 12 l 12 5 l -12 5 l -5 12 l -5 -12 l -12 -5 l 12 -5 z" fill="#FFD27A"/>')
    return _tile(uid, a, glyph)

def draw_film(uid, a):
    """Video generator: a clapperboard with a play triangle."""
    def glyph(acc):
        return (f'<rect x="258" y="222" width="104" height="72" rx="10" fill="#fff"/>'
                f'<path d="M 258 222 l 8 -22 h 96 l -8 22 z" fill="#fff"/><path d="M 274 200 l 12 22 M 298 200 l 12 22 M 322 200 l 12 22 M 346 200 l 12 22" stroke="{acc}" stroke-width="6"/>'
                f'<path d="M 298 240 l 34 18 l -34 18 z" fill="{acc}"/>')
    return _tile(uid, a, glyph)

def draw_voice(uid, a):
    """Voice / audio app: a waveform."""
    def glyph(acc):
        bars = [(262, 22), (280, 44), (298, 70), (316, 96), (334, 70), (352, 44), (370, 22)]
        return "".join(f'<rect x="{x-6}" y="{240-h/2}" width="12" height="{h}" rx="6" fill="{"#fff" if i % 2 == 0 else acc}"/>' for i, (x, h) in enumerate(bars))
    return _tile(uid, a, glyph)

def draw_lightbox(uid, a):
    """Portable photo light box: an open cube with a bright LED rim and a small product (a bottle) inside."""
    body = a.get("body", "#F2F2F2"); accent = a.get("accent", "#1E8E5A")
    out = [defs(uid, body, accent), studio(uid, 300, 336, 200, 16)]
    # back and side walls (soft white), floor
    out.append(f'<path d="M 150 100 L 450 100 L 450 300 L 150 300 Z" fill="#FAFAFA" stroke="#D5D5D5" stroke-width="2"/>'
               f'<path d="M 150 100 L 110 150 L 110 330 L 150 300 Z" fill="#E9E9E9" stroke="#D5D5D5" stroke-width="2"/>'
               f'<path d="M 450 100 L 490 150 L 490 330 L 450 300 Z" fill="#E9E9E9" stroke="#D5D5D5" stroke-width="2"/>'
               f'<path d="M 110 330 L 150 300 L 450 300 L 490 330 Z" fill="#F4F4F4" stroke="#D5D5D5" stroke-width="2"/>')
    # LED strips glowing along the top edge
    out.append(f'<path d="M 150 100 L 450 100" stroke="#FFF3C4" stroke-width="10" stroke-linecap="round"/><path d="M 150 100 L 450 100" stroke="#FFD27A" stroke-width="3" stroke-linecap="round"/>'
               f'<path d="M 110 150 L 150 100 M 450 100 L 490 150" stroke="#FFF3C4" stroke-width="8" stroke-linecap="round"/>')
    # the product inside: a small bottle in the accent colour, with a soft shadow
    out.append(f'<ellipse cx="300" cy="300" rx="42" ry="8" fill="#000" opacity="0.08"/>'
               f'<rect x="276" y="188" width="48" height="108" rx="14" fill="{accent}"/><rect x="284" y="172" width="32" height="24" rx="8" fill="{shade(accent, -.3)}"/>'
               f'<rect x="284" y="216" width="32" height="40" rx="4" fill="#fff" opacity="0.85"/>')
    # a phone on a mini stand at the front, aimed at the product
    out.append(f'<rect x="392" y="262" width="34" height="62" rx="6" fill="#1B2A41" transform="rotate(-12 409 293)"/><rect x="396" y="268" width="26" height="46" rx="3" fill="#3A4453" transform="rotate(-12 409 293)"/>')
    return "\n".join(out)

def draw_tripod(uid, a):
    """Phone tripod: three legs, a centre column and a phone clamp holding a phone."""
    body = a.get("body", "#2F3A48"); accent = a.get("accent", "#1E8E5A")
    out = [defs(uid, body, accent), studio(uid, 300, 336, 170, 16)]
    dark = shade(body, -.3)
    for dx in (-70, 0, 70):
        out.append(f'<path d="M 300 236 L {300 + dx * 1.5} 332" stroke="{body}" stroke-width="12" stroke-linecap="round"/>'
                   f'<circle cx="{300 + dx * 1.5}" cy="332" r="8" fill="{dark}"/>')
    out.append(f'<rect x="292" y="130" width="16" height="110" rx="6" fill="{dark}"/><circle cx="300" cy="236" r="16" fill="{body}"/>')
    # ball head and clamp with a phone in portrait
    out.append(f'<circle cx="300" cy="126" r="12" fill="{accent}"/>'
               f'<rect x="268" y="52" width="64" height="70" rx="6" fill="{dark}"/><rect x="262" y="58" width="76" height="12" rx="4" fill="{body}"/><rect x="262" y="104" width="76" height="12" rx="4" fill="{body}"/>'
               f'<rect x="274" y="60" width="52" height="56" rx="4" fill="#3A4453"/><rect x="278" y="64" width="44" height="48" rx="3" fill="#8FD3AE"/>')
    return "\n".join(out)

def draw_ssd(uid, a):
    """Portable SSD: a small rounded slab with a USB-C cable."""
    body = a.get("body", "#2F3A48"); accent = a.get("accent", "#1E8E5A")
    out = [defs(uid, body, accent), studio(uid, 300, 336, 190, 16)]
    dark = shade(body, -.3); lite = shade(body, .2)
    out.append(f'<rect x="190" y="170" width="220" height="118" rx="22" fill="url(#{uid}-front)" transform="rotate(-6 300 229)"/>'
               f'<rect x="190" y="170" width="220" height="118" rx="22" fill="none" stroke="{lite}" stroke-width="2" opacity="0.6" transform="rotate(-6 300 229)"/>'
               f'<rect x="214" y="196" width="80" height="12" rx="6" fill="{lite}" opacity="0.7" transform="rotate(-6 300 229)"/>'
               f'<rect x="214" y="218" width="120" height="8" rx="4" fill="{lite}" opacity="0.4" transform="rotate(-6 300 229)"/>'
               f'<rect x="300" y="250" width="86" height="22" rx="8" fill="{accent}" transform="rotate(-6 300 229)"/>')
    # USB-C port and cable
    out.append(f'<rect x="404" y="214" width="14" height="22" rx="4" fill="{dark}" transform="rotate(-6 300 229)"/>'
               f'<path d="M 418 226 q 60 10 80 60 q 10 30 -20 44" fill="none" stroke="{dark}" stroke-width="7" stroke-linecap="round"/>'
               f'<rect x="466" y="322" width="22" height="12" rx="4" fill="{dark}" transform="rotate(-30 477 328)"/>')
    return "\n".join(out)

DRAW = {"robot": draw_robot, "earbuds": draw_earbuds, "glasses": draw_glasses, "power": draw_power, "tracker": draw_tracker, "bottle": draw_bottle, "cleaner": draw_cleaner, "groomvac": draw_groomvac, "roller": draw_roller, "litterbot": draw_litterbot, "harness": draw_harness, "kong": draw_kong, "bags": draw_bags, "chat": draw_chat, "film": draw_film, "voice": draw_voice, "lightbox": draw_lightbox, "tripod": draw_tripod, "ssd": draw_ssd}

def render_product(category, art, uid, scale=1.0, tx=0, ty=0, with_studio=True):
    """Return SVG fragment (a <g>) with the product drawn at 600x400 coordinates, transformed."""
    svg = DRAW[category](uid, art)
    if not with_studio:
        # drop the studio background rect but keep the soft shadow
        svg = svg.replace(f'<rect width="{W}" height="{H}" rx="18" fill="url(#{uid}-bg)"/>', '', 1)
    return f'<g transform="translate({tx} {ty}) scale({scale})">{svg}</g>'

def card_svg(category, c):
    uid = "c" + "".join(ch for ch in c["id"] if ch.isalnum())
    inner = DRAW[category](uid, c.get("art", {}))
    chip = c.get("chip", ""); chip_w = 16 + int(len(chip) * 7.2)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(c["name"])} (product render)">
{inner}
<g font-family="{FONT}">
<rect x="18" y="18" width="{chip_w}" height="28" rx="14" fill="{NAVY}"/>
<text x="{18 + chip_w/2}" y="37" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">{esc(chip)}</text>
<text x="22" y="380" font-size="22" font-weight="700" fill="{NAVY}">{esc(c.get("short", c["name"]))}</text>
<text x="578" y="382" text-anchor="end" font-size="11" fill="#9a9a9a">Render, not a photo</text>
</g>
</svg>
'''

def main(post_dir):
    d = pathlib.Path(post_dir)
    spec = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    outdir = d / "images" / "cards"; outdir.mkdir(parents=True, exist_ok=True)
    for c in spec["cards"]:
        (outdir / f"{c['id']}.svg").write_text(card_svg(c.get("category", spec["category"]), c), encoding="utf-8")
    print(f"wrote {len(spec['cards'])} cards to {outdir}")

if __name__ == "__main__":
    main(sys.argv[1])
