#!/usr/bin/env python3
"""Real product photos instead of drawn renders (daily/README.md section 0, "Images"; daily/image-plan-2026-10-23.md).

A card in cards.json may carry a photo we are allowed to publish:
  "photo": {"file": "brand/photos/<slug>.jpg",          # the shared library (repo path), or images/photos/<id>.jpg in the post
            "kind": "own" | "brand",                      # our own photo, or the maker's press/media-kit photo
            "credit": "Instant Brands press kit",         # shown on the picture and in the post's image credits
            "source": "https://…",                        # the page the file came from (brand only)
            "terms": "https://…",                         # the page whose terms allow editorial use (brand only)
            "uses": ["web"] | ["web", "social"],          # social = covers and Pinterest pins (own photos: always)
            "checked": "2026-10-23"}
Amazon product images are never downloaded, stored, cropped or hosted here (Associates Program Policies, IP License 2(h)
and Participation Requirement 6(a)); once the Creators API opens they may be shown only as live API links (the plan's
phase 2). When a product has no allowed photo, it gets a plain name tile, not a drawing pretending to be the product.

  python3 scripts/product_photos.py posts/<dir>     # shrink photos to 1400 px, strip metadata, report what is missing
"""
import html, json, pathlib, sys

PAGES = "https://actsb.github.io/claudefold/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
NAVY = "#1B2A41"
FONT = "-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"


def esc(s):
    return html.escape(str(s), quote=True)


def path(d, p):
    """A photo file: repo-relative when it starts with brand/ (the shared library), else inside the post folder."""
    return ROOT / p["file"] if p["file"].startswith("brand/") else pathlib.Path(d) / p["file"]


def photo(d, c, use="web"):
    """The card's photo dict when the file exists and the use is allowed, else None."""
    p = c.get("photo")
    if not isinstance(p, dict) or not p.get("file"):
        return None
    if not path(d, p).exists():
        return None
    if p.get("kind") == "own":
        return p
    if p.get("kind") == "brand" and use in p.get("uses", []) and p.get("credit") and p.get("terms"):
        return p
    return None


def url(d, p):
    return PAGES + path(d, p).resolve().relative_to(ROOT).as_posix()


def credit_text(p):
    return "Our photo" if p.get("kind") == "own" else f"Photo: {p['credit']}"


def card_svg(d, c, chip_w, chip, short):
    """The 600x400 card picture with the photo contained (never cropped), the chip and name, and the credit."""
    p = photo(d, c)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 400" role="img" aria-label="{esc(c["name"])} ({esc(credit_text(p).lower())})">
<rect width="600" height="400" rx="18" fill="#ffffff"/>
<image href="{esc(url(d, p))}" x="40" y="54" width="520" height="300" preserveAspectRatio="xMidYMid meet"/>
<g font-family="{FONT}">
<rect x="18" y="18" width="{chip_w}" height="28" rx="14" fill="{NAVY}"/>
<text x="{18 + chip_w/2}" y="37" text-anchor="middle" font-size="13" font-weight="700" fill="#fff">{esc(chip)}</text>
<text x="22" y="380" font-size="22" font-weight="700" fill="{NAVY}">{esc(short)}</text>
<text x="578" y="382" text-anchor="end" font-size="11" fill="#8a8a8a">{esc(credit_text(p))}</text>
</g>
</svg>
'''


def tile(uid, label):
    """No allowed photo yet: a plain tile with the product's name (600x400 coordinates), never a pretend product."""
    words, lines, cur = str(label).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > 18 and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    lines = lines[:3]
    y0 = 200 - (len(lines) - 1) * 26
    text = "".join(f'<text x="300" y="{y0 + i * 52}" text-anchor="middle" font-size="40" font-weight="800" fill="{NAVY}">{esc(l)}</text>' for i, l in enumerate(lines))
    return (f'<rect x="60" y="60" width="480" height="280" rx="28" fill="#F4F2EC"/>'
            f'<rect x="60" y="60" width="480" height="280" rx="28" fill="none" stroke="#E3E1DB" stroke-width="2"/>'
            f'<g font-family="{FONT}">{text}</g>')


def image_credits(d, cards):
    """The line for the post's footer: every brand photo's credit, linked to its source."""
    seen, out = set(), []
    for c in cards:
        p = photo(d, c)
        if p and p.get("kind") == "brand" and p["credit"] not in seen:
            seen.add(p["credit"])
            out.append(f'<a href="{esc(p.get("source") or p["terms"])}" rel="nofollow noopener" target="_blank">{esc(p["credit"])}</a>')
    return ("Image credits: product photos from " + ", ".join(out) + ", used under their press terms.") if out else ""


def main(post_dir):
    """Shrink every photo to at most 1400 px on its long side and drop its metadata; list cards without an allowed photo."""
    from PIL import Image
    d = pathlib.Path(post_dir)
    spec = json.loads((d / "cards.json").read_text(encoding="utf-8"))
    cards, renamed = spec["cards"], False
    for c in cards:
        p = c.get("photo")
        f = path(d, p) if isinstance(p, dict) and p.get("file") else None
        if f and f.exists():
            im = Image.open(f); im.load()
            if max(im.size) > 1400 or im.info.get("exif") or f.suffix.lower() not in (".jpg", ".jpeg"):
                im = im.convert("RGB"); im.thumbnail((1400, 1400))
                out = f.with_suffix(".jpg"); im.save(out, "JPEG", quality=85, optimize=True)
                if out != f:
                    f.unlink(); p["file"] = (out.relative_to(ROOT) if p["file"].startswith("brand/") else out.relative_to(d)).as_posix(); renamed = True
        status = "ok" if photo(d, c) else ("photo listed but not usable (file, credit, terms or uses missing)" if p else "no photo: name tile")
        print(f"  {c['id']}: {status}")
    if renamed:
        (d / "cards.json").write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
