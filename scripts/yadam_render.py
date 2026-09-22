"""Render the yadam animation: cut-out animation with ffmpeg from the parsed script, the narration timing,
the SVG-derived PNG assets (see yadam_art.py) and the synthesised audio (see yadam_music.py).

Per scene: world canvas 2400x1350 = background + props + characters (breathing/sway, blinking, mouth flaps while
that character's line is being narrated) + weather FX, then a slow camera move (zoom/pan) down to 1920x1080,
then large burned-in Korean subtitles (libass). Chapter/title cards are Pillow-composited PNGs with a slow zoom.
Clips are concatenated losslessly; the soundtrack (narration + music beds + ambience + stings) is mixed with numpy
and loudness-normalised at the final mux.

Usage: python3 scripts/yadam_render.py video/2026-09-yadam-manbok [--only 3] [--jobs 2] [--fps 24] [--preview]
  --only N     render only scene index N (0-based, across all chapters) and stop (for QA)
  --preview    720p, faster encode
Requires a full ffmpeg (FFMPEG env var or the ffmpeg-static binary in the session scratchpad).
"""
import argparse, json, math, os, pathlib, random, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np

FF = os.environ.get("FFMPEG") or str(next(pathlib.Path("/tmp").glob("claude-0/*/*/scratchpad/ffm/node_modules/ffmpeg-static/ffmpeg"), "ffmpeg"))
REPO = pathlib.Path(__file__).resolve().parent.parent
WW, WH = 2400, 1350            # world (composite) size
GROUND = 1262                  # world y of the characters' feet
CHAR_SCALE = 0.78              # stand sprite 1000 px -> 860 world px
FONT_DIR = "/usr/share/fonts/truetype/nanum"
FONT_SUB = "NanumSquareRound"
FONT_TITLE = f"{FONT_DIR}/NanumMyeongjoBold.ttf"
FONT_TITLE2 = f"{FONT_DIR}/NanumSquareRoundB.ttf"
BLINK_PERIOD, BLINK_LEN, MOUTH_PERIOD = 4.3, 0.16, 0.22


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.stderr.write(r.stderr[-4000:]); raise SystemExit(f"ffmpeg failed (rc={r.returncode}): {' '.join(map(str, cmd))[:300]}")
    return r


# ----------------------------------------------------------------------------- cards (Pillow)
def make_card(assets, out, title, sub=None, kind="chapter"):
    from PIL import Image, ImageDraw, ImageFont
    bg = Image.open(assets / "bg" / "title_card.png").convert("RGB").resize((1920, 1080), Image.LANCZOS)
    d = ImageDraw.Draw(bg)
    if kind == "title":
        f1, f2 = ImageFont.truetype(FONT_TITLE, 118), ImageFont.truetype(FONT_TITLE2, 54)
        _center(d, title, f1, 1920, 430, fill=(46, 32, 22), stroke=(255, 250, 238))
        if sub: _center(d, sub, f2, 1920, 610, fill=(110, 70, 40))
    else:
        f1, f2 = ImageFont.truetype(FONT_TITLE, 60), ImageFont.truetype(FONT_TITLE, 104)
        head, _, rest = title.partition(' ')
        if head.startswith('제') and head.endswith('장') or head.startswith('에필'):
            _center(d, head, f1, 1920, 400, fill=(150, 60, 40)); _center(d, rest or title, f2, 1920, 540, fill=(46, 32, 22), stroke=(255, 250, 238))
        else:
            _center(d, title, f2, 1920, 470, fill=(46, 32, 22), stroke=(255, 250, 238))
    bg.save(out)


def _center(d, text, font, W, y, fill, stroke=None):
    w = d.textlength(text, font=font)
    if stroke:
        d.text(((W - w) / 2, y), text, font=font, fill=fill, stroke_width=6, stroke_fill=stroke)
    else:
        d.text(((W - w) / 2, y), text, font=font, fill=fill)


def render_card(png, seconds, out, fps, W, H):
    n = int(seconds * fps)
    vf = (f"scale={2*W}:{2*H},zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={fps},"
          f"fade=t=in:st=0:d=0.8,fade=t=out:st={seconds-0.8}:d=0.8,format=yuv420p")
    sh([FF, "-y", "-loglevel", "error", "-loop", "1", "-t", str(seconds + 1), "-i", png, "-vf", vf, "-t", str(seconds),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(fps), "-an", out])


