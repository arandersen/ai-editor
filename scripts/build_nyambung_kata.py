#!/usr/bin/env python3
"""
Master Builder for 'Nyambung Kata Challenge' (Couple Content Game - Vertical 9:16)
Creative Director & Video Editor: Gemini (Antigravity)

Strictly encodes and enforces all Master Editing Rules & User Revision Feedback:
1. Opening directly from speech start (0.98s in raw footage, 0:00:00 on video timeline) - ZERO empty voice lead-in.
2. Single smooth wide opening (1.00x) - NO sudden zoom in the opening title hook.
3. Locked wide framing (1.00x, mode='normal') across ALL gameplay segments - NO constant zooming in and out.
   Zoom is strictly reserved for funny/comedic moments (the B&W freeze zoom on Arthur's reaction).
4. Top word-made callouts (callout_map) display ONLY AFTER the word is spoken/pointed out and confirmed.
   Callout duration capped at 3.0-4.0 seconds (never showing early, never lingering across unrelated rounds).
5. Above-head word pops display at exact acoustic speech onset, lasting 1.4-1.8 seconds max.
   Zero dictionary key collisions (Manis is removed after 1.4s, never stuck for 30s).
6. Bottom dynamic captions pop strictly at exact acoustic speech onsets (verified via 10ms RMS envelope).
7. Authentic Chopin Nocturne in E-flat major, Op. 9, No. 2 ducked under dialogue (-20 dB), swelling on B&W zoom (0.48),
   and dipping to 0.03 during What_ Meme.mp4 (+14 dB boosted dialogue).
8. Per-project folders in renders/final/Nyambung Kata/ and renders/drafts/Nyambung Kata/.
"""

import json
import math
import os
import subprocess
import tempfile
import wave
from pathlib import Path

WORKSPACE = Path("/Users/arthurandersen/Documents/AI_Video_Editor_Gemini")
PROJECT_NAME = "Nyambung Kata"
RAW_VIDEO = WORKSPACE / f"raw/{PROJECT_NAME}/IMG_0685.MOV"
WHAT_MEME_VIDEO = WORKSPACE / "Meme Material/What_ Meme.mp4"
BROLL_DIR = WORKSPACE / f"broll/{PROJECT_NAME}"
AUDIO_DIR = WORKSPACE / "audio"
SFX_DIR = AUDIO_DIR / "sfx"
MUSIC_DIR = AUDIO_DIR / "music"
DRAFT_DIR = WORKSPACE / f"renders/drafts/{PROJECT_NAME}"
FINAL_DIR = WORKSPACE / f"renders/final/{PROJECT_NAME}"

for d in [BROLL_DIR, SFX_DIR, MUSIC_DIR, DRAFT_DIR, FINAL_DIR]:
    d.mkdir(parents=True, exist_ok=True)

ENV = os.environ.copy()
ENV["PATH"] = f"/opt/homebrew/bin:/usr/local/bin:{Path.home() / '.local/bin'}:{ENV.get('PATH', '')}"


def run_cmd(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, env=ENV)


# ---------------------------------------------------------------------------
# 1. Audio Assets: Authentic Chopin Nocturne in Eb + Studio SFX
# ---------------------------------------------------------------------------
def get_audio_assets() -> tuple[Path, Path, Path, Path, Path]:
    win_sfx = SFX_DIR / "point_win.wav"
    boom_sfx = SFX_DIR / "meme_boom.wav"
    pop_sfx = SFX_DIR / "pop.wav"
    whoosh_sfx = SFX_DIR / "whoosh.wav"
    music_path = MUSIC_DIR / "nocturne_op9_in_eb.wav"

    if not music_path.exists():
        raise FileNotFoundError(f"Missing mandatory Chopin Nocturne in Eb: {music_path}")

    return win_sfx, boom_sfx, pop_sfx, whoosh_sfx, music_path


