"""QA contact sheet for a rendered yadam video: grab one frame every N seconds and tile them.
Usage: python3 scripts/yadam_qa.py video/2026-09-yadam-manbok/yadam_manbok_1080p.mp4 out.png [--every 90] [--cols 6]
Also prints duration, resolution, fps and audio stream info from ffprobe.
"""
import argparse, json, os, pathlib, subprocess, tempfile
from PIL import Image

FF = os.environ.get("FFMPEG") or str(next(pathlib.Path("/tmp").glob("claude-0/*/*/scratchpad/ffm/node_modules/ffmpeg-static/ffmpeg"), "ffmpeg"))
FP = FF.replace("ffmpeg", "ffprobe") if FF.endswith("ffmpeg") else "ffprobe"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("out"); ap.add_argument("--every", type=float, default=90); ap.add_argument("--cols", type=int, default=6)
    a = ap.parse_args()
    info = json.loads(subprocess.run([FP, "-v", "error", "-show_format", "-show_streams", "-of", "json", a.video], capture_output=True, text=True).stdout)
    dur = float(info["format"]["duration"])
    for s in info["streams"]:
        print(s["codec_type"], s.get("codec_name"), s.get("width"), s.get("height"), s.get("r_frame_rate"), s.get("sample_rate"), s.get("channels"))
    print(f"duration {dur/60:.2f} min, size {int(info['format']['size'])/1e6:.0f} MB")
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
