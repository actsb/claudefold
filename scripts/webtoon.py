#!/usr/bin/env python3
"""Render a post's vertical-scroll comic (webtoon.json) into 800-px-wide SVG slices, plus a transcript.

  python3 scripts/webtoon.py posts/<dir> [--svg-only]   # images/toon/<id>-<n>.svg, then 1600-px WebP slices; toon-<id>.json (slices, alt text, transcript)
  In src/00-easy.html put <!--TOON:<id>--> where the comic goes (assemble_post.py turns it into the images and a transcript).

webtoon.json:
{ "id": "ep1", "series": "Verdict Picks Toon", "title": "...", "subtitle": "...",
  "panels": [ { "gap": 60, "h": 520, "bg": "night-room", "full": false, "border": true,
                "items": [ {"t": "char", "who": "sam", "expr": "worried", "pose": "phone", "x": 60, "y": 160, "s": 1.0, "flip": false},
                           {"t": "say", "who": "sam", "text": "...", "x": 400, "y": 30, "w": 360, "tail": [200, 200], "kind": "talk|shout|whisper"},
                           {"t": "narr", "text": "...", "x": 20, "y": 20, "w": 400},
                           {"t": "sfx", "text": "BZZT", "x": 600, "y": 120, "size": 64, "rot": -10, "color": "#E63946"},
                           {"t": "dog"|"robot"|"cord"|"sock"|"phone"|"chibi"|"card"|"focus"|"text"|"arrow", ...} ] } ] }
Coordinates are inside the panel (panel width 720, or 800 when "full"). Characters are original; facts in the
dialogue must come from the post with its source. The first and last panels carry the fictional-characters note.
"""
import json, math, pathlib, re, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import toon_cast as C

W, MARGIN, MAXH = 800, 40, 1280
FONT, INK = C.FONT, C.INK
NAMES = {"vera": "Vera", "sam": "Sam", "jo": "Jo", "june": "Grandma June", "narr": "Caption"}

def esc(s): return html.escape(s, quote=False)

def wrap(text, width, size, bold=False):
    cw = size * (0.58 if bold else 0.53)
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split():
            t = (line + " " + w).strip()
            if len(t) * cw > width and line: out.append(line); line = w
            else: line = t
        out.append(line)
    return out

def text_block(lines, x, y, size, weight=600, anchor="middle", fill=INK, lh=1.28):
    return "".join(f'<text x="{x:.0f}" y="{y + size + i*size*lh:.0f}" text-anchor="{anchor}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(l)}</text>' for i, l in enumerate(lines))