# ----------------------------------------------------------------------------- FX layers (Pillow)
def make_fx(kind, out):
    from PIL import Image, ImageDraw
    rnd = random.Random(11 if kind == "rain" else 12)
    img = Image.new("RGBA", (WW, WH), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    if kind == "rain":
        for _ in range(2600):
            x, y = rnd.randrange(WW), rnd.randrange(WH); L = rnd.randint(40, 90)
            d.line([(x, y), (x - 8, y + L)], fill=(220, 230, 255, rnd.randint(60, 120)), width=2)
    else:  # snow
        for _ in range(900):
            x, y, r = rnd.randrange(WW), rnd.randrange(WH), rnd.randint(3, 9)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, rnd.randint(120, 220)))
    img.save(out)


# ----------------------------------------------------------------------------- subtitles
def ass_header(W, H):
    size = 62 if H >= 1080 else 42
    return ("[Script Info]\nScriptType: v4.00+\nPlayResX: %d\nPlayResY: %d\nWrapStyle: 0\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Nar,%s,%d,&H00FFFFFF,&H000000FF,&H00101010,&H78000000,-1,0,0,0,100,100,0,0,3,3,0,2,120,120,58,1\n"
            "Style: Dlg,%s,%d,&H00F0FFFF,&H000000FF,&H00101010,&H78000000,-1,0,0,0,100,100,0,0,3,3,0,2,120,120,58,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n") % (W, H, FONT_SUB, size, FONT_SUB, size)


def ass_time(s):
    s = max(0.0, s); h = int(s // 3600); m = int(s % 3600 // 60); sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"


NAMES = {"manbok": "만복", "sunok": "순옥", "dolsoe": "돌쇠", "mother": "어머니", "kim_jinsa": "김 진사", "yongchil": "용칠", "eosa_ragged": "나그네",
         "eosa_official": "어사", "satto": "사또", "villager_m": "마을 남자", "villager_f": "마을 아낙", "merchant": "보부상", "grandpa_modern": "할아버지", "girl_modern": "손녀"}


def write_ass(scene, t0, path, W, H):
    ev = []
    for ln in scene["lines"]:
        for i, sb in enumerate(ln["subs"]):
            end = sb["end"] + (0.25 if i == len(ln["subs"]) - 1 else 0.0)
            txt = sb["text"].replace("\\", "").replace("{", "").replace("}", "")
            if ln["speaker"]:
                txt = f"{NAMES.get(ln['speaker'], ln['speaker'])} · " + txt if i == 0 else txt
            ev.append(f"Dialogue: 0,{ass_time(sb['start']-t0)},{ass_time(end-t0)},{'Dlg' if ln['speaker'] else 'Nar'},,0,0,0,,{txt}")
    path.write_text(ass_header(W, H) + "\n".join(ev) + "\n", encoding="utf-8")


# ----------------------------------------------------------------------------- scene graph
def sprite_path(assets, man, name, pose, mouth, eyes):
    c = man["char"][name]
    if pose not in c["poses"]:
        pose = "stand" if "stand" in c["poses"] else next(iter(c["poses"]))
    p = c["poses"][pose]
    return assets / p["states"][f"{mouth}_{eyes}"], p["w"], p["h"], pose


def sprite_sheet(assets, man, name, pose, flip, work):
    """4 states side by side: 0 closed/open, 1 open/open, 2 closed/closed, 3 open/closed (mouth/eyes)."""
    from PIL import Image
    _, sw, sh_, pose = sprite_path(assets, man, name, pose, "closed", "open")
    out = work / f"sheet_{name}_{pose}_{'f' if flip else 'n'}.png"
    if not out.exists():
        sheet = Image.new("RGBA", (4 * sw, sh_), (0, 0, 0, 0))
        for i, (m, e) in enumerate([("closed", "open"), ("open", "open"), ("closed", "closed"), ("open", "closed")]):
            im = Image.open(sprite_path(assets, man, name, pose, m, e)[0]).convert("RGBA")
            if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
            sheet.paste(im, (i * sw, 0))
        sheet.save(out)
    return out, sw, sh_, pose


def camera_filter(cam, D, W, H):
    """world (2400x1350) -> WxH with a slow move. Zoom uses per-frame scale, pan uses a moving crop."""
    base = W / WW                       # scale that shows the whole world
    zin = 1.22
    if cam == "zoomin":
        s = f"{base}*(1+{zin-1}*min(t/{D},1))"
    elif cam == "zoomout":
        s = f"{base}*({zin}-{zin-1}*min(t/{D},1))"
    elif cam in ("panleft", "panright"):
        s = f"{base}*{zin}"
    else:
        s = f"{base}*(1+0.05*min(t/{D},1))"
    f = f"scale=w='trunc({WW}*{s}/2)*2':h='trunc({WH}*{s}/2)*2':eval=frame:flags=bicubic"
    # the crop window sits low in the world (y bias 0.78) so the characters' feet stay in frame when zoomed
    if cam == "panleft":
        f += f",crop={W}:{H}:x='(iw-{W})*(1-min(t/{D},1))':y='(ih-{H})*0.86'"
    elif cam == "panright":
        f += f",crop={W}:{H}:x='(iw-{W})*min(t/{D},1)':y='(ih-{H})*0.86'"
    else:
        f += f",crop={W}:{H}:x='(iw-{W})/2':y='(ih-{H})*0.86'"
    return f


def ease(u):
    u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)


