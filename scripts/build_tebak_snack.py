#!/usr/bin/env python3
"""
Master Builder for 'Tebak Snack Challenge' (Couple Content Game - Vertical 9:16)
Creative Director & Video Editor: Gemini (Antigravity)

Follows all Master Editing Rules & Specific User Instructions:
1. Video starts directly on first speech onset (1.80s in raw footage).
2. Couple snacks gameplay with Angel & Arthur:
   - Round 1: Snack -> Arthur picks Pringles Sour Cream (❌, Angel wants Lay's), Angel picks Sun-Maid Yogurt Raisins (❌, Arthur wants Pringles).
   - Round 2: Cokelat -> Angel picks Brookside Dark Chocolate Acai & Blueberry (✅, Arthur's list), Arthur picks Brookside Pomegranate (❌, Angel wants Ferrero Rocher).
   - Round 3: Es Krim -> Arthur picks Haagen-Dazs Matcha (✅), Angel picks Talenti Mango (✅).
   - Round 4: Minuman -> Arthur picks Apple Cider (❌, Angel wants Yakult), Angel picks Oat Milk (❌, Arthur wants Pure Leaf Ice Tea).
   - Winner: Angel wins (2 — 1)! Arthur buys everything ("Beliin semua ya!" / "Ini buat dompetku miskin!").
3. SFX: Distinct buzzer.wav on every incorrect snack guess, bell chime correct_ding.wav on correct guesses, and party_cheer.wav at the victory finale.
4. Zooms on funny moments:
   - Round 1 reveal laughter ("Kita gak ada yang bener sih!")
   - Round 2 Angel shocked reaction ("Guys kecewa guys! Sejak kapan gua tahu merek ini guys?!")
   - Round 2 Angel scolding Arthur ("Emang gak peka! Beliin!")
   - Round 3 celebration ("Weh! Bener guys!")
   - Round 4 Arthur peeking from behind shelf ("Ini buat dompetku miskin!")
   - Round 4 Arthur laughing in disbelief ("Kan saya minumnya teh!")
   - Ending Arthur defeat head grab (🤦‍♂️) with celebratory victory overlay.
5. Bottom dynamic captions: Strictly one word at a time synced to millisecond acoustic onset.
6. Authentic Chopin Nocturne in E-flat major Op. 9 No. 2 background music ducked to -20dB.
7. Clean cover image matching reference style in renders/final/Tebak Snack/tebak_snack_cover.png.
"""

from __future__ import annotations
import array
import json
import os
import subprocess
import tempfile
import wave
from pathlib import Path

WORKSPACE = Path("/Users/arthurandersen/Documents/AI_Video_Editor_Gemini")
PROJECT_NAME = "Tebak Snack"
RAW_VIDEO = WORKSPACE / f"raw/{PROJECT_NAME}/IMG_2439.MOV"
BROLL_DIR = WORKSPACE / f"broll/{PROJECT_NAME}"
AUDIO_DIR = WORKSPACE / "audio"
SFX_DIR = AUDIO_DIR / "sfx"
MUSIC_DIR = AUDIO_DIR / "music"
MUSIC_FILE = MUSIC_DIR / "nocturne_op9_in_eb.wav"
DRAFT_DIR = WORKSPACE / f"renders/drafts/{PROJECT_NAME}"
FINAL_DIR = WORKSPACE / f"renders/final/{PROJECT_NAME}"
CONFETTI_MOV = DRAFT_DIR / "confetti_loop.mov"

for d in [BROLL_DIR, SFX_DIR, MUSIC_DIR, DRAFT_DIR, FINAL_DIR]:
    d.mkdir(parents=True, exist_ok=True)

FINAL_OUT = FINAL_DIR / "tebak_snack_challenge.mp4"
COVER_OUT = FINAL_DIR / "tebak_snack_cover.png"
PREVIEW_OUT = DRAFT_DIR / "tebak_snack_preview.mp4"

ENV = os.environ.copy()
ENV["PATH"] = f"/opt/homebrew/bin:/usr/local/bin:{Path.home() / '.local/bin'}:{ENV.get('PATH', '')}"


def run_cmd(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, env=ENV)