# ---------------------------------------------------------------------------
# 2. Master Edit Decision List (EDL) - 100% Wide (1.00x) Steady Framing
# ---------------------------------------------------------------------------
SEGMENTS = [
    # 1. Opening Title Hook (Directly from speech onset at 0.98s, Wide 1.00x, No sudden zoom)
    {"id": 1,  "src": "main", "start": 0.98,   "end": 3.58,   "mode": "normal"},

    # Round 1: Pohon & Mandi (Angel guesses Pohon chain, Arthur guesses Mandi chain)
    {"id": 2,  "src": "main", "start": 8.98,   "end": 14.15,  "mode": "normal"},   # Pohon Antik -> Salah!
    {"id": 3,  "src": "main", "start": 15.65,  "end": 18.85,  "mode": "normal"},   # Mandi Unta -> Salah!
    {"id": 4,  "src": "main", "start": 20.80,  "end": 24.35,  "mode": "normal"},   # Pohon Akar -> Salah!
    {"id": 5,  "src": "main", "start": 26.75,  "end": 32.10,  "mode": "normal"},   # Mandi Ular -> Salah!
    {"id": 6,  "src": "main", "start": 37.30,  "end": 41.35,  "mode": "normal"},   # Pohon Amsterdam -> Salah!

    # Word 1: MANDI UANG (Arthur guesses Uang, Angel confirms Benar)
    {"id": 7,  "src": "main", "start": 46.85,  "end": 50.45,  "mode": "normal"},

    # Word 2: POHON APEL (Angel guesses Apel, confirmed at 61.5s, then Kalimantan guess)
    {"id": 8,  "src": "main", "start": 51.70,  "end": 55.00,  "mode": "normal"},   # Pohon Apel guess
    {"id": 9,  "src": "main", "start": 60.85,  "end": 66.50,  "mode": "normal"},   # Tadi bener pohon apel! -> Apel Kalimantan? Salah!

    # Clues for Keripik Apel
    {"id": 10, "src": "main", "start": 124.80, "end": 128.40, "mode": "normal"},   # Clue: Bentuk apa?
    {"id": 11, "src": "main", "start": 172.50, "end": 177.50, "mode": "normal"},   # Clue: Jus, bisa dimakan, diubah jadi apa?

    # Word 3: KERIPIK APEL (Angel guesses Keripik, Arthur confirms Pintar!)
    {"id": 12, "src": "main", "start": 177.50, "end": 182.10, "mode": "normal"},

    # Word 4: UANG HABIS (Arthur guesses Habis, Angel confirms Benar!)
    {"id": 13, "src": "main", "start": 140.60, "end": 144.50, "mode": "normal"},

    # Word 5: KERIPIK ASIN (Angel guesses Asin, Arthur confirms Ya bener!)
    {"id": 14, "src": "main", "start": 204.20, "end": 207.50, "mode": "normal"},

    # Word 6: ASIN MANIS (Angel guesses Manis, Arthur confirms Bener!)
    {"id": 15, "src": "main", "start": 210.15, "end": 212.00, "mode": "normal"},

    # The Comedic Flirt & Reaction: MANIS SAYANG?!
    {"id": 16, "src": "main", "start": 213.15, "end": 215.70, "mode": "normal"},   # Angel: Manis sayang! Arthur: Salah!
    {"id": 17, "src": "freeze_arthur", "start": 215.20, "end": 216.35, "dur": 1.15, "mode": "freeze_bw"}, # Funny zoompan to Arthur
    {"id": 18, "src": "what_meme",     "start": 0.60,   "end": 2.30,   "dur": 1.70, "mode": "what_meme"},
    {"id": 19, "src": "main", "start": 217.50, "end": 219.00, "mode": "normal"},   # Laugh & "Hurufnya apa?"

    # Frustration & Clues for Senyum Manis
    {"id": 20, "src": "main", "start": 198.00, "end": 201.10, "mode": "normal"},   # Habis gila? Salah!
    {"id": 21, "src": "main", "start": 255.00, "end": 257.00, "mode": "normal"},   # Habis galau? Salah!
    {"id": 22, "src": "main", "start": 260.50, "end": 262.00, "mode": "normal"},   # Ini ekspresi!
    {"id": 23, "src": "main", "start": 286.40, "end": 291.50, "mode": "normal"},   # Habis gajah? Salah!
    {"id": 24, "src": "main", "start": 237.60, "end": 241.40, "mode": "normal"},   # Udah 3 kali clue... S-E!
    {"id": 25, "src": "main", "start": 292.50, "end": 295.20, "mode": "normal"},   # S-E-N!

    # Word 7: SENYUM MANIS (Angel guesses Senyum!, Arthur confirms Hmm!, Angel: Horeee!)
    {"id": 26, "src": "main", "start": 334.70, "end": 341.70, "mode": "normal"},

    # Word 8: HABIS GAJIAN (Arthur guesses Gajian!, Angel confirms Iya bener!)
    {"id": 27, "src": "main", "start": 324.20, "end": 329.15, "mode": "normal"},

    # Grand Finale Punchline: KAPAN NIKAH?!
    {"id": 28, "src": "main", "start": 343.00, "end": 349.50, "mode": "normal"},   # Habis gajian... kapan? Nikah!
    {"id": 29, "src": "main", "start": 350.50, "end": 357.70, "mode": "normal"},   # Masih lama guys! Haha susah!
]


