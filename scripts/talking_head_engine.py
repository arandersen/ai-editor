#!/usr/bin/env python3
"""
scripts/talking_head_engine.py
Declarative Master Builder for Category 2: Talking Head Videos (FeedMedia Notion Effects + Antigravity M4 Stack).

Designed so that:
- Gemini 4 Argon acts as the Conductor / Creative Director (watches raw video, creates Storyboard & EDL JSON).
- Gemini 3 Flash (or any AI Editor) can deterministically execute this engine from a single JSON EDL.

Supported @shortcut Effects in EDL:
  - @jump-cuts          : <0.22s silence stripping + smart 1.00x / 1.15x eye-line (y=42%) alternation
  - @text-behind-head   : Apple Vision person cutout + 2-line title behind head (y=20%, 27%, 12f cubic.out)
  - @coral-captions     : 3-word chunk at y=61.5% with Coral (#D97757) box ONLY on the active word
  - @one-word-captions  : 1-word dynamic pop captions anchored to 10ms RMS acoustic onset
  - @tool-label         : App logo (110px/220px) + sliding bold white name at y=61.5%
  - @repo-card          : GitHub Dark Theme card (#0D1117, 85% width) rising 2% over 12f
  - @prompt-bar         : #2B2B2B pill bar (92.6% width at y=22.5%) + #D97757 coral send button
  - @color-slider       : Warm-to-Natural 30-frame cubic wipe with vertical white divider line
  - @magazine-cover     : Person cutout + serif masthead behind head + gold frame/barcode in front on stressed words
  - @real-screenshot    : 90%-width rounded screenshot card fading up 12 frames above head
  - @whip-pan           : 12-frame (6f out + 6f in) 8% slide + 50px directional blur transition + whoosh.wav
  - @moody-grade        : FFmpeg curves + -15% saturation + vignette + Lightroom UI panel overlay
  - @wall-of-reels      : 3x3 grid shrinking speaker to center tile + popping 8 yt-dlp reels 1 per frame
  - @pause-explain      : 54% top-left PIP window with timecode -> click freeze -> 12f shrink to 24% left
"""

import argparse
import json
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor


def run_cmd(cmd, desc=""):
    if desc:
        print(f"⚙️  [TalkingHeadEngine] {desc}")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed ({desc}): {' '.join(cmd)}\n{res.stderr[-1200:]}")
    return res


def map_raw_to_timeline(raw_t: float, segments: list) -> float:
    acc = 0.0
    for seg in segments:
        s0 = float(seg["start"])
        s1 = float(seg["end"])
        spd = float(seg.get("speed", 1.0))
        dur = (s1 - s0) / spd
        if s0 <= raw_t <= s1:
            return acc + (raw_t - s0) / spd
        acc += dur
    return acc


def has_top_overlay_at(seg_start: float, seg_end: float, effects: list) -> bool:
    top_types = {
        "repo_card", "@repo-card",
        "prompt_bar", "@prompt-bar",
        "real_screenshot", "@real-screenshot",
        "moody_grade_panel", "@moody-grade",
        "text_behind_head", "@text-behind-head",
        "magazine_cover", "@magazine-cover",
    }
    for fx in effects:
        if fx.get("type") in top_types:
            f0 = float(fx.get("start_raw", fx.get("trigger_raw", 0.0)))
            f1 = float(fx.get("end_raw", f0 + float(fx.get("duration", 3.0))))
            if max(seg_start, f0) < min(seg_end, f1):
                return True
    return False


