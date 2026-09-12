// Render a contact sheet of PNG/SVG files into one PNG using Playwright.
// Usage: node scripts/contact_sheet.mjs <out.png> <file1> <file2> ...
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); } catch { ({ chromium } = require(join(execSync('npm root -g').toString().trim(), 'playwright'))); }
const [out, ...files] = process.argv.slice(2);
const cols = 3, cw = 400, ch = 267;
const imgs = files.map(f => {
  const abs = resolve(f);
  const b64 = readFileSync(abs).toString('base64');
  const mime = f.endsWith('.svg') ? 'image/svg+xml' : 'image/png';
  return `<div style="width:${cw}px;height:${ch}px;overflow:hidden;background:#fff"><img src="data:${mime};base64,${b64}" style="width:100%;display:block"><div style="font:11px sans-serif;color:#666;padding:2px 4px">${f.split('/').pop()}</div></div>`;
}).join('');
const rows = Math.ceil(files.length / cols);
const html = `<body style="margin:0;background:#ddd"><div style="display:grid;grid-template-columns:repeat(${cols},${cw}px);gap:6px;padding:6px">${imgs}</div></body>`;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: cols*(cw+6)+6, height: rows*(ch+22+6)+6 }, deviceScaleFactor: 1 });
await page.setContent(html);
await page.screenshot({ path: out, fullPage: true });
await browser.close();
console.log('wrote', out);
