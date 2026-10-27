#!/usr/bin/env python3
import subprocess
import os

assets_dir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/02_assets/real_downloads"
target_dir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/04_hyperframes/assets"
os.makedirs(target_dir, exist_ok=True)

ffmpeg = "/opt/homebrew/bin/ffmpeg"

def run_cmd(cmd):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

# 1. Classroom photo: Crop, warm editorial grading, 900x560
run_cmd([
    ffmpeg, "-y",
    "-i", f"{assets_dir}/beat02_classroom.jpg",
    "-vf", "crop=1800:1120:180:160,scale=900:560,eq=contrast=1.2:brightness=0.02:saturation=0.7",
    "-update", "1", "-frames:v", "1",
    f"{target_dir}/beat02_classroom_real.jpg"
])

# 2. Starter pistol: Crop gun, contrast, scale 640:480
run_cmd([
    ffmpeg, "-y",
    "-i", f"{assets_dir}/beat02_starter_gun.jpg",
    "-vf", "crop=2800:2100:600:460,scale=640:480,eq=contrast=1.25:saturation=0.5",
    "-update", "1", "-frames:v", "1",
    f"{target_dir}/beat02_starter_gun.jpg"
])

# 3. Banknote Money: Crop banknote, warm tone, scale 700:360
run_cmd([
    ffmpeg, "-y",
    "-i", f"{assets_dir}/beat03_money.jpg",
    "-vf", "scale=700:320,eq=contrast=1.2:saturation=0.85",
    "-update", "1", "-frames:v", "1",
    f"{target_dir}/beat03_money_card.jpg"
])

# 4. City Skyline: NYC vintage skyline, scale 700:440
run_cmd([
    ffmpeg, "-y",
    "-i", f"{assets_dir}/beat03_city.jpg",
    "-vf", "crop=1600:1000:27:25,scale=700:440,eq=contrast=1.15:saturation=0.8",
    "-update", "1", "-frames:v", "1",
    f"{target_dir}/beat03_city_card.jpg"
])

# 5. Handshake: Business handshake, scale 700:460
run_cmd([
    ffmpeg, "-y",
    "-i", f"{assets_dir}/beat03_handshake.jpg",
    "-vf", "crop=3800:2500:1100:750,scale=700:460,eq=contrast=1.2:saturation=0.75",
    "-update", "1", "-frames:v", "1",
    f"{target_dir}/beat03_handshake_card.jpg"
])

# 6. Lap 9 Runner: Sprinter surging across finish line, scale 500:700
run_cmd([
    ffmpeg, "-y",
    "-i", f"{assets_dir}/beat05_lap9_runner.jpg",
    "-vf", "crop=1200:1680:180:340,scale=500:700,eq=contrast=1.2:saturation=0.8",
    "-update", "1", "-frames:v", "1",
    f"{target_dir}/beat05_lap9_runner.jpg"
])

# 7. Lap 3 Runner: Track runner in race (image is 2139x1307), crop 900x1200, scale 500:700
run_cmd([
    ffmpeg, "-y",
    "-i", f"{assets_dir}/beat05_lap3_runner.jpg",
    "-vf", "crop=900:1200:600:50,scale=500:700,eq=contrast=1.25:saturation=0.6",
    "-update", "1", "-frames:v", "1",
    f"{target_dir}/beat05_lap3_runner.jpg"
])

print("✅ All real archival photos successfully cropped and graded!")