def balloon(it, pw=720):
    size = it.get("size", 28); kind = it.get("kind", "talk"); maxw = it.get("w", 360)
    lines = wrap(it["text"], maxw - 44, size, bold=(kind == "shout"))
    tw = max(len(l) for l in lines) * size * (0.58 if kind == "shout" else 0.53)
    bw = min(maxw, tw + 48); bh = len(lines) * size * 1.28 + 30
    cx, y = it["x"], it["y"]; x = min(max(cx - bw / 2, 14), pw - bw - 14); cx = x + bw / 2   # keep the balloon inside the panel
    stroke = 'stroke-dasharray="8 6"' if kind == "whisper" else ""
    out = []
    if "tail" in it:
        tx, ty = it["tail"]; bx = min(max(tx, x + 30), x + bw - 30); by = y + bh / 2
        ang = math.atan2(ty - by, tx - bx); px, py = 16 * math.sin(ang), -16 * math.cos(ang)
        out.append(f'<path d="M {bx+px:.0f} {by+py:.0f} L {tx:.0f} {ty:.0f} L {bx-px:.0f} {by-py:.0f} Z" fill="#fff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    if kind == "shout":
        pts = []; n = 22; rx, ry = bw / 2 * 1.18 + 14, bh / 2 * 1.5 + 12
        for i in range(n * 2):
            a = math.pi * i / n; r = 1.0 if i % 2 == 0 else 0.86
            pts.append(f"{x + bw/2 + rx*r*math.cos(a):.0f},{y + bh/2 + ry*r*math.sin(a):.0f}")
        out.append(f'<polygon points="{" ".join(pts)}" fill="#fff" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')
    else:
        out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{bh:.0f}" rx="{min(34, bh/2):.0f}" fill="#fff" stroke="{INK}" stroke-width="3" {stroke}/>')
        if "tail" in it:   # hide the tail's base line inside the balloon
            out.append(f'<rect x="{x+3:.0f}" y="{y+3:.0f}" width="{bw-6:.0f}" height="{bh-6:.0f}" rx="{min(31, bh/2-3):.0f}" fill="#fff"/>')
    out.append(text_block(lines, cx, y + 13, size, 800 if kind == "shout" else 600))
    return "".join(out)

def narr(it):
    size = it.get("size", 25); w = it.get("w", 420)
    lines = wrap(it["text"], w - 36, size)
    h = len(lines) * size * 1.3 + 26
    dark = it.get("dark", False)
    bg, fg = ("#1B2A41", "#FFFFFF") if dark else ("#FFF4D6", INK)
    return (f'<rect x="{it["x"]}" y="{it["y"]}" width="{w}" height="{h:.0f}" fill="{bg}" stroke="{INK}" stroke-width="2.5"/>'
            + text_block(lines, it["x"] + 18, it["y"] + 11, size, 600, "start", fg, 1.3))

def sfx(it):
    size = it.get("size", 64)
    return (f'<text x="{it["x"]}" y="{it["y"]}" transform="rotate({it.get("rot", -8)} {it["x"]} {it["y"]})" text-anchor="middle" font-family="Impact,Arial Black,{FONT}" '
            f'font-size="{size}" font-weight="900" fill="{it.get("color", "#E63946")}" stroke="#fff" stroke-width="{size/7:.0f}" paint-order="stroke" letter-spacing="2">{esc(it["text"])}</text>')

def card(it):
    """An explainer board: title plus rows of [label, value] or plain lines."""
    w = it.get("w", 560); size = it.get("size", 24); rows = it["rows"]; x, y = it["x"], it["y"]
    h = 70 + len(rows) * (size + 22)
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#fff" stroke="{INK}" stroke-width="3.5"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="54" rx="18" fill="{it.get("color", "#1E8E5A")}"/><rect x="{x}" y="{y+36}" width="{w}" height="18" fill="{it.get("color", "#1E8E5A")}"/>',
           f'<text x="{x+22}" y="{y+37}" font-family="{FONT}" font-size="{size}" font-weight="800" fill="#fff">{esc(it["title"])}</text>']
    for i, r in enumerate(rows):
        ry = y + 54 + 14 + i * (size + 22) + size
        if isinstance(r, list):
            out.append(f'<text x="{x+22}" y="{ry}" font-family="{FONT}" font-size="{size}" font-weight="800" fill="{INK}">{esc(r[0])}</text>'
                       f'<text x="{x+w-22}" y="{ry}" text-anchor="end" font-family="{FONT}" font-size="{size}" font-weight="600" fill="{r[2] if len(r) > 2 else INK}">{esc(r[1])}</text>')
        else:
            out.append(f'<text x="{x+22}" y="{ry}" font-family="{FONT}" font-size="{size}" font-weight="600" fill="{INK}">{esc(r)}</text>')
    return "".join(out)

def focus(pw, ph, color="#1B2A41", n=56):
    cx, cy = pw / 2, ph / 2; R = math.hypot(pw, ph); out = []
    for i in range(n):
        a = 2 * math.pi * i / n + (i % 3) * 0.02; r0 = R * (0.30 + 0.12 * ((i * 7) % 5) / 5)
        a2 = a + 0.025
        out.append(f'<path d="M {cx+R*math.cos(a):.0f} {cy+R*math.sin(a):.0f} L {cx+r0*math.cos(a):.0f} {cy+r0*math.sin(a):.0f} L {cx+R*math.cos(a2):.0f} {cy+R*math.sin(a2):.0f} Z" fill="{color}" opacity="0.55"/>')
    return "".join(out)

