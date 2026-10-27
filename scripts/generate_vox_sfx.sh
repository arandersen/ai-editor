#!/usr/bin/env bash
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

SFX_DIR="audio/sfx"
mkdir -p "$SFX_DIR"

# 1. Paper Thock (Low-frequency muffled impact of thick paper card hitting table)
ffmpeg -y -f lavfi -i "sine=frequency=140:sample_rate=48000:duration=0.12" \
  -af "lowpass=f=220,afade=t=in:st=0:d=0.005,afade=t=out:st=0.02:d=0.10:curve=exp,volume=1.8" \
  "$SFX_DIR/paper_thock.wav" -loglevel error

# 2. Paper Slide (Gentle friction swish of card dealing onto paper)
ffmpeg -y -f lavfi -i "anoisesrc=d=0.22:c=pink:r=48000:a=0.4" \
  -af "bandpass=f=1400:width_type=h:w=900,afade=t=in:st=0:d=0.04:curve=qsin,afade=t=out:st=0.08:d=0.14:curve=esin,volume=1.1" \
  "$SFX_DIR/paper_slide.wav" -loglevel error

# 3. Marker Squeak (Resonant marker sweep across dry paper)
ffmpeg -y -f lavfi -i "sine=frequency=1650:sample_rate=48000:duration=0.28" \
  -af "bandpass=f=1600:width_type=h:w=400,afade=t=in:st=0:d=0.03,afade=t=out:st=0.12:d=0.16:curve=exp,volume=0.9" \
  "$SFX_DIR/marker_squeak.wav" -loglevel error

# 4. Timeline Tick (Crisp subtle tick for timestamp markers)
ffmpeg -y -f lavfi -i "sine=frequency=2400:sample_rate=48000:duration=0.035" \
  -af "afade=t=in:st=0:d=0.002,afade=t=out:st=0.006:d=0.029:curve=exp,volume=0.85" \
  "$SFX_DIR/timeline_tick.wav" -loglevel error

echo "✅ Vox custom SFX synthesized in $SFX_DIR/:"
ls -lh "$SFX_DIR"/paper_thock.wav "$SFX_DIR"/paper_slide.wav "$SFX_DIR"/marker_squeak.wav "$SFX_DIR"/timeline_tick.wav