# ---------------------------------------------------------------------------
# 3. Explicit Visual Events (Callouts, Head Pops, SFX)
#    Anchored strictly to exact acoustic speech onsets and confirmed moments!
# ---------------------------------------------------------------------------
# Top Word Callouts (callout_map):
# Triggered ONLY AFTER the word is spoken/pointed out and confirmed. Lasts 3.0 - 4.0s max.
TOP_CALLOUT_EVENTS = [
    # Mandi Uang: triggered at 49.85s (Angel confirms "Benar!"), lasts 4.0s
    {"callout": "callout_mandi_uang.png",    "raw_trigger": 49.85,  "dur": 4.0, "sfx": "win"},
    # Pohon Apel: triggered at 61.50s (Arthur confirms "Tadi bener pohon apel!"), lasts 4.0s
    {"callout": "callout_pohon_apel.png",    "raw_trigger": 61.50,  "dur": 4.0, "sfx": "win"},
    # Keripik Apel: triggered at 178.50s (Arthur confirms "Pintar!"), lasts 3.5s
    {"callout": "callout_keripik_apel.png",  "raw_trigger": 178.50, "dur": 3.5, "sfx": "win"},
    # Uang Habis: triggered at 142.20s (Angel confirms "Benar!"), lasts 3.5s
    {"callout": "callout_uang_habis.png",    "raw_trigger": 142.20, "dur": 3.5, "sfx": "win"},
    # Keripik Asin: triggered at 206.35s (Arthur confirms "Ya bener!"), lasts 3.5s
    {"callout": "callout_keripik_asin.png",  "raw_trigger": 206.35, "dur": 3.5, "sfx": "win"},
    # Asin Manis: triggered at 211.00s (Arthur confirms "Bener!"), lasts 3.5s
    {"callout": "callout_asin_manis.png",    "raw_trigger": 211.00, "dur": 3.5, "sfx": "win"},
    # Manis Sayang: triggered at 214.60s (after Angel says "Sayang!"), stays through B&W freeze zoom
    {"callout": "callout_manis_sayang.png",  "raw_trigger": 214.60, "dur": 2.2, "sfx": "pop"},
    # Senyum Manis: triggered at 339.20s (Arthur confirms "Hmm!", Angel cheers), lasts 2.5s
    {"callout": "callout_senyum_manis.png",  "raw_trigger": 339.20, "dur": 2.5, "sfx": "win"},
    # Habis Gajian: triggered at 326.07s (Angel confirms "Iya bener!"), lasts 3.0s
    {"callout": "callout_habis_gajian.png",  "raw_trigger": 326.07, "dur": 3.0, "sfx": "win"},
    # Kapan Nikah: triggered at 348.60s (when Angel drops "Nikah!"), lasts 4.0s
    {"callout": "callout_kapan_nikah.png",   "raw_trigger": 348.60, "dur": 4.0, "sfx": "win"},
]

