import json

with open("transcripts/Kartu Pasangan/IMG_0651_whisper.json") as f:
    data = json.load(f)

print(f"Total segments: {len(data['segments'])}")
for i, seg in enumerate(data["segments"]):
    text = seg["text"].strip()
    print(f"Seg {i:03d} [{seg['start']:6.2f}s -> {seg['end']:6.2f}s]: {text}")
