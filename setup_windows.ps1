# One-time setup on the Windows PC (run in PowerShell inside D:\Claude_Work\LongYoutube)
#   Set-ExecutionPolicy -Scope Process Bypass; .\setup_windows.ps1
$ErrorActionPreference = "Stop"
Write-Host "== Python / Node / git check"
python --version; node --version; git --version
Write-Host "== Python packages"
python -m pip install --upgrade pip
python -m pip install sherpa-onnx soundfile numpy pillow
Write-Host "== Playwright Chromium (only needed to regenerate the art)"
npm i -g playwright | Out-Null
npx playwright install chromium
Write-Host "== ffmpeg + Korean TTS model into tools/ and models/"
python scripts\yadam_build.py video\2026-09-yadam-manbok --setup
Write-Host "== fonts: copy NanumSquareRoundB.ttf, NanumSquareB.ttf, NanumMyeongjoBold.ttf into .\fonts\ (optional; Malgun Gothic is the fallback)"
Write-Host "== Claude Code"
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) { irm https://claude.ai/install.ps1 | iex }
Write-Host "done. Next: python scripts\yadam_build.py video\2026-09-yadam-manbok   (full build)   /   claude   (work here)"
