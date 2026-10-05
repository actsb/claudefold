"""Generic infographics for the product-of-the-day posts, driven by posts/<dir>/infographics.json (a list of specs).
  {"type": "steps",  "name": "howto",  "title": "...", "sub": "...", "footer": "...", "items": [{"head": "...", "body": "..."} x 4–6]}
  {"type": "stores", "name": "stores", "title": "...", "sub": "...", "footer": "...", "rows": [{"store", "price", "ship", "returns", "note", "verdict": "win|ok|no"}]}
Usage: python3 scripts/daily_infographic.py posts/<dir>   → images/<name>.svg for each spec
"""
import json, pathlib, sys
FONT = "-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
NAVY, GREEN, AMBER, PAPER, INK2, RED = "#1B2A41", "#1E8E5A", "#C9781B", "#F7F5F0", "#555", "#C8102E"

def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def text(x, y, s, size=22, weight=400, fill=NAVY, anchor="start"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>'
def wrap(s, n):
    words, cur, rows = str(s).split(), "", []
    for w in words:
        if len(cur) + len(w) + 1 > n: rows.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    rows.append(cur); return rows
def para(x, y, s, n, size=15, lh=20, fill="#333"):
    return "".join(text(x, y + i * lh, r, size, 400, fill) for i, r in enumerate(wrap(s, n)))
def tile(x, y, w, h, fill="#fff", stroke="#E3E1DB"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}"/>'
def mark(x, y, kind):
    if kind == "win":
        return f'<circle cx="{x}" cy="{y}" r="12" fill="{GREEN}"/><path d="M {x-5} {y} l 4 4 l 7 -8" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
    if kind == "no":
        return f'<circle cx="{x}" cy="{y}" r="12" fill="{RED}"/><path d="M {x-4.5} {y-4.5} l 9 9 M {x+4.5} {y-4.5} l -9 9" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>'
    return f'<circle cx="{x}" cy="{y}" r="12" fill="{AMBER}"/><rect x="{x-6}" y="{y-1.5}" width="12" height="3" rx="1.5" fill="#fff"/>'
def frame(W, H, spec):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(spec["title"])}"><rect width="{W}" height="{H}" rx="18" fill="{PAPER}"/><g font-family="{FONT}">',
            text(40, 52, spec["title"], 30, 800), text(40, 84, spec.get("sub", ""), 20, 400, INK2)]
def close(W, H, spec):
    return [text(40, H - 22, spec.get("footer", ""), 13, 400, "#888"), "</g></svg>"]

def steps(spec):
    items = spec["items"][:6]; cols = 3 if len(items) > 4 else 2; rows = (len(items) + cols - 1) // cols
    W = 1200; tw = (W - 80 - (cols - 1) * 20) / cols; th = 176; H = 112 + rows * (th + 18) + 40
    o = frame(W, H, spec)
    for i, it in enumerate(items):
        c, r = i % cols, i // cols; x = 40 + c * (tw + 20); y = 112 + r * (th + 18)
        o.append(tile(x, y, tw, th))
        o.append(f'<circle cx="{x+34}" cy="{y+34}" r="20" fill="{NAVY}"/>' + text(x + 34, y + 41, str(i + 1), 20, 800, "#fff", "middle"))
        o.append(text(x + 64, y + 40, it["head"], 19, 800))
        o.append(para(x + 20, y + 76, it["body"], int(tw / 8.6), 15, 20))
    return "\n".join(o + close(W, H, spec))

def stores(spec):
    rows = spec["rows"]; W = 1200; H = 170 + len(rows) * 62 + 40
    o = frame(W, H, spec)
    y = 116; o.append(f'<rect x="40" y="{y}" width="1120" height="40" rx="10" fill="{NAVY}"/>')
    for x, t in ((60, "Store"), (300, "Price seen"), (500, "Delivery"), (700, "Returns"), (880, "Note")): o.append(text(x, y + 26, t, 15, 700, "#fff"))
    for i, r in enumerate(rows):
        yy = y + 52 + i * 62
        o.append(f'<rect x="40" y="{yy}" width="1120" height="52" rx="10" fill="#fff" stroke="#E3E1DB"/>')
        o.append(mark(66, yy + 26, r.get("verdict", "ok"))); o.append(text(88, yy + 32, r["store"], 17, 700))
        o.append(text(300, yy + 32, r.get("price", ""), 16, 400, "#333")); o.append(text(500, yy + 32, r.get("ship", ""), 15, 400, "#333"))
        o.append(text(700, yy + 32, r.get("returns", ""), 15, 400, "#333")); o.append(para(880, yy + 24, r.get("note", ""), 34, 13, 15, "#444"))
    return "\n".join(o + close(W, H, spec))

def matrix(spec):
    """A comparison table: spec["columns"] = [{"head", "w"}...] (relative widths; the first column is the row label),
    spec["rows"] = [{"cells": [...], "verdict": "win|ok|no" (optional)}]. Cells and the footer wrap to fit."""
    cols = spec["columns"]; W = 1200
    widths = [c["w"] for c in cols]; scale = (W - 80) / sum(widths); widths = [w * scale for w in widths]
    label_chars = max(8, int((widths[0] - 46) / 9.4))                     # bold 16 px label
    cell_chars = [max(8, int((w - 24) / 7.9)) for w in widths]            # regular 14.5 px cells
    def n_lines(i, txt): return len(wrap(txt, label_chars if i == 0 else cell_chars[i]))
    row_h = [max(52, 24 + 19 * max(n_lines(i, c) for i, c in enumerate(r["cells"]))) for r in spec["rows"]]
    foot = wrap(spec.get("footer", ""), 150)
    H = 168 + sum(h + 10 for h in row_h) + 16 + 17 * len(foot) + 14
    o = frame(W, H, spec)
    y = 116; o.append(f'<rect x="40" y="{y}" width="1120" height="40" rx="10" fill="{NAVY}"/>')
    x = 40
    for i, c in enumerate(cols):
        o.append(text(x + (34 if i == 0 else 12), y + 26, c["head"], 15, 700, "#fff")); x += widths[i]
    yy = y + 52
    for r, h in zip(spec["rows"], row_h):
        o.append(f'<rect x="40" y="{yy}" width="1120" height="{h}" rx="10" fill="#fff" stroke="#E3E1DB"/>')
        x = 40
        for i, cell in enumerate(r["cells"]):
            if i == 0:
                if r.get("verdict"): o.append(mark(60, yy + 26, r["verdict"]))
                o.append("".join(text(x + 34, yy + 30 + k * 19, ln, 16, 700, NAVY) for k, ln in enumerate(wrap(cell, label_chars))))
            else:
                o.append(para(x + 12, yy + 28, cell, cell_chars[i], 14.5, 19, "#333"))
            x += widths[i]
        yy += h + 10
    o.append("".join(text(40, yy + 14 + k * 17, ln, 13, 400, "#888") for k, ln in enumerate(foot)))
    o.append("</g></svg>")
    return "\n".join(o)

def main(post_dir):
    d = pathlib.Path(post_dir); specs = json.loads((d / "infographics.json").read_text(encoding="utf-8"))
    for spec in specs:
        svg = {"steps": steps, "stores": stores, "matrix": matrix}[spec["type"]](spec)
        (d / "images" / f"{spec['name']}.svg").write_text(svg, encoding="utf-8")
    print("wrote", ", ".join(s["name"] for s in specs), "->", d / "images")

if __name__ == "__main__":
    main(sys.argv[1])
