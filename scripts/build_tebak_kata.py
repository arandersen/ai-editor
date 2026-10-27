#!/usr/bin/env python3
"""
Master Builder for "Tebak Kata Challenge" (Couple Content Game - Vertical 9:16)
Creative Director & Video Editor: Gemini 4 Argon (Antigravity)

Following Master Rules:
- Rule 37: Left Player is Angel, Right Player is Arthur. No scoreboards or point counters.
- Rule 38: Opening Title Hook & Cover Image:
  - Both lines shown from 0:00: Line 1 'challenge' + Line 2 'TEBAK KATA 🧠'
  - Line 1: HelveticaNeue-Bold (66pt), Black fill with crisp White outline
  - Line 2: Arial-Black (88pt), Pure White fill with thin dark edge and drop shadow
  - Natural camera color grading 100% consistent from 0:00 to end
  - No bottom caption during opening title hook
  - Cover saved to renders/final/Tebak Kata/tebak_kata_cover.png
- Rule 39: Unified clean typography across title, top callouts, head letters & bottom captions
- Rule 40: Above-Head Bold Word Pops aligned horizontally at y=510 (Angel at x=305, Arthur at x=760) with pop.wav
- Rule 41: Borderless Word Callouts at Top (y=235) — just word + emoji / result (no liquid glass box)
- Rule 42: Fast Zoom-In Transition + Black & White on Punchline Reaction (Arthur's frustration zoom)
- Rule 43: Comfortable Portrait Framing on What_ Meme.mp4 (1080x1440 over soft matching backdrop)
- Rule 44: Authentic Chopin Nocturne in E-flat major, Op. 9, No. 2 (nocturne_op9_in_eb.wav) ducked to -20 dB
- Rule 45: Per-Project Output Folder (renders/final/Tebak Kata/, renders/drafts/Tebak Kata/, etc.)
- Rule 46: +14 dB volume boost on reaction meme cutaway with background music ducked to 0.03
- Rule 49: Dynamic one-word spoken captions synced to exact millisecond timestamps (no emoji glyph boxes in ASS)
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
PROJECT_NAME = "Tebak Kata"
RAW_VIDEO = WORKSPACE / f"raw/{PROJECT_NAME}/IMG_0680.MOV"
MEME_VIDEO = WORKSPACE / "Meme Material/What_ Meme.mp4"
MUSIC_WAV = WORKSPACE / "audio/music/nocturne_op9_in_eb.wav"
AUDIO_DIR = WORKSPACE / "audio"
SFX_DIR = AUDIO_DIR / "sfx"
BROLL_DIR = WORKSPACE / f"broll/{PROJECT_NAME}"
DRAFT_DIR = WORKSPACE / f"renders/drafts/{PROJECT_NAME}"
FINAL_DIR = WORKSPACE / f"renders/final/{PROJECT_NAME}"

for d in [BROLL_DIR, DRAFT_DIR, FINAL_DIR]:
    d.mkdir(parents=True, exist_ok=True)

ENV = os.environ.copy()
ENV["PATH"] = f"/opt/homebrew/bin:/usr/local/bin:{Path.home() / '.local/bin'}:{ENV.get('PATH', '')}"


def run_cmd(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, env=ENV)


# ---------------------------------------------------------------------------
# 1. Render High-Contrast Graphics via Swift (Native AppKit)
# ---------------------------------------------------------------------------
def render_graphics_swift() -> dict[str, Path]:
    print("🎨 [1/4] Rendering 1080x1920 High-Contrast Graphics via Swift...")
    swift_code = f"""
import AppKit
import Foundation

let outDir = "{BROLL_DIR}"
try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true, attributes: nil)

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
    NSGraphicsContext.current = ctx
    return (rep, ctx)
}}

func savePNG(_ rep: NSBitmapImageRep, _ filename: String) {{
    let url = URL(fileURLWithPath: "\\(outDir)/\\(filename)")
    let pngData = rep.representation(using: .png, properties: [:])!
    try! pngData.write(to: url)
}}

let pCenter = NSMutableParagraphStyle()
pCenter.alignment = .center

let fontSub  = NSFont(name: "HelveticaNeue-Bold", size: 66) ?? NSFont.boldSystemFont(ofSize: 66)
let fontMain = NSFont(name: "Arial-Black", size: 88) ?? NSFont.boldSystemFont(ofSize: 88)
let fontTop  = NSFont(name: "Arial-Black", size: 80) ?? NSFont.boldSystemFont(ofSize: 80)
let fontHead = NSFont(name: "Arial-Black", size: 76) ?? NSFont.boldSystemFont(ofSize: 76)

