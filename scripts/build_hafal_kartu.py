#!/usr/bin/env python3
"""
Master Automated Video Editor — Challenge Hafal Kartu (v5)
- Rule 38 & 39: Simple 2-line hook title from 0:00 ('challenge' + 'HAFAL KARTU 🃏'),
  consistent natural color grading from start to end, no bottom caption during hook.
- Rule 44: Authentic Chopin Nocturne in E-flat major, Op. 9, No. 2 (audio/music/nocturne_op9_in_eb.wav).
- Rule 45: Dedicated per-project folders (`renders/final/Hafal Kartu/`, `renders/drafts/Hafal Kartu/`).
- Rule 46: Synchronized score/result top headers — NEVER show the final score header
  (`ANGEL: 8 POIN 👏` or `8 — 8 SERI 🤝`) until the final card pair is actually opened and shown!
- Rule 47: 30-second memorization phase fast-forwarded as a 4.0x timelapse with
  clock_ticking.wav SFX and NO bottom caption.
- Rule 48: Audience Participation Psychology — 100% uncut card matching (placing) and
  100% uncut card opening (results), no meme unless someone loses.
- Rule 49: One-Word-at-a-Time Dynamic Spoken Captions — show ONLY one word at a time
  synced to the exact moment it is spoken (e.g. "Babi" appears when spoken and then
  immediately disappears), never static multi-sentence blocks.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

PROJECT_ROOT = Path("/Users/arthurandersen/Documents/AI_Video_Editor_Gemini")
PROJECT_NAME = "Hafal Kartu"
RAW_VIDEO = PROJECT_ROOT / "raw" / PROJECT_NAME / "IMG_0658.MOV"

BROLL_DIR = PROJECT_ROOT / "broll" / PROJECT_NAME
DRAFTS_DIR = PROJECT_ROOT / "renders" / "drafts" / PROJECT_NAME
FINAL_DIR = PROJECT_ROOT / "renders" / "final" / PROJECT_NAME
SFX_DIR = PROJECT_ROOT / "audio" / "sfx"
MUSIC_FILE = PROJECT_ROOT / "audio" / "music" / "nocturne_op9_in_eb.wav"
TICK_FILE = SFX_DIR / "clock_ticking.wav"

FINAL_OUT = FINAL_DIR / "hafal_kartu_challenge.mp4"
COVER_OUT = FINAL_DIR / "hafal_kartu_cover.png"
PREVIEW_OUT = DRAFTS_DIR / "hafal_kartu_preview.mp4"


def run_cmd(cmd: list[str], desc: str = "") -> None:
    if desc:
        print(f"🎬 {desc}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"❌ Command failed: {' '.join(cmd)}\nSTDERR:\n{res.stderr[-2500:]}")
        raise RuntimeError(f"Command failed with exit code {res.returncode}")


def build_atempo_chain(speed: float) -> str:
    """Build valid FFmpeg atempo filter chain for any speed multiplier (e.g. 4.0 -> atempo=2.0,atempo=2.0)."""
    rem = speed
    parts = []
    while rem > 2.0:
        parts.append("atempo=2.0")
        rem /= 2.0
    while rem < 0.5:
        parts.append("atempo=0.5")
        rem /= 0.5
    parts.append(f"atempo={rem:.4f}")
    return ",".join(parts)


# ---------------------------------------------------------------------------
# 1. Generate Transparent PNG Overlays via Native macOS AppKit / Swift
# ---------------------------------------------------------------------------
def generate_overlay_assets() -> dict[str, Path]:
    BROLL_DIR.mkdir(parents=True, exist_ok=True)
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DIR.mkdir(parents=True, exist_ok=True)

    swift_code = f"""
import Cocoa

let width = 1080
let height = 1920
let outDir = "{BROLL_DIR.as_posix()}"

func createCanvas() -> (NSBitmapImageRep, NSGraphicsContext) {{
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

let fontSub = NSFont(name: "HelveticaNeue-Bold", size: 68) ?? NSFont.systemFont(ofSize: 68, weight: .bold)
let fontMain = NSFont(name: "Arial-Black", size: 96) ?? NSFont.systemFont(ofSize: 96, weight: .black)
let fontWord = NSFont(name: "Arial-Black", size: 64) ?? NSFont.systemFont(ofSize: 64, weight: .black)

// Draw 'challenge' (Black fill, pure crisp White border, outer soft shadow)
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
        .paragraphStyle: pCenter
    ]
    NSAttributedString(string: text, attributes: p2).draw(in: rect)
}}

// Draw 'HAFAL KARTU 🃏' / Word Callouts (Full-weight White fill, thin dark edge + drop shadow)
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

// 1. Hook Title Overlay (Upper window blinds area, from 0:00)
let (repHook, _) = createCanvas()
drawBlackWithWhiteOutline("challenge", rect: NSRect(x: 40, y: 1690, width: 1000, height: 95), font: fontSub)
drawWhiteBeanBoozleStyle("HAFAL KARTU 🃏", rect: NSRect(x: 30, y: 1570, width: 1020, height: 120), font: fontMain)
savePNG(repHook, "hook_hafal_kartu.png")

// 2. Top Phase & Result Callouts (y=1640, pure white + shadow, clean words without +1 or !)
struct Callout {{
    let filename: String
    let text: String
}}

