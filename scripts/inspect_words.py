import json

with open("transcripts/Hafal Kartu/IMG_0658_16k.json") as f:
    d = json.load(f)

words = []
for s in d.get("segments", []):
    for w in s.get("words", []):
        words.append(w)

print(f"Total words: {len(words)}")

def show_words(t0, t1):
    sub = [w for w in words if w["start"] >= t0 - 0.2 and w["end"] <= t1 + 0.2]
    print(f"\n=== Range {t0}s to {t1}s ===")
    parts = []
    for w in sub:
        parts.append(f"{w['word']} [{w['start']:.2f}-{w['end']:.2f}]")
    print(" ".join(parts))

show_words(0.0, 12.0)
show_words(140.0, 165.0)
show_words(169.0, 178.0)
show_words(195.0, 201.0)
show_words(312.0, 320.0)
show_words(326.0, 336.0)
show_words(345.0, 351.0)
show_words(371.0, 377.0)
show_words(382.0, 388.0)
show_words(398.0, 410.0)
show_words(423.0, 433.0)
show_words(447.0, 456.0)
show_words(483.0, 491.0)
show_words(505.0, 516.0)
show_words(525.0, 532.0)
show_words(551.0, 557.0)
show_words(561.0, 568.0)
show_words(583.0, 604.0)
