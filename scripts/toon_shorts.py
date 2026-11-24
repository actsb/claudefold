#!/usr/bin/env python3
"""Turn a post's comic (webtoon.json + toon-art/) into a YouTube Short: 1080x1920, 30 fps, under 60 s, music, English
subtitles, plus subtitle files and titles/descriptions in 11 languages (translated by Gemini through the proxy-held key).

  python3 scripts/toon_shorts.py posts/<dir> OUT_DIR [--no-translate]

Writes OUT_DIR/<id>.mp4, <id>.<lang>.srt for every language and <id>-youtube.json (title and description per language,
plus the upload settings). Every panel is the lettered comic panel (the same facts as the guide), centred over a blurred
copy of its art with a slow push-in, crossfaded to the next. Music is synthesised by scripts/make_music.py (no samples).
Needs FFMPEG (scripts/bootstrap.sh) and Playwright (scripts/render_png.mjs).
"""
import json, os, pathlib, re, subprocess, sys, urllib.request, urllib.error, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import webtoon

ROOT = pathlib.Path(__file__).resolve().parent.parent
FF = os.environ.get("FFMPEG") or str(next(pathlib.Path("/tmp").glob("claude-0/*/*/scratchpad/ffm/node_modules/ffmpeg-static/ffmpeg"), "ffmpeg"))
VW, VH, FPS, XF = 1080, 1920, 30, 0.35
LANGS = {"en": "English", "es": "Spanish", "pt": "Portuguese (Brazil)", "fr": "French", "de": "German", "ja": "Japanese",
         "ko": "Korean", "zh-Hans": "Chinese (Simplified)", "hi": "Hindi", "id": "Indonesian", "vi": "Vietnamese"}
BLOG = "https://acts39.blogspot.com"

def run(*a): subprocess.run([str(x) for x in a], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def panel_lines(p):
    out = []
    for it in p.get("items", []) + p.get("over", []):
        if it["t"] in ("say", "narr"): out.append(it["text"])
        elif it["t"] == "card": out.append(it["title"] + ": " + "; ".join(" ".join(r[:2]) if isinstance(r, list) else r for r in it["rows"]))
        elif it["t"] == "text": out.append(it["text"])
    return out

def band_svg(top, bottom):
    def t(x, y, s, size, weight, fill, anchor="middle", ls=0):
        return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter,Helvetica,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}" letter-spacing="{ls}">{html.escape(s)}</text>'
    lines = webtoon.wrap(top[1], 960, 46, True)[:2]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}">'
            f'<defs><linearGradient id="g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1424" stop-opacity="0.92"/><stop offset="1" stop-color="#0B1424" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="g2" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#0B1424" stop-opacity="0.92"/><stop offset="1" stop-color="#0B1424" stop-opacity="0"/></linearGradient></defs>'
            f'<rect width="{VW}" height="300" fill="url(#g1)"/><rect y="{VH-260}" width="{VW}" height="260" fill="url(#g2)"/>'
            + t(VW / 2, 92, top[0], 30, 800, "#7FD1A8", ls=6)
            + "".join(t(VW / 2, 158 + i * 56, l, 46, 800, "#FFFFFF") for i, l in enumerate(lines))
            + t(VW / 2, VH - 120, bottom, 34, 700, "#FFFFFF")
            + t(VW / 2, VH - 72, "Characters are fictional · art made with Google Gemini (AI)", 24, 500, "#C9D4E5")
            + '</svg>')

