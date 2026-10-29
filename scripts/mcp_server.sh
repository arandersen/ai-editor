#!/usr/bin/env bash
# Launch optional providers relative to this checkout, from any caller directory.
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"
case "${1:-}" in
  free-audio) exec node "$REPO_DIR/scripts/free_audio_mcp.mjs" ;;
  flow)
    FLOW_ENTRY="${FLOW_MCP_ENTRY:-$REPO_DIR/tools/flow-mcp/dist/index.js}"
    if [ ! -f "$FLOW_ENTRY" ]; then
      echo 'Optional Flow provider missing. Install it separately and set FLOW_MCP_ENTRY.' >&2
      exit 1
    fi
    export FLOW_MCP_OUTPUT="${FLOW_MCP_OUTPUT:-$REPO_DIR/broll/flow}"
    exec node "$FLOW_ENTRY" ;;
  *) echo 'Usage: scripts/mcp_server.sh free-audio|flow' >&2; exit 1 ;;
esac
