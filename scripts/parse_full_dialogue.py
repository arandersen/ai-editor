import json

with open("transcripts/Kartu Pasangan/IMG_0651_whisper.json") as f:
    data = json.load(f)

print(f"Total Whisper segments: {len(data['segments'])}")
for seg in data["segments"]:
    start = seg["start"]
    end = seg["end"]
    text = seg["text"].strip()
    words = seg.get("words", [])
    print(f"\n[{start:6.2f}s -> {end:6.2f}s] {text}")
    w_list = [f"{w['word'].strip()}({w['start']:.2f}-{w['end']:.2f})" for w in words]
    print("  " + " ".join(w_list))
