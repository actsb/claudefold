"""One-command build of the yadam video on any machine (Windows PC or Linux):
  python scripts/yadam_build.py video/2026-09-yadam-manbok            # everything that is missing or stale
  python scripts/yadam_build.py video/2026-09-yadam-manbok --from tts  # redo from a step: art|music|script|tts|render|thumb|qa
  python scripts/yadam_build.py video/2026-09-yadam-manbok --setup     # download ffmpeg (Windows) + the TTS model into tools/ and models/
Steps: art (SVG -> PNG via Playwright Chromium) -> music (synth) -> script (parse) -> tts (Supertonic 3 cast) -> render (1080p mp4)
       -> thumb -> qa. Outputs stay under <root>/build and <root>/*.mp4 (git-ignored); sources are in git.
"""
import argparse, pathlib, subprocess, sys, tarfile, urllib.request, zipfile, shutil, os
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import yadam_env

PY = sys.executable
STEPS = ["art", "music", "script", "tts", "render", "thumb", "qa"]


def run(cmd):
    print("$", " ".join(map(str, cmd)), flush=True)
    r = subprocess.run(cmd)
    if r.returncode:
        sys.exit(f"step failed (rc={r.returncode})")


def download(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    print("downloading", url, "->", dest, flush=True)
    urllib.request.urlretrieve(url, dest)


def setup():
    yadam_env.MODELS.mkdir(exist_ok=True); yadam_env.TOOLS.mkdir(exist_ok=True)
    if not yadam_env.model_dir(yadam_env.ST3_NAME):
        f = yadam_env.MODELS / (yadam_env.ST3_NAME + ".tar.bz2"); download(yadam_env.ST3_URL, f)
        with tarfile.open(f) as t: t.extractall(yadam_env.MODELS)
        f.unlink()
    if yadam_env.WIN and not (shutil.which("ffmpeg") or os.environ.get("FFMPEG") or (yadam_env.TOOLS / "ffmpeg" / "bin" / "ffmpeg.exe").exists()):
        z = yadam_env.TOOLS / "ffmpeg.zip"; download("https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip", z)
        with zipfile.ZipFile(z) as zf: zf.extractall(yadam_env.TOOLS / "_ff")
        inner = next((yadam_env.TOOLS / "_ff").glob("ffmpeg-*")); shutil.move(str(inner), str(yadam_env.TOOLS / "ffmpeg")); shutil.rmtree(yadam_env.TOOLS / "_ff"); z.unlink()
    if yadam_env.WIN and not (yadam_env.FONTS / "NanumSquareRoundB.ttf").exists():
        print("fonts: put NanumSquareRoundB.ttf, NanumSquareB.ttf, NanumMyeongjoBold.ttf into fonts/ (free from hangeul.naver.com);"
              " without them Windows' Malgun Gothic is used automatically.")
    run([PY, "-m", "pip", "install", "-q", "sherpa-onnx", "soundfile", "numpy", "pillow"])
    run([PY, str(yadam_env.REPO / "scripts" / "yadam_env.py")])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("root"); ap.add_argument("--from", dest="frm", default=""); ap.add_argument("--setup", action="store_true")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 4) - 1)); a = ap.parse_args()
    if a.setup:
        setup(); return
    root = pathlib.Path(a.root); S = yadam_env.REPO / "scripts"; build = root / "build"
    start = STEPS.index(a.frm) if a.frm else None
    def need(step, outputs):
        if start is not None: return STEPS.index(step) >= start
        return not all(pathlib.Path(o).exists() for o in outputs)
    if need("art", [root / "assets" / "manifest.json"]): run([PY, S / "yadam_art.py", root / "assets"])
    if need("music", [build / "audio" / "bed_calm.wav"]): run([PY, S / "yadam_music.py", build / "audio"])
    if need("script", [build / "script.json"]) or start is None: run([PY, S / "yadam_script.py", root])
    if need("tts", [build / "narration.wav", build / "timing.json"]) or start is None: run([PY, S / "yadam_tts.py", root, "--engine", "supertonic", "--speed", "0.9"])
    if need("render", [root / "yadam_manbok_1080p.mp4"]):
        if start is not None and start <= STEPS.index("render"):
            shutil.rmtree(build / "clips", ignore_errors=True); (build / "mix.wav").unlink(missing_ok=True)
        run([PY, S / "yadam_render.py", root, "--jobs", str(a.jobs)])
    if need("thumb", [root / "thumbnail.png"]): run([PY, S / "yadam_thumbnail.py", root, "--variant", "a", "--out", "thumbnail.png"])
    if need("qa", [root / "qa_sheet.png"]): run([PY, S / "yadam_qa.py", root / "yadam_manbok_1080p.mp4", root / "qa_sheet.png", "--every", "100"])
    print("done:", root / "yadam_manbok_1080p.mp4")


if __name__ == "__main__":
    main()
