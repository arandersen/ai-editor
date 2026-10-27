#!/usr/bin/env python3
import sys
import os
import asyncio
import subprocess
import json

sys.path.append(os.path.expanduser('~/Library/Python/3.9/lib/python/site-packages'))
import edge_tts

VOICE = "en-GB-RyanNeural"
VO_DIR = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/03_vo"
os.makedirs(VO_DIR, exist_ok=True)

BEATS = [
    {
        "id": 1,
        "text": "Your twenties are a race. There is just one problem: nobody started at the same line."
    },
    {
        "id": 2,
        "text": "At twenty two, it looks fair. Same classrooms, same exams, same starting gun."
    },
    {
        "id": 3,
        "text": "Then life deals the cards. Family money. The city you are born in. Who you know."
    },
    {
        "id": 4,
        "text": "And every day, your phone shows you the scoreboard: promotions, weddings, houses, everyone's highlights, on loop."
    },
    {
        "id": 5,
        "text": "So you compare your lap three, to somebody else's lap nine. Of course you feel behind."
    },
    {
        "id": 6,
        "text": "But look at the actual timeline. The degree lands at twenty nine. The business at twenty seven. The wedding at twenty four. There is no schedule."
    },
    {
        "id": 7,
        "text": "A sprinter and a marathoner can share a track. It does not make either of them slow."
    },
    {
        "id": 8,
        "text": "The only fair scoreboard is you, versus you, one year ago."
    },
    {
        "id": 9,
        "text": "Same race. Different laps. Run yours."
    }
]

async def generate_all():
    print(f"Generating 9 narration beats with British English neural voice: {VOICE} at rate +9%...")
    durations = []
    beat_files = []
    for b in BEATS:
        mp3_path = f"{VO_DIR}/beat_{b['id']:02d}.mp3"
        communicate = edge_tts.Communicate(b['text'], VOICE, rate="+9%")
        await communicate.save(mp3_path)
        
        # probe duration
        res = subprocess.run(
            ["/opt/homebrew/bin/ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", mp3_path],
            capture_output=True, text=True, check=True
        )
        dur = float(res.stdout.strip())
        durations.append(dur)
        beat_files.append(mp3_path)
        print(f"  Beat {b['id']} ({dur:.2f}s): {b['text']}")
    
    total_speech = sum(durations)
    print(f"Total speech duration: {total_speech:.2f}s")
    
    # Calculate beat start and end times with natural padding
    # Target: 59.5s total duration
    # Distribute small padding between beats (approx 0.15s - 0.25s)
    remaining_time = 59.50 - total_speech
    pause_per_gap = max(0.08, remaining_time / 8.0)
    print(f"Adding inter-beat pause: {pause_per_gap:.2f}s")
    
    beat_timings = []
    current_t = 0.0
    for i, b in enumerate(BEATS):
        dur = durations[i]
        start_t = round(current_t, 2)
        end_t = round(start_t + dur, 2)
        beat_timings.append({
            "id": b["id"],
            "t_start": start_t,
            "t_end": end_t,
            "duration": round(dur, 2),
            "vo": b["text"]
        })
        current_t = end_t + pause_per_gap
    
    # Save beat-timing.json
    with open(f"{VO_DIR}/beat-timing.json", "w") as f:
        json.dump(beat_timings, f, indent=2)
    print(f"Saved beat-timing.json (Final timestamp: {beat_timings[-1]['t_end']:.2f}s)")
    
    # Build combined vo.wav using FFmpeg filter complex
    filter_parts = []
    inputs = []
    for i, fpath in enumerate(beat_files):
        inputs.extend(["-i", fpath])
        delay_ms = int(beat_timings[i]["t_start"] * 1000)
        filter_parts.append(f"[{i}:a]adelay={delay_ms}|{delay_ms}[a{i}]")
    
    mix_str = "".join(f"[a{i}]" for i in range(len(beat_files)))
    fc = f"{';'.join(filter_parts)};{mix_str}amix=inputs={len(beat_files)}:normalize=0[out]"
    
    out_wav = f"{VO_DIR}/vo.wav"
    ffmpeg_cmd = ["/opt/homebrew/bin/ffmpeg", "-y"] + inputs + [
        "-filter_complex", fc,
        "-map", "[out]",
        "-ar", "48000",
        "-ac", "1",
        "-t", "59.53",
        out_wav
    ]
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"✅ Generated combined master voiceover: {out_wav}")

if __name__ == "__main__":
    asyncio.run(generate_all())