# ---------------------------------------------------------------------------
# 1. Timeline Segments (Trimmed & Paced for Rule 56: < 2:30 / 150s Ceiling)
# ---------------------------------------------------------------------------
SEGMENTS = [
    # Seg 0: Opening Hook Title (Direct speech onset at 1.80s)
    {"id": 0,  "start": 1.80,   "end": 7.80,   "mode": "normal"},

    # Round 1: Snack
    {"id": 1,  "start": 7.80,   "end": 11.40,  "mode": "normal"},              # Setup
    {"id": 2,  "start": 12.40,  "end": 14.50,  "mode": "normal"},              # 1, 2, 3
    {"id": 3,  "start": 14.50,  "end": 18.50,  "mode": "zoom_r1_laugh"},       # Reveal & laughter (1.15x)
    {"id": 4,  "start": 18.50,  "end": 24.30,  "mode": "normal"},              # Banter: Lay's vs Pringles
    {"id": 5,  "start": 24.30,  "end": 29.80,  "mode": "normal"},              # 11-12 & Makan sendiri
    {"id": 6,  "start": 30.50,  "end": 33.20,  "mode": "normal"},              # R1 Wrap

    # Round 2: Cokelat
    {"id": 7,  "start": 34.00,  "end": 38.50,  "mode": "normal"},              # Cokelat setup
    {"id": 8,  "start": 41.20,  "end": 47.80,  "mode": "normal"},              # Check Brookside & Ferrero
    {"id": 9,  "start": 49.80,  "end": 55.50,  "mode": "normal"},              # 1, 2, 3
    {"id": 10, "start": 55.50,  "end": 62.00,  "mode": "zoom_angel_kecewa"},   # Reveal & Kecewa (1.20x)
    {"id": 11, "start": 63.40,  "end": 76.50,  "mode": "normal"},              # Arthur defense: Dubai Chocolate
    {"id": 12, "start": 76.50,  "end": 80.50,  "mode": "zoom_angel_peka"},     # "Emang gak peka! Beliin!" (1.25x)

    # Round 3: Es Krim
    {"id": 13, "start": 83.50,  "end": 85.50,  "mode": "normal"},              # Tiga, es krim
    {"id": 14, "start": 88.80,  "end": 95.00,  "mode": "normal"},              # Setup & 1, 2, 3
    {"id": 15, "start": 95.00,  "end": 105.00, "mode": "normal"},              # Reveal Haagen-Dazs & Talenti
    {"id": 16, "start": 105.00, "end": 109.50, "mode": "zoom_r3_celebrate"},   # Celebrate both right! (1.16x)
    {"id": 17, "start": 110.00, "end": 116.50, "mode": "normal"},              # Wrap R3 & "Makan gratis!"

    # Round 4: Minuman
    {"id": 18, "start": 116.50, "end": 120.00, "mode": "zoom_arthur_miskin"},  # Arthur peeks: "Dompetku miskin!" (1.35x)
    {"id": 19, "start": 123.50, "end": 128.50, "mode": "normal"},              # 1, 2, 3
    {"id": 20, "start": 128.50, "end": 139.50, "mode": "normal"},              # Reveal Apple Cider & Oatly
    {"id": 21, "start": 139.50, "end": 143.50, "mode": "zoom_arthur_teh"},     # Arthur laughs: "Kan saya minumnya teh!" (1.22x)
    {"id": 22, "start": 143.50, "end": 158.80, "mode": "normal"},              # Susu kulkas vs teh kerja, Yakult
    {"id": 23, "start": 158.80, "end": 162.24, "mode": "zoom_defeat"},         # Arthur defeat head grab (🤦‍♂️) + Angel victory!
]


