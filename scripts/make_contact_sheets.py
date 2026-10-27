#!/usr/bin/env python3
import subprocess
from pathlib import Path

preview = Path("renders/drafts/Kartu Pasangan/kartu_pasangan_preview.mp4")
out_dir = Path("renders/drafts/Kartu Pasangan")

def make_sheet(start_sec, end_sec, step_sec, out_name):
    # Select frames every step_sec between start_sec and end_sec, tile them into a contact sheet
    num_frames = int((end_sec - start_sec) / step_sec)
    # create temporary tiled sheet using ffmpeg select and tile
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-to", str(end_sec),
        "-i", str(preview),
        "-vf", (
            f"fps=1/{step_sec},"
            f"drawtext=text='%{{pts\\:hms}}':x=20:y=20:fontsize=36:fontcolor=yellow:box=1:boxcolor=black@0.8,"
            f"scale=270:480,"
            f"tile=5x4"
        ),
        "-q:v", "3",
        str(out_dir / out_name)
    ]
    subprocess.run(cmd, check=True)
    print(f"Created {out_name}")

make_sheet(35, 75, 2, "sheet_35_75.jpg")
make_sheet(75, 115, 2, "sheet_75_115.jpg")
make_sheet(115, 155, 2, "sheet_115_155.jpg")
