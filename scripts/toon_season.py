#!/usr/bin/env python3
"""Build the landscape long-form video for a season from its own plan (shorts/season1.json), never from the Shorts.

  python3 scripts/toon_season.py shorts/season1.json OUT_DIR

Per episode: a new 16:9 cold-open scene (Gemini), the story told with the comic's lettered panels, then "Vera's whiteboard":
explainer slides from the guide (comparison, cost, checklist, buy/wait/skip, each with its source) over a new 16:9 Vera scene.
A season key-art intro and an outro card. 1920x1080, chapters (story / explained per episode), synthesised music,
subtitles and titles/descriptions in the 11 languages: the story panels reuse the Shorts' translated subtitle lines
(OUT_DIR/<ep>.<lang>.srt); everything new (captions, slides, intro, outro, title, description) is translated here.
New art is cached in shorts/art/ (rerun costs nothing).
"""
import base64, html, json, os, pathlib, re, shutil, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import webtoon, toon_shorts as TS, toon_art as A, toon_longform as L

ROOT = TS.ROOT; FF = TS.FF
L.VW, L.VH = 1920, 1080
VW, VH, XF = 1920, 1080, 0.45
INK = "#1B2A41"

def art(key, prompt, cast, out):
    f = out / "art" / f"{key}.jpg"
    if f.exists(): return f
    f.parent.mkdir(parents=True, exist_ok=True)
    refs = [ROOT / "brand" / "toon-cast" / f"{c}.jpg" for c in cast if (ROOT / "brand" / "toon-cast" / f"{c}.jpg").exists()]
    p = (A.STYLE + "Characters: " + " ".join(A.CAST[c] for c in cast) + " Scene: " + prompt + A.NO_TEXT
         + (" The attached images are character model sheets: use them only for each character's face, hair, colors and outfit. Draw ONE single scene." if refs else ""))
    old = A.RATIO.get("16:9"); A.RATIO["16:9"] = "16:9"
    png = A.gen(p, "16:9", refs); tmp = f.with_suffix(".png"); tmp.write_bytes(png)
    A.trim(tmp)
    subprocess.run(["convert", str(tmp), "-resize", "1920x1080^", "-gravity", "center", "-extent", "1920x1080", "-quality", "88", str(f)], check=True); tmp.unlink()
    print("art", f.name); return f

def t(x, y, s, size, weight, fill, anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter,Helvetica,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}">{html.escape(s)}</text>'

def slide_svg(bg, s, label):
    """A whiteboard card over the right 60% of the Vera scene."""
    x0, y0, w = 780, 150, 1080
    rows = s.get("rows"); bullets = s.get("bullets")
    body, y = [], y0 + 150
    if rows:
        size = 34 if len(rows) <= 5 else 30; step = size + 30
        for a, b in rows:
            body.append(f'<line x1="{x0+50}" y1="{y-size-8}" x2="{x0+w-50}" y2="{y-size-8}" stroke="#E3E8EF" stroke-width="2"/>')
            body.append(t(x0 + 50, y, a, size, 700, INK)); body.append(t(x0 + w - 50, y, b, size, 600, "#1E8E5A", "end")); y += step
    else:
        for b in bullets:
            lines = webtoon.wrap(b, w - 150, 34)
            body.append(f'<circle cx="{x0+62}" cy="{y-11}" r="8" fill="#1E8E5A"/>')
            for i, l in enumerate(lines): body.append(t(x0 + 90, y + i * 46, l, 34, 600, INK))
            y += 46 * len(lines) + 30
    h = max(560, y - y0 + 80)
    src = webtoon.wrap("Source: " + s["source"], w - 100, 24)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}">'
            f'<image href="data:image/jpeg;base64,{base64.b64encode(bg.read_bytes()).decode()}" width="{VW}" height="{VH}" preserveAspectRatio="xMidYMid slice"/>'
            f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="28" fill="#FFFFFF" fill-opacity="0.96" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x0}" y="{y0}" width="{w}" height="96" rx="28" fill="{INK}"/><rect x="{x0}" y="{y0+60}" width="{w}" height="36" fill="{INK}"/>'
            + t(x0 + 50, y0 + 64, s["title"], 42, 800, "#FFFFFF") + "".join(body)
            + "".join(t(x0 + 50, y0 + h - 40 - 32 * (len(src) - 1 - i), l, 24, 500, "#5A6578") for i, l in enumerate(src))
            + f'<rect x="0" y="0" width="{VW}" height="96" fill="#0B1424" fill-opacity="0.55"/>'
            + t(48, 62, label, 30, 800, "#FFFFFF") + t(VW - 48, 62, "VERDICT PICKS TOON", 24, 800, "#7FD1A8", "end") + '</svg>')

