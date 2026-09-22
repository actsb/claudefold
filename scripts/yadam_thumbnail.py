"""YouTube thumbnail (1280x720) for the yadam video, built the way the high-click yadam/senior channels do it:
dark high-contrast backdrop, two big faces (surprised mouth), 2-3 lines of very large yellow/white text with
thick black stroke, one red keyword box, a corner badge. Everything is drawn from the generated assets.
Usage: python3 scripts/yadam_thumbnail.py video/2026-09-yadam-manbok [--variant a|b] [--out thumbnail.png]
"""
import argparse, json, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

FONT = "/usr/share/fonts/truetype/nanum/NanumSquareRoundB.ttf"       # very bold rounded gothic (readable when tiny)
FONT_B = "/usr/share/fonts/truetype/nanum/NanumSquareB.ttf"
W, H = 1280, 720


def face_crop(assets, man, name, mouth="open", height=520, flip=False):
    """Head-and-shoulders crop of a character sprite, mouth open = surprise."""
    p = man["char"][name]["poses"]["stand"]["states"][f"{mouth}_open"]
    im = Image.open(assets / p).convert("RGBA")
    im = im.crop((60, 0, im.width - 60, int(im.height * 0.52)))          # head + shoulders
    s = height / im.height; im = im.resize((int(im.width * s), int(height)), Image.LANCZOS)
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    return im


def text_block(d, lines, x, y, size, colors, stroke=10, gap=8):
    f = ImageFont.truetype(FONT, size)
    for ln, col in zip(lines, colors):
        d.text((x, y), ln, font=f, fill=col, stroke_width=stroke, stroke_fill=(10, 8, 6))
        y += size + gap
    return y


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--variant", default="a"); ap.add_argument("--out", default="thumbnail.png")
    a = ap.parse_args()
    root = pathlib.Path(a.root); assets = root / "assets"; man = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))

    # backdrop: market scene, darkened and slightly blurred so the faces and text pop
    bg = Image.open(assets / man["bg"]["market" if a.variant == "a" else "village_night"]["file"]).convert("RGB")
    bw, bh = bg.size; cw = int(bw * 0.7); ch = int(cw * H / W)
    bg = bg.crop(((bw - cw) // 2, bh - ch - int(bh * 0.05), (bw + cw) // 2, bh - int(bh * 0.05))).resize((W, H), Image.LANCZOS)
    bg = ImageEnhance.Brightness(bg).enhance(0.55).filter(ImageFilter.GaussianBlur(2))
    # left-side dark gradient for the text
    grad = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(grad)
    for x in range(W):
        gd.line([(x, 0), (x, H)], fill=int(190 * max(0.0, 1 - x / (W * 0.66))))
    bg = Image.composite(Image.new("RGB", (W, H), (12, 8, 6)), bg, grad)

    # faces: Sunok (worried) and Manbok (surprised), big, with a soft shadow
    for name, x, hgt, flip in (("sunok", 1060, 560, True), ("manbok", 830, 620, False)):
        im = face_crop(assets, man, name, mouth="open" if name == "manbok" else "closed", height=hgt, flip=flip)
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 150), (0, 0), im); sh = sh.filter(ImageFilter.GaussianBlur(14))
        bg.paste(sh, (int(x - im.width / 2) + 10, H - hgt + 20), sh)
        bg.paste(im, (int(x - im.width / 2), H - hgt + 6), im)

    d = ImageDraw.Draw(bg)
    if a.variant == "a":
        y = text_block(d, ["전 재산 서른 냥에", "과부를 샀다"], 48, 70, 118, [(255, 255, 255), (255, 232, 70)])
        # red keyword box
        f = ImageFont.truetype(FONT, 66); txt = "십 년 뒤, 마을이 뒤집혔다"
        tw = d.textlength(txt, font=f); d.rounded_rectangle([48, y + 18, 48 + tw + 44, y + 18 + 92], radius=16, fill=(200, 30, 30))
        d.text((70, y + 26), txt, font=f, fill=(255, 255, 255), stroke_width=4, stroke_fill=(90, 0, 0))
    else:
        y = text_block(d, ["바보라 불린 머슴이", "암행어사를", "집에 재웠다"], 48, 40, 108, [(255, 255, 255), (255, 232, 70), (255, 255, 255)])
        f = ImageFont.truetype(FONT, 60); txt = "조선 야담 · 반전 실화"
        tw = d.textlength(txt, font=f); d.rounded_rectangle([48, y + 14, 48 + tw + 44, y + 14 + 84], radius=16, fill=(200, 30, 30))
        d.text((70, y + 22), txt, font=f, fill=(255, 255, 255), stroke_width=4, stroke_fill=(90, 0, 0))
    # corner badge: runtime
    f2 = ImageFont.truetype(FONT_B, 44); badge = "55분 몰입 야담"
    bw2 = d.textlength(badge, font=f2)
    d.rounded_rectangle([W - bw2 - 74, 28, W - 28, 28 + 70], radius=14, fill=(255, 232, 70))
    d.text((W - bw2 - 52, 38), badge, font=f2, fill=(30, 20, 10))
    out = root / a.out; bg.save(out, quality=92); print("wrote", out)


if __name__ == "__main__":
    main()
