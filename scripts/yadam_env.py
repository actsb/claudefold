"""Where the yadam pipeline finds its tools on any machine (Linux cloud session or a Windows PC).

Resolution order for everything: environment variable -> project-local folder (tools/, models/, fonts/ under the
repo root, all git-ignored) -> the cloud session's scratchpad -> the system (PATH, C:\\Windows\\Fonts, /usr/share/fonts).
Run `python3 scripts/yadam_env.py` to print what was found and what is missing.
"""
import os, pathlib, shutil, sys

REPO = pathlib.Path(__file__).resolve().parent.parent
TOOLS, MODELS, FONTS = REPO / "tools", REPO / "models", REPO / "fonts"
ST3_NAME = "sherpa-onnx-supertonic-3-tts-int8-2026-05-11"
ST3_URL = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/{ST3_NAME}.tar.bz2"
MIMIC_NAME = "vits-mimic3-ko_KO-kss_low"
MIMIC_URL = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/{MIMIC_NAME}.tar.bz2"
WIN = sys.platform.startswith("win")


def _first(paths):
    for p in paths:
        if p and pathlib.Path(p).exists():
            return pathlib.Path(p)
    return None


def ffmpeg():
    exe = "ffmpeg.exe" if WIN else "ffmpeg"
    p = _first([os.environ.get("FFMPEG"), TOOLS / "ffmpeg" / "bin" / exe, TOOLS / "ffmpeg" / exe, TOOLS / exe]
               + sorted(pathlib.Path("/tmp").glob("claude-0/*/*/scratchpad/ffm/node_modules/ffmpeg-static/ffmpeg")))
    return str(p) if p else (shutil.which("ffmpeg") or "ffmpeg")


def model_dir(name):
    env = {ST3_NAME: "YADAM_ST3_MODEL", MIMIC_NAME: "YADAM_TTS_MODEL"}.get(name)
    return _first([os.environ.get(env) if env else None, MODELS / name] + sorted(pathlib.Path("/tmp").glob(f"claude-0/*/*/scratchpad/tts/{name}")))


def font_dir():
    """Folder that holds the Nanum fonts (used for libass fontsdir)."""
    return _first([os.environ.get("YADAM_FONT_DIR"), FONTS, "/usr/share/fonts/truetype/nanum", r"C:\Windows\Fonts"]) or FONTS


def font(kind):
    """kind: 'sub' (bold rounded gothic), 'title' (bold serif), 'ui' (bold gothic) -> a .ttf path that exists."""
    want = {"sub": ["NanumSquareRoundB.ttf", "NanumSquareRoundEB.ttf", "NanumGothicBold.ttf", "malgunbd.ttf", "NotoSansCJK-Bold.ttc"],
            "title": ["NanumMyeongjoBold.ttf", "NanumMyeongjoExtraBold.ttf", "batang.ttc", "malgunbd.ttf", "NotoSerifCJK-Bold.ttc"],
            "ui": ["NanumSquareB.ttf", "NanumGothicBold.ttf", "malgunbd.ttf", "NotoSansCJK-Bold.ttc"]}[kind]
    dirs = [d for d in [os.environ.get("YADAM_FONT_DIR"), FONTS, "/usr/share/fonts/truetype/nanum", "/usr/share/fonts/opentype/noto", r"C:\Windows\Fonts"] if d]
    for w in want:
        for d in dirs:
            p = pathlib.Path(d) / w
            if p.exists():
                return str(p)
    sys.exit("no Korean font found: put NanumSquareRoundB.ttf etc. in fonts/ or set YADAM_FONT_DIR")


def sub_font_name():
    """Font family name for the ASS subtitle style, matching font('sub')."""
    f = pathlib.Path(font("sub")).name.lower()
    return {"nanumsquareroundb.ttf": "NanumSquareRound", "nanumsquareroundeb.ttf": "NanumSquareRound", "nanumgothicbold.ttf": "NanumGothic",
            "malgunbd.ttf": "Malgun Gothic", "notosanscjk-bold.ttc": "Noto Sans CJK KR"}.get(f, "NanumSquareRound")


if __name__ == "__main__":
    print("repo      :", REPO)
    print("ffmpeg    :", ffmpeg(), "(ok)" if shutil.which(ffmpeg()) or pathlib.Path(ffmpeg()).exists() else "(MISSING)")
    for n in (ST3_NAME, MIMIC_NAME):
        print(f"{n[:22]:22s}:", model_dir(n) or f"MISSING -> download {ST3_URL if n == ST3_NAME else MIMIC_URL} and extract into models/")
    print("font dir  :", font_dir())
    for k in ("sub", "title", "ui"):
        print(f"font {k:5s}:", font(k))
    print("sub family:", sub_font_name())
    try:
        import sherpa_onnx, soundfile, numpy, PIL; print("python    : sherpa_onnx", sherpa_onnx.__version__, "ok")
    except Exception as e:
        print("python    : MISSING ->", e, "-> pip install sherpa-onnx soundfile numpy pillow")
