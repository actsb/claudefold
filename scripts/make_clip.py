"""Cut a short, silent-source, music-backed, English-captioned clip from a raw video (no player chrome, no Korean).
Usage:
  python3 scripts/make_clip.py IN.mp4 OUT_BASENAME --start 12 --end 20 --caption "Live from the fur zone" \
      [--sub "Every hair here has a couch in its future"] [--orient landscape|portrait] [--music music.wav] [--speed 1.0]
Writes OUT_BASENAME.mp4 (H.264, AAC, faststart, ~1.5 Mbps) and OUT_BASENAME.jpg (poster).
Requires a full ffmpeg (set FFMPEG env var; defaults to the ffmpeg-static binary in the session scratchpad).
"""
import argparse, os, pathlib, subprocess, sys
FF = os.environ.get("FFMPEG") or str(next(pathlib.Path("/tmp").glob("claude-0/*/*/scratchpad/ffm/node_modules/ffmpeg-static/ffmpeg"), "ffmpeg"))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def esc(s):  # drawtext escaping
    return s.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--start", type=float, default=0); ap.add_argument("--end", type=float, required=True)
    ap.add_argument("--caption", required=True); ap.add_argument("--sub", default="")
    ap.add_argument("--orient", default="landscape"); ap.add_argument("--music", default=""); ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--crop", default="", help="optional W:H:X:Y crop in source pixels before scaling (e.g. to cut a burned-in caption)")
    a = ap.parse_args()
    dur = (a.end - a.start) / a.speed
    W, H = (1280, 720) if a.orient == "landscape" else (720, 1280)
    vf = []
    if a.crop: vf.append(f"crop={a.crop}")
    if a.speed != 1.0: vf.append(f"setpts=PTS/{a.speed}")
    vf.append(f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}")
    # caption band: rendered from SVG to a transparent PNG with Chromium (this ffmpeg build has no drawtext), then overlaid
    size = 44 if a.orient == "landscape" else 40; sub_size = 30 if a.orient == "landscape" else 28
    band_h = 190 if a.sub else 130
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{band_h}" viewBox="0 0 {W} {band_h}">'
           f'<rect width="{W}" height="{band_h}" fill="#000" fill-opacity="0.45"/>'
           f'<text x="{W/2}" y="{62 if a.sub else 80}" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="{size}" font-weight="800" fill="#fff" style="paint-order:stroke" stroke="#000" stroke-opacity="0.35" stroke-width="3">{a.caption.replace("&","&amp;").replace("<","&lt;")}</text>'
           + (f'<text x="{W/2}" y="{band_h-46}" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif" font-size="{sub_size}" fill="#E6E9EE">{a.sub.replace("&","&amp;").replace("<","&lt;")}</text>' if a.sub else "")
           + f'<rect x="{W/2-40}" y="{band_h-16}" width="80" height="5" rx="2.5" fill="#1E8E5A"/></svg>')
    band_dir = pathlib.Path(a.out).parent / "_band"; band_dir.mkdir(parents=True, exist_ok=True)
    (band_dir / "band.svg").write_text(svg, encoding="utf-8")
    repo = pathlib.Path(__file__).resolve().parent.parent
    subprocess.run(["node", str(repo / "scripts" / "render_png.mjs"), str(band_dir)], check=True, capture_output=True)
    band_png = band_dir / "band.png"   # render_png writes at 2x; scale it back in the filter graph
    vf.append(f"fade=t=in:st=0:d=0.4,fade=t=out:st={max(0, dur-0.5):.2f}:d=0.5,format=yuv420p")
    pre = vf[:-1]; post = vf[-1]   # everything before the fade, then fade/format after the overlay
    cmd = [FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(a.start), "-t", str(a.end - a.start), "-i", a.inp, "-i", str(band_png)]
    graph = f"[0:v]{','.join(pre)}[base];[1:v]scale={W}:{band_h}[band];[base][band]overlay=0:{H-band_h},{post}[v]"
    if a.music:
        cmd += ["-stream_loop", "-1", "-i", a.music]
        af = f"[2:a]volume=0.9,afade=t=in:st=0:d=0.6,afade=t=out:st={max(0, dur-0.8):.2f}:d=0.8,atrim=0:{dur:.2f}[m]"
        cmd += ["-filter_complex", graph + ";" + af, "-map", "[v]", "-map", "[m]", "-c:a", "aac", "-b:a", "96k", "-shortest"]
    else:
        cmd += ["-filter_complex", graph, "-map", "[v]", "-an"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "23", "-r", "30", "-movflags", "+faststart", "-t", f"{dur:.2f}", a.out + ".mp4"]
    subprocess.run(cmd, check=True)
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", "0.6", "-i", a.out + ".mp4", "-frames:v", "1", "-q:v", "3", a.out + ".jpg"], check=True)
    print("wrote", a.out + ".mp4", os.path.getsize(a.out + ".mp4") // 1024, "KB and", a.out + ".jpg")

if __name__ == "__main__":
    main()