def caption_svg(bg, caption, label):
    lines = webtoon.wrap(caption, 1500, 44, True)
    y = VH - 120 - 58 * len(lines)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}">'
            f'<image href="data:image/jpeg;base64,{base64.b64encode(bg.read_bytes()).decode()}" width="{VW}" height="{VH}" preserveAspectRatio="xMidYMid slice"/>'
            f'<rect x="80" y="{y-70}" width="{VW-160}" height="{58*len(lines)+70}" rx="16" fill="#0B1424" fill-opacity="0.78"/>'
            + "".join(t(VW / 2, y + i * 58, l, 44, 700, "#FFFFFF", "middle") for i, l in enumerate(lines))
            + f'<rect x="0" y="0" width="{VW}" height="96" fill="#0B1424" fill-opacity="0.45"/>'
            + t(48, 62, label, 30, 800, "#FFFFFF") + t(VW - 48, 62, "VERDICT PICKS TOON", 24, 800, "#7FD1A8", "end") + '</svg>')

def still_clip(png, D, out, zoom=0.04):
    TS.run(FF, "-y", "-framerate", "30", "-loop", "1", "-t", f"{D:.3f}", "-i", png, "-filter_complex",
           f"[0:v]scale={VW*2}:{VH*2},zoompan=z='1+{zoom}*on/({D*30:.0f})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={VW}x{VH}:fps=30,format=yuv420p[v]",
           "-map", "[v]", "-t", f"{D:.3f}", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", out)

def main(cfg_path, out):
    cfg = json.loads(pathlib.Path(cfg_path).read_text(encoding="utf-8")); out = pathlib.Path(out); sid = cfg["id"]
    work = out / f"{sid}-work"; png = work / "png"; shutil.rmtree(work, ignore_errors=True); png.mkdir(parents=True)
    shots, chapters, new_lines = [], [], []    # shot: (kind, file, art, band, seconds, ref); ref = ("ep", eid, idx) | ("new", k)
    def new(text): new_lines.append(text); return ("new", len(new_lines) - 1)
    specs, open_cast = {}, {}
    # intro
    key = art(f"{sid}-intro", cfg["intro"]["art"], cfg["intro"]["cast"], out)
    (png / "intro.svg").write_text(caption_svg(key, " ".join(cfg["intro"]["card"] + cfg["intro"]["sub"]), "Season 1"), encoding="utf-8")
    shots.append(("still", png / "intro.png", None, None, 5.5, new(" ".join(cfg["intro"]["card"] + cfg["intro"]["sub"]))))
    for e in cfg["episodes"]:
        d = ROOT / e["dir"]; spec, blocks = webtoon.build(d, return_blocks=True); eid = spec["id"]; label = f"Episode {eid[2:]} · {spec['title']}"
        specs[eid] = spec; open_cast[len(new_lines)] = [c for c in e["open"].get("cast", []) if c in ("sam", "jo", "june", "vera")]
        chapters.append((f"Episode {eid[2:]}: {spec['title']}", 0 if not chapters else len(shots)))
        op = art(f"{sid}-{eid}-open", e["open"]["art"], e["open"].get("cast", []), out)
        (png / f"{eid}-open.svg").write_text(caption_svg(op, e["open"]["caption"], label), encoding="utf-8")
        shots.append(("still", png / f"{eid}-open.png", None, None, 5.0, new(e["open"]["caption"])))
        for i, (gap, h, svg, tr) in enumerate(blocks[1:-1], 1):          # the story: lettered comic panels (no title or end card)
            (png / f"{eid}-b{i:02d}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {h}"><rect width="800" height="{h}" fill="#fff"/>{svg}</svg>', encoding="utf-8")
            n = sum(len(x) for x in TS.panel_lines(spec["panels"][i - 1])); board = "art" not in spec["panels"][i - 1]
            shots.append(("panel", png / f"{eid}-b{i:02d}.png", d / "toon-art" / f"{eid}-p{i:02d}.jpg", png / f"{eid}-band.png",
                          min(7.5, max(5.0 if board else 3.0, 2.2 + 0.06 * n)), ("ep", eid, i)))
        (png / f"{eid}-band.svg").write_text(L.band(f"Episode {eid[2:]}", spec["title"]), encoding="utf-8")
        chapters.append((f"Episode {eid[2:]} explained", len(shots)))
        bd = art(f"{sid}-{eid}-board", e["board"]["art"], e["board"].get("cast", []), out)
        for k, s in enumerate(e["slides"]):
            (png / f"{eid}-s{k}.svg").write_text(slide_svg(bd, s, label), encoding="utf-8")
            txt = s["title"] + ": " + "; ".join((" — ".join(r) for r in s["rows"]) if s.get("rows") else s["bullets"]) + f" (Source: {s['source']})"
            shots.append(("still", png / f"{eid}-s{k}.png", None, None, min(11.0, max(7.0, 2.5 + 0.045 * len(txt))), new(txt)))
    (png / "outro.svg").write_text(L.card(cfg["outro"]["card"], cfg["outro"]["sub"]), encoding="utf-8")
    shots.append(("still", png / "outro.png", None, None, 6.0, new(" ".join(cfg["outro"]["card"] + cfg["outro"]["sub"]))))
    subprocess.run(["node", str(ROOT / "scripts" / "render_png.mjs"), str(png)], check=True, stdout=subprocess.DEVNULL)
    for f in png.glob("*-band.svg"):
        subprocess.run(["node", str(ROOT / "scripts" / "render_png.mjs"), str(png), f.name], check=True, stdout=subprocess.DEVNULL, env={**os.environ, "ALPHA": "1"})
    import toon_voice as V
    plan = []
    for k, (kind, p, a, b, D, ref) in enumerate(shots):
        if ref[0] == "ep":
            pn = specs[ref[1]]["panels"][ref[2] - 1]; plan.append({"kind": f"story panel, episode {ref[1][2:]}", "text": TS.panel_lines(pn), "speakers": TS.panel_speakers(pn)})
        elif k == 0: plan.append({"kind": "season opening over the key art", "text": [new_lines[ref[1]]], "speakers": ["narrator"]})
        elif k == len(shots) - 1: plan.append({"kind": "outro card", "text": [new_lines[ref[1]], "Links to the full guides are in the description."], "speakers": ["narrator", "vera"]})
        elif ref[1] in open_cast: plan.append({"kind": "episode cold open", "text": [new_lines[ref[1]]], "speakers": ["narrator"] + open_cast[ref[1]]})
        else: plan.append({"kind": "Vera's whiteboard slide: read the key facts clearly, with one quick joke at most", "text": [new_lines[ref[1]]], "speakers": ["vera", "narrator"]})
    script = V.write_script(plan, "6-to-7-minute landscape YouTube video: three comic stories, each followed by Vera explaining the facts on a whiteboard",
                            out / f"{sid}-narration.json", 900,
                            extra="Be a lively sitcom: in most story shots the narrator adds a quick joke or reaction, and characters banter. On whiteboard slides the rows are "
                                  "already on screen, so Vera does NOT read every row: she picks the two or three that matter most, says them with energy, and the narrator "
                                  "adds one playful line; never read the word 'Source' or dashes aloud (name the source naturally once, e.g. 'says CNET').")
    voiced, dur = [], []
    for k, ((kind, p, a, b, D, ref), lines) in enumerate(zip(shots, script)):
        vs = [(l, *V.synth(l["text"], l["who"])) for l in lines]
        speech = sum(x[2] for x in vs) + 0.15 * max(0, len(vs) - 1)
        floor = 4.0 if kind == "still" and ref[0] == "new" and plan[k]["kind"].startswith("Vera") else 2.2
        dur.append(max(floor, speech + 0.8)); voiced.append(vs)
    clips = []
    for k, ((kind, p, a, b, D, ref), D2) in enumerate(zip(shots, dur)):
        c = work / f"c{k:03d}.mp4"
        (still_clip(p, D2, c) if kind == "still" else L.clip(p, a, D2, b, c)); clips.append(c)
    starts, x = [], 0.0
    for D in dur: starts.append(x); x += D - XF
    total = x + XF
    placed, cues = [], []
    for k, vs in enumerate(voiced):
        t = starts[k] + 0.3
        for l, f, sec in vs: placed.append((t, f)); cues.append((t, t + sec, l["text"])); t += sec + 0.15
    music = work / "music.wav"; mixed = work / "mix.wav"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "make_music.py"), str(music), str(int(total) + 2), str(cfg.get("music_seed", 5))], check=True, stdout=subprocess.DEVNULL)
    V.mix(placed, total, music, mixed)
    ins = []; [ins.extend(["-i", str(c)]) for c in clips]
    chain, last, off = [], "[0:v]", 0.0
    for i in range(1, len(clips)):
        off += dur[i - 1] - XF; chain.append(f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]"); last = f"[x{i}]"
    mp4 = out / f"{sid}.mp4"
    TS.run(FF, "-y", *ins, "-i", mixed, "-filter_complex", ";".join(chain), "-map", last, "-map", f"{len(clips)}:a", "-t", f"{total:.2f}",
           "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-maxrate", "1800k", "-bufsize", "3600k", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", mp4)
    def ts(s): s = int(s); return f"{s//60}:{s%60:02d}"
    chap = "\n".join(f"{ts(starts[i])} {name}" for name, i in chapters)
    desc_en = cfg["description"].replace("{chapters}", chap)
    meta, subs = TS.localize(sid, out, cfg["title"], desc_en, cfg.get("tags", []), [c[2] for c in cues], "video")
    for lang, lines in subs.items():
        (out / f"{sid}.{lang}.srt").write_text("".join(f"{k+1}\n{TS.srt_time(a)} --> {TS.srt_time(b)}\n{l}\n\n" for k, ((a, b, _), l) in enumerate(zip(cues, lines))), encoding="utf-8")
    th = ROOT / "shorts" / "thumbs" / f"{sid}.jpg"
    subprocess.run(["convert", str(th if th.exists() else png / "intro.png"), "-resize", "1280x720", "-quality", "90", str(out / f"{sid}-thumb.jpg")], check=True)
    (out / f"{sid}-youtube.json").write_text(json.dumps({"video": mp4.name, "thumbnail": f"{sid}-thumb.jpg", "orientation": "1920x1080", "seconds": round(total, 1),
        "default_language": "en", "made_for_kids": False, "category": "Howto & Style", "altered_content": "No (stylised cartoon, not realistic)", "paid_promotion": False,
        "voices": "Google Gemini TTS (AI voices)", "chapters": chap, "languages": TS.LANGS, "metadata": meta}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    shutil.rmtree(work, ignore_errors=True)
    print(f"{mp4} ({mp4.stat().st_size // 1024} KB, {total:.0f} s, {len(clips)} shots, {len(cues)} voice lines)\n{chap}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
