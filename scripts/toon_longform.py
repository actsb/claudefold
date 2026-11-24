#!/usr/bin/env python3
"""Join comic episodes into one YouTube video, landscape (1920x1080) or portrait (1080x1920), with chapters, music,
subtitles and titles/descriptions in the same 11 languages as the Shorts.

  python3 scripts/toon_longform.py CONFIG.json OUT_DIR

CONFIG: {"id": "season1", "orient": "landscape" | "portrait", "title": ..., "description": ... ({chapters} is replaced),
         "intro_card": [...], "intro_sub": [...], "outro_card": [...], "outro_sub": [...]   (omit for no intro/outro card),
         "episodes": ["posts/<dir>", ...], "music_seed": 5,
         "reuse_meta": "ep1-youtube.json"   (optional: take the 11-language title/description from this file, minus #Shorts)}
Each episode's panel subtitles are reused from OUT_DIR/<ep>.<lang>.srt (made by toon_shorts.py), so the translations match
the Shorts; only intro/outro lines, the title and the description are translated here (Gemini via the proxy).
"""
import json, os, pathlib, re, subprocess, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import webtoon, toon_shorts as TS

ROOT = TS.ROOT; FF = TS.FF; FPS, XF = 30, 0.45
VW, VH = 1920, 1080

def t(x, y, s, size, weight, fill, anchor="middle", ls=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter,Helvetica,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" letter-spacing="{ls}">{html.escape(s)}</text>'

def band(label, title):
    if VW < VH:   # portrait: the Shorts band
        return TS.band_svg((label.upper(), title), "Full guide and sources: link in description")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}"><defs>'
            '<linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1424" stop-opacity="0.85"/><stop offset="1" stop-color="#0B1424" stop-opacity="0"/></linearGradient>'
            '<linearGradient id="b" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#0B1424" stop-opacity="0.85"/><stop offset="1" stop-color="#0B1424" stop-opacity="0"/></linearGradient></defs>'
            f'<rect width="{VW}" height="130" fill="url(#a)"/><rect y="{VH-110}" width="{VW}" height="110" fill="url(#b)"/>'
            + t(48, 62, f"{label} · {title}", 30, 800, "#FFFFFF", "start") + t(VW - 48, 62, "VERDICT PICKS TOON", 24, 800, "#7FD1A8", "end", 5)
            + t(VW / 2, VH - 40, "Characters are fictional · art made with Google Gemini (AI) · full guides and sources: links in the description", 24, 500, "#DDE6F2")
            + '</svg>')

def card(lines, sub):
    big = 76 if VW > VH else 70; y0 = VH * 0.39
    body = "".join(t(VW / 2, y0 + i * (big + 16), l, big, 800, "#FFFFFF") for i, l in enumerate(lines))
    subs = [x for s in sub for x in webtoon.wrap(s, VW - 200, 36)]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}"><rect width="{VW}" height="{VH}" fill="#1B2A41"/>'
            f'<rect x="60" y="60" width="{VW-120}" height="{VH-120}" fill="none" stroke="#2E4266" stroke-width="4"/>'
            + t(VW / 2, y0 - 120, "VERDICT PICKS TOON", 34, 800, "#7FD1A8", ls=10) + body
            + "".join(t(VW / 2, y0 + 30 + len(lines) * (big + 16) + i * 52, s, 36, 500, "#DDE6F2") for i, s in enumerate(subs)) + '</svg>')

def srt_lines(f):
    blocks = re.split(r"\n\s*\n", f.read_text(encoding="utf-8").strip())
    return [" ".join(b.splitlines()[2:]) for b in blocks]

