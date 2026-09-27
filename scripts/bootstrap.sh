#!/usr/bin/env bash
# Fresh-session setup for the post pipeline (ffmpeg-static + sharp live in the session scratchpad, Playwright is preinstalled).
# Usage: bash scripts/bootstrap.sh [scratchpad-dir]     Safe to re-run; prints the paths the other scripts will find.
set -e
S="${1:-$(ls -d /tmp/claude-0/*/*/scratchpad 2>/dev/null | head -1)}"
[ -n "$S" ] || { echo "no scratchpad dir found; pass it as the first argument"; exit 1; }
mkdir -p "$S/ffm" "$S/imgtool"
if [ ! -x "$S/ffm/node_modules/ffmpeg-static/ffmpeg" ]; then (cd "$S/ffm" && npm init -y >/dev/null 2>&1 && npm install ffmpeg-static --no-audit --no-fund --silent); fi
if [ ! -d "$S/imgtool/node_modules/sharp" ]; then (cd "$S/imgtool" && npm init -y >/dev/null 2>&1 && npm install sharp --no-audit --no-fund --silent); fi
node -e "require('playwright')" 2>/dev/null || node -e "require(require('child_process').execSync('npm root -g').toString().trim()+'/playwright')" || echo "WARN: playwright not found (render_png.mjs needs it)"
python3 -c "import html, json, re" && echo "python ok"
echo "FFMPEG=$S/ffm/node_modules/ffmpeg-static/ffmpeg"
echo "NODE_PATH=$S/imgtool/node_modules"
"$S/ffm/node_modules/ffmpeg-static/ffmpeg" -version 2>/dev/null | head -1 || echo "WARN: ffmpeg-static missing"