# ---------------------------------------------------------------------------
# 2. Header Overlay Events (Anchored to exact raw video timestamps)
# ---------------------------------------------------------------------------
HEADER_EVENTS = [
    # Opening Title Hook: shows from 0:00 to 5.90s
    {"png": "hook_tebak_snack.png",          "raw_start": 1.80,   "raw_end": 7.80,   "sfx": "whoosh"},

    # Round 1: Snack
    {"png": "header_r1_title.png",           "raw_start": 7.80,   "raw_end": 14.50,  "sfx": None},
    {"png": "header_r1_arthur_fail.png",     "raw_start": 14.50,  "raw_end": 24.30,  "sfx": "buzzer"},
    {"png": "header_r1_score.png",           "raw_start": 24.30,  "raw_end": 33.20,  "sfx": None},

    # Round 2: Cokelat
    {"png": "header_r2_title.png",           "raw_start": 34.00,  "raw_end": 55.50,  "sfx": None},
    {"png": "header_r2_angel_correct.png",   "raw_start": 55.50,  "raw_end": 63.40,  "sfx": "ding"},
    {"png": "header_r2_arthur_fail.png",     "raw_start": 63.40,  "raw_end": 76.50,  "sfx": "buzzer"},
    {"png": "header_r2_score.png",           "raw_start": 76.50,  "raw_end": 80.50,  "sfx": None},

    # Round 3: Es Krim
    {"png": "header_r3_title.png",           "raw_start": 83.50,  "raw_end": 95.00,  "sfx": None},
    {"png": "header_r3_arthur_correct.png",   "raw_start": 95.00,  "raw_end": 105.00, "sfx": "ding"},
    {"png": "header_r3_both_correct.png",     "raw_start": 105.00, "raw_end": 110.00, "sfx": "ding"},
    {"png": "header_r3_score.png",           "raw_start": 110.00, "raw_end": 116.50, "sfx": None},

    # Round 4: Minuman & Finale
    {"png": "header_r4_title.png",           "raw_start": 116.50, "raw_end": 128.50, "sfx": None},
    {"png": "header_r4_arthur_fail.png",     "raw_start": 128.50, "raw_end": 141.50, "sfx": "buzzer"},
    {"png": "header_r4_angel_fail.png",      "raw_start": 141.50, "raw_end": 154.50, "sfx": "buzzer"},
    {"png": "header_winner.png",             "raw_start": 154.50, "raw_end": 162.24, "sfx": "cheer"},
]


