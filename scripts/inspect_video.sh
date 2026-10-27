#!/usr/bin/env bash
# scripts/inspect_video.sh
# Inspects a video clip for duration, resolution, silences, black frames, and generates:
# 1. Full-duration 5x6 timestamped contact sheet (<name>_contact_sheet.jpg)
# 2. Optional table-crop contact sheet (--table-crop) for card/prop games (<name>_table_sheet.jpg)
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

if [ $# -lt 1 ]; then
    echo "Usage: ./scripts/inspect_video.sh <path_to_video.mp4> [--table-crop]"
    exit 1
fi

INPUT_VIDEO="$1"
TABLE_CROP="${2:-}"
BASENAME="$(basename "${INPUT_VIDEO%.*}")"
DRAFT_DIR="renders/drafts"
mkdir -p "$DRAFT_DIR"

echo "🔍 [Inspect] Analyzing media properties for: $INPUT_VIDEO"
DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT_VIDEO")
RESOLUTION=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$INPUT_VIDEO")
FPS_RAW=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 "$INPUT_VIDEO")
echo "   • Duration:   ${DURATION}s"
echo "   • Resolution: ${RESOLUTION} (${FPS_RAW} fps)"

# Detect silences > 0.22s (Talking Head & Couple threshold)
echo "🔇 [Inspect] Detecting silences (>0.22s at -35dB)..."
ffmpeg -i "$INPUT_VIDEO" -af "silencedetect=noise=-35dB:d=0.22" -f null - 2>&1 | grep -E "silence_(start|end)" | head -n 30 || true

# Detect black frames across the full video
echo "⬛ [Inspect] Detecting black frames across full duration..."
ffmpeg -i "$INPUT_VIDEO" -vf "blackdetect=d=0.08:pix_th=0.10" -an -f null - 2>&1 | grep "black_start" | head -n 20 || true

# Dynamically compute FPS interval so 30 tiles (5x6) always span 100% of the video duration
STEP=$(python3 -c "d = float('${DURATION:-30}'); print(f'{max(0.2, d / 30.0):.4f}')")
CONTACT_SHEET="$DRAFT_DIR/${BASENAME}_contact_sheet.jpg"
echo "🖼️  [Inspect] Generating full-duration 5x6 contact sheet (1 frame every ${STEP}s) -> $CONTACT_SHEET"
ffmpeg -y -v error -i "$INPUT_VIDEO" \
    -vf "fps=1/${STEP},scale=360:-1,drawtext=text='%{pts\:hms}':x=10:y=10:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.75,tile=5x6" \
    -frames:v 1 -q:v 2 "$CONTACT_SHEET"

if [ "$TABLE_CROP" = "--table-crop" ]; then
    TABLE_SHEET="$DRAFT_DIR/${BASENAME}_table_sheet.jpg"
    echo "🃏 [Inspect] Generating lower-half table-crop contact sheet -> $TABLE_SHEET"
    ffmpeg -y -v error -i "$INPUT_VIDEO" \
        -vf "fps=1/${STEP},crop=iw:ih*0.45:0:ih*0.55,scale=360:-1,drawtext=text='%{pts\:hms}':x=10:y=10:fontsize=22:fontcolor=yellow:box=1:boxcolor=black@0.75,tile=5x6" \
        -frames:v 1 -q:v 2 "$TABLE_SHEET"
fi

# Generate lightweight <15MB 540p H.264+AAC Vision Proxy MP4 so Gemini view_file can ALWAYS watch & listen natively
# even when raw 4K .MOV files exceed the 100MB tool limit.
VISION_PROXY="$DRAFT_DIR/${BASENAME}_vision_proxy.mp4"
echo "🎬 [Inspect] Generating lightweight <15MB Vision Proxy MP4 (with audio + burned timecode) -> $VISION_PROXY"
ffmpeg -y -v error -i "$INPUT_VIDEO" \
    -vf "scale=-2:540,fps=15,drawtext=text='%{pts\:hms}':x=12:y=12:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.7" \
    -c:v libx264 -preset ultrafast -crf 28 -pix_fmt yuv420p \
    -c:a aac -b:a 64k -ac 1 \
    -movflags +faststart "$VISION_PROXY"

echo "✅ [Inspect] Complete!"
echo "   • Contact Sheet: $CONTACT_SHEET"
echo "   • Vision Proxy:  $VISION_PROXY (Always <15MB for Gemini native video+audio watching)"
ls -lh "$CONTACT_SHEET" "$VISION_PROXY"
