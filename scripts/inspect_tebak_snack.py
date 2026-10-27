import json

with open("transcripts/Tebak Snack/IMG_2439_whisper.json") as f:
    data = json.load(f)

print("=== SEGMENTS & WORDS ===")
for i, seg in enumerate(data["segments"]):
    s = seg["start"]
    e = seg["end"]
    txt = seg["text"].strip()
    print(f"\nSEG {i:02d} [{s:6.2f} -> {e:6.2f}]: {txt}")
    words = [f"{w['start']:5.2f}-{w['end']:5.2f}:{w['word']}" for w in seg.get("words", [])]
    print("   WORDS: " + " | ".join(words[:12]))
    if len(words) > 12:
        print("          " + " | ".join(words[12:]))
