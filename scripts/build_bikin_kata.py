#!/usr/bin/env python3
"""
Master Builder for 'Bikin Kata Challenge' (Couple Content Game - Vertical 9:16)
Creative Director & Video Editor: Gemini 4 Argon (Antigravity)

Strictly encodes and enforces all Master Editing Rules:
- Rule 37: Couple Identity: Angel (Left) & Arthur (Right) — No Scoreboard or point badges.
- Rule 38: Reference-Style Title Hook & Cover:
  * Both 'challenge' AND 'BIKIN KATA 🔥' show immediately from 0:00.
  * Line 1: HelveticaNeue-Bold (68pt), Black fill with crisp White border (#FFFFFF).
  * Line 2: Arial-Black (96pt), Pure White fill with thin dark edge (-4.5) and soft drop shadow.
  * No blue gradient; 100% consistent natural color grading start to end.
  * No bottom caption during opening title hook.
- Rule 39: Unified Clean Typography & No duplicate captions when word is completed.
- Rule 40: Horizontally Aligned Above-Head Bold Letter Pops at y=510 (Angel x=305, Arthur x=760).
- Rule 41: Borderless Word Callouts at Top (API! 🔥, PAPI! ✨, JANTUNG! 🫀, SANTE ❌, SANTET?! 💀) at y=235.
- Rule 42: Fast Zoom-In Transition (1.15x -> 2.15x over ~0.17s) to Arthur's face + Black & White.
- Rule 43: Comfortable Portrait Framing on What_ Meme.mp4 (1080x1440 over soft matching blurred background).
- Rule 44: Authentic Chopin — Nocturne in E-flat major, Op. 9, No. 2 (Musopen master) ducked to -20 dB (0.10),
  swelling on B&W zoom (0.48), and dipping to 0.03 during meme cutaway.
- Rule 45: Per-Project Output Folders (renders/final/Bikin Kata Challenge/, etc.).
- Rule 46: Meme speech volume boosted (+14 dB w/ limiter) and music ducked to 0.03; clean captions without emoji boxes.
- Rule 49: One-Word-at-a-Time Dynamic Spoken Captions (Never Show Static Full Sentences).
"""

import json
import math
import os
import subprocess
import tempfile
import wave
from pathlib import Path
import numpy as np

WORKSPACE = Path("/Users/arthurandersen/Documents/AI_Video_Editor_Gemini")
PROJECT_NAME = "Bikin Kata Challenge"
RAW_VIDEO = WORKSPACE / f"raw/{PROJECT_NAME}/IMG_0662.MOV"
WHAT_MEME_VIDEO = WORKSPACE / "Meme Material/What_ Meme.mp4"
if not WHAT_MEME_VIDEO.exists():
    WHAT_MEME_VIDEO = WORKSPACE / f"raw/{PROJECT_NAME}/What_ Meme.mp4"
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
    if not win_sfx.exists():
        run_cmd([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "aevalsrc='0.35*sin(2*PI*523.25*t)*exp(-6*t)+0.45*sin(2*PI*783.99*t)*exp(-4*t)':s=48000:d=0.85",
            "-af", "afade=t=out:st=0.65:d=0.20",
            "-loglevel", "error",
            str(win_sfx),
        ])

    boom_sfx = SFX_DIR / "meme_boom.wav"
    if not boom_sfx.exists():
        run_cmd([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", "aevalsrc='0.75*sin(2*PI*(110*exp(-4*t)+38)*t)*exp(-2.2*t)':s=48000:d=1.1",
            "-af", "lowpass=f=280,afade=t=out:st=0.75:d=0.35",
            "-loglevel", "error",
            str(boom_sfx),
        ])

    pop_sfx = SFX_DIR / "pop.wav"
    whoosh_sfx = SFX_DIR / "whoosh.wav"
    music_path = MUSIC_DIR / "nocturne_op9_in_eb.wav"
    if not music_path.exists():
        raise FileNotFoundError(f"Missing mandatory Chopin Nocturne in Eb: {music_path}")

    return win_sfx, boom_sfx, pop_sfx, whoosh_sfx, music_path


