#!/usr/bin/env python3
"""The webtoon cast and props, drawn as flat SVG (original characters; no existing series' designs).

person(who, expr="neutral", pose="rest", x=0, y=0, s=1.0, flip=False) -> <g>
  who:   vera  (the Verdict Picks host: long dark hair, navy jacket, green top, as in host.py)
         sam   (a shopper: short curly hair, mustard hoodie)
         jo    (a shopper: bob haircut, round glasses, teal cardigan)
  expr:  neutral, happy, shock, worried, smug, think, sad, determined
  pose:  rest, phone, point, present, headgrab, thumbsup, wave, hold (box or object in both hands), chin (hand on chin)
  Box: 300 x 360, waist-up, head centre (150, 118). Feet are never drawn.
chibi(who, expr, x, y, s)      big-head comedy version, box 200 x 220
dog(x, y, s, mood)             a small original beagle-type dog, mood: calm, alert, sleepy
robot(x, y, s, beams, view)    a generic round robot vacuum with a laser turret, no brand marks; view: side, top
cord(x, y, w), sock(x, y, s)   floor clutter
phone(x, y, s, lines, title)   a phone screen with text lines (headline style)
Everything returns an SVG fragment; coordinates are the caller's.
"""
FONT = "-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
INK = "#1B2A41"

CAST = {
    "vera": dict(skin="#EDBB94", skin_d="#D89C74", hair="#3A2A22", hair_l="#5A4034", outfit="#1B2A41", outfit_d="#14202F", top="#1E8E5A", lip="#C9575D", style="long"),
    "sam":  dict(skin="#B9825C", skin_d="#9A6644", hair="#2B1E18", hair_l="#4A372C", outfit="#E0A43B", outfit_d="#C08528", top="#F5E6C8", lip="#9C5A4A", style="curly"),
    "jo":   dict(skin="#F2CDA9", skin_d="#DDAA82", hair="#8A4B2A", hair_l="#A9653D", outfit="#2A9D8F", outfit_d="#1F7A6F", top="#FFFFFF", lip="#C9575D", style="bob"),
}

def _g(inner, x, y, s, flip, w=300):
    tr = f"translate({x:.1f} {y:.1f}) scale({s})" + (f" translate({w} 0) scale(-1 1)" if flip else "")
    return f'<g transform="{tr}">{inner}</g>'

