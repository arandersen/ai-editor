#!/usr/bin/env bash
# Diagnose by default; explicitly request installation of pinned Node dependencies.
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"
if [ "${1:-}" = "--install" ]; then
  npm ci
  mkdir -p assets/audio/music assets/audio/sfx raw broll transcripts renders/drafts renders/final projects memory/lessons
  if [ ! -e audio ] && [ ! -L audio ]; then
    ln -s assets/audio audio
  fi
elif [ "$#" -gt 0 ]; then
  echo 'Usage: scripts/setup_tools.sh [--install]' >&2
  exit 1
fi
exec python3 -m editor doctor
