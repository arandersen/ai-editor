import json
from pathlib import Path

transcript_file = Path("transcripts/Hafal Kartu/IMG_0658_16k.json")
with open(transcript_file) as f:
    d = json.load(f)

segments = d.get("segments", [])
print(f"Total segments: {len(segments)}")

with open("transcripts/Hafal Kartu/segments_readable.txt", "w") as out:
    for idx, s in enumerate(segments):
        start = s.get("start", 0)
        end = s.get("end", 0)
        txt = s.get("text", "").strip()
        line = f"{idx:03d} [{start:6.2f}s -> {end:6.2f}s] {txt}\n"
        out.write(line)

print("Saved to transcripts/Hafal Kartu/segments_readable.txt")
