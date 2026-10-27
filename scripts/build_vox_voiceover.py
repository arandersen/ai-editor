#!/usr/bin/env python3
import subprocess
import os
import json

beats_config = [
    {
        "id": 1,
        "rate": 160,
        "target_dur": 6.0,
        "text": "Your twenties are a race. There's just one problem: nobody started at the same line."
    },
    {
        "id": 2,
        "rate": 160,
        "target_dur": 6.5,
        "text": "At twenty-two, it looks fair. Same classrooms, same exams, same starting gun."
    },
    {
        "id": 3,
        "rate": 165,
        "target_dur": 6.5,
        "text": "Then life deals the cards. Family money. The city you're born in. Who you know."
    },
    {
        "id": 4,
        "rate": 178,
        "target_dur": 7.0,
        "text": "And every day, your phone shows you the scoreboard: promotions, weddings, houses — everyone's highlights, on loop."
    },
    {
        "id": 5,
        "rate": 175,
        "target_dur": 6.5,
        "text": "So you compare your lap three… to somebody else's lap nine. Of course you feel behind."
    },
    {
        "id": 6,
        "rate": 185,
        "target_dur": 8.0,
        "text": "But look at the actual timeline. The degree lands at twenty-nine. The business at twenty-seven. The wedding at twenty-four. There is no schedule."
    },
    {
        "id": 7,
        "rate": 165,
        "target_dur": 5.8,
        "text": "A sprinter and a marathoner can share a track. It doesn't make either of them slow."
    },
    {
        "id": 8,
        "rate": 160,
        "target_dur": 5.2,
        "text": "The only fair scoreboard is you, versus you, one year ago."
    },
    {
        "id": 9,
        "rate": 140,
        "target_dur": 6.0,
        "text": "Same race. Different laps. Run yours."
    }
]

out_dir = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/03_vo"
os.makedirs(out_dir, exist_ok=True)
tmp_files = []
timeline_events = []
current_time = 0.0

print("Synthesizing voice lines with zero clipping...")
for b in beats_config:
    bid = b["id"]
    text = b["text"]
    rate = b["rate"]
    target_dur = b["target_dur"]
    
    aiff_path = f"/tmp/vo_beat_{bid}.aiff"
    wav_raw = f"/tmp/vo_beat_{bid}_raw.wav"
    wav_padded = f"/tmp/vo_beat_{bid}_padded.wav"
    
    # Synthesize line
    subprocess.run(["say", "-v", "Daniel", "-r", str(rate), "-o", aiff_path, text], check=True)
    subprocess.run(["/opt/homebrew/bin/ffmpeg", "-y", "-i", aiff_path, "-ar", "48000", "-ac", "1", wav_raw], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # Measure raw duration
    probe_cmd = ["/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", wav_raw]
    raw_dur = float(subprocess.check_output(probe_cmd).decode().strip())
    
    if raw_dur > target_dur:
        # Increase target duration to prevent any clipping
        actual_dur = raw_dur + 0.35 # add 350ms natural breathing room
    else:
        actual_dur = target_dur
        
    pad_dur = actual_dur - raw_dur
    # Pad audio without clipping
    subprocess.run([
        "/opt/homebrew/bin/ffmpeg", "-y", "-i", wav_raw,
        "-af", f"apad=pad_dur={pad_dur:.3f}",
        "-ar", "48000", "-ac", "1", wav_padded
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    tmp_files.append(wav_padded)
    timeline_events.append({
        "beat": bid,
        "start": current_time,
        "end": current_time + actual_dur,
        "speech_duration": raw_dur,
        "total_duration": actual_dur,
        "text": text
    })
    print(f"Beat {bid}: speech={raw_dur:.2f}s, pad={pad_dur:.2f}s, total={actual_dur:.2f}s [Start: {current_time:.2f}s, End: {current_time+actual_dur:.2f}s]")
    current_time += actual_dur

concat_txt = "/tmp/vo_concat.txt"
with open(concat_txt, "w") as f:
    for tf in tmp_files:
        f.write(f"file '{tf}'\n")

final_vo = os.path.join(out_dir, "vo.wav")
subprocess.run([
    "/opt/homebrew/bin/ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", concat_txt, "-ar", "48000", "-ac", "1", final_vo
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

probe_final = ["/opt/homebrew/bin/ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", final_vo]
tot_dur = float(subprocess.check_output(probe_final).decode().strip())

print(f"\n✅ Master voiceover generated: {final_vo}")
print(f"⏱️ Total runtime: {tot_dur:.2f}s (Constraint: 60s ± 2s [58.0s - 62.0s])")

# Save beat timing metadata
with open(os.path.join(out_dir, "beat-timing.json"), "w") as f:
    json.dump({
        "total_duration": tot_dur,
        "beats": timeline_events
    }, f, indent=2)
print("Saved beat-timing.json")