let callouts: [Callout] = [
    Callout(filename: "card_suit.png", text: "SUIT DULU ✌️"),
    Callout(filename: "card_timer_angel.png", text: "30 DETIK MENGHAFAL ⏱️"),
    Callout(filename: "card_gak_ingat.png", text: "GAK INGAT 😂"),
    Callout(filename: "card_matching_angel.png", text: "SUSUN KARTU ANGEL 🃏"),
    Callout(filename: "card_open_angel.png", text: "BUKA KARTU ANGEL 🔍"),
    Callout(filename: "card_angel_score.png", text: "ANGEL: 8 POIN 👏"),
    Callout(filename: "card_timer_arthur.png", text: "GILIRAN ARTHUR ⏱️"),
    Callout(filename: "card_matching_arthur.png", text: "SUSUN KARTU ARTHUR 🃏"),
    Callout(filename: "card_open_arthur.png", text: "BUKA KARTU ARTHUR 🔍"),
    Callout(filename: "card_seri.png", text: "8 — 8 SERI 🤝"),
    Callout(filename: "card_fair_game.png", text: "FAIR GAME 🏆")
]

for c in callouts {{
    let (rep, _) = createCanvas()
    drawWhiteBeanBoozleStyle(c.text, rect: NSRect(x: 20, y: 1640, width: 1040, height: 110), font: fontWord)
    savePNG(rep, c.filename)
}}

let (repEmpty, _) = createCanvas()
savePNG(repEmpty, "empty.png")
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
        "hook": BROLL_DIR / "hook_hafal_kartu.png",
        "card_suit": BROLL_DIR / "card_suit.png",
        "card_timer_angel": BROLL_DIR / "card_timer_angel.png",
        "card_gak_ingat": BROLL_DIR / "card_gak_ingat.png",
        "card_matching_angel": BROLL_DIR / "card_matching_angel.png",
        "card_open_angel": BROLL_DIR / "card_open_angel.png",
        "card_angel_score": BROLL_DIR / "card_angel_score.png",
        "card_timer_arthur": BROLL_DIR / "card_timer_arthur.png",
        "card_matching_arthur": BROLL_DIR / "card_matching_arthur.png",
        "card_open_arthur": BROLL_DIR / "card_open_arthur.png",
        "card_seri": BROLL_DIR / "card_seri.png",
        "card_fair_game": BROLL_DIR / "card_fair_game.png",
        "empty": BROLL_DIR / "empty.png",
    }