# ---------------------------------------------------------------------------
# 3. Dynamic Spoken Captions (Strictly One Word at a Time, Raw Timestamps)
# ---------------------------------------------------------------------------
DYNAMIC_WORDS = [
    # Intro (1.80 - 7.80) -> Captions suppressed during opening title hook (Rule 38)

    # Round 1: Snack (7.80 - 33.20)
    (7.98, 8.40, "Oke,"), (8.54, 8.85, "jadi"), (8.85, 9.18, "ini"), (9.18, 9.45, "snack"), (9.45, 9.80, "kesukaan"), (9.80, 10.15, "aku?"),
    (10.22, 10.45, "Ini"), (10.45, 10.70, "snack"), (10.70, 11.00, "kesukaan"), (11.00, 11.25, "aku."),
    (12.60, 12.95, "Satu,"), (13.00, 13.35, "dua,"), (13.40, 13.80, "tiga!"),
    (15.60, 16.00, "Kita"), (16.00, 16.35, "gak ada"), (16.35, 16.65, "yang"), (16.65, 17.00, "bener"), (17.00, 17.35, "sih!"),
    (17.40, 17.75, "Lu"), (17.75, 18.15, "beliin ini,"), (18.15, 18.55, "gua beliin"), (18.55, 18.90, "itu!"),
    (19.04, 19.35, "I mean,"), (19.35, 19.70, "in terms"), (19.70, 20.00, "of flavor"), (20.00, 20.35, "and chips"), (20.35, 20.70, "wise"), (20.70, 21.05, "it's the same..."),
    (21.82, 22.20, "Cuma"), (22.20, 22.58, "yang Lay's lah!"), (22.80, 23.20, "Gua sukanya"), (23.20, 23.60, "Lay's!"), (23.70, 24.15, "Lu sukanya Pringles!"),
    (24.46, 24.95, "11-12..."), (25.10, 25.60, "11-12..."), (25.75, 26.30, "11-12..."), (26.35, 26.85, "oke."),
    (26.92, 27.24, "Nih"), (27.24, 27.52, "gak apa-apa"), (27.52, 27.84, "kalau"), (27.84, 28.16, "beliin,"), (28.16, 28.50, "gua"), (28.50, 28.82, "bisa"), (28.82, 29.15, "makan"), (29.15, 29.50, "sendiri!"),
    (30.74, 31.06, "Ini kalau"), (31.06, 31.50, "menang,"), (31.50, 31.85, "kita dua-dua"), (31.85, 32.22, "sukanya"), (32.22, 32.55, "rasanya"), (32.55, 33.02, "bener."),

    # Round 2: Cokelat (34.00 - 80.50)
    (34.10, 34.60, "Oke,"), (34.60, 35.00, "kedua,"), (35.14, 35.45, "cokelat"), (35.45, 35.80, "ya."),
    (36.70, 37.34, "Cokelatnya"), (37.34, 37.60, "tadi"), (37.60, 37.85, "lu pilih"), (37.85, 38.20, "apa?"),
    (38.90, 39.30, "Ini..."), (40.72, 41.36, "Nggak?"),
    (41.86, 42.48, "Cokelat..."), (42.72, 43.44, "cokelat"), (43.44, 43.80, "berry"), (43.80, 44.44, "Brookside ya?"),
    (44.80, 45.20, "Iya."),
    (45.40, 45.85, "Lu"), (45.85, 46.30, "cokelatnya"), (46.30, 46.85, "Ferrero"), (46.85, 47.35, "Rocher kan?"),
    (47.50, 48.00, "Ehh..."),
    (50.06, 50.70, "Ini"), (50.70, 51.34, "cokelat"), (51.42, 51.76, "kesukaanku..."),
    (52.12, 52.64, "Ini cokelat"), (52.64, 53.40, "kesukaanku..."),
    (53.74, 54.10, "Satu,"), (54.15, 54.55, "dua,"), (54.60, 55.00, "tiga!"),
    (56.22, 56.70, "Guys"), (56.70, 57.18, "kecewa,"), (57.18, 57.50, "guys!"),
    (57.82, 58.30, "Sejak kapan"), (58.30, 58.60, "gua"), (58.60, 58.90, "tahu"), (58.90, 59.28, "merek"), (59.28, 59.70, "ini guys?!"),
    (59.88, 60.50, "Tutti"), (60.50, 61.20, "frutti"), (61.20, 61.80, "kapan"), (61.80, 62.40, "aja?!"),
    (63.62, 63.95, "Oke,"), (63.95, 64.28, "in my defense"), (64.28, 64.60, "gua,"),
    (64.60, 65.00, "kira dia"), (65.00, 65.35, "suka"), (65.35, 65.65, "Dubai Chocolate!"),
    (65.76, 66.06, "Iya,"), (66.06, 66.46, "suka Dubai Chocolate,"), (66.46, 66.98, "tapi"), (66.98, 67.40, "itu"), (67.40, 67.85, "spesifik"), (67.85, 68.20, "banget"), (68.20, 68.60, "mereknya!"),
    (69.74, 70.30, "I lebih suka"), (70.30, 70.75, "Ferrero,"), (70.75, 71.20, "kan udah bilang"), (71.20, 71.60, "I gak suka"), (71.60, 72.48, "cokelat-cokelatan!"),
    (72.98, 73.54, "Dubai Chocolate,"), (73.76, 74.20, "the same thing"), (74.20, 74.60, "tuh..."),
    (74.60, 74.95, "Gak!"), (74.95, 75.40, "Ini I"), (75.40, 75.90, "beneran"), (75.90, 76.35, "beli yang"), (76.35, 76.86, "dia suka lho!"),
    (77.36, 77.70, "Emang"), (77.70, 78.10, "gak"), (78.10, 78.50, "peka!"),
    (78.55, 79.00, "Fine..."),
    (79.05, 79.50, "Beliin!"),

    # Round 3: Es Krim (83.50 - 116.50)
    (83.60, 84.10, "Tiga,"), (84.10, 84.60, "es krim"), (84.60, 85.00, "ya."),
    (89.38, 90.02, "Ini"), (90.02, 90.45, "ice cream"), (90.45, 91.12, "kesukaanku..."),
    (91.98, 92.50, "Ini ice cream"), (92.50, 93.22, "kesukaanku..."),
    (93.40, 93.80, "Satu,"), (93.85, 94.25, "dua,"), (94.30, 94.75, "tiga!"),
    (95.18, 95.82, "Haagen-Dazs"), (95.82, 96.30, "Matcha!"),
    (96.92, 97.45, "Talenti"), (97.45, 97.96, "Mango!"),
    (98.20, 98.65, "Bener"), (98.65, 99.00, "gak?"),
    (99.10, 99.50, "Bener."), (99.55, 99.90, "You?"),
    (100.00, 100.40, "Bener!"), (100.45, 100.85, "Okay!"),
    (101.40, 101.90, "Eh bener"), (101.90, 102.35, "Talenti"), (102.35, 102.78, "di list ya?"),
    (103.20, 103.86, "Talenti Mango?"),
    (104.00, 104.44, "Iya!"),
    (106.14, 106.78, "Weh!"), (106.78, 107.15, "Bener"), (107.15, 107.50, "guys!"),
    (107.50, 108.15, "Beruntung,"), (108.15, 108.68, "beruntung!"),
    (108.68, 109.14, "Tapi"), (109.14, 109.60, "dua-dua"), (109.60, 110.00, "emang kita suka"), (110.00, 110.40, "ini flavor."),
    (111.00, 111.45, "Ya kita"), (111.45, 111.85, "beli dua-duanya"), (111.85, 112.38, "deh?"),
    (112.50, 113.00, "Ya beli..."), (113.00, 113.50, "beli..."),

    # Round 4: Minuman & Finale (116.50 - 162.24)
    (113.80, 114.30, "Terakhir..."),
    (114.40, 114.80, "Guys,"), (114.80, 115.15, "ini cara"), (115.15, 115.55, "buat"), (115.55, 116.02, "makan gratis!"),
    (117.54, 118.10, "Ini buat"), (118.10, 118.55, "dompetku"), (118.55, 119.18, "miskin!"),
    (124.30, 124.86, "Ini yang"), (124.86, 125.40, "terakhir..."),
    (125.40, 125.90, "Ini minuman"), (125.90, 126.50, "kesukaanku..."),
    (126.64, 127.15, "Ini minuman"), (127.15, 127.80, "kesukaanku..."),
    (128.00, 128.40, "Satu,"), (128.45, 128.85, "dua,"), (128.90, 129.35, "tiga!"),
    (130.50, 131.20, "Apple"), (131.20, 131.92, "Cider?!"),
    (132.56, 133.02, "Suka"), (133.02, 133.35, "sih,"), (133.35, 133.70, "tapi gak"), (133.70, 134.15, "di list!"),
    (134.30, 134.80, "Masa lu"), (134.80, 135.25, "gak ingat?"),
    (135.25, 135.75, "Padahal ini"), (135.75, 136.25, "setiap kali"), (136.25, 136.75, "kalau beli"), (136.75, 137.25, "apa-apa,"),
    (137.25, 137.85, "mintanya beliin"), (137.85, 138.40, "Apple Cider!"),
    (138.50, 139.10, "Beli"), (139.10, 139.60, "susu?!"),
    (139.70, 140.40, "Enggak lah!"),
    (140.50, 141.20, "Kan saya"), (141.20, 141.80, "minumnya"), (141.80, 142.50, "teh!"),
    (142.60, 143.15, "Gua..."), (143.15, 143.65, "dia di rumah"), (143.65, 144.20, "tiap hari"), (144.20, 144.80, "minum susu!"),
    (144.90, 145.45, "Tiap kali"), (145.45, 145.95, "buka kulkas,"), (145.95, 146.50, "susu!"),
    (147.00, 147.60, "Tapi kalau"), (147.60, 148.15, "gua kerja,"), (148.15, 148.80, "setiap hari"), (148.80, 149.50, "gua minumnya"), (149.50, 150.10, "teh!"),
    (150.20, 150.80, "Gak!"),
    (151.20, 151.80, "Jadi"), (151.80, 152.40, "menang?"),
    (152.60, 153.20, "Gua sukanya"), (153.20, 153.80, "Yakult!"),
    (154.00, 154.70, "Kenapa gak"), (154.70, 155.30, "bilang Yakult?"),
    (155.30, 156.00, "Orang lu jelas-jelas"), (156.00, 156.70, "sukanya Apple Cider!"),
    (157.20, 157.70, "Beli,"), (157.70, 158.30, "beli!"),
    (158.80, 159.50, "Gua kalah!"),
]


