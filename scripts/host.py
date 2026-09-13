#!/usr/bin/env python3
"""Vera — the illustrated Verdict Picks host. Flat-illustration style, waist-up, several poses.

draw_host(uid, pose="present", tx=0, ty=0, scale=1.0, glasses=None, earbud=None, flip=False)
  poses: present (open palm to the right), point, thumbsup, ear (finger to ear), hold (both hands in front), wave
  glasses: None | dict(frame="#111", style="wayfarer"|"round"|"xr")
  earbud:  None | colour  -> a bud in the visible ear
Coordinates: a 320x360 box, feet not drawn (waist-up). Returns an SVG <g>.
"""
FONT = "-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
SKIN, SKIN_D, HAIR, HAIR_L = "#EDBB94", "#D89C74", "#3A2A22", "#5A4034"
JACKET, JACKET_D, TOP, LIP, BLUSH = "#1B2A41", "#14202F", "#1E8E5A", "#C9575D", "#E58A7A"

def _arm(kind, flip):
    s = -1 if flip else 1
    def X(x): return 160 + s * (x - 160)
    if kind == "present":   # right arm extended to the right, palm up
        return (f'<path d="M {X(222)} 232 Q {X(262)} 236 {X(292)} 226 L {X(300)} 244 Q {X(266)} 258 {X(226)} 252 Z" fill="{JACKET}"/>'
                f'<ellipse cx="{X(312)}" cy="232" rx="17" ry="12" fill="{SKIN}"/>'
                f'<g stroke="{SKIN}" stroke-width="7" stroke-linecap="round"><path d="M {X(318)} 222 L {X(336)} 214"/><path d="M {X(322)} 228 L {X(342)} 224"/><path d="M {X(322)} 236 L {X(342)} 236"/><path d="M {X(318)} 242 L {X(336)} 246"/></g>')
    if kind == "point":
        return (f'<path d="M {X(222)} 232 Q {X(262)} 226 {X(296)} 208 L {X(306)} 224 Q {X(270)} 248 {X(226)} 252 Z" fill="{JACKET}"/>'
                f'<circle cx="{X(308)}" cy="214" r="13" fill="{SKIN}"/><path d="M {X(316)} 206 L {X(342)} 192" stroke="{SKIN}" stroke-width="9" stroke-linecap="round"/>')
    if kind == "thumbsup":
        return (f'<path d="M {X(222)} 232 Q {X(250)} 236 {X(262)} 210 L {X(280)} 216 Q {X(268)} 256 {X(226)} 254 Z" fill="{JACKET}"/>'
                f'<rect x="{X(258)-14}" y="176" width="28" height="30" rx="9" fill="{SKIN}"/><path d="M {X(262)} 178 q 0 -22 8 -26 q 10 -2 8 14 l -2 14" fill="{SKIN}" stroke="{SKIN_D}" stroke-width="1.5"/>')
    if kind == "ear":
        return (f'<path d="M {X(222)} 232 Q {X(262)} 222 {X(258)} 170 L {X(276)} 166 Q {X(284)} 240 {X(226)} 254 Z" fill="{JACKET}"/>'
                f'<circle cx="{X(266)}" cy="158" r="12" fill="{SKIN}"/><path d="M {X(262)} 150 L {X(236)} 132" stroke="{SKIN}" stroke-width="8" stroke-linecap="round"/>')
    if kind == "wave":
        return (f'<path d="M {X(222)} 232 Q {X(256)} 220 {X(262)} 176 L {X(282)} 178 Q {X(280)} 246 {X(226)} 254 Z" fill="{JACKET}"/>'
                f'<circle cx="{X(272)}" cy="160" r="15" fill="{SKIN}"/><g stroke="{SKIN}" stroke-width="8" stroke-linecap="round"><path d="M {X(264)} 148 L {X(258)} 126"/><path d="M {X(274)} 146 L {X(274)} 122"/><path d="M {X(284)} 150 L {X(292)} 128"/></g>')
    return ""

