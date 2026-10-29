#!/usr/bin/env bash
# Project-scoped sheets, structured diagnostics, and verified-size proxy parts.
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="$REPO_DIR${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m editor inspect "$@"
