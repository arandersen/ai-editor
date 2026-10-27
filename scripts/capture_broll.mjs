#!/usr/bin/env node
/**
 * capture_broll.mjs
 * Captures crisp 4K screenshots of research papers, articles, GitHub repos, or websites
 * using local Google Chrome so the Researcher subagent can turn them into B-roll.
 *
 * Usage:
 *   node ./scripts/capture_broll.mjs --url "https://arxiv.org/abs/..." --output "broll/paper.png"
 */

import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';

const args = process.argv.slice(2);
function getArg(flag, fallback = null) {
  const idx = args.indexOf(flag);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : fallback;
}

const url = getArg('--url');
const output = getArg('--output', 'broll/screenshot.png');
const width = getArg('--width', '2560');
const height = getArg('--height', '1440');

if (!url) {
  console.error('Usage: node ./scripts/capture_broll.mjs --url <URL> [--output broll/out.png] [--width 2560] [--height 1440]');
  process.exit(1);
}

const outPath = resolve(output);
mkdirSync(dirname(outPath), { recursive: true });

const chromePaths = [
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
];

const chromeBin = chromePaths.find((p) => existsSync(p));
if (!chromeBin) {
  console.error('❌ Could not find Google Chrome in /Applications.');
  process.exit(1);
}

console.log(`🌐 Capturing 4K B-Roll screenshot from: ${url}`);
execFileSync(
  chromeBin,
  [
    '--headless=new',
    '--disable-gpu',
    '--hide-scrollbars',
    `--window-size=${width},${height}`,
    '--force-device-scale-factor=2',
    `--screenshot=${outPath}`,
    url
  ],
  { stdio: 'inherit' }
);

console.log(`✅ Saved B-Roll screenshot to: ${outPath}`);