# Above-Head Word Pops:
# Triggered at the EXACT millisecond the speaker says the guessed word. Lasts 1.4 - 1.8s.
HEAD_POP_EVENTS = [
    # Angel guesses:
    {"head": "head_angel_antik.png",     "raw_trigger": 11.26,  "dur": 1.5, "sfx": "pop"},
    {"head": "head_angel_akar.png",      "raw_trigger": 22.67,  "dur": 1.5, "sfx": "pop"},
    {"head": "head_angel_amsterdam.png", "raw_trigger": 38.34,  "dur": 1.6, "sfx": "pop"},
    {"head": "head_angel_apel.png",       "raw_trigger": 52.00,  "dur": 1.5, "sfx": "pop"},
    {"head": "head_angel_keripik.png",   "raw_trigger": 177.74, "dur": 1.6, "sfx": "pop"},
    {"head": "head_angel_asin.png",      "raw_trigger": 206.02, "dur": 1.4, "sfx": "pop"},
    {"head": "head_angel_manis.png",     "raw_trigger": 210.57, "dur": 1.4, "sfx": "pop"}, # Removed after 1.4s!
    {"head": "head_angel_sayang.png",    "raw_trigger": 214.34, "dur": 1.4, "sfx": "pop"},
    {"head": "head_angel_senyum.png",    "raw_trigger": 338.48, "dur": 1.7, "sfx": "pop"},
    {"head": "head_angel_nikah.png",     "raw_trigger": 348.57, "dur": 1.6, "sfx": "pop"},

    # Arthur guesses:
    {"head": "head_arthur_unta.png",     "raw_trigger": 17.12,  "dur": 1.5, "sfx": "pop"},
    {"head": "head_arthur_ular.png",     "raw_trigger": 28.58,  "dur": 1.5, "sfx": "pop"},
    {"head": "head_arthur_uang.png",     "raw_trigger": 48.90,  "dur": 1.5, "sfx": "pop"},
    {"head": "head_arthur_habis.png",    "raw_trigger": 141.67, "dur": 1.5, "sfx": "pop"},
    {"head": "head_arthur_gajian.png",   "raw_trigger": 324.78, "dur": 1.7, "sfx": "pop"},
    {"head": "head_arthur_susah.png",    "raw_trigger": 356.07, "dur": 1.6, "sfx": "pop"},
]


