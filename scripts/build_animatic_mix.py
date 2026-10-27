#!/usr/bin/env python3
import subprocess
import os

base_dir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race"
raw_video = f"{base_dir}/05_renders/animatic_raw.mp4"
vo_audio = f"{base_dir}/03_vo/vo.wav"
bg_music = f"{base_dir}/03_vo/documentary_piano.mp3"
sfx_dir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/audio/sfx"

out_video = f"{base_dir}/05_renders/animatic.mp4"
frames_dir = f"{base_dir}/06_review/animatic-frames"
os.makedirs(frames_dir, exist_ok=True)

# Build SFX schedule: (time_in_sec, sfx_file, volume)
sfx_events = [
    # Beat 1 (0.00 - 6.00s)
    (0.3, f"{sfx_dir}/paper_thock.wav", 0.6),
    (0.6, f"{sfx_dir}/paper_thock.wav", 0.6),
    (0.9, f"{sfx_dir}/paper_thock.wav", 0.6),
    (1.2, f"{sfx_dir}/paper_thock.wav", 0.6),
    (1.5, f"{sfx_dir}/paper_thock.wav", 0.6),
    (4.1, f"{sfx_dir}/marker_squeak.wav", 0.5),
    # Beat 2 (6.06 - 12.88s)
    (6.2, f"{sfx_dir}/paper_slide.wav", 0.7),
    (9.3, f"{sfx_dir}/pop.wav", 0.6),
    (10.5, f"{sfx_dir}/paper_thock.wav", 0.8),
    # Beat 3 (12.93 - 20.32s)
    (14.0, f"{sfx_dir}/paper_slide.wav", 0.7),
    (16.5, f"{sfx_dir}/paper_slide.wav", 0.7),
    (18.5, f"{sfx_dir}/paper_slide.wav", 0.7),
    # Beat 4 (20.38 - 27.94s)
    (21.0, f"{sfx_dir}/paper_thock.wav", 0.8),
    (22.2, f"{sfx_dir}/pop.wav", 0.5),
    (23.4, f"{sfx_dir}/pop.wav", 0.55),
    (24.4, f"{sfx_dir}/pop.wav", 0.6),
    (25.3, f"{sfx_dir}/pop.wav", 0.65),
    (26.2, f"{sfx_dir}/pop.wav", 0.7),
    (26.9, f"{sfx_dir}/pop.wav", 0.75),
    # Beat 5 (28.00 - 34.28s)
    (29.5, f"{sfx_dir}/marker_squeak.wav", 0.6),
    (31.5, f"{sfx_dir}/marker_squeak.wav", 0.6),
    # Beat 6 (34.34 - 45.45s)
    (37.2, f"{sfx_dir}/timeline_tick.wav", 0.7),
    (39.8, f"{sfx_dir}/timeline_tick.wav", 0.7),
    (42.2, f"{sfx_dir}/timeline_tick.wav", 0.7),
    # Beat 7 (45.51 - 51.12s)
    (45.7, f"{sfx_dir}/whoosh.wav", 0.5),
    (46.0, f"{sfx_dir}/paper_slide.wav", 0.7),
    (46.3, f"{sfx_dir}/paper_slide.wav", 0.7),
    # Beat 8 (51.18 - 55.33s)
    (51.6, f"{sfx_dir}/paper_thock.wav", 0.7),
    (52.7, f"{sfx_dir}/paper_thock.wav", 0.8),
    (53.6, f"{sfx_dir}/marker_squeak.wav", 0.6),
    # Beat 9 (55.39 - 60.36s)
    (55.8, f"{sfx_dir}/paper_thock.wav", 0.7),
    (56.8, f"{sfx_dir}/paper_thock.wav", 0.7),
    (57.9, f"{sfx_dir}/paper_thock.wav", 0.9),
    (58.6, f"{sfx_dir}/pop.wav", 0.5)
]

print("Assembling SFX track...")
sfx_inputs = []
sfx_filter_parts = []
for i, (t_sec, fpath, vol) in enumerate(sfx_events):
    sfx_inputs.extend(["-i", fpath])
    delay_ms = int(t_sec * 1000)
    sfx_filter_parts.append(f"[{i+3}:a]volume={vol},adelay={delay_ms}|{delay_ms}[sfx{i}]")

mix_inputs_str = "".join(f"[sfx{i}]" for i in range(len(sfx_events)))
sfx_mix_filter = f"{';'.join(sfx_filter_parts)};{mix_inputs_str}amix=inputs={len(sfx_events)}:normalize=0[sfx_all]"

# Full FFmpeg pipeline:
cmd = [
    "/opt/homebrew/bin/ffmpeg", "-y",
    "-i", raw_video,
    "-i", vo_audio,
    "-i", bg_music
] + sfx_inputs

fc = (
    "[0:v]scale=540:960,fps=30[v_out];"
    "[2:a]volume='if(gte(t,57.8), 0.12 + 0.33*(t-57.8)/2.5, 0.12)':eval=frame,atrim=0:60.36,asetpts=PTS-STARTPTS[music_ducked];"
    f"{sfx_mix_filter};"
    "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11[vo_norm];"
    "[vo_norm][music_ducked][sfx_all]amix=inputs=3:duration=first:weights=1.0 0.85 1.0[a_out]"
)

cmd.extend([
    "-filter_complex", fc,
    "-map", "[v_out]",
    "-map", "[a_out]",
    "-c:v", "libx264",
    "-crf", "22",
    "-preset", "fast",
    "-c:a", "aac",
    "-b:a", "192k",
    "-t", "60.36",
    out_video
])

print("Running master FFmpeg animatic render...")
subprocess.run(cmd, check=True)
print(f"✅ Animatic successfully rendered to: {out_video}")

# Extract 9 review frames (one per beat at visual climax)
frame_times = [
    (1, 4.8),
    (2, 11.2),
    (3, 18.8),
    (4, 26.5),
    (5, 32.5),
    (6, 44.0),
    (7, 48.0),
    (8, 54.0),
    (9, 59.0)
]

print("Extracting review frames for all 9 beats...")
for b_num, t in frame_times:
    frame_path = f"{frames_dir}/beat{b_num:02d}_frame.jpg"
    sub_cmd = [
        "/opt/homebrew/bin/ffmpeg", "-y",
        "-ss", f"{t:.2f}",
        "-i", out_video,
        "-vframes", "1",
        "-q:v", "2",
        frame_path
    ]
    subprocess.run(sub_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"  Frame Beat {b_num} (at {t:.1f}s): {frame_path}")

print("All 9 review frames extracted successfully!")
