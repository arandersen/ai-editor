#!/usr/bin/env bash
# scripts/transcribe.sh
# Extracts 16kHz mono & stereo WAV, runs local ASR (Parakeet for English or Whisper for Indonesian/Bilingual),
# and refines all word timestamps via 10ms RMS acoustic onset + Left/Right speaker diarization.
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

if [ $# -lt 1 ]; then
    echo "Usage: ./scripts/transcribe.sh <path_to_video_or_audio> [--lang en|id]"
    exit 1
fi

INPUT_FILE="$1"
LANG_MODE="${2:---lang}"
LANG_VAL="${3:-en}"
if [ "$LANG_MODE" = "id" ] || [ "$LANG_MODE" = "--id" ]; then
    LANG_VAL="id"
fi

BASENAME="$(basename "${INPUT_FILE%.*}")"
PARENT_DIR="$(basename "$(dirname "$INPUT_FILE")")"
if [ "$PARENT_DIR" != "raw" ] && [ "$PARENT_DIR" != "." ]; then
    OUTPUT_DIR="transcripts/$PARENT_DIR"
else
    OUTPUT_DIR="transcripts"
fi
mkdir -p "$OUTPUT_DIR"

echo "🎙️ [Transcribe] Extracting 16kHz audio from: $INPUT_FILE"
AUDIO_WAV="$OUTPUT_DIR/${BASENAME}_16k.wav"
AUDIO_STEREO_WAV="$OUTPUT_DIR/${BASENAME}_16k_stereo.wav"
ffmpeg -y -v error -i "$INPUT_FILE" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$AUDIO_WAV"
ffmpeg -y -v error -i "$INPUT_FILE" -vn -acodec pcm_s16le -ar 16000 -ac 2 "$AUDIO_STEREO_WAV" || cp "$AUDIO_WAV" "$AUDIO_STEREO_WAV"

ASR_JSON="$OUTPUT_DIR/${BASENAME}_16k.json"
ASR_SRT="$OUTPUT_DIR/${BASENAME}_16k.srt"
ASR_TXT="$OUTPUT_DIR/${BASENAME}_16k.txt"

# Resolve local Python interpreter that has OpenAI Whisper + PyTorch MPS installed
WHISPER_PY="python3"
if command -v whisper >/dev/null 2>&1; then
    CANDIDATE_PY="$(head -n 1 "$(command -v whisper)" | sed 's/^#!//')"
    if [ -x "$CANDIDATE_PY" ]; then
        WHISPER_PY="$CANDIDATE_PY"
    fi
fi

PARAKEET_BIN=""
if command -v parakeet-mlx >/dev/null 2>&1 && parakeet-mlx --help >/dev/null 2>&1; then
    PARAKEET_BIN="$(command -v parakeet-mlx)"
elif [ -x "$HOME/.venvs/parakeet/bin/parakeet-mlx" ] && "$HOME/.venvs/parakeet/bin/parakeet-mlx" --help >/dev/null 2>&1; then
    PARAKEET_BIN="$HOME/.venvs/parakeet/bin/parakeet-mlx"
fi

if [ "$LANG_VAL" = "en" ] && [ -n "$PARAKEET_BIN" ]; then
    echo "⚡ [Transcribe] Running Parakeet-MLX on Apple Silicon Metal GPU..."
    "$PARAKEET_BIN" "$AUDIO_WAV" \
        --highlight-words \
        --output-format all \
        --output-dir "$OUTPUT_DIR"
else
    echo "🎙️ [Transcribe] Running Local Apple Silicon Metal Whisper ASR (--lang $LANG_VAL) with word-level timestamps..."
    "$WHISPER_PY" - "$AUDIO_WAV" "$ASR_JSON" "$ASR_SRT" "$ASR_TXT" "$LANG_VAL" << 'EOF'
import os, sys, json, torch, whisper, whisper.timing

# Patch DTW to move tensor to CPU first to avoid Apple MPS float64 limitation during word timestamp alignment
orig_dtw = whisper.timing.dtw
def cpu_dtw(x):
    if isinstance(x, torch.Tensor):
        return orig_dtw(x.cpu())
    return orig_dtw(x)
whisper.timing.dtw = cpu_dtw

def fmt_srt_time(seconds: float) -> str:
    ms = int(round((seconds - int(seconds)) * 1000))
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

wav_path, out_json, out_srt, out_txt, lang_val = sys.argv[1:6]
device = "mps" if torch.backends.mps.is_available() else "cpu"
cache_dir = os.path.expanduser("~/.cache/whisper")

if lang_val == "id":
    model_name = "base"
    prompt = "Angel, Arthur, challenge, suit, batu gunting kertas, babi, domba, sapi, alpaka, kambing, kelinci, traktor, snack, benar, salah, poin."
else:
    model_name = "small.en" if os.path.exists(os.path.join(cache_dir, "small.en.pt")) else "base"
    prompt = "AI video editing, Claude Code, Antigravity, Gemini, HyperFrames, FFmpeg, Notion, GitHub, workflow, tutorial."

print(f"   • Model: {model_name} on {device.upper()}")
model = whisper.load_model(model_name, device=device)
res = model.transcribe(
    wav_path,
    language="id" if lang_val == "id" else "en",
    word_timestamps=True,
    condition_on_previous_text=False,
    initial_prompt=prompt,
)

with open(out_json, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)

with open(out_txt, "w", encoding="utf-8") as f:
    for seg in res.get("segments", []):
        f.write(f"[{seg.get('start', 0):.2f}s -> {seg.get('end', 0):.2f}s] {seg.get('text', '').strip()}\n")

with open(out_srt, "w", encoding="utf-8") as f:
    for idx, seg in enumerate(res.get("segments", []), start=1):
        f.write(f"{idx}\n{fmt_srt_time(seg.get('start', 0))} --> {fmt_srt_time(seg.get('end', 0))}\n{seg.get('text', '').strip()}\n\n")
EOF
fi

# Run 10ms RMS Acoustic Onset & Stereo Diarization Refiner
ACOUSTIC_JSON="$OUTPUT_DIR/${BASENAME}_acoustic.json"
python3 ./scripts/acoustic_onset.py \
    --wav "$AUDIO_STEREO_WAV" \
    --json "$ASR_JSON" \
    --output "$ACOUSTIC_JSON"

echo "✅ [Transcribe] Saved transcripts & 10ms RMS acoustic onset schedule to: $OUTPUT_DIR/"
ls -lh "$OUTPUT_DIR/${BASENAME}"*
