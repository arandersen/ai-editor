#!/usr/bin/env python3
"""
Master Builder for 'Lengkapin Kata Challenge' (Couple Content Game - Vertical 9:16)
Creative Director & Video Editor: Gemini 4 Argon (Antigravity)

V2 Fixes Applied (User Revision):
1. Strict No-Spoiler Top Word Header Timing:
   - Completed word headers (CACING, ANJINGS, ALAS, ANGELS, AMIDIS, AKTIFIS, GANAS, DOMINO, KAKAK, MALUKU)
     are NEVER shown during the countdown ("Satu, dua, tiga...").
   - Each header card appears strictly at the exact millisecond when the player shouts the word.
2. Accurate Speaker Letter Attribution & Precise Letter Pop Timing:
   - Round 1: Angel: 'C', Arthur: 'K' -> Arthur says 'Cacing!'
   - Round 2: Angel: 'S', Arthur: 'S' -> Arthur yells 'ANJINGS!'
   - Round 3: Count -> Angel blurts out 'Amidis!' -> later Angel says 'Aktifis!'
   - Round 4: Angel: 'G', Arthur: 'S' (Fixed: Angel is G, Arthur is S) -> Arthur says 'Ganas!'
   - Round 5: Angel: 'D', Arthur: 'O' -> Angel says 'Domino!'
   - Round 6: Angel: 'KA', Arthur: 'KA' -> Arthur yells 'Kakak!'
   - Round 7: Angel: 'M', Arthur: 'U' -> Arthur says 'Maluku!'
   - Above-head letter pops (Angel x=305, Arthur x=760 at y=510) are invisible during countdown
     and appear strictly at the exact millisecond the letter is vocalized with pop.wav.
3. One-word-at-a-time dynamic captions (Rule 49).
4. Authentic Chopin Nocturne Op. 9 No. 2 in E-flat major (Rule 44).
5. Clean reference cover image without blue gradient (Rule 38).
"""

import json
import math
import os
import subprocess
import tempfile
from pathlib import Path