# ---------------------------------------------------------------------------
# 2. Master Edit Decision List (EDL)
#    - 4.0x Timelapse on 30s Memorization (with clock ticking & NO captions)
#    - 100% Continuous Card Matching (Placing) for Audience Participation
#    - 100% Continuous Card Opening (Results) for Audience Participation
#    - Exact Final Score Header Timing:
#      * `ANGEL: 8 POIN 👏` ONLY appears at 383.00 -> 386.80 when the last card (Barn) is shown!
#      * `8 — 8 SERI 🤝` ONLY appears at 594.20 -> 597.50 when the last card (Haystack) is shown!
# ---------------------------------------------------------------------------
SEGMENTS = [
    # 1. Opening Hook & Title (1.0x) — No bottom caption
    {
        "id": 1,
        "start": 0.00,
        "end": 4.50,
        "speed": 1.0,
        "mode": "normal",
        "card": "hook",
        "no_caption": True,
        "sfx": "whoosh",
    },
    # 2. Suit / Gambreng (1.25x)
    {
        "id": 2,
        "start": 6.30,
        "end": 10.80,
        "speed": 1.25,
        "mode": "zoom_both",
        "card": "card_suit",
        "sfx": "pop",
    },
    # 3. Arthur Starts Angel's 30s Timer (1.25x)
    {
        "id": 3,
        "start": 142.70,
        "end": 146.50,
        "speed": 1.25,
        "mode": "zoom_both",
        "card": "card_timer_angel",
        "sfx": "pop",
    },
    # 4. Angel's 30-Second Memorization (4.0x FAST-FORWARD TIMELAPSE + CLOCK TICKING + NO CAPTION)
    {
        "id": 4,
        "start": 146.50,
        "end": 173.80,
        "speed": 4.0,
        "ticking": True,
        "mode": "normal",
        "card": "card_timer_angel",
        "no_caption": True,
        "sfx": "",
    },
    # 5. Timer Ends: "3, 2, 1, teng! Tutup mata!" (1.25x)
    {
        "id": 5,
        "start": 173.80,
        "end": 176.00,
        "speed": 1.25,
        "mode": "zoom_both",
        "card": "card_timer_angel",
        "sfx": "pop",
    },
    # 6. Flipping Cards Face Down & Angel "Ah nggak ingat, tau!" (1.25x)
    {
        "id": 6,
        "start": 195.80,
        "end": 199.20,
        "speed": 1.25,
        "mode": "zoom_angel",
        "card": "card_gak_ingat",
        "sfx": "pop",
    },
    # 7. Angel Matching Part A — First Cards Placed (204.90 -> 238.60, Continuous!)
    {
        "id": 7,
        "start": 204.90,
        "end": 238.60,
        "speed": 1.85,
        "mode": "normal",
        "card": "card_matching_angel",
        "sfx": "pop",
    },
    # 8. Angel Matching Part B — Middle Grid Cards Placed (238.60 -> 283.60, Continuous!)
    {
        "id": 8,
        "start": 238.60,
        "end": 283.60,
        "speed": 2.6,
        "mode": "normal",
        "card": "card_matching_angel",
        "sfx": "",
    },
    # 9. Angel Matching Part C — Final Cards Placed (283.60 -> 306.00, Continuous!)
    {
        "id": 9,
        "start": 283.60,
        "end": 306.00,
        "speed": 1.85,
        "mode": "normal",
        "card": "card_matching_angel",
        "sfx": "pop",
    },
    # 10. Angel Opening Cards Part A — Domba (Match), Kuda (Match), Ayam (Miss) (311.50 -> 325.80)
    {
        "id": 10,
        "start": 311.50,
        "end": 325.80,
        "speed": 1.75,
        "mode": "zoom_both",
        "card": "card_open_angel",
        "sfx": "win",
    },
    # 11. Angel Opening Cards Part B — Traktor (Kebalik), Ayam (Match), Domba & Kuda (Miss) (325.80 -> 345.50)
    {
        "id": 11,
        "start": 325.80,
        "end": 345.50,
        "speed": 1.75,
        "mode": "zoom_both",
        "card": "card_open_angel",
        "sfx": "pop",
    },
    # 12. Angel Opening Cards Part C — Sapi, Babi, Telur (Match), Sapi (Match), Kambing (Miss) (345.50 -> 367.50)
    {
        "id": 12,
        "start": 345.50,
        "end": 367.50,
        "speed": 1.75,
        "mode": "zoom_both",
        "card": "card_open_angel",
        "sfx": "win",
    },
    # 13. Angel Opening Cards Part D1 — Traktor & Kelinci Opened, Reaching for Last Card (367.50 -> 383.00)
    #     Keep header as `BUKA KARTU ANGEL 🔍` until the last pair is actually revealed at 383.00!
    {
        "id": 13,
        "start": 367.50,
        "end": 383.00,
        "speed": 1.65,
        "mode": "zoom_both",
        "card": "card_open_angel",
        "sfx": "win",
    },
    # 14. Angel Opening Cards Part D2 — Final Barn Pair Shown -> ANGEL: 8 POIN 👏 (383.00 -> 386.80)
    {
        "id": 14,
        "start": 383.00,
        "end": 386.80,
        "speed": 1.40,
        "mode": "zoom_both",
        "card": "card_angel_score",
        "sfx": "win",
    },
    # 15. Arthur's Turn Setup (1.25x)
    {
        "id": 15,
        "start": 399.00,
        "end": 404.50,
        "speed": 1.25,
        "mode": "zoom_angel",
        "card": "card_timer_arthur",
        "sfx": "pop",
    },
    # 16. Arthur's 30-Second Memorization (4.0x FAST-FORWARD TIMELAPSE + CLOCK TICKING + NO CAPTION)
    {
        "id": 16,
        "start": 404.50,
        "end": 429.80,
        "speed": 4.0,
        "ticking": True,
        "mode": "normal",
        "card": "card_timer_arthur",
        "no_caption": True,
        "sfx": "",
    },
    # 17. Arthur Timer Ends: "3, 2, 1, tutup mata!" (1.25x)
    {
        "id": 17,
        "start": 429.80,
        "end": 432.30,
        "speed": 1.25,
        "mode": "zoom_both",
        "card": "card_timer_arthur",
        "sfx": "pop",
    },
    # 18. Arthur Reaction "Anjir gua ngafal apa lagi?!" (1.25x)
    {
        "id": 18,
        "start": 448.20,
        "end": 451.80,
        "speed": 1.25,
        "mode": "zoom_both",
        "card": "card_gak_ingat",
        "sfx": "pop",
    },
    # 19. Arthur Matching Part A — Starting From First Card Placed (462.50 -> 504.50, Continuous!)
    {
        "id": 19,
        "start": 462.50,
        "end": 504.50,
        "speed": 1.9,
        "mode": "normal",
        "card": "card_matching_arthur",
        "sfx": "pop",
    },
    # 20. Arthur Matching Part B — Final Cards & "Kita buka!" (504.50 -> 523.60, Continuous!)
    {
        "id": 20,
        "start": 504.50,
        "end": 523.60,
        "speed": 1.9,
        "mode": "normal",
        "card": "card_matching_arthur",
        "sfx": "pop",
    },
    # 21. Arthur Opening Cards Part A — Traktor (Match), Alpaca (Miss), Ayam Bertelur (Match) (523.60 -> 543.50)
    {
        "id": 21,
        "start": 523.60,
        "end": 543.50,
        "speed": 1.75,
        "mode": "zoom_both",
        "card": "card_open_arthur",
        "sfx": "win",
    },
    # 22. Arthur Opening Cards Part B — Traktor Hijau (Match), Babi (Tebak Benar!), Barn & Kelinci (Miss) (543.50 -> 566.00)
    {
        "id": 22,
        "start": 543.50,
        "end": 566.00,
        "speed": 1.75,
        "mode": "zoom_both",
        "card": "card_open_arthur",
        "sfx": "win",
    },
    # 23. Arthur Opening Cards Part C — Sapi (Match), Kuda (Match), Ayam (Miss), Kambing (Match) (566.00 -> 583.50)
    {
        "id": 23,
        "start": 566.00,
        "end": 583.50,
        "speed": 1.75,
        "mode": "zoom_both",
        "card": "card_open_arthur",
        "sfx": "win",
    },
    # 24. Arthur Opening Cards Part D1 — Counting 1..7 & Reaching for Final Card (583.50 -> 594.20)
    #     Keep header as `BUKA KARTU ARTHUR 🔍` until the final pair is revealed at 594.20!
    {
        "id": 24,
        "start": 583.50,
        "end": 594.20,
        "speed": 1.40,
        "mode": "zoom_both",
        "card": "card_open_arthur",
        "sfx": "pop",
    },
    # 25. Arthur Opening Cards Part D2 — Final Haystack Pair Shown -> 8 — 8 SERI 🤝 (594.20 -> 597.50)
    {
        "id": 25,
        "start": 594.20,
        "end": 597.50,
        "speed": 1.20,
        "mode": "zoom_both",
        "card": "card_seri",
        "sfx": "win",
    },
]