// Line 1: 'challenge' in Black with White Outline
func drawBlackWithWhiteOutline(_ text: String, rect: NSRect, font: NSFont) {{
    let sh = NSShadow()
    sh.shadowColor = NSColor(calibratedWhite: 0.0, alpha: 0.35)
    sh.shadowBlurRadius = 8.0
    sh.shadowOffset = NSSize(width: 0, height: -4)

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
func drawWhiteBeanBoozleStyle(_ text: String, rect: NSRect, font: NSFont, accentColor: NSColor = .white) {{
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
        .foregroundColor: accentColor,
        .paragraphStyle: pCenter,
        .kern: -1.5
    ]
    NSAttributedString(string: text, attributes: b2).draw(in: rect)
}}

// 1. Opening Title Hook (Show both lines from 0:00)
for step in 1...2 {{
    let (rep, _) = createCanvas()
    drawBlackWithWhiteOutline(
        "challenge",
        rect: NSRect(x: 40, y: 1355, width: 1000, height: 100),
        font: fontSub
    )
    drawWhiteBeanBoozleStyle(
        "TEBAK KATA 🧠",
        rect: NSRect(x: 30, y: 1235, width: 1020, height: 130),
        font: fontMain
    )
    savePNG(rep, "hook_tebak_\\(step).png")
}}

// 2. Top Result Overlays (Borderless, pure word + emoji)
// In AppKit coords: y=1555 is ~235px from top
struct TopCallout {{
    let filename: String
    let text: String
    let color: NSColor
}}

let topCallouts: [TopCallout] = [
    TopCallout(filename: "top_bisa.png", text: "BISA ❌", color: .white),
    TopCallout(filename: "top_rapi.png", text: "RAPI ❌", color: .white),
    TopCallout(filename: "top_jari.png", text: "JARI ❌", color: .white),
    TopCallout(filename: "top_koki.png", text: "KOKI 1️⃣", color: .white),
    TopCallout(filename: "top_sari.png", text: "SARI ❌", color: .white),
    TopCallout(filename: "top_soto.png", text: "SOTO 1️⃣", color: .white),
    TopCallout(filename: "top_bola.png", text: "BOLA 1️⃣", color: .white),
    TopCallout(filename: "top_meja.png", text: "MEJA ❌", color: .white),
    TopCallout(filename: "top_joki.png", text: "JOKI 1️⃣", color: .white),
    TopCallout(filename: "top_ayam.png", text: "AYAM 2️⃣", color: .white),
    TopCallout(filename: "top_tape.png", text: "TAPE 3️⃣", color: NSColor(red: 1.0, green: 0.85, blue: 0.2, alpha: 1.0)),
    TopCallout(filename: "top_tali.png", text: "TALI ❌", color: .white),
    TopCallout(filename: "top_akar.png", text: "AKAR 🏆", color: NSColor(red: 0.35, green: 1.0, blue: 0.35, alpha: 1.0)),
    TopCallout(filename: "top_lope.png", text: "LOPE-LOPE 💕", color: NSColor(red: 1.0, green: 0.45, blue: 0.75, alpha: 1.0)),
]

for tc in topCallouts {{
    let (rep, _) = createCanvas()
    drawWhiteBeanBoozleStyle(
        tc.text,
        rect: NSRect(x: 40, y: 1555, width: 1000, height: 130),
        font: fontTop,
        accentColor: tc.color
    )
    savePNG(rep, tc.filename)
}}

// 3. Above-Head Word Callouts (Rule 40: Aligned at y=510 from top -> y=1280 in AppKit)
// Angel at x=305 (center width 460 -> x=75), Arthur at x=760 (center width 460 -> x=530)
struct HeadCallout {{
    let filename: String
    let text: String
    let isAngel: Bool
}}

let headCallouts: [HeadCallout] = [
    // Angel's guesses
    HeadCallout(filename: "head_angel_bisa.png", text: "BISA", isAngel: true),
    HeadCallout(filename: "head_angel_jari.png", text: "JARI", isAngel: true),
    HeadCallout(filename: "head_angel_sari.png", text: "SARI", isAngel: true),
    HeadCallout(filename: "head_angel_bola.png", text: "BOLA", isAngel: true),
    HeadCallout(filename: "head_angel_akar.png", text: "AKAR!", isAngel: true),
    // Arthur's guesses
    HeadCallout(filename: "head_arthur_rapi.png", text: "RAPI", isAngel: false),
    HeadCallout(filename: "head_arthur_koki.png", text: "KOKI", isAngel: false),
    HeadCallout(filename: "head_arthur_soto.png", text: "SOTO", isAngel: false),
    HeadCallout(filename: "head_arthur_meja.png", text: "MEJA", isAngel: false),
    HeadCallout(filename: "head_arthur_joki.png", text: "JOKI", isAngel: false),
    HeadCallout(filename: "head_arthur_ayam.png", text: "AYAM", isAngel: false),
    HeadCallout(filename: "head_arthur_tape.png", text: "TAPE", isAngel: false),
    HeadCallout(filename: "head_arthur_tali.png", text: "TALI", isAngel: false),
]

for hc in headCallouts {{
    let (rep, _) = createCanvas()
    let rx: CGFloat = hc.isAngel ? 75 : 530
    drawWhiteBeanBoozleStyle(
        hc.text,
        rect: NSRect(x: rx, y: 1280, width: 460, height: 110),
        font: fontHead
    )
    savePNG(rep, hc.filename)
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
        "hook1": BROLL_DIR / "hook_tebak_1.png",
        "hook2": BROLL_DIR / "hook_tebak_2.png",
        # Top Callouts
        "top_bisa": BROLL_DIR / "top_bisa.png",
        "top_rapi": BROLL_DIR / "top_rapi.png",
        "top_jari": BROLL_DIR / "top_jari.png",
        "top_koki": BROLL_DIR / "top_koki.png",
        "top_sari": BROLL_DIR / "top_sari.png",
        "top_soto": BROLL_DIR / "top_soto.png",
        "top_bola": BROLL_DIR / "top_bola.png",
        "top_meja": BROLL_DIR / "top_meja.png",
        "top_joki": BROLL_DIR / "top_joki.png",
        "top_ayam": BROLL_DIR / "top_ayam.png",
        "top_tape": BROLL_DIR / "top_tape.png",
        "top_tali": BROLL_DIR / "top_tali.png",
        "top_akar": BROLL_DIR / "top_akar.png",
        "top_lope": BROLL_DIR / "top_lope.png",
        # Above-head
        "head_angel_bisa": BROLL_DIR / "head_angel_bisa.png",
        "head_angel_jari": BROLL_DIR / "head_angel_jari.png",
        "head_angel_sari": BROLL_DIR / "head_angel_sari.png",
        "head_angel_bola": BROLL_DIR / "head_angel_bola.png",
        "head_angel_akar": BROLL_DIR / "head_angel_akar.png",
        "head_arthur_rapi": BROLL_DIR / "head_arthur_rapi.png",
        "head_arthur_koki": BROLL_DIR / "head_arthur_koki.png",
        "head_arthur_soto": BROLL_DIR / "head_arthur_soto.png",
        "head_arthur_meja": BROLL_DIR / "head_arthur_meja.png",
        "head_arthur_joki": BROLL_DIR / "head_arthur_joki.png",
        "head_arthur_ayam": BROLL_DIR / "head_arthur_ayam.png",
        "head_arthur_tape": BROLL_DIR / "head_arthur_tape.png",
        "head_arthur_tali": BROLL_DIR / "head_arthur_tali.png",
    }


# ---------------------------------------------------------------------------
# 2. Edit Decision List (EDL) Segments
# ---------------------------------------------------------------------------
# Fast-paced deduction duel + climax + frustration + meme
SEGMENTS = [
    # 1. Opening Hook (0:00 -> ~4.5s)
    # Line 1 'challenge' + Line 2 'TEBAK KATA 🧠' displayed from 0:00!
    {"id": 1,  "src": "main", "start": 1.15,  "end": 2.20,  "mode": "normal",    "top": "top_hook1", "head": "", "sfx": "whoosh"},
    {"id": 2,  "src": "main", "start": 2.20,  "end": 3.40,  "mode": "zoom_both", "top": "top_hook2", "head": "", "sfx": "pop"},
    {"id": 3,  "src": "main", "start": 3.40,  "end": 5.40,  "mode": "zoom_both", "top": "", "head": "", "sfx": "pop"},
    {"id": 4,  "src": "main", "start": 6.70,  "end": 8.70,  "mode": "normal",    "top": "", "head": "", "sfx": ""},

    # Guess 1: Angel guesses "BISA"
    {"id": 5,  "src": "main", "start": 9.50,  "end": 10.60, "mode": "zoom_angel", "top": "", "head": "head_angel_bisa", "sfx": "pop"},
    {"id": 6,  "src": "main", "start": 11.20, "end": 13.50, "mode": "zoom_arthur", "top": "top_bisa", "head": "", "sfx": "pop"},

    # Guess 2: Arthur guesses "RAPI"
    {"id": 7,  "src": "main", "start": 15.20, "end": 16.50, "mode": "zoom_arthur", "top": "", "head": "head_arthur_rapi", "sfx": "pop"},
    {"id": 8,  "src": "main", "start": 17.20, "end": 18.50, "mode": "zoom_angel", "top": "top_rapi", "head": "", "sfx": "pop"},

    # Guess 3: Angel guesses "JARI"
    {"id": 9,  "src": "main", "start": 23.50, "end": 24.80, "mode": "zoom_angel", "top": "", "head": "head_angel_jari", "sfx": "pop"},
    {"id": 10, "src": "main", "start": 25.40, "end": 27.50, "mode": "zoom_arthur", "top": "top_jari", "head": "", "sfx": "pop"},

    # Guess 4: Arthur guesses "KOKI"
    {"id": 11, "src": "main", "start": 33.50, "end": 36.50, "mode": "zoom_arthur", "top": "", "head": "head_arthur_koki", "sfx": "pop"},
    {"id": 12, "src": "main", "start": 37.00, "end": 40.50, "mode": "zoom_angel", "top": "top_koki", "head": "", "sfx": "pop"},

    # Guess 5: Angel guesses "SARI"
    {"id": 13, "src": "main", "start": 41.80, "end": 43.20, "mode": "zoom_angel", "top": "", "head": "head_angel_sari", "sfx": "pop"},
    {"id": 14, "src": "main", "start": 43.80, "end": 46.20, "mode": "zoom_arthur", "top": "top_sari", "head": "", "sfx": "pop"},

    # Guess 6: Arthur guesses "SOTO"
    {"id": 15, "src": "main", "start": 50.40, "end": 52.00, "mode": "zoom_arthur", "top": "", "head": "head_arthur_soto", "sfx": "pop"},
    {"id": 16, "src": "main", "start": 52.20, "end": 55.20, "mode": "zoom_angel", "top": "top_soto", "head": "", "sfx": "pop"},

    # Guess 7: Angel guesses "BOLA"
    {"id": 17, "src": "main", "start": 91.20, "end": 93.00, "mode": "zoom_angel", "top": "", "head": "head_angel_bola", "sfx": "pop"},
    {"id": 18, "src": "main", "start": 93.80, "end": 96.00, "mode": "zoom_arthur", "top": "top_bola", "head": "", "sfx": "pop"},

    # Guess 8: Arthur guesses "MEJA"
    {"id": 19, "src": "main", "start": 102.00, "end": 104.20, "mode": "zoom_arthur", "top": "", "head": "head_arthur_meja", "sfx": "pop"},
    {"id": 20, "src": "main", "start": 104.80, "end": 107.00, "mode": "zoom_angel", "top": "top_meja", "head": "", "sfx": "pop"},

    # Guess 9: Arthur guesses "JOKI"
    {"id": 21, "src": "main", "start": 212.00, "end": 215.00, "mode": "zoom_arthur", "top": "", "head": "head_arthur_joki", "sfx": "pop"},
    {"id": 22, "src": "main", "start": 215.50, "end": 217.20, "mode": "zoom_angel", "top": "top_joki", "head": "", "sfx": "pop"},

    # Guess 10: Arthur guesses "AYAM" (Bener 2!)
    {"id": 23, "src": "main", "start": 217.40, "end": 218.80, "mode": "zoom_arthur", "top": "", "head": "head_arthur_ayam", "sfx": "pop"},
    {"id": 24, "src": "main", "start": 219.80, "end": 223.50, "mode": "zoom_angel", "top": "top_ayam", "head": "", "sfx": "pop"},

    # Guess 11: Arthur guesses "TAPE" (Bener 3!)
    {"id": 25, "src": "main", "start": 247.50, "end": 250.00, "mode": "zoom_arthur", "top": "", "head": "head_arthur_tape", "sfx": "pop"},
    {"id": 26, "src": "main", "start": 253.50, "end": 257.50, "mode": "zoom_both", "top": "top_tape", "head": "", "sfx": "win"},

    # Guess 12: Arthur guesses "TALI" (Salah semua!)
    {"id": 27, "src": "main", "start": 284.50, "end": 286.00, "mode": "zoom_arthur", "top": "", "head": "head_arthur_tali", "sfx": "pop"},
    {"id": 28, "src": "main", "start": 286.20, "end": 287.60, "mode": "zoom_angel", "top": "top_tali", "head": "", "sfx": "pop"},

    # Guess 13: Angel guesses "AKAR!" (ANGEL WINS!)
    {"id": 29, "src": "main", "start": 292.50, "end": 294.00, "mode": "zoom_angel", "top": "", "head": "head_angel_akar", "sfx": "pop"},
    {"id": 30, "src": "main", "start": 294.00, "end": 297.00, "mode": "zoom_both", "top": "top_akar", "head": "", "sfx": "win"},
    {"id": 31, "src": "main", "start": 297.00, "end": 298.20, "mode": "zoom_angel", "top": "top_akar", "head": "", "sfx": ""},

    # Climax Reveal & Frustration:
    # Arthur asks: "O-P-E belakangnya, depannya apa?!"
    {"id": 32, "src": "main", "start": 298.20, "end": 301.20, "mode": "zoom_arthur", "top": "", "head": "", "sfx": "pop"},
    # Angel: "Lope-lope!"
    {"id": 33, "src": "main", "start": 301.20, "end": 303.00, "mode": "zoom_angel", "top": "top_lope", "head": "", "sfx": "boom"},
    # Arthur disbelief: "Lope-lope bukan bahasa Indo!"
    {"id": 34, "src": "main", "start": 303.00, "end": 307.00, "mode": "zoom_both", "top": "top_lope", "head": "", "sfx": "pop"},
    # Arthur holds head: "Gak ada! Ini bahasa Indo baku! Lope-lope bukan bahasa Indo baku!"
    {"id": 35, "src": "main", "start": 307.00, "end": 313.80, "mode": "zoom_arthur", "top": "top_lope", "head": "", "sfx": ""},
    # Angel finger heart: "Gini... lope-lope!"
    {"id": 36, "src": "main", "start": 314.80, "end": 317.50, "mode": "zoom_angel", "top": "top_lope", "head": "", "sfx": "pop"},
    # Arthur screaming frustration: "Ini membuat gua frustrasi!"
    {"id": 37, "src": "main", "start": 317.50, "end": 320.20, "mode": "zoom_arthur", "top": "top_lope", "head": "", "sfx": ""},

    # Rule 42: Fast Zoom-In Transition + Black & White on Arthur's face
    {"id": 38, "src": "freeze_arthur", "start": 319.80, "end": 320.65, "mode": "freeze_bw", "top": "", "head": "", "sfx": "riser"},

    # Rule 43 & 46: What_ Meme Cutaway (Guy in green hoodie)
    {"id": 39, "src": "what_meme", "start": 0.00, "end": 1.95, "mode": "meme", "top": "", "head": "", "sfx": ""},

    # Outro: Arthur and Angel laughing together
    {"id": 40, "src": "main", "start": 320.80, "end": 323.50, "mode": "zoom_both", "top": "", "head": "", "sfx": "win"},
]


# ---------------------------------------------------------------------------
# 3. Dynamic One-Word Spoken Captions (Rule 49)
# ---------------------------------------------------------------------------
# Synced word-by-word with exact timestamps, no multi-sentence blocks, no emoji in ASS strings
CAPTIONS = [
    # Hook
    (1.15, 1.80, "Challenge"),
    (1.80, 2.50, "Tebak"),
    (2.50, 3.20, "Kata!"),
    (3.40, 4.30, "Ini kata gue!"),
    (4.40, 5.40, "Ini kata gue!"),
    (6.70, 7.70, "Ladies first deh,"),
    (7.80, 8.70, "kan always!"),

    # Round 1: BISA
    (9.50, 10.50, "Bisa!"),
    (11.20, 11.90, "Bisa..."),
    (12.00, 13.40, "Salah semua!"),

    # Round 2: RAPI
    (15.20, 16.30, "Rapi!"),
    (17.20, 18.40, "Salah semua!"),

    # Round 3: JARI
    (23.50, 24.60, "Jari!"),
    (25.40, 26.10, "Jari..."),
    (26.20, 27.40, "Salah semua!"),

    # Round 4: KOKI
    (33.50, 35.80, "Koki!"),
    (37.00, 38.30, "Bener satu!"),
    (38.60, 40.30, "Bener satu, oke!"),

    # Round 5: SARI
    (41.80, 43.00, "Sari!"),
    (43.80, 44.60, "Sari..."),
    (44.70, 46.10, "Salah semua!"),

    # Round 6: SOTO
    (50.40, 51.80, "Soto!"),
    (52.20, 53.30, "Salah..."),
    (53.40, 55.00, "Bener satu!"),

    # Round 7: BOLA
    (91.20, 92.80, "Bola!"),
    (93.80, 95.80, "Bener satu!"),

    # Round 8: MEJA
    (102.00, 103.80, "Meja!"),
    (104.80, 106.80, "Salah semua!"),

    # Round 9: JOKI
    (212.00, 214.50, "Joki!"),
    (215.50, 217.00, "Bener satu!"),

    # Round 10: AYAM
    (217.40, 218.60, "Ayam!"),
    (219.80, 221.20, "Bener dua!"),
    (221.40, 223.30, "Ayam bener dua!"),

    # Round 11: TAPE
    (247.50, 249.50, "Tape!"),
    (253.50, 255.00, "Tape..."),
    (255.10, 257.30, "Bener tiga!"),

    # Round 12: TALI
    (284.50, 285.80, "Tali!"),
    (286.20, 287.50, "Salah semua!"),

    # Round 13: AKAR
    (292.50, 293.80, "Akar!"),
    (294.00, 295.20, "Anjir bener!"),
    (295.30, 296.80, "Bener anjir!"),
    (297.00, 298.10, "Tadaaa!"),

    # Climax Reveal
    (298.20, 299.40, "Apaan teh..."),
    (299.50, 301.10, "O-P-E belakangnya, depannya apa?!"),
    (301.20, 302.80, "Lope-lope!"),
    (303.00, 304.80, "Lope-lope"),
    (304.90, 306.80, "bukan bahasa Indo!"),
    (307.00, 309.20, "Itu bukan bahasa Indo astaga!"),
    (309.40, 311.50, "Ini bahasa Indo baku!"),
    (311.60, 313.70, "Lope-lope bukan bahasa Indo baku!"),
    (314.80, 315.80, "Gini..."),
    (315.90, 317.40, "Lope-lope!"),
    (317.50, 319.80, "Ini membuat gua frustrasi!"),
]


def generate_ass_subtitles(timeline_events: list[dict], ass_path: Path) -> None:
    """Generate ASS subtitle file with word-by-word popping captions."""
    def sec_to_ass(s: float) -> str:
        h = int(s // 3600)
        m = int((s % 3600) // 60)
        sec = s % 60
        return f"{h}:{m:02d}:{sec:05.2f}"

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        # Clean Arial Black with pure white fill, thick black stroke & drop shadow (Rule 39)
        "Style: Default,Arial Black,72,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5.0,4.0,2,60,60,140,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    # Map raw timestamps to stitched timeline
    for cap_start, cap_end, text in CAPTIONS:
        # Find which event(s) cover this range
        for ev in timeline_events:
            if ev["src"] != "main":
                continue
            e_s, e_e = ev["start"], ev["end"]
            # Check overlap
            o_s = max(cap_start, e_s)
            o_e = min(cap_end, e_e)
            if o_e - o_s > 0.08:
                t0_out = ev["t0"] + (o_s - e_s)
                t1_out = ev["t0"] + (o_e - e_s)
                # Omit bottom caption during opening title hook (Rule 38)
                if t0_out < 4.0:
                    continue
                # Suppress captions during meme cutaway or freeze
                lines.append(f"Dialogue: 0,{sec_to_ass(t0_out)},{sec_to_ass(t1_out)},Default,,0,0,0,,{text}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# 4. Master Assembly & FFmpeg Rendering
# ---------------------------------------------------------------------------
def build_video():
    print("🚀 Starting Master Build for 'Tebak Kata Challenge'...")
    graphics = render_graphics_swift()

    # Calculate stitched timeline mapping
    timeline_events = []
    curr_t = 0.0
    for seg in SEGMENTS:
        dur = seg["end"] - seg["start"]
        ev = dict(seg)
        ev["dur"] = dur
        ev["t0"] = curr_t
        ev["t1"] = curr_t + dur
        ev["n_frames"] = int(round(dur * 30))
        timeline_events.append(ev)
        curr_t += dur

    total_duration = curr_t
    print(f"📊 Total Stitched Duration: {total_duration:.2f}s ({len(timeline_events)} segments)")

    with tempfile.TemporaryDirectory() as tmpdir:
        seg_files = []
        print(f"✂️  [2/4] Cutting and framing {len(SEGMENTS)} segments...")

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
                # Consistent natural camera color grading (Rule 38)
                if mode == "zoom_both":
                    vf = f"scale=1080*1.08:1920*1.08,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.42,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
                elif mode == "zoom_angel":
                    # Focus on Angel (Left)
                    vf = f"scale=1080*1.38:1920*1.38,crop=1080:1920:120:420,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
                elif mode == "zoom_arthur":
                    # Focus on Arthur (Right)
                    vf = f"scale=1080*1.42:1920*1.42,crop=1080:1920:450:380,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
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
                # Rule 42: Fast animated zoom-in transition onto Arthur's face + Black & White!
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
                # Rule 43: Comfortable portrait framing on green hoodie guy (1080x1440 over soft background)
                vf = (
                    f"split[m1][m2];"
                    f"[m1]crop=640:720:460:0,scale=1080:1920,gblur=sigma=25[bg];"
                    f"[m2]crop=640:720:460:0,scale=1080:1440[fg];"
                    f"[bg][fg]overlay=0:(H-h)/2,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS,setsar=1:1,format=yuv420p"
                )
                # Rule 46: +14 dB audio boost on meme speech
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
                    "-i", str(MEME_VIDEO),
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

        print("🎬 [3/4] Synthesizing SFX timeline & ASS Subtitles...")
        ass_path = Path(tmpdir) / "captions.ass"
        generate_ass_subtitles(timeline_events, ass_path)

        # Build SFX timeline
        sr = 48000
        sfx_track = np.zeros(int((total_duration + 2.0) * sr), dtype=np.float32)

        def load_wav(p: Path) -> np.ndarray:
            with wave.open(str(p), "rb") as w:
                return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

        wav_map = {
            "pop": load_wav(SFX_DIR / "pop.wav") * 0.65,
            "whoosh": load_wav(SFX_DIR / "whoosh.wav") * 0.55,
            "win": load_wav(SFX_DIR / "point_win.wav") * 0.70,
            "boom": load_wav(SFX_DIR / "meme_boom.wav") * 0.85,
            "riser": load_wav(SFX_DIR / "riser.wav") * 0.60,
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
            int_data = np.clip(sfx_track * 32767.0, -32768.0, 32767.0).astype(np.int16)
            wf.writeframes(int_data.tobytes())

        print("🎼 [4/4] Final Assembly: Overlays, ASS Subtitles & Chopin Nocturne Audio Mixing...")
        final_mp4 = FINAL_DIR / "tebak_kata_challenge_final.mp4"
        cover_png = FINAL_DIR / "tebak_kata_cover.png"
        draft_preview = DRAFT_DIR / "tebak_kata_preview.mp4"

        # Collect visual windows for top and head overlays
        top_windows: dict[str, list[list[float]]] = {}
        head_windows: dict[str, list[list[float]]] = {}
        freeze_window = [0.0, 0.0]
        meme_window = [0.0, 0.0]

        for ev in timeline_events:
            top_name = ev.get("top")
            if top_name:
                if top_name not in top_windows:
                    top_windows[top_name] = []
                top_windows[top_name].append([ev["t0"], ev["t1"]])

            head_name = ev.get("head")
            if head_name:
                if head_name not in head_windows:
                    head_windows[head_name] = []
                head_windows[head_name].append([ev["t0"], ev["t1"]])

            if ev["src"] == "freeze_arthur":
                freeze_window = [ev["t0"], ev["t1"]]
            if ev["src"] == "what_meme":
                meme_window = [ev["t0"], ev["t1"]]

        # Build overlay input list and filter chain
        overlay_inputs = []
        overlay_names = []

        # Hook titles
        overlay_inputs.extend(["-i", str(graphics["hook1"])])
        overlay_names.append(("hook1", top_windows.get("top_hook1", [])))
        overlay_inputs.extend(["-i", str(graphics["hook2"])])
        overlay_names.append(("hook2", top_windows.get("top_hook2", [])))

        # Top callouts
        for k in ["bisa", "rapi", "jari", "koki", "sari", "soto", "bola", "meja", "joki", "ayam", "tape", "tali", "akar", "lope"]:
            key = f"top_{k}"
            overlay_inputs.extend(["-i", str(graphics[key])])
            overlay_names.append((key, top_windows.get(key, [])))

        # Above-head callouts
        for k in ["angel_bisa", "angel_jari", "angel_sari", "angel_bola", "angel_akar",
                  "arthur_rapi", "arthur_koki", "arthur_soto", "arthur_meja", "arthur_joki", "arthur_ayam", "arthur_tape", "arthur_tali"]:
            key = f"head_{k}"
            overlay_inputs.extend(["-i", str(graphics[key])])
            overlay_names.append((key, head_windows.get(key, [])))

        # Construct filtergraph
        # Inputs:
        # [0:v] Stitched video
        # [0:a] Stitched dialogue audio
        # [1..N:v] Overlays
        # [N+1:a] sfx_timeline.wav
        # [N+2:a] Chopin Nocturne audio
        sfx_idx = len(overlay_names) + 1
        music_idx = len(overlay_names) + 2

        vf_chain = ["[0:v]"]
        curr_label = "0:v"

        for idx, (oname, intervals) in enumerate(overlay_names):
            if not intervals:
                continue
            input_idx = idx + 1
            cond_parts = []
            for t0, t1 in intervals:
                cond_parts.append(f"between(t,{t0:.3f},{t1:.3f})")
            enable_cond = "+".join(cond_parts)
            next_label = f"v_ov_{idx}"
            vf_chain.append(f"[{curr_label}][{input_idx}:v]overlay=0:0:enable='{enable_cond}'[{next_label}];")
            curr_label = next_label

        # Burn in ASS Subtitles at the very end
        vf_chain.append(f"[{curr_label}]ass={ass_path}[vout]")
        v_filter_str = "".join(vf_chain[1:])

        # Audio ducking:
        # Dialogue normalized (-14 LUFS)
        # Chopin Nocturne: default -20 dB (volume=0.10), swell on freeze (volume=0.28), dip on meme (volume=0.03)
        music_filter = (
            f"[{music_idx}:a]atrim=0:{total_duration + 0.5:.3f},asetpts=PTS-STARTPTS,"
            f"volume='if(between(t,{freeze_window[0]:.3f},{freeze_window[1]:.3f}),0.28,"
            f"if(between(t,{meme_window[0]:.3f},{meme_window[1]:.3f}),0.03,0.10))':eval=frame[music_ducked];"
            f"[0:a]volume=1.0[dia];"
            f"[{sfx_idx}:a]volume=1.0[sfx];"
            f"[dia][music_ducked][sfx]amix=inputs=3:duration=first:dropout_transition=2,"
            f"loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        )

        filter_complex = f"{v_filter_str};{music_filter}"

        print("⚡ Rendering Master Final Video...")
        run_cmd([
            "ffmpeg", "-y",
            "-i", str(stitched_mov),
            *overlay_inputs,
            "-i", str(sfx_wav_path),
            "-i", str(MUSIC_WAV),
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "320k",
            "-t", f"{total_duration:.3f}",
            "-loglevel", "error",
            str(final_mp4),
        ])

        print("📸 Generating Clean Cover Image (tebak_kata_cover.png)...")
        # Rule 38: Opening hook title from 0:00 composited over first frame
        run_cmd([
            "ffmpeg", "-y",
            "-ss", "0.000",
            "-i", str(RAW_VIDEO),
            "-i", str(graphics["hook1"]),
            "-filter_complex", "[0:v]scale=1080:1920,setsar=1:1[bg];[bg][1:v]overlay=0:0[cov]",
            "-map", "[cov]",
            "-frames:v", "1",
            "-q:v", "2",
            "-loglevel", "error",
            str(cover_png),
        ])

        print(f"✅ Master Build Complete!")
        print(f"   🎬 Final Video: {final_mp4}")
        print(f"   🖼️  Cover Image: {cover_png}")


if __name__ == "__main__":
    build_video()