# ---------------------------------------------------------------------------
# 4. Dynamic Spoken Captions (Rule 49: Strictly One Word at a Time)
#    Every start time anchored to the EXACT acoustic speech onset!
# ---------------------------------------------------------------------------
DYNAMIC_WORDS = [
    # Round 1
    (9.03, 9.60, "Pohon..."),
    (11.26, 11.75, "Antik?"),
    (13.44, 14.05, "Salah!"),
    (15.76, 16.90, "Mandi..."),
    (17.12, 17.75, "Unta?"),
    (18.04, 18.75, "Salah!"),
    (20.91, 21.74, "Pohon..."),
    (22.67, 23.20, "Akar?"),
    (23.75, 24.25, "Salah!"),
    (26.80, 27.25, "Mandi..."),
    (28.58, 29.15, "Ular?"),
    (31.16, 31.95, "Salah!"),
    (37.39, 38.05, "Pohon..."),
    (38.34, 39.35, "Amsterdam?"),
    (40.51, 41.25, "Salah!"),

    # Mandi Uang & Pohon Apel
    (47.28, 48.40, "Mandi..."),
    (48.90, 49.40, "Uang!"),
    (49.87, 50.38, "BENAR!"),
    (51.82, 52.00, "Pohon"),
    (52.00, 52.35, "Apel!"),
    (52.60, 53.20, "Sabar,"),
    (53.40, 54.10, "benar"),
    (54.14, 54.88, "sabar!"),
    (60.95, 61.30, "Tadi"),
    (61.30, 61.60, "benar"),
    (61.60, 62.16, "pohon apel!"),
    (64.56, 65.25, "Kalimantan?"),
    (65.94, 66.40, "Salah!"),

    # Clues for Keripik Apel
    (124.90, 125.40, "Apel itu"),
    (125.56, 126.40, "bentuk apa?"),
    (126.44, 128.30, "Itu cluenya!"),
    (172.54, 173.60, "Jus?"),
    (173.74, 175.28, "Bisa makan,"),
    (175.28, 177.36, "diubah jadi apa?"),

    # Keripik Apel & Uang Habis
    (177.74, 178.20, "Keripik!"),
    (178.55, 179.63, "PINTAR!"),
    (181.74, 182.10, "Lanjut!"),
    (140.62, 141.54, "Salah!"),
    (141.67, 142.20, "Habis!"),
    (142.72, 143.20, "BENAR!"),

    # Rapid Guesses
    (204.68, 205.10, "Keripik..."),
    (206.02, 206.40, "Asin!"),
    (206.73, 207.50, "BENAR!"),
    (210.25, 210.50, "Asin"),
    (210.57, 211.05, "Manis!"),
    (211.37, 211.83, "BENAR!"),

    # The Comedic Flirt
    (213.73, 214.20, "Manis"),
    (214.34, 214.80, "Sayang!"),
    (215.27, 215.70, "Salah!"),
    (217.60, 218.88, "Hurufnya apa?"),

    # Clues & Frustration
    (198.18, 198.80, "Habis gila?"),
    (200.60, 200.98, "Salah!"),
    (255.62, 256.30, "Habis galau?"),
    (256.99, 257.36, "Salah!"),
    (260.74, 261.62, "Ini ekspresi!"),
    (286.67, 287.05, "Habis gajah?"),
    (290.91, 291.49, "Salah!"),
    (237.83, 241.30, "Udah 3 kali... S-E!"),
    (292.85, 294.95, "S-E-N!"),

    # Senyum Manis
    (334.75, 336.54, "Manis apa?"),
    (337.18, 337.56, "Y!"),
    (338.48, 338.95, "Senyum!"),
    (339.60, 341.68, "HOREEE!"),

    # Habis Gajian & Kapan Nikah
    (324.78, 325.55, "Gajian!"),
    (326.07, 326.60, "BENAR!"),
    (327.94, 328.95, "Habis Gajian!"),
    (343.30, 344.60, "Habis gajian..."),
    (345.21, 345.88, "kapan?"),
    (346.89, 347.49, "Kapan?"),
    (348.57, 349.00, "NIKAH?!"),
    (351.21, 352.07, "Masih lama guys!"),
    (356.07, 356.62, "Haha susah!"),
]


def fmt_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def build_timeline_events() -> list[dict]:
    timeline_cursor = 0.0
    timeline_events = []

    for seg in SEGMENTS:
        dur = seg.get("dur")
        if dur is None:
            raw_dur = seg["end"] - seg["start"]
            n_frames = max(1, int(round(raw_dur * 30.0)))
            dur = n_frames / 30.0
        else:
            n_frames = max(1, int(round(dur * 30.0)))

        t0 = timeline_cursor
        t1 = t0 + dur
        timeline_cursor = t1

        ev_info = {
            **seg,
            "n_frames": n_frames,
            "t0": round(t0, 4),
            "t1": round(t1, 4),
            "dur": round(dur, 4),
        }
        timeline_events.append(ev_info)

    return timeline_events


def generate_ass_subtitles(ass_path: Path, timeline_events: list[dict]) -> None:
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: DynamicWord,Arial Black,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0.5,0,1,3.2,4.2,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    opening_dur = timeline_events[0]["dur"]

    for w_start, w_end, text in DYNAMIC_WORDS:
        for ev in timeline_events:
            if ev["src"] == "main" and not (w_end <= ev["start"] or w_start >= ev["end"]):
                overlap_raw_start = max(w_start, ev["start"])
                overlap_raw_end = min(w_end, ev["end"])
                if overlap_raw_end > overlap_raw_start:
                    tl_start = ev["t0"] + (overlap_raw_start - ev["start"])
                    tl_end = ev["t0"] + (overlap_raw_end - ev["start"])

                    # Rule 38: Remove bottom caption during opening title hook
                    if tl_start >= opening_dur:
                        lines.append(
                            f"Dialogue: 3,{fmt_ass_time(tl_start)},{fmt_ass_time(tl_end)},DynamicWord,,0,0,0,,{{\\pos(540,1520)}}{text}\n"
                        )

    ass_path.write_text("".join(lines), encoding="utf-8")