def draw_host(uid, pose="present", tx=0, ty=0, scale=1.0, glasses=None, earbud=None, flip=False, outfit=JACKET):
    g = []
    # hair back (long, behind the shoulders)
    g.append(f'<path d="M 108 120 Q 92 200 104 250 L 216 250 Q 228 200 212 120 Q 160 40 108 120 Z" fill="{HAIR}"/>')
    # neck & shoulders / torso
    g.append(f'<rect x="146" y="166" width="28" height="36" rx="10" fill="{SKIN_D}"/>')
    g.append(f'<path d="M 96 236 Q 100 210 132 202 L 160 196 L 188 202 Q 220 210 224 236 L 232 360 L 88 360 Z" fill="{outfit}"/>')
    g.append(f'<path d="M 138 204 L 160 244 L 182 204 L 172 200 L 160 220 L 148 200 Z" fill="{TOP}"/>')  # v-neck top
    g.append(f'<path d="M 136 204 L 118 360 M 184 204 L 202 360" stroke="{JACKET_D}" stroke-width="3" fill="none" opacity="0.6"/>')  # lapels
    # far arm (left, relaxed) unless pose is hold
    if pose == "hold":
        g.append(f'<path d="M 100 244 Q 104 292 140 292 L 180 292 Q 216 292 220 244 L 206 240 Q 200 274 176 274 L 144 274 Q 120 274 114 240 Z" fill="{outfit}"/>')
        g.append(f'<circle cx="138" cy="290" r="13" fill="{SKIN}"/><circle cx="182" cy="290" r="13" fill="{SKIN}"/>')
    else:
        g.append(f'<path d="M 98 240 Q 84 300 96 350 L 116 348 Q 108 300 118 244 Z" fill="{outfit}"/>')
        g.append(f'<circle cx="106" cy="352" r="12" fill="{SKIN}"/>')
    # head
    g.append(f'<ellipse cx="160" cy="118" rx="50" ry="58" fill="{SKIN}"/>')
    g.append(f'<path d="M 110 118 q -8 26 12 22 M 210 118 q 8 26 -12 22" stroke="{SKIN}" stroke-width="10" stroke-linecap="round" fill="none"/>')  # ears
    # hair front: side-swept bangs
    g.append(f'<path d="M 108 116 Q 112 52 168 56 Q 216 60 212 118 Q 208 92 184 84 Q 150 104 122 92 Q 110 100 108 116 Z" fill="{HAIR}"/>')
    g.append(f'<path d="M 128 72 Q 150 60 178 66" stroke="{HAIR_L}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.8"/>')
    # brows
    g.append(f'<path d="M 130 100 q 12 -8 26 -2 M 166 98 q 14 -6 26 2" stroke="{HAIR}" stroke-width="3.2" fill="none" stroke-linecap="round"/>')
    # eyes
    for ex in (143, 179):
        g.append(f'<path d="M {ex-12} 116 q 12 -12 24 0 q -12 10 -24 0 z" fill="#fff"/><circle cx="{ex+1}" cy="115" r="5.2" fill="#3B2A22"/><circle cx="{ex+3}" cy="113" r="1.8" fill="#fff"/>')
        g.append(f'<path d="M {ex-12} 116 q 12 -12 24 0" stroke="#2A1D17" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    # nose, mouth, blush
    g.append(f'<path d="M 160 124 q -6 12 4 16" stroke="{SKIN_D}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
    g.append(f'<path d="M 146 150 q 14 14 30 0 q -15 6 -30 0 z" fill="{LIP}"/><path d="M 146 150 q 14 8 30 0" stroke="#A8434A" stroke-width="1.5" fill="none"/>')
    g.append(f'<ellipse cx="132" cy="136" rx="9" ry="5" fill="{BLUSH}" opacity="0.35"/><ellipse cx="190" cy="136" rx="9" ry="5" fill="{BLUSH}" opacity="0.35"/>')
    # earrings
    g.append(f'<circle cx="112" cy="146" r="3.5" fill="#D4AF37"/><circle cx="208" cy="146" r="3.5" fill="#D4AF37"/>')
    if earbud:
        g.append(f'<ellipse cx="209" cy="140" rx="7" ry="8" fill="{earbud}"/><circle cx="211" cy="138" r="2" fill="#fff" opacity="0.6"/>')
    if glasses:
        fr = glasses.get("frame", "#111"); st = glasses.get("style", "wayfarer")
        if st == "round":
            g.append(f'<circle cx="143" cy="116" r="17" fill="#8FB3D9" fill-opacity="0.35" stroke="{fr}" stroke-width="3.5"/><circle cx="179" cy="116" r="17" fill="#8FB3D9" fill-opacity="0.35" stroke="{fr}" stroke-width="3.5"/>')
        else:
            g.append(f'<path d="M 124 104 h 36 q 4 0 4 4 l -3 20 q -1 5 -6 5 h -26 q -5 0 -6 -5 l -3 -20 q 0 -4 4 -4 z" fill="#8FB3D9" fill-opacity="0.35" stroke="{fr}" stroke-width="3.5" stroke-linejoin="round"/>'
                     f'<path d="M 162 104 h 36 q 4 0 4 4 l -3 20 q -1 5 -6 5 h -26 q -5 0 -6 -5 l -3 -20 q 0 -4 4 -4 z" fill="#8FB3D9" fill-opacity="0.35" stroke="{fr}" stroke-width="3.5" stroke-linejoin="round"/>')
            g.append(f'<circle cx="128" cy="108" r="2.5" fill="#333"/>')
        g.append(f'<path d="M 158 108 q 2 -4 6 0 M 121 108 L 112 106 M 201 108 L 210 106" stroke="{fr}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    # near arm (pose)
    g.append(_arm(pose, flip))
    inner = "".join(g)
    tr = f"translate({tx} {ty}) scale({scale})" + (" translate(320 0) scale(-1 1)" if flip else "")
    return f'<g transform="{tr}">{inner}</g>'

def speech_bubble(x, y, w, lines, tail="left", font=17, bold_first=True):
    """A rounded speech bubble with wrapped lines (list of strings)."""
    h = 22 + len(lines) * (font + 6)
    tail_path = f'M {x+30} {y+h} l 10 18 l 14 -18 z' if tail == "left" else f'M {x+w-44} {y+h} l -10 18 l -14 -18 z'
    t = "".join(f'<text x="{x+16}" y="{y+18+font+i*(font+6)}" font-family="{FONT}" font-size="{font}" font-weight="{800 if (i==0 and bold_first) else 500}" fill="#1B2A41">{ln}</text>' for i, ln in enumerate(lines))
    return f'<path d="{tail_path}" fill="#fff" stroke="#1B2A41" stroke-width="3"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#fff" stroke="#1B2A41" stroke-width="3"/><rect x="{x+3}" y="{y+3}" width="{w-6}" height="{h-6}" rx="12" fill="#fff"/>{t}'

def host_banner(uid, lines, pose="present", glasses=None, earbud=None, name="Vera, your Verdict Picks host"):
    """1200x300 banner: the host at left, a speech bubble with the verdict at right."""
    bubble = speech_bubble(330, 40, 830, lines, tail="left", font=24)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" role="img" aria-label="{name}: {" ".join(lines)}">'
            f'<rect width="1200" height="300" rx="18" fill="#F7F5F0"/>'
            f'<ellipse cx="160" cy="296" rx="150" ry="10" fill="#000" opacity="0.12"/>'
            + draw_host(uid, pose, tx=20, ty=-10, scale=0.86, glasses=glasses, earbud=earbud)
            + bubble
            + f'<text x="1160" y="284" text-anchor="end" font-family="{FONT}" font-size="13" fill="#888">{name} · illustration</text>'
            + '</svg>')

if __name__ == "__main__":
    import sys, pathlib
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/host-test.svg")
    poses = ["present", "point", "thumbsup", "ear", "hold", "wave"]
    body = "".join(draw_host("t", p, tx=20 + i*330, ty=40, scale=0.9, glasses={"frame": "#111"} if p in ("present",) else None, earbud="#222" if p == "ear" else None) for i, p in enumerate(poses))
    out.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2000 400"><rect width="2000" height="400" fill="#F7F5F0"/>{body}</svg>')
    print("wrote", out)