WORKSPACE = Path("/Users/arthurandersen/Documents/AI_Video_Editor_Gemini")
PROJECT_NAME = "Lengkapin Kata"
RAW_VIDEO = WORKSPACE / f"raw/{PROJECT_NAME}/IMG_0671.MOV"
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
# 1. Render Clean Title & Word Callout Overlays via Native Swift + AppKit
# ---------------------------------------------------------------------------
def render_graphics_swift() -> dict[str, Path]:
    swift_code = f"""
import AppKit
import Foundation

let outDir = "{BROLL_DIR}"

func createCanvas() -> (NSBitmapImageRep, NSGraphicsContext) {{
    let width = 1080
    let height = 1920
    let rep = NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: width,
        pixelsHigh: height,
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .deviceRGB,
        bytesPerRow: width * 4,
        bitsPerPixel: 32
    )!
    let ctx = NSGraphicsContext(bitmapImageRep: rep)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = ctx
    NSColor.clear.set()
    NSRect(x: 0, y: 0, width: width, height: height).fill()
    return (rep, ctx)
}}

func savePNG(_ rep: NSBitmapImageRep, _ filename: String) {{
    NSGraphicsContext.restoreGraphicsState()
    let data = rep.representation(using: .png, properties: [:])!
    let url = URL(fileURLWithPath: "\\(outDir)/\\(filename)")
    try! data.write(to: url)
}}

let pCenter = NSMutableParagraphStyle()
pCenter.alignment = .center

let fontSub = NSFont(name: "HelveticaNeue-Bold", size: 68) ?? NSFont.systemFont(ofSize: 68, weight: .bold)
let fontMain = NSFont(name: "Arial-Black", size: 96) ?? NSFont.systemFont(ofSize: 96, weight: .black)
let fontWord = NSFont(name: "Arial-Black", size: 88) ?? NSFont.systemFont(ofSize: 88, weight: .black)

func drawBlackWithWhiteOutline(_ text: String, rect: NSRect, font: NSFont) {{
    let sh = NSShadow()
    sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.55)
    sh.shadowBlurRadius = 8.0
    sh.shadowOffset = NSSize(width: 0, height: -3)

    let p1: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.white,
        .strokeColor: NSColor.white,
        .strokeWidth: -15.0,
        .shadow: sh,
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: text, attributes: p1).draw(in: rect)

    let p2: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.black,
        .strokeColor: NSColor.black,
        .strokeWidth: 0.0,
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: text, attributes: p2).draw(in: rect)
}}

func drawWhiteWithDarkShadow(_ text: String, rect: NSRect, font: NSFont) {{
    let sh = NSShadow()
    sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.70)
    sh.shadowBlurRadius = 9.0
    sh.shadowOffset = NSSize(width: 0, height: -4)

    let p1: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.black,
        .strokeColor: NSColor.black,
        .strokeWidth: -4.5,
        .shadow: sh,
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: text, attributes: p1).draw(in: rect)

    let p2: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.white,
        .strokeColor: NSColor.white,
        .strokeWidth: 0.0,
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: text, attributes: p2).draw(in: rect)
}}

// 1. Hook Title
let (repHook, _) = createCanvas()
drawBlackWithWhiteOutline("challenge", rect: NSRect(x: 40, y: 1680, width: 1000, height: 95), font: fontSub)
drawWhiteWithDarkShadow("LENGKAPIN KATA ✍️", rect: NSRect(x: 30, y: 1560, width: 1020, height: 120), font: fontMain)
savePNG(repHook, "hook_lengkapin_kata.png")

// 2. Top Word Callouts
struct WordCallout {{
    let filename: String
    let text: String
}}

let callouts: [WordCallout] = [
    WordCallout(filename: "card_cacing.png",  text: "CACING 🐛"),
    WordCallout(filename: "card_anjings.png", text: "ANJINGS 🐶"),
    WordCallout(filename: "card_alas.png",    text: "ALAS"),
    WordCallout(filename: "card_angels.png",  text: "ANGELS 👼"),
    WordCallout(filename: "card_amidis.png",  text: "AMIDIS 💧"),
    WordCallout(filename: "card_aktifis.png", text: "AKTIFIS ✊"),
    WordCallout(filename: "card_ganas.png",   text: "GANAS 🔥"),
    WordCallout(filename: "card_domino.png",  text: "DOMINO 🀄"),
    WordCallout(filename: "card_kakak.png",   text: "KAKAK 👫"),
    WordCallout(filename: "card_maluku.png",  text: "MALUKU 🏝️"),
]

for c in callouts {{
    let (rep, _) = createCanvas()
    drawWhiteWithDarkShadow(c.text, rect: NSRect(x: 30, y: 1650, width: 1020, height: 120), font: fontWord)
    savePNG(rep, c.filename)
}}
"""
    with tempfile.NamedTemporaryFile("w", suffix=".swift", delete=False) as sf:
        sf.write(swift_code)
        swift_file = sf.name

    try:
        run_cmd(["swift", "-module-cache-path", "/tmp/swift_cache", swift_file])
    finally:
        if os.path.exists(swift_file):
            os.remove(swift_file)

    cards = {
        "hook": BROLL_DIR / "hook_lengkapin_kata.png",
        "cacing": BROLL_DIR / "card_cacing.png",
        "anjings": BROLL_DIR / "card_anjings.png",
        "alas": BROLL_DIR / "card_alas.png",
        "angels": BROLL_DIR / "card_angels.png",
        "amidis": BROLL_DIR / "card_amidis.png",
        "aktifis": BROLL_DIR / "card_aktifis.png",
        "ganas": BROLL_DIR / "card_ganas.png",
        "domino": BROLL_DIR / "card_domino.png",
        "kakak": BROLL_DIR / "card_kakak.png",
        "maluku": BROLL_DIR / "card_maluku.png",
    }
    return cards