def camera_window(cam, t, D, W, H):
    """Return the world-space crop box (x0, y0, x1, y1) for time t; s = world->output scale."""
    base = W / WW; zin = 1.22; u = ease(t / D)
    if cam == "zoomin": s = base * (1 + (zin - 1) * u)
    elif cam == "zoomout": s = base * (zin - (zin - 1) * u)
    elif cam in ("panleft", "panright"): s = base * zin
    else: s = base * (1 + 0.05 * u)
    w, h = W / s, H / s
    if cam == "panleft": x0 = (WW - w) * (1 - u)
    elif cam == "panright": x0 = (WW - w) * u
    else: x0 = (WW - w) / 2
    y0 = (WH - h) * 0.86
    return (x0, y0, x0 + w, y0 + h)


def build_scene(scene, idx, root, assets, man, out, fps, W, H):
    """Composite every frame with Pillow (base world image + animated sprites + weather), apply the camera crop,
    and pipe raw RGB frames into ffmpeg for fades, burned-in subtitles and H.264 encoding."""
    from PIL import Image
    D = scene["end"] - scene["start"]; t0 = scene["start"]
    work = root / "build" / "work"; work.mkdir(parents=True, exist_ok=True); pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    base = Image.open(assets / man["bg"][scene["bg"]]["file"]).convert("RGBA").resize((WW, WH), Image.BICUBIC)
    for p in scene.get("props", []):
        if p["name"] not in man["prop"]:
            continue
        m = man["prop"][p["name"]]
        im = Image.open(assets / m["file"]).convert("RGBA")
        w, h = max(1, int(m["w"] * p["scale"])), max(1, int(m["h"] * p["scale"]))
        im = im.resize((w, h), Image.BICUBIC)
        base.paste(im, (int(p["x"] * WW - w / 2), int(p["y"] * WH - h / 2)), im)
    rnd = random.Random(idx); chars = []
    for ci, c in enumerate(scene.get("chars", [])):
        if c["name"] not in man["char"]:
            continue
        _, sw, shh, pose = sprite_path(assets, man, c["name"], c["pose"], "closed", "open")
        w, h = int(sw * CHAR_SCALE), int(shh * CHAR_SCALE)
        states = []
        for m, e in [("closed", "open"), ("open", "open"), ("closed", "closed"), ("open", "closed")]:
            im = Image.open(sprite_path(assets, man, c["name"], c["pose"], m, e)[0]).convert("RGBA").resize((w, h), Image.BICUBIC)
            if c.get("flip"): im = im.transpose(Image.FLIP_LEFT_RIGHT)
            states.append(im)
        chars.append({"states": states, "bx": c["x"] * WW - w / 2, "by": GROUND - h,
                      "talks": [(ln["start"] - t0, ln["end"] - t0) for ln in scene["lines"] if ln["speaker"] == c["name"]],
                      "blink_ph": rnd.uniform(0, BLINK_PERIOD), "bob": (9, 0.55) if pose == "walk" else (4, 3.1 + 0.3 * ci),
                      "sway_per": 4.6 + 0.4 * ci, "ph": ci})
    fx = scene.get("fx", "none"); fx_im = None
    if fx in ("rain", "snow"):
        fxp = work / f"fx_{fx}.png"
        if not fxp.exists():
            make_fx(fx, fxp)
        fx_im = Image.open(fxp).convert("RGBA"); fx_speed = 1500 if fx == "rain" else 140
    ass = work / f"scene{idx:03d}.ass"; write_ass(scene, t0, ass, W, H)
    n_frames = int(round(D * fps))
    vf = f"fade=t=in:st=0:d=0.7,fade=t=out:st={max(0.0, D-0.7):.2f}:d=0.7,ass='{ass}':fontsdir={FONT_DIR},format=yuv420p"
    cmd = [FF, "-y", "-loglevel", "error", "-threads", "2", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
           "-vf", vf, "-frames:v", str(n_frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-tune", "animation", "-pix_fmt", "yuv420p", "-r", str(fps), "-an", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for n in range(n_frames):
            t = n / fps
            frame = base.copy()
            for c in chars:
                talking = any(a <= t <= b for a, b in c["talks"])
                mouth = 1 if talking and (t % MOUTH_PERIOD) < MOUTH_PERIOD / 2 else 0
                blink = 1 if ((t + c["blink_ph"]) % BLINK_PERIOD) < BLINK_LEN else 0
                im = c["states"][mouth + 2 * blink]
                x = c["bx"] + 3 * math.sin(2 * math.pi * t / c["sway_per"] + c["ph"])
                y = c["by"] + c["bob"][0] * math.sin(2 * math.pi * t / c["bob"][1] + c["ph"])
                frame.paste(im, (int(x), int(y)), im)
            if fx_im is not None:
                yy = (t * fx_speed) % WH; xx = 0 if fx == "rain" else int(40 * math.sin(2 * math.pi * t / 6))
                frame.paste(fx_im, (xx, int(yy) - WH), fx_im); frame.paste(fx_im, (xx, int(yy)), fx_im)
            box = camera_window(scene["cam"], t, D, W, H)
            outim = frame.convert("RGB").resize((W, H), Image.BICUBIC, box=box)
            try:
                proc.stdin.write(outim.tobytes())
            except BrokenPipeError:
                break
    finally:
        proc.stdin.close()
    err = proc.stderr.read().decode(errors="replace"); proc.wait()
    if proc.returncode:
        sys.stderr.write(err[-3000:]); raise SystemExit(f"ffmpeg failed (rc={proc.returncode}) on scene {idx}")
    return out


# ----------------------------------------------------------------------------- audio
def build_audio(timing, audio_dir, narration, out):
    import soundfile as sf
    SR = 44100
    nar, sr = sf.read(narration, dtype="float32")
    if sr != SR:
        tmp = narration.with_name("narration44.wav")
        sh([FF, "-y", "-loglevel", "error", "-i", str(narration), "-ar", str(SR), "-ac", "1", str(tmp)]); nar, sr = sf.read(tmp, dtype="float32")
    total = timing["total"] + 3.0
    N = int(total * SR); mix = np.zeros((N, 2), np.float32)
    mix[:len(nar), 0] = nar[:N]; mix[:len(nar), 1] = nar[:N]
    def load(name):
        p = audio_dir / name
        if not p.exists():
            return None
        x, s = sf.read(p, dtype="float32")
        if x.ndim == 1: x = np.stack([x, x], 1)
        if s != SR:
            tmp = p.with_name(p.stem + "_44.wav"); sh([FF, "-y", "-loglevel", "error", "-i", str(p), "-ar", str(SR), str(tmp)]); x, _ = sf.read(tmp, dtype="float32")
            if x.ndim == 1: x = np.stack([x, x], 1)
        return x
    def place(x, start, dur, gain, fade=2.5, loop=True):
        if x is None: return
        s0 = int(start * SR); n = int(dur * SR)
        seg = np.tile(x, (n // len(x) + 2, 1))[:n] if loop else x[:n]
        n = len(seg); env = np.ones(n, np.float32); f = min(int(fade * SR), n // 2)
        if f > 0:
            env[:f] = np.linspace(0, 1, f); env[-f:] = np.linspace(1, 0, f)
        mix[s0:s0 + n] += seg * (env[:, None] * gain)
    beds = {k: load(f"bed_{k}.wav") for k in ("calm", "tense", "warm")}
    ambs = {k: load(f"amb_{k}.wav") for k in ("day", "night", "rain", "market", "river", "winter", "room", "park_modern")}
    st_intro, st_chap, st_end = load("sting_intro.wav"), load("sting_chapter.wav"), load("sting_end.wav")
    # runs of identical music / ambience keys across scenes
    segs = []
    for ch in timing["chapters"]:
        if ch.get("card"):
            segs.append(("card", ch["card"][0], ch["card"][1], None, None))
        for sc in ch["scenes"]:
            segs.append(("scene", sc["start"], sc["end"], sc.get("music", "calm"), sc.get("amb", "none")))
    def runs(key_idx):
        out, cur = [], None
        for s in segs:
            k = s[key_idx]
            if cur and cur[0] == k and s[0] == "scene": cur[2] = s[2]
            elif s[0] == "scene": cur = [k, s[1], s[2]]; out.append(cur)
            elif cur: cur[2] = s[2]  # cards extend the running bed
        return out
    for k, a, b in runs(3):
        if k in beds: place(beds[k], a, b - a, 0.10 if k != "tense" else 0.11, fade=3.0)
    for k, a, b in runs(4):
        if k in ambs: place(ambs[k], a, b - a, 0.16, fade=2.0)
    for ch in timing["chapters"]:
        if ch.get("card"): place(st_chap, ch["card"][0] + 0.3, 4.0, 0.5, fade=0.2, loop=False)
        for sc in ch["scenes"]:
            if sc.get("kind") == "title": place(st_intro, sc["card"][0], 8.0, 0.6, fade=0.2, loop=False)
    place(st_end, timing["total"] - 8.0, 10.0, 0.5, fade=0.2, loop=False)
    peak = np.abs(mix).max()
    if peak > 0.98: mix *= 0.98 / peak
    sf.write(out, mix, SR)
    return out


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--only", type=int, default=-1); ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--fps", type=int, default=24); ap.add_argument("--seconds", type=float, default=0, help="with --only: render only the first N seconds"); ap.add_argument("--preview", action="store_true"); ap.add_argument("--audio-dir", default="")
    a = ap.parse_args()
    root = pathlib.Path(a.root); assets = root / "assets"; build = root / "build"; clips = build / ("clips720" if a.preview else "clips"); clips.mkdir(parents=True, exist_ok=True)
    W, H = (1280, 720) if a.preview else (1920, 1080)
    man = json.loads((assets / "manifest.json").read_text(encoding="utf-8"))
    timing = json.loads((build / "timing.json").read_text(encoding="utf-8"))
    audio_dir = pathlib.Path(a.audio_dir) if a.audio_dir else build / "audio"
    # flatten into an ordered list of clips
    items = []
    for ch in timing["chapters"]:
        if ch.get("card"):
            items.append({"kind": "card", "title": ch["title"], "start": ch["card"][0], "end": ch["card"][1]})
        for sc in ch["scenes"]:
            if sc.get("kind") == "title":   # the title card covers the whole title scene (it has no narration)
                items.append({"kind": "title", "title": sc["title"], "sub": sc["sub"], "start": sc["start"], "end": sc["end"]}); continue
            items.append({"kind": "scene", "scene": sc, "start": sc["start"], "end": sc["end"]})
    scene_idx = [i for i, it in enumerate(items) if it["kind"] == "scene"]
    if a.only >= 0:
        it = items[scene_idx[a.only]]; out = clips / f"scene_{a.only:03d}.mp4"; sc = it["scene"]
        if a.seconds:
            sc = {**sc, "end": min(sc["end"], sc["start"] + a.seconds)}
        build_scene(sc, a.only, root, assets, man, out, a.fps, W, H); print("wrote", out); return
    def do(i):
        it = items[i]; out = clips / f"clip_{i:03d}.mp4"
        if out.exists() and out.stat().st_size > 1000:
            return out
        if it["kind"] in ("card", "title"):
            png = build / "work" / f"card_{i:03d}.png"; png.parent.mkdir(exist_ok=True, parents=True)
            make_card(assets, png, it["title"], it.get("sub"), kind=it["kind"]); render_card(str(png), it["end"] - it["start"], str(out), a.fps, W, H)
        else:
            build_scene(it["scene"], scene_idx.index(i), root, assets, man, out, a.fps, W, H)
        print(f"clip {i:03d} {it['kind']} {it['end']-it['start']:.1f}s done", flush=True); return out
    with ThreadPoolExecutor(a.jobs) as ex:
        outs = list(ex.map(do, range(len(items))))
    lst = build / "concat.txt"; lst.write_text("".join(f"file '{o.resolve()}'\n" for o in outs), encoding="utf-8")
    silent = build / ("video_silent720.mp4" if a.preview else "video_silent.mp4")
    sh([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(silent)])
    mixwav = build / "mix.wav"
    if not mixwav.exists():
        build_audio(timing, audio_dir, build / "narration.wav", mixwav)
    final = root / ("yadam_manbok_720p.mp4" if a.preview else "yadam_manbok_1080p.mp4")
    sh([FF, "-y", "-loglevel", "error", "-i", str(silent), "-i", str(mixwav), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(final)])
    print("final:", final)


if __name__ == "__main__":
    main()