def gemini_json(prompt, model="gemini-3.1-pro-preview"):
    """Native Gemini API (x-goog-api-key) first, the OpenAI-compatible endpoint (Bearer) if that key is not set up."""
    try:
        body = json.dumps({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}}).encode()
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent", data=body,
                                     headers={"x-goog-api-key": "proxy-injected", "Content-Type": "application/json"})
        r = json.load(urllib.request.urlopen(req, timeout=600))
        txt = "".join(p.get("text", "") for p in r["candidates"][0]["content"]["parts"] if not p.get("thought"))
    except urllib.error.HTTPError as e:
        if e.code not in (400, 401, 403): raise
        body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}], "response_format": {"type": "json_object"}}).encode()
        req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", data=body,
                                     headers={"Authorization": "Bearer proxy-injected", "Content-Type": "application/json"})
        txt = json.load(urllib.request.urlopen(req, timeout=600))["choices"][0]["message"]["content"]
    return json.loads(re.sub(r"^```(json)?|```$", "", txt.strip(), flags=re.M))

def srt_time(t):
    ms = int(round(t * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"

def main(d, out, translate=True):
    d = pathlib.Path(d); out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    spec, blocks = webtoon.build(d, return_blocks=True); sid = spec["id"]
    yt = json.loads((d / "youtube.json").read_text(encoding="utf-8"))          # English title/description/hook written for this episode
    work = out / f"{sid}-work"; (work / "png").mkdir(parents=True, exist_ok=True)
    for f in (work / "png").glob("*"): f.unlink()
    # 1. every block (title card, panels, end card) as its own lettered image
    for i, (gap, h, svg, tr) in enumerate(blocks):
        (work / "png" / f"b{i:02d}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 {h}"><rect width="800" height="{h}" fill="#fff"/>{svg}</svg>', encoding="utf-8")
    (work / "png" / "band.svg").write_text(band_svg((f'VERDICT PICKS TOON · EP {sid[2:]}', spec["title"]), yt.get("band", "Full guide and sources: link in description")), encoding="utf-8")
    subprocess.run(["node", str(ROOT / "scripts" / "render_png.mjs"), str(work / "png")], check=True, stdout=subprocess.DEVNULL)
    subprocess.run(["node", str(ROOT / "scripts" / "render_png.mjs"), str(work / "png"), "band.svg"], check=True, stdout=subprocess.DEVNULL, env={**os.environ, "ALPHA": "1"})
    # 2. timing: reading time per panel, the whole Short under 59 s
    texts = [[f'{spec.get("series", "Verdict Picks Toon")}: {spec["title"]}']] + [panel_lines(p) for p in spec["panels"]] + [[spec.get("end", ""), "Link in description."]]
    dur = []
    for i, tx in enumerate(texts):
        n = sum(len(t) for t in tx)
        board = i and i <= len(spec["panels"]) and "art" not in spec["panels"][i - 1]
        dur.append(2.6 if i == 0 else 3.2 if i == len(texts) - 1 else min(6.2, max(4.4 if board else 2.4, 1.7 + 0.052 * n)))
    total = sum(dur) - XF * (len(dur) - 1)
    if total > 58.5: dur = [x * 58.5 / total for x in dur]; total = 58.5
    # 3. one clip per block: blurred art behind, the lettered panel pushing in, the top/bottom bands
    clips = []
    for i, D in enumerate(dur):
        png = work / "png" / f"b{i:02d}.png"; c = work / f"c{i:02d}.mp4"
        w, h = [int(v) for v in subprocess.run(["identify", "-format", "%w %h", str(png)], capture_output=True, text=True).stdout.split()]
        fw = 1000; fh = round(fw * h / w)
        if fh > 1340: fh = 1340; fw = round(fh * w / h)
        art = d / "toon-art" / f"{sid}-p{i:02d}.jpg"
        bg_in = ["-loop", "1", "-t", f"{D:.3f}", "-i", str(art if art.exists() else png)]
        fg = f"[1:v]scale={fw}:{fh},format=rgba,scale=w='trunc({fw}*(1+0.045*t/{D:.3f})/2)*2':h=-2:eval=frame[fg]"
        bg = f"[0:v]scale={VW}:{VH}:force_original_aspect_ratio=increase,crop={VW}:{VH},gblur=sigma=28,eq=brightness=-0.18:saturation=1.1[bg]"
        flt = f"{bg};{fg};[bg][fg]overlay=x='(W-w)/2':y='(H-h)/2+30':eval=frame[v1];[2:v]format=rgba,scale={VW}:{VH}[band];[v1][band]overlay=0:0,fps={FPS},format=yuv420p[v]"
        run(FF, "-y", *bg_in, "-loop", "1", "-t", f"{D:.3f}", "-i", png, "-loop", "1", "-t", f"{D:.3f}", "-i", work / "png" / "band.png",
            "-filter_complex", flt, "-map", "[v]", "-r", FPS, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", c)
        clips.append(c)
    # 4. crossfade the clips, add music
    ins = []; [ins.extend(["-i", str(c)]) for c in clips]
    chain, last, off = [], "[0:v]", 0.0
    for i in range(1, len(clips)):
        off += dur[i - 1] - XF
        chain.append(f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]"); last = f"[x{i}]"
    music = work / "music.wav"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "make_music.py"), str(music), str(int(total) + 2), str(yt.get("music_seed", 7))], check=True, stdout=subprocess.DEVNULL)
    mp4 = out / f"{sid}.mp4"
    run(FF, "-y", *ins, "-i", music, "-filter_complex", ";".join(chain) + f";[{len(clips)}:a]volume=0.55,afade=t=in:d=0.8,afade=t=out:st={total-1.6:.2f}:d=1.6[a]",
        "-map", last, "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-maxrate", "8M", "-bufsize", "12M",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", mp4)
    run(FF, "-y", "-ss", "1.2", "-i", mp4, "-frames:v", "1", "-q:v", "3", out / f"{sid}-thumb.jpg")
    # 5. subtitles and metadata in 11 languages
    starts, t = [], 0.0
    for D in dur: starts.append(t); t += D - XF
    cues = [(starts[i] + 0.15, starts[i] + dur[i] - XF, " ".join(tx)) for i, tx in enumerate(texts)]
    meta = {"en": {"title": yt["title"], "description": yt["description"]}}
    subs = {"en": [c[2] for c in cues]}
    if translate:
        for lang, name in LANGS.items():
            if lang == "en": continue
            r = gemini_json(f"Translate this YouTube Short's metadata and subtitles from English into {name}. Keep product names, model numbers, prices, "
                            f"units, URLs, hashtags and source names (CPSC, NFPA, CNET, ring.com) exactly as written; translate dates naturally; 'space heater' means an electric room heater; keep it natural and short, as a native "
                            f"speaker would write subtitles. Return JSON {{\"title\": str (max 100 characters, keep #Shorts), \"description\": str, \"subtitles\": [str, ...] "
                            f"(same count and order)}}.\n\n" + json.dumps({"title": yt["title"], "description": yt["description"], "subtitles": subs["en"]}, ensure_ascii=False))
            if len(r.get("subtitles", [])) != len(cues): raise SystemExit(f"{lang}: subtitle count mismatch")
            meta[lang] = {"title": r["title"][:100], "description": r["description"]}; subs[lang] = r["subtitles"]
            print("translated", lang)
    for lang, lines in subs.items():
        (out / f"{sid}.{lang}.srt").write_text("".join(f"{k+1}\n{srt_time(a)} --> {srt_time(b)}\n{line}\n\n" for k, ((a, b, _), line) in enumerate(zip(cues, lines))), encoding="utf-8")
    (out / f"{sid}-youtube.json").write_text(json.dumps({"video": mp4.name, "seconds": round(total, 1), "default_language": "en", "made_for_kids": False,
        "category": "Howto & Style", "altered_content": "No (stylised cartoon, not realistic)", "paid_promotion": False,
        "languages": LANGS, "metadata": meta}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    import shutil; shutil.rmtree(work, ignore_errors=True)
    print(f"{mp4} ({mp4.stat().st_size // 1024} KB, {total:.1f} s, {len(clips)} shots); subtitles: {', '.join(subs)}")

if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], "--no-translate" not in a)