# ---------------------------------------------------------------------------
# 2. Master Edit Decision List (EDL) with Millisecond-Precise Letter & Card Triggers
# ---------------------------------------------------------------------------
# Every letter and top word card has an exact raw trigger timestamp.
# They will NEVER show before that exact moment!
SEGMENTS = [
    # --- Hook & Intro ---
    # Seg 1: "Challenge Lengkapin Kata!"
    {
        "id": 1,
        "start": 0.85,
        "end": 3.25,
        "mode": "normal",
        "no_caption": True,
        # Hook card shows throughout the hook
        "card": "hook",
        "card_raw_start": 0.85,
        "card_raw_end": 3.25,
    },

    # --- Round 1: C & K -> Cacing! ---
    # Seg 2: Arthur count "Satu, dua, ga..." + Arthur: "K", Angel: "C"
    # Letters vocalized at 4.98s
    {
        "id": 2,
        "start": 3.45,
        "end": 5.50,
        "mode": "normal",
        "letter_raw_start": 4.98,
        "girl_letter": "C",
        "guy_letter": "K",
    },
    # Seg 3: Arthur says "Cacing!" (raw 6.30s) -> card appears ONLY at 6.30s!
    {
        "id": 3,
        "start": 6.15,
        "end": 7.45,
        "mode": "zoom_both",
        "card": "cacing",
        "card_raw_start": 6.30,
        "card_raw_end": 7.45,
        # Keep letters as reference
        "girl_letter": "C",
        "guy_letter": "K",
    },
    # Seg 4: Angel laughs "Cacing kan C..."
    {
        "id": 4,
        "start": 8.60,
        "end": 10.45,
        "mode": "normal",
    },

    # --- Round 2: S & S -> ANJINGS! & Alas & Skip ---
    # Seg 5: Arthur count "Satu, dua, tiga..." + Angel: "S", Arthur: "S"
    # Letters vocalized at 12.70s
    {
        "id": 5,
        "start": 10.80,
        "end": 13.50,
        "mode": "normal",
        "letter_raw_start": 12.70,
        "girl_letter": "S",
        "guy_letter": "S",
    },
    # Seg 6: Arthur yells "ANJINGS!" (raw 15.70s) -> card appears ONLY at 15.70s!
    {
        "id": 6,
        "start": 15.50,
        "end": 18.90,
        "mode": "zoom_arthur",
        "card": "anjings",
        "card_raw_start": 15.70,
        "card_raw_end": 18.90,
    },
    # Seg 7: Arthur: "Alas!" (raw 19.90s) -> card appears ONLY at 19.90s!
    {
        "id": 7,
        "start": 19.20,
        "end": 23.30,
        "mode": "zoom_both",
        "card": "alas",
        "card_raw_start": 19.90,
        "card_raw_end": 23.30,
    },
    # Seg 8: Skip deliberation: "Apas... Ah... Oke kita skip deh."
    {
        "id": 8,
        "start": 34.00,
        "end": 38.80,
        "mode": "normal",
    },
    # Seg 9: Angel tries "Angels!" (raw 42.50s) -> card appears ONLY at 42.50s!
    {
        "id": 9,
        "start": 40.50,
        "end": 47.40,
        "mode": "zoom_both",
        "card": "angels",
        "card_raw_start": 42.50,
        "card_raw_end": 47.40,
    },

    # --- Round 3: Amidis & Aktifis (Angel Wins) ---
    # Seg 10: Arthur count -> Angel blurts out "Amidis!" at 50.30s!
    {
        "id": 10,
        "start": 48.00,
        "end": 54.30,
        "mode": "normal",
        "card": "amidis",
        "card_raw_start": 50.30,
        "card_raw_end": 54.30,
    },
    # Seg 11: Angel laughs "Pikir..." + Arthur: "Agas..."
    {
        "id": 11,
        "start": 54.80,
        "end": 56.80,
        "mode": "zoom_both",
    },
    # Seg 12: Angel: "Ah, Aktifis!" (raw 63.60s) -> card appears ONLY at 63.60s!
    {
        "id": 12,
        "start": 63.40,
        "end": 68.00,
        "mode": "zoom_angel",
        "card": "aktifis",
        "card_raw_start": 63.60,
        "card_raw_end": 68.00,
    },

    # --- Round 4: Angel: 'G', Arthur: 'S' -> Ganas (Arthur Wins) ---
    # Seg 13: Arthur count "Tu, wa, tiga..." + Angel: "G", Arthur: "S"
    # Letters vocalized at 69.95s
    {
        "id": 13,
        "start": 68.20,
        "end": 70.80,
        "mode": "normal",
        "letter_raw_start": 69.95,
        "girl_letter": "G",
        "guy_letter": "S",
    },
    # Seg 14: Arthur yells: "Ganas!" (raw 73.20s) -> card appears ONLY at 73.20s!
    {
        "id": 14,
        "start": 73.20,
        "end": 76.50,
        "mode": "zoom_arthur",
        "card": "ganas",
        "card_raw_start": 73.20,
        "card_raw_end": 76.50,
        "girl_letter": "G",
        "guy_letter": "S",
    },

    # --- Round 5: Angel: 'D', Arthur: 'O' -> Domino (Angel Wins) ---
    # Seg 15: Both count "Tu, wa, ga..." + Angel: "D", Arthur: "O"
    # Letters vocalized at 79.10s
    {
        "id": 15,
        "start": 77.00,
        "end": 80.00,
        "mode": "normal",
        "letter_raw_start": 79.10,
        "girl_letter": "D",
        "guy_letter": "O",
    },
    # Seg 16: Arthur: "D..." Angel: "Domino!" (raw 83.10s) -> card appears ONLY at 83.10s!
    {
        "id": 16,
        "start": 82.40,
        "end": 87.50,
        "mode": "zoom_both",
        "card": "domino",
        "card_raw_start": 83.10,
        "card_raw_end": 87.50,
    },

    # --- Round 6: Ka & Ka -> Kakak vs Kakek (Arthur Wins) ---
    # Seg 17: Both count + Both say "Ka!" at 93.30s -> Arthur shouts "Kakak!" at 94.15s!
    {
        "id": 17,
        "start": 91.00,
        "end": 97.50,
        "mode": "normal",
        "letter_raw_start": 93.30,
        "girl_letter": "KA",
        "guy_letter": "KA",
        "card": "kakak",
        "card_raw_start": 94.15,
        "card_raw_end": 97.50,
    },
    # Seg 18: Arthur celebration: "Kakak tercinta... Yo, poin buat gua. Terakhir."
    {
        "id": 18,
        "start": 97.80,
        "end": 103.50,
        "mode": "zoom_arthur",
        "card": "kakak",
        "card_raw_start": 97.80,
        "card_raw_end": 103.50,
    },

    # --- Round 7: Angel: 'M', Arthur: 'U' -> Maluku! & Outro ---
    # Seg 19: Count + Angel: "M", Arthur: "U" vocalized at 107.35s
    {
        "id": 19,
        "start": 105.80,
        "end": 109.80,
        "mode": "normal",
        "letter_raw_start": 107.35,
        "girl_letter": "M",
        "guy_letter": "U",
    },
    # Seg 20: Arthur: "Maluku!" (raw 109.80s / 110.0s) -> card appears ONLY at 110.0s and stays till end!
    {
        "id": 20,
        "start": 110.00,
        "end": 119.67,
        "mode": "zoom_both",
        "card": "maluku",
        "card_raw_start": 110.00,
        "card_raw_end": 119.67,
    },
]


