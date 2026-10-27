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

if [ "$LANG_VAL" = "id" ]; then
    echo "🇮🇩 [Transcribe] Running Bilingual Indonesian-English Whisper ASR with word timestamps..."
    python3 - "$AUDIO_WAV" "$ASR_JSON" << 'EOF'
import sys, json, torch, whisper, whisper.timing

orig_dtw = whisper.timing.dtw
def cpu_dtw(x):
    if isinstance(x, torch.Tensor):
        return orig_dtw(x.cpu().double().numpy())
    return orig_dtw(x)
whisper.timing.dtw = cpu_dtw

wav_path, out_json = sys.argv[1], sys.argv[2]
device = "mps" if torch.backends.mps.is_available() else "cpu"
model = whisper.load_model("base", device=device)
prompt = "Angel, Arthur, challenge, suit, batu gunting kertas, babi, domba, sapi, alpaka, kambing, kelinci, traktor, snack, benar, salah, poin."
res = model.transcribe(wav_path, language="id", word_timestamps=True, condition_on_previous_text=False, initial_prompt=prompt)
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
EOF
else
    echo "⚡ [Transcribe] Running Parakeet-MLX on Apple Silicon Metal GPU..."
    if command -v parakeet-mlx >/dev/null 2>&1; then
        parakeet-mlx "$AUDIO_WAV" \
            --highlight-words \
            --output-format all \
            --output-dir "$OUTPUT_DIR"
    elif command -v parakeet-cli >/dev/null 2>&1; then
        parakeet-cli "$AUDIO_WAV" --json > "$ASR_JSON"
    else
        echo "❌ Neither parakeet-mlx nor parakeet-cli found in PATH."
        exit 1
    fi
fi

# Run 10ms RMS Acoustic Onset & Stereo Diarization Refiner
ACOUSTIC_JSON="$OUTPUT_DIR/${BASENAME}_acoustic.json"
python3 ./scripts/acoustic_onset.py \
    --wav "$AUDIO_STEREO_WAV" \
    --json "$ASR_JSON" \
    --output "$ACOUSTIC_JSON"

echo "✅ [Transcribe] Saved transcripts & 10ms RMS acoustic onset schedule to: $OUTPUT_DIR/"
ls -lh "$OUTPUT_DIR/${BASENAME}"*