# ---------------------------------------------------------------------------
# 2. Render Clean Title & Word-Made Overlays via Native macOS Swift + CoreGraphics
#    (Matches 'yang kena bomb makan / BEAN BOOZLE 🤮' Reference Image)
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

// Line 1: 'challenge' (Black fill, pure crisp White border, subtle drop shadow)
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
        .foregroundColor: NSColor.white,
        .strokeColor: NSColor.white,
        .strokeWidth: -14.0,
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: text, attributes: p2).draw(in: rect)

    let p3: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.black,
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: text, attributes: p3).draw(in: rect)
}}

// Line 2 & Word Callouts: Pure White fill, thin dark edge + soft drop shadow
func drawWhiteBeanBoozleStyle(_ text: String, rect: NSRect, font: NSFont) {{
    let sh = NSShadow()
    sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.90)
    sh.shadowBlurRadius = 10.0
    sh.shadowOffset = NSSize(width: 0, height: -6)

    let b1: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.black,
        .strokeColor: NSColor.black,
        .strokeWidth: -4.5,
        .shadow: sh,
        .paragraphStyle: pCenter,
        .kern: -1.5
    ]
    NSAttributedString(string: text, attributes: b1).draw(in: rect)

    let b2: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.white,
        .paragraphStyle: pCenter,
        .kern: -1.5
    ]
    NSAttributedString(string: text, attributes: b2).draw(in: rect)
}}

// Opening Title Hook: Both 'challenge' AND 'BIKIN KATA 🔥' show from 0:00!
for step in 1...2 {{
    let (rep, _) = createCanvas()

    drawBlackWithWhiteOutline(
        "challenge",
        rect: NSRect(x: 40, y: 1355, width: 1000, height: 100),
        font: fontSub
    )
    drawWhiteBeanBoozleStyle(
        "BIKIN KATA 🔥",
        rect: NSRect(x: 30, y: 1235, width: 1020, height: 130),
        font: fontMain
    )

    savePNG(rep, "hook_kinetic_\\(step).png")
}}

// Completed Word Callouts at Top (Borderless, Pure Word + Emoji)
struct WordOverlay {{
    let filename: String
    let text: String
}}

let wordOverlays: [WordOverlay] = [
    WordOverlay(filename: "glass_api.png",     text: "API! 🔥"),
    WordOverlay(filename: "glass_papi.png",    text: "PAPI! ✨"),
    WordOverlay(filename: "glass_jantung.png", text: "JANTUNG! 🫀"),
    WordOverlay(filename: "glass_sante.png",   text: "SANTE ❌"),
    WordOverlay(filename: "glass_santet.png",  text: "SANTET?! 💀")
]