# ---------------------------------------------------------------------------
# 3. Dynamic Word-by-Word Dialogue Captions (Rule 49 & Rule 39)
# ---------------------------------------------------------------------------
RAW_SPOKEN_WORDS = [
    # Round 1
    (3.50, 3.90, "Satu"),
    (4.25, 4.60, "dua"),
    (4.85, 5.20, "ga"),
    (6.30, 7.10, "Cacing!"),
    (8.70, 9.40, "Cacing"),
    (9.45, 9.75, "kan"),
    (9.80, 10.25, "C"),

    # Round 2
    (10.90, 11.40, "Satu"),
    (11.50, 11.90, "dua"),
    (12.10, 12.60, "tiga"),
    (15.70, 16.50, "Anjings!"),
    (16.70, 17.20, "Gak"),
    (17.25, 17.70, "boleh!"),
    (17.80, 18.30, "Apa?"),
    (19.30, 19.80, "Ah"),
    (19.90, 20.70, "Alas!"),
    (20.80, 21.30, "Itu"),
    (21.35, 21.80, "cuma"),
    (21.85, 22.30, "dua"),
    (22.35, 22.70, "ya"),
    (34.40, 35.00, "Apas"),
    (36.80, 37.30, "Oke"),
    (37.35, 37.60, "kita"),
    (37.65, 38.10, "skip"),
    (38.15, 38.60, "deh"),
    (42.50, 43.40, "Angels!"),
    (44.60, 45.00, "Nama"),
    (45.05, 45.30, "gak"),
    (45.35, 45.80, "boleh!"),
    (46.00, 46.40, "Skip,"),
    (46.45, 46.80, "skip,"),
    (46.85, 47.30, "skip"),

    # Round 3
    (48.05, 48.45, "Tu,"),
    (48.50, 48.80, "wa"),
    (48.85, 49.30, "Gak"),
    (49.35, 49.70, "tahu"),
    (49.75, 50.10, "apa"),
    (50.15, 50.40, "ya"),
    (50.45, 51.30, "Amidis!"),
    (52.20, 52.60, "Itu"),
    (52.65, 53.20, "merek"),
    (53.25, 53.60, "gak"),
    (53.65, 54.10, "sih?"),
    (55.20, 56.50, "Pikir..."),
    (61.30, 62.10, "Agas..."),
    (63.50, 64.00, "Ah,"),
    (64.05, 65.10, "Aktifis!"),
    (66.40, 66.80, "Oke"),
    (66.85, 67.20, "lah"),
    (67.25, 67.60, "fine,"),
    (67.65, 68.10, "next"),

    # Round 4
    (68.30, 68.70, "Tu,"),
    (68.80, 69.20, "wa,"),
    (69.30, 69.70, "tiga"),
    (73.30, 74.20, "Ganas!"),
    (75.20, 75.70, "Oke,"),
    (75.80, 76.40, "2-1"),

    # Round 5
    (77.10, 77.50, "Tu,"),
    (77.60, 78.00, "wa,"),
    (78.10, 78.50, "ga"),
    (83.10, 84.00, "Domino!"),
    (84.60, 85.00, "Oke,"),
    (85.10, 85.50, "oke,"),
    (85.60, 86.00, "oke"),

    # Round 6
    (91.20, 91.60, "Tu,"),
    (91.80, 92.20, "wa,"),
    (92.40, 92.80, "tiga"),
    (94.20, 94.80, "Kakak!"),
    (94.90, 95.50, "Kakek!"),
    (95.60, 96.00, "Gua"),
    (96.05, 96.60, "duluan,"),
    (96.65, 97.40, "KAKAK!"),
    (97.90, 98.60, "Kakak"),
    (98.65, 99.40, "tercinta"),
    (99.70, 100.30, "Yo,"),
    (100.35, 100.80, "poin"),
    (100.85, 101.20, "buat"),
    (101.25, 101.60, "gua"),
    (101.80, 102.50, "Terakhir"),

    # Round 7
    (106.30, 106.70, "Tu,"),
    (106.80, 107.20, "wa,"),
    (107.30, 107.70, "tiga"),
    (108.60, 109.10, "Hah?"),
    (109.15, 109.60, "Apa?"),
    (109.80, 110.20, "M"),
    (110.30, 111.10, "Maluku!"),
    (111.60, 112.00, "Gak"),
    (112.05, 112.50, "boleh"),
    (112.55, 113.00, "nama"),
    (113.05, 113.40, "itu"),
    (113.50, 113.80, "Kan"),
    (113.85, 114.20, "tetap"),
    (114.25, 114.50, "aja"),
    (114.55, 115.00, "kata"),
    (115.05, 115.70, "Indonesia,"),
    (115.80, 116.30, "kota!"),
    (116.50, 117.80, "Maluku~"),
    (117.90, 118.40, "Poin"),
    (118.45, 118.80, "dong"),
    (118.85, 119.20, "buat"),
    (119.25, 119.60, "gua"),
]