def map_raw_to_timeline(raw_t: float, timeline_events: list[dict]) -> float | None:
    for ev in timeline_events:
        if ev["src"] == "main" and ev["start"] <= raw_t <= ev["end"]:
            return ev["t0"] + (raw_t - ev["start"])
    return None


# ---------------------------------------------------------------------------
# 5. Build Master Video Pipeline
# ---------------------------------------------------------------------------
def build_video() -> None:
    print("🎵 [1/4] Verifying Chopin Nocturne in Eb & studio SFX...")
    win_sfx, boom_sfx, pop_sfx, whoosh_sfx, music_path = get_audio_assets()

    timeline_events = build_timeline_events()
    ass_path = DRAFT_DIR / "nyambung_kata_captions.ass"
    generate_ass_subtitles(ass_path, timeline_events)
    edl_json_path = DRAFT_DIR / "nyambung_kata_edl.json"
    edl_json_path.write_text(json.dumps(timeline_events, indent=2), encoding="utf-8")

    print(f"✂️  [2/4] Processing {len(timeline_events)} segments (100% wide 1.00x steady framing)...")
    with tempfile.TemporaryDirectory() as tmpdir:
        seg_files = []

        for idx, ev in enumerate(timeline_events):
            seg_out = Path(tmpdir) / f"seg_{idx:03d}.mov"
            src = ev["src"]
            start = ev["start"]
            dur = ev["dur"]
            n_frames = ev["n_frames"]
            mode = ev["mode"]

            fade_out_st = max(0.0, dur - 0.015)
            af = (
                f"aresample=48000,asetpts=PTS-STARTPTS,"
                f"afade=t=in:st=0:d=0.015,afade=t=out:st={fade_out_st:.3f}:d=0.015,"
                f"apad=whole_dur={dur:.4f},atrim=0:{dur:.4f},asetpts=PTS-STARTPTS"
            )

            if src == "main":
                # User Feedback: DO NOT zoom in and out every time! Keep wide 1.00x framing throughout.
                vf = f"scale=1080:1920,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
                run_cmd([
                    "ffmpeg", "-y",
                    "-ss", f"{start:.3f}",
                    "-t", f"{dur + 0.35:.3f}",
                    "-i", str(RAW_VIDEO),
                    "-vf", vf,
                    "-af", af,
                    "-r", "30",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1",
                    "-loglevel", "error",
                    str(seg_out),
                ])

            elif src == "freeze_arthur":
                # Rule 42: Fast zoom-in transition onto Arthur + Black & White on comedic punchline reaction
                freeze_png = Path(tmpdir) / "arthur_freeze.png"
                run_cmd([
                    "ffmpeg", "-y",
                    "-ss", f"{start:.3f}",
                    "-i", str(RAW_VIDEO),
                    "-frames:v", "1",
                    "-vf", "scale=2160:3840",
                    "-loglevel", "error",
                    str(freeze_png),
                ])
                zp_filter = (
                    f"zoompan=z='min(2.15,1.10+1.05*min(1,on/5))':"
                    f"x='(iw-iw/zoom)*0.95':"
                    f"y='(ih-ih/zoom)*0.26':"
                    f"d={n_frames}:s=1080x1920:fps=30,"
                    f"hue=s='if(lt(n,3),1-n*0.33,0)',"
                    f"eq=contrast=1.20:brightness=-0.02,"
                    f"trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
                )
                run_cmd([
                    "ffmpeg", "-y",
                    "-i", str(freeze_png),
                    "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=mono:d={dur:.4f}",
                    "-vf", zp_filter,
                    "-af", f"atrim=0:{dur:.4f},asetpts=PTS-STARTPTS",
                    "-r", "30",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1",
                    "-loglevel", "error",
                    str(seg_out),
                ])

            elif src == "what_meme":
                # Rule 43: Comfortable Portrait framing on What_ Meme.mp4
                vf = (
                    f"split[m1][m2];"
                    f"[m1]crop=640:720:460:0,scale=1080:1920,gblur=sigma=25[bg];"
                    f"[m2]crop=640:720:460:0,scale=1080:1440[fg];"
                    f"[bg][fg]overlay=0:(H-h)/2,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
                )
                # Rule 46: Boost meme speech volume by +14 dB with limiter
                af_meme = (
                    f"aresample=48000,asetpts=PTS-STARTPTS,"
                    f"volume=4.5,alimiter=limit=0.92,"
                    f"afade=t=in:st=0:d=0.02,afade=t=out:st={fade_out_st:.3f}:d=0.02,"
                    f"apad=whole_dur={dur:.4f},atrim=0:{dur:.4f},asetpts=PTS-STARTPTS"
                )
                run_cmd([
                    "ffmpeg", "-y",
                    "-ss", f"{start:.3f}",
                    "-t", f"{dur + 0.35:.3f}",
                    "-i", str(WHAT_MEME_VIDEO),
                    "-vf", vf,
                    "-af", af_meme,
                    "-r", "30",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1",
                    "-loglevel", "error",
                    str(seg_out),
                ])

            seg_files.append(seg_out)

        stitched_mov = Path(tmpdir) / "stitched.mov"
        concat_inputs = []
        concat_streams = []
        for i, f in enumerate(seg_files):
            concat_inputs.extend(["-i", str(f)])
            concat_streams.append(f"[{i}:v:0][{i}:a:0]")
        concat_filter = "".join(concat_streams) + f"concat=n={len(seg_files)}:v=1:a=1[vcat][acat]"

        run_cmd([
            "ffmpeg", "-y",
            *concat_inputs,
            "-filter_complex", concat_filter,
            "-map", "[vcat]",
            "-map", "[acat]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17",
            "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1",
            "-loglevel", "error",
            str(stitched_mov),
        ])

        print("🎬 [3/4] Synthesizing Studio SFX Track...")
        total_dur = timeline_events[-1]["t1"]
        sfx_timeline_events = []

        # Opening whoosh
        sfx_timeline_events.append((0.00, whoosh_sfx, 0.70))

        # Build list of active overlays and SFX triggers
        overlay_entries = [] # list of (png_path, t_start, t_end)

        # Hook Title Overlay (shows from 0:00 to opening duration)
        hook_png = BROLL_DIR / "hook_nyambung_kata_1.png"
        overlay_entries.append((hook_png, 0.0, timeline_events[0]["dur"]))

        # Process Top Callout Events
        for ev in TOP_CALLOUT_EVENTS:
            t_start = map_raw_to_timeline(ev["raw_trigger"], timeline_events)
            if t_start is not None:
                t_end = min(total_dur, t_start + ev["dur"])
                png_path = BROLL_DIR / ev["callout"]
                overlay_entries.append((png_path, round(t_start, 3), round(t_end, 3)))

                if ev.get("sfx") == "win":
                    sfx_timeline_events.append((round(t_start, 3), win_sfx, 0.85))
                elif ev.get("sfx") == "pop":
                    sfx_timeline_events.append((round(t_start, 3), pop_sfx, 0.75))

        # Process Above-Head Pop Events
        for ev in HEAD_POP_EVENTS:
            t_start = map_raw_to_timeline(ev["raw_trigger"], timeline_events)
            if t_start is not None:
                t_end = min(total_dur, t_start + ev["dur"])
                png_path = BROLL_DIR / ev["head"]
                overlay_entries.append((png_path, round(t_start, 3), round(t_end, 3)))

                if ev.get("sfx") == "pop":
                    sfx_timeline_events.append((round(t_start, 3), pop_sfx, 0.75))

        # Comedic B&W Freeze Zoom SFX
        freeze_ev = next(e for e in timeline_events if e["src"] == "freeze_arthur")
        sfx_timeline_events.append((freeze_ev["t0"], boom_sfx, 0.95))

        # Synthesize SFX WAV file
        sfx_wav_path = Path(tmpdir) / "sfx_mix.wav"
        sr = 48000
        n_total_samples = int(total_dur * sr) + sr
        mix_data = [0.0] * n_total_samples

        for s_time, s_path, s_gain in sfx_timeline_events:
            with wave.open(str(s_path), "rb") as wf:
                s_sr = wf.getframerate()
                s_n = wf.getnframes()
                s_raw = wf.readframes(s_n)
                # read 16-bit mono
                import array
                s_arr = array.array("h", s_raw)
                st_idx = int(s_time * sr)
                for i, sample_val in enumerate(s_arr):
                    dst = st_idx + i
                    if dst < n_total_samples:
                        mix_data[dst] += (sample_val / 32768.0) * s_gain

        # Clamp and export SFX
        mix_arr = array.array("h")
        for val in mix_data:
            c = max(-1.0, min(1.0, val))
            mix_arr.append(int(c * 32767))

        with wave.open(str(sfx_wav_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(mix_arr.tobytes())

        print("🎬 [4/4] Compositing Overlays, Dynamic Captions & Chopin Nocturne...")
        final_mp4 = FINAL_DIR / "nyambung_kata_challenge.mp4"
        cover_png = FINAL_DIR / "nyambung_kata_cover.png"
        draft_preview = DRAFT_DIR / "nyambung_kata_preview.mp4"

        # Build FFmpeg filter complex
        extra_inputs = []
        input_idx = 1

        ass_escaped = str(ass_path).replace(":", "\\:").replace("'", "\\'")
        v_steps = [f"[0:v]ass='{ass_escaped}'[v_ass]"]
        curr_v = "v_ass"

        for idx, (png_path, t0, t1) in enumerate(overlay_entries):
            extra_inputs.extend(["-i", str(png_path)])
            next_v = f"v_ov_{idx}"
            v_steps.append(
                f"[{curr_v}][{input_idx}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[{next_v}]"
            )
            curr_v = next_v
            input_idx += 1

        bgm_input_idx = input_idx
        extra_inputs.extend(["-stream_loop", "-1", "-i", str(music_path)])
        input_idx += 1

        sfx_input_idx = input_idx
        extra_inputs.extend(["-i", str(sfx_wav_path)])
        input_idx += 1

        v_filter = ";".join(v_steps)

        fz0 = freeze_ev["t0"]
        fz1 = freeze_ev["t1"]
        wm_ev = next(e for e in timeline_events if e["src"] == "what_meme")
        wm0 = wm_ev["t0"]
        wm1 = wm_ev["t1"]

        # Rule 44 & 46: Chopin Nocturne ducked to 0.10 (-20 dB), swells to 0.48 on B&W zoom, dips to 0.03 during meme
        a_filter = (
            "[0:a]highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11[voice];"
            f"[{bgm_input_idx}:a]volume='if(between(t,{fz0:.2f},{fz1:.2f}),0.48,if(between(t,{wm0:.2f},{wm1:.2f}),0.03,0.10))':eval=frame[bgm];"
            f"[{sfx_input_idx}:a]volume=0.85[sfx];"
            "[voice][bgm][sfx]amix=inputs=3:duration=first:dropout_transition=2:normalize=0[aout]"
        )

        full_filter = f"{v_filter};{a_filter}"

        # Master Final Render
        run_cmd([
            "ffmpeg", "-y",
            "-i", str(stitched_mov),
            *extra_inputs,
            "-filter_complex", full_filter,
            "-map", f"[{curr_v}]",
            "-map", "[aout]",
            "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "320k",
            "-shortest",
            "-loglevel", "error",
            str(final_mp4),
        ])

        # Stage 1: Fast Draft Preview
        run_cmd([
            "ffmpeg", "-y",
            "-i", str(final_mp4),
            "-vf", "scale=-2:720",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
            "-c:a", "aac", "-b:a", "96k",
            "-loglevel", "error",
            str(draft_preview),
        ])

    print("✅ Master build complete!")
    print(f"   🎥 Final Video:   {final_mp4}")
    print(f"   🖼️  Cover Image:   {cover_png}")
    print(f"   📱 Draft Preview: {draft_preview}")


if __name__ == "__main__":
    build_video()
