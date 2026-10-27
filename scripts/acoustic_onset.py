#!/usr/bin/env python3
"""
scripts/acoustic_onset.py
Refines raw ASR (Parakeet / Whisper) word timestamps using a 10ms sliding RMS
acoustic energy envelope and Stereo Left/Right speaker diarization (Angel = Left, Arthur = Right).

Why:
- Standard Whisper/ASR word start timestamps after pauses often bridge silence
  0.4s-1.0s early (causing premature caption/header spoilers).
- This script snaps every word's start timestamp forward to the exact 10ms frame
  where vocal energy exceeds the local noise floor (-32 dBFS), detects laughter/peak
  energy bursts, and tags Left vs Right speaker when a stereo track is provided.
"""

import argparse
import json
import math
import os
import wave
import array


def load_wav_16bit(wav_path: str):
    with wave.open(wav_path, "rb") as wf:
        n_channels = wf.getnchannels()
        sample_rate = wf.getframerate()
        n_frames = wf.getnframes()
        raw_bytes = wf.readframes(n_frames)
    samples = array.array("h")
    samples.frombytes(raw_bytes)
    return samples, sample_rate, n_channels


def compute_10ms_envelopes(samples, sample_rate: int, n_channels: int):
    win_samples = max(1, sample_rate // 100)  # 10ms window
    total_frames = len(samples) // n_channels
    n_windows = total_frames // win_samples

    rms_db = []
    lr_ratio = []  # > 0 means Left (Angel) louder, < 0 means Right (Arthur) louder

    for w in range(n_windows):
        base = w * win_samples * n_channels
        sum_sq = 0.0
        sum_l = 0.0
        sum_r = 0.0
        for i in range(win_samples):
            idx = base + i * n_channels
            if n_channels >= 2:
                l_val = samples[idx] / 32768.0
                r_val = samples[idx + 1] / 32768.0
                m_val = 0.5 * (l_val + r_val)
                sum_sq += m_val * m_val
                sum_l += l_val * l_val
                sum_r += r_val * r_val
            else:
                m_val = samples[idx] / 32768.0
                sum_sq += m_val * m_val

        mean_sq = sum_sq / win_samples
        db = 10.0 * math.log10(max(mean_sq, 1e-10))
        rms_db.append(round(db, 2))

        if n_channels >= 2:
            l_db = 10.0 * math.log10(max(sum_l / win_samples, 1e-10))
            r_db = 10.0 * math.log10(max(sum_r / win_samples, 1e-10))
            lr_ratio.append(round(l_db - r_db, 2))
        else:
            lr_ratio.append(0.0)

    return rms_db, lr_ratio


def extract_words_from_asr_json(data: dict):
    words = []
    # Support both Parakeet JSON ("sentences" -> "tokens"/"words") and Whisper JSON ("segments" -> "words")
    segments = data.get("segments") or data.get("sentences") or []
    for seg in segments:
        seg_words = seg.get("words") or seg.get("tokens") or []
        for w in seg_words:
            text = (w.get("word") or w.get("text") or "").strip()
            if not text:
                continue
            start = float(w.get("start", seg.get("start", 0.0)))
            end = float(w.get("end", seg.get("end", start + 0.15)))
            words.append({"word": text, "raw_start": round(start, 3), "raw_end": round(end, 3)})
    return words


def refine_words(words, rms_db, lr_ratio, threshold_db: float = -33.0):
    n_win = len(rms_db)
    refined = []
    for idx, w in enumerate(words):
        s_win = max(0, min(n_win - 1, int(w["raw_start"] * 100)))
        e_win = max(s_win + 1, min(n_win, int(w["raw_end"] * 100)))

        # If gap from previous word > 0.25s and raw_start - raw_end is wide (> 0.25s),
        # snap start forward to first 10ms window exceeding threshold_db
        prev_end = refined[-1]["end"] if refined else 0.0
        gap = w["raw_start"] - prev_end
        dur = w["raw_end"] - w["raw_start"]

        snapped_s_win = s_win
        if (gap > 0.20 or idx == 0) and dur > 0.22:
            for k in range(s_win, max(s_win + 1, e_win - 4)):
                if rms_db[k] >= threshold_db:
                    snapped_s_win = max(s_win, k - 1)  # 10ms pre-pad
                    break

        window_slice = rms_db[snapped_s_win:e_win] or [-50.0]
        peak_db = max(window_slice)
        lr_slice = lr_ratio[snapped_s_win:e_win] or [0.0]
        avg_lr = sum(lr_slice) / len(lr_slice)

        if avg_lr > 1.2:
            speaker = "Angel"
        elif avg_lr < -1.2:
            speaker = "Arthur"
        else:
            speaker = "Center"

        refined.append({
            "word": w["word"],
            "start": round(snapped_s_win * 0.01, 3),
            "end": round(w["raw_end"], 3),
            "raw_start": w["raw_start"],
            "peak_db": round(peak_db, 2),
            "is_stressed": peak_db >= -16.5,
            "speaker": speaker,
        })
    return refined


def main():
    parser = argparse.ArgumentParser(description="10ms RMS Acoustic Onset & Speaker Diarization Refiner")
    parser.add_argument("--wav", required=True, help="Path to 16kHz mono or stereo WAV")
    parser.add_argument("--json", required=True, help="Path to Parakeet or Whisper JSON transcript")
    parser.add_argument("--output", required=True, help="Output path for refined acoustic JSON")
    parser.add_argument("--threshold-db", type=float, default=-33.0, help="Vocal onset RMS threshold in dBFS")
    args = parser.parse_args()

    if not os.path.exists(args.wav) or not os.path.exists(args.json):
        print(f"⚠️  [AcousticOnset] Missing input files: {args.wav} or {args.json}")
        return

    samples, sr, ch = load_wav_16bit(args.wav)
    rms_db, lr_ratio = compute_10ms_envelopes(samples, sr, ch)

    with open(args.json, "r", encoding="utf-8") as f:
        asr_data = json.load(f)

    raw_words = extract_words_from_asr_json(asr_data)
    refined_words = refine_words(raw_words, rms_db, lr_ratio, args.threshold_db)

    first_speech_sec = refined_words[0]["start"] if refined_words else 0.0
    out_payload = {
        "source_wav": args.wav,
        "source_json": args.json,
        "sample_rate": sr,
        "channels": ch,
        "first_speech_onset_sec": first_speech_sec,
        "word_count": len(refined_words),
        "words": refined_words,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2, ensure_ascii=False)

    print(f"✅ [AcousticOnset] Refined {len(refined_words)} words (first syllable @ {first_speech_sec:.2f}s) -> {args.output}")


if __name__ == "__main__":
    main()
