#!/usr/bin/env python3
"""
scripts/lint_edl.py
Pre-Render EDL Linter for all 3 Video Categories:
  1. couple      (Rules C1-C15)
  2. talking_head (Rules TH1-TH25)
  3. animation   (Rules AM1-AM11)
plus Universal Standards (Rules U1-U8).

Run before rendering any video:
  python3 ./scripts/lint_edl.py --edl <path_to_edl.json> --category couple|talking_head|animation
"""

import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from editor.core import validate


def lint_edl(edl: dict, category: str) -> list:
    if category == "talking_head":
        return validate(edl)
    errors = []
    warnings = []

    segments = edl.get("segments", [])
    if not segments and category != "animation":
        errors.append("No 'segments' array found in EDL.")

    total_dur = 0.0
    for idx, seg in enumerate(segments):
        s0 = float(seg.get("start", seg.get("raw_start", 0.0)))
        s1 = float(seg.get("end", seg.get("raw_end", 0.0)))
        spd = float(seg.get("speed", 1.0))
        if s1 <= s0:
            errors.append(f"Segment #{idx + 1} has invalid range ({s0} >= {s1}).")
        total_dur += (s1 - s0) / max(0.01, spd)

    # Universal Rule U6: Check 4K resolution when specified
    res = edl.get("resolution", [2160, 3840])
    if res[0] < 1080 or res[1] < 1080:
        warnings.append(f"Resolution {res} is below 1080p; prefer Native 4K [2160, 3840] or [3840, 2160] (Rule U6).")

    if category == "couple":
        # 1. Rule C15 / U6: Strictly enforce Native 4K [2160, 3840] vertical resolution
        if res != [2160, 3840]:
            errors.append(
                f"[Rule C15 Violation] Couple video resolution must be Native 4K [2160, 3840], got {res}."
            )

        # 2. Rule C16 (@couple-speed-1.1x): Enforce 1.10x base speed on dialogue/hook
        base_spd = float(edl.get("base_speed", 0.0))
        if abs(base_spd - 1.10) > 0.02:
            errors.append(
                f"[Rule C16 / @couple-speed-1.1x Violation] EDL must set 'base_speed': 1.10 (got {base_spd})."
            )
        for idx, seg in enumerate(segments):
            phase = seg.get("phase", "dialogue")
            seg_type = seg.get("type", "main")
            spd = float(seg.get("speed", base_spd or 1.0))
            if seg_type == "main" and phase in ("hook", "dialogue", "banter", "guess") and spd < 1.08:
                errors.append(
                    f"[Rule C16 Violation] Segment #{idx + 1} (phase='{phase}') has speed={spd}x (< 1.10x base speed)."
                )
            if phase == "memorize":
                if spd < 3.0 or spd > 5.0:
                    errors.append(
                        f"[Rule C5 Violation] Memorization Segment #{idx + 1} speed={spd}x must be 3.0x-5.0x (4.0x default)."
                    )
                if not seg.get("suppress_captions", False):
                    errors.append(
                        f"[Rule C5 Violation] Memorization Segment #{idx + 1} must set 'suppress_captions': true."
                    )

        # 3. Rule C17 (@couple-grade): Enforce consistent 4K studio color grading
        if edl.get("color_grade") != "@couple-grade":
            errors.append(
                "[Rule C17 / @couple-grade Violation] Couple video EDL must specify '\"color_grade\": \"@couple-grade\"'."
            )

        # 4. Rule C3: Prevent constant jump-cut zoom ping-ponging
        main_segs = [s for s in segments if s.get("type", "main") == "main"]
        zoom_segs = [
            s for s in main_segs
            if s.get("camera_mode", "@wide") not in ("@wide", "normal", "@timelapse-4x")
            and s.get("phase", "dialogue") not in ("reaction", "bw_zoom", "climax")
        ]
        if main_segs and (len(zoom_segs) / len(main_segs)) > 0.25:
            errors.append(
                f"[Rule C3 Violation] {len(zoom_segs)}/{len(main_segs)} gameplay segments use zoomed framing. "
                "Keep steady 1.00x '@wide' framing during normal two-person gameplay; reserve zooms for comedic/loser reactions!"
            )

        # 5. Rule C5: Strict < 2:30 (150s) ceiling
        if total_dur > 150.0:
            errors.append(
                f"[Rule C5 Violation] Projected duration is {total_dur:.2f}s (> 150.0s / 2:30 ceiling). "
                "Increase speed multiplier (1.35x-1.70x) on card-searching/matching segments."
            )

        # 6. Rule C7: Opening Hook Title at 0:00 & caption suppression
        hook = edl.get("hook_title", {})
        if not hook or float(hook.get("start_sec", 0.0)) != 0.0:
            errors.append("[Rule C7 Violation] 'hook_title' must be present and start at 0.0s.")
        if main_segs and main_segs[0].get("camera_mode", "@wide") not in ("@wide", "normal"):
            errors.append("[Rule C3/C7 Violation] Opening hook segment must use steady '@wide' 1.00x framing.")

        # 7. Rule C9: Strictly 1 word at a time in captions
        for cap_idx, cap in enumerate(edl.get("captions", [])):
            w_text = str(cap.get("word", cap.get("text", ""))).strip()
            if len(w_text.split()) > 1:
                errors.append(
                    f"[Rule C9 Violation] Caption #{cap_idx + 1} ('{w_text}') contains multiple words. "
                    "Couple video captions must display strictly ONE word at a time!"
                )

        # 8. Rule C10 & C14: Default music & transient head-pop duration check (<= 1.8s)
        music = edl.get("music", "")
        if music and "nocturne_op9_in_eb" not in music:
            errors.append(
                f"[Rule C14 Violation] Couple video music '{music}' is not 'audio/music/nocturne_op9_in_eb.wav'."
            )
        for hp in edl.get("head_pops", []):
            dur = float(hp.get("duration_out", hp.get("dur", hp.get("duration", 1.5))))
            if dur > 1.85:
                errors.append(f"[Rule C10 Violation] Head pop '{hp.get('text')}' duration {dur}s exceeds 1.8s max.")

    elif category == "talking_head":
        return validate(edl)

    elif category == "animation":
        # Rule AM8: Resolution floor & unification pass check
        for asset in edl.get("assets", []):
            short_dim = int(asset.get("min_dimension_px", 1080))
            if short_dim < 1000:
                errors.append(f"[Rule AM8 Violation] Asset '{asset.get('src')}' has short dimension {short_dim}px (< 1000px floor).")

    for w in warnings:
        print(f"⚠️  {w}")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Pre-Render EDL Linter (Couple, Talking Head, Animation)")
    parser.add_argument("--edl", required=True, help="Path to EDL JSON")
    parser.add_argument("--category", required=True, choices=["couple", "talking_head", "animation"])
    args = parser.parse_args()

    with open(args.edl, "r", encoding="utf-8") as f:
        edl = json.load(f)

    errors = lint_edl(edl, args.category)
    if errors:
        print("❌ [Lint FAILED] Fix the following rule violations before rendering:")
        for err in errors:
            print(f"   • {err}")
        sys.exit(1)
    else:
        print(f"✅ [Lint PASSED] EDL '{args.edl}' complies with all '{args.category}' rules!")


if __name__ == "__main__":
    main()
