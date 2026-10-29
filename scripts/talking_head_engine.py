#!/usr/bin/env python3
"""Compatibility entry point; use python3 -m editor render for the same contract."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from editor.__main__ import main

if __name__ == '__main__':
    raise SystemExit(main(['render', *sys.argv[1:]]))
