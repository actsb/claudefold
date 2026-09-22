"""YouTube thumbnail (1280x720) for the yadam video: background + two character sprites + big high-contrast Korean text.
Usage: python3 scripts/yadam_thumbnail.py video/2026-09-yadam-manbok [--bg market] [--text "전 재산 서른 냥으로|과부를 샀다"] [--out thumbnail.png]
"""
import argparse, json, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/usr/share/fonts/truetype/nanum/NanumSquareRoundB.ttf"
FONT2 = "/usr/share/fonts/truetype/nanum/NanumMyeongjoBold.ttf"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--bg", default="market")
    ap.add_argument("--text", default="전 재산 서른 냥으로|과부를 샀다"); ap.add_argument("--tag", default="바보 머슴 만복이 · 야담 1시간")
    ap.add_argument("--out", default="thumbnail.png"); a = ap.parse_args()
    root = pathlib.Path(a.root); assets = root / "assets"; man = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    W, H = 1280, 720
    bg = Image.open(assets / man["bg"][a.bg]["file"]).convert("RGB")
    # crop the lower-middle of the world so the ground is near the bottom
    bw, bh = bg.size; cw, ch = int(bw * 0.78), int(bw * 0.78 * H / W)
    bg = bg.crop(((bw - cw) // 2, bh - ch - int(bh * 0.04), (bw + cw) // 2, bh - int(bh * 0.04))).resize((W, H), Image.LANCZOS)
    # darken left half for text legibility
    grad = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(grad)
    for x in range(W):
        gd.line([(x, 0), (x, H)], fill=int(150 * max(0.0, 1 - x / (W * 0.62))))
    bg = Image.composite(Image.new("RGB", (W, H), (20, 12, 8)), bg, grad)

    def sprite(name, x, height, flip=False):
        p = man["char"][name]["poses"]["stand"]["states"]["closed_open"]
        im = Image.open(assets / p).convert("RGBA")
        s = height / im.height; im = im.resize((int(im.width * s), int(height)), Image.LANCZOS)
        if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 120), (0, 0), im); sh = sh.filter(ImageFilter.GaussianBlur(10))
        bg.paste(sh, (int(x - im.width / 2) + 8, H - int(height) + 14), sh)
        bg.paste(im, (int(x - im.width / 2), H - int(height) + 4), im)
    sprite("sunok", 1010, 640, flip=True); sprite("manbok", 800, 690)

    d = ImageDraw.Draw(bg)
    lines = a.text.split("|"); f = ImageFont.truetype(FONT, 108); y = 120
    for i, ln in enumerate(lines):
        fill = (255, 240, 120) if i == len(lines) - 1 else (255, 255, 255)
        d.text((56, y), ln, font=f, fill=fill, stroke_width=9, stroke_fill=(20, 10, 5)); y += 128
    f2 = ImageFont.truetype(FONT2, 44)
    d.rounded_rectangle([56, H - 118, 56 + d.textlength(a.tag, font=f2) + 44, H - 52], radius=14, fill=(150, 40, 30))
    d.text((78, H - 110), a.tag, font=f2, fill=(255, 250, 240))
    out = root / a.out; bg.save(out, quality=92); print("wrote", out)


if __name__ == "__main__":
    main()
