import os
os.environ["PATH"] = "/opt/homebrew/bin:/usr/local/bin:" + os.environ.get("PATH", "")
import json
import torch
import whisper
import whisper.timing

# Fix MPS float64 bug by moving tensor to CPU before double()
def patched_dtw(x: torch.Tensor):
    return whisper.timing.dtw_cpu(x.cpu().double().numpy())
whisper.timing.dtw = patched_dtw

wav_path = "transcripts/Kartu Pasangan/IMG_0651_16k.wav"
out_dir = "transcripts/Kartu Pasangan"
os.makedirs(out_dir, exist_ok=True)

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Loading whisper base on {device}...")
model = whisper.load_model("base", device=device)

print("Transcribing Indonesian audio with word timestamps...")
result = model.transcribe(
    wav_path,
    language="id",
    word_timestamps=True,
    condition_on_previous_text=False,
    verbose=True
)

json_path = os.path.join(out_dir, "IMG_0651_whisper.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

txt_path = os.path.join(out_dir, "IMG_0651_whisper.txt")
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(result["text"])

# Write readable segments
readable_path = os.path.join(out_dir, "segments_readable.txt")
with open(readable_path, "w", encoding="utf-8") as f:
    for i, seg in enumerate(result["segments"]):
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        f.write(f"{i:03d} [{start:6.2f}s -> {end:6.2f}s] {text}\n")

print(f"Done! Saved {json_path} and {readable_path}")
