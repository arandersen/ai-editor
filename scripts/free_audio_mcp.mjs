#!/usr/bin/env node
/**
 * free_audio_mcp.mjs
 * 100% Free MCP Server replacing paid Epidemic Sound.
 *
 * Provides 3 MCP tools over stdio:
 * 1. search_free_audio     -> Queries Openverse Audio API (Jamendo, Freesound, Wikimedia CC0/commercial) with NO API key required (plus optional Freesound API key support).
 * 2. download_free_audio   -> Downloads a direct audio URL or YouTube Audio Library / CC0 URL (via yt-dlp) into audio/music/ or audio/sfx/.
 * 3. generate_studio_sfx   -> Generates studio-grade editing SFX (whoosh, pop, click, riser, sub_drop) locally using FFmpeg.
 */

import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import readline from 'node:readline';

const WORKSPACE_DIR = process.cwd();

async function searchOpenverseAudio({ query, category = 'music', licenseType = 'commercial', pageSize = 10 }) {
  const params = new URLSearchParams({
    q: query,
    page_size: String(pageSize),
    license_type: licenseType,
  });
  if (category === 'music' || category === 'sound_effect') {
    params.set('category', category);
  }
  const url = `https://api.openverse.org/v1/audio/?${params.toString()}`;
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Antigravity-AI-Video-Editor/1.0' }
  });
  if (!res.ok) {
    throw new Error(`Openverse API HTTP ${res.status}`);
  }
  const data = await res.json();
  return (data.results || []).map((item) => ({
    id: item.id,
    title: item.title,
    creator: item.creator,
    source: item.source,
    license: `${item.license} ${item.license_version || ''}`.trim(),
    duration_ms: item.duration,
    audio_url: item.url,
    foreign_landing_url: item.foreign_landing_url,
    tags: (item.tags || []).slice(0, 6).map((t) => t.name)
  }));
}

async function downloadAudio({ url, filename, folder = 'music' }) {
  const targetDir = resolve(WORKSPACE_DIR, 'audio', folder === 'sfx' ? 'sfx' : 'music');
  mkdirSync(targetDir, { recursive: true });
  const outPath = resolve(targetDir, filename);

  if (url.includes('youtube.com/') || url.includes('youtu.be/')) {
    const ytdlp = existsSync('/Users/arthurandersen/.local/bin/yt-dlp')
      ? '/Users/arthurandersen/.local/bin/yt-dlp'
      : 'yt-dlp';
    execFileSync(
      ytdlp,
      [
        '--ffmpeg-location',
        '/opt/homebrew/bin',
        '-x',
        '--audio-format',
        'mp3',
        '--audio-quality',
        '0',
        '-o',
        outPath,
        url
      ],
      { stdio: 'pipe' }
    );
    return { saved_to: outPath, method: 'yt-dlp' };
  }

  const res = await fetch(url, {
    headers: { 'User-Agent': 'Antigravity-AI-Video-Editor/1.0' }
  });
  if (!res.ok) {
    throw new Error(`Failed to download audio (${res.status}) from ${url}`);
  }
  const buf = Buffer.from(await res.arrayBuffer());
  writeFileSync(outPath, buf);
  return { saved_to: outPath, bytes: buf.length, method: 'direct_http' };
}

function generateStudioSfx() {
  const scriptPath = resolve(WORKSPACE_DIR, 'scripts', 'generate_sfx_pack.sh');
  const out = execFileSync('/bin/bash', [scriptPath], { encoding: 'utf-8' });
  return { status: 'ok', output: out.trim() };
}

const TOOLS = [
  {
    name: 'search_free_audio',
    description:
      'Search 1M+ free, royalty-free / Creative Commons commercial music tracks and sound effects via Openverse (Jamendo, Freesound, Wikimedia) with zero API key required.',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Search query (e.g., "lofi chill beat", "cinematic ambient", "whoosh transition")' },
        category: { type: 'string', enum: ['music', 'sound_effect', 'all'], default: 'music' },
        pageSize: { type: 'number', default: 8 }
      },
      required: ['query']
    }
  },
  {
    name: 'download_free_audio',
    description:
      'Download a free music track or sound effect URL (direct MP3/WAV from Openverse/Freesound or a YouTube Audio Library/CC0 URL via yt-dlp) into audio/music/ or audio/sfx/.',
    inputSchema: {
      type: 'object',
      properties: {
        url: { type: 'string', description: 'Direct audio URL or YouTube CC0 URL' },
        filename: { type: 'string', description: 'Output filename (e.g., "lofi_bg.mp3" or "whoosh_01.wav")' },
        folder: { type: 'string', enum: ['music', 'sfx'], default: 'music' }
      },
      required: ['url', 'filename']
    }
  },
  {
    name: 'generate_studio_sfx',
    description:
      'Synthesize a complete studio pack of YouTube editing SFX (whoosh.wav, pop.wav, click.wav, riser.wav, sub_drop.wav) locally into audio/sfx/ using FFmpeg.',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  }
];

function sendResponse(id, result) {
  process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id, result }) + '\n');
}

function sendError(id, code, message) {
  process.stdout.write(JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } }) + '\n');
}

const rl = readline.createInterface({ input: process.stdin, terminal: false });

rl.on('line', async (line) => {
  if (!line.trim()) return;
  let msg;
  try {
    msg = JSON.parse(line);
  } catch {
    return;
  }

  const { id, method, params } = msg;

  try {
    if (method === 'initialize') {
      sendResponse(id, {
        protocolVersion: '2024-11-05',
        capabilities: { tools: {} },
        serverInfo: { name: 'free-audio-mcp', version: '1.0.0' }
      });
    } else if (method === 'notifications/initialized') {
      // No response needed for notification
    } else if (method === 'tools/list') {
      sendResponse(id, { tools: TOOLS });
    } else if (method === 'tools/call') {
      const toolName = params?.name;
      const args = params?.arguments || {};
      if (toolName === 'search_free_audio') {
        const results = await searchOpenverseAudio(args);
        sendResponse(id, {
          content: [{ type: 'text', text: JSON.stringify(results, null, 2) }]
        });
      } else if (toolName === 'download_free_audio') {
        const res = await downloadAudio(args);
        sendResponse(id, {
          content: [{ type: 'text', text: JSON.stringify(res, null, 2) }]
        });
      } else if (toolName === 'generate_studio_sfx') {
        const res = generateStudioSfx();
        sendResponse(id, {
          content: [{ type: 'text', text: JSON.stringify(res, null, 2) }]
        });
      } else {
        sendError(id, -32601, `Unknown tool: ${toolName}`);
      }
    } else if (id !== undefined) {
      sendResponse(id, {});
    }
  } catch (err) {
    if (id !== undefined) {
      sendResponse(id, {
        isError: true,
        content: [{ type: 'text', text: `Error: ${err.message}` }]
      });
    }
  }
});