def background(kind, pw, ph, uid):
    if kind == "none": return ""
    if kind.startswith("color:"): return f'<rect width="{pw}" height="{ph}" fill="{kind[6:]}"/>'
    fy = ph * 0.74
    if kind == "night-room":
        return (f'<defs><radialGradient id="lamp{uid}" cx="0.82" cy="0.28" r="0.5"><stop offset="0" stop-color="#FFD98A" stop-opacity="0.55"/><stop offset="1" stop-color="#FFD98A" stop-opacity="0"/></radialGradient></defs>'
                f'<rect width="{pw}" height="{ph}" fill="#2E3A59"/><rect x="{pw*0.08:.0f}" y="{ph*0.10:.0f}" width="{pw*0.26:.0f}" height="{ph*0.36:.0f}" fill="#141C33" stroke="#4C5A80" stroke-width="8"/>'
                f'<circle cx="{pw*0.25:.0f}" cy="{ph*0.20:.0f}" r="{ph*0.05:.0f}" fill="#F5F1D8"/><circle cx="{pw*0.13:.0f}" cy="{ph*0.36:.0f}" r="2.5" fill="#fff"/><circle cx="{pw*0.29:.0f}" cy="{ph*0.38:.0f}" r="2" fill="#fff"/>'
                f'<rect width="{pw}" height="{ph}" fill="url(#lamp{uid})"/><rect x="{pw*0.80:.0f}" y="{ph*0.18:.0f}" width="{pw*0.08:.0f}" height="{ph*0.10:.0f}" fill="#F2C063"/><rect x="{pw*0.835:.0f}" y="{ph*0.28:.0f}" width="6" height="{fy-ph*0.28:.0f}" fill="#555E7A"/>'
                f'<rect y="{fy:.0f}" width="{pw}" height="{ph-fy:.0f}" fill="#43395A"/>')
    if kind == "day-room":
        return (f'<rect width="{pw}" height="{ph}" fill="#F6EBDD"/><rect x="{pw*0.62:.0f}" y="{ph*0.10:.0f}" width="{pw*0.28:.0f}" height="{ph*0.36:.0f}" fill="#BDE3FF" stroke="#FFFFFF" stroke-width="10"/>'
                f'<circle cx="{pw*0.80:.0f}" cy="{ph*0.20:.0f}" r="{ph*0.05:.0f}" fill="#FFD166"/><rect y="{fy:.0f}" width="{pw}" height="{ph-fy:.0f}" fill="#D8B184"/>'
                + "".join(f'<path d="M 0 {fy+i*(ph-fy)/4:.0f} H {pw}" stroke="#C49A6C" stroke-width="2"/>' for i in range(1, 4)))
    if kind == "floor":
        return (f'<rect width="{pw}" height="{ph}" fill="#D8B184"/>' + "".join(f'<path d="M 0 {i*ph/6:.0f} H {pw}" stroke="#C49A6C" stroke-width="2"/>' for i in range(1, 6))
                + f'<rect width="{pw}" height="{ph*0.16:.0f}" fill="#F6EBDD"/><rect y="{ph*0.16:.0f}" width="{pw}" height="10" fill="#FFFFFF"/>')
    if kind == "board":
        dots = "".join(f'<circle cx="{x}" cy="{y}" r="2" fill="#C9DDD2"/>' for x in range(20, int(pw), 40) for y in range(20, int(ph), 40))
        return f'<rect width="{pw}" height="{ph}" fill="#EEF6F1"/>{dots}'
    if kind == "focus":
        return f'<rect width="{pw}" height="{ph}" fill="#FFFFFF"/>' + focus(pw, ph)
    if kind == "alarm":
        return f'<rect width="{pw}" height="{ph}" fill="#FFE3E0"/>' + focus(pw, ph, "#E63946", 40)
    return f'<rect width="{pw}" height="{ph}" fill="#F7F5F0"/>'

def item_svg(it, pw, ph, uid):
    t = it["t"]
    if t == "char": return C.person(it["who"], it.get("expr", "neutral"), it.get("pose", "rest"), it["x"], it["y"], it.get("s", 1.0), it.get("flip", False))
    if t == "chibi": return C.chibi(it["who"], it.get("expr", "shock"), it["x"], it["y"], it.get("s", 1.0), it.get("flip", False))
    if t == "dog": return C.dog(it["x"], it["y"], it.get("s", 1.0), it.get("mood", "calm"), it.get("flip", False))
    if t == "robot": return C.robot(it["x"], it["y"], it.get("s", 1.0), it.get("beams", False), it.get("view", "side"), it.get("flip", False), it.get("label"))
    if t == "cord": return C.cord(it["x"], it["y"], it.get("w", 300))
    if t == "sock": return C.sock(it["x"], it["y"], it.get("s", 1.0), it.get("color", "#E76F51"))
    if t == "phone": return C.phone(it["x"], it["y"], it.get("s", 1.0), it.get("title", ""), it.get("lines", []))
    if t == "say": return balloon(it, pw)
    if t == "narr": return narr(it)
    if t == "sfx": return sfx(it)
    if t == "card": return card(it)
    if t == "focus": return focus(pw, ph, it.get("color", INK))
    if t == "text":
        return text_block(wrap(it["text"], it.get("w", 600), it.get("size", 24), it.get("weight", 600) >= 700), it["x"], it["y"], it.get("size", 24), it.get("weight", 600), it.get("anchor", "middle"), it.get("color", INK))
    if t == "arrow":
        x, y, L = it["x"], it["y"], it.get("len", 90)
        return f'<path d="M {x} {y} V {y+L}" stroke="{it.get("color", "#1E8E5A")}" stroke-width="12" stroke-linecap="round"/><path d="M {x-30} {y+L-26} L {x} {y+L+8} L {x+30} {y+L-26}" stroke="{it.get("color", "#1E8E5A")}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    raise SystemExit(f"unknown item type {t}")