def fmt_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        s += 1
        cs = 0
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def generate_ass_subtitles(ass_file: Path) -> tuple[list[dict], list[dict], list[dict]]:
    timeline_events = []
    card_events = []
    letter_events = []
    current_time = 0.0

    for seg in SEGMENTS:
        base_dur = seg["end"] - seg["start"]
        t_start = current_time
        t_end = current_time + base_dur

        ev = {
            "id": seg["id"],
            "t_start": t_start,
            "t_end": t_end,
            "dur": base_dur,
            "raw_start": seg["start"],
            "raw_end": seg["end"],
            "mode": seg["mode"],
            "no_caption": seg.get("no_caption", False),
        }
        timeline_events.append(ev)

        # Card trigger timing (Strictly at card_raw_start!)
        card_key = seg.get("card", "")
        if card_key:
            c_raw_st = seg.get("card_raw_start", seg["start"])
            c_raw_et = seg.get("card_raw_end", seg["end"])
            card_t0 = t_start + max(0.0, c_raw_st - seg["start"])
            card_t1 = t_start + min(base_dur, c_raw_et - seg["start"])
            card_events.append({
                "card": card_key,
                "t0": round(card_t0, 3),
                "t1": round(card_t1, 3),
            })

        # Letter trigger timing (Strictly at letter_raw_start!)
        gl = seg.get("girl_letter", "")
        bl = seg.get("guy_letter", "")
        if gl or bl:
            # If letter_raw_start is specified, pop letters strictly at that moment!
            # Otherwise if continuing as reference (like in seg 3), keep visible throughout
            if "letter_raw_start" in seg:
                let_raw_st = seg["letter_raw_start"]
                let_t0 = t_start + max(0.0, let_raw_st - seg["start"])
            else:
                let_t0 = t_start
            let_t1 = t_end

            letter_events.append({
                "girl_letter": gl,
                "guy_letter": bl,
                "t0": round(let_t0, 3),
                "t1": round(let_t1, 3),
                "is_new_pop": "letter_raw_start" in seg,
            })

        current_time += base_dur

    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BottomWord,Arial Black,64,&H00FFFFFF,&H000000FF,&H00000000,&HB4000000,-1,0,0,0,100,100,0,0,1,3.2,4.2,2,50,50,155,1
