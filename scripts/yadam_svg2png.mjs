// Rasterise SVGs for the yadam video with the pre-installed Chromium (Playwright).
// Usage:
//   node scripts/yadam_svg2png.mjs <jobs.json>      jobs = [{"svg":..., "png":..., "transparent":true|false}]
//   node scripts/yadam_svg2png.mjs <dir> [--opaque] every *.svg in <dir> -> *.png next to it (transparent unless --opaque)
// Output size == viewBox size exactly (deviceScaleFactor 1). Sprites: transparent background
// (omitBackground); backgrounds: opaque white body under the SVG.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { readdirSync, readFileSync, existsSync, statSync, mkdirSync } from 'node:fs';
import { join, basename, dirname, resolve } from 'node:path';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(join(execSync('npm root -g').toString().trim(), 'playwright'))); }

const arg = process.argv[2];
if (!arg) { console.error('usage: yadam_svg2png.mjs <jobs.json | dir> [--opaque]'); process.exit(2); }
let jobs;
if (statSync(arg).isDirectory()) {
  const transparent = !process.argv.includes('--opaque');
  jobs = readdirSync(arg).filter(n => n.endsWith('.svg')).sort()
    .map(n => ({ svg: join(arg, n), png: join(arg, basename(n, '.svg') + '.png'), transparent }));
} else {
  jobs = JSON.parse(readFileSync(arg, 'utf8'));
}

// cloud session's pre-installed Chromium first; on a PC Playwright's own browser (npx playwright install chromium)
const exe = [process.env.YADAM_CHROME, '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'].filter(Boolean).find(existsSync);
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage({ deviceScaleFactor: 1 });
let done = 0;
for (const job of jobs) {
  const svg = readFileSync(job.svg, 'utf8');
  const m = svg.match(/viewBox="-?\d+ -?\d+ (\d+) (\d+)"/);
  if (!m) throw new Error('no integer viewBox in ' + job.svg);
  const w = +m[1], h = +m[2];
  await page.setViewportSize({ width: w, height: h });
  const bg = job.transparent ? 'transparent' : '#ffffff';
  await page.setContent(
    `<!doctype html><html><head><style>html,body{margin:0;padding:0;background:${bg};overflow:hidden}</style></head>` +
    `<body>${svg.replace(/<svg /, `<svg style="width:${w}px;height:${h}px;display:block" `)}</body></html>`,
    { waitUntil: 'load' });
  mkdirSync(dirname(resolve(job.png)), { recursive: true });
  await page.screenshot({ path: job.png, omitBackground: !!job.transparent, clip: { x: 0, y: 0, width: w, height: h } });
  done++;
}
await browser.close();
console.log(`rasterised ${done} svg(s)`);