def _eyes(c, expr):
    g = []
    if expr == "happy":
        for ex in (131, 169):
            g.append(f'<path d="M {ex-12} 120 q 12 -14 24 0" stroke="#2A1D17" stroke-width="4" fill="none" stroke-linecap="round"/>')
        return "".join(g)
    if expr == "shock":
        for ex in (131, 169):
            g.append(f'<ellipse cx="{ex}" cy="116" rx="13" ry="15" fill="#fff" stroke="#2A1D17" stroke-width="2.6"/><circle cx="{ex}" cy="117" r="3.6" fill="#2A1D17"/>')
        return "".join(g)
    if expr == "smug":
        for ex in (131, 169):
            g.append(f'<path d="M {ex-12} 118 q 12 -6 24 0 q -12 8 -24 0 z" fill="#fff"/><circle cx="{ex+2}" cy="119" r="4.6" fill="#3B2A22"/>'
                     f'<path d="M {ex-13} 117 q 13 -6 26 0" stroke="#2A1D17" stroke-width="3.4" fill="none" stroke-linecap="round"/>')
        return "".join(g)
    if expr == "determined":
        for ex in (131, 169):
            g.append(f'<path d="M {ex-12} 118 q 12 -10 24 0 q -12 9 -24 0 z" fill="#fff"/><circle cx="{ex}" cy="117" r="5.4" fill="#3B2A22"/><circle cx="{ex+2}" cy="115" r="1.8" fill="#fff"/>'
                     f'<path d="M {ex-12} 118 q 12 -10 24 0" stroke="#2A1D17" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
        return "".join(g)
    dx, dy = (4, -4) if expr == "think" else (1, 0)
    for ex in (131, 169):
        g.append(f'<path d="M {ex-12} 118 q 12 -13 24 0 q -12 11 -24 0 z" fill="#fff"/><circle cx="{ex+dx}" cy="{117+dy}" r="5.4" fill="#3B2A22"/><circle cx="{ex+dx+2}" cy="{115+dy}" r="1.8" fill="#fff"/>')
        g.append(f'<path d="M {ex-12} 118 q 12 -13 24 0" stroke="#2A1D17" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
    return "".join(g)

def _brows(c, expr):
    h = c["hair"]
    shapes = {
        "neutral": "M 118 100 q 12 -7 25 -2 M 157 98 q 13 -5 25 2",
        "happy": "M 118 98 q 12 -9 25 -3 M 157 95 q 13 -6 25 3",
        "shock": "M 117 90 q 13 -10 26 -4 M 157 86 q 13 -6 26 4",
        "worried": "M 118 96 q 12 2 24 -6 M 158 90 q 12 8 24 6",
        "sad": "M 118 98 q 12 2 24 -6 M 158 92 q 12 8 24 6",
        "smug": "M 118 102 q 12 -3 25 0 M 157 92 q 13 -8 25 0",
        "think": "M 118 96 q 12 -8 25 -2 M 157 100 q 13 -2 25 0",
        "determined": "M 118 96 q 12 6 25 8 M 157 104 q 13 -2 25 -8",
    }
    return f'<path d="{shapes.get(expr, shapes["neutral"])}" stroke="{h}" stroke-width="4" fill="none" stroke-linecap="round"/>'

def _mouth(c, expr):
    lip = c["lip"]
    if expr == "happy":
        return f'<path d="M 132 146 q 18 22 36 0 z" fill="#7A2E33"/><path d="M 138 152 q 12 8 24 0" fill="#E98C8C"/>'
    if expr == "shock":
        return '<ellipse cx="150" cy="154" rx="10" ry="13" fill="#4A1F24"/><ellipse cx="150" cy="160" rx="6" ry="4" fill="#D9737A"/>'
    if expr in ("worried", "sad"):
        return f'<path d="M 136 156 q 7 -7 14 0 q 7 7 14 0" stroke="#7A2E33" stroke-width="3.2" fill="none" stroke-linecap="round"/>' if expr == "worried" else \
               '<path d="M 138 158 q 12 -10 24 0" stroke="#7A2E33" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
    if expr == "smug":
        return '<path d="M 136 150 q 14 8 30 -6" stroke="#7A2E33" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
    if expr == "think":
        return '<path d="M 142 154 h 14" stroke="#7A2E33" stroke-width="3.4" stroke-linecap="round"/>'
    if expr == "determined":
        return '<path d="M 136 150 q 14 6 28 0" stroke="#7A2E33" stroke-width="3.6" fill="none" stroke-linecap="round"/>'
    return f'<path d="M 136 148 q 14 14 28 0 q -14 6 -28 0 z" fill="{lip}"/>'

def _extras(expr):
    if expr == "shock":
        return ('<g stroke="#2A1D17" stroke-width="3" stroke-linecap="round"><path d="M 82 70 l -16 -14"/><path d="M 74 96 l -22 -4"/><path d="M 218 70 l 16 -14"/><path d="M 226 96 l 22 -4"/></g>')
    if expr in ("worried", "sad"):
        return '<path d="M 206 84 q 10 16 0 22 q -10 -6 0 -22 z" fill="#7FC4F0" stroke="#3B7FB0" stroke-width="1.5"/>'
    if expr == "happy":
        return '<ellipse cx="118" cy="138" rx="10" ry="5" fill="#E58A7A" opacity="0.55"/><ellipse cx="182" cy="138" rx="10" ry="5" fill="#E58A7A" opacity="0.55"/>'
    if expr == "determined":
        return '<path d="M 214 66 l 10 -14 l 4 12 l 12 -6" stroke="#E0A43B" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    return ""

def head(who, expr="neutral"):
    c = CAST[who]; g = []
    st = c["style"]
    if st == "long":
        g.append(f'<path d="M 96 118 Q 80 200 92 252 L 208 252 Q 220 200 204 118 Q 150 34 96 118 Z" fill="{c["hair"]}"/>')
    elif st == "bob":
        g.append(f'<path d="M 92 120 Q 86 172 100 182 L 200 182 Q 214 172 208 120 Q 150 36 92 120 Z" fill="{c["hair"]}"/>')
    g.append(f'<ellipse cx="150" cy="118" rx="52" ry="58" fill="{c["skin"]}"/>')
    g.append(f'<ellipse cx="98" cy="124" rx="9" ry="13" fill="{c["skin"]}"/><ellipse cx="202" cy="124" rx="9" ry="13" fill="{c["skin"]}"/>')
    if st == "long":
        g.append(f'<path d="M 96 116 Q 100 50 156 54 Q 206 58 204 118 Q 198 90 172 82 Q 138 102 110 90 Q 98 98 96 116 Z" fill="{c["hair"]}"/>'
                 f'<path d="M 116 70 Q 138 58 166 64" stroke="{c["hair_l"]}" stroke-width="4" fill="none" stroke-linecap="round"/>'
                 '<circle cx="99" cy="142" r="3.5" fill="#D4AF37"/><circle cx="201" cy="142" r="3.5" fill="#D4AF37"/>')
    elif st == "curly":
        bumps = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c["hair"]}"/>' for cx, cy, r in
                        [(104, 92, 18), (118, 72, 20), (142, 60, 21), (166, 60, 21), (188, 72, 20), (200, 92, 17), (128, 82, 16), (172, 82, 16), (150, 74, 18)])
        g.append(bumps + f'<path d="M 132 66 q 8 -6 16 0 M 162 68 q 8 -6 14 2" stroke="{c["hair_l"]}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    elif st == "bob":
        g.append(f'<path d="M 94 120 Q 96 52 152 52 Q 206 54 206 120 Q 200 84 150 80 Q 104 84 94 120 Z" fill="{c["hair"]}"/>'
                 f'<path d="M 120 64 Q 146 54 176 62" stroke="{c["hair_l"]}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    g.append(_brows(c, expr)); g.append(_eyes(c, expr))
    g.append(f'<path d="M 150 126 q -6 12 4 16" stroke="{c["skin_d"]}" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
    g.append(_mouth(c, expr))
    if who == "jo":
        g.append('<g fill="#9FC3E6" fill-opacity="0.25" stroke="#3A2A22" stroke-width="3.2"><circle cx="131" cy="118" r="18"/><circle cx="169" cy="118" r="18"/></g>'
                 '<path d="M 149 116 q 1 -4 2 0 M 113 116 L 100 112 M 187 116 L 200 112" stroke="#3A2A22" stroke-width="3" fill="none"/>')
    g.append(_extras(expr))
    return "".join(g)

def _arm(c, kind):
    o, sk = c["outfit"], c["skin"]
    if kind == "present":
        return (f'<path d="M 212 232 Q 252 236 282 226 L 290 244 Q 256 258 216 252 Z" fill="{o}"/><ellipse cx="302" cy="232" rx="17" ry="12" fill="{sk}"/>'
                f'<g stroke="{sk}" stroke-width="7" stroke-linecap="round"><path d="M 308 222 L 326 214"/><path d="M 312 228 L 332 224"/><path d="M 312 236 L 332 236"/></g>')
    if kind == "point":
        return (f'<path d="M 212 232 Q 252 226 286 206 L 296 222 Q 260 248 216 252 Z" fill="{o}"/>'
                f'<circle cx="298" cy="212" r="13" fill="{sk}"/><path d="M 306 204 L 334 188" stroke="{sk}" stroke-width="9" stroke-linecap="round"/>')
    if kind == "thumbsup":
        return (f'<path d="M 212 232 Q 240 236 252 210 L 270 216 Q 258 256 216 254 Z" fill="{o}"/>'
                f'<rect x="244" y="176" width="28" height="30" rx="9" fill="{sk}"/><path d="M 252 178 q 0 -22 8 -26 q 10 -2 8 14 l -2 14" fill="{sk}"/>')
    if kind == "wave":
        return (f'<path d="M 212 232 Q 246 220 252 176 L 272 178 Q 270 246 216 254 Z" fill="{o}"/>'
                f'<circle cx="262" cy="160" r="15" fill="{sk}"/><g stroke="{sk}" stroke-width="8" stroke-linecap="round"><path d="M 254 148 L 248 126"/><path d="M 264 146 L 264 122"/><path d="M 274 150 L 282 128"/></g>')
    if kind == "chin":
        return (f'<path d="M 212 236 Q 220 196 186 184 L 178 200 Q 200 212 200 250 Z" fill="{o}"/><circle cx="172" cy="178" r="14" fill="{sk}"/>')
    return ""

def person(who, expr="neutral", pose="rest", x=0, y=0, s=1.0, flip=False, prop=None):
    c = CAST[who]; o, od, sk = c["outfit"], c["outfit_d"], c["skin"]; g = []
    g.append(f'<rect x="136" y="164" width="28" height="40" rx="10" fill="{c["skin_d"]}"/>')
    g.append(f'<path d="M 86 236 Q 90 210 122 202 L 150 196 L 178 202 Q 210 210 214 236 L 222 360 L 78 360 Z" fill="{o}"/>')
    if who == "sam":   # hoodie: hood rim and strings
        g.append(f'<path d="M 112 206 Q 150 236 188 206 Q 182 198 150 214 Q 118 198 112 206 Z" fill="{od}"/>'
                 f'<path d="M 138 222 l -2 40 M 162 222 l 2 40" stroke="{c["top"]}" stroke-width="4" stroke-linecap="round"/>')
    else:
        g.append(f'<path d="M 128 204 L 150 244 L 172 204 L 162 200 L 150 220 L 138 200 Z" fill="{c["top"]}"/>'
                 f'<path d="M 126 204 L 108 360 M 174 204 L 192 360" stroke="{od}" stroke-width="3" fill="none" opacity="0.6"/>')
    both = pose in ("phone", "hold", "headgrab")
    if pose == "phone":
        g.append(f'<path d="M 90 244 Q 96 290 130 290 L 170 290 Q 204 290 210 244 L 196 240 Q 190 274 166 274 L 134 274 Q 110 274 104 240 Z" fill="{o}"/>'
                 f'<rect x="128" y="236" width="44" height="66" rx="7" fill="#22252B" transform="rotate(-8 150 270)"/><rect x="133" y="242" width="34" height="52" rx="4" fill="#9FD3FF" transform="rotate(-8 150 270)"/>'
                 f'<circle cx="130" cy="284" r="12" fill="{sk}"/><circle cx="172" cy="280" r="12" fill="{sk}"/>')
    elif pose == "hold":
        g.append(f'<path d="M 90 244 Q 94 292 130 292 L 170 292 Q 206 292 210 244 L 196 240 Q 190 274 166 274 L 134 274 Q 110 274 104 240 Z" fill="{o}"/>')
        if prop: g.append(prop)
        g.append(f'<circle cx="128" cy="290" r="13" fill="{sk}"/><circle cx="172" cy="290" r="13" fill="{sk}"/>')
    elif pose == "headgrab":
        g.append(f'<path d="M 90 240 Q 60 180 86 120 L 104 128 Q 84 180 108 236 Z" fill="{o}"/><path d="M 210 240 Q 240 180 214 120 L 196 128 Q 216 180 192 236 Z" fill="{o}"/>')
    else:
        g.append(f'<path d="M 88 240 Q 74 300 86 350 L 106 348 Q 98 300 108 244 Z" fill="{o}"/><circle cx="96" cy="352" r="12" fill="{sk}"/>')
    g.append(head(who, expr))
    if pose == "headgrab":
        g.append(f'<circle cx="94" cy="110" r="15" fill="{sk}"/><circle cx="206" cy="110" r="15" fill="{sk}"/>')
    if not both:
        g.append(_arm(c, pose) if pose != "rest" else f'<path d="M 212 240 Q 226 300 214 350 L 194 348 Q 202 300 192 244 Z" fill="{o}"/><circle cx="204" cy="352" r="12" fill="{sk}"/>')
    return _g("".join(g), x, y, s, flip)

def chibi(who, expr="shock", x=0, y=0, s=1.0, flip=False, arms="up"):
    """Comedy reaction: a big head on a small body (box about 200 x 240)."""
    c = CAST[who]; o, sk = c["outfit"], c["skin"]
    body = f'<path d="M 64 150 Q 100 132 136 150 L 146 238 L 54 238 Z" fill="{o}"/>'
    if arms == "up":
        body += (f'<path d="M 70 162 L 26 104" stroke="{o}" stroke-width="18" stroke-linecap="round"/><circle cx="22" cy="98" r="12" fill="{sk}"/>'
                 f'<path d="M 130 162 L 174 104" stroke="{o}" stroke-width="18" stroke-linecap="round"/><circle cx="178" cy="98" r="12" fill="{sk}"/>')
    h = f'<g transform="translate(-20 -6) scale(0.8)">{head(who, expr)}</g>'
    return _g(body + h, x, y, s, flip, w=200)

def dog(x=0, y=0, s=1.0, mood="calm", flip=False):
    """Sitting beagle-type dog, box 220 x 220, facing right."""
    eye = {"calm": '<circle cx="150" cy="78" r="6" fill="#2A1D17"/><circle cx="152" cy="76" r="2" fill="#fff"/>',
           "alert": '<circle cx="150" cy="78" r="8" fill="#fff" stroke="#2A1D17" stroke-width="2"/><circle cx="152" cy="78" r="4" fill="#2A1D17"/>',
           "sleepy": '<path d="M 142 78 q 8 6 16 0" stroke="#2A1D17" stroke-width="3" fill="none" stroke-linecap="round"/>'}[mood]
    g = ('<path d="M 30 196 Q 20 120 70 104 L 120 100 Q 140 140 132 196 Z" fill="#C8894B"/>'           # body
         '<path d="M 52 130 Q 74 112 104 118 Q 96 150 60 150 Z" fill="#3A2A22"/>'                          # saddle
         '<path d="M 96 150 Q 116 150 122 196 L 92 196 Z" fill="#FFF6EA"/>'                                 # chest
         '<path d="M 30 186 q -24 -20 -10 -60" stroke="#C8894B" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M 22 130 q -2 -10 4 -14" stroke="#FFF6EA" stroke-width="12" stroke-linecap="round"/>'
         '<ellipse cx="62" cy="198" rx="26" ry="10" fill="#C8894B"/><ellipse cx="110" cy="200" rx="18" ry="9" fill="#FFF6EA"/>'
         '<ellipse cx="136" cy="80" rx="42" ry="38" fill="#C8894B"/>'                                       # head
         '<path d="M 150 60 Q 186 70 184 96 Q 170 112 150 104 Z" fill="#FFF6EA"/>'                         # muzzle blaze
         '<ellipse cx="184" cy="92" rx="8" ry="6" fill="#2A1D17"/>'
         '<path d="M 106 60 Q 84 70 92 122 Q 112 118 116 76 Z" fill="#7A4A26"/>'                            # ear
         + eye + '<path d="M 166 106 q 8 6 16 0" stroke="#2A1D17" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    return _g(g, x, y, s, flip, w=220)

def robot(x=0, y=0, s=1.0, beams=False, view="side", flip=False, label=None):
    """Generic round robot vacuum, box 260 x 120 (side) with a LiDAR turret; no brand marks."""
    if view == "top":
        g = ('<circle cx="130" cy="130" r="120" fill="#F4F5F7" stroke="#B8BEC8" stroke-width="4"/><circle cx="130" cy="130" r="96" fill="none" stroke="#DDE1E7" stroke-width="3"/>'
             '<circle cx="130" cy="96" r="30" fill="#2B2F36"/><circle cx="130" cy="96" r="18" fill="#3D434C"/><path d="M 40 210 A 120 120 0 0 0 220 210" stroke="#7D8590" stroke-width="10" fill="none"/>')
        if beams:
            g += "".join(f'<path d="M 130 96 L {130+260*__import__("math").cos(a):.0f} {96+260*__import__("math").sin(a):.0f}" stroke="#E63946" stroke-width="3" stroke-dasharray="10 8" opacity="0.8"/>' for a in [i*0.785 for i in range(8)])
        return _g(g, x, y, s, flip, w=260)
    g = ('<ellipse cx="130" cy="96" rx="128" ry="22" fill="#00000022"/>'
         '<path d="M 6 66 L 6 86 Q 130 122 254 86 L 254 66 Z" fill="#B8BEC8"/>'
         '<ellipse cx="130" cy="66" rx="124" ry="30" fill="#F4F5F7" stroke="#B8BEC8" stroke-width="3"/>'
         '<path d="M 200 80 Q 236 76 252 66 L 254 86 Q 236 96 200 100 Z" fill="#5F6873"/>'      # front bumper band
         '<path d="M 98 48 L 98 30 Q 130 22 162 30 L 162 48 Q 130 56 98 48 Z" fill="#2B2F36"/>'
         '<ellipse cx="130" cy="30" rx="32" ry="8" fill="#3D434C"/>')
    if beams:
        g += ('<g stroke="#E63946" stroke-width="3" stroke-dasharray="10 8" opacity="0.85">'
              '<path d="M 164 38 L 330 10"/><path d="M 164 40 L 340 48"/><path d="M 96 38 L -70 10"/><path d="M 96 40 L -80 50"/></g>')
    if label:
        g += f'<text x="130" y="76" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#5F6873">{label}</text>'
    return _g(g, x, y, s, flip, w=260)

def cord(x=0, y=0, w=300, color="#222"):
    return (f'<path d="M {x} {y} q {w*0.2} -30 {w*0.4} 0 t {w*0.4} 0 q {w*0.1} 14 {w*0.2} -6" stroke="{color}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<rect x="{x+w-6}" y="{y-20}" width="26" height="18" rx="3" fill="#EEE" stroke="#999" stroke-width="2"/>')

def sock(x=0, y=0, s=1.0, color="#E76F51"):
    return _g(f'<path d="M 10 10 L 50 10 L 50 46 Q 52 62 72 64 L 76 80 Q 30 86 14 60 Z" fill="{color}"/><path d="M 10 10 L 50 10 L 50 22 L 10 22 Z" fill="#fff" opacity="0.7"/>', x, y, s, False, w=90)

def phone(x=0, y=0, s=1.0, title="", lines=()):
    """A phone held up to the reader: 300 x 520 box."""
    t = "".join(f'<text x="36" y="{166 + i*32}" font-family="{FONT}" font-size="21" fill="#1B2A41">{l}</text>' for i, l in enumerate(lines))
    g = ('<rect x="0" y="0" width="300" height="520" rx="40" fill="#22252B"/><rect x="16" y="40" width="268" height="440" rx="16" fill="#FFFFFF"/>'
         '<rect x="120" y="16" width="60" height="10" rx="5" fill="#444"/>'
         f'<rect x="16" y="40" width="268" height="76" rx="16" fill="#E9EEF5"/><text x="40" y="90" font-family="{FONT}" font-size="22" font-weight="800" fill="#C1121F">{title}</text>' + t)
    return _g(g, x, y, s, False, w=300)
