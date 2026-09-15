"""Infographics for the dog-essentials guide.
Usage: python3 scripts/dog_infographics.py posts/<slug>   -> images/{fit,kong,retailers,bagmath}.svg (retailers/bagmath only when data is set below)
"""
import pathlib, sys
FONT = "-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
NAVY, GREEN, AMBER, PAPER, INK2 = "#1B2A41", "#1E8E5A", "#C9781B", "#F7F5F0", "#555"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def text(x, y, s, size=22, weight=400, fill=NAVY, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'
def check(x, y, c=GREEN):
    return f'<circle cx="{x}" cy="{y}" r="11" fill="{c}"/><path d="M {x-5} {y} l 4 4 l 7 -8" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
def warn(x, y, c=AMBER):
    return f'<path d="M {x} {y-12} l 12 21 h -24 z" fill="{c}"/><rect x="{x-1.3}" y="{y-5}" width="2.6" height="8" rx="1.3" fill="#fff"/><circle cx="{x}" cy="{y+6}" r="1.6" fill="#fff"/>'
def wrap(s, n):
    words, cur, rows = s.split(), "", []
    for w in words:
        if len(cur) + len(w) + 1 > n: rows.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    rows.append(cur); return rows
def head(W, H, label, title, sub):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}"><rect width="{W}" height="{H}" rx="18" fill="{PAPER}"/><g font-family="{FONT}">',
            text(40, 52, title, 30, 800), text(40, 84, sub, 20, 400, INK2)]

def dog(x, y, s=1.0, coat="#8B6B43", harness=NAVY, front_ring=True):
    """Side-view dog silhouette (spitz type) with a harness drawn on it; origin at the front paws."""
    g = [f'<g transform="translate({x} {y}) scale({s})">']
    # body, legs, tail, head, ears
    g.append(f'<path d="M 40 -120 Q 20 -190 90 -196 L 250 -196 Q 300 -196 300 -150 L 300 -120 Q 300 -90 270 -84 L 250 -84 L 250 -10 L 226 -10 L 226 -70 L 120 -70 L 120 -10 L 96 -10 L 96 -84 Q 40 -84 40 -120 Z" fill="{coat}"/>')
    g.append(f'<path d="M 296 -190 q 40 -40 20 -80 q -6 40 -34 60" fill="{coat}"/>')
    g.append(f'<path d="M 90 -196 Q 60 -250 10 -236 L -20 -216 Q -34 -206 -20 -196 L 40 -186 Q 60 -180 90 -196 Z" fill="{coat}"/>')
    g.append(f'<path d="M 34 -236 l -6 -40 l 30 26 z M 66 -230 l 6 -40 l 20 34 z" fill="{shade(coat)}"/>')
    g.append(f'<circle cx="8" cy="-224" r="4" fill="#222"/><circle cx="-18" cy="-206" r="5" fill="#222"/>')
    # harness: chest strap (front), girth strap (behind the front legs), back plate with ring
    g.append(f'<path d="M 92 -140 Q 60 -150 48 -170" fill="none" stroke="{harness}" stroke-width="12" stroke-linecap="round"/>')      # chest strap
    g.append(f'<path d="M 150 -196 L 150 -90" fill="none" stroke="{harness}" stroke-width="12" stroke-linecap="round"/>')             # girth strap
    g.append(f'<path d="M 100 -196 Q 130 -206 160 -196" fill="none" stroke="{harness}" stroke-width="14" stroke-linecap="round"/>')   # back plate
    g.append(f'<path d="M 92 -140 L 150 -150" fill="none" stroke="{harness}" stroke-width="10" stroke-linecap="round"/>')             # belly link
    g.append(f'<circle cx="132" cy="-208" r="8" fill="none" stroke="#B9BEC6" stroke-width="4"/>')
    if front_ring: g.append(f'<circle cx="86" cy="-142" r="7" fill="none" stroke="#B9BEC6" stroke-width="4"/>')
    g.append('</g>'); return "".join(g)

