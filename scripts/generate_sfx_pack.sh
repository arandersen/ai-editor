#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
SFX_DIR="audio/sfx"
mkdir -p "$SFX_DIR"

echo "🔊 Generating 100% free studio SFX pack in $SFX_DIR/ using FFmpeg..."

# 1. Whoosh (Filtered pink noise sweep for transitions & B-roll entrances)
ffmpeg -y -f lavfi -i "anoisesrc=d=0.38:c=pink:r=48000:a=0.5" \
  -af "bandpass=f=900:width_type=h:w=1200,afade=t=in:st=0:d=0.14:curve=qsin,afade=t=out:st=0.14:d=0.24:curve=esin,volume=1.4" \
  "$SFX_DIR/whoosh.wav" -loglevel error

# 2. Pop (Clean pitch-drop sine pop for badges, callouts & lower-thirds)
ffmpeg -y -f lavfi -i "sine=frequency=520:sample_rate=48000:duration=0.09" \
  -af "asetrate=48000*0.65,aresample=48000,afade=t=in:st=0:d=0.005,afade=t=out:st=0.02:d=0.07:curve=exp,volume=0.9" \
  "$SFX_DIR/pop.wav" -loglevel error

# 3. Click (Crisp UI / mechanical switch click for kinetic text & highlights)
ffmpeg -y -f lavfi -i "sine=frequency=1800:sample_rate=48000:duration=0.025" \
  -af "afade=t=in:st=0:d=0.002,afade=t=out:st=0.004:d=0.021:curve=exp,volume=0.8" \
  "$SFX_DIR/click.wav" -loglevel error

# 4. Riser (1.2s tension sweep leading into reveals or hooks)
ffmpeg -y -f lavfi -i "anoisesrc=d=1.2:c=white:r=48000:a=0.35" \
  -af "lowpass=f=2400,afade=t=in:st=0:d=1.05:curve=exp,afade=t=out:st=1.05:d=0.15,volume=1.2" \
  "$SFX_DIR/riser.wav" -loglevel error

# 5. Sub Drop (Deep 60Hz bass impact for pattern interrupts & hook drops)
ffmpeg -y -f lavfi -i "sine=frequency=65:sample_rate=48000:duration=0.65" \
  -af "afade=t=in:st=0:d=0.01,afade=t=out:st=0.08:d=0.57:curve=exp,volume=1.1" \
  "$SFX_DIR/sub_drop.wav" -loglevel error

echo "✅ Studio SFX Pack generated:"
ls -lh "$SFX_DIR"
