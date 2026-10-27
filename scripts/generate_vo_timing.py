#!/usr/bin/env python3
import json
import re

with open("VOX-TEST_race/03_vo/beat-timing.json", "r") as f:
    beat_data = json.load(f)

all_words = []
structured_beats = []

for b in beat_data:
    bid = b["id"]
    b_start = b["t_start"]
    speech_dur = b["duration"]
    text = b["vo"]
    
    # Clean words and split - strictly no hyphens
    tokens = re.findall(r"[A-Za-z0-9']+", text)
    
    # Weight word duration by length
    weights = [max(2, len(t)) for t in tokens]
    total_weight = sum(weights)
    
    cur_t = b_start
    beat_words = []
    for t, w in zip(tokens, weights):
        dur = (w / total_weight) * speech_dur
        w_obj = {
            "word": t,
            "start": round(cur_t, 3),
            "end": round(cur_t + dur * 0.92, 3),
            "beat": bid
        }
        all_words.append(w_obj)
        beat_words.append(w_obj)
        cur_t += dur
        
    structured_beats.append({
        "beat": bid,
        "start": b_start,
        "end": b["t_end"],
        "text": text,
        "words": beat_words
    })

total_dur = beat_data[-1]["t_end"]
output = {
    "project": "the-race-you-never-signed-up-for",
    "total_duration": total_dur,
    "words": all_words,
    "beats": structured_beats
}

with open("VOX-TEST_race/03_vo/vo-timing.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Generated vo-timing.json with {len(all_words)} words across {len(structured_beats)} beats!")
print(f"Total VO runtime: {total_dur}s")