def shade(h):
    r, gg, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
    return "#%02x%02x%02x" % (max(0, r - 30), max(0, gg - 30), max(0, b - 30))

def fit():
    W, H = 1200, 620
    o = head(W, H, "How to fit a no-pull harness: two-finger rule, strap positions, front clip vs back clip", "Fit it once, properly", "The four checks that stop a spitz-type dog from backing out of a harness.")
    o.append(f'<rect x="40" y="108" width="560" height="470" rx="16" fill="#fff" stroke="#e3e1db"/>')
    o.append(dog(150, 520, 1.15, harness=NAVY))
    # callouts
    # number markers on the drawing: 1 chest strap, 2 back plate, 3 girth strap, 4 front ring
    for px, py, n in ((214, 336, 1), (288, 284, 2), (322, 350, 3), (272, 382, 4)):
        o.append(f'<circle cx="{px}" cy="{py}" r="15" fill="{GREEN}" stroke="#fff" stroke-width="3"/>' + text(px, py + 6, str(n), 16, 800, "#fff", "middle"))
    # right column: checks and the escape fix
    x = 640
    o.append(f'<rect x="{x}" y="108" width="520" height="470" rx="16" fill="#fff" stroke="#e3e1db"/>')
    o.append(text(x + 24, 150, "The four checks", 22, 800))
    items = [("Two fingers, not a fist", "If your hand slides under the girth strap, the dog can too. Snug enough to stay put, loose enough to breathe."),
             ("Straps off the armpits", "The girth strap should sit a hand's width behind the front legs. Rubbing means it is too far forward."),
             ("Front clip on days that pull", "The chest ring turns a lunge into a sideways step. Switch to the back ring once the dog walks nicely."),
             ("The escape test", "Spitz dogs (Jindos, huskies, shibas) back out of loose harnesses. Before the walk, hold the leash and step back: if the harness slides toward the ears, tighten the girth.")]
    y = 186
    for k, (t, d) in enumerate(items):
        o.append(check(x + 36, y - 6)); o.append(text(x + 58, y, t, 19, 700, NAVY))
        for j, r in enumerate(wrap(d, 52)): o.append(text(x + 58, y + 24 + j * 22, r, 16, 400, "#333"))
        y += 96
    o.append(text(40, 606, "Sizing: measure the widest part of the chest, then pick the size whose range puts that number in the middle, not at the edge.", 15, 400, "#777"))
    o.append("</g></svg>"); return "\n".join(o)

