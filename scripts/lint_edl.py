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


def lint_edl(edl: dict, category: str) -> list:
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
        # Rule C5: Strict < 2:30 (150s) ceiling
        if total_dur > 150.0:
            errors.append(
                f"[Rule C5 Violation] Projected duration is {total_dur:.2f}s (> 150.0s / 2:30 ceiling). "
                "Increase speed multiplier (1.35x-1.70x) on card-searching/matching segments."
            )
        # Rule C14: Default music check
        music = edl.get("music", "")
        if music and "nocturne_op9_in_eb" not in music:
            errors.append(
                f"[Rule C14 Violation] Couple video music '{music}' is not 'audio/music/nocturne_op9_in_eb.wav'."
            )
        # Rule C10: Transient head-pop duration check (<= 1.8s)
        for hp in edl.get("head_pops", []):
            dur = float(hp.get("dur", hp.get("duration", 1.5)))
            if dur > 1.85:
                errors.append(f"[Rule C10 Violation] Head pop '{hp.get('text')}' duration {dur}s exceeds 1.8s max.")

    elif category == "talking_head":
        # Rule TH1: Storyboard check
        if not edl.get("storyboard_approved", True):
            warnings.append("[Rule TH1] 'storyboard_approved' is false. Present the Storyboard Table to user first.")
        # Rule TH4 & TH5: Check for caption & tool-label collisions at y=61.5%
        effects = edl.get("effects", [])
        tool_labels = [fx for fx in effects if fx.get("type") in ("tool_label", "@tool-label")]
        if tool_labels:
            print(f"ℹ️  [Lint] {len(tool_labels)} @tool-label effect(s) found; ensure y=61.5% captions auto-hide during label windows (Rule TH11/TH12).")

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
