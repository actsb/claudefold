"""Infographics for the Claude + Higgsfield MCP workflow guide.
Usage: python3 scripts/ai_workflow_infographics.py posts/<slug>
Writes images/{workflow,setup,uses,cost,money,rules}.svg (1200 px wide; render_png.mjs makes the PNGs).
Figures shown are the ones stated in the post and are labelled "seen September 2026" where they change often.
"""
import pathlib, sys
FONT = "-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
NAVY, GREEN, AMBER, PAPER, INK2, PURPLE, ORANGE, RED = "#1B2A41", "#1E8E5A", "#C9781B", "#F7F5F0", "#555", "#7C5CFF", "#C9781B", "#C8102E"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def text(x, y, s, size=22, weight=400, fill=NAVY, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'
def wrap(s, n):
    words, cur, rows = s.split(), "", []
    for w in words:
        if len(cur) + len(w) + 1 > n: rows.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    rows.append(cur); return rows
def para(x, y, s, n, size=17, lh=23, fill="#333", weight=400):
    return "".join(text(x, y + i * lh, r, size, weight, fill) for i, r in enumerate(wrap(s, n)))
def check(x, y, c=GREEN, r=11):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/><path d="M {x-5} {y} l 4 4 l 7 -8" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
def warn(x, y, c=AMBER):
    return f'<path d="M {x} {y-12} l 12 21 h -24 z" fill="{c}"/><rect x="{x-1.3}" y="{y-5}" width="2.6" height="8" rx="1.3" fill="#fff"/><circle cx="{x}" cy="{y+6}" r="1.6" fill="#fff"/>'
def cross(x, y, c=RED):
    return f'<circle cx="{x}" cy="{y}" r="11" fill="{c}"/><path d="M {x-4.5} {y-4.5} l 9 9 M {x+4.5} {y-4.5} l -9 9" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>'
def head(W, H, label, title, sub):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}"><rect width="{W}" height="{H}" rx="18" fill="{PAPER}"/><g font-family="{FONT}">',
            text(40, 52, title, 30, 800), text(40, 84, sub, 20, 400, INK2)]
def foot(W, H, s):
    return [text(40, H - 22, s, 13, 400, "#888"), "</g></svg>"]
def tile(x, y, w, h, fill="#fff", stroke="#E3E1DB", rx=16):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'
def pill(x, y, w, s, fill=NAVY, color="#fff", size=13):
    return f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="{fill}"/>' + text(x + w / 2, y + 18, s, size, 700, color, "middle")
def coin(x, y, n, c=AMBER):
    """a small stack of credit coins"""
    out = ""
    for i in range(n):
        out += f'<ellipse cx="{x}" cy="{y - i*6}" rx="16" ry="6" fill="{c}" stroke="{NAVY}" stroke-width="1.2"/>'
    return out

