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
shift
LANG_VAL="en"
SPEAKERS="SpeakerLeft,SpeakerRight"
while [ "$#" -gt 0 ]; do
    case "$1" in
        --lang) LANG_VAL="${2:?--lang requires en or id}"; shift 2 ;;
        --speakers) SPEAKERS="${2:?--speakers requires left,right}"; shift 2 ;;
        id|--id) LANG_VAL="id"; shift ;;
        *) echo "Unknown argument: $1" >&2; exit 1 ;;
    esac
done
case "$LANG_VAL" in en|id) ;; *) echo "Supported languages: en, id" >&2; exit 1 ;; esac

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

# Resolve local Python interpreter that has faster-whisper / OpenAI Whisper installed
WHISPER_PY="python3"
if [ -x "$HOME/.venvs/whisper/bin/python3" ]; then
    WHISPER_PY="$HOME/.venvs/whisper/bin/python3"
elif command -v whisper >/dev/null 2>&1; then
    CANDIDATE_PY="$(head -n 1 "$(command -v whisper)" | sed 's/^#!//')"
    if [ -x "$CANDIDATE_PY" ]; then
        WHISPER_PY="$CANDIDATE_PY"
    fi
fi

ARCH="$(uname -m)"
PARAKEET_BIN=""
if [ "$ARCH" = "arm64" ]; then
    if command -v parakeet-mlx >/dev/null 2>&1 && parakeet-mlx --help >/dev/null 2>&1; then
        PARAKEET_BIN="$(command -v parakeet-mlx)"
    elif [ -x "$HOME/.venvs/parakeet/bin/parakeet-mlx" ] && "$HOME/.venvs/parakeet/bin/parakeet-mlx" --help >/dev/null 2>&1; then
        PARAKEET_BIN="$HOME/.venvs/parakeet/bin/parakeet-mlx"
    fi
fi

if [ "$LANG_VAL" = "en" ] && [ -n "$PARAKEET_BIN" ]; then
    echo "⚡ [Transcribe] Running Parakeet-MLX on Apple Silicon Metal GPU..."
    "$PARAKEET_BIN" "$AUDIO_WAV" \
        --highlight-words \
        --output-format all \
        --output-dir "$OUTPUT_DIR"
else
    echo "🎙️ [Transcribe] Running Local Whisper ASR (--lang $LANG_VAL on $ARCH) with word-level timestamps..."
    "$WHISPER_PY" - "$AUDIO_WAV" "$ASR_JSON" "$ASR_SRT" "$ASR_TXT" "$LANG_VAL" << 'EOF'
import os, sys, json

def fmt_srt_time(seconds: float) -> str:
    ms = int(round((seconds - int(seconds)) * 1000))
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

wav_path, out_json, out_srt, out_txt, lang_val = sys.argv[1:6]
cache_dir = os.path.expanduser("~/.cache/whisper")

if lang_val == "id":
    model_name = "base"
    prompt = "Angel, Arthur, challenge, suit, batu gunting kertas, babi, domba, sapi, alpaka, kambing, kelinci, traktor, snack, benar, salah, poin."
else:
    model_name = "small.en"
    prompt = "AI video editing, Claude Code, Antigravity, Gemini, HyperFrames, FFmpeg, Notion, GitHub, workflow, tutorial."

res = None
# Prefer faster-whisper (CTranslate2 int8) on CPU/x86_64 for 4-6x faster transcription with word timestamps
try:
    import wave
    import numpy as np
    from faster_whisper import WhisperModel
    fw_cache = os.path.expanduser("~/.cache/faster_whisper")
    os.makedirs(fw_cache, exist_ok=True)
    print(f"   • Engine: faster-whisper ({model_name}, int8 CPU)")
    with wave.open(wav_path, "rb") as wf:
        raw_pcm = wf.readframes(wf.getnframes())
    audio_np = np.frombuffer(raw_pcm, dtype=np.int16).astype(np.float32) / 32768.0
    fw_model = WhisperModel(model_name, device="cpu", compute_type="int8", download_root=fw_cache, local_files_only=True)
    segments_gen, info = fw_model.transcribe(
        audio_np,
        language="id" if lang_val == "id" else "en",
        word_timestamps=True,
        condition_on_previous_text=False,
        initial_prompt=prompt,
    )
    seg_list = []
    full_text = []
    for idx, seg in enumerate(segments_gen):
        words_out = []
        for w in (seg.words or []):
            words_out.append({
                "word": w.word,
                "start": round(float(w.start), 3),
                "end": round(float(w.end), 3),
                "probability": round(float(getattr(w, "probability", 1.0)), 3),
            })
        seg_list.append({
            "id": idx,
            "start": round(float(seg.start), 3),
            "end": round(float(seg.end), 3),
            "text": seg.text,
            "words": words_out,
        })
        full_text.append(seg.text.strip())
    res = {"text": " ".join(full_text), "segments": seg_list, "language": lang_val}
except Exception as fw_err:
    print(f"   • Note: faster-whisper unavailable ({fw_err}), falling back to openai-whisper...")

if res is None:
    import torch, whisper, whisper.timing
    orig_dtw = whisper.timing.dtw
    def cpu_dtw(x):
        if isinstance(x, torch.Tensor):
            return orig_dtw(x.cpu())
        return orig_dtw(x)
    whisper.timing.dtw = cpu_dtw

    device = "mps" if torch.backends.mps.is_available() else "cpu"
    if lang_val != "id" and not os.path.exists(os.path.join(cache_dir, "small.en.pt")) and os.path.exists(os.path.join(cache_dir, "base.pt")):
        model_name = "base"
    print(f"   • Engine: openai-whisper ({model_name}) on {device.upper()}")
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
    --output "$ACOUSTIC_JSON" --speakers "$SPEAKERS"

echo "✅ [Transcribe] Saved transcripts & 10ms RMS acoustic onset schedule to: $OUTPUT_DIR/"
ls -lh "$OUTPUT_DIR/${BASENAME}"*