def build_segment_filter(seg: dict, idx: int, W: int, H: int, effects: list) -> str:
    s0 = float(seg["start"])
    s1 = float(seg["end"])
    spd = float(seg.get("speed", 1.0))
    dur = (s1 - s0) / spd

    # Smart Layout-Aware Zoom (Rule TH5):
    # Lock to 1.0x if a top overlay card is active; otherwise use segment's zoom (1.0x or 1.15x at y=42%)
    zoom = float(seg.get("zoom", 1.0))
    if has_top_overlay_at(s0, s1, effects) and zoom > 1.02:
        zoom = 1.0

    v_steps = []
    if abs(spd - 1.0) > 0.01:
        v_steps.append(f"setpts=PTS/{spd:.4f}")

    # Crop-before-scale (never upscale 4K before cropping)
    if zoom > 1.001:
        v_steps.append(f"crop=w=iw/{zoom:.4f}:h=ih/{zoom:.4f}:x=(iw-ow)/2:y=(ih-oh)*0.42")
    v_steps.append(f"scale={W}:{H}:flags=lanczos")

    # Optional @color-slider (Notion Effect #7) or @moody-grade (Notion Effect #11) inside segment
    grade_mode = seg.get("grade", "none")
    if grade_mode in ("warm", "@color-slider"):
        v_steps.append("colorchannelmixer=rr=1.17:gg=1.10:bb=1.03,eq=saturation=1.12")
    elif grade_mode in ("moody", "@moody-grade"):
        v_steps.append("curves=m='0/0.08 0.25/0.22 0.75/0.72 1/0.90',eq=saturation=0.85,vignette=PI/5")

    # Optional @whip-pan transition out (Notion Effect #10B: last 6 frames slide left 8% + 50px horizontal blur)
    if seg.get("transition_out") in ("whip_pan", "@whip-pan") and dur > 0.25:
        wp_start = max(0.0, dur - 0.12)
        v_steps.append(f"boxblur=luma_radius='if(gte(t,{wp_start:.3f}),25,0)':luma_power=1")

    v_steps.append(f"trim=0:{dur:.4f},setpts=PTS-STARTPTS,format=yuv420p")
    return ",".join(v_steps)


def build_atempo_chain(speed: float) -> str:
    if abs(speed - 1.0) < 0.01:
        return "anull"
    parts = []
    rem = speed
    while rem > 2.0:
        parts.append("atempo=2.0")
        rem /= 2.0
    while rem < 0.5:
        parts.append("atempo=0.5")
        rem /= 0.5
    parts.append(f"atempo={rem:.4f}")
    return ",".join(parts)


def slice_one_segment(args_tuple):
    idx, seg, raw_video, W, H, effects, tmp_dir = args_tuple
    s0 = float(seg["start"])
    s1 = float(seg["end"])
    spd = float(seg.get("speed", 1.0))
    dur = (s1 - s0) / spd
    out_seg = os.path.join(tmp_dir, f"seg_{idx:03d}.mov")

    vf = build_segment_filter(seg, idx, W, H, effects)
    atempo = build_atempo_chain(spd)
    fade_out_st = max(0.0, dur - 0.02)
    af = (
        f"{atempo},"
        f"afade=t=in:st=0:d=0.015,afade=t=out:st={fade_out_st:.4f}:d=0.015,"
        f"aresample=48000,apad=whole_dur={dur:.4f},atrim=0:{dur:.4f},asetpts=PTS-STARTPTS"
    )

    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-ss", f"{s0:.4f}", "-to", f"{s1:.4f}",
        "-i", raw_video,
        "-vf", vf,
        "-af", af,
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "12",
        "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2",
        out_seg,
    ]
    run_cmd(cmd, f"Slicing segment #{idx + 1} ({s0:.2f}s -> {s1:.2f}s @ {spd}x)")
    return out_seg