Style: HeadLetterGirl,Arial Black,125,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,4.0,5.0,5,20,20,20,1
Style: HeadLetterGuy,Arial Black,125,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,4.0,5.0,5,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [ass_header.strip()]

    # 1. Map each raw spoken word into the edited timeline (Strictly ONE word at a time!)
    mapped_words = []
    for ws, we, word_text in RAW_SPOKEN_WORDS:
        for ev in timeline_events:
            if ev["no_caption"]:
                continue
            r0, r1 = ev["raw_start"], ev["raw_end"]
            if ws >= r0 - 0.05 and ws < r1 - 0.02:
                w_clamped_start = max(ws, r0)
                w_clamped_end = min(we, r1)
                t0 = ev["t_start"] + (w_clamped_start - r0)
                t1 = ev["t_start"] + (w_clamped_end - r0)
                if t1 - t0 < 0.18:
                    t1 = min(ev["t_end"], t0 + 0.24)
                elif t1 - t0 > 0.65:
                    t1 = t0 + 0.65
                mapped_words.append((t0, t1, word_text))
                break

    mapped_words.sort(key=lambda x: x[0])
    cleaned_words = []
    for i, (t0, t1, txt) in enumerate(mapped_words):
        if i + 1 < len(mapped_words):
            next_t0 = mapped_words[i + 1][0]
            if t1 > next_t0 - 0.03:
                t1 = max(t0 + 0.12, next_t0 - 0.03)
        cleaned_words.append((t0, t1, txt))

    for t0, t1, txt in cleaned_words:
        st_str = fmt_ass_time(t0)
        et_str = fmt_ass_time(t1)
        lines.append(f"Dialogue: 1,{st_str},{et_str},BottomWord,,0,0,0,,{txt}")

    # 2. Add Above-Head Letter Pops (Rule 40: Angel x=305, Arthur x=760 at y=510)
    for lev in letter_events:
        gl = lev["girl_letter"]
        bl = lev["guy_letter"]
        st_str = fmt_ass_time(lev["t0"])
        et_str = fmt_ass_time(lev["t1"])
        anim = r"{\pos(305,510)\fscx140\fscy140\t(0,140,\fscx100\fscy100)}" if lev["is_new_pop"] else r"{\pos(305,510)}"
        anim_b = r"{\pos(760,510)\fscx140\fscy140\t(0,140,\fscx100\fscy100)}" if lev["is_new_pop"] else r"{\pos(760,510)}"

        if gl:
            lines.append(f"Dialogue: 3,{st_str},{et_str},HeadLetterGirl,,0,0,0,,{anim}{gl}")
        if bl:
            lines.append(f"Dialogue: 3,{st_str},{et_str},HeadLetterGuy,,0,0,0,,{anim_b}{bl}")

    ass_file.write_text("\n".join(lines), encoding="utf-8")
    return timeline_events, card_events, letter_events


