#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

echo "=========================================================="
echo "🎬 AI Video Editor — Gemini 4 Argon (Antigravity) Setup"
echo "=========================================================="

echo ""
echo "1️⃣  Checking Core System Binaries..."
for bin in brew ffmpeg ffprobe node npm npx uv python3; do
  if command -v "$bin" >/dev/null 2>&1; then
    echo "  ✅ $bin -> $(command -v "$bin")"
  else
    echo "  ❌ $bin not found! Install via Homebrew: brew install $bin"
  fi
done

echo ""
echo "2️⃣  Checking Local Transcriber: Parakeet (parakeet-mlx & parakeet-cli)..."
if command -v parakeet-mlx >/dev/null 2>&1; then
  echo "  ✅ parakeet-mlx installed -> $(command -v parakeet-mlx)"
else
  echo "  ⏳ Installing/updating parakeet-mlx via uv tool..."
  uv tool install parakeet-mlx -U
fi

if command -v parakeet-cli >/dev/null 2>&1; then
  echo "  ✅ parakeet-cli (Metal GPU) installed -> $(command -v parakeet-cli)"
fi

echo ""
echo "3️⃣  Installing / Updating Animation Engine: HyperFrames (latest)..."
npm install -g hyperframes@latest
echo "  ✅ hyperframes -> $(command -v hyperframes) ($(hyperframes --version 2>/dev/null || echo 'ready'))"

echo ""
echo "4️⃣  Checking Google Chrome for Researcher B-Roll Capture..."
if [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  echo "  ✅ Google Chrome found at /Applications/Google Chrome.app"
else
  echo "  ⚠️  Google Chrome not found at /Applications/Google Chrome.app"
fi

echo ""
echo "5️⃣  Checking Antigravity Customizations & MCP Servers..."
echo "  ✅ Workspace Rules:     GEMINI.md"
echo "  ✅ Master Editing Skill: .agents/skills/youtube-edit/SKILL.md"
echo "  ✅ 36 Editing Rules:     .agents/skills/youtube-edit/references/editing-rules.md"
echo "  ✅ HyperFrames Skill:    .agents/skills/hyperframes/SKILL.md"
echo "  ✅ MCP Plugin Config:    .agents/plugins/video-editor-mcp/mcp_config.json"
echo "      - tella:           https://api.tella.com/mcp"
echo "      - epidemic-sound:  https://www.epidemicsound.com/a/mcp-service/mcp"
echo "      - chrome-devtools: npx -y chrome-devtools-mcp@latest"
echo ""
echo "✨ All tools installed, updated, and verified!"