def kong():
    W, H = 1200, 560
    o = head(W, H, "How to stuff a KONG: four fillings from easy to expert, and how long each keeps a dog busy", "The KONG, from 3 minutes to 30", "Same toy, four difficulty levels. The freezer is the whole trick.")
    levels = [("Level 1", "Kibble only", "Dry kibble poured in; the dog tips it out.", "3–5 min", GREEN),
              ("Level 2", "Kibble + a smear", "Kibble sealed in with peanut butter (xylitol-free) or plain yogurt.", "10–15 min", GREEN),
              ("Level 3", "Layered and frozen", "Soaked kibble or wet food, a treat in the middle, frozen 2–3 hours on a plate.", "20–30 min", AMBER),
              ("Level 4", "The dinner KONG", "The whole meal goes in; two frozen KONGs replace the bowl on a rainy day.", "30 min+", NAVY)]
    for i, (lv, name, desc, mins, c) in enumerate(levels):
        x = 40 + i * 285
        o.append(f'<rect x="{x}" y="110" width="265" height="330" rx="16" fill="#fff" stroke="#e3e1db"/><rect x="{x}" y="110" width="265" height="12" rx="6" fill="{c}"/>')
        o.append(text(x + 20, 158, lv, 16, 800, c, extra='letter-spacing="2"'))
        o.append(text(x + 20, 190, name, 22, 800, NAVY))
        # a small KONG glyph filled to the level
        kx, ky = x + 212, 318
        o.append(f'<ellipse cx="{kx}" cy="{ky + 40}" rx="30" ry="24" fill="#C8102E"/><ellipse cx="{kx}" cy="{ky + 6}" rx="23" ry="19" fill="#C8102E"/><ellipse cx="{kx}" cy="{ky - 22}" rx="16" ry="13" fill="#C8102E"/>')
        fill_h = [14, 28, 46, 60][i]
        o.append(f'<clipPath id="k{i}"><ellipse cx="{kx}" cy="{ky + 40}" rx="30" ry="24"/><ellipse cx="{kx}" cy="{ky + 6}" rx="23" ry="19"/><ellipse cx="{kx}" cy="{ky - 22}" rx="16" ry="13"/></clipPath>')
        o.append(f'<rect x="{kx - 32}" y="{ky + 64 - fill_h}" width="64" height="{fill_h}" fill="#F4B942" opacity="0.9" clip-path="url(#k{i})"/>')
        for j, r in enumerate(wrap(desc, 27)): o.append(text(x + 20, 226 + j * 22, r, 16, 400, "#333"))
        o.append(f'<rect x="{x + 20}" y="396" width="150" height="34" rx="17" fill="{PAPER}" stroke="#e3e1db"/>' + text(x + 95, 419, f"Busy: {mins}", 15, 700, NAVY, "middle"))
    o.append(text(40, 480, "Rules: no xylitol (check peanut-butter labels), no cooked bones, size up for power chewers, and wash it in the top rack of the dishwasher.", 16, 700, NAVY))
    o.append(text(40, 508, "Times are typical for a food-motivated medium dog; a KONG that empties in a minute needs a harder level or a smaller opening (freeze it).", 15, 400, "#777"))
    o.append(text(40, 540, "Vets and trainers recommend feeding at least one meal a day from a puzzle; this is the cheapest puzzle there is.", 15, 400, "#777"))
    o.append("</g></svg>"); return "\n".join(o)

def retailers():
    W, H = 1200, 700
    o = head(W, H, "Where Amazon wins and loses for dog supplies in 2026: price, speed, returns, subscriptions, authenticity, compared with Chewy, Walmart, Petco and Temu",
             "Where Amazon wins, and where it doesn't", "Five things that decide where a dog owner should buy, scored from 2025–2026 policies and price studies.")
    cols = ["Amazon", "Chewy", "Walmart", "Petco / PetSmart", "Temu"]
    rows = [("Everyday price on brands", ["~6% below the field (Profitero 2025)", "~1% above Amazon", "~3% above; rollbacks can beat it", "list price, coupons", "no genuine brands — copies only"], [2, 1, 1, 0, -1]),
            ("Speed", ["same-day on $25+ with Prime", "1–3 days, $49 for free shipping", "1–3 days; $35 free", "same-day via DoorDash, $39–$49", "3–7 days \"local\", 7–15 from China"], [2, 1, 1, 1, -1]),
            ("Returns", ["30 days; food and meds excluded", "365 days, free, often \"keep it\"", "90 days (marketplace 30)", "60 days, in store", "90 days; one free label, then $7.99"], [0, 2, 1, 1, -1]),
            ("Re-order savings", ["Subscribe & Save 5%, 15% with 5+ items", "Autoship 35% first ($20 cap), then 5%", "subscription; discount status unclear", "Repeat Delivery 35% first, then 5%", "coupons and games"], [2, 1, 0, 1, -1]),
            ("Authenticity", ["check the \"Sold by\" line; 15M fakes seized in 2025", "first-party only", "first-party good; marketplace risky", "first-party, in store", "look-alike harnesses, KONGs, bags"], [1, 2, 0, 2, -1])]
    x0, y0, cw, rh = 40, 118, 200, 96
    o.append(f'<rect x="{x0}" y="{y0}" width="{W - 80}" height="{rh * len(rows) + 44}" rx="16" fill="#fff" stroke="#e3e1db"/>')
    o.append(f'<rect x="{x0}" y="{y0}" width="{W - 80}" height="44" rx="16" fill="{NAVY}"/><rect x="{x0}" y="{y0 + 22}" width="{W - 80}" height="22" fill="{NAVY}"/>')
    for i, c in enumerate(cols):
        o.append(text(x0 + 220 + i * 180 + 90, y0 + 29, c, 16, 800, "#fff", "middle"))
    for r, (name, cells, score) in enumerate(rows):
        y = y0 + 44 + r * rh
        if r % 2: o.append(f'<rect x="{x0}" y="{y}" width="{W - 80}" height="{rh}" fill="{PAPER}"/>')
        o.append(text(x0 + 16, y + 40, name, 17, 800, NAVY))
        for i, (cell, sc) in enumerate(zip(cells, score)):
            cx = x0 + 220 + i * 180 + 90
            colour = GREEN if sc == 2 else ("#5FAF84" if sc == 1 else ("#999" if sc == 0 else AMBER))
            glyph = "★★" if sc == 2 else ("★" if sc == 1 else ("–" if sc == 0 else "✕"))
            o.append(text(cx, y + 30, glyph, 16, 800, colour, "middle"))
            for k, ln in enumerate(wrap(cell, 24)[:3]): o.append(text(cx, y + 52 + k * 16, ln, 12.5, 400, "#333", "middle"))
    o.append(text(40, 662, "Sources: Profitero Price Wars 2025 (pet supplies, 23 retailers); retailer policy pages and Temu's returns policy, September 2026; Toy Association safety tests, December 2025.", 13, 400, "#777"))
    o.append(text(40, 684, "★★ best in class · ★ good · – neutral · ✕ weak. Temu carries no genuine Rabbitgoo, KONG, Earth Rated or Chuckit!. Prices move daily; the pattern is what matters.", 13, 400, "#777"))
    o.append("</g></svg>"); return "\n".join(o)