# ---------------------------------------------------------------------------
# 3. Exact Word-by-Word Spoken Timeline (One Word at a Time, Immediately Disappears)
#    Derived from Whisper word-level timestamps (`IMG_0658_16k.json`) with
#    all Indonesian card names & spoken words verified for 100% accuracy.
# ---------------------------------------------------------------------------
RAW_SPOKEN_WORDS = [
    # Seg 2: Suit (6.30 -> 10.80)
    (7.30, 7.85, "Gambreng!"),
    (8.60, 9.10, "Oke!"),
    (10.30, 10.55, "You"),
    (10.55, 10.78, "first?"),

    # Seg 3: Arthur starts Angel's 30s timer (142.70 -> 146.50)
    (142.74, 143.16, "Untuk"),
    (143.16, 143.55, "mulai"),
    (143.80, 144.10, "3"),
    (144.28, 144.60, "2"),
    (144.76, 145.05, "1"),
    (145.10, 145.55, "mulai!"),
    (145.62, 145.95, "30"),
    (145.96, 146.45, "seconds!"),

    # Seg 5: Timer ends (173.80 -> 176.00)
    (174.10, 174.45, "Satu!"),
    (174.70, 175.10, "Teng!"),
    (175.35, 175.60, "Tutup"),
    (175.60, 175.95, "mata!"),

    # Seg 6: Angel "Ah nggak ingat, tau!" (195.80 -> 199.20)
    (196.55, 196.95, "Ah"),
    (197.00, 197.35, "nggak"),
    (197.35, 197.80, "ingat"),
    (197.85, 198.35, "tau!"),

    # Seg 7: Angel Matching Part A (204.90 -> 238.60)
    (204.98, 205.80, "Oke"),
    (206.10, 206.45, "Angel"),
    (206.45, 207.00, "memiliki"),
    (207.00, 208.50, "16"),
    (208.50, 209.38, "kartu"),
    (209.60, 210.05, "Kamu"),
    (210.05, 210.50, "tunjukin"),
    (210.50, 211.20, "penontonnya"),
    (211.48, 211.85, "mana"),
    (212.30, 213.50, "kartu"),
    (213.50, 214.05, "tersebut"),
    (214.05, 215.10, "berada"),
    (215.64, 216.08, "Mulai"),
    (216.08, 216.32, "dari"),
    (216.32, 216.68, "barn"),
    (216.68, 217.25, "kecil"),
    (217.98, 218.90, "Yakin"),
    (218.90, 219.50, "di"),
    (219.50, 219.95, "sana?"),
    (220.05, 220.40, "Coba"),
    (220.40, 220.95, "tunjukkan"),
    (221.98, 222.90, "Kambingnya"),
    (223.20, 223.50, "apa"),
    (223.50, 224.15, "kudanya?"),
    (225.10, 226.40, "Sapinya"),
    (226.80, 227.15, "yakin"),
    (227.15, 227.65, "sini?"),
    (228.65, 229.30, "Traktor"),
    (229.30, 230.00, "biru"),
    (231.30, 231.95, "Angel"),
    (231.95, 232.60, "mulai"),
    (235.15, 235.80, "Babinya"),
    (235.80, 236.30, "kali"),
    (236.80, 237.25, "Anda"),
    (237.25, 237.85, "lihat"),
    (237.85, 238.55, "satu-satu"),

    # Seg 8: Angel Matching Part B (238.60 -> 283.60) — Only spoken words, no noise
    (242.00, 243.10, "Traktor"),
    (246.00, 247.30, "Kelinci"),
    (253.80, 255.00, "Babi"),
    (255.10, 256.30, "Telur"),
    (256.40, 257.50, "Yakin?"),
    (259.60, 261.00, "Domba"),

    # Seg 9: Angel Matching Part C (283.60 -> 306.00)
    (284.10, 284.50, "Kayaknya"),
    (284.50, 285.10, "sini"),
    (286.60, 287.00, "Habis"),
    (287.00, 287.45, "itu"),
    (287.45, 287.90, "ayamnya"),
    (287.90, 288.35, "mana?"),
    (288.35, 288.75, "Gak"),
    (288.75, 289.10, "ingat"),
    (289.10, 289.55, "ayam"),
    (293.40, 293.85, "Aduh"),
    (293.85, 294.55, "pikir"),
    (294.55, 295.15, "baik-baik"),
    (295.44, 295.95, "Ayam"),
    (295.95, 296.40, "apa"),
    (296.40, 296.80, "ya?"),
    (296.84, 297.35, "Kuda"),
    (297.52, 297.90, "Kayak"),
    (297.90, 298.35, "sini"),
    (298.40, 298.95, "Ayam"),
    (302.20, 302.45, "Ada"),
    (302.45, 302.75, "dua"),
    (302.75, 303.10, "lagi"),
    (303.18, 303.42, "Ini"),
    (303.42, 303.65, "sama"),
    (303.65, 303.95, "ini"),
    (305.26, 305.95, "Oke!"),

    # Seg 10: Angel Opening Part A (311.50 -> 325.80)
    (311.56, 312.20, "Oke"),
    (312.25, 312.50, "mari"),
    (312.50, 312.72, "kita"),
    (312.72, 313.10, "lihat"),
    (313.30, 313.90, "Domba"),
    (313.98, 314.55, "dapet"),
    (314.55, 315.18, "domba!"),
    (315.28, 315.65, "Satu"),
    (315.65, 316.00, "poin"),
    (316.00, 316.55, "anda!"),
    (317.35, 318.05, "Dua"),
    (318.35, 319.00, "ketemu"),
    (319.00, 319.60, "juga!"),
    (320.60, 321.25, "Ternyata"),
    (321.25, 321.85, "salah!"),
    (322.85, 323.50, "Ayamnya"),
    (323.50, 323.95, "sama"),
    (323.95, 324.55, "baby"),
    (324.55, 324.90, "ayam"),
    (324.90, 325.20, "gak"),
    (325.20, 325.65, "sama!"),

    # Seg 11: Angel Opening Part B (325.80 -> 345.50)
    (326.20, 326.60, "Apakah"),
    (326.60, 327.15, "traktor"),
    (327.15, 327.55, "sama"),
    (327.55, 328.05, "traktor?"),
    (328.18, 328.74, "Sayangnya"),
    (328.74, 329.20, "traktor"),
    (329.20, 329.75, "kebalik!"),
    (331.70, 332.35, "Guys"),
    (332.70, 333.50, "traktor"),
    (333.60, 334.10, "benar"),
    (334.10, 334.65, "traktor"),
    (334.74, 335.30, "Ini"),
    (335.30, 336.90, "ayamnya"),
    (337.55, 338.35, "Ayamnya"),
    (338.35, 339.30, "sama!"),
    (339.55, 340.35, "Sama!"),
    (341.35, 341.75, "Sayang"),
    (341.75, 342.20, "sekali"),
    (342.48, 343.10, "Domba"),
    (343.10, 343.70, "sama"),
    (344.20, 344.65, "kuda"),
    (344.65, 345.00, "gak"),
    (345.00, 345.40, "sama!"),

    # Seg 12: Angel Opening Part C (345.50 -> 367.50)
    (346.14, 346.85, "Apakah"),
    (346.85, 347.50, "sapi"),
    (347.62, 348.15, "sama"),
    (348.15, 348.65, "kuda?"),
    (348.75, 349.05, "Gak"),
    (349.05, 349.55, "sama!"),
    (350.50, 351.00, "Babinya"),
    (351.00, 351.50, "artinya"),
    (352.15, 352.95, "Sapi!"),
    (353.95, 354.45, "Apakah"),
    (354.45, 355.05, "telur?"),
    (355.18, 355.68, "Anda"),
    (355.68, 356.10, "dapet"),
    (356.10, 356.80, "poin!"),
    (357.54, 358.00, "Apakah"),
    (358.00, 358.35, "PD"),
    (358.35, 358.75, "ini?"),
    (359.35, 359.75, "Iya"),
    (360.35, 361.05, "Dapet"),
    (361.05, 361.50, "poin"),
    (361.50, 362.15, "juga!"),
    (362.48, 363.10, "Kambing"),
    (363.10, 363.65, "benar?"),
    (363.80, 364.30, "Kambing"),
    (364.30, 364.90, "sama"),
    (364.90, 365.50, "ayam"),
    (365.50, 366.30, "beda!"),

    # Seg 13: Angel Opening Part D1 (367.50 -> 383.00)
    (367.60, 367.85, "Ini"),
    (367.85, 368.25, "sama?"),
    (368.64, 369.35, "Anjay"),
    (369.65, 370.25, "dapet"),
    (370.25, 370.80, "juga!"),
    (372.00, 372.55, "Kelinci"),
    (372.60, 373.35, "kelinci!"),
    (373.70, 374.45, "Dapet"),
    (374.45, 374.85, "juga"),
    (374.85, 375.55, "kelincinya!"),
    (376.10, 376.85, "PD"),
    (376.85, 377.40, "ini?"),
    (377.90, 378.35, "Iya"),
    (378.94, 379.85, "Artinya"),
    (379.85, 380.30, "terakhir"),
    (380.30, 380.80, "benar"),
    (380.80, 381.45, "juga!"),

    # Seg 14: Angel Opening Part D2 — 8 Poin Reveal (383.00 -> 386.80)
    (383.15, 384.20, "Delapan!"),
    (384.85, 385.40, "Delapan"),
    (385.40, 386.35, "poin!"),

    # Seg 15: Arthur's Turn Setup (399.00 -> 404.50)
    (399.02, 399.30, "Oke"),
    (399.30, 399.60, "guys"),
    (399.68, 400.00, "sekarang"),
    (400.00, 400.30, "giliran"),
    (400.30, 400.65, "Arthur!"),
    (400.74, 401.00, "Ini"),
    (401.00, 401.35, "30"),
    (401.35, 401.92, "seconds"),
    (401.92, 402.58, "mulai"),
    (402.58, 403.30, "dari"),
    (403.95, 404.48, "sekarang!"),

    # Seg 17: Arthur Timer Ends (429.80 -> 432.30)
    (429.95, 430.25, "Dua"),
    (430.35, 430.70, "satu"),
    (430.80, 431.35, "teng!"),
    (431.75, 432.02, "Tutup"),
    (432.02, 432.28, "mata!"),

    # Seg 18: Arthur Reaction (448.20 -> 451.80)
    (448.35, 449.05, "Anjir"),
    (449.10, 449.40, "gua"),
    (449.40, 449.85, "ngafal"),
    (449.85, 450.15, "apa"),
    (450.15, 450.65, "lagi?!"),

    # Seg 19: Arthur Matching Part A (462.50 -> 504.50) — One word at a time!
    (463.20, 463.80, "Mulai!"),
    (467.10, 467.80, "Kelinci"),
    (467.88, 468.25, "Ayo"),
    (468.25, 468.85, "kelinci"),
    (469.40, 470.35, "Ayam"),
    (472.25, 473.60, "Traktor"),
    (474.28, 475.05, "Traktor"),
    (477.30, 478.10, "Sapi"),
    (479.20, 480.00, "Kuda"),
    (480.85, 481.65, "Telur"),
    (484.40, 485.30, "Babi"),
    (487.24, 487.75, "Anjir"),
    (487.75, 488.00, "ada"),
    (488.00, 488.30, "ayam"),
    (488.30, 488.80, "beda?"),
    (489.95, 490.40, "Ada"),
    (490.40, 490.98, "ayam"),
    (491.40, 492.10, "Ayam"),
    (492.15, 492.95, "ayam"),
    (496.40, 497.80, "Domba"),
    (499.75, 500.80, "Anjir"),
    (501.10, 502.00, "Haystack"),

    # Seg 20: Arthur Matching Part B (504.50 -> 523.60)
    (505.70, 506.15, "Apa"),
    (506.15, 506.55, "ya?"),
    (507.45, 507.80, "Gua"),
    (507.80, 508.25, "atas"),
    (508.80, 509.60, "Barn"),
    (513.40, 514.50, "Apa"),
    (514.50, 515.80, "ya"),
    (515.80, 516.70, "tadi"),
    (516.70, 517.25, "ya?"),
    (518.45, 519.00, "Apa"),
    (519.00, 519.50, "tadi?"),
    (520.50, 521.35, "Oke!"),
    (521.80, 522.25, "Berapa"),
    (522.25, 522.80, "PD?"),
    (523.15, 523.38, "Kita"),
    (523.38, 523.60, "buka!"),

    # Seg 21: Arthur Opening Part A (523.60 -> 543.50)
    (524.04, 524.50, "Gua"),
    (524.50, 525.05, "PD"),
    (525.25, 525.75, "dikit"),
    (525.98, 526.65, "Tada!"),
    (526.65, 527.15, "Traktor"),
    (527.15, 527.90, "benar!"),
    (528.24, 528.95, "Satu"),
    (528.95, 529.40, "at-least"),
    (530.05, 530.90, "Benar!"),
    (532.15, 532.65, "Benar"),
    (532.65, 533.20, "anjir!"),
    (535.08, 535.75, "Eh"),
    (535.75, 536.35, "salah!"),
    (536.95, 537.45, "Gak"),
    (537.45, 538.15, "bisa!"),
    (539.75, 540.40, "Tada!"),
    (540.80, 541.20, "Ayam"),
    (541.20, 541.75, "bertelur"),
    (541.75, 542.10, "guys!"),
    (542.44, 543.15, "Sebelahnya"),
    (543.15, 543.50, "artinya"),

    # Seg 22: Arthur Opening Part B (543.50 -> 566.00)
    (543.94, 544.50, "Telurnya"),
    (544.50, 545.10, "diinjak"),
    (545.10, 545.80, "traktor!"),
    (545.80, 546.65, "Traktor!"),
    (548.35, 549.00, "Hei"),
    (549.00, 549.60, "benar!"),
    (550.25, 551.10, "Tada!"),
    (552.10, 552.70, "Tiga!"),
    (552.90, 553.30, "Anjay"),
    (553.30, 553.55, "gua"),
    (553.55, 553.85, "tebak"),
    (553.85, 554.25, "benar!"),
    (555.40, 556.10, "Babi!"),
    (556.75, 557.40, "Di"),
    (557.40, 558.20, "kandangnya"),
    (558.48, 559.05, "Babi"),
    (559.05, 559.65, "bukan?"),
    (559.70, 560.35, "Ternyata"),
    (560.35, 561.40, "kelinci!"),
    (562.34, 562.80, "Tadi"),
    (562.80, 563.25, "kelinci"),
    (563.25, 563.50, "taruh"),
    (563.50, 563.75, "mana?"),
    (563.82, 564.45, "Ternyata"),
    (564.45, 565.00, "babi!"),
    (565.45, 565.95, "Anjir!"),

    # Seg 23: Arthur Opening Part C (566.00 -> 583.50)
    (566.08, 566.85, "Itu"),
    (566.85, 567.55, "benar"),
    (567.55, 568.05, "pasti!"),
    (569.10, 569.75, "Sapi!"),
    (570.55, 570.86, "Kuda"),
    (570.86, 571.10, "pasti"),
    (571.10, 571.45, "benar!"),
    (572.45, 573.15, "Pasti!"),
    (573.65, 573.95, "Gua"),
    (573.95, 574.20, "lupa"),
    (574.20, 574.55, "ayamnya"),
    (574.55, 574.90, "bawah"),
    (574.94, 575.35, "atau"),
    (575.35, 575.86, "atas"),
    (576.30, 576.70, "Gua"),
    (576.70, 577.00, "ingat"),
    (577.00, 577.40, "ayam"),
    (578.10, 578.75, "Kebalik!"),
    (579.80, 580.45, "Lima!"),
    (581.55, 582.35, "Benar!"),

    # Seg 24: Arthur Opening Part D1 — Counting 1..7 Before Final Card Opened (583.50 -> 594.20)
    (583.74, 584.40, "Satu"),
    (584.55, 585.15, "dua"),
    (585.50, 586.05, "tiga"),
    (586.25, 586.75, "empat"),
    (586.85, 587.30, "lima"),
    (587.34, 587.90, "enam"),
    (588.34, 588.78, "Fix"),
    (588.78, 589.30, "benar!"),
    (589.75, 590.50, "Tujuh!"),
    (591.10, 591.45, "Benar"),
    (591.45, 591.70, "gak"),
    (591.70, 592.20, "terakhir?"),

    # Seg 25: Arthur Opening Part D2 — Final Card Shown -> 8 — 8 SERI! (594.20 -> 597.50)
    (594.22, 594.85, "Benar!"),
    (595.25, 595.95, "Delapan"),
    (595.95, 596.55, "seri!"),
    (596.65, 597.05, "Fair"),
    (597.05, 597.48, "game!"),
]