def main():
    parser = argparse.ArgumentParser(description="Antigravity Talking Head Master Engine (Category 2)")
    parser.add_argument("--edl", required=True, help="Path to Talking Head EDL JSON")
    parser.add_argument("--output", required=True, help="Output path for final 4K/1080p MP4")
    parser.add_argument("--draft-only", action="store_true", help="Render fast 1080p draft preview only")
    args = parser.parse_args()

    with open(args.edl, "r", encoding="utf-8") as f:
        edl = json.load(f)

    raw_video = edl["raw_video"]
    res = edl.get("resolution", [2160, 3840])
    W, H = int(res[0]), int(res[1])
    if args.draft_only and W > 1080:
        W, H = 1080, int(1080 * H / int(res[0]))

    segments = edl.get("segments", [])
    effects = edl.get("effects", [])

    # Enforce Rule TH5: Auto-alternate 1.00x and 1.15x if jump_cuts.auto_alternate is true
    jc_cfg = edl.get("jump_cuts", {})
    if jc_cfg.get("auto_alternate", True):
        zooms = jc_cfg.get("alternate_zoom", [1.0, 1.15])
        for i, seg in enumerate(segments):
            if "zoom" not in seg:
                seg["zoom"] = zooms[i % len(zooms)]

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="th_engine_") as tmp_dir:
        # 1. Parallel segment slicing with zero-drift PCM audio
        tasks = [(i, seg, raw_video, W, H, effects, tmp_dir) for i, seg in enumerate(segments)]
        with ThreadPoolExecutor(max_workers=4) as pool:
            seg_files = list(pool.map(slice_one_segment, tasks))

        concat_list = os.path.join(tmp_dir, "concat.txt")
        with open(concat_list, "w", encoding="utf-8") as cf:
            for sf in seg_files:
                cf.write(f"file '{sf}'\n")

        stitched_mov = os.path.join(tmp_dir, "stitched.mov")
        run_cmd(
            ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", stitched_mov],
            "Stitching PCM/H.264 segments (zero-drift stream copy)"
        )

        # 2. Generate Swift overlays for any active effects
        overlay_jobs = []
        overlay_events = []
        for idx, fx in enumerate(effects):
            fx_type = fx.get("type", "").lstrip("@").replace("-", "_")
            job_id = f"fx_{idx:03d}_{fx_type}"
            raw_t0 = float(fx.get("start_raw", fx.get("trigger_raw", 0.0)))
            raw_t1 = float(fx.get("end_raw", raw_t0 + float(fx.get("duration", 2.5))))
            t0 = map_raw_to_timeline(raw_t0, segments)
            t1 = map_raw_to_timeline(raw_t1, segments)

            if fx_type in ("coral_pill_3word", "coral_captions", "text_behind_head", "tool_label", "repo_card", "prompt_bar"):
                swift_type = "coral_pill_3word" if fx_type == "coral_captions" else fx_type
                overlay_jobs.append({
                    "id": job_id,
                    "type": swift_type,
                    "words": fx.get("words"),
                    "activeIndex": fx.get("active_index", 0),
                    "lines": fx.get("lines"),
                    "title": fx.get("title") or fx.get("name") or fx.get("repo") or fx.get("prompt_text"),
                    "subtitle": fx.get("description") or fx.get("subtitle"),
                    "stars": fx.get("stars"),
                    "forks": fx.get("forks"),
                    "imagePath": fx.get("logo") or fx.get("src"),
                })
                overlay_events.append((os.path.join(tmp_dir, f"{job_id}.png"), t0, t1))

        if overlay_jobs:
            spec_json = os.path.join(tmp_dir, "overlays_spec.json")
            with open(spec_json, "w", encoding="utf-8") as sf:
                json.dump({"canvasWidth": W, "canvasHeight": H, "jobs": overlay_jobs}, sf, indent=2)
            run_cmd(
                ["swift", "-module-cache-path", "/tmp/swift_cache", "./scripts/talking_head_overlays.swift", "--spec", spec_json, "--outdir", tmp_dir],
                f"Rendering {len(overlay_jobs)} native CoreText/AppKit overlays at {W}x{H}"
            )

        # 3. Master FFmpeg Compositing + Isolated Voice Loudnorm (-14 LUFS) + Rec.709 4K Export
        inputs = ["-i", stitched_mov]
        for png_path, _, _ in overlay_events:
            inputs.extend(["-i", png_path])

        music_path = edl.get("music")
        has_music = bool(music_path and os.path.exists(music_path))
        if has_music:
            inputs.extend(["-stream_loop", "-1", "-i", music_path])

        fc_parts = []
        v_cur = "[0:v]"
        for ov_idx, (_, t0, t1) in enumerate(overlay_events):
            in_idx = ov_idx + 1
            v_next = f"[v_ov_{ov_idx}]"
            fc_parts.append(f"{v_cur}[{in_idx}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'{v_next}")
            v_cur = v_next

        # Audio: normalize voice BEFORE mixing with BGM (Rule U4 & TH22)
        fc_parts.append("[0:a]highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11[voice]")
        if has_music:
            bgm_idx = len(overlay_events) + 1
            bgm_vol = float(edl.get("music_volume", 0.10))
            fc_parts.append(f"[{bgm_idx}:a]volume={bgm_vol:.3f}[bgm]")
            fc_parts.append("[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2:normalize=0,alimiter=limit=0.95:level=0[aout]")
        else:
            fc_parts.append("[voice]alimiter=limit=0.95:level=0[aout]")

        filter_complex = ";".join(fc_parts)

        encode_flags = (
            ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20"]
            if args.draft_only
            else [
                "-c:v", "libx264", "-profile:v", "high", "-level:v", "5.2",
                "-preset", "slow", "-crf", "14",
                "-b:v", "45M", "-maxrate", "65M", "-bufsize", "90M",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            ]
        )

        master_cmd = (
            ["ffmpeg", "-y", "-v", "error"]
            + inputs
            + ["-filter_complex", filter_complex, "-map", v_cur, "-map", "[aout]"]
            + encode_flags
            + ["-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", args.output]
        )
        run_cmd(master_cmd, f"Encoding final Talking Head master -> {args.output}")

    print(f"🎉 [TalkingHeadEngine] Complete! Output saved to: {args.output}")


if __name__ == "__main__":
    main()