def title_card(spec, h=560):
    lines = wrap(spec["title"], 660, 50, True)
    out = [f'<rect width="{W}" height="{h}" fill="#1B2A41"/>',
           f'<rect x="40" y="40" width="{W-80}" height="{h-80}" fill="none" stroke="#2E4266" stroke-width="3"/>',
           f'<text x="{W/2}" y="110" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="800" letter-spacing="5" fill="#7FD1A8">{esc(spec.get("series", "VERDICT PICKS TOON").upper())}</text>',
           f'<text x="{W/2}" y="150" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="600" fill="#9FB0C8">{esc(spec.get("episode", ""))}</text>',
           text_block(lines, W / 2, 190, 50, 800, "middle", "#FFFFFF", 1.2)]
    sub = wrap(spec.get("subtitle", ""), 640, 26)
    out.append(text_block(sub, W / 2, 210 + len(lines) * 60, 26, 500, "middle", "#DDE6F2"))
    out.append(text_block(wrap(spec.get("note", "Characters and scenes are fictional. Every number in the comic comes from the guide below, with its source."), 640, 18), W / 2, h - 110, 18, 500, "middle", "#9FB0C8"))
    return "".join(out), h

def end_card(spec, h=None):
    credit = ("Art generated with Google Gemini (AI) from our script; story, lettering and facts by Verdict Picks. " if spec.get("ai_art") else "")
    lines = wrap(spec.get("end", "The full comparison is below."), 640, 30, True)
    ay = 70 + 39 * len(lines); h = h or ay + 70 + 110
    out = [f'<rect width="{W}" height="{h}" fill="#F7F5F0"/>',
           text_block(lines, W / 2, 40, 30, 800, "middle", INK),
           item_svg({"t": "arrow", "x": W / 2, "y": ay, "len": 40}, W, h, "end"),
           text_block(wrap(credit + "Verdict Picks Toon · characters and scenes are fictional; the facts are sourced in the guide below. Not sponsored by any brand shown or named.", 680, 17), W / 2, h - 100, 17, 500, "middle", "#666")]
    return "".join(out), h

