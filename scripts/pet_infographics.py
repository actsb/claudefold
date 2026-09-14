"""Infographics for the pet best-sellers guide: tiers, cost-per-year, owner voices, buying on Amazon.
Usage: python3 scripts/pet_infographics.py posts/<slug>   -> images/{tiers,cost,voices,amazon}.svg
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

def tiers():
    W, H = 1200, 560
    cols = [("GOOD", "$25", "ChomChom Roller", ["Solves: fur on the couch, the car seat, the duvet", "For: every home with a shedding pet", "Runs on: nothing — no refills, no batteries"], GREEN),
            ("BETTER", "$85", "Neakasa P1 Pro grooming kit", ["Solves: fur before it leaves the dog (or cat)", "For: weekly brushers, double coats, multi-pet homes", "Runs on: a wall outlet; filters and blades wear"], AMBER),
            ("BEST", "$699", "Whisker Litter-Robot 4", ["Solves: scooping, odor, the sitter problem", "For: 1–4 cats, travellers, scoop-haters", "Runs on: liners and filters, about $50–$120 a year"], NAVY)]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Three tiers of pet product: Good $25 ChomChom Roller, Better $85 Neakasa P1 Pro, Best $699 Litter-Robot 4"><rect width="{W}" height="{H}" rx="18" fill="{PAPER}"/><g font-family="{FONT}">',
         text(40, 52, "Three prices, three jobs", 30, 800), text(40, 84, "Buy the tier that matches the problem, not the one that matches the budget.", 20, 400, INK2)]
    for i, (tier, price, name, lines, c) in enumerate(cols):
        x = 40 + i * 380
        o.append(f'<rect x="{x}" y="110" width="360" height="400" rx="16" fill="#fff" stroke="#e3e1db"/><rect x="{x}" y="110" width="360" height="12" rx="6" fill="{c}"/>')
        o.append(text(x + 24, 168, tier, 18, 800, c, extra='letter-spacing="2"'))
        o.append(text(x + 24, 236, price, 60, 800, NAVY))
        o.append(text(x + 24, 276, name, 22, 700, NAVY))
        for j, ln in enumerate(lines):
            # wrap at ~34 chars
            words, cur, rows = ln.split(), "", []
            for w in words:
                if len(cur) + len(w) + 1 > 34: rows.append(cur); cur = w
                else: cur = (cur + " " + w).strip()
            rows.append(cur)
            y = 318 + j * 62
            o.append(check(x + 34, y - 6, c))
            for k, r in enumerate(rows): o.append(text(x + 56, y + k * 24, r, 18, 400, "#222"))
    o.append(text(40, 540, "Prices: 2026 US sale prices at the time of writing. Everyday prices sit higher; deal days sit lower.", 15, 400, "#777"))
    o.append("</g></svg>")
    return "\n".join(o)

def cost():
    W, H = 1200, 400
    rows = [("ChomChom Roller", 0, 0, "$0 — nothing to buy, ever", None),
            ("Neakasa P1 Pro", 20, 40, "about $20–$40 — filters and clipper blades (our estimate)", None),
            ("Litter-Robot 4", 50, 120, "$50–$120 typical — liners and carbon filters", 360)]
    x0, x1, maxv = 300, 1120, 400
    sx = lambda v: x0 + (x1 - x0) * v / maxv
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Yearly running cost: ChomChom $0, Neakasa P1 Pro about $20 to $40, Litter-Robot 4 $50 to $120 typical, up to about $360 with OdorTrap packs"><rect width="{W}" height="{H}" rx="18" fill="{PAPER}"/><g font-family="{FONT}">',
         text(40, 52, "What each one costs to run, per year", 30, 800), text(40, 84, "After the box arrives. Consumables only; electricity is pennies.", 20, 400, INK2)]
    for v in (0, 100, 200, 300, 400):
        x = sx(v); o.append(f'<path d="M {x} 120 V 320" stroke="#e3e1db" stroke-width="1"/>'); o.append(text(x, 344, f"${v}", 15, 400, "#777", "middle"))
    for i, (name, lo, hi, label, ext) in enumerate(rows):
        y = 150 + i * 62
        o.append(text(280, y + 8, name, 20, 700, NAVY, "end"))
        if ext: o.append(f'<rect x="{sx(hi)}" y="{y-11}" width="{sx(ext)-sx(hi)}" height="22" rx="0" fill="{GREEN}" opacity="0.22"/>')
        if hi == 0: o.append(f'<circle cx="{sx(0)}" cy="{y}" r="9" fill="{GREEN}"/>')
        else: o.append(f'<rect x="{sx(lo)}" y="{y-11}" width="{max(sx(hi)-sx(lo), 8)}" height="22" rx="4" fill="{GREEN}"/>')
        o.append(text(sx(hi if hi else 0) + 18, y + 7, label, 17, 400, "#222"))
    o.append(text(sx(360) - 4, 150 + 2 * 62 + 34, "up to ~$360 if you run OdorTrap packs nonstop", 14, 400, "#777", "end"))
    o.append(text(40, 380, "Sources: Whisker consumable prices and owner cost breakdowns (Petful, Reviewed); Neakasa parts listings. Ranges, not quotes.", 14, 400, "#777"))
    o.append("</g></svg>")
    return "\n".join(o)

def voices():
    W, H = 1200, 700
    rows = [("ChomChom Roller", "190,000+ ratings · 4.5★ (reported)",
             ["A cushion cleared in about 30 seconds", "No refills, no batteries, no cord", "Works on fine cat hair and coarse dog hair"],
             ["A week to learn the short 45° stroke", "Needs taut fabric; useless on carpet pile", "Door button sits right under your thumb"]),
            ("Neakasa P1 Pro", "Dogster 4.9/5 · brand site 4.8/5",
             ["Fur goes straight into the bin", "Quiet enough for vacuum-shy dogs (52 dB eco)", "Pays for itself in a groomer visit or two"],
             ["1-liter cup fills fast on big shedders", "Clipper trims; it does not shave", "Suction fades if the filter clogs"]),
            ("Litter-Robot 4", "7,000+ verified reviews · 4.4/5 (Whisker)",
             ["Sealed drawer keeps the odor in", "Truly hands-off; scoop once a week", "App caught a cat's UTI early (reviewer)"],
             ["$699 hurts", "False 'drawer full' until you wipe the sensors", "OdorTrap refills add up"])]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="What owners praise and complain about for each of the three products"><rect width="{W}" height="{H}" rx="18" fill="{PAPER}"/><g font-family="{FONT}">',
         text(40, 52, "What the owners keep saying", 30, 800), text(40, 84, "The recurring themes across the reviews and the expert tests we read — not our own lab.", 20, 400, INK2),
         text(330, 134, "PRAISE", 16, 800, GREEN, extra='letter-spacing="2"'), text(760, 134, "COMPLAINTS", 16, 800, AMBER, extra='letter-spacing="2"')]
    for i, (name, meta, pros, cons) in enumerate(rows):
        y = 160 + i * 176
        o.append(f'<rect x="40" y="{y}" width="1120" height="156" rx="14" fill="#fff" stroke="#e3e1db"/>')
        o.append(text(64, y + 44, name, 22, 800, NAVY))
        for k, part in enumerate(meta.split(" · ")): o.append(text(64, y + 72 + k * 22, part, 14, 400, "#777"))
        for k, ln in enumerate(pros): o.append(check(330 + 12, y + 40 + k * 40 - 6)); o.append(text(360, y + 40 + k * 40, ln, 17, 400, "#222"))
        for k, ln in enumerate(cons): o.append(warn(760 + 12, y + 40 + k * 40 - 4)); o.append(text(790, y + 40 + k * 40, ln, 17, 400, "#222"))
    o.append("</g></svg>")
    return "\n".join(o)

def amazon():
    W, H = 1200, 620
    panels = [("Delivery", GREEN, ["Prime: same- or next-day on most of these in most", "US cities; same-day is free over $25", "Prime is $14.99/mo or $139/yr; 30-day free trial"]),
              ("Returns", NAVY, ["30 days from delivery for these three", "Pet food and litter-type consumables: mostly", "non-returnable unless damaged", "Label-free drop-off at 10,000+ locations"]),
              ("Subscribe & Save", AMBER, ["5% off every delivery; up to 15% with five or", "more subscriptions on one delivery day", "Food, litter, liners and filters qualify —", "the roller and the vacuum don't need it"]),
              ("Spot the real one", "#3C8DAD", ["Read both lines: 'Ships from' and 'Sold by'", "ChomChom: look for the Transparency code", "'#1 Best Seller' = top sales rank, updated hourly", "'Frequently returned item' is a warning, read it"])]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="What buying pet supplies on Amazon gets you: delivery, returns, Subscribe and Save, and how to spot the real listing"><rect width="{W}" height="{H}" rx="18" fill="{PAPER}"/><g font-family="{FONT}">',
         text(40, 52, "What buying on Amazon actually gets you", 30, 800), text(40, 84, "The parts that matter for pet gear, from Amazon's own policy pages and 2025–2026 announcements.", 20, 400, INK2)]
    for i, (title, c, lines) in enumerate(panels):
        x = 40 + (i % 2) * 570; y = 110 + (i // 2) * 245
        o.append(f'<rect x="{x}" y="{y}" width="550" height="225" rx="14" fill="#fff" stroke="#e3e1db"/><rect x="{x}" y="{y}" width="10" height="225" rx="5" fill="{c}"/>')
        o.append(text(x + 30, y + 44, title, 22, 800, NAVY))
        for k, ln in enumerate(lines): o.append(text(x + 30, y + 84 + k * 30, ln, 17, 400, "#222"))
    o.append(text(40, 600, "Prime price and trial length as of September 2026; return rules per Amazon's help pages; always check the buy box before paying.", 14, 400, "#777"))
    o.append("</g></svg>")
    return "\n".join(o)

def main(post_dir):
    d = pathlib.Path(post_dir) / "images"; d.mkdir(parents=True, exist_ok=True)
    for name, fn in (("tiers", tiers), ("cost", cost), ("voices", voices), ("amazon", amazon)):
        (d / f"{name}.svg").write_text(fn(), encoding="utf-8"); print("wrote", d / f"{name}.svg")

if __name__ == "__main__":
    main(sys.argv[1])