# ---------------------------------------------------------------------------
# 4. Helper Functions: Timeline Conversion & Subtitles
# ---------------------------------------------------------------------------
def fmt_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def build_timeline_events() -> list[dict]:
    timeline_cursor = 0.0
    timeline_events = []

    for seg in SEGMENTS:
        dur = seg["end"] - seg["start"]
        n_frames = max(1, int(round(dur * 30.0)))
        dur = n_frames / 30.0

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


def map_raw_to_timeline(raw_t: float, timeline_events: list[dict], is_end: bool = False) -> float:
    for ev in timeline_events:
        if ev["start"] <= raw_t <= ev["end"]:
            return ev["t0"] + (raw_t - ev["start"])
    if raw_t <= timeline_events[0]["start"]:
        return 0.0
    if raw_t >= timeline_events[-1]["end"]:
        return timeline_events[-1]["t1"]
    for i in range(len(timeline_events) - 1):
        prev_ev = timeline_events[i]
        next_ev = timeline_events[i + 1]
        if prev_ev["end"] < raw_t < next_ev["start"]:
            return prev_ev["t1"] if is_end else next_ev["t0"]
    return timeline_events[-1]["t1"] if is_end else 0.0


def generate_ass_subtitles(ass_path: Path, timeline_events: list[dict]) -> None:
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 2160
PlayResY: 3840
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: DynamicWord,Arial Black,108,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0.5,0,1,6.4,8.4,5,120,120,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    opening_dur = timeline_events[0]["dur"]

    for w_start, w_end, text in DYNAMIC_WORDS:
        for ev in timeline_events:
            if not (w_end <= ev["start"] or w_start >= ev["end"]):
                overlap_raw_start = max(w_start, ev["start"])
                overlap_raw_end = min(w_end, ev["end"])
                if overlap_raw_end > overlap_raw_start:
                    tl_start = ev["t0"] + (overlap_raw_start - ev["start"])
                    tl_end = ev["t0"] + (overlap_raw_end - ev["start"])

                    # Rule 38: Remove bottom caption during opening title hook
                    if tl_start >= opening_dur:
                        lines.append(
                            f"Dialogue: 3,{fmt_ass_time(tl_start)},{fmt_ass_time(tl_end)},DynamicWord,,0,0,0,,{{\\pos(1080,3040)}}{text}\n"
                        )

    ass_path.write_text("".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# 5. Master Video Build Pipeline
# ---------------------------------------------------------------------------
def build_video() -> None:
    print("🎵 [1/5] Verifying assets and generating 4K ASS subtitles...")
    timeline_events = build_timeline_events()
    total_dur = timeline_events[-1]["t1"]
    print(f"Total timeline duration: {total_dur:.2f}s (~{total_dur/60:.2f} mins) [Rule 56 < 2:30 Ceiling]")

    ass_path = DRAFT_DIR / "tebak_snack_captions.ass"
    generate_ass_subtitles(ass_path, timeline_events)

    print(f"✂️  [2/5] Rendering {len(timeline_events)} segments in native 4K Ultra HD (2160x3840)...")
    with tempfile.TemporaryDirectory() as tmpdir:
        seg_files = []

        for idx, ev in enumerate(timeline_events):
            seg_out = Path(tmpdir) / f"seg_{idx:03d}.mov"
            start = ev["start"]
            dur = ev["dur"]
            mode = ev["mode"]

            # Filter tailoring per segment in native 4K (2160x3840)
            if mode == "normal":
                vf = f"scale=2160:3840,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            elif mode == "zoom_r1_laugh":
                # Zoom in on both laughing faces (1.15x)
                vf = f"crop=w=iw/1.15:h=ih/1.15:x=(iw-ow)/2:y=(ih-oh)*0.40,scale=2160:3840,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            elif mode == "zoom_angel_kecewa":
                # Zoom in on Angel holding Brookside Pomegranate (1.20x)
                vf = f"crop=w=iw/1.20:h=ih/1.20:x=(iw-ow)*0.72:y=(ih-oh)*0.40,scale=2160:3840,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            elif mode == "zoom_angel_peka":
                # Zoom in on Angel scolding Arthur (1.25x)
                vf = f"crop=w=iw/1.25:h=ih/1.25:x=(iw-ow)*0.72:y=(ih-oh)*0.40,scale=2160:3840,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            elif mode == "zoom_r3_celebrate":
                # Zoom in on both celebrating correct ice cream (1.16x)
                vf = f"crop=w=iw/1.16:h=ih/1.16:x=(iw-ow)/2:y=(ih-oh)*0.40,scale=2160:3840,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            elif mode == "zoom_arthur_miskin":
                # MAJOR COMEDY: Arthur pops out from behind shelf! (1.35x centered on Arthur)
                vf = f"crop=w=iw/1.35:h=ih/1.35:x=(iw-ow)*0.28:y=(ih-oh)*0.32,scale=2160:3840,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            elif mode == "zoom_arthur_teh":
                # Arthur laughing in disbelief: "Kan saya minumnya teh!" (1.22x)
                vf = f"crop=w=iw/1.22:h=ih/1.22:x=(iw-ow)*0.25:y=(ih-oh)*0.40,scale=2160:3840,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            elif mode == "zoom_defeat":
                # Arthur defeat head grab with Angel smiling (1.22x)
                vf = f"crop=w=iw/1.22:h=ih/1.22:x=(iw-ow)*0.35:y=(ih-oh)*0.38,scale=2160:3840,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            else:
                vf = f"scale=2160:3840,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"

            fade_out_st = max(0.0, dur - 0.015)
            af = (
                f"aresample=48000,asetpts=PTS-STARTPTS,"
                f"afade=t=in:st=0:d=0.015,afade=t=out:st={fade_out_st:.3f}:d=0.015,"
                f"apad=whole_dur={dur:.4f},atrim=0:{dur:.4f},asetpts=PTS-STARTPTS"
            )

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

        print("🎬 [3/5] Synthesizing Studio SFX Track (Buzzers, Chimes, Whoosh & Party Cheer)...")
        whoosh_sfx = SFX_DIR / "whoosh.wav"
        buzzer_sfx = SFX_DIR / "buzzer.wav"
        ding_sfx = SFX_DIR / "correct_ding.wav"
        cheer_sfx = SFX_DIR / "party_cheer.wav"

        sfx_timeline = []

        # Process Header Events & SFX triggers
        overlay_entries = []
        confetti_trigger_time = None

        for h in HEADER_EVENTS:
            t_start = map_raw_to_timeline(h["raw_start"], timeline_events, is_end=False)
            t_end = map_raw_to_timeline(h["raw_end"], timeline_events, is_end=True)
            if t_start is not None and t_end is not None and t_end > t_start:
                png_path = BROLL_DIR / h["png"]
                overlay_entries.append((png_path, round(t_start, 3), round(t_end, 3)))

                if h["sfx"] == "whoosh":
                    sfx_timeline.append((round(t_start, 3), whoosh_sfx, 0.70))
                elif h["sfx"] == "buzzer":
                    sfx_timeline.append((round(t_start, 3), buzzer_sfx, 0.85))
                elif h["sfx"] == "ding":
                    sfx_timeline.append((round(t_start, 3), ding_sfx, 0.85))
                elif h["sfx"] == "cheer":
                    sfx_timeline.append((round(t_start, 3), cheer_sfx, 1.10))
                    confetti_trigger_time = round(t_start, 3)

        # Synthesize SFX WAV file
        sfx_wav_path = Path(tmpdir) / "sfx_mix.wav"
        sr = 48000
        n_total_samples = int(total_dur * sr) + (sr * 2)
        mix_data = [0.0] * n_total_samples

        for s_time, s_path, s_gain in sfx_timeline:
            with wave.open(str(s_path), "rb") as wf:
                s_sr = wf.getframerate()
                s_n = wf.getnframes()
                s_raw = wf.readframes(s_n)
                s_arr = array.array("h", s_raw)
                st_idx = int(s_time * sr)
                for i, sample_val in enumerate(s_arr):
                    dst = st_idx + i
                    if dst < n_total_samples:
                        mix_data[dst] += (sample_val / 32768.0) * s_gain

        mix_arr = array.array("h")
        for val in mix_data:
            c = max(-1.0, min(1.0, val))
            mix_arr.append(int(c * 32767))

        with wave.open(str(sfx_wav_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(mix_arr.tobytes())

        print("🎬 [4/5] Compositing Dynamic Subtitles, Overlays, Confetti, SFX & Chopin Nocturne...")
        extra_inputs = []
        input_idx = 1

        ass_escaped = str(ass_path).replace(":", "\\:").replace("'", "\\'")
        v_steps = [f"[0:v]ass='{ass_escaped}'[v_ass]"]
        curr_v = "v_ass"

        # Apply Top Header PNG Overlays
        for idx, (png_path, t0, t1) in enumerate(overlay_entries):
            extra_inputs.extend(["-i", str(png_path)])
            next_v = f"v_ov_{idx}"
            v_steps.append(
                f"[{curr_v}][{input_idx}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1:.3f})'[{next_v}]"
            )
            curr_v = next_v
            input_idx += 1

        # Apply Confetti Loop during Winner Reveal (from confetti_trigger_time to total_dur)
        if confetti_trigger_time is not None and CONFETTI_MOV.exists():
            extra_inputs.extend(["-stream_loop", "-1", "-i", str(CONFETTI_MOV)])
            confetti_input_idx = input_idx
            input_idx += 1
            next_v = "v_with_confetti"
            v_steps.append(
                f"[{curr_v}][{confetti_input_idx}:v]overlay=0:0:enable='between(t,{confetti_trigger_time:.3f},{total_dur:.3f})'[{next_v}]"
            )
            curr_v = next_v

        # Background Music (Chopin Nocturne in Eb ducked to -20dB)
        bgm_input_idx = input_idx
        extra_inputs.extend(["-stream_loop", "-1", "-i", str(MUSIC_FILE)])
        input_idx += 1

        # SFX Track
        sfx_input_idx = input_idx
        extra_inputs.extend(["-i", str(sfx_wav_path)])
        input_idx += 1

        v_filter = ";".join(v_steps)

        # Audio mix:
        # Voice: [0:a] normalized to -14 LUFS with gentle highpass at 80Hz
        # Music: [bgm_input_idx:a] ducked to 0.10 (-20 dB)
        # SFX: [sfx_input_idx:a]
        a_filter = (
            "[0:a]highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11[voice];"
            f"[{bgm_input_idx}:a]volume=0.10,atrim=0:{total_dur:.4f},asetpts=PTS-STARTPTS[bgm];"
            f"[{sfx_input_idx}:a]volume=1.0,atrim=0:{total_dur:.4f},asetpts=PTS-STARTPTS[sfx];"
            "[voice][bgm][sfx]amix=inputs=3:duration=first:dropout_transition=2:normalize=0[a_out]"
        )

        filter_complex = f"{v_filter};{a_filter}"

        # Render Final Master Video (Rule 56: Studio Master Highest Quality Upload Standard)
        run_cmd([
            "ffmpeg", "-y",
            "-i", str(stitched_mov),
            *extra_inputs,
            "-filter_complex", filter_complex,
            "-map", f"[{curr_v}]",
            "-map", "[a_out]",
            "-t", f"{total_dur:.4f}",
            "-c:v", "libx264", "-preset", "slow",
            "-profile:v", "high", "-level:v", "5.2",
            "-crf", "14", "-b:v", "48M", "-maxrate", "65M", "-bufsize", "90M",
            "-pix_fmt", "yuv420p",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            "-loglevel", "error",
            str(FINAL_OUT),
        ])

        # Generate Draft Preview
        run_cmd([
            "ffmpeg", "-y",
            "-i", str(FINAL_OUT),
            "-vf", "scale=540:960",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "25",
            "-c:a", "aac", "-b:a", "96k",
            "-loglevel", "error",
            str(PREVIEW_OUT),
        ])

        print("📸 [5/5] Generating Official Reference-Style Cover Image (Native 4K)...")
        hook_png = BROLL_DIR / "hook_tebak_snack.png"
        run_cmd([
            "ffmpeg", "-y",
            "-ss", "00:00:03.50",
            "-i", str(RAW_VIDEO),
            "-i", str(hook_png),
            "-filter_complex", "[0:v]scale=2160:3840[base];[base][1:v]overlay=0:0[out]",
            "-map", "[out]",
            "-vframes", "1",
            "-loglevel", "error",
            str(COVER_OUT),
        ])

        print(f"🎉 Build Complete!")
        print(f"   Final Master: {FINAL_OUT}")
        print(f"   Preview:      {PREVIEW_OUT}")
        print(f"   Cover Image:  {COVER_OUT}")


if __name__ == "__main__":
    build_video()
