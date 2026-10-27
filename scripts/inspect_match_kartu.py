import json

with open("transcripts/Match Kartu/IMG_0648_16k.json") as f:
    d = json.load(f)

for s in d.get("segments", []):
    st = s.get("start", 0)
    en = s.get("end", 0)
    txt = s.get("text", "").strip()
    print(f"[{st:5.2f} -> {en:5.2f}] {txt}")

print("\n--- Detailed Word Timestamps from 55s to 95s ---")
for s in d.get("segments", []):
    for w in s.get("words", []):
        if w.get("start", 0) >= 55.0:
            print(f"  {w.get('word')} [{w.get('start', 0):.2f} - {w.get('end', 0):.2f}]")
