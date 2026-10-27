#!/usr/bin/env python3
import subprocess
from pathlib import Path

preview = Path("renders/drafts/Kartu Pasangan/kartu_pasangan_preview.mp4")
out_dir = Path("renders/drafts/Kartu Pasangan/timeline_inspect")
out_dir.mkdir(parents=True, exist_ok=True)

# Extract 1 frame every 2 seconds
cmd = [
    "ffmpeg", "-y",
    "-i", str(preview),
    "-vf", "fps=0.5",
    "-q:v", "3",
    str(out_dir / "sec_%03d.jpg")
]
subprocess.run(cmd, check=True)
print("Extracted frames!")
