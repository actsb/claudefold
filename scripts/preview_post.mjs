// Screenshot a built post at a Blogger-like column width for visual QA.
// Usage: node scripts/preview_post.mjs posts/<slug>/post.html <out-prefix> [width] [maxHeight]
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require(join(execSync('npm root -g').toString().trim(), 'playwright'))); }
const [file, out, widthArg, maxArg] = process.argv.slice(2);
const width = Number(widthArg || 760), maxH = Number(maxArg || 3200);
let html = readFileSync(file, 'utf8');
// YouTube is unreachable from the sandbox: replace iframes with grey boxes so layout still shows.
html = html.replace(/<iframe[^>]*youtube\.com\/embed\/([A-Za-z0-9_\-]+)[^>]*><\/iframe>/g, '<div style="position:absolute;top:0;left:0;width:100%;height:100%;background:#333;color:#fff;font:14px sans-serif;display:flex;align-items:center;justify-content:center;">▶ YouTube $1</div>');
html = html.replace(/class="vp-short" style="/g, 'class="vp-short" style="position:relative;');
html = html.replace(/(src|poster)="https:\/\/raw\.githubusercontent\.com\/actsb\/claudefold\/[^"]*\/(posts\/[^"]+\.(png|jpe?g))"/g, (m, attr, rel, ext) => { try { return `${attr}="data:image/${ext === 'png' ? 'png' : 'jpeg'};base64,` + readFileSync(rel).toString('base64') + '"'; } catch { return m; } });
const page_html = `<body style="margin:0;background:#eee"><div style="width:${width}px;margin:0 auto;background:#fff;padding:24px 28px;font-family:Roboto,Helvetica,Arial,sans-serif;">${html}</div></body>`;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: width + 56, height: 1200 }, deviceScaleFactor: 1 });
await page.setContent(page_html, { waitUntil: 'load' });
await page.waitForTimeout(1500);
const total = await page.evaluate(() => document.body.scrollHeight);
const slices = Math.min(Math.ceil(total / maxH), 12);
for (let i = 0; i < slices; i++) {
  await page.screenshot({ path: `${out}-${i + 1}.png`, clip: { x: 0, y: i * maxH, width: width + 56, height: Math.min(maxH, total - i * maxH) }, fullPage: true });
}
console.log(`total height ${total}px → ${slices} slices to ${out}-N.png`);
await browser.close();
