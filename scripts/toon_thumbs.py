#!/usr/bin/env python3
"""Thumbnails for the comic videos: dramatic Gemini key art (cast sheets attached) plus our own bold lettering.

  python3 scripts/toon_thumbs.py posts/<dir>          # Short cover, 1080x1920 -> shorts/thumbs/<ep>-cover.jpg (also the Short's first shot)
  python3 scripts/toon_thumbs.py shorts/season1.json  # long-form thumbnail, 1280x720 -> shorts/thumbs/season1.jpg
The spec is the "thumb" dict in posts/<dir>/youtube.json or in the season JSON:
  {"art": scene prompt, "cast": [...], "lines": ["BIG", "WORDS"], "accent": "#FFD23F", "badge": "EP.1"}
The model never draws the words (no-text rule); the lettering is SVG, so it is spelled right and on brand.
"""
import base64, html, json, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import toon_art as A

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "shorts" / "thumbs"

def art(key, spec, ratio):
    f = OUT / f"art-{key}.jpg"
    if f.exists(): return f
    OUT.mkdir(parents=True, exist_ok=True)
    cast = spec.get("cast", [])
    refs = [ROOT / "brand" / "toon-cast" / f"{c}.jpg" for c in cast if (ROOT / "brand" / "toon-cast" / f"{c}.jpg").exists()]
    p = ("Eye-catching YouTube thumbnail key art in professional Korean webtoon style: one single full-bleed image, bold saturated colors, dramatic lighting, "
         "strong rim light, exaggerated comic expressions, dynamic diagonal composition, high contrast, clean line art, cel shading. "
         + ("Characters: " + " ".join(A.CAST[c] for c in cast) + " " if cast else "") + "Scene: " + spec["art"] + A.NO_TEXT
         + (" The attached images are character model sheets: use them only for each character's face, hair, colors and outfit." if refs else ""))
    A.RATIO[ratio] = ratio
    png = A.gen(p, ratio, refs); tmp = f.with_suffix(".png"); tmp.write_bytes(png); A.trim(tmp)
    subprocess.run(["convert", str(tmp), "-quality", "92", str(f)], check=True); tmp.unlink()
    return f

def letter(bg, spec, W, H, out):
    lines = spec["lines"]; accent = spec.get("accent", "#FFD23F")
    portrait = H > W
    longest = max(len(l) for l in lines)
    size = int(min(W * (0.19 if portrait else 0.105), W * (0.86 if portrait else 0.52) / (0.66 * longest))); lh = size * 1.0
    size = int(size * spec.get("scale", 1.0))
    x = W * 0.06; y0 = H * spec.get("y", 0.10 if portrait else 0.17)
    anchor = "start"
    if spec.get("align") == "right": x = W * 0.94; anchor = "end"
    txt = "".join(
        f'<text x="{x}" y="{y0 + size + i * lh}" text-anchor="{anchor}" font-family="Inter,Arial Black,sans-serif" font-size="{size}" font-weight="900" '
        f'fill="{accent if i == len(lines) - 1 else "#FFFFFF"}" stroke="#0B1424" stroke-width="{size * 0.16:.0f}" stroke-linejoin="round" paint-order="stroke" '
        f'transform="rotate(-4 {x} {y0 + size + i * lh})">{html.escape(l)}</text>' for i, l in enumerate(lines))
    bs = int(W * (0.045 if portrait else 0.03))
    badge = (f'<rect x="{W*0.06}" y="{H - bs*2.6}" width="{bs * (len(spec.get("badge","")) * 0.62 + 1.6)}" height="{bs*1.6}" rx="{bs*0.3}" fill="#1E8E5A"/>'
             f'<text x="{W*0.06 + bs*0.8}" y="{H - bs*1.35}" font-family="Inter,sans-serif" font-size="{bs}" font-weight="900" fill="#FFFFFF">{html.escape(spec.get("badge",""))}</text>'
             f'<text x="{W*0.94}" y="{H - bs*1.35}" text-anchor="end" font-family="Inter,sans-serif" font-size="{bs*0.8}" font-weight="900" fill="#FFFFFF" stroke="#0B1424" stroke-width="{bs*0.12:.0f}" paint-order="stroke" letter-spacing="3">VERDICT PICKS TOON</text>')
    shade = (f'<defs><linearGradient id="s" x1="0" y1="0" x2="{0 if portrait else 1}" y2="{1 if portrait else 0}"><stop offset="0" stop-color="#0B1424" stop-opacity="0.55"/>'
             f'<stop offset="0.55" stop-color="#0B1424" stop-opacity="0"/></linearGradient><linearGradient id="b" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#0B1424" stop-opacity="0.6"/><stop offset="0.25" stop-color="#0B1424" stop-opacity="0"/></linearGradient></defs>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">{shade}'
           f'<image href="data:image/jpeg;base64,{base64.b64encode(bg.read_bytes()).decode()}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>'
           f'<rect width="{W}" height="{H}" fill="url(#s)"/><rect width="{W}" height="{H}" fill="url(#b)"/>{txt}{badge}</svg>')
    work = OUT / "work"; work.mkdir(exist_ok=True)
    for f in work.glob("*"): f.unlink()
    (work / "t.svg").write_text(svg, encoding="utf-8")
    subprocess.run(["node", str(ROOT / "scripts" / "render_png.mjs"), str(work)], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["convert", str(work / "t.png"), "-resize", f"{W}x{H}", "-quality", "90", str(out)], check=True)
    for f in work.glob("*"): f.unlink()
    work.rmdir()
    print("thumb", out.relative_to(ROOT), f"{out.stat().st_size // 1024} KB")

def main(target):
    p = ROOT / target
    if p.is_dir():
        yt = json.loads((p / "youtube.json").read_text(encoding="utf-8")); sid = json.loads((p / "webtoon.json").read_text(encoding="utf-8"))["id"]
        letter(art(f"{sid}-cover", yt["thumb"], "9:16"), yt["thumb"], 1080, 1920, OUT / f"{sid}-cover.jpg")
    else:
        cfg = json.loads(p.read_text(encoding="utf-8"))
        letter(art(cfg["id"], cfg["thumb"], "16:9"), cfg["thumb"], 1280, 720, OUT / f"{cfg['id']}.jpg")

if __name__ == "__main__":
    for t in sys.argv[1:]: main(t)