# ---------------------------------------------------------------------------
# 4. Master Video Assembly
# ---------------------------------------------------------------------------
def build_video() -> None:
    print("🖼️  [1/4] Rendering pixel-perfect typography overlays via Swift...")
    cards = render_graphics_swift()

    ass_path = DRAFT_DIR / "captions_lengkapin_kata.ass"
    timeline_events, card_events, letter_events = generate_ass_subtitles(ass_path)
    total_dur = timeline_events[-1]["t_end"]
    print(f"⏱️  Total edited timeline duration: {total_dur:.2f}s ({len(timeline_events)} segments)")

    edl_json_path = DRAFT_DIR / "lengkapin_kata_edl.json"
    edl_json_path.write_text(json.dumps({
        "segments": timeline_events,
        "cards": card_events,
        "letters": letter_events,
    }, indent=2), encoding="utf-8")

    print(f"✂️  [2/4] Cutting {len(timeline_events)} segments with dynamic framing (fast intermediate encoding)...")
    with tempfile.TemporaryDirectory(prefix="lengkapin_kata_segs_") as tmpdir:
        seg_dir = Path(tmpdir)
        seg_files = []

        for idx, ev in enumerate(timeline_events):
            seg_out = seg_dir / f"seg_{idx:03d}.mov"
            start = ev["raw_start"]
            dur = ev["dur"]
            mode = ev["mode"]

            # Video filter based on framing mode (eyeline anchored at upper third)
            if mode == "zoom_both":
                vf = f"scale=1080*1.10:1920*1.10,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.42,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            elif mode == "zoom_angel":
                vf = f"scale=1080*1.32:1920*1.32,crop=1080:1920:80:350,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            elif mode == "zoom_arthur":
                vf = f"scale=1080*1.38:1920*1.38,crop=1080:1920:410:320,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
            else:
                vf = f"scale=1080:1920,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"

            # Audio filter with 15ms crossfade padding
            fade_out_st = max(0.0, dur - 0.015)
            af = f"aresample=48000,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.015,afade=t=out:st={fade_out_st:.3f}:d=0.015,apad=whole_dur={dur:.4f},atrim=0:{dur:.4f},asetpts=PTS-STARTPTS"

            # Use ultrafast visually-lossless H.264 (CRF 13) for lightning-fast intermediate slicing
            cmd = [
                "ffmpeg", "-y",
                "-ss", f"{start:.3f}",
                "-t", f"{dur + 0.35:.3f}",
                "-i", str(RAW_VIDEO),
                "-vf", vf,
                "-af", af,
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "13",
                "-c:a", "pcm_s16le",
                "-ar", "48000",
                "-ac", "2",
                str(seg_out),
            ]
            run_cmd(cmd)
            seg_files.append(seg_out)

        print("🔗 [3/4] Concatenating cuts into clean intermediate stream...")
        concat_list = seg_dir / "concat_list.txt"
        with open(concat_list, "w") as f:
            for s in seg_files:
                f.write(f"file '{s.resolve()}'\n")

        concat_mov = DRAFT_DIR / "lengkapin_kata_concat.mov"
        run_cmd([
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            str(concat_mov),
        ])

        print("🎵 [4/4] Master Assembly: Card Overlays (Strict Timing) + ASS Subtitles + Chopin + SFX...")
        music_path = MUSIC_DIR / "nocturne_op9_in_eb.wav"
        pop_sfx = SFX_DIR / "pop.wav"
        win_sfx = SFX_DIR / "point_win.wav"
        boom_sfx = SFX_DIR / "meme_boom.wav"
        whoosh_sfx = SFX_DIR / "whoosh.wav"

        # 1. Video Filter Graph: Chain Top Card Overlays (Strict enable between t0 and t1!)
        # Collect distinct card files needed as video inputs
        needed_card_keys = list(set(c["card"] for c in card_events if c["card"] in cards))
        card_input_map = {}
        video_inputs = []

        for idx, k in enumerate(needed_card_keys):
            card_input_map[k] = 2 + idx  # input index (0: concat, 1: music, 2..N: cards)
            video_inputs.extend(["-i", str(cards[k])])

        v_chain_lines = ["[0:v]"]
        curr_label = "0:v"

        for idx, cev in enumerate(card_events):
            ckey = cev["card"]
            if ckey in card_input_map:
                inp_idx = card_input_map[ckey]
                next_label = f"v_card_{idx}"
                t0, t1 = cev["t0"], cev["t1"]
                v_chain_lines.append(
                    f"[{curr_label}][{inp_idx}:v] overlay=0:0:enable='between(t,{t0:.2f},{t1:.2f})' [{next_label}]"
                )
                curr_label = next_label

        # Finally apply ASS subtitles on top of all cards
        v_chain_lines.append(f"[{curr_label}] ass='{ass_path.resolve()}' [outv]")
        # Note: drop first "[0:v]" item
        video_filter_complex = "; ".join(v_chain_lines[1:])

        # 2. SFX Inputs & Triggers
        # Trigger pop on letter reveals and win/boom/pop on word headers
        sfx_inputs = []
        sfx_filter_chains = []
        sfx_labels = []
        sfx_count = 0
        base_sfx_inp_offset = 2 + len(needed_card_keys)

        # Trigger SFX for new letter pops
        for lev in letter_events:
            if lev["is_new_pop"]:
                delay_ms = max(0, int(lev["t0"] * 1000))
                sfx_inputs.extend(["-i", str(pop_sfx)])
                inp_idx = base_sfx_inp_offset + sfx_count
                sfx_filter_chains.append(
                    f"[{inp_idx}:a] aresample=48000,adelay={delay_ms}|{delay_ms},volume=0.45 [sfx{sfx_count}]"
                )
                sfx_labels.append(f"[sfx{sfx_count}]")
                sfx_count += 1

        # Trigger SFX for word card reveals
        for cev in card_events:
            ckey = cev["card"]
            t0 = cev["t0"]
            if ckey == "hook":
                sfx_file = whoosh_sfx
                vol = 0.40
            elif ckey in ["aktifis", "ganas", "domino", "kakak"]:
                sfx_file = win_sfx
                vol = 0.55
            elif ckey == "anjings":
                sfx_file = boom_sfx
                vol = 0.65
            else:
                sfx_file = pop_sfx
                vol = 0.45

            delay_ms = max(0, int(t0 * 1000))
            sfx_inputs.extend(["-i", str(sfx_file)])
            inp_idx = base_sfx_inp_offset + sfx_count
            sfx_filter_chains.append(
                f"[{inp_idx}:a] aresample=48000,adelay={delay_ms}|{delay_ms},volume={vol:.2f} [sfx{sfx_count}]"
            )
            sfx_labels.append(f"[sfx{sfx_count}]")
            sfx_count += 1

        all_sfx_mix = "".join(sfx_labels) + f" amix=inputs={sfx_count}:normalize=0 [all_sfx]"

        # Audio Filter Complex: Voice + Chopin Nocturne (ducked to -20 dB) + SFX -> -14 LUFS
        audio_filter_parts = [
            f"[1:a] atrim=0:{total_dur:.3f},asetpts=PTS-STARTPTS,volume=0.10,afade=t=in:st=0:d=1.5,afade=t=out:st={total_dur-2.0:.3f}:d=2.0 [music]",
            *sfx_filter_chains,
            all_sfx_mix,
            "[0:a] highpass=f=80,volume=1.25 [voice]",
            "[voice][music][all_sfx] amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11 [outa]",
        ]
        audio_filter_complex = "; ".join(audio_filter_parts)

        master_filter_complex = f"{video_filter_complex}; {audio_filter_complex}"

        final_master_mp4 = FINAL_DIR / "lengkapin_kata_final.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-i", str(concat_mov),
            "-i", str(music_path),
            *video_inputs,
            *sfx_inputs,
            "-filter_complex", master_filter_complex,
            "-map", "[outv]",
            "-map", "[outa]",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "320k",
            "-ar", "48000",
            "-t", f"{total_dur:.3f}",
            str(final_master_mp4),
        ]
        run_cmd(cmd)

        print("📸 Generating high-res Cover Image (Rule 38)...")
        cover_png = FINAL_DIR / "lengkapin_kata_cover.png"
        run_cmd([
            "ffmpeg", "-y",
            "-ss", "1.50",
            "-i", str(final_master_mp4),
            "-frames:v", "1",
            "-q:v", "1",
            str(cover_png),
        ])

        print(f"✅ Video editing complete! Final render saved to:\n   {final_master_mp4}")
        print(f"   Cover saved to:\n   {cover_png}")


if __name__ == "__main__":
    build_video()