def clip(png, art, D, bandpng, out):
    w, h = [int(v) for v in subprocess.run(["identify", "-format", "%w %h", str(png)], capture_output=True, text=True).stdout.split()]
    if VW > VH:
        fh = 860; fw = round(fh * w / h)
        if fw > 1700: fw = 1700; fh = round(fw * h / w)
    else:
        fw = 1000; fh = round(fw * h / w)
        if fh > 1340: fh = 1340; fw = round(fh * w / h)
    src = art if art and art.exists() else png
    dy = 8 if VW > VH else 30
    flt = (f"[0:v]scale={VW}:{VH}:force_original_aspect_ratio=increase,crop={VW}:{VH},gblur=sigma=30,eq=brightness=-0.2:saturation=1.1[bg];"
           f"[1:v]scale={fw}:{fh},format=rgba,scale=w='trunc({fw}*(1+0.035*t/{D:.3f})/2)*2':h=-2:eval=frame[fg];"
           f"[bg][fg]overlay=x='(W-w)/2':y='(H-h)/2+{dy}':eval=frame[v1];[2:v]format=rgba,scale={VW}:{VH}[band];[v1][band]overlay=0:0,fps={FPS},format=yuv420p[v]")
    TS.run(FF, "-y", "-loop", "1", "-t", f"{D:.3f}", "-i", src, "-loop", "1", "-t", f"{D:.3f}", "-i", png, "-loop", "1", "-t", f"{D:.3f}", "-i", bandpng,
           "-filter_complex", flt, "-map", "[v]", "-r", FPS, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out)

def card_clip(png, D, out):
    TS.run(FF, "-y", "-loop", "1", "-t", f"{D:.3f}", "-i", png, "-vf", f"scale={VW}:{VH},fps={FPS},format=yuv420p", "-c:v", "libx264", "-crf", "18", out)