# ---------------------------------------------------------------------------------------------------
def workflow():
    W, H = 1200, 640
    o = head(W, H, "The three-step rule: plan in Claude for free, approve stills, then spend credits on video",
             "The three-step rule the creators keep repeating", "Plan for free, lock the look on cheap stills, and only then pay for video")
    cols = [("1 · Plan", "in Claude", "0 credits", ORANGE, ["Product photo + one sentence of intent", "Shot list: length, aspect ratio, camera move", "Prompts written for the model you will use", "Iterate as often as you like"], 0),
            ("2 · Stills", "in Higgsfield", "a few credits each", NAVY, ["Generate 3–6 test frames from the plan", "Check colour, product shape, framing", "Send back what's wrong; approve what's right", "Video only ever sees approved frames"], 1),
            ("3 · Video", "in Higgsfield", "the expensive step", PURPLE, ["Image-to-video on the approved frames", "5–15 s per clip; retries cost the same again", "Voice and music added after", "Export, caption, label as AI-made"], 4)]
    for i, (t, where, cost, col, lines, coins) in enumerate(cols):
        x = 40 + i * 380
        o.append(tile(x, 110, 360, 400))
        o.append(f'<rect x="{x}" y="110" width="360" height="70" rx="16" fill="{col}"/><rect x="{x}" y="150" width="360" height="30" fill="{col}"/>')
        o.append(text(x + 20, 148, t, 28, 800, "#fff")); o.append(text(x + 340, 148, where, 17, 400, "#fff", "end"))
        o.append(text(x + 20, 214, "Credits:", 15, 700, INK2)); o.append(text(x + 96, 214, cost, 17, 800, GREEN if coins == 0 else (AMBER if coins < 3 else RED)))
        if coins: o.append(coin(x + 320, 216, coins))
        else: o.append(check(x + 320, 208))
        for k, l in enumerate(lines):
            o.append(check(x + 30, 254 + k * 52, col, 9)); o.append(para(x + 50, 259 + k * 52, l, 34, 16, 20))
        if i < 2: o.append(f'<path d="M {x+362} 300 l 14 0 M {x+368} 292 l 8 8 l -8 8" fill="none" stroke="{NAVY}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
    # the two warnings
    o.append(tile(40, 532, 1120, 70, "#FFF6E3", "#F0D9A8"))
    o.append(warn(70, 567)); o.append(para(92, 560, "Two things the tutorials flag: generations sent through the MCP or CLI always deduct credits, even on an \"unlimited\" web plan; and in Claude's connector settings set every generating tool to \"approval required\" so nothing renders without a click.", 118, 15, 20))
    o += foot(W, H, "Process as taught in the Oppadu Excel lesson (July 2026) and Higgsfield's MCP help centre; credit costs vary by model and resolution.")
    return "\n".join(o)

# ---------------------------------------------------------------------------------------------------
def setup():
    W, H = 1200, 560
    o = head(W, H, "Connecting Claude to Higgsfield in six steps: connector, sign-in, permissions, skills, first run",
             "The ten-minute setup, no code", "What the Oppadu lesson and Higgsfield's help centre have you do, in order")
    steps = [("Open Claude's connector settings", "Claude web or desktop: Settings → Connectors → Add custom connector. Claude Code and Cowork can add the same server."),
             ("Paste the Higgsfield MCP address", "Name it Higgsfield and paste the MCP URL from Higgsfield's MCP page (mcp.higgsfield.ai). No API key."),
             ("Connect and sign in", "Click Connect and log in with your Higgsfield account. One time; afterwards the tools appear inside the chat."),
             ("Set the permissions", "Block the billing tool (\"Cancel Auto-Renewal\"). Set the image, video, character and voice tools to \"approval required\"."),
             ("Add the skills", "Oppadu's five higgs-* skills (Korean lesson) or Higgsfield's nine official skills: product photoshoot, brand kit, explainer, thumbnails, more."),
             ("First run: plan only", "Upload one product photo, ask for a 15-second plan, read it. Generate nothing until the shot list is right. That run costs zero credits.")]
    for i, (t, body) in enumerate(steps):
        c, r = i % 3, i // 3; x = 40 + c * 380; y = 112 + r * 200
        o.append(tile(x, y, 360, 182))
        o.append(f'<circle cx="{x+34}" cy="{y+34}" r="20" fill="{NAVY}"/>' + text(x + 34, y + 41, str(i + 1), 20, 800, "#fff", "middle"))
        o.append(text(x + 64, y + 40, t, 19, 800))
        o.append(para(x + 20, y + 76, body, 40, 15, 20))
    o += foot(W, H, "Sources: Higgsfield MCP page and help centre (April 2026 launch); Oppadu Excel lesson (July 2026). Menu names may move; the order does not.")
    return "\n".join(o)

# ---------------------------------------------------------------------------------------------------
def uses():
    W, H = 1200, 700
    o = head(W, H, "Thirteen jobs the Claude + Higgsfield workflow does: ads, content, brand assets",
             "Thirteen jobs, one chat window", "The uses covered by Oppadu's five skills and Higgsfield's nine official skills")
    groups = [("Ads and listings", ORANGE, ["Ad plan from one product photo or a shop link", "Ad poster from the approved plan", "Short-form ad, 9:16, 5–15 seconds", "Product photoshoot: same item, many scenes", "Marketplace cards for Amazon or Etsy listings"]),
              ("Channels and content", PURPLE, ["3D-character Shorts from a character + topic", "Explainer video with narration", "Faceless edutainment clips, scripted scene by scene", "YouTube thumbnails that match the video"]),
              ("Brand and web", NAVY, ["A new logo, or a clean-up of the old one", "Brand kit: colours, type, icon set", "Website hero visuals and scroll animation", "A consistent character (Soul ID) reused across every job"])]
    n = 1
    for i, (t, col, items) in enumerate(groups):
        x = 40 + i * 380
        o.append(tile(x, 110, 360, 540))
        o.append(f'<rect x="{x}" y="110" width="360" height="54" rx="16" fill="{col}"/><rect x="{x}" y="140" width="360" height="24" fill="{col}"/>')
        o.append(text(x + 20, 146, t, 22, 800, "#fff"))
        for k, it in enumerate(items):
            y = 196 + k * 92
            o.append(f'<circle cx="{x+34}" cy="{y}" r="17" fill="{col}"/>' + text(x + 34, y + 6, str(n), 16, 800, "#fff", "middle")); n += 1
            o.append(para(x + 62, y + 5, it, 30, 16, 21))
    o += foot(W, H, "Jobs 1–3, 6–7 and 10 are Oppadu's higgs-* skills; 4–5, 8–9 and 11–13 are Higgsfield's official skills repo (github.com/higgsfield-ai/skills). Counted once each.")
    return "\n".join(o)

# ---------------------------------------------------------------------------------------------------
def cost():
    W, H = 1200, 690
    o = head(W, H, "What a fifteen-second AI product ad costs in credits, from stills to three clips and retries",
             "What a 15-second ad really costs", "One worked example in credits, with the numbers creators reported in 2026 (check today's plan page)")
    rows = [("Plan and shot list", "Claude", "0", 0, "free at every tier of the workflow"),
            ("6 test stills, 3 approved", "image model", "~30", 1, "roughly 5 credits a frame; cheap enough to iterate"),
            ("3 clips × 5 s, image-to-video", "Kling 3.0 via MCP", "75", 3, "25 credits per 5-second clip in one creator's logged run"),
            ("One retry per clip (plan for it)", "same", "75", 3, "a failed generation costs the same as a good one"),
            ("Narration line", "voice model", "~5", 1, "or record it yourself for free")]
    y = 118
    o.append(f'<rect x="40" y="{y}" width="1120" height="40" rx="10" fill="{NAVY}"/>')
    for x, t in ((60, "Step"), (420, "Model"), (640, "Credits"), (760, "What it means")): o.append(text(x, y + 26, t, 15, 700, "#fff"))
    for i, (step, model, cr, coins, note) in enumerate(rows):
        yy = y + 52 + i * 58
        o.append(f'<rect x="40" y="{yy}" width="1120" height="50" rx="10" fill="#fff" stroke="#E3E1DB"/>')
        o.append(text(60, yy + 31, step, 17, 700)); o.append(text(420, yy + 31, model, 16, 400, INK2))
        o.append(text(640, yy + 31, cr, 20, 800, GREEN if cr == "0" else NAVY))
        if coins: o.append(coin(720, yy + 34, coins))
        o.append(text(760, yy + 31, note, 15, 400, "#333"))
    yy = y + 52 + 5 * 58 + 8
    o.append(f'<rect x="40" y="{yy}" width="1120" height="84" rx="10" fill="{GREEN}"/>')
    o.append(text(60, yy + 36, "Total: about 185 credits for one finished 15-second ad", 22, 800, "#fff"))
    o.append(text(60, yy + 64, "About $12 bought as prepaid credits at the rate seen in September 2026, or roughly a fifth of the mid-tier monthly plan.", 15, 400, "#E6F4EC"))
    o.append(tile(40, yy + 102, 1120, 64, "#FFF6E3", "#F0D9A8")); o.append(warn(70, yy + 134))
    o.append(para(92, yy + 127, "Credits per generation depend on the model and resolution and change without notice; Higgsfield renamed its plans twice in 2026. Run one clip, read what it cost in your history, then multiply. Never buy an annual plan before that.", 120, 15, 20))
    o += foot(W, H, "Per-clip figure from a creator's published run log (Kling 3.0, 5 s, June 2026); still and voice estimates rounded from Higgsfield's model pricing pages. Your plan page shows the current rates.")
    return "\n".join(o)

# ---------------------------------------------------------------------------------------------------
def money():
    W, H = 1200, 640
    o = head(W, H, "Four ways creators get paid for this workflow, and what each one requires",
             "Who pays for the video: the four routes creators describe", "No income figures here on purpose. Each route has a gate you must clear first.")
    routes = [("1 · A client pays per video", ORANGE, "Local shops, medical practices, restaurants: a 15-second ad or a product detail page. The Korean tutorials are built around this.", ["Client's product, client's brief", "Written approval of the plan before you spend credits", "Keep the generation log as your delivery record"]),
              ("2 · Your own listing sells more", GREEN, "Amazon, Etsy or Shopify sellers make listing videos, lifestyle shots and marketplace cards for products they already sell.", ["Only the product you sell, shown as it is", "No invented features, no fake reviews", "Amazon's video rules still apply to AI clips"]),
              ("3 · A platform pays for views", PURPLE, "YouTube Partner Program: 1,000 subscribers plus 4,000 watch hours or 10 million Shorts views, then the July 2025 \"inauthentic content\" rule decides if AI clips qualify.", ["Original narrative, editing and voice each video", "Label altered or synthetic content on upload", "Higgsfield's own creator campaigns are a separate pool"]),
              ("4 · Referrals pay a share", NAVY, "Reviewers and teachers earn a commission when a reader subscribes through their link: Higgsfield up to 25% for 12 months, ElevenLabs 22%, most others 20–30%.", ["Disclose before the link, in plain words", "First-hand use, original clips, honest drawbacks", "No earnings promises; attribute every number"])]
    for i, (t, col, body, reqs) in enumerate(routes):
        c, r = i % 2, i // 2; x = 40 + c * 570; y = 112 + r * 250
        o.append(tile(x, y, 550, 232))
        o.append(f'<rect x="{x}" y="{y}" width="550" height="46" rx="16" fill="{col}"/><rect x="{x}" y="{y+24}" width="550" height="22" fill="{col}"/>')
        o.append(text(x + 18, y + 31, t, 20, 800, "#fff"))
        o.append(para(x + 18, y + 74, body, 62, 15, 20))
        for k, rq in enumerate(reqs):
            o.append(check(x + 28, y + 150 + k * 26, col, 9)); o.append(text(x + 46, y + 155 + k * 26, rq, 15, 600, "#333"))
    o += foot(W, H, "Program terms as published in September 2026 and subject to change; YouTube thresholds from the Partner Program page. Reported creator incomes are marketing claims and are not shown.")
    return "\n".join(o)

# ---------------------------------------------------------------------------------------------------
def rules():
    W, H = 1200, 700
    o = head(W, H, "Twelve rules that keep an AI product video legal in the United States: disclosure, likeness, licences, labels",
             "Before you publish an AI ad: the twelve-line checklist", "US rules as of September 2026; the ones the FTC, the platforms and the tool licences actually enforce")
    items = [("Disclose paid links before the click", "FTC Endorsement Guides: \"paid link\" or \"I earn a commission\", near the link, not only in a footer."),
             ("No fake or AI-written reviews", "FTC rule effective Oct 21, 2024; civil penalties per violation. An AI avatar is not a customer."),
             ("No earnings promises", "\"Creators report\" with a source and a date; never \"you will make\". Typical results, if any, must be substantiated."),
             ("Label synthetic media where the platform asks", "YouTube's altered-or-synthetic disclosure on upload; TikTok and Meta have their own labels."),
             ("Never generate a real person's face or voice", "State right-of-publicity laws (Tennessee's ELVIS Act among them) and the federal TAKE IT DOWN Act; use invented characters."),
             ("Commercial rights come with the paid tier", "Free tiers of Kling, Runway, HeyGen and ElevenLabs are watermarked or non-commercial; keep the invoice."),
             ("Own the music", "Synthesize it, license it, or use the tool's licensed library; YouTube's audio library is for YouTube only."),
             ("Say what is AI in the ad itself", "\"Generated with Higgsfield\" in the caption. New York's synthetic-performer law reaches ads from 2026."),
             ("Show the product as it is", "No invented features or sizes; the FTC's truth-in-advertising standard applies to synthetic footage."),
             ("Keep the generation log", "Prompts, dates, model names and credit receipts; the record that answers a client, a platform or a regulator."),
             ("Embed, never re-upload, other creators' videos", "YouTube's player is licensed for embedding; downloading or re-hosting a video is not."),
             ("Name tools, don't borrow their logos", "Nominative use of Claude, Higgsfield or Kling is fine; their logos and any hint of endorsement are not.")]
    for i, (t, body) in enumerate(items):
        c, r = i % 2, i // 2; x = 40 + c * 570; y = 108 + r * 90
        o.append(tile(x, y, 550, 78)); o.append(check(x + 26, y + 26))
        o.append(text(x + 46, y + 31, t, 17, 800)); o.append(para(x + 46, y + 54, body, 78, 13.5, 17, "#444"))
    o += foot(W, H, "Summarised from the FTC Endorsement Guides (2023), the Consumer Reviews and Testimonials Rule (2024), YouTube's policies, state publicity laws and the tools' terms. Not legal advice.")
    return "\n".join(o)

def main(post_dir):
    d = pathlib.Path(post_dir) / "images"; d.mkdir(parents=True, exist_ok=True)
    for name, fn in (("workflow", workflow), ("setup", setup), ("uses", uses), ("cost", cost), ("money", money), ("rules", rules)):
        (d / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print("wrote workflow, setup, uses, cost, money, rules ->", d)

if __name__ == "__main__":
    main(sys.argv[1])
