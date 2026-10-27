import json

with open("transcripts/Kartu Pasangan/IMG_0651_whisper.json") as f:
    data = json.load(f)

# Search for words related to cards and points
keywords = ["sapi", "donkey", "nongki", "domba", "babi", "pick", "klinci", "linji", "ayam", "kuda", "telur", "traktor", "raktor", "menang", "curang", "pura", "poin", "satu", "dua", "tiga", "sebelas", "double"]

for seg in data["segments"]:
    text_lower = seg["text"].lower()
    if any(k in text_lower for k in keywords):
        print(f"[{seg['start']:6.2f} - {seg['end']:6.2f}] {seg['text'].strip()}")
        # print words
        words_str = " ".join([f"{w['word']}({w['start']:.1f}-{w['end']:.1f})" for w in seg.get("words", [])])
        print(f"    Words: {words_str}")
