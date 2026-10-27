#!/usr/bin/env python3
"""
build_match_kartu.py — Complete AI Automated Editing Pipeline for "Match Kartu Challenge"
Vertical 9:16 (1080x1920) Master Cut — Revision v3.

Fixes Implemented (User Revision & Learned Rules):
1. Song: Authentic Chopin Nocturne in E-flat major, Op. 9, No. 2 (nocturne_op9_in_eb.wav - Frank Levy Musopen).
2. Word Callouts: Removed '+1' and '!' (clean words only: ALPAKA, BABI, KUDA, DOMBA, KAMBING, SAPI).
   Removed 'CLEAN SWEEP!' from winner badge.
3. Lamb (Domba) Fully Shown: Extended cut to 60.40 -> 64.50 so both cards and Angel tapping the pair are completely visible.
4. Correct Sapi & Kambing Pair Timing:
   - Kambing: 66.50 -> 73.50 (shows second goat card reveal at 72.8s with KAMBING callout).
   - Sapi: 73.80 -> 78.00 (shows both final cow cards revealed with SAPI callout).
   - Winner badge: appears only during celebration at 78.50s.
5. Accurate Caption: Corrected Arthur's last reaction words from 'Gak bisa terima' to 'Gak terima!'.
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path

WORKSPACE = Path("/Users/arthurandersen/Documents/AI_Video_Editor_Gemini")
PROJECT_NAME = "Match Kartu"
RAW_VIDEO = WORKSPACE / f"raw/{PROJECT_NAME}/IMG_0648.MOV"
MEME_VIDEO = WORKSPACE / "Meme Material/Hi! Okay,,, (Original video).mp4"
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
# 1. Render High-Contrast Title & Scoreboard Overlays via Swift
# ---------------------------------------------------------------------------
def render_graphics_swift() -> dict[str, Path]:
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

func drawBlackWithWhiteOutline(_ text: String, rect: NSRect, font: NSFont) {{
    let textStorage = NSTextStorage(string: text)
    let textContainer = NSTextContainer(containerSize: rect.size)
    let layoutManager = NSLayoutManager()
    layoutManager.addTextContainer(textContainer)
    textStorage.addLayoutManager(layoutManager)
    
    let style = NSMutableParagraphStyle()
    style.alignment = .center
    textStorage.addAttribute(.font, value: font, range: NSRange(location: 0, length: text.count))
    textStorage.addAttribute(.paragraphStyle, value: style, range: NSRange(location: 0, length: text.count))
    
    NSGraphicsContext.current?.saveGraphicsState()
    let shadow = NSShadow()
    shadow.shadowColor = NSColor.black.withAlphaComponent(0.4)
    shadow.shadowOffset = NSSize(width: 0, height: -3)
    shadow.shadowBlurRadius = 8
    shadow.set()
    
    textStorage.addAttribute(.strokeColor, value: NSColor.white, range: NSRange(location: 0, length: text.count))
    textStorage.addAttribute(.strokeWidth, value: 12.0, range: NSRange(location: 0, length: text.count))
    layoutManager.drawGlyphs(forGlyphRange: NSRange(location: 0, length: textStorage.length), at: rect.origin)
    
    textStorage.addAttribute(.foregroundColor, value: NSColor.black, range: NSRange(location: 0, length: text.count))
    textStorage.addAttribute(.strokeWidth, value: 0, range: NSRange(location: 0, length: text.count))
    layoutManager.drawGlyphs(forGlyphRange: NSRange(location: 0, length: textStorage.length), at: rect.origin)
    NSGraphicsContext.current?.restoreGraphicsState()
}}

func drawWhiteWithBlackOutline(_ text: String, rect: NSRect, font: NSFont, accentColor: NSColor = .white) {{
    let textStorage = NSTextStorage(string: text)
    let textContainer = NSTextContainer(containerSize: rect.size)
    let layoutManager = NSLayoutManager()
    layoutManager.addTextContainer(textContainer)
    textStorage.addLayoutManager(layoutManager)
    
    let style = NSMutableParagraphStyle()
    style.alignment = .center
    textStorage.addAttribute(.font, value: font, range: NSRange(location: 0, length: text.count))
    textStorage.addAttribute(.paragraphStyle, value: style, range: NSRange(location: 0, length: text.count))
    
    NSGraphicsContext.current?.saveGraphicsState()
    let shadow = NSShadow()
    shadow.shadowColor = NSColor.black.withAlphaComponent(0.85)
    shadow.shadowOffset = NSSize(width: 0, height: -4)
    shadow.shadowBlurRadius = 10
    shadow.set()
    
    textStorage.addAttribute(.strokeColor, value: NSColor.black, range: NSRange(location: 0, length: text.count))
    textStorage.addAttribute(.strokeWidth, value: 13.0, range: NSRange(location: 0, length: text.count))
    layoutManager.drawGlyphs(forGlyphRange: NSRange(location: 0, length: textStorage.length), at: rect.origin)
    
    textStorage.addAttribute(.foregroundColor, value: accentColor, range: NSRange(location: 0, length: text.count))
    textStorage.addAttribute(.strokeWidth, value: 0, range: NSRange(location: 0, length: text.count))
    layoutManager.drawGlyphs(forGlyphRange: NSRange(location: 0, length: textStorage.length), at: rect.origin)
    NSGraphicsContext.current?.restoreGraphicsState()
}}

// 1. Hook Title (Upper window blinds area)
let (repHook, _) = createCanvas()
let fontSub = NSFont(name: "HelveticaNeue-Bold", size: 66) ?? NSFont.boldSystemFont(ofSize: 66)
let fontMain = NSFont(name: "Arial-Black", size: 88) ?? NSFont.boldSystemFont(ofSize: 88)
drawBlackWithWhiteOutline("challenge", rect: NSRect(x: 40, y: 1690, width: 1000, height: 95), font: fontSub)
drawWhiteWithBlackOutline("MATCH KARTU 🃏", rect: NSRect(x: 30, y: 1570, width: 1020, height: 120), font: fontMain)
savePNG(repHook, "hook_match_kartu.png")

// 2. Scoreboard Badges: Clean animal names only (NO '+1' and NO '!')
struct ScoreInfo {{
    let filename: String
    let text: String
    let sub: String
    let isGold: Bool
}}

let scores: [ScoreInfo] = [
    ScoreInfo(filename: "score_0_0.png", text: "ANGEL 0 — 0 ARTHUR", sub: "", isGold: false),
    ScoreInfo(filename: "score_1_0.png", text: "ANGEL 1 — 0 ARTHUR", sub: "ALPAKA", isGold: false),
    ScoreInfo(filename: "score_2_0.png", text: "ANGEL 2 — 0 ARTHUR", sub: "BABI", isGold: false),
    ScoreInfo(filename: "score_3_0.png", text: "ANGEL 3 — 0 ARTHUR", sub: "KUDA", isGold: false),
    ScoreInfo(filename: "score_4_0.png", text: "ANGEL 4 — 0 ARTHUR", sub: "DOMBA", isGold: false),
    ScoreInfo(filename: "score_5_0.png", text: "ANGEL 5 — 0 ARTHUR", sub: "KAMBING", isGold: false),
    ScoreInfo(filename: "score_6_0.png", text: "ANGEL 6 — 0 ARTHUR", sub: "SAPI", isGold: false),
    ScoreInfo(filename: "score_winner.png", text: "🏆 ANGEL WINS 6 — 0! 🏆", sub: "", isGold: true)
]

let fontScore = NSFont(name: "Arial-Black", size: 52) ?? NSFont.boldSystemFont(ofSize: 52)
let fontSubScore = NSFont(name: "Arial-Black", size: 40) ?? NSFont.boldSystemFont(ofSize: 40)
let goldColor = NSColor(red: 1.0, green: 0.84, blue: 0.0, alpha: 1.0)
let limeColor = NSColor(red: 0.35, green: 1.0, blue: 0.35, alpha: 1.0)

for s in scores {{
    let (rep, _) = createCanvas()
    let mainColor = s.isGold ? goldColor : .white
    drawWhiteWithBlackOutline(s.text, rect: NSRect(x: 40, y: 1770, width: 1000, height: 75), font: fontScore, accentColor: mainColor)
    if !s.sub.isEmpty {{
        drawWhiteWithBlackOutline(s.sub, rect: NSRect(x: 40, y: 1700, width: 1000, height: 65), font: fontSubScore, accentColor: limeColor)
    }}
    savePNG(rep, s.filename)
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
        "hook": BROLL_DIR / "hook_match_kartu.png",
        "score_0_0": BROLL_DIR / "score_0_0.png",
        "score_1_0": BROLL_DIR / "score_1_0.png",
        "score_2_0": BROLL_DIR / "score_2_0.png",
        "score_3_0": BROLL_DIR / "score_3_0.png",
        "score_4_0": BROLL_DIR / "score_4_0.png",
        "score_5_0": BROLL_DIR / "score_5_0.png",
        "score_6_0": BROLL_DIR / "score_6_0.png",
        "score_winner": BROLL_DIR / "score_winner.png",
    }


# ---------------------------------------------------------------------------
# 2. Define the Edit Decision List (EDL) with Precise Pair Revelations
# ---------------------------------------------------------------------------
SEGMENTS = [
    # 1. Opening Title Hook (0.00 -> 2.62)
    {
        "id": 1,
        "src": "main",
        "start": 0.00,
        "end": 2.62,
        "mode": "normal",
        "card": "hook",
        "caption": "",
        "sfx": "whoosh",
    },
    # 2. Suit / Gambreng (3.08 -> 5.70)
    {
        "id": 2,
        "src": "main",
        "start": 3.08,
        "end": 5.70,
        "mode": "zoom_both",
        "card": "score_0_0",
        "caption": "Suit dulu! Ladies first...",
        "sfx": "pop",
    },
    # 3. Arthur's Turn: Babi & Sapi (19.20 -> 22.80)
    {
        "id": 3,
        "src": "main",
        "start": 19.20,
        "end": 22.80,
        "mode": "zoom_arthur",
        "card": "score_0_0",
        "caption": "Babi... aduh dua-duanya beda!",
        "sfx": "pop",
    },
    # 4. Angel's Match 1: Alpaka! (23.00 -> 27.80)
    {
        "id": 4,
        "src": "main",
        "start": 23.00,
        "end": 27.80,
        "mode": "zoom_angel",
        "card": "score_1_0",
        "caption": "Ini apa guys? Alpaka... dapet satu!",
        "sfx": "win",
    },
    # 5. Arthur's Blunder: Flips Pig and forgets where the other was! (38.80 -> 41.50)
    {
        "id": 5,
        "src": "main",
        "start": 38.80,
        "end": 41.50,
        "mode": "zoom_arthur",
        "card": "score_1_0",
        "caption": "Babi! Eh tadi babi mana ya?",
        "sfx": "pop",
    },
    # 6. Angel Steal! (41.50 -> 44.30)
    {
        "id": 6,
        "src": "main",
        "start": 41.50,
        "end": 44.30,
        "mode": "normal",
        "card": "score_2_0",
        "caption": "Babi! HAHAHA!",
        "sfx": "win",
    },
    # 7. Arthur Facepalm with Freeze / Pause on Arthur (44.30 -> 46.50 + 0.6s hold)
    {
        "id": 7,
        "src": "main",
        "start": 44.30,
        "end": 46.50,
        "freeze_hold": 0.60,
        "mode": "arthur_bw_zoom",
        "card": "score_2_0",
        "caption": "Kok gitu ya?!",
        "sfx": "boom",
    },
    # 8. MEME CUTAWAY: Hi! Okay,,, (Original video).mp4 from 4.00s to end (6.64s)
    {
        "id": 8,
        "src": "meme",
        "start": 4.00,
        "end": 6.64,
        "mode": "meme_portrait",
        "card": "",
        "caption": "Okay...",
        "sfx": "",
    },
    # 9. Angel Match 3: Kuda / Donkey (56.40 -> 59.50)
    {
        "id": 9,
        "src": "main",
        "start": 56.40,
        "end": 59.50,
        "mode": "zoom_both",
        "card": "score_3_0",
        "caption": "Donkey / Kuda!",
        "sfx": "win",
    },
    # 10. Angel Match 4: Domba / Sheep (60.40 -> 64.50) — Fully shows both lamb cards face up!
    {
        "id": 10,
        "src": "main",
        "start": 60.40,
        "end": 64.50,
        "mode": "zoom_both",
        "card": "score_4_0",
        "caption": "Domba! Domba!",
        "sfx": "win",
    },
    # 11. Angel Match 5: Kambing (66.50 -> 73.50) — Shows second goat card reveal at 72.8s!
    {
        "id": 11,
        "src": "main",
        "start": 66.50,
        "end": 73.50,
        "mode": "zoom_both",
        "card": "score_5_0",
        "caption": "Guys look at this, I'm so clever! Kambing!",
        "sfx": "win",
    },
    # 12. Angel Match 6: Sapi Final Match (73.80 -> 78.00) — Shows both cow cards flipped!
    {
        "id": 12,
        "src": "main",
        "start": 73.80,
        "end": 78.00,
        "mode": "zoom_both",
        "card": "score_6_0",
        "caption": "Tadaaa! Sapi!",
        "sfx": "win",
    },
    # 13. Celebration & Arthur's Defeat: "Hoki hoki hoki... Gak terima!" (78.50 -> 85.00)
    {
        "id": 13,
        "src": "main",
        "start": 78.50,
        "end": 85.00,
        "mode": "zoom_both",
        "card": "score_winner",
        "caption": "Hoki hoki hoki! Gak terima!",
        "sfx": "win",
    },
    # 14. Outro Punchline (88.50 -> 91.50)
    {
        "id": 14,
        "src": "main",
        "start": 88.50,
        "end": 91.50,
        "mode": "zoom_arthur",
        "card": "score_winner",
        "caption": "Gua lupa taruhnya tadi di mana...",
        "sfx": "",
    },
]


# ---------------------------------------------------------------------------
# 3. Dynamic Spoken Captions (Rule 49 & Rule 38)
#    - One word / short phrase at a time, synced to speech, vanishes on pause
#    - No captions during opening title hook (0:00 -> 2.62)
# ---------------------------------------------------------------------------
DYNAMIC_WORDS = [
    # Seg 2: Suit (3.08 -> 5.70)
    (4.76, 5.04, "Oh"),
    (5.04, 5.30, "oke,"),
    (5.40, 5.70, "Ladies"),
    (5.70, 5.90, "dulu!"),
    # Seg 3: Arthur's turn (19.20 -> 22.80)
    (19.28, 19.60, "Ayo"),
    (19.60, 20.20, "ini..."),
    (20.84, 21.20, "Gak ada"),
    (21.34, 21.80, "beda!"),
    (21.98, 22.35, "Semua"),
    (22.35, 22.75, "sama!"),
    # Seg 4: Angel match 1 (23.00 -> 27.80)
    (23.84, 24.16, "Ini"),
    (24.16, 24.50, "apa"),
    (24.50, 24.92, "guys?"),
    (25.30, 25.80, "Alpaka..."),
    (26.16, 26.66, "Dapet"),
    (26.66, 27.40, "satu!"),
    # Seg 5: Arthur flips Pig (38.80 -> 41.50)
    (39.42, 39.90, "Babi!"),
    (40.62, 41.00, "Eh tadi"),
    (41.00, 41.45, "mana ya?"),
    # Seg 6: Angel Steal (41.50 -> 44.30)
    (42.44, 43.10, "BABI!"),
    (43.40, 44.20, "HAHAHA!"),
    # Seg 7: Arthur Facepalm (44.30 -> 46.50 + 0.60s freeze hold)
    (45.40, 45.95, "Kok"),
    (45.95, 46.40, "gitu"),
    (46.40, 47.10, "ya?!"),
    # Seg 9: Angel Match 3 (56.40 -> 59.50)
    (57.66, 58.20, "Donkey..."),
    (58.20, 58.80, "KUDA!"),
    # Seg 10: Angel Match 4 (60.40 -> 64.50)
    (62.20, 62.80, "DOMBA!"),
    (62.90, 63.60, "DOMBA!"),
    # Seg 11: Angel Match 5 (66.50 -> 73.50)
    (67.24, 68.20, "Look at this..."),
    (68.50, 69.20, "I'm so"),
    (69.20, 70.30, "clever!"),
    (71.18, 71.90, "KAMBING!"),
    (72.00, 72.80, "Tadi di sini!"),
    # Seg 12: Angel Match 6 (73.80 -> 78.00)
    (74.48, 75.30, "Tadaaa!"),
    (75.50, 77.20, "SAPI!"),
    # Seg 13: Celebration (78.50 -> 85.00)
    (79.30, 79.66, "Hoki,"),
    (79.75, 80.10, "hoki,"),
    (80.30, 80.80, "hoki!"),
    (83.30, 83.90, "Gak"),
    (83.90, 84.60, "terima!"),
    # Seg 14: Outro (88.50 -> 91.50)
    (88.52, 89.00, "Gua"),
    (89.00, 89.40, "lupa,"),
    (89.50, 90.00, "tadi"),
    (90.00, 90.70, "di mana?"),
]


def generate_ass_subtitles(ass_file: Path) -> list[dict]:
    timeline_events = []
    current_time = 0.0

    for seg in SEGMENTS:
        base_dur = seg["end"] - seg["start"]
        freeze_hold = seg.get("freeze_hold", 0.0)
        dur = base_dur + freeze_hold

        ev = {
            "id": seg["id"],
            "src": seg["src"],
            "t_start": current_time,
            "t_end": current_time + dur,
            "dur": dur,
            "base_dur": base_dur,
            "freeze_hold": freeze_hold,
            "raw_start": seg["start"],
            "raw_end": seg["end"],
            "mode": seg["mode"],
            "card": seg["card"],
            "caption": seg["caption"],
            "sfx": seg["sfx"],
        }
        timeline_events.append(ev)
        current_time += dur

    def fmt_time(t: float) -> str:
        hours = int(t // 3600)
        minutes = int((t % 3600) // 60)
        secs = t % 60
        return f"{hours}:{minutes:02d}:{secs:05.2f}"

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "WrapStyle: 0",
        "ScaledBorderAndShadow: yes",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Default,Arial Black,50,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5.0,2.5,2,60,60,190,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    for ev in timeline_events:
        if ev["id"] == 1:
            # Rule 38: No bottom captions during hook title
            continue

        if ev["src"] == "meme":
            # Synced meme punchline caption
            s_str = fmt_time(ev["t_start"] + 0.40)
            e_str = fmt_time(ev["t_end"] - 0.30)
            lines.append(f"Dialogue: 0,{s_str},{e_str},Default,,0,0,0,,Okay...")
            continue

        # Map dynamic spoken words to timeline
        for w_start, w_end, text in DYNAMIC_WORDS:
            if w_start >= ev["raw_start"] - 0.05 and w_end <= ev["raw_end"] + ev["freeze_hold"] + 0.15:
                t_sub_start = ev["t_start"] + max(0.0, w_start - ev["raw_start"])
                t_sub_end = ev["t_start"] + min(ev["dur"], w_end - ev["raw_start"])
                if t_sub_end > t_sub_start + 0.10:
                    s_str = fmt_time(t_sub_start)
                    e_str = fmt_time(t_sub_end)
                    lines.append(f"Dialogue: 0,{s_str},{e_str},Default,,0,0,0,,{text}")

    ass_file.write_text("\n".join(lines), encoding="utf-8")
    return timeline_events


# ---------------------------------------------------------------------------
# 4. Master Build Video
# ---------------------------------------------------------------------------
def build_video() -> None:
    print("🎨 [1/5] Rendering High-Contrast Title & Scoreboard Overlays via Swift...")
    cards = render_graphics_swift()

    ass_path = DRAFT_DIR / "match_kartu_captions.ass"
    timeline_events = generate_ass_subtitles(ass_path)
    edl_path = DRAFT_DIR / "match_kartu_edl.json"
    edl_path.write_text(json.dumps(timeline_events, indent=2), encoding="utf-8")

    total_duration = timeline_events[-1]["t_end"]
    print(f"⏱️  Total edited timeline duration: {total_duration:.2f}s ({len(timeline_events)} segments)")

    # Authentic Chopin Nocturne Op. 9 No. 2 in E-flat Major
    music_src = MUSIC_DIR / "nocturne_op9_in_eb.wav"
    pop_sfx = SFX_DIR / "pop.wav"
    win_sfx = SFX_DIR / "point_win.wav"
    boom_sfx = SFX_DIR / "meme_boom.wav"
    whoosh_sfx = SFX_DIR / "whoosh.wav"

    print("✂️  [2/5] Slicing camera cuts, freeze-frame, meme, and overlays...")
    with tempfile.TemporaryDirectory() as tmpdir:
        seg_files = []

        for idx, ev in enumerate(timeline_events):
            seg_out = Path(tmpdir) / f"seg_{idx:03d}.mp4"
            src = ev["src"]
            start = ev["raw_start"]
            dur = ev["dur"]
            base_dur = ev["base_dur"]
            freeze_hold = ev["freeze_hold"]
            mode = ev["mode"]
            card_key = ev["card"]

            fade_out_st = max(0.0, dur - 0.015)
            af = f"aresample=48000,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.015,afade=t=out:st={fade_out_st:.3f}:d=0.015,apad=whole_dur={dur:.4f},atrim=0:{dur:.4f},asetpts=PTS-STARTPTS"

            if src == "meme":
                fade_out_st = max(0.0, dur - 0.015)
                # Boost meme audio +14 dB with limiter so "Okay..." dialogue is clear and loud
                af_meme = (
                    f"aresample=48000,asetpts=PTS-STARTPTS,volume=4.5,alimiter=limit=0.92,"
                    f"afade=t=in:st=0:d=0.015,afade=t=out:st={fade_out_st:.3f}:d=0.015,"
                    f"apad=whole_dur={dur:.4f},atrim=0:{dur:.4f},asetpts=PTS-STARTPTS"
                )
                filter_complex = (
                    f"[0:v]scale=1080:1920,gblur=sigma=30[bg];"
                    f"[0:v]scale=1080:608[fg];"
                    f"[bg][fg]overlay=0:(1920-608)/2,fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS[vout];"
                    f"[0:a]{af_meme}[aout]"
                )
                run_cmd([
                    "ffmpeg", "-y",
                    "-ss", f"{start:.3f}",
                    "-t", f"{dur:.4f}",
                    "-i", str(MEME_VIDEO),
                    "-filter_complex", filter_complex,
                    "-map", "[vout]",
                    "-map", "[aout]",
                    "-r", "30",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1",
                    "-loglevel", "error",
                    str(seg_out),
                ])
            else:
                card_png = cards[card_key]

                if mode == "zoom_both":
                    vf_cam = "scale=1080*1.10:1920*1.10,crop=1080:1920:(iw-1080)/2:(ih-1920)*0.25"
                elif mode == "zoom_arthur":
                    vf_cam = "scale=1080*1.28:1920*1.28,crop=1080:1920:280:200"
                elif mode == "zoom_angel":
                    vf_cam = "scale=1080*1.28:1920*1.28,crop=1080:1920:20:240"
                elif mode == "arthur_bw_zoom":
                    vf_cam = f"scale=1080*1.65:1920*1.65,crop=1080:1920:560:320,hue=s=0,tpad=stop_mode=clone:stop_duration={freeze_hold:.3f}"
                else:
                    vf_cam = "scale=1080:1920"

                filter_complex = (
                    f"[0:v]{vf_cam},fps=30,trim=0:{dur:.4f},setpts=PTS-STARTPTS[vbase];"
                    f"[vbase][1:v]overlay=0:0:format=auto[vout];"
                    f"[0:a]{af}[aout]"
                )

                run_cmd([
                    "ffmpeg", "-y",
                    "-ss", f"{start:.3f}",
                    "-t", f"{base_dur + 0.35:.3f}",
                    "-i", str(RAW_VIDEO),
                    "-loop", "1",
                    "-t", f"{dur:.4f}",
                    "-i", str(card_png),
                    "-filter_complex", filter_complex,
                    "-map", "[vout]",
                    "-map", "[aout]",
                    "-r", "30",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
                    "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1",
                    "-loglevel", "error",
                    str(seg_out),
                ])
            seg_files.append(seg_out)

        # Concatenate video segments
        print("🔗 [3/5] Concatenating edited video segments...")
        concat_txt = Path(tmpdir) / "concat_list.txt"
        with open(concat_txt, "w") as f:
            for s in seg_files:
                f.write(f"file '{s}'\n")

        raw_concat_mp4 = Path(tmpdir) / "raw_concat.mp4"
        run_cmd([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c:v", "copy",
            "-c:a", "copy",
            "-loglevel", "error",
            str(raw_concat_mp4),
        ])

        # Mix Sound Design: Ducked Nocturne in E-flat Major + SFX
        print("🎵 [4/5] Mixing Sound Design (Ducked Chopin Nocturne in E-flat Major + SFX + ASS Captions)...")
        sfx_delays = []
        sfx_merge_tags = []

        for ev in timeline_events:
            sfx_type = ev["sfx"]
            t_ms = int(ev["t_start"] * 1000)
            if sfx_type == "whoosh":
                sfx_delays.append(f"[2:a]adelay={t_ms}|{t_ms},volume=0.9[sfx_w_{ev['id']}];")
                sfx_merge_tags.append(f"[sfx_w_{ev['id']}]")
            elif sfx_type == "pop":
                sfx_delays.append(f"[3:a]adelay={t_ms}|{t_ms},volume=0.8[sfx_p_{ev['id']}];")
                sfx_merge_tags.append(f"[sfx_p_{ev['id']}]")
            elif sfx_type == "win":
                sfx_delays.append(f"[4:a]adelay={t_ms}|{t_ms},volume=1.0[sfx_win_{ev['id']}];")
                sfx_merge_tags.append(f"[sfx_win_{ev['id']}]")
            elif sfx_type == "boom":
                sfx_delays.append(f"[5:a]adelay={t_ms}|{t_ms},volume=1.1[sfx_boom_{ev['id']}];")
                sfx_merge_tags.append(f"[sfx_boom_{ev['id']}]")

        sfx_filter_body = "".join(sfx_delays)
        all_sfx_tags = "".join(sfx_merge_tags)
        num_sfx = len(sfx_merge_tags)

        meme_ev = next((ev for ev in timeline_events if ev["src"] == "meme"), None)
        if meme_ev:
            m_st = meme_ev["t_start"]
            m_en = meme_ev["t_end"]
            music_vol_expr = f"'if(between(t,{m_st:.3f},{m_en:.3f}),0.03,0.20)':eval=frame"
        else:
            music_vol_expr = "0.20"

        # Audio ducking: Nocturne in E-flat Major ducked under dialogue (-20 dB), dipped sharply to 0.03 during meme
        audio_filter = (
            f"[0:a]volume=1.25,highpass=f=80[speech];"
            f"[1:a]atrim=0:{total_duration:.3f},asetpts=PTS-STARTPTS,volume={music_vol_expr},"
            f"afade=t=in:st=0:d=0.3,afade=t=out:st={total_duration-1.2:.3f}:d=1.2[music_bed];"
            f"{sfx_filter_body}"
            f"{all_sfx_tags}amix=inputs={num_sfx}:duration=first:dropout_transition=0[all_sfx];"
            f"[speech][music_bed][all_sfx]amix=inputs=3:duration=first:dropout_transition=0[aout]"
        )

        final_mp4 = FINAL_DIR / "match_kartu_challenge.mp4"
        cover_png = FINAL_DIR / "match_kartu_cover.png"
        preview_mp4 = DRAFT_DIR / "match_kartu_preview.mp4"

        print(f"🎬 [5/5] Exporting master render with burned-in ASS captions to {final_mp4}...")
        run_cmd([
            "ffmpeg", "-y",
            "-i", str(raw_concat_mp4),
            "-i", str(music_src),
            "-i", str(whoosh_sfx),
            "-i", str(pop_sfx),
            "-i", str(win_sfx),
            "-i", str(boom_sfx),
            "-filter_complex",
            f"[0:v]subtitles={ass_path}:fontsdir=/System/Library/Fonts[vout];" + audio_filter,
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "320k",
            "-shortest",
            "-loglevel", "error",
            str(final_mp4),
        ])

        # Export high-res clean cover frame at 00:01.40
        print("🖼️  Exporting cover image...")
        run_cmd([
            "ffmpeg", "-y",
            "-ss", "1.40",
            "-i", str(final_mp4),
            "-frames:v", "1",
            "-loglevel", "error",
            str(cover_png),
        ])

        # Export fast low-res draft preview for instant inspection
        print("⚡ Exporting draft preview...")
        run_cmd([
            "ffmpeg", "-y",
            "-i", str(final_mp4),
            "-vf", "scale=-2:720",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
            "-c:a", "aac", "-b:a", "96k",
            "-loglevel", "error",
            str(preview_mp4),
        ])

    print("=================================================================")
    print(f"✅ Master Final Export: {final_mp4}")
    print(f"🖼️  Cover Image:        {cover_png}")
    print(f"⚡ Fast Draft Preview:  {preview_mp4}")
    print("=================================================================")


if __name__ == "__main__":
    build_video()
