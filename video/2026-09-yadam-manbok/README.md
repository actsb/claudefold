# 바보 머슴 만복이와 서른 냥의 약속 — 1시간 야담 애니메이션 롱폼

시니어 시청자를 위한 조선 야담 각색 애니메이션(약 61분, 1920×1080, 24fps). 대본·그림·음성·음악·자막을
모두 이 저장소의 스크립트로 생성한다. 기획 근거는 `research/yadam-longform-2026-09.md`.

| 경로 | 내용 |
|---|---|
| `script/00_prologue.md` … `10_epilogue.md` | 대본(프롤로그 + 9장 + 에필로그). 장면 헤더(`## SCENE bg=… cam=… chars=…`)와 나레이션/대사(`@이름`) |
| `assets/` | 생성된 그림: `bg/` 배경 17장(2400×1350), `char/` 인물 스프라이트 120장(입·눈 4상태), `prop/` 소품 15개, `svg/` 원본 |
| `youtube-meta.md` | 업로드용 제목·설명·태그·챕터 타임스탬프 |
| `thumbnail.png` | 썸네일(1280×720) |
| `build/` (git 제외) | 나레이션 wav, 타이밍 JSON, 음악/효과음, 장면 클립, 최종 `../yadam_manbok_1080p.mp4` |

## 한 줄로 만들기 (윈도우·리눅스 공통)

```powershell
python scripts\yadam_build.py video\2026-09-yadam-manbok --setup    # 처음 한 번: ffmpeg·한국어 음성 모델(Supertonic 3)·파이썬 패키지
python scripts\yadam_build.py video\2026-09-yadam-manbok            # 그림→음악→대본→나레이션→렌더→썸네일→QA
python scripts\yadam_build.py video\2026-09-yadam-manbok --from tts # 대본을 고친 뒤: 바뀐 문장만 다시 합성하고 다시 렌더
```

## 처음부터 다시 만들기 (단계별)

```bash
# 0) 준비: Python 3.11, Node 22 + playwright(전역), ffmpeg(static), 나눔·Noto CJK 폰트,
#    pip install sherpa-onnx soundfile numpy pillow
#    한국어 TTS 모델(오프라인): mimic3 ko_KO/kss_low → sherpa-onnx 변환본
curl -L -o m.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-mimic3-ko_KO-kss_low.tar.bz2 && tar xjf m.tar.bz2
export YADAM_TTS_MODEL=$PWD/vits-mimic3-ko_KO-kss_low   FFMPEG=/path/to/ffmpeg

# 1) 그림 (SVG → PNG, Chromium)          2) 음악·효과음 (전부 합성)
python3 scripts/yadam_art.py video/2026-09-yadam-manbok/assets
python3 scripts/yadam_music.py video/2026-09-yadam-manbok/build/audio

# 3) 대본 파싱 → 4) 나레이션 합성(문장별, 0.76배속 + 쉼) → 5) 렌더(장면 컷아웃 애니메이션 + 자막 + 믹스)
python3 scripts/yadam_script.py video/2026-09-yadam-manbok
python3 scripts/yadam_tts.py    video/2026-09-yadam-manbok --speed 0.76
python3 scripts/yadam_render.py video/2026-09-yadam-manbok --jobs 3      # 약 40분(4코어)

# QA / 썸네일
python3 scripts/yadam_qa.py video/2026-09-yadam-manbok/yadam_manbok_1080p.mp4 qa.png --every 90
python3 scripts/yadam_thumbnail.py video/2026-09-yadam-manbok
```

한 장면만 확인: `python3 scripts/yadam_render.py video/2026-09-yadam-manbok --only 12 --seconds 20 --preview`

## 대본을 고치면
`script/*.md`만 고친 뒤 3)→4)→5)를 다시 실행하면 된다. 바뀐 문장만 다시 합성되고(캐시), 바뀐 장면 클립만 다시
렌더하려면 `build/clips/`에서 해당 `clip_NNN.mp4`를 지우면 된다.

## 윈도우(D:\Claude_Work\LongYoutube)에서 이어서 작업하기

```powershell
# 1) 저장소를 원하는 폴더로 받기 (기존 clone을 옮겨도 됨: 폴더째 이동하면 git이 그대로 따라온다)
git clone -b claude/youtube-yaddam-animation-7kgov5 https://github.com/actsb/claudefold.git D:\Claude_Work\LongYoutube
cd D:\Claude_Work\LongYoutube
claude            # 이 폴더에서 Claude Code를 열면 이후 작업은 여기서 진행

# 2) 도구: Python 3.11, Node 22, ffmpeg (winget install Gyan.FFmpeg), 나눔글꼴 설치
pip install sherpa-onnx soundfile numpy pillow
npm i -g playwright ; npx playwright install chromium
# 3) TTS 모델을 위 curl 주소에서 받아 압축을 풀고
$env:YADAM_TTS_MODEL="D:\Claude_Work\LongYoutube\vits-mimic3-ko_KO-kss_low"
$env:FFMPEG="C:\ffmpeg\bin\ffmpeg.exe"
```
스크립트 안의 폰트 경로(`/usr/share/fonts/truetype/nanum`)는 윈도우에서 `C:\Windows\Fonts` 등으로 바꿔야 한다
(`yadam_render.py`의 `FONT_DIR`, `FONT_TITLE`, `yadam_thumbnail.py`의 `FONT`).
완성된 mp4·wav 같은 대용량 산출물은 git에 넣지 않으므로(`.gitignore`), 세션에서 내려받아 `build/`에 두거나 위 순서로 재생성한다.