def build(d, return_blocks=False):
    d = pathlib.Path(d); spec = json.loads((d / "webtoon.json").read_text(encoding="utf-8")); sid = spec["id"]
    blocks = []   # (gap_before, height, svg, [transcript lines])
    svg, h = title_card(spec); blocks.append((0, h, svg, [f'{spec.get("series", "Verdict Picks Toon")}: {spec["title"]}']))
    for i, p in enumerate(spec["panels"]):
        full = p.get("full", False); pw = W if full else W - 2 * MARGIN; px = 0 if full else MARGIN; uid = f"{sid}{i}"
        art = d / "toon-art" / f"{sid}-p{i+1:02d}.jpg" if "art" in p else None
        if art is not None:
            if not art.exists(): raise SystemExit(f"missing {art}: run scripts/toon_art.py {d} first")
            import subprocess
            aw, ah = [int(v) for v in subprocess.run(["identify", "-format", "%w %h", str(art)], capture_output=True, text=True, check=True).stdout.split()]   # real size after trimming
            ph = p.get("h", round(pw * ah / aw))
            import base64
            bg = (f'<image href="data:image/jpeg;base64,{base64.b64encode(art.read_bytes()).decode()}" x="0" y="{p.get("art_y", 0)}" width="{pw}" height="{round(pw * ah / aw)}" '
                  f'preserveAspectRatio="xMidYMid slice"/>')
        else:
            ph = p["h"]; bg = background(p.get("bg", "plain"), pw, ph, uid)
        inner = bg + "".join(item_svg(it, pw, ph, uid) for it in p.get("items", []))
        clip = f'<clipPath id="c{uid}"><rect width="{pw}" height="{ph}" rx="{0 if full else 6}"/></clipPath>' if p.get("clip", True) else ""
        body = f'<g clip-path="url(#c{uid})">{inner}</g>' if clip else inner
        border = f'<rect width="{pw}" height="{ph}" rx="6" fill="none" stroke="{INK}" stroke-width="4"/>' if p.get("border", not full) and p.get("bg", "plain") != "none" else ""
        over = "".join(item_svg(it, pw, ph, uid) for it in p.get("over", []))   # balloons that may cross the frame
        svg = f'<g transform="translate({px} 0)"><defs>{clip}</defs>{body}{border}{over}</g>'
        tr = []
        for it in p.get("items", []) + p.get("over", []):
            if it["t"] == "say": tr.append(f'{NAMES.get(it.get("who", ""), it.get("who", "?"))}: {it["text"]}')
            elif it["t"] == "narr": tr.append(f'Caption: {it["text"]}')
            elif it["t"] == "card": tr.append(f'Board, {it["title"]}: ' + "; ".join(" ".join(r[:2]) if isinstance(r, list) else r for r in it["rows"]))
            elif it["t"] == "phone": tr.append(f'Phone screen: {it.get("title", "")} ' + " ".join(it.get("lines", [])))
            elif it["t"] == "sfx": tr.append(f'(Sound: {it["text"]})')
            elif it["t"] == "text": tr.append(it["text"])
        blocks.append((p.get("gap", 60), ph, svg, tr))
    svg, h = end_card(spec); blocks.append((80, h, svg, [spec.get("end", "")]))
    if return_blocks: return spec, blocks
    # stack and slice: cut only in the middle of gaps, so no panel is split
    slices, cur, y = [], [], 0
    for gap, h, svg, tr in blocks:
        top_pad = gap // 2 if cur else 0
        if cur and y + gap + h > MAXH:
            slices.append((cur, y + gap - gap // 2)); cur, y = [], gap // 2
        else:
            y += gap if cur else top_pad
        cur.append((y, h, svg, tr)); y += h
    slices.append((cur, y + 40))
    out_dir = d / "images" / "toon"; out_dir.mkdir(parents=True, exist_ok=True)
    for f in out_dir.glob(f"{sid}-*.svg"): f.unlink()
    meta = {"id": sid, "title": spec["title"], "panels": len(spec["panels"]), "ai_art": bool(spec.get("ai_art")), "series": spec.get("series", "Verdict Picks Toon"), "slices": [], "transcript": []}
    for n, (parts, sh) in enumerate(slices, 1):
        body = "".join(f'<g transform="translate(0 {y})">{svg}</g>' for y, h, svg, tr in parts)
        alt_bits = [t for _, _, _, tr in parts for t in tr]
        alt = f'Comic, part {n} of {len(slices)}: ' + " ".join(alt_bits)
        doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {sh}" role="img" aria-label="{html.escape(alt)}">'
               f'<rect width="{W}" height="{sh}" fill="#FFFFFF"/>{body}</svg>')
        (out_dir / f"{sid}-{n}.svg").write_text(doc, encoding="utf-8")
        meta["slices"].append({"file": f"{sid}-{n}.png", "w": W, "h": sh, "alt": alt[:900]})
        meta["transcript"] += alt_bits
    (d / f"toon-{sid}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"webtoon {sid}: {len(spec['panels'])} panels -> {len(slices)} slices in {out_dir}")

def rasterize(d):
    """SVG slices -> 2x PNG (render_png.mjs) -> WebP q82 (about a quarter of the PNG); the PNGs are removed."""
    import subprocess
    d = pathlib.Path(d); td = d / "images" / "toon"; root = pathlib.Path(__file__).resolve().parent.parent
    subprocess.run(["node", str(root / "scripts" / "render_png.mjs"), str(td)], check=True, stdout=subprocess.DEVNULL)
    for png in sorted(td.glob("*.png")):
        subprocess.run(["convert", str(png), "-quality", "80", "-define", "webp:method=6", str(png.with_suffix(".webp"))], check=True)
        png.unlink()
    if json.loads((d / "webtoon.json").read_text(encoding="utf-8")).get("ai_art"):
        for f in td.glob("*.svg"): f.unlink()   # these embed the art as base64: rebuilt from webtoon.json + toon-art/, not kept
    meta = d / f"toon-{json.loads((d / 'webtoon.json').read_text(encoding='utf-8'))['id']}.json"
    m = json.loads(meta.read_text(encoding="utf-8"))
    for sl in m["slices"]: sl["file"] = sl["file"].replace(".png", ".webp")
    meta.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    kb = sum(f.stat().st_size for f in td.glob("*.webp")) // 1024
    print(f"webtoon images: {len(m['slices'])} WebP slices, {kb} KB")

if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    build(d)
    if "--svg-only" not in sys.argv: rasterize(d)