for wo in wordOverlays {{
    let (rep, _) = createCanvas()

    drawWhiteBeanBoozleStyle(
        wo.text,
        rect: NSRect(x: 40, y: 1555, width: 1000, height: 130),
        font: fontWord
    )

    savePNG(rep, wo.filename)
}}
"""
    with tempfile.NamedTemporaryFile("w", suffix=".swift", delete=False) as sf:
        sf.write(swift_code)
        swift_file = sf.name

    try:
        run_cmd(["/usr/bin/swift", "-module-cache-path", "/tmp/swift_cache", swift_file])
    finally:
        if os.path.exists(swift_file):
            os.remove(swift_file)

    return {
        "hook1": BROLL_DIR / "hook_kinetic_1.png",
        "hook2": BROLL_DIR / "hook_kinetic_2.png",
        "api": BROLL_DIR / "glass_api.png",
        "papi": BROLL_DIR / "glass_papi.png",
        "jantung": BROLL_DIR / "glass_jantung.png",
        "sante": BROLL_DIR / "glass_sante.png",
        "santet": BROLL_DIR / "glass_santet.png",
    }


# ---------------------------------------------------------------------------
# 3. Master Edit Decision List (EDL)
# ---------------------------------------------------------------------------
SEGMENTS = [
    # 1. Opening Title Hook (0:00 -> 3.12s) — Both 'challenge' and 'BIKIN KATA 🔥' show from 0:00
    {"id": 1,  "src": "main", "start": 1.04,  "end": 1.72,  "mode": "normal",    "word_so_far": "", "girl_letter": "", "guy_letter": "", "sfx": "whoosh", "glass": "hook1"},
    {"id": 2,  "src": "main", "start": 1.72,  "end": 3.12,  "mode": "zoom_both", "word_so_far": "", "girl_letter": "", "guy_letter": "", "sfx": "pop",    "glass": "hook2"},

    # Round 1: A - P - I (Word made at seg 5-6 -> bottom word tracker cleared!)
    {"id": 3,  "src": "main", "start": 5.25,  "end": 5.70,  "mode": "normal",    "word_so_far": "a",   "girl_letter": "A", "guy_letter": "",  "sfx": "pop"},
    {"id": 4,  "src": "main", "start": 5.92,  "end": 6.40,  "mode": "normal",    "word_so_far": "a p", "girl_letter": "A", "guy_letter": "P", "sfx": "pop"},
    {"id": 5,  "src": "main", "start": 7.36,  "end": 8.20,  "mode": "zoom_both", "word_so_far": "",    "girl_letter": "I", "guy_letter": "P", "sfx": "win", "glass": "api"},
    {"id": 6,  "src": "main", "start": 9.15,  "end": 10.00, "mode": "zoom_both", "word_so_far": "",    "girl_letter": "I", "guy_letter": "",  "sfx": "",    "glass": "api"},

    # Round 2: P - A - P - I
    {"id": 7,  "src": "main", "start": 11.48, "end": 11.95, "mode": "normal",    "word_so_far": "p",     "girl_letter": "",  "guy_letter": "P", "sfx": "pop"},
    {"id": 8,  "src": "main", "start": 12.40, "end": 12.86, "mode": "normal",    "word_so_far": "p a",   "girl_letter": "A", "guy_letter": "P", "sfx": "pop"},
    {"id": 9,  "src": "main", "start": 13.66, "end": 14.18, "mode": "normal",    "word_so_far": "p a p", "girl_letter": "A", "guy_letter": "P", "sfx": "pop"},
    {"id": 10, "src": "main", "start": 15.68, "end": 17.65, "mode": "zoom_both", "word_so_far": "",      "girl_letter": "I", "guy_letter": "P", "sfx": "win", "glass": "papi"},
    {"id": 11, "src": "main", "start": 17.90, "end": 20.50, "mode": "zoom_both", "word_so_far": "",      "girl_letter": "",  "guy_letter": "",  "sfx": "",    "glass": "papi"},

    # Round 3: J - A - N - T - U - N - G
    {"id": 12, "src": "main", "start": 22.36, "end": 22.88, "mode": "normal",    "word_so_far": "j",           "girl_letter": "J", "guy_letter": "",  "sfx": "pop"},
    {"id": 13, "src": "main", "start": 23.40, "end": 23.94, "mode": "normal",    "word_so_far": "j a",         "girl_letter": "J", "guy_letter": "A", "sfx": "pop"},
    {"id": 14, "src": "main", "start": 26.36, "end": 26.88, "mode": "normal",    "word_so_far": "j a n",       "girl_letter": "N", "guy_letter": "A", "sfx": "pop"},
    {"id": 15, "src": "main", "start": 28.96, "end": 30.45, "mode": "zoom_both", "word_so_far": "j a n t",    "girl_letter": "N", "guy_letter": "T", "sfx": "pop"},
    {"id": 16, "src": "main", "start": 33.00, "end": 34.55, "mode": "zoom_both", "word_so_far": "j a n t",    "girl_letter": "N", "guy_letter": "T", "sfx": ""},
    {"id": 17, "src": "main", "start": 35.90, "end": 36.38, "mode": "normal",    "word_so_far": "j a n t u",   "girl_letter": "U", "guy_letter": "T", "sfx": "pop"},
    {"id": 18, "src": "main", "start": 38.80, "end": 39.35, "mode": "normal",    "word_so_far": "j a n t u n", "girl_letter": "U", "guy_letter": "N", "sfx": "pop"},
    {"id": 19, "src": "main", "start": 39.88, "end": 42.10, "mode": "zoom_both", "word_so_far": "",            "girl_letter": "G", "guy_letter": "N", "sfx": "win", "glass": "jantung"},
    {"id": 20, "src": "main", "start": 42.70, "end": 43.85, "mode": "zoom_both", "word_so_far": "",            "girl_letter": "",  "guy_letter": "",  "sfx": "",    "glass": "jantung"},

    # Round 4: S - A - N - T - E -> Fast Zoom-In to Arthur + Black & White -> What_ Meme -> Outro Laugh
    {"id": 21, "src": "main", "start": 44.50, "end": 45.14, "mode": "normal",    "word_so_far": "s",         "girl_letter": "",  "guy_letter": "S", "sfx": "pop"},
    {"id": 22, "src": "main", "start": 46.26, "end": 46.74, "mode": "normal",    "word_so_far": "s a",       "girl_letter": "A", "guy_letter": "S", "sfx": "pop"},
    {"id": 23, "src": "main", "start": 47.26, "end": 47.84, "mode": "normal",    "word_so_far": "s a n",     "girl_letter": "A", "guy_letter": "N", "sfx": "pop"},
    {"id": 24, "src": "main", "start": 49.55, "end": 50.90, "mode": "zoom_both", "word_so_far": "s a n",     "girl_letter": "A", "guy_letter": "N", "sfx": ""},
    {"id": 25, "src": "main", "start": 51.70, "end": 53.50, "mode": "zoom_both", "word_so_far": "s a n",     "girl_letter": "A", "guy_letter": "N", "sfx": ""},
    {"id": 26, "src": "main", "start": 54.95, "end": 55.44, "mode": "normal",    "word_so_far": "s a n t",   "girl_letter": "T", "guy_letter": "N", "sfx": "pop"},
    {"id": 27, "src": "main", "start": 58.35, "end": 58.88, "mode": "normal",    "word_so_far": "s a n t e", "girl_letter": "T", "guy_letter": "E", "sfx": "pop"},
    {"id": 28, "src": "main", "start": 62.20, "end": 64.08, "mode": "zoom_both", "word_so_far": "",         "girl_letter": "T", "guy_letter": "E", "sfx": "", "glass": "sante"},
    {"id": 29, "src": "main", "start": 65.90, "end": 66.62, "mode": "zoom_angel","word_so_far": "",         "girl_letter": "",  "guy_letter": "",  "sfx": "", "glass": "sante"},
    {"id": 30, "src": "main", "start": 67.90, "end": 70.15, "mode": "zoom_both", "word_so_far": "",         "girl_letter": "",  "guy_letter": "",  "sfx": "", "glass": "sante"},
    {"id": 31, "src": "main", "start": 71.18, "end": 74.15, "mode": "zoom_angel","word_so_far": "",         "girl_letter": "",  "guy_letter": "",  "sfx": "", "glass": "sante"},
    {"id": 32, "src": "main", "start": 74.75, "end": 76.10, "mode": "zoom_both", "word_so_far": "",         "girl_letter": "",  "guy_letter": "",  "sfx": "boom", "glass": "santet"},
    {"id": 33, "src": "freeze_arthur", "start": 76.08, "end": 77.08, "mode": "freeze_arthur_bw", "word_so_far": "", "girl_letter": "", "guy_letter": "", "sfx": "whoosh"},
    {"id": 34, "src": "what_meme",     "start": 0.35,  "end": 4.75,  "mode": "what_meme",        "word_so_far": "", "girl_letter": "", "guy_letter": "", "sfx": ""},
    {"id": 35, "src": "main", "start": 76.85, "end": 80.25, "mode": "zoom_both", "word_so_far": "",         "girl_letter": "",  "guy_letter": "",  "sfx": ""},
]


# ---------------------------------------------------------------------------
# 4. Dynamic Spoken Captions (Rule 49 & Rule 38)
#    - One word at a time, synced to speech, vanishes on pause
#    - No captions during opening title hook (0:00 -> 3.12s)
# ---------------------------------------------------------------------------
DYNAMIC_WORDS = [
    # Seg 11: Papi bahasa Indonesia kan? (raw: 17.90 -> 20.50)
    (17.95, 18.25, "Papi"),
    (18.30, 18.70, "bahasa"),
    (18.75, 19.45, "Indonesia"),
    (19.50, 20.10, "kan?"),

    # Seg 15: T?! (raw: 28.96 -> 30.45)
    (29.20, 29.85, "T?!"),

    # Seg 16: Emang bisa? Bisa! (raw: 33.00 -> 34.55)
    (33.08, 33.40, "Emang"),
    (33.40, 33.85, "bisa?"),
    (33.85, 34.35, "Bisa!"),

    # Seg 20: Kalah lagi! (raw: 42.70 -> 43.85)
    (42.70, 43.20, "Kalah"),
    (43.20, 43.75, "lagi!"),

    # Seg 24: S-A-N? Iya! (raw: 49.55 -> 50.90)
    (49.65, 50.20, "S-A-N?"),
    (50.25, 50.80, "Iya!"),

    # Seg 25: Ayo cepet! (raw: 51.70 -> 53.50)
    (51.75, 52.15, "Ayo"),
    (52.15, 52.80, "cepet!"),

    # Seg 28: E?! S-A-N-T-E?! (raw: 62.20 -> 64.08)
    (62.30, 62.75, "E?!"),
    (62.80, 63.85, "S-A-N-T-E?!"),

    # Seg 29: Sante? (raw: 65.90 -> 66.62)
    (65.95, 66.55, "Sante?"),

    # Seg 30: Sante! Bisa, nyante kan sante! (raw: 67.90 -> 70.15)
    (68.00, 68.55, "Sante!"),
    (68.65, 69.05, "Bisa,"),
    (69.15, 69.50, "nyante"),
    (69.50, 69.75, "kan"),
    (69.75, 70.10, "sante!"),

    # Seg 31: Itu bukan bahasa Indonesia yang baik dan benar! (raw: 71.18 -> 74.15)
    (71.25, 71.60, "Itu"),
    (71.70, 72.05, "bukan"),
    (72.20, 72.65, "bahasa"),
    (72.65, 73.15, "Indonesia"),
    (73.15, 73.40, "yang"),
    (73.40, 73.65, "baik"),
    (73.65, 73.85, "dan"),
    (73.85, 74.15, "benar!"),

    # Seg 32: Gua tadinya mau bilang SANTET! (raw: 74.75 -> 76.10)
    (74.80, 75.05, "Gua"),
    (75.05, 75.45, "tadinya"),
    (75.45, 75.65, "mau"),
    (75.65, 75.85, "bilang"),
    (75.85, 76.10, "SANTET!"),

    # Seg 35: Parah banget! (raw: 76.85 -> 80.25)
    (76.95, 77.40, "Parah"),
    (77.40, 77.95, "banget!"),
]


def fmt_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def generate_ass_subtitles(ass_path: Path) -> list[dict]:
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: WordTable,Arial Black,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,2.4,3.8,5,40,40,40,1
Style: DynamicWord,Arial Black,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0.5,0,1,3.0,4.0,5,60,60,60,1
Style: HeadLetterGirl,Arial Black,125,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.2,4.5,5,20,20,20,1
Style: HeadLetterGuy,Arial Black,125,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.2,4.5,5,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    timeline_cursor = 0.0
    timeline_events = []

    prev_girl = ""
    prev_guy = ""

    for seg in SEGMENTS:
        raw_dur = seg["end"] - seg["start"]
        n_frames = max(1, int(round(raw_dur * 30.0)))
        dur = n_frames / 30.0
        t0 = timeline_cursor
        t1 = t0 + dur
        timeline_cursor = t1

        st_str = fmt_ass_time(t0)
        et_str = fmt_ass_time(t1)

        # 1. Lower-bottom Word Tracker on the wooden table (only while building a word!)
        if seg["word_so_far"]:
            lines.append(
                f"Dialogue: 2,{st_str},{et_str},WordTable,,0,0,0,,{{\\pos(540,1455)}}{seg['word_so_far'].upper()}\n"
            )

        # 2. Bold Letter on top of Angel's Head (Left: x=305, y=510 — aligned with Arthur!)
        gl = seg["girl_letter"]
        if gl:
            if gl != prev_girl:
                anim = r"{\pos(305,510)\fscx150\fscy150\t(0,135,\fscx100\fscy100)}"
            else:
                anim = r"{\pos(305,510)}"
            lines.append(f"Dialogue: 4,{st_str},{et_str},HeadLetterGirl,,0,0,0,,{anim}{gl}\n")
        prev_girl = gl

        # 3. Bold Letter on top of Arthur's Head (Right: x=760, y=510 — aligned with Angel!)
        bl = seg["guy_letter"]
        if bl:
            if bl != prev_guy:
                anim = r"{\pos(760,510)\fscx150\fscy150\t(0,135,\fscx100\fscy100)}"
            else:
                anim = r"{\pos(760,510)}"
            lines.append(f"Dialogue: 4,{st_str},{et_str},HeadLetterGuy,,0,0,0,,{anim}{bl}\n")
        prev_guy = bl

        ev_info = {
            **seg,
            "n_frames": n_frames,
            "t0": round(t0, 4),
            "t1": round(t1, 4),
            "dur": round(dur, 4),
        }
        timeline_events.append(ev_info)

    # 4. Map Dynamic Spoken Words (Rule 49: Strictly One Word at a Time)
    for w_start, w_end, text in DYNAMIC_WORDS:
        # Find which segment contains this word
        for ev in timeline_events:
            if ev["src"] == "main" and not (w_end <= ev["start"] or w_start >= ev["end"]):
                # Overlaps with this segment
                overlap_raw_start = max(w_start, ev["start"])
                overlap_raw_end = min(w_end, ev["end"])
                if overlap_raw_end > overlap_raw_start:
                    tl_start = ev["t0"] + (overlap_raw_start - ev["start"])
                    tl_end = ev["t0"] + (overlap_raw_end - ev["start"])

                    # If word_so_far is present, place slightly lower (1585) so it doesn't overlap the tracker
                    y_pos = 1585 if ev["word_so_far"] else 1500
                    lines.append(
                        f"Dialogue: 3,{fmt_ass_time(tl_start)},{fmt_ass_time(tl_end)},DynamicWord,,0,0,0,,{{\\pos(540,{y_pos})}}{text}\n"
                    )

    ass_path.write_text("".join(lines), encoding="utf-8")
    return timeline_events


# ---------------------------------------------------------------------------
# 5. Build Master Video Pipeline
# ---------------------------------------------------------------------------
def build_video() -> None:
    print("🎵 [1/4] Verifying Chopin Nocturne in Eb & studio SFX...")
    win_sfx, boom_sfx, pop_sfx, whoosh_sfx, music_path = get_audio_assets()

    print("🖼️  [2/4] Rendering Reference-Style Title & Word Overlays via Swift...")
    cards = render_graphics_swift()

    ass_path = DRAFT_DIR / "bikin_kata_captions.ass"
    timeline_events = generate_ass_subtitles(ass_path)
    edl_json_path = DRAFT_DIR / "bikin_kata_edl.json"
    edl_json_path.write_text(json.dumps(timeline_events, indent=2), encoding="utf-8")

    print(f"✂️  [3/4] Processing {len(SEGMENTS)} segments with consistent natural color grading & B&W zoom...")
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
            af = f"aresample=48000,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.015,afade=t=out:st={fade_out_st:.3f}:d=0.015,apad=whole_dur={dur:.4f},atrim=0:{dur:.4f},asetpts=PTS-STARTPTS"

            if src == "main":
                # Consistent natural color grading across every segment from 0:00 to the end!
                if mode == "zoom_both":
                    vf = f"scale=1080*1.08:1920*1.08,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.42,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
                elif mode == "zoom_angel":
                    vf = f"scale=1080*1.45:1920*1.45,crop=1080:1920:90:430,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
                elif mode == "zoom_arthur":
                    vf = f"scale=1080*1.55:1920*1.55,crop=1080:1920:490:360,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
                else:
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
                # Extract high-res frame at 76.08s, then fast zoompan transition
                # onto Arthur's face while switching to Black & White (Rule 42)!
                freeze_png = Path(tmpdir) / "arthur_full_frame.png"
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
                    f"zoompan=z='min(2.15,1.15+1.00*min(1,on/5))':"
                    f"x='(iw-iw/zoom)*0.96':"
                    f"y='(ih-ih/zoom)*0.27':"
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
                # Rule 43: Zoomed-out portrait framing on green hoodie guy (1080x1440 over blurred background)
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

        print("🎬 [4/4] Compositing Reference-Style Title, Top Words, Dynamic Captions & Chopin Nocturne...")
        final_mp4 = FINAL_DIR / "bikin_kata_challenge_final.mp4"
        cover_png = FINAL_DIR / "bikin_kata_cover.png"
        draft_preview = DRAFT_DIR / "bikin_kata_preview.mp4"

        glass_windows: dict[str, list[float]] = {}
        freeze_window = [0.0, 0.0]
        what_meme_window = [0.0, 0.0]
        for ev in timeline_events:
            g = ev.get("glass")
            if g:
                if g not in glass_windows:
                    glass_windows[g] = [ev["t0"], ev["t1"]]
                else:
                    glass_windows[g][1] = ev["t1"]
            if ev["src"] == "freeze_arthur":
                freeze_window = [ev["t0"], ev["t1"]]
            if ev["src"] == "what_meme":
                what_meme_window = [ev["t0"], ev["t1"]]

        w_h1 = glass_windows["hook1"]
        w_h2 = glass_windows["hook2"]
        w_api = glass_windows["api"]
        w_papi = glass_windows["papi"]
        w_jantung = glass_windows["jantung"]
        w_sante = glass_windows["sante"]
        w_santet = glass_windows["santet"]

        total_dur = timeline_events[-1]["t1"]
        sr = 48000
        sfx_track = np.zeros(int((total_dur + 1.0) * sr), dtype=np.float32)

        def load_wav(p: Path) -> np.ndarray:
            with wave.open(str(p), "rb") as w:
                return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

        wav_map = {
            "pop": load_wav(pop_sfx) * 0.65,
            "whoosh": load_wav(whoosh_sfx) * 0.55,
            "win": load_wav(win_sfx) * 0.65,
            "boom": load_wav(boom_sfx) * 0.85,
        }

        for ev in timeline_events:
            sfx_name = ev.get("sfx")
            if sfx_name and sfx_name in wav_map:
                samples = wav_map[sfx_name]
                i0 = int(ev["t0"] * sr)
                i1 = min(len(sfx_track), i0 + len(samples))
                sfx_track[i0:i1] += samples[: i1 - i0]

        sfx_wav_path = Path(tmpdir) / "sfx_timeline.wav"
        with wave.open(str(sfx_wav_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes((np.clip(sfx_track, -0.95, 0.95) * 32767).astype(np.int16).tobytes())

        ass_escaped = str(ass_path).replace("\\", "/").replace(":", "\\:")

        v_filter = (
            f"[0:v]ass='{ass_escaped}'[v_ass];"
            f"[v_ass][1:v]overlay=0:0:enable='between(t,{w_h1[0]:.3f},{w_h1[1]:.3f})'[vh1];"
            f"[vh1][2:v]overlay=0:0:enable='between(t,{w_h2[0]:.3f},{w_h2[1]:.3f})'[vh2];"
            f"[vh2][3:v]overlay=0:0:enable='between(t,{w_api[0]:.3f},{w_api[1]:.3f})'[v1];"
            f"[v1][4:v]overlay=0:0:enable='between(t,{w_papi[0]:.3f},{w_papi[1]:.3f})'[v2];"
            f"[v2][5:v]overlay=0:0:enable='between(t,{w_jantung[0]:.3f},{w_jantung[1]:.3f})'[v3];"
            f"[v3][6:v]overlay=0:0:enable='between(t,{w_sante[0]:.3f},{w_sante[1]:.3f})'[v4];"
            f"[v4][7:v]overlay=0:0:enable='between(t,{w_santet[0]:.3f},{w_santet[1]:.3f})'[vout]"
        )

        fz0, fz1 = freeze_window
        wm0, wm1 = what_meme_window
        # Rule 44 & Rule 46:
        # Chopin Nocturne in Eb sits at -20 dB (0.10) under dialogue, swells to 0.48 on B&W zoom,
        # and dips sharply to 0.03 during What_ Meme.mp4
        a_filter = (
            "[0:a]highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11[voice];"
            f"[8:a]volume='if(between(t,{fz0:.2f},{fz1:.2f}),0.48,if(between(t,{wm0:.2f},{wm1:.2f}),0.03,0.10))':eval=frame[bgm];"
            "[9:a]volume=0.85[sfx];"
            "[voice][bgm][sfx]amix=inputs=3:duration=first:dropout_transition=2:normalize=0[aout]"
        )

        # Stage 2: Master Final Render
        run_cmd([
            "ffmpeg", "-y",
            "-i", str(stitched_mov),
            "-i", str(cards["hook1"]),
            "-i", str(cards["hook2"]),
            "-i", str(cards["api"]),
            "-i", str(cards["papi"]),
            "-i", str(cards["jantung"]),
            "-i", str(cards["sante"]),
            "-i", str(cards["santet"]),
            "-stream_loop", "-1", "-i", str(music_path),
            "-i", str(sfx_wav_path),
            "-filter_complex", f"{v_filter};{a_filter}",
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "320k",
            "-shortest",
            "-loglevel", "error",
            str(final_mp4),
        ])

        # Export Cover Image at 1.40s
        run_cmd([
            "ffmpeg", "-y",
            "-ss", "1.40",
            "-i", str(final_mp4),
            "-frames:v", "1",
            "-loglevel", "error",
            str(cover_png),
        ])

        # Stage 1: Draft Preview for fast review
        run_cmd([
            "ffmpeg", "-y",
            "-i", str(final_mp4),
            "-vf", "scale=-2:720",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
            "-c:a", "aac", "-b:a", "96k",
            "-loglevel", "error",
            str(draft_preview),
        ])

    print(f"✅ Final video rendered:  {final_mp4}")
    print(f"🖼️  Cover image exported: {cover_png}")
    print(f"📱 Draft preview:        {draft_preview}")


if __name__ == "__main__":
    build_video()
