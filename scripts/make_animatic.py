"""Build a short 'animatic' from a shot list: stills with slow zoom/pan (Ken Burns), our own clips, and SVG end cards,
each with an English caption band, cross-faded, over music synthesised by make_music.py. No people, no on-screen Korean.
Usage: python3 scripts/make_animatic.py shots.json OUT_BASENAME [--orient portrait|landscape] [--music music.wav]
shots.json: {"shots": [{"image": "path.jpg" | "video": "path.mp4" | "svg": "path.svg", "start": 0, "seconds": 4,
                        "caption": "SHOT 1 · HERO", "sub": "what happens", "motion": "zoomin|zoomout|panleft|panright|none"}]}
Writes OUT_BASENAME.mp4 (H.264, AAC, faststart) and OUT_BASENAME.jpg (poster from the first shot).
"""
import argparse, json, os, pathlib, shutil, subprocess
FF = os.environ.get("FFMPEG") or str(next(pathlib.Path("/tmp").glob("claude-0/*/*/scratchpad/ffm/node_modules/ffmpeg-static/ffmpeg"), "ffmpeg"))
REPO = pathlib.Path(__file__).resolve().parent.parent
FONT = "-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"
FPS, XF = 30, 0.5

def x(s): return s.replace("&", "&amp;").replace("<", "&lt;")

def band_svg(W, caption, sub):
    size, sub_size = (44, 30) if W > 1000 else (40, 28)
    h = 190 if sub else 130
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}"><rect width="{W}" height="{h}" fill="#000" fill-opacity="0.45"/>'
            f'<text x="{W/2}" y="{62 if sub else 80}" text-anchor="middle" font-family="{FONT}" font-size="{size}" font-weight="800" fill="#fff" style="paint-order:stroke" stroke="#000" stroke-opacity="0.35" stroke-width="3">{x(caption)}</text>'
            + (f'<text x="{W/2}" y="{h-46}" text-anchor="middle" font-family="{FONT}" font-size="{sub_size}" fill="#E6E9EE">{x(sub)}</text>' if sub else "")
            + f'<rect x="{W/2-40}" y="{h-16}" width="80" height="5" rx="2.5" fill="#1E8E5A"/></svg>'), h

def motion_filter(kind, secs, W, H):
    n = int(secs * FPS)
    if kind == "none":
        return f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},trim=duration={secs},setpts=PTS-STARTPTS"
    z = {"zoomin": f"1+0.18*on/{n}", "zoomout": f"1.18-0.18*on/{n}", "panleft": "1.18", "panright": "1.18"}[kind]
    px = {"panleft": f"(iw-iw/zoom)*(1-on/{n})", "panright": f"(iw-iw/zoom)*on/{n}"}.get(kind, "iw/2-(iw/zoom/2)")
    # oversample 2x so the zoom does not shimmer, then zoompan at the output size
    return (f"scale={2*W}:{2*H}:force_original_aspect_ratio=increase,crop={2*W}:{2*H},"
            f"zoompan=z='{z}':x='{px}':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},trim=duration={secs},setpts=PTS-STARTPTS")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("shots"); ap.add_argument("out")
    ap.add_argument("--orient", default="portrait"); ap.add_argument("--music", default="")
    a = ap.parse_args()
    W, H = (720, 1280) if a.orient == "portrait" else (1280, 720)
    spec = json.loads(pathlib.Path(a.shots).read_text(encoding="utf-8")); shots = spec["shots"]
    work = pathlib.Path(a.out).parent / "_anim"; shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
    # caption bands and SVG cards are rasterised with Chromium (this ffmpeg has no drawtext)
    bands = []
    for i, s in enumerate(shots):
        svg, h = band_svg(W, s.get("caption", ""), s.get("sub", ""))
        (work / f"band{i}.svg").write_text(svg, encoding="utf-8"); bands.append(h)
        if s.get("svg"): shutil.copy(s["svg"], work / f"card{i}.svg")
    subprocess.run(["node", str(REPO / "scripts" / "render_png.mjs"), str(work)], check=True, capture_output=True)
    inputs, chains, total = [], [], 0.0
    for i, s in enumerate(shots):
        secs = float(s.get("seconds", 4)); total += secs
        if s.get("video"):
            inputs += ["-ss", str(s.get("start", 0)), "-t", str(secs), "-i", s["video"]]
            vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},trim=duration={secs},setpts=PTS-STARTPTS"
        else:
            src = str(work / f"card{i}.png") if s.get("svg") else s["image"]
            inputs += ["-loop", "1", "-t", str(secs + 1), "-i", src]
            vf = motion_filter(s.get("motion", "none" if s.get("svg") else "zoomin"), secs, W, H)
        inputs += ["-i", str(work / f"band{i}.png")]
        vi, bi = 2 * i, 2 * i + 1
        chains.append(f"[{vi}:v]{vf}[s{i}];[{bi}:v]scale={W}:{bands[i]}[b{i}];[s{i}][b{i}]overlay=0:{H-bands[i]}:format=auto,fps={FPS},format=yuv420p[c{i}]")
    # cross-fades: each transition eats XF seconds
    cur, off = "c0", 0.0
    for i in range(1, len(shots)):
        off += float(shots[i-1].get("seconds", 4)) - XF
        chains.append(f"[{cur}][c{i}]xfade=transition=fade:duration={XF}:offset={off:.2f}[x{i}]"); cur = f"x{i}"
    dur = total - XF * (len(shots) - 1)
    chains.append(f"[{cur}]fade=t=in:st=0:d=0.4,fade=t=out:st={dur-0.6:.2f}:d=0.6[v]")
    cmd = [FF, "-hide_banner", "-loglevel", "error", "-y"] + inputs
    if a.music:
        cmd += ["-stream_loop", "-1", "-i", a.music]
        mi = 2 * len(shots)
        chains.append(f"[{mi}:a]volume=0.9,afade=t=in:st=0:d=0.6,afade=t=out:st={dur-0.9:.2f}:d=0.9,atrim=0:{dur:.2f}[m]")
        cmd += ["-filter_complex", ";".join(chains), "-map", "[v]", "-map", "[m]", "-c:a", "aac", "-b:a", "96k"]
    else:
        cmd += ["-filter_complex", ";".join(chains), "-map", "[v]", "-an"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "23", "-r", str(FPS), "-movflags", "+faststart", "-t", f"{dur:.2f}", a.out + ".mp4"]
    subprocess.run(cmd, check=True)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", "0.8", "-i", a.out + ".mp4", "-frames:v", "1", "-q:v", "3", a.out + ".jpg"], check=True)
    shutil.rmtree(work, ignore_errors=True)
    print("wrote", a.out + ".mp4", os.path.getsize(a.out + ".mp4") // 1024, "KB,", f"{dur:.1f}s, and", a.out + ".jpg")

if __name__ == "__main__":
    main()