def main(cfg_path, out):
    global VW, VH
    cfg = json.loads(pathlib.Path(cfg_path).read_text(encoding="utf-8")); out = pathlib.Path(out); sid = cfg["id"]
    VW, VH = (1080, 1920) if cfg.get("orient") == "portrait" else (1920, 1080)
    work = out / f"{sid}-work"; png = work / "png"; png.mkdir(parents=True, exist_ok=True)
    for f in png.glob("*"): f.unlink()
    for f in work.glob("c*.mp4"): f.unlink()
    shots, chapters = [], []      # shot: (kind, png, art, band, seconds, (episode id, cue index) or None)
    if cfg.get("intro_card"):
        (png / "intro.svg").write_text(card(cfg["intro_card"], cfg["intro_sub"]), encoding="utf-8")
        shots.append(("card", png / "intro.png", None, None, 4.5, None))
    for d in cfg["episodes"]:
        d = ROOT / d; spec, blocks = webtoon.build(d, return_blocks=True); eid = spec["id"]
        for i, (gap, h, svg, tr) in enumerate(blocks):
            (png / f"{eid}-b{i:02d}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {h}"><rect width="800" height="{h}" fill="#fff"/>{svg}</svg>', encoding="utf-8")
        (png / f"{eid}-band.svg").write_text(band(f"Episode {eid[2:]}", spec["title"]), encoding="utf-8")
        texts = [[spec["title"]]] + [TS.panel_lines(p) for p in spec["panels"]] + [[spec.get("end", "")]]
        chapters.append((f"Episode {eid[2:]}: {spec['title']}", 0 if not chapters else len(shots)))
        for i, tx in enumerate(texts):
            n = sum(len(x) for x in tx); board = 0 < i <= len(spec["panels"]) and "art" not in spec["panels"][i - 1]
            D = 3.4 if i == 0 else 3.6 if i == len(texts) - 1 else min(8.0, max(5.5 if board else 3.2, 2.4 + 0.065 * n))
            shots.append(("panel", png / f"{eid}-b{i:02d}.png", d / "toon-art" / f"{eid}-p{i:02d}.jpg", png / f"{eid}-band.png", D, (eid, i)))
    if cfg.get("outro_card"):
        (png / "outro.svg").write_text(card(cfg["outro_card"], cfg["outro_sub"]), encoding="utf-8")
        shots.append(("card", png / "outro.png", None, None, 6.0, None))
    subprocess.run(["node", str(ROOT / "scripts" / "render_png.mjs"), str(png)], check=True, stdout=subprocess.DEVNULL)
    for f in png.glob("*-band.svg"):
        subprocess.run(["node", str(ROOT / "scripts" / "render_png.mjs"), str(png), f.name], check=True, stdout=subprocess.DEVNULL, env={**os.environ, "ALPHA": "1"})
    clips = []
    for k, (kind, p, art, bandpng, D, _) in enumerate(shots):
        c = work / f"c{k:03d}.mp4"
        (card_clip(p, D, c) if kind == "card" else clip(p, art, D, bandpng, c)); clips.append(c)
    dur = [s[4] for s in shots]; total = sum(dur) - XF * (len(dur) - 1)
    starts, x = [], 0.0
    for D in dur: starts.append(x); x += D - XF
    ins = []; [ins.extend(["-i", str(c)]) for c in clips]
    chain, last, off = [], "[0:v]", 0.0
    for i in range(1, len(clips)):
        off += dur[i - 1] - XF; chain.append(f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]"); last = f"[x{i}]"
    music = work / "music.wav"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "make_music.py"), str(music), str(int(total) + 2), str(cfg.get("music_seed", 5))], check=True, stdout=subprocess.DEVNULL)
    mp4 = out / f"{sid}.mp4"
    TS.run(FF, "-y", *ins, "-i", music, "-filter_complex", ";".join(chain) + f";[{len(clips)}:a]volume=0.5,afade=t=in:d=1,afade=t=out:st={total-2.5:.2f}:d=2.5[a]",
           "-map", last, "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", mp4)
    def ts(s): s = int(s); return f"{s//60}:{s%60:02d}"
    chap = "\n".join(f"{ts(starts[i])} {name}" for name, i in chapters) if len(chapters) >= 3 else ""
    extra_en = [" ".join(cfg.get("intro_card", []) + cfg.get("intro_sub", [])), " ".join(cfg.get("outro_card", []) + cfg.get("outro_sub", []))]
    reuse = json.loads((out / cfg["reuse_meta"]).read_text(encoding="utf-8"))["metadata"] if cfg.get("reuse_meta") else None
    strip = lambda s: re.sub(r"\s*#Shorts\b", "", s).strip()
    meta, extra_by = {}, {}
    if reuse:
        meta = {lang: {"title": strip(v["title"]), "description": strip(v["description"])} for lang, v in reuse.items()}
        extra_by = {lang: extra_en for lang in TS.LANGS}
    else:
        desc_en = cfg["description"].replace("{chapters}", chap)
        meta["en"] = {"title": cfg["title"], "description": desc_en}; extra_by["en"] = extra_en
        for lang, name in TS.LANGS.items():
            if lang == "en": continue
            r = TS.gemini_json(f"Translate this YouTube video's title, description and two subtitle lines from English into {name}. Keep product names, model numbers, "
                               f"prices, URLs, hashtags, timestamps at the start of chapter lines, and source names exactly; translate dates naturally; "
                               f"'space heater' is an electric room heater. Return JSON {{\"title\": str (max 100 characters), \"description\": str, \"subtitles\": [str, str]}}.\n\n"
                               + json.dumps({"title": cfg["title"], "description": desc_en, "subtitles": extra_en}, ensure_ascii=False))
            meta[lang] = {"title": r["title"][:100], "description": r["description"]}; extra_by[lang] = r["subtitles"]; print("translated", lang)
    for lang in TS.LANGS:
        ep_lines = {}
        for kind, p, art, b, D, ref in shots:
            if ref and ref[0] not in ep_lines: ep_lines[ref[0]] = srt_lines(out / f"{ref[0]}.{lang}.srt")
        lines = []
        for k, (kind, p, art, b, D, ref) in enumerate(shots):
            if ref: lines.append(ep_lines[ref[0]][ref[1]])
            else: lines.append(extra_by[lang][0] if k == 0 else extra_by[lang][1])
        (out / f"{sid}.{lang}.srt").write_text("".join(f"{k+1}\n{TS.srt_time(starts[k] + 0.15)} --> {TS.srt_time(starts[k] + dur[k] - XF)}\n{l}\n\n" for k, l in enumerate(lines) if l), encoding="utf-8")
    TS.run(FF, "-y", "-ss", "6", "-i", mp4, "-frames:v", "1", "-q:v", "3", out / f"{sid}-thumb.jpg")
    (out / f"{sid}-youtube.json").write_text(json.dumps({"video": mp4.name, "orientation": f"{VW}x{VH}", "seconds": round(total, 1), "default_language": "en",
        "made_for_kids": False, "category": "Howto & Style", "altered_content": "No (stylised cartoon, not realistic)", "paid_promotion": False,
        "chapters": chap, "languages": TS.LANGS, "metadata": meta}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    import shutil; shutil.rmtree(work, ignore_errors=True)
    print(f"{mp4} ({mp4.stat().st_size // 1024} KB, {total:.0f} s, {len(clips)} shots, {VW}x{VH})" + (f"\n{chap}" if chap else ""))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
