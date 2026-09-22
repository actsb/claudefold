"""QA contact sheet for a rendered yadam video: grab one frame every N seconds and tile them.
Usage: python3 scripts/yadam_qa.py video/2026-09-yadam-manbok/yadam_manbok_1080p.mp4 out.png [--every 90] [--cols 6]
Also prints duration, resolution, fps and audio stream info from ffprobe.
"""
import argparse, json, os, pathlib, subprocess, tempfile
from PIL import Image

FF = os.environ.get("FFMPEG") or str(next(pathlib.Path("/tmp").glob("claude-0/*/*/scratchpad/ffm/node_modules/ffmpeg-static/ffmpeg"), "ffmpeg"))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("out"); ap.add_argument("--every", type=float, default=90); ap.add_argument("--cols", type=int, default=6)
    a = ap.parse_args()
    # this ffmpeg-static build ships no ffprobe: read Duration/Stream lines from `ffmpeg -i`
    import re
    err = subprocess.run([FF, "-hide_banner", "-i", a.video], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err); dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    for line in err.splitlines():
        if "Stream #" in line: print(line.strip())
    print(f"duration {dur/60:.2f} min, size {os.path.getsize(a.video)/1e6:.0f} MB")
    times = [t for t in [i * a.every for i in range(int(dur // a.every) + 1)] if t < dur]
    tw, th = 320, 180; rows = (len(times) + a.cols - 1) // a.cols
    sheet = Image.new("RGB", (a.cols * tw, rows * th), (0, 0, 0))
    with tempfile.TemporaryDirectory() as td:
        for i, t in enumerate(times):
            f = pathlib.Path(td) / f"{i}.jpg"
            subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(t), "-i", a.video, "-frames:v", "1", "-vf", f"scale={tw}:{th}", str(f)], check=True)
            sheet.paste(Image.open(f), ((i % a.cols) * tw, (i // a.cols) * th))
    sheet.save(a.out); print("wrote", a.out, len(times), "frames")


if __name__ == "__main__":
    main()
