// Rasterize every SVG in a folder to a 2x PNG with the pre-installed Chromium.
// Usage: node scripts/render_png.mjs posts/<slug>/images
// Resolves Playwright from the project first, then from the global npm root.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join, basename } from 'node:path';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(join(execSync('npm root -g').toString().trim(), 'playwright'))); }

const dir = process.argv[2] ?? 'posts/2026-09-best-robot-vacuums/images';
const exe = ['/opt/pw-browsers/chromium-1194/chrome-linux/chrome'].find(existsSync);
const browser = await chromium.launch(exe ? { executablePath: exe } : {});
const page = await browser.newPage({ deviceScaleFactor: 2 });
for (const f of readdirSync(dir).filter(n => n.endsWith('.svg'))) {
  const svg = readFileSync(join(dir, f), 'utf8');
  const m = svg.match(/viewBox="-?\d+ -?\d+ (\d+) (\d+)"/);
  const w = m ? +m[1] : 1000, h = m ? +m[2] : 600;
  await page.setViewportSize({ width: w, height: h });
  await page.setContent(`<body style="margin:0;background:#fff">${svg.replace(/<svg /, `<svg style="width:${w}px;height:${h}px;display:block" `)}</body>`);
  const out = join(dir, basename(f, '.svg') + '.png');
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: w, height: h } });
  console.log('wrote', out);
}
await browser.close();