def bagmath():
    W, H = 1200, 460
    o = head(W, H, "Poop-bag math for one dog: about 730 bags a year; cost per year by brand", "Poop-bag math, one dog, one year", "Two bags a day, every day: about 60 a month, 730 a year. Here is what that costs per brand at the prices we found.")
    rows = [("Amazon Basics 900-count (Amazon only)", 1.5, "$11", GREEN), ("Earth Rated 270-count on Amazon, with Subscribe & Save", 3.3, "$24", GREEN),
            ("Pogi's 300 with handles (one-handed tying)", 4.8, "$35", AMBER), ("Earth Rated 270-count at Chewy ($14.99)", 5.4, "$39", AMBER), ("Pogi's compostable 270", 6.7, "$49", NAVY)]
    x0, y0, bw = 470, 120, 470
    for i, (name, cents, yr, c) in enumerate(rows):
        y = y0 + i * 58
        o.append(text(x0 - 16, y + 22, name, 15, 700, NAVY, "end"))
        w = bw * cents / 7.0
        o.append(f'<rect x="{x0}" y="{y}" width="{w}" height="34" rx="8" fill="{c}" opacity="0.9"/>')
        o.append(text(x0 + w + 12, y + 23, f"{cents:.1f}¢ a bag · about {yr} a year", 15, 700, NAVY))
    o.append(text(40, 420, "Per-bag prices from September 2026 listings and deal snippets; counts assume two bags a day, 365 days.", 13, 400, "#777"))
    o.append(text(40, 442, "Earth Rated won CNN Underscored's eight-brand 2026 test; Amazon Basics was the only other bag to survive its asphalt-scoop test.", 13, 400, "#777"))
    o.append("</g></svg>"); return "\n".join(o)

def main(post_dir):
    out = pathlib.Path(post_dir) / "images"; out.mkdir(parents=True, exist_ok=True)
    (out / "fit.svg").write_text(fit(), encoding="utf-8"); (out / "kong.svg").write_text(kong(), encoding="utf-8")
    (out / "retailers.svg").write_text(retailers(), encoding="utf-8"); (out / "bagmath.svg").write_text(bagmath(), encoding="utf-8")
    print("wrote fit, kong, retailers, bagmath")

if __name__ == "__main__":
    main(sys.argv[1])