# ---------------------------------------------------------------------------
# 4. Generate ASS Subtitles (One Word at a Time!)
# ---------------------------------------------------------------------------
def generate_ass_subtitles(ass_file: Path) -> list[dict]:
    timeline_events = []
    current_time = 0.0

    for seg in SEGMENTS:
        base_dur = seg["end"] - seg["start"]
        speed = seg.get("speed", 1.0)
        scaled_dur = base_dur / speed

        ev = {
            "id": seg["id"],
            "t_start": current_time,
            "t_end": current_time + scaled_dur,
            "dur": scaled_dur,
            "base_dur": base_dur,
            "speed": speed,
            "ticking": seg.get("ticking", False),
            "no_caption": seg.get("no_caption", False),
            "raw_start": seg["start"],
            "raw_end": seg["end"],
            "mode": seg["mode"],
            "card": seg["card"],
            "sfx": seg["sfx"],
        }
        timeline_events.append(ev)
        current_time += scaled_dur

    def fmt_ass_time(seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        cs = int(round((seconds - int(seconds)) * 100))
        if cs >= 100:
            s += 1
            cs = 0
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

    # Slightly larger, punchy single-word font (64pt Arial Black) at bottom
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: BottomWord,Arial Black,64,&H00FFFFFF,&H000000FF,&H00000000,&HB4000000,-1,0,0,0,100,100,0,0,1,3.2,4.2,2,50,50,155,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [ass_header.strip()]

    # Map each raw spoken word into the edited timeline (one word at a time!)
    mapped_words = []
    for ws, we, word_text in RAW_SPOKEN_WORDS:
        for ev in timeline_events:
            if ev["no_caption"]:
                continue
            r0, r1 = ev["raw_start"], ev["raw_end"]
            # Check if word falls within this segment
            if ws >= r0 - 0.05 and ws < r1 - 0.02:
                w_clamped_start = max(ws, r0)
                w_clamped_end = min(we, r1)
                t0 = ev["t_start"] + (w_clamped_start - r0) / ev["speed"]
                t1 = ev["t_start"] + (w_clamped_end - r0) / ev["speed"]
                # Ensure minimum readable flash (at least 0.16s, max 0.65s so it disappears quickly)
                if t1 - t0 < 0.16:
                    t1 = min(ev["t_end"], t0 + 0.22)
                elif t1 - t0 > 0.65:
                    t1 = t0 + 0.65
                mapped_words.append((t0, t1, word_text))
                break

    # Prevent any overlap between consecutive words so strictly ONE word is shown at a time
    mapped_words.sort(key=lambda x: x[0])
    cleaned_words = []
    for i, (t0, t1, txt) in enumerate(mapped_words):
        if i + 1 < len(mapped_words):
            next_t0 = mapped_words[i + 1][0]
            if t1 > next_t0 - 0.02:
                t1 = max(t0 + 0.08, next_t0 - 0.02)
        if t1 > t0 + 0.04:
            cleaned_words.append((t0, t1, txt))

    for t0, t1, txt in cleaned_words:
        start_str = fmt_ass_time(t0)
        end_str = fmt_ass_time(t1)
        lines.append(f"Dialogue: 0,{start_str},{end_str},BottomWord,,0,0,0,,{{\\fad(25,25)}}{txt}")

    ass_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return timeline_events


# ---------------------------------------------------------------------------
# 5. Render Individual Segments & Concatenate with Full Audio Design
# ---------------------------------------------------------------------------
def build_video() -> None:
    print("🎨 [1/5] Rendering High-Contrast Title & Callout Overlays via Swift...")
    assets = generate_overlay_assets()

    ass_file = DRAFTS_DIR / "captions_hafal_kartu.ass"
    timeline = generate_ass_subtitles(ass_file)
    total_dur = timeline[-1]["t_end"]
    print(f"⏱️  Total edited timeline duration: {total_dur:.2f}s ({len(timeline)} segments) [~{total_dur/60:.2f} min]")

    seg_dir = Path(tempfile.mkdtemp(prefix="hafal_kartu_segs_"))
    seg_files: list[Path] = []

    print("✂️  [2/5] Slicing 4x memorization timelapses, full card matching, and full card opening...")
    for ev in timeline:
        seg_id = ev["id"]
        seg_out = seg_dir / f"seg_{seg_id:02d}.mp4"
        seg_files.append(seg_out)

        card_png = assets.get(ev["card"], assets["empty"])
        mode = ev["mode"]
        speed = ev["speed"]
        raw_dur = ev["base_dur"]
        out_dur = ev["dur"]

        # Base crop / framing per mode
        if mode == "normal":
            base_v = "[0:v]scale=1080:1920,setsar=1[bg]"
        elif mode == "zoom_both":
            base_v = "[0:v]scale=1188:2112,crop=1080:1920:54:85,setsar=1[bg]"
        elif mode == "zoom_angel":
            base_v = "[0:v]scale=1380:2453,crop=1080:1920:45:190,setsar=1[bg]"
        elif mode == "zoom_arthur":
            base_v = "[0:v]scale=1380:2453,crop=1080:1920:255:190,setsar=1[bg]"
        else:
            base_v = "[0:v]scale=1080:1920,setsar=1[bg]"

        vf_parts = [
            base_v,
            f"[1:v] scale=1080:1920 [card]",
            f"[bg][card] overlay=0:0 [v_over]",
        ]

        if abs(speed - 1.0) > 0.01:
            vf_parts.append(f"[v_over] setpts=PTS/{speed:.4f},fps=60,format=yuv420p [vout]")
            af_str = f"{build_atempo_chain(speed)},aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo"
        else:
            vf_parts.append(f"[v_over] fps=60,format=yuv420p [vout]")
            af_str = "aresample=48000,aformat=sample_rates=48000:channel_layouts=stereo"

        vf_str = ";".join(vf_parts)

        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{ev['raw_start']:.3f}",
            "-t", f"{raw_dur:.3f}",
            "-i", str(RAW_VIDEO),
            "-loop", "1", "-t", f"{raw_dur:.3f}", "-i", str(card_png),
            "-filter_complex", vf_str,
            "-map", "[vout]",
            "-map", "0:a",
            "-af", af_str,
            "-t", f"{out_dur:.3f}",
            "-r", "60",
            "-c:v", "h264_videotoolbox", "-b:v", "18M",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
            str(seg_out),
        ]
        run_cmd(cmd)

    # Concatenate all segments
    concat_list = seg_dir / "concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{f.as_posix()}'" for f in seg_files) + "\n",
        encoding="utf-8",
    )
    concat_mp4 = seg_dir / "concat_raw.mp4"
    run_cmd(
        [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            str(concat_mp4),
        ],
        desc="[3/5] Concatenating edited video segments",
    )

    # -----------------------------------------------------------------------
    # 6. Build Master Audio Mix (Voice + Ducked Chopin Nocturne + Clock Ticking + SFX)
    # -----------------------------------------------------------------------
    print("🎵 [4/5] Mixing Sound Design (Ducked Chopin Nocturne in E-flat Major + SFX + Word-by-Word Captions)...")

    sfx_map = {
        "pop": (SFX_DIR / "pop.wav", 0.30),
        "whoosh": (SFX_DIR / "whoosh.wav", 0.36),
        "win": (SFX_DIR / "ding.wav", 0.36),
        " riser": (SFX_DIR / "riser.wav", 0.35),
        "boing": (SFX_DIR / "boing.wav", 0.40),
    }

    #Inputs:
    # 0: concat_mp4
    # 1: MUSIC_FILE (Chopin Nocturne Op. 9 No. 2 in E-flat Major)
    # 2: TICK_FILE (Clock Ticking for Angel's 30s Memorization Timelapse)
    # 3: TICK_FILE (Clock Ticking for Arthur's 30s Memorization Timelapse)
    angel_mem_ev = next(ev for ev in timeline if ev["id"] == 4)
    arthur_mem_ev = next(ev for ev in timeline if ev["id"] == 16)

    inputs = [
        "-i", str(concat_mp4),
        "-stream_loop", "-1", "-i", str(MUSIC_FILE),
        "-i", str(TICK_FILE),
        "-i", str(TICK_FILE),
    ]
    filter_chains = []

    # Main dialogue audio
    filter_chains.append(
        "[0:a]highpass=f=80,acompressor=threshold=-18dB:ratio=2.5:attack=10:release=120:makeup=2.5[voice]"
    )

    # Background music: Chopin Nocturne Op. 9 No. 2 in E-flat major
    fade_out_st = max(0.0, total_dur - 2.5)
    filter_chains.append(
        f"[1:a]atrim=0:{total_dur:.3f},asetpts=PTS-STARTPTS,"
        f"volume='0.14':eval=frame,"
        f"afade=t=in:st=0:d=1.0,afade=t=out:st={fade_out_st:.3f}:d=2.5[music]"
    )

    # Clock Ticking SFX for Angel's 4x Memorization Timelapse (Seg 4) and Arthur's 4x Memorization Timelapse (Seg 16)
    angel_tick_ms = int(round(angel_mem_ev["t_start"] * 1000))
    angel_tick_dur = angel_mem_ev["dur"]
    arthur_tick_ms = int(round(arthur_mem_ev["t_start"] * 1000))
    arthur_tick_dur = arthur_mem_ev["dur"]

    filter_chains.append(
        f"[2:a]atrim=0:{angel_tick_dur:.3f},asetpts=PTS-STARTPTS,"
        f"volume=0.80,adelay={angel_tick_ms}|{angel_tick_ms}[tick_angel]"
    )
    filter_chains.append(
        f"[3:a]atrim=0:{arthur_tick_dur:.3f},asetpts=PTS-STARTPTS,"
        f"volume=0.80,adelay={arthur_tick_ms}|{arthur_tick_ms}[tick_arthur]"
    )

    sfx_labels = ["[voice]", "[music]", "[tick_angel]", "[tick_arthur]"]
    input_idx = 4

    # Add segment SFX triggers
    for ev in timeline:
        sname = ev["sfx"]
        if not sname or sname not in sfx_map:
            continue
        spath, svol = sfx_map[sname]
        if not spath.exists():
            continue
        delay_ms = max(0, int(round(ev["t_start"] * 1000)))
        inputs.extend(["-i", str(spath)])
        lbl = f"[sfx_{input_idx}]"
        filter_chains.append(f"[{input_idx}:a]volume={svol:.2f},adelay={delay_ms}|{delay_ms}{lbl}")
        sfx_labels.append(lbl)
        input_idx += 1

    amix_inputs = "".join(sfx_labels)
    num_inputs = len(sfx_labels)
    filter_chains.append(
        f"{amix_inputs}amix=inputs={num_inputs}:duration=first:dropout_transition=0:normalize=0,"
        f"alimiter=limit=0.95[aout]"
    )

    # Burn in ASS captions
    ass_escaped = ass_file.as_posix().replace(":", "\\:").replace("'", "\\'")
    filter_chains.append(f"[0:v]ass='{ass_escaped}'[vfinal]")

    master_fc = ";".join(filter_chains)

    cmd_final = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", master_fc,
        "-map", "[vfinal]",
        "-map", "[aout]",
        "-t", f"{total_dur:.3f}",
        "-r", "60",
        "-c:v", "h264_videotoolbox", "-b:v", "14M",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(FINAL_OUT),
    ]
    run_cmd(cmd_final, desc=f"[5/5] Exporting master render with burned-in one-word captions to {FINAL_OUT}")

    # Export Cover Image at 1.40s
    run_cmd(
        [
            "ffmpeg", "-y",
            "-ss", "1.40",
            "-i", str(FINAL_OUT),
            "-frames:v", "1",
            "-q:v", "2",
            str(COVER_OUT),
        ],
        desc="🖼️  Exporting clean cover image at 00:01.40",
    )

    # Export lightweight preview for inspection (< 25 MB)
    run_cmd(
        [
            "ffmpeg", "-y",
            "-i", str(FINAL_OUT),
            "-vf", "scale=540:960,fps=30",
            "-c:v", "h264_videotoolbox", "-b:v", "1500k",
            "-c:a", "aac", "-b:a", "128k",
            str(PREVIEW_OUT),
        ],
        desc="⚡ Exporting draft preview",
    )

    print("=================================================================")
    print(f"✅ Master Final Export: {FINAL_OUT}")
    print(f"🖼️  Cover Image:        {COVER_OUT}")
    print(f"⚡ Fast Draft Preview:  {PREVIEW_OUT}")
    print("=================================================================")


if __name__ == "__main__":
    build_video()
