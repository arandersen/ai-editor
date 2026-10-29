#!/usr/bin/env python3
"""
scripts/build_fx_library.py
Builds:
1. Canonical starter assets in `assets/` (SVG app logos, device mockups, paper/grain textures, manifest.json, README.md)
2. All 31 Reusable HyperFrames Motion Graphics Templates in `animations/_fx_library/<slug>/`
   (each with deterministic GSAP `index.html` + `params.json` documenting all inputs & Dual-Handle asset paths).
"""

import json
import os
import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from editor.scene_bindings import binding_script

REFRESH_SCENES = False

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT, "assets")
FX_LIB_DIR = os.path.join(ROOT, "animations", "_fx_library")


def write_text(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and not (REFRESH_SCENES and Path(path).is_relative_to(FX_LIB_DIR)):
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def build_starter_assets():
    # 1. App Logos in assets/logos/apps/
    logos = {
        "capcut.svg": ('#000000', '#FFFFFF', 'CC', 'CapCut'),
        "edits.svg": ('#1E1B2E', '#F472B6', 'ED', 'Edits'),
        "inshot.svg": ('#E11D48', '#FFFFFF', 'IN', 'InShot'),
        "premiere.svg": ('#00005B', '#9999FF', 'Pr', 'Premiere'),
        "ffmpeg.svg": ('#007808', '#4ADE80', 'FF', 'FFmpeg'),
        "claude.svg": ('#D97757', '#FFF7ED', 'AI', 'Claude'),
        "hyperframes.svg": ('#0A0D14', '#38BDF8', 'HF', 'HyperFrames'),
    }
    for fname, (bg, fg, short, label) in logos.items():
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240">
  <rect width="240" height="240" rx="54" fill="{bg}"/>
  <rect x="6" y="6" width="228" height="228" rx="48" fill="none" stroke="{fg}" stroke-opacity="0.35" stroke-width="6"/>
  <text x="120" y="148" text-anchor="middle" font-family="Inter, -apple-system, Helvetica Neue, sans-serif" font-weight="900" font-size="104" fill="{fg}">{short}</text>
</svg>"""
        write_text(os.path.join(ASSETS_DIR, "logos", "apps", fname), svg)

    # 2. Device Mockup in assets/mockups/devices/iphone_16_pro_frame.svg
    iphone_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1840" width="900" height="1840">
  <rect x="12" y="12" width="876" height="1816" rx="136" fill="#141417" stroke="#3F3F46" stroke-width="16"/>
  <rect x="44" y="44" width="812" height="1752" rx="108" fill="#090A0F"/>
  <rect x="290" y="76" width="320" height="76" rx="38" fill="#000000"/>
  <circle cx="566" cy="114" r="16" fill="#1E293B"/>
</svg>"""
    write_text(os.path.join(ASSETS_DIR, "mockups", "devices", "iphone_16_pro_frame.svg"), iphone_svg)

    # 3. Textures in assets/photo/textures/
    grid_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M 48 0 L 0 0 0 48" fill="none" stroke="#CBD5E1" stroke-width="2"/>
    </pattern>
  </defs>
  <rect width="1080" height="1920" fill="#F8FAFC"/>
  <rect width="1080" height="1920" fill="url(#grid)"/>
</svg>"""
    write_text(os.path.join(ASSETS_DIR, "photo", "textures", "notebook_grid_paper.svg"), grid_svg)

    cream_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <rect width="1080" height="1920" fill="#F0EADE"/>
</svg>"""
    write_text(os.path.join(ASSETS_DIR, "photo", "textures", "cream_editorial_paper.svg"), cream_svg)

    # 4. Write assets/manifest.json documenting the Dual-Handle Asset System
    manifest = {
        "schema_version": "2.0",
        "description": "Strict Dual-Handle Asset Registry for AI Video Editor (Conductor + Flash Editor)",
        "handles": {
            "@asset": {
                "root": "assets/",
                "description": "Global reusable studio library (videos, photos, reels, backgrounds, memes, logos, mockups, fonts, SFX, music).",
                "subfolders": {
                    "@asset/video/backgrounds": "assets/video/backgrounds/ (Loopable studio, abstract, & green-screen replacement plates)",
                    "@asset/video/reels": "assets/video/reels/ (Vertical 9:16 reference reels for @orbit, @reel-grid, @wall-of-reels)",
                    "@asset/video/broll": "assets/video/broll/ (Cinematic B-roll clips & Veo 3.1 reusable library)",
                    "@asset/video/memes": "assets/video/memes/ (Reaction memes & green-screen comedy clips)",
                    "@asset/video/overlays": "assets/video/overlays/ (ProRes 4444 confetti, film grain, light leaks, glass shards)",
                    "@asset/video/screen_recordings": "assets/video/screen_recordings/ (App/UI screen captures for @phone-mockup & @pause-explain)",
                    "@asset/photo/backgrounds": "assets/photo/backgrounds/ (High-res ≥1000px architectural, room, & wall plates)",
                    "@asset/photo/screenshots": "assets/photo/screenshots/ (Retina 4K web/GitHub/article captures via capture_broll.mjs)",
                    "@asset/photo/textures": "assets/photo/textures/ (Torn cream paper #F0EADE, notebook grid, halftone, newspaper clippings)",
                    "@asset/photo/people": "assets/photo/people/ (Cutout portraits & archival human subjects)",
                    "@asset/photo/headlines": "assets/photo/headlines/ (Rendered headline clippings for @headline-wall)",
                    "@asset/photo/thumbnails": "assets/photo/thumbnails/ (Reel cover frames for @reel-grid & @contact-sheet-hook)",
                    "@asset/logos/apps": "assets/logos/apps/ (App/tool SVG/PNG icons for @tool-label, @jiggle-delete, @icon-strike)",
                    "@asset/logos/brands": "assets/logos/brands/ (Brand marks & social icons)",
                    "@asset/mockups/devices": "assets/mockups/devices/ (iPhone 16 Pro & desktop window frames)",
                    "@asset/mockups/ui": "assets/mockups/ui/ (NLE timeline, Lightroom inspector, IG Reel frame chrome)",
                    "@asset/audio/sfx": "assets/audio/sfx/ (48kHz studio foley: pop.wav, whoosh.wav, click.wav, sub_drop.wav, paper_thock.wav, paper_slide.wav, marker_squeak.wav, timeline_tick.wav)",
                    "@asset/audio/music": "assets/audio/music/ (Royalty-free background music tracks)",
                    "@asset/fonts": "assets/fonts/ (Local display, serif, and monospace font files)"
                }
            },
            "@project": {
                "root": "broll/<Project>/ | raw/<Project>/ | transcripts/<Project>/",
                "description": "Per-project scoped handle for clip-specific recordings, Apple Vision ProRes 4444 cutouts, and rendered overlays.",
                "subfolders": {
                    "@project/raw": "raw/<Project>/ (Source camera .MOV/.MP4 clips)",
                    "@project/cutout": "broll/<Project>/cutout_*.mov (ProRes 4444 alpha mattes from scripts/person_cutout.swift)",
                    "@project/broll": "broll/<Project>/ (Project-specific screenshots, Flow AI generations, & HyperFrames .mov/.webm overlays)",
                    "@project/transcript": "transcripts/<Project>/ (10ms RMS acoustic onset JSON & SRT)"
                }
            }
        }
    }
    write_text(os.path.join(ASSETS_DIR, "manifest.json"), json.dumps(manifest, indent=2))

    # 5. Write assets/README.md
    assets_readme = """# Studio Asset Library (`assets/`) & Strict Dual-Handle Resolution Guide

Every AI agent (**Gemini 4 Argon Conductor** & **Gemini 3.8 Flash Editor**) MUST use the **Two-Handle Asset System** (`@asset/...` and `@project/...`) to locate or store videos, photos, reels, backgrounds, logos, mockups, and audio. **Never guess paths or dump files into `/tmp` or the project root.**

---

## 1. Handle #1: `@asset/<type>/<category>/<file>` (Global Reusable Studio Library)

Resolves directly to `<repository>/assets/<type>/<category>/<file>`:

| Handle Prefix | Physical Directory | What Lives Here & Which `@shortcut` Uses It |
| :--- | :--- | :--- |
| **`@asset/video/backgrounds/`** | `assets/video/backgrounds/` | Loopable studio backgrounds, green-screen replacement clips (`@green-screen`). |
| **`@asset/video/reels/`** | `assets/video/reels/` | Vertical 9:16 reference reels (`@orbit`, `@reel-grid`, `@wall-of-reels`). Downloaded via `yt-dlp` or copied from past `renders/final/`. |
| **`@asset/video/broll/`** | `assets/video/broll/` | Reusable cinematic B-roll & Google Flow (**Veo 3.1**) clips (`@flow-video`). |
| **`@asset/video/memes/`** | `assets/video/memes/` | Reaction memes (`What_ Meme.mp4`, `Hi! Okay,,,.mp4`, Rick Astley clip for `@green-screen`, `@meme-what`, `@meme-okay`). |
| **`@asset/video/overlays/`** | `assets/video/overlays/` | ProRes 4444 / alpha overlays (`confetti_loop.mov`, 35mm film grain for `@film-look`, glass shards for `@frame-break`). |
| **`@asset/video/screen_recordings/`** | `assets/video/screen_recordings/` | Screen recordings & scrolling UI captures (`@phone-mockup`, `@pause-explain`). |
| **`@asset/photo/backgrounds/`** | `assets/photo/backgrounds/` | High-res (`>= 1000px`) room, architectural, & paper plates (`@green-screen`, `@vox-collage`). |
| **`@asset/photo/screenshots/`** | `assets/photo/screenshots/` | Authentic 4K Retina web/repo screenshots captured via `scripts/capture_broll.mjs` (`@real-screenshot`, `@phone-mockup`). |
| **`@asset/photo/textures/`** | `assets/photo/textures/` | Cream paper (`#F0EADE`), grid notebook paper, torn edges (`@paper-cut`, `@headline-wall`, `@screenplay-page`). |
| **`@asset/photo/headlines/`** | `assets/photo/headlines/` | Newspaper & article clipping cards (`@headline-wall`). |
| **`@asset/photo/thumbnails/`** | `assets/photo/thumbnails/` | Extracted vertical reel cover frames (`@reel-grid`, `@contact-sheet-hook`, `@video-card`). |
| **`@asset/logos/apps/`** | `assets/logos/apps/` | Starter letter-badge SVGs; replace with verified app artwork when needed (`capcut.svg`, `edits.svg`, `inshot.svg`, `premiere.svg`, `ffmpeg.svg`, `claude.svg` for `@tool-label`, `@jiggle-delete`, `@icon-strike`). |
| **`@asset/logos/brands/`** | `assets/logos/brands/` | Social & brand icons (Instagram Reel chrome, heart, comment, share). |
| **`@asset/mockups/devices/`** | `assets/mockups/devices/` | Device bezels (`iphone_16_pro_frame.svg` for `@phone-mockup`). |
| **`@asset/mockups/ui/`** | `assets/mockups/ui/` | NLE timeline chrome, Lightroom grading panels (`@ui-world`, `@pull-back`, `@nle-timeline`, `@moody-grade`). |
| **`@asset/audio/sfx/`** | `assets/audio/sfx/` (symlinked at `audio/sfx/`) | 48kHz studio SFX (`pop.wav`, `whoosh.wav`, `click.wav`, `sub_drop.wav`, `paper_thock.wav`, `paper_slide.wav`, `marker_squeak.wav`, `timeline_tick.wav`). |
| **`@asset/audio/music/`** | `assets/audio/music/` (symlinked at `audio/music/`) | Royalty-free music beds (`nocturne_op9_in_eb.wav` & `free-audio` MCP tracks). |

---

## 2. Handle #2: `@project/<type>/<file>` (Per-Project Scoped Assets)

Resolves to the active project `<Project Name>` mirrored across `raw/`, `broll/`, `transcripts/`, and `renders/`:

| Handle Prefix | Physical Directory | What Lives Here |
| :--- | :--- | :--- |
| **`@project/raw/<clip>`** | `raw/<Project Name>/<clip>` | Raw camera `.MOV` / `.MP4` footage. |
| **`@project/cutout/<name>.mov`** | `broll/<Project Name>/<name>.mov` | Apple Vision ProRes 4444 (`yuva444p10le`) person cutout generated by `swift ./scripts/person_cutout.swift` (`@text-behind-head`, `@magazine-cover`, `@vertigo`, `@green-screen`, `@paper-cut`, `@orbit`, `@doodle-boil`, `@depth-scatter`, `@reel-grid`). |
| **`@project/broll/<file>`** | `broll/<Project Name>/<file>` | Project-specific HyperFrames rendered overlays (`.mov` / `.webm` / `.mp4`), Google Flow outputs, and captured screenshots. |
| **`@project/transcript/<file>`** | `transcripts/<Project Name>/<file>` | 10ms RMS acoustic onset JSON (`*_acoustic.json`) & SRT files. |

---

## 3. Fallback Sourcing Protocol (When an Asset Does Not Exist Yet)

1. **Web / Article / GitHub Screenshot Needed (`@real-screenshot`, `@headline-wall`, `@phone-mockup`)**:
   Run `node ./scripts/capture_broll.mjs --url <url> --output assets/photo/screenshots/<name>.png`.
2. **Reference Vertical Reels Needed (`@reel-grid`, `@orbit`, `@wall-of-reels`)**:
   Check `assets/video/reels/` first; if fewer than required, extract clips from `renders/final/` or download via `yt-dlp -o "assets/video/reels/%(id)s.%(ext)s" <url>`.
3. **Bespoke Visual / Background Video or Photo Needed (`@green-screen`, `@flow-image`, `@flow-video`)**:
   Generate via **Google Flow MCP** (`flow_generate` + `flow_wait`) and save into `assets/video/backgrounds/` or `broll/<Project Name>/`.
"""
    write_text(os.path.join(ASSETS_DIR, "README.md"), assets_readme)


# Specification of all 31 new Talking Head Effect Templates
FX_SPECS = [
    {
        "slug": "effect-hud",
        "shortcut": "@effect-hud",
        "rule": "Rule TH26",
        "title": "On-Screen Effect Checklist HUD (Split-Dark & Sidebar-Green Themes)",
        "duration": 3.0,
        "sfx": "@asset/audio/sfx/timeline_tick.wav",
        "requires_cutout": False,
        "top_zone": True,
        "default_vars": {
            "theme": "split-dark",
            "headerNumber": "16",
            "headerTitle": "video effects\nclaude can create",
            "activeIndex": 1,
            "itemsLeft": ["01 headline wall", "02 zoom-through cut", "03 vertigo", "04 green screen", "05 phone mockup", "06 digital zoom", "07 paper cut", "08 ui world"],
            "itemsRight": ["09 orbit", "10 frame break", "11 doodle boil", "12 sticky text", "13 before + after", "14 pull-back reveal", "15 depth scatter", "16 comment bubble"]
        },
        "body_html": """
      <div class="hud-wrap" id="hud">
        <div class="hud-title"><span class="accent" id="num">16</span> <span id="ttl">video effects<br/>claude can create</span></div>
        <div class="hud-cols">
          <div class="hud-panel" id="col-left">
            <div class="item active"><b>01</b> headline wall</div>
            <div class="item"><b>02</b> zoom-through cut</div>
            <div class="item"><b>03</b> vertigo</div>
            <div class="item"><b>04</b> green screen</div>
            <div class="item"><b>05</b> phone mockup</div>
            <div class="item"><b>06</b> digital zoom</div>
            <div class="item"><b>07</b> paper cut</div>
            <div class="item"><b>08</b> ui world</div>
          </div>
          <div class="hud-panel" id="col-right">
            <div class="item"><b>09</b> orbit</div>
            <div class="item"><b>10</b> frame break</div>
            <div class="item"><b>11</b> doodle boil</div>
            <div class="item"><b>12</b> sticky text</div>
            <div class="item"><b>13</b> before + after</div>
            <div class="item"><b>14</b> pull-back reveal</div>
            <div class="item"><b>15</b> depth scatter</div>
            <div class="item"><b>16</b> comment bubble</div>
          </div>
        </div>
      </div>""",
        "extra_css": """
      .hud-wrap { position: absolute; top: 6%; left: 4%; right: 4%; display: flex; flex-direction: column; align-items: center; gap: 28px; }
      .hud-title { font-size: 72px; font-weight: 900; line-height: 1.04; text-align: center; letter-spacing: -0.03em; color: #FFFFFF; text-shadow: 0 8px 28px rgba(0,0,0,0.65); }
      .hud-title .accent { color: #F6E478; }
      .hud-cols { width: 100%; display: flex; justify-content: space-between; gap: 36px; }
      .hud-panel { width: 44%; background: rgba(18, 18, 20, 0.72); border: 2px solid rgba(255,255,255,0.14); border-radius: 28px; padding: 26px 32px; display: flex; flex-direction: column; gap: 10px; }
      .item { font-size: 30px; font-weight: 600; color: rgba(255,255,255,0.62); padding: 4px 10px; border-radius: 10px; }
      .item b { opacity: 0.55; margin-right: 8px; font-variant-numeric: tabular-nums; }
      .item.active { color: #F6E478; font-weight: 800; background: rgba(246, 228, 120, 0.14); }
""",
        "gsap_js": """
      tl.fromTo('#hud', { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.35, ease: 'power3.out' }, 0)
        .fromTo('.item.active', { scale: 0.94 }, { scale: 1.03, duration: 0.25, yoyo: true, repeat: 1, ease: 'power2.out' }, 0.2);
"""
    },
    {
        "slug": "keyword-captions",
        "shortcut": "@keyword-captions",
        "rule": "Rule TH27",
        "title": "Dual-Theme Hook/CTA Keyword Captions (Yellow-Glow & White-Pill-Stack)",
        "duration": 2.4,
        "sfx": "@asset/audio/sfx/pop.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "theme": "yellow-glow",
            "line1": "all of these",
            "keyword": "effects?",
            "yPercent": 52.0
        },
        "body_html": """
      <div class="kw-wrap" id="kw">
        <div class="kw-line1" id="l1">all of these</div>
        <div class="kw-hero" id="l2">effects?</div>
      </div>""",
        "extra_css": """
      .kw-wrap { position: absolute; top: 52%; left: 8%; right: 8%; transform: translateY(-50%); text-align: center; display: flex; flex-direction: column; align-items: center; gap: 10px; }
      .kw-line1 { font-size: 84px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; text-shadow: 0 10px 30px rgba(0,0,0,0.75); opacity: 0; }
      .kw-hero { font-size: 124px; font-weight: 900; color: #F6E478; letter-spacing: -0.03em; text-shadow: 0 0 36px rgba(246,228,120,0.55), 0 12px 32px rgba(0,0,0,0.8); opacity: 0; }
""",
        "gsap_js": """
      tl.fromTo('#l1', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.22, ease: 'power3.out' }, 0.0)
        .fromTo('#l2', { opacity: 0, scale: 0.84, filter: 'blur(18px)' }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.28, ease: 'back.out(1.6)' }, 0.16)
        .to('#kw', { opacity: 0, y: -16, duration: 0.2, ease: 'power2.in' }, 2.1);
"""
    },
    {
        "slug": "headline-wall",
        "shortcut": "@headline-wall",
        "rule": "Rule TH28",
        "title": "Torn-Paper Newspaper Clippings Slam + Yellow Marker Highlight",
        "duration": 2.2,
        "sfx": "@asset/audio/sfx/paper_thock.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "kicker": "CREATOR NEWS · TODAY",
            "headlineLine1": "claude can now",
            "headlineLine2": "edit your videos",
            "subClippings": ["claude did the edit", "video, edited by claude", "claude now edits your videos"]
        },
        "body_html": """
      <div class="clip clip-tl" id="c1"><span class="kicker">PRESS</span><div>claude did the edit</div></div>
      <div class="clip clip-tr" id="c2"><span class="kicker">TECH</span><div>video, edited by claude</div></div>
      <div class="clip clip-ml" id="c3"><span class="kicker">REPORT</span><div>claude now edits your videos</div></div>
      <div class="clip clip-hero" id="c4">
        <div class="kicker">CREATOR NEWS · TODAY</div>
        <div class="serif-line">claude can now</div>
        <div class="serif-line hl-wrap"><span class="hl-bar" id="hl"></span><span class="hl-txt">edit your videos</span></div>
      </div>""",
        "extra_css": """
      .clip { position: absolute; background: #F0EADE; color: #141413; padding: 28px 38px; border-radius: 6px; box-shadow: 0 24px 54px rgba(0,0,0,0.65); font-family: Georgia, 'Times New Roman', serif; opacity: 0; border-top: 6px dashed rgba(20,20,19,0.18); border-bottom: 6px dashed rgba(20,20,19,0.18); }
      .kicker { font-family: Inter, sans-serif; font-size: 20px; font-weight: 800; letter-spacing: 0.12em; color: #57534E; margin-bottom: 8px; text-transform: uppercase; }
      .clip-tl { top: 4%; left: 3%; width: 34%; font-size: 38px; font-weight: 700; transform: rotate(-4deg); }
      .clip-tr { top: 3%; right: 3%; width: 34%; font-size: 38px; font-weight: 700; transform: rotate(3.5deg); }
      .clip-ml { top: 38%; left: 3%; width: 36%; font-size: 44px; font-weight: 700; transform: rotate(-2.5deg); }
      .clip-hero { top: 53%; left: 26%; width: 66%; padding: 38px 48px; transform: rotate(-1.5deg); }
      .serif-line { font-size: 74px; font-weight: 700; line-height: 1.08; position: relative; }
      .hl-wrap { display: inline-block; position: relative; }
      .hl-bar { position: absolute; left: -8px; right: -8px; bottom: 4px; height: 78%; background: #F6E478; z-index: 0; transform-origin: left center; transform: scaleX(0); }
      .hl-txt { position: relative; z-index: 1; }
""",
        "gsap_js": """
      tl.fromTo('#c1', { opacity: 0, scale: 1.45, y: -60 }, { opacity: 1, scale: 1, y: 0, duration: 0.22, ease: 'power3.out' }, 0.0)
        .fromTo('#c2', { opacity: 0, scale: 1.45, y: -60 }, { opacity: 1, scale: 1, y: 0, duration: 0.22, ease: 'power3.out' }, 0.10)
        .fromTo('#c3', { opacity: 0, scale: 1.45, x: -80 }, { opacity: 1, scale: 1, x: 0, duration: 0.22, ease: 'power3.out' }, 0.20)
        .fromTo('#c4', { opacity: 0, scale: 1.55, y: 90 }, { opacity: 1, scale: 1, y: 0, duration: 0.26, ease: 'back.out(1.4)' }, 0.30)
        .to('#hl', { scaleX: 1, duration: 0.32, ease: 'power2.out' }, 0.52);
"""
    },
    {
        "slug": "zoom-through",
        "shortcut": "@zoom-through",
        "rule": "Rule TH29",
        "title": "Camera Zoom-Through Punch Transition + 2-Frame Warm White Flash",
        "duration": 0.65,
        "sfx": "@asset/audio/sfx/whoosh.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "peakScale": 6.5,
            "flashColor": "#FFFDF5"
        },
        "body_html": """
      <div class="zoom-ring" id="zr"></div>
      <div class="flash-plate" id="fl"></div>""",
        "extra_css": """
      .zoom-ring { width: 640px; height: 360px; border: 18px solid rgba(240,234,222,0.85); border-radius: 24px; opacity: 0; }
      .flash-plate { position: absolute; inset: 0; background: radial-gradient(circle, #FFFDF5 0%, #F6E478 55%, rgba(255,255,255,0) 100%); opacity: 0; }
""",
        "gsap_js": """
      tl.fromTo('#zr', { opacity: 0.9, scale: 1 }, { opacity: 0, scale: vars.peakScale, duration: 0.28, ease: 'power3.in' }, 0.0)
        .to('#fl', { opacity: 0.95, duration: 0.08, ease: 'power2.in' }, 0.22)
        .to('#fl', { opacity: 0, duration: 0.28, ease: 'power3.out' }, 0.30);
"""
    },
    {
        "slug": "vertigo",
        "shortcut": "@vertigo",
        "rule": "Rule TH30",
        "title": "Dolly-Zoom (Contrazoom) Background Expansion Behind Locked Person Cutout",
        "duration": 1.4,
        "sfx": "@asset/audio/sfx/whoosh.wav",
        "requires_cutout": True,
        "top_zone": False,
        "default_vars": {
            "bgStartScale": 1.0,
            "bgEndScale": 1.38,
            "fgScale": 1.02,
            "cutoutHandle": "@project/cutout/vertigo_cutout.mov"
        },
        "body_html": """
      <div class="vertigo-bg" id="vbg">
        <div class="persp-grid"></div>
      </div>
      <div class="vertigo-badge" id="vbdg">03 vertigo · dolly zoom</div>""",
        "extra_css": """
      .vertigo-bg { position: absolute; inset: -15%; border: 3px solid rgba(246,228,120,0.18); display: flex; align-items: center; justify-content: center; }
      .persp-grid { width: 80%; height: 80%; border: 4px dashed rgba(255,255,255,0.16); border-radius: 32px; }
      .vertigo-badge { position: absolute; bottom: 10%; padding: 16px 36px; border-radius: 999px; background: rgba(18,18,20,0.78); color: #F6E478; font-size: 36px; font-weight: 800; opacity: 0; }
""",
        "gsap_js": """
      tl.fromTo('#vbg', { scale: vars.bgStartScale }, { scale: vars.bgEndScale, duration: 1.2, ease: 'sine.inOut' }, 0.0)
        .fromTo('#vbdg', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.25, ease: 'power2.out' }, 0.1);
"""
    },
    {
        "slug": "green-screen",
        "shortcut": "@green-screen",
        "rule": "Rule TH31",
        "title": "Person-Cutout Background Replacement + Flash Wipe",
        "duration": 2.0,
        "sfx": "@asset/audio/sfx/whoosh.wav",
        "requires_cutout": True,
        "top_zone": False,
        "default_vars": {
            "backgroundVideo": "@asset/video/memes/bg_replacement.mp4",
            "cutoutHandle": "@project/cutout/greenscreen_cutout.mov",
            "vignetteOpacity": 0.45
        },
        "body_html": """
      <div class="gs-wipe" id="gsw">
        <div class="gs-label">GREEN SCREEN PLATE · @asset/video/backgrounds/</div>
      </div>
      <div class="gs-flash" id="gsf"></div>""",
        "extra_css": """
      .gs-wipe { position: absolute; inset: 0; background: linear-gradient(160deg, #1E293B 0%, #0F172A 100%); display: flex; align-items: center; justify-content: center; clip-path: inset(0 100% 0 0); }
      .gs-label { font-size: 42px; font-weight: 800; color: rgba(255,255,255,0.35); letter-spacing: 0.08em; }
      .gs-flash { position: absolute; inset: 0; background: #FFFFFF; opacity: 0; pointer-events: none; }
""",
        "gsap_js": """
      tl.to('#gsf', { opacity: 0.75, duration: 0.08 }, 0.0)
        .to('#gsw', { clipPath: 'inset(0 0% 0 0)', duration: 0.24, ease: 'power3.out' }, 0.04)
        .to('#gsf', { opacity: 0, duration: 0.18 }, 0.10);
"""
    },
    {
        "slug": "phone-mockup",
        "shortcut": "@phone-mockup",
        "rule": "Rule TH32",
        "title": "3D Tilted iPhone Mockup Slide-In + Scrolling Screen Capture",
        "duration": 2.4,
        "sfx": "@asset/audio/sfx/whoosh.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "deviceFrame": "@asset/mockups/devices/iphone_16_pro_frame.svg",
            "screenAsset": "@asset/photo/screenshots/app_feed.png",
            "headline": "YOU FILM.\nCLAUDE EDITS.",
            "xPercent": 20.0,
            "yPercent": 50.0
        },
        "body_html": """
      <div class="phone-stage">
        <div class="phone-card" id="ph">
          <div class="island"></div>
          <div class="screen-Viewport">
            <div class="screen-scroll" id="scr">
              <div class="poster-block">
                <div class="poster-title">YOU FILM.<br/>CLAUDE EDITS.</div>
                <div class="poster-cta">TRY IT NOW</div>
              </div>
              <div class="article-block">
                <div class="art-h">Automated 4K Timeline</div>
                <div class="art-p">Every pause, jump cut, and motion graphic synced to 10ms RMS onset.</div>
              </div>
            </div>
          </div>
        </div>
      </div>""",
        "extra_css": """
      .phone-stage { position: absolute; left: 5%; top: 30%; width: 38%; height: 46%; perspective: 1400px; }
      .phone-card { width: 100%; height: 100%; background: #141417; border: 12px solid #3F3F46; border-radius: 72px; padding: 22px; box-shadow: 0 36px 80px rgba(0,0,0,0.75); position: relative; overflow: hidden; opacity: 0; }
      .island { width: 34%; height: 34px; background: #000; border-radius: 20px; margin: 8px auto 18px; }
      .screen-Viewport { width: 100%; height: 88%; border-radius: 48px; overflow: hidden; background: #0B0C10; }
      .screen-scroll { display: flex; flex-direction: column; gap: 28px; padding: 28px; }
      .poster-block { background: linear-gradient(145deg, #7C2D12, #090A0F); border-radius: 32px; padding: 44px 28px; color: #FFF; }
      .poster-title { font-size: 54px; font-weight: 900; line-height: 1.02; margin-bottom: 28px; }
      .poster-cta { display: inline-block; background: #EA580C; padding: 14px 26px; border-radius: 16px; font-size: 24px; font-weight: 800; }
      .article-block { background: #F8FAFC; color: #0F172A; border-radius: 32px; padding: 36px 28px; }
      .art-h { font-size: 40px; font-weight: 800; margin-bottom: 12px; }
      .art-p { font-size: 28px; line-height: 1.35; color: #334155; }
""",
        "gsap_js": """
      tl.fromTo('#ph', { opacity: 0, x: -160, rotateY: 28, rotateZ: -8, scale: 0.86 }, { opacity: 1, x: 0, rotateY: 14, rotateZ: -4, scale: 1, duration: 0.42, ease: 'back.out(1.4)' }, 0.0)
        .to('#scr', { y: -260, duration: 1.4, ease: 'power2.inOut' }, 0.55);
"""
    },
    {
        "slug": "digital-zoom",
        "shortcut": "@digital-zoom",
        "rule": "Rule TH33",
        "title": "Camera Viewfinder HUD & Focal-Length Lens Ring (Camcorder | Lens-Ring Styles)",
        "duration": 2.0,
        "sfx": "@asset/audio/sfx/timeline_tick.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "style": "camcorder",
            "startZoom": 1.00,
            "endZoom": 1.30,
            "focalLengths": [85, 70, 50, 35, 24]
        },
        "body_html": """
      <div class="cam-hud" id="cam">
        <div class="face-box" id="fbox">
          <span class="c tl"></span><span class="c tr"></span><span class="c bl"></span><span class="c br"></span>
        </div>
        <div class="hud-bottom">
          <div class="rec"><span class="dot"></span> REC <span class="tc">00:00:08:14</span></div>
          <div class="ruler">I · · · · I · · · · I · · · · I</div>
          <div class="zval" id="zv">1.30×</div>
        </div>
        <div class="lens-bar" id="lbar">
          <div class="ticks" id="lticks"><span>85</span><span>70</span><span>50</span><span>35</span><span class="gold">24</span></div>
        </div>
      </div>""",
        "extra_css": """
      .cam-hud { position: absolute; inset: 0; pointer-events: none; }
      .face-box { position: absolute; left: 26%; top: 20%; width: 48%; height: 34%; }
      .c { position: absolute; width: 44px; height: 44px; border-color: rgba(255,255,255,0.9); border-style: solid; }
      .tl { top: 0; left: 0; border-width: 5px 0 0 5px; }
      .tr { top: 0; right: 0; border-width: 5px 5px 0 0; }
      .bl { bottom: 0; left: 0; border-width: 0 0 5px 5px; }
      .br { bottom: 0; right: 0; border-width: 0 5px 5px 0; }
      .hud-bottom { position: absolute; left: 6%; right: 6%; bottom: 28%; display: flex; justify-content: space-between; align-items: center; font-family: 'SF Mono', Menlo, monospace; font-size: 32px; color: #FFFFFF; text-shadow: 0 4px 12px rgba(0,0,0,0.8); }
      .rec { display: flex; align-items: center; gap: 12px; font-weight: 700; }
      .dot { width: 22px; height: 22px; border-radius: 50%; background: #EF4444; display: inline-block; }
      .ruler { opacity: 0.65; letter-spacing: 0.14em; }
      .zval { font-size: 44px; font-weight: 800; color: #F6E478; }
      .lens-bar { position: absolute; top: 14%; left: 4%; width: 58%; background: rgba(18, 48, 36, 0.92); border: 2px solid #2A5240; border-radius: 20px; padding: 24px 32px; overflow: hidden; opacity: 0; }
      .ticks { display: flex; gap: 72px; font-size: 40px; font-weight: 700; color: #F0EADE; }
      .ticks .gold { color: #C6A254; font-weight: 900; }
""",
        "gsap_js": """
      tl.fromTo('#fbox', { opacity: 0, scale: 1.18 }, { opacity: 1, scale: 1, duration: 0.3, ease: 'power3.out' }, 0.0)
        .fromTo('#zv', { opacity: 0.5, scale: 0.9 }, { opacity: 1, scale: 1, duration: 0.4, ease: 'power2.out' }, 0.1)
        .fromTo('#lticks', { x: 0 }, { x: -120, duration: 1.2, ease: 'power2.inOut' }, 0.1);
"""
    },
    {
        "slug": "paper-cut",
        "shortcut": "@paper-cut",
        "rule": "Rule TH34",
        "title": "Stop-Motion Torn-Paper Cutout + Ransom-Note Letters + Vertical Tear Exit",
        "duration": 2.0,
        "sfx": "@asset/audio/sfx/paper_thock.wav",
        "requires_cutout": True,
        "top_zone": False,
        "default_vars": {
            "word1": "PAPER",
            "word2": "CUT",
            "cutoutHandle": "@project/cutout/papercut_cutout.mov",
            "gridTexture": "@asset/photo/textures/notebook_grid_paper.svg"
        },
        "body_html": """
      <div class="ransom-wrap" id="rw">
        <div class="ransom-row">
          <span class="chip c1" id="l1">P</span><span class="chip c2" id="l2">A</span><span class="chip c3" id="l3">P</span><span class="chip c4" id="l4">e</span><span class="chip c5" id="l5">r</span>
        </div>
        <div class="ransom-row">
          <span class="chip c6" id="l6">c</span><span class="chip c7" id="l7">u</span><span class="chip c8" id="l8">t</span>
        </div>
      </div>""",
        "extra_css": """
      .ransom-wrap { position: absolute; top: 44%; left: 16%; right: 16%; display: flex; flex-direction: column; align-items: center; gap: 22px; }
      .ransom-row { display: flex; gap: 14px; }
      .chip { display: inline-flex; align-items: center; justify-content: center; width: 108px; height: 124px; font-size: 86px; font-weight: 900; box-shadow: 0 12px 26px rgba(0,0,0,0.55); opacity: 0; }
      .c1 { background: #F0EADE; color: #1E293B; transform: rotate(-5deg); font-family: Georgia, serif; }
      .c2 { background: #2563EB; color: #FFFFFF; transform: rotate(4deg); }
      .c3 { background: #141413; color: #F6E478; transform: rotate(-3deg); }
      .c4 { background: #F6E478; color: #141413; transform: rotate(6deg); font-family: Georgia, serif; }
      .c5 { background: #F0EADE; color: #DC2626; transform: rotate(-4deg); }
      .c6 { background: #F0EADE; color: #141413; transform: rotate(4deg); }
      .c7 { background: #141413; color: #FFFFFF; transform: rotate(-5deg); font-family: Georgia, serif; }
      .c8 { background: #2563EB; color: #FFFFFF; transform: rotate(3deg); }
""",
        "gsap_js": """
      tl.to('.chip', { opacity: 1, scale: 1, duration: 0.08, stagger: 0.06, ease: 'back.out(2.0)' }, 0.05);
"""
    },
    {
        "slug": "ui-world",
        "shortcut": "@ui-world",
        "rule": "Rule TH35",
        "title": "Floating 3D Glassmorphism Editor HUD (Prompt + Timeline + Live Preview)",
        "duration": 2.4,
        "sfx": "@asset/audio/sfx/click.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "promptText": "edit my reel",
            "previewLabel": "doodle boil"
        },
        "body_html": """
      <div class="ui-card ui-prompt" id="up">
        <div class="ui-kicker">PROMPT <span class="send-dot">↑</span></div>
        <div class="ui-input">edit my reel<span class="caret">|</span></div>
        <div class="ui-prog-row"><span>editing...</span><span class="pct" id="upct">100% ✓</span></div>
        <div class="ui-bar"><div class="ui-fill" id="ufill"></div></div>
      </div>
      <div class="ui-card ui-tl" id="utl">
        <div class="ui-kicker">TIMELINE <span>reel_v2.mp4</span></div>
        <div class="ui-strip">
          <div class="th"></div><div class="th"></div><div class="th"></div><div class="th"></div><div class="th"></div>
          <div class="playhead" id="uph"></div>
        </div>
      </div>
      <div class="ui-card ui-prev" id="upr">
        <div class="ui-kicker">PREVIEW <span class="live">● LIVE</span></div>
        <div class="prev-box">doodle boil</div>
      </div>""",
        "extra_css": """
      .ui-card { position: absolute; background: rgba(16, 18, 22, 0.84); border: 2px solid rgba(255,255,255,0.16); border-radius: 28px; padding: 26px 32px; color: #FFFFFF; box-shadow: 0 28px 64px rgba(0,0,0,0.7); opacity: 0; }
      .ui-kicker { font-size: 20px; font-weight: 800; letter-spacing: 0.1em; color: rgba(255,255,255,0.55); display: flex; justify-content: space-between; margin-bottom: 14px; }
      .send-dot { background: #F6E478; color: #141413; width: 32px; height: 32px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; }
      .ui-prompt { top: 28%; left: 4%; width: 38%; }
      .ui-input { font-size: 40px; font-weight: 800; margin-bottom: 18px; }
      .caret { color: #F6E478; }
      .ui-prog-row { display: flex; justify-content: space-between; font-size: 24px; color: #F6E478; margin-bottom: 8px; font-weight: 700; }
      .ui-bar { height: 10px; background: rgba(255,255,255,0.14); border-radius: 99px; overflow: hidden; }
      .ui-fill { height: 100%; width: 100%; background: #F6E478; transform-origin: left center; transform: scaleX(0); }
      .ui-tl { top: 48%; left: 4%; width: 52%; }
      .ui-strip { position: relative; display: flex; gap: 10px; height: 84px; }
      .th { flex: 1; background: rgba(255,255,255,0.12); border-radius: 12px; }
      .playhead { position: absolute; top: -8px; bottom: -8px; left: 0; width: 4px; background: #F6E478; }
      .ui-prev { top: 38%; right: 4%; width: 36%; }
      .live { color: #4ADE80; }
      .prev-box { height: 260px; border-radius: 18px; background: linear-gradient(145deg, #1E293B, #0F172A); display: flex; align-items: flex-end; justify-content: center; padding: 20px; font-size: 38px; font-weight: 900; color: #F6E478; }
""",
        "gsap_js": """
      tl.fromTo('#up', { opacity: 0, x: -60, y: 20 }, { opacity: 1, x: 0, y: 0, duration: 0.3, ease: 'power3.out' }, 0.0)
        .fromTo('#utl', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.3, ease: 'power3.out' }, 0.10)
        .fromTo('#upr', { opacity: 0, x: 60 }, { opacity: 1, x: 0, duration: 0.3, ease: 'power3.out' }, 0.16)
        .to('#ufill', { scaleX: 1, duration: 0.9, ease: 'power2.inOut' }, 0.25)
        .fromTo('#uph', { x: 40 }, { x: 460, duration: 1.2, ease: 'none' }, 0.25);
"""
    },
    {
        "slug": "orbit",
        "shortcut": "@orbit",
        "rule": "Rule TH36",
        "title": "3D Carousel Ring of Vertical Reel Cards Orbiting Around Speaker Cutout",
        "duration": 2.2,
        "sfx": "@asset/audio/sfx/whoosh.wav",
        "requires_cutout": True,
        "top_zone": False,
        "default_vars": {
            "reelCards": ["@asset/video/reels/reel_01.mp4", "@asset/video/reels/reel_02.mp4", "@asset/video/reels/reel_03.mp4", "@asset/video/reels/reel_04.mp4"],
            "cutoutHandle": "@project/cutout/orbit_cutout.mov",
            "radiusPx": 420
        },
        "body_html": """
      <div class="orbit-scene">
        <div class="orbit-ring" id="oring">
          <div class="ocard oc1">ui world</div>
          <div class="ocard oc2">frame break</div>
          <div class="ocard oc3">doodle boil</div>
          <div class="ocard oc4">paper cut</div>
        </div>
      </div>""",
        "extra_css": """
      .orbit-scene { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; perspective: 1400px; }
      .orbit-ring { width: 680px; height: 420px; position: relative; transform-style: preserve-3d; }
      .ocard { position: absolute; left: 200px; top: 20px; width: 260px; height: 420px; border-radius: 28px; background: linear-gradient(160deg, #1E293B, #090D16); border: 4px solid rgba(255,255,255,0.28); box-shadow: 0 24px 60px rgba(0,0,0,0.75); display: flex; align-items: flex-end; justify-content: center; padding: 24px; font-size: 34px; font-weight: 900; color: #F6E478; }
      .oc1 { transform: rotateY(0deg) translateZ(380px); }
      .oc2 { transform: rotateY(90deg) translateZ(380px); }
      .oc3 { transform: rotateY(180deg) translateZ(380px); }
      .oc4 { transform: rotateY(270deg) translateZ(380px); }
""",
        "gsap_js": """
      tl.fromTo('#oring', { rotationY: -35, rotationX: -6 }, { rotationY: 145, rotationX: -6, duration: 2.0, ease: 'power2.inOut' }, 0.0);
"""
    },
    {
        "slug": "frame-break",
        "shortcut": "@frame-break",
        "rule": "Rule TH37",
        "title": "Instagram Reel Card Pull-Back + 3D Glass Shard Shatter",
        "duration": 2.0,
        "sfx": "@asset/audio/sfx/sub_drop.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "handle": "tenfoldmarc",
            "caption": "16 video effects claude can create"
        },
        "body_html": """
      <div class="shard s1" id="sh1"></div>
      <div class="shard s2" id="sh2"></div>
      <div class="shard s3" id="sh3"></div>
      <div class="shard s4" id="sh4"></div>
      <div class="reel-frame" id="rf">
        <div class="reel-top">Reels</div>
        <div class="reel-icons"><span>♡</span><span>💬</span><span>⌲</span></div>
        <div class="reel-meta">
          <div class="handle">@tenfoldmarc · <span class="fbtn">Follow</span></div>
          <div class="rcap">16 video effects claude can create</div>
        </div>
      </div>""",
        "extra_css": """
      .reel-frame { position: absolute; width: 64%; height: 64%; top: 20%; left: 18%; border-radius: 38px; border: 3px solid rgba(255,255,255,0.28); box-shadow: 0 36px 90px rgba(0,0,0,0.85); padding: 32px; display: flex; flex-direction: column; justify-content: space-between; background: rgba(15, 23, 42, 0.35); }
      .reel-top { font-size: 34px; font-weight: 800; }
      .reel-icons { position: absolute; right: 28px; bottom: 140px; display: flex; flex-direction: column; gap: 26px; font-size: 44px; }
      .reel-meta { display: flex; flex-direction: column; gap: 10px; }
      .handle { font-size: 28px; font-weight: 700; }
      .fbtn { border: 2px solid #FFF; border-radius: 10px; padding: 2px 12px; margin-left: 8px; font-size: 22px; }
      .rcap { font-size: 24px; color: rgba(255,255,255,0.75); }
      .shard { position: absolute; width: 220px; height: 280px; background: linear-gradient(135deg, rgba(255,255,255,0.32), rgba(255,255,255,0.04)); clip-path: polygon(10% 0%, 100% 25%, 75% 100%, 0% 80%); opacity: 0; }
      .s1 { top: 6%; left: 8%; } .s2 { top: 8%; right: 8%; } .s3 { bottom: 10%; left: 10%; } .s4 { bottom: 12%; right: 10%; }
""",
        "gsap_js": """
      tl.fromTo('#rf', { scale: 1.35, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.32, ease: 'power3.out' }, 0.0)
        .fromTo('#sh1', { opacity: 0.9, x: 120, y: 120, rotation: 0 }, { opacity: 0, x: -180, y: -220, rotation: -45, duration: 0.7, ease: 'power3.out' }, 0.25)
        .fromTo('#sh2', { opacity: 0.9, x: -120, y: 120, rotation: 0 }, { opacity: 0, x: 180, y: -220, rotation: 50, duration: 0.7, ease: 'power3.out' }, 0.25)
        .fromTo('#sh3', { opacity: 0.9, x: 120, y: -120, rotation: 0 }, { opacity: 0, x: -180, y: 220, rotation: -35, duration: 0.7, ease: 'power3.out' }, 0.28)
        .fromTo('#sh4', { opacity: 0.9, x: -120, y: -120, rotation: 0 }, { opacity: 0, x: 180, y: 220, rotation: 40, duration: 0.7, ease: 'power3.out' }, 0.28);
"""
    },
    {
        "slug": "doodle-boil",
        "shortcut": "@doodle-boil",
        "rule": "Rule TH38",
        "title": "Hand-Drawn Neon Chalk Outline + Boiling Stop-Motion Spark Bursts",
        "duration": 2.0,
        "sfx": "@asset/audio/sfx/marker_squeak.wav",
        "requires_cutout": True,
        "top_zone": False,
        "default_vars": {
            "colors": ["#FFFFFF", "#F6E478", "#FF7EB6", "#38BDF8"],
            "boilFps": 12
        },
        "body_html": """
      <svg class="doodle-svg" id="dsvg" viewBox="0 0 1080 1920">
        <path id="dp1" d="M 140 820 Q 260 720 340 520 Q 380 280 540 270 Q 700 280 740 520 Q 820 720 940 820" fill="none" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" stroke-dasharray="1800" stroke-dashoffset="1800"/>
        <path id="dp2" d="M 155 800 Q 275 700 355 505 Q 395 265 540 255 Q 685 265 725 505 Q 805 700 925 800" fill="none" stroke="#F6E478" stroke-width="8" stroke-linecap="round" stroke-dasharray="1800" stroke-dashoffset="1800"/>
        <circle class="sp" cx="460" cy="1080" r="34" fill="none" stroke="#F6E478" stroke-width="8"/>
        <circle class="sp" cx="550" cy="1050" r="46" fill="none" stroke="#FF7EB6" stroke-width="8"/>
        <circle class="sp" cx="630" cy="1110" r="28" fill="none" stroke="#38BDF8" stroke-width="8"/>
      </svg>""",
        "extra_css": """
      .doodle-svg { position: absolute; inset: 0; width: 100%; height: 100%; }
      .sp { opacity: 0; transform-origin: center; }
""",
        "gsap_js": """
      tl.to('#dp1, #dp2', { strokeDashoffset: 0, duration: 0.45, stagger: 0.08, ease: 'power2.out' }, 0.0)
        .fromTo('.sp', { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1.15, duration: 0.25, stagger: 0.08, yoyo: true, repeat: 3, ease: 'steps(3)' }, 0.35)
        .to('#dsvg', { x: 4, y: -3, rotation: 0.6, duration: 1/vars.boilFps, yoyo: true, repeat: 12, ease: 'steps(2)' }, 0.2);
"""
    },
    {
        "slug": "sticky-text",
        "shortcut": "@sticky-text",
        "rule": "Rule TH39",
        "title": "HUD List Detach -> Tilted Yellow Adhesive Sticker Slap",
        "duration": 2.0,
        "sfx": "@asset/audio/sfx/pop.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "number": "12",
            "label": "sticky text",
            "tiltDeg": -5.5
        },
        "body_html": """
      <div class="sticky-pill" id="st">
        <span class="st-num">12</span>
        <span class="st-txt">sticky text</span>
      </div>""",
        "extra_css": """
      .sticky-pill { position: absolute; top: 58%; left: 48%; background: #F6E478; color: #141413; padding: 22px 42px; border-radius: 22px; font-size: 56px; font-weight: 900; box-shadow: 0 22px 48px rgba(0,0,0,0.65); display: inline-flex; align-items: center; gap: 18px; opacity: 0; }
      .st-num { font-size: 38px; font-weight: 700; opacity: 0.65; }
""",
        "gsap_js": """
      tl.fromTo('#st', { opacity: 0, x: 140, y: -520, scale: 0.45, rotation: 18 }, { opacity: 1, x: 0, y: 0, scale: 1, rotation: vars.tiltDeg, duration: 0.38, ease: 'back.out(1.7)' }, 0.0)
        .to('#st', { rotation: -3.5, duration: 0.18, yoyo: true, repeat: 3, ease: 'sine.inOut' }, 0.42);
"""
    },
    {
        "slug": "before-after",
        "shortcut": "@before-after",
        "rule": "Rule TH40",
        "title": "Vertical Light-Leak Split Wipe + Before/After Frosted Badges",
        "duration": 2.0,
        "sfx": "@asset/audio/sfx/whoosh.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "leftLabel": "before",
            "rightLabel": "• after",
            "beamColor": "#FFF7D6"
        },
        "body_html": """
      <div class="ba-pill ba-left" id="bal">before</div>
      <div class="ba-pill ba-right" id="bar">• after</div>
      <div class="ba-beam" id="beam"></div>""",
        "extra_css": """
      .ba-pill { position: absolute; top: 56%; padding: 14px 32px; border-radius: 999px; background: rgba(20,20,22,0.72); border: 2px solid rgba(255,255,255,0.22); color: #FFFFFF; font-size: 34px; font-weight: 700; opacity: 0; }
      .ba-left { left: 8%; }
      .ba-right { right: 8%; color: #F6E478; }
      .ba-beam { position: absolute; top: 0; bottom: 0; left: 0; width: 14px; background: #FFFDF5; box-shadow: 0 0 48px 24px rgba(246, 228, 120, 0.85), 0 0 110px 48px rgba(255, 255, 255, 0.55); }
""",
        "gsap_js": """
      tl.to('#bal', { opacity: 1, duration: 0.2 }, 0.05)
        .fromTo('#beam', { x: 40 }, { x: 1020, duration: 1.35, ease: 'power2.inOut' }, 0.1)
        .to('#bar', { opacity: 1, duration: 0.25 }, 0.65);
"""
    },
    {
        "slug": "pull-back",
        "shortcut": "@pull-back",
        "rule": "Rule TH41",
        "title": "3D Perspective Pull-Back into NLE Editor Window + Checklist + Waveform",
        "duration": 2.4,
        "sfx": "@asset/audio/sfx/whoosh.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "windowTitle": "effects reel",
            "checklist": ["cut pauses", "add effects", "export"]
        },
        "body_html": """
      <div class="nle-stage">
        <div class="nle-win" id="nwin">
          <div class="nle-top">effects reel · 00:16.42</div>
          <div class="nle-mid">
            <div class="nle-side">
              <div class="side-h">checklist · claude</div>
              <div class="chk" id="ck1">✓ cut pauses</div>
              <div class="chk" id="ck2">✓ add effects</div>
              <div class="chk" id="ck3">✓ export</div>
            </div>
            <div class="nle-canvas">LIVE VIDEO VIEWPORT</div>
            <div class="nle-side">
              <div class="side-h">effects</div>
              <div class="fx-row">14 pull-back reveal</div>
              <div class="fx-row">15 depth scatter</div>
            </div>
          </div>
          <div class="nle-tracks">
            <div class="t-clips"><span class="c- p"></span><span class="c- b"></span><span class="c- y"></span><span class="c- g"></span><span class="c- p"></span></div>
            <div class="t-wave">▂▄▆█▄▂▁▃▆█▅▂▄▇█▃▁▂▆█▄▂▁▃▆█▅▂</div>
          </div>
        </div>
      </div>""",
        "extra_css": """
      .nle-stage { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; perspective: 1400px; }
      .nle-win { width: 92%; height: 78%; background: #0B0D12; border: 3px solid rgba(255,255,255,0.18); border-radius: 32px; padding: 28px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 40px 100px rgba(0,0,0,0.85); }
      .nle-top { text-align: center; font-size: 28px; font-weight: 700; color: rgba(255,255,255,0.65); }
      .nle-mid { display: flex; gap: 20px; height: 68%; }
      .nle-side { width: 24%; background: rgba(255,255,255,0.05); border-radius: 20px; padding: 20px; display: flex; flex-direction: column; gap: 16px; }
      .side-h { font-size: 22px; color: rgba(255,255,255,0.5); font-weight: 700; text-transform: uppercase; }
      .chk { font-size: 26px; font-weight: 700; color: #4ADE80; opacity: 0.35; }
      .fx-row { font-size: 24px; color: #F6E478; font-weight: 700; }
      .nle-canvas { flex: 1; border-radius: 24px; border: 2px solid rgba(255,255,255,0.15); display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 800; color: rgba(255,255,255,0.35); }
      .nle-tracks { background: rgba(255,255,255,0.04); border-radius: 20px; padding: 18px; display: flex; flex-direction: column; gap: 12px; }
      .t-clips { display: flex; gap: 8px; height: 36px; }
      .c- { flex: 1; border-radius: 8px; }
      .p { background: #A855F7; } .b { background: #38BDF8; } .y { background: #FACC15; } .g { background: #4ADE80; }
      .t-wave { font-family: monospace; font-size: 32px; color: #4ADE80; letter-spacing: 0.08em; overflow: hidden; white-space: nowrap; }
""",
        "gsap_js": """
      tl.fromTo('#nwin', { scale: 1.75, rotationX: 0, rotationY: 0 }, { scale: 1, rotationX: 8, rotationY: -10, duration: 0.55, ease: 'power3.out' }, 0.0)
        .to('#ck1, #ck2, #ck3', { opacity: 1, duration: 0.2, stagger: 0.22 }, 0.45);
"""
    },
    {
        "slug": "depth-scatter",
        "shortcut": "@depth-scatter",
        "rule": "Rule TH42",
        "title": "Multi-Plane 3D Z-Depth Letter Scatter + Rack-Focus Blur (Behind & In Front of Head)",
        "duration": 2.2,
        "sfx": "@asset/audio/sfx/whoosh.wav",
        "requires_cutout": True,
        "top_zone": True,
        "default_vars": {
            "wordBehind": "depth",
            "wordFront": "scatter",
            "cutoutHandle": "@project/cutout/depth_scatter_cutout.mov"
        },
        "body_html": """
      <div class="ds-behind" id="dsb">
        <span class="dl">d</span><span class="dl">e</span><span class="dl">p</span><span class="dl">t</span><span class="dl">h</span>
      </div>
      <div class="ds-front" id="dsf">
        <span class="fl">s</span><span class="fl">c</span><span class="fl">a</span><span class="fl">t</span><span class="fl">t</span><span class="fl">e</span><span class="fl">r</span>
      </div>""",
        "extra_css": """
      .ds-behind { position: absolute; top: 24%; left: 0; right: 0; display: flex; justify-content: center; gap: 6px; font-size: 210px; font-weight: 900; color: #FFFFFF; letter-spacing: -0.04em; text-shadow: 0 18px 48px rgba(0,0,0,0.75); }
      .ds-front { position: absolute; top: 44%; left: 0; right: 0; display: flex; justify-content: center; gap: 4px; font-size: 196px; font-weight: 900; color: #F6E478; letter-spacing: -0.04em; text-shadow: 0 0 42px rgba(246,228,120,0.45), 0 18px 48px rgba(0,0,0,0.85); }
      .dl, .fl { display: inline-block; }
""",
        "gsap_js": """
      tl.fromTo('.dl', { opacity: 0, scale: 1.8, y: -90, filter: 'blur(20px)' }, { opacity: 1, scale: 1, y: 0, filter: 'blur(0px)', duration: 0.38, stagger: 0.04, ease: 'power3.out' }, 0.0)
        .fromTo('.fl', { opacity: 0, scale: 0.4, y: 110, filter: 'blur(22px)' }, { opacity: 1, scale: 1, y: 0, filter: 'blur(0px)', duration: 0.42, stagger: 0.04, ease: 'back.out(1.5)' }, 0.18);
"""
    },
    {
        "slug": "reel-grid",
        "shortcut": "@reel-grid",
        "rule": "Rule TH43",
        "title": "Unified Multi-Reel Grid (background | collapse | playing | cascade Modes)",
        "duration": 2.4,
        "sfx": "@asset/audio/sfx/pop.wav",
        "requires_cutout": False,
        "top_zone": True,
        "default_vars": {
            "mode": "cascade",
            "reelAssets": [],
            "thumbAssets": [],
            "columns": 4,
            "rows": 2
        },
        "body_html": """
      <div class="rg-wrap" id="rg">
        <div class="rg-card">01</div><div class="rg-card">02</div><div class="rg-card">03</div><div class="rg-card">04</div>
        <div class="rg-card">05</div><div class="rg-card">06</div><div class="rg-card">07</div><div class="rg-card">08</div>
      </div>""",
        "extra_css": """
      .rg-wrap { position: absolute; top: 12%; left: 5%; width: 58%; display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
      .rg-card { aspect-ratio: 9/16; border-radius: 20px; background: linear-gradient(155deg, #1E3A2F, #0F172A); border: 3px solid rgba(240,234,222,0.35); box-shadow: 0 18px 40px rgba(0,0,0,0.65); display: flex; align-items: flex-end; justify-content: center; padding: 14px; font-size: 28px; font-weight: 800; color: #F0EADE; opacity: 0; }
""",
        "gsap_js": """
      tl.fromTo('.rg-card', { opacity: 0, y: 48, scale: 0.82 }, { opacity: 1, y: 0, scale: 1, duration: 0.28, stagger: 0.06, ease: 'back.out(1.5)' }, 0.0);
"""
    },
    {
        "slug": "comment-bubble",
        "shortcut": "@comment-bubble",
        "rule": "Rule TH44",
        "title": "Automated Social CTA Comment-to-DM Funnel (Input -> Heart Bubble -> Link Reply)",
        "duration": 2.8,
        "sfx": "@asset/audio/sfx/click.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "keyword": "STUDIO",
            "replyText": "Sent you the link",
            "buttonText": "🔗 Open link"
        },
        "body_html": """
      <div class="cb-input" id="cbi">
        <div class="cb-av"></div>
        <div class="cb-typed" id="cbt">STUDIO</div>
        <div class="cb-send">↑</div>
      </div>
      <div class="cb-stack" id="cbs">
        <div class="cb-user">
          <span class="cb-you">you</span> <b>STUDIO</b>
          <span class="cb-heart">❤️</span>
        </div>
        <div class="cb-reply" id="cbr">
          <div class="cb-rep-txt">Sent you the link</div>
          <div class="cb-btn">🔗 Open link</div>
        </div>
      </div>""",
        "extra_css": """
      .cb-input { position: absolute; bottom: 16%; left: 10%; right: 10%; background: rgba(18,18,22,0.92); border: 3px solid #F6E478; border-radius: 999px; padding: 20px 28px; display: flex; align-items: center; gap: 20px; box-shadow: 0 24px 60px rgba(0,0,0,0.75); }
      .cb-av { width: 56px; height: 56px; border-radius: 50%; background: #475569; }
      .cb-typed { flex: 1; font-size: 44px; font-weight: 800; color: #FFFFFF; }
      .cb-send { width: 64px; height: 64px; border-radius: 50%; background: #F6E478; color: #141413; display: flex; align-items: center; justify-content: center; font-size: 38px; font-weight: 900; }
      .cb-stack { position: absolute; bottom: 14%; left: 16%; right: 16%; display: flex; flex-direction: column; align-items: center; gap: 18px; opacity: 0; }
      .cb-user { position: relative; background: #FFFFFF; color: #141413; padding: 22px 44px; border-radius: 999px; font-size: 48px; box-shadow: 0 20px 48px rgba(0,0,0,0.65); }
      .cb-you { color: #64748B; font-size: 34px; margin-right: 10px; }
      .cb-heart { position: absolute; top: -18px; right: -14px; background: #FFF; border-radius: 50%; padding: 6px 10px; font-size: 30px; box-shadow: 0 6px 16px rgba(0,0,0,0.3); }
      .cb-reply { background: rgba(18,18,22,0.94); border: 2px solid rgba(255,255,255,0.18); border-radius: 36px; padding: 28px 42px; display: flex; flex-direction: column; gap: 16px; align-items: flex-start; opacity: 0; }
      .cb-rep-txt { font-size: 36px; font-weight: 700; color: #FFFFFF; }
      .cb-btn { background: #F6E478; color: #141413; padding: 14px 32px; border-radius: 999px; font-size: 32px; font-weight: 800; }
""",
        "gsap_js": """
      tl.fromTo('#cbi', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.28, ease: 'power3.out' }, 0.0)
        .to('#cbi', { opacity: 0, scale: 0.88, duration: 0.18 }, 0.95)
        .fromTo('#cbs', { opacity: 0, scale: 0.85, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.28, ease: 'back.out(1.6)' }, 1.05)
        .fromTo('#cbr', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.28, ease: 'power3.out' }, 1.45);
"""
    },
    {
        "slug": "knockout-captions",
        "shortcut": "@knockout-captions",
        "rule": "Rule TH45",
        "title": "Editorial Cream Card with Knocked-Out Transparent Stencil Display Type",
        "duration": 1.8,
        "sfx": "@asset/audio/sfx/sub_drop.wav",
        "requires_cutout": False,
        "top_zone": True,
        "default_vars": {
            "pillText": "knockout",
            "subText": "captions.",
            "stencilLine1": "KNOCK",
            "stencilLine2": "OUT"
        },
        "body_html": """
      <div class="ko-intro" id="koi">
        <div class="ko-pill">knockout</div>
        <div class="ko-sub">captions.</div>
      </div>
      <div class="ko-card" id="koc">
        <div class="ko-header">captions.</div>
        <div class="ko-big">KNOCK<br/>OUT</div>
      </div>""",
        "extra_css": """
      .ko-intro { position: absolute; top: 26%; left: 10%; width: 48%; display: flex; flex-direction: column; align-items: center; gap: 14px; }
      .ko-pill { background: #123024; border: 2px solid #2A5240; color: #F0EADE; padding: 14px 36px; border-radius: 16px; font-size: 48px; font-family: Georgia, serif; }
      .ko-sub { background: #123024; color: #F0EADE; padding: 14px 42px; border-radius: 16px; font-size: 64px; font-family: Georgia, serif; }
      .ko-card { position: absolute; top: 10%; left: 4%; width: 60%; background: #F0EADE; color: #121414; padding: 38px 32px; border-radius: 12px; text-align: center; opacity: 0; mix-blend-mode: screen; }
      .ko-header { font-family: Georgia, serif; font-style: italic; font-size: 56px; margin-bottom: 12px; }
      .ko-big { font-family: Georgia, 'Times New Roman', serif; font-size: 168px; font-weight: 900; line-height: 0.92; letter-spacing: -0.04em; color: #000000; }
""",
        "gsap_js": """
      tl.fromTo('#koi', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.22, ease: 'power3.out' }, 0.0)
        .to('#koi', { opacity: 0, duration: 0.1 }, 0.50)
        .fromTo('#koc', { opacity: 0, scale: 1.18 }, { opacity: 1, scale: 1, duration: 0.22, ease: 'power4.out' }, 0.52);
"""
    },
    {
        "slug": "live-markup",
        "shortcut": "@live-markup",
        "rule": "Rule TH46",
        "title": "Self-Tracing Rose-Pink Marker Circle + Handwritten Arrow Callout",
        "duration": 1.8,
        "sfx": "@asset/audio/sfx/marker_squeak.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "label": "markup",
            "strokeColor": "#C06672",
            "cx": 460,
            "cy": 690,
            "rx": 180,
            "ry": 220
        },
        "body_html": """
      <svg class="mk-svg" viewBox="0 0 1080 1920">
        <text id="mkt" x="80" y="420" fill="#C06672" font-family="Georgia, cursive, serif" font-style="italic" font-weight="700" font-size="78" opacity="0">markup</text>
        <path id="mka" d="M 220 460 Q 260 540 340 540" fill="none" stroke="#C06672" stroke-width="10" stroke-linecap="round" stroke-dasharray="300" stroke-dashoffset="300"/>
        <ellipse id="mkc" cx="460" cy="690" rx="185" ry="225" fill="none" stroke="#C06672" stroke-width="12" stroke-linecap="round" stroke-dasharray="1400" stroke-dashoffset="1400"/>
      </svg>""",
        "extra_css": """
      .mk-svg { position: absolute; inset: 0; width: 100%; height: 100%; }
""",
        "gsap_js": """
      tl.fromTo('#mkt', { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.22 }, 0.0)
        .to('#mka', { strokeDashoffset: 0, duration: 0.22, ease: 'power2.out' }, 0.12)
        .to('#mkc', { strokeDashoffset: 0, duration: 0.45, ease: 'power2.inOut' }, 0.20);
"""
    },
    {
        "slug": "film-look",
        "shortcut": "@film-look",
        "rule": "Rule TH47",
        "title": "Top-to-Bottom Horizontal Scanline Film Grade Wipe + 16mm Grain",
        "duration": 1.8,
        "sfx": "@asset/audio/sfx/whoosh.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "lineColor": "#F0EADE",
            "grainOverlay": "@asset/video/overlays/film_grain_16mm.mov"
        },
        "body_html": """
      <div class="film-scan" id="fscan"></div>""",
        "extra_css": """
      .film-scan { position: absolute; left: 0; right: 0; top: 0; height: 6px; background: #F0EADE; box-shadow: 0 0 28px rgba(240,234,222,0.85); }
""",
        "gsap_js": """
      tl.fromTo('#fscan', { y: 120, opacity: 1 }, { y: 1760, opacity: 0, duration: 1.1, ease: 'power2.inOut' }, 0.0);
"""
    },
    {
        "slug": "jiggle-delete",
        "shortcut": "@jiggle-delete",
        "rule": "Rule TH48",
        "title": "iOS Edit-Mode Jiggling Competitor App Icons + Sequential Pop Delete",
        "duration": 2.0,
        "sfx": "@asset/audio/sfx/pop.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "apps": [
                {"name": "CapCut", "icon": "@asset/logos/apps/capcut.svg"},
                {"name": "Edits", "icon": "@asset/logos/apps/edits.svg"},
                {"name": "InShot", "icon": "@asset/logos/apps/inshot.svg"},
                {"name": "Premiere", "icon": "@asset/logos/apps/premiere.svg"}
            ]
        },
        "body_html": """
      <div class="jd-card" id="jdc">
        <div class="jd-head"><span>EDIT MODE</span><span id="jcnt">4 apps</span></div>
        <div class="jd-row">
          <div class="jd-app" id="ja1"><span class="minus">-</span><div class="ic cc">CC</div><div class="nm">CapCut</div></div>
          <div class="jd-app" id="ja2"><span class="minus">-</span><div class="ic ed">ED</div><div class="nm">Edits</div></div>
          <div class="jd-app" id="ja3"><span class="minus">-</span><div class="ic in">IN</div><div class="nm">InShot</div></div>
          <div class="jd-app" id="ja4"><span class="minus">-</span><div class="ic pr">Pr</div><div class="nm">Premiere</div></div>
        </div>
      </div>""",
        "extra_css": """
      .jd-card { position: absolute; top: 56%; left: 6%; right: 6%; background: #F0EADE; color: #141413; border-radius: 32px; padding: 28px 36px; box-shadow: 0 28px 64px rgba(0,0,0,0.75); }
      .jd-head { display: flex; justify-content: space-between; font-size: 22px; font-weight: 800; letter-spacing: 0.1em; color: #57534E; margin-bottom: 24px; }
      .jd-row { display: flex; justify-content: space-around; }
      .jd-app { position: relative; display: flex; flex-direction: column; align-items: center; gap: 10px; }
      .minus { position: absolute; top: -10px; left: -10px; width: 36px; height: 36px; border-radius: 50%; background: #EF4444; color: #FFF; font-weight: 900; display: flex; align-items: center; justify-content: center; font-size: 28px; }
      .ic { width: 120px; height: 120px; border-radius: 28px; display: flex; align-items: center; justify-content: center; font-size: 48px; font-weight: 900; color: #FFF; }
      .cc { background: #141413; } .ed { background: #7C2D12; } .in { background: #E11D48; } .pr { background: #1E1B4B; color: #A5B4FC; }
      .nm { font-size: 22px; font-weight: 700; }
""",
        "gsap_js": """
      tl.fromTo('#jdc', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.25, ease: 'power3.out' }, 0.0)
        .fromTo('.jd-app', { rotation: -3 }, { rotation: 3, duration: 0.09, yoyo: true, repeat: 10, ease: 'sine.inOut' }, 0.1)
        .to('#ja1, #ja2, #ja3, #ja4', { opacity: 0, scale: 0, duration: 0.16, stagger: 0.14, ease: 'back.in(2.0)' }, 0.45);
"""
    },
    {
        "slug": "screenplay-page",
        "shortcut": "@screenplay-page",
        "rule": "Rule TH49",
        "title": "Courier Screenplay Page Slide-In + Yellow Highlighter Sweep",
        "duration": 1.8,
        "sfx": "@asset/audio/sfx/paper_slide.wav",
        "requires_cutout": False,
        "top_zone": True,
        "default_vars": {
            "slugline": "INT. GREEN ROOM - DAY",
            "character": "JUSTYN",
            "parenthetical": "(to camera)",
            "highlightedLine": "Screenplay page."
        },
        "body_html": """
      <div class="sp-page" id="spp">
        <div class="sp-slug">INT. GREEN ROOM - DAY</div>
        <div class="sp-char">JUSTYN</div>
        <div class="sp-par">(to camera)</div>
        <div class="sp-dia">
          <span class="muted">Film look. Jiggle delete.</span><br/>
          <span class="sp-hl-wrap"><span class="sp-hl" id="sphl"></span><b>Screenplay page.</b></span><br/>
          <span class="muted">Grid collapse.</span>
        </div>
        <div class="sp-cut">CUT TO:</div>
      </div>""",
        "extra_css": """
      .sp-page { position: absolute; top: 0; bottom: 0; left: 0; width: 66%; background: #F0EADE; color: #141413; font-family: 'Courier New', Courier, monospace; padding: 380px 56px 120px; box-shadow: 24px 0 64px rgba(0,0,0,0.65); }
      .sp-slug { font-size: 30px; font-weight: 700; margin-bottom: 48px; }
      .sp-char { font-size: 30px; font-weight: 700; text-align: center; }
      .sp-par { font-size: 28px; text-align: center; margin-bottom: 18px; }
      .sp-dia { font-size: 32px; line-height: 1.42; margin-bottom: 48px; }
      .muted { opacity: 0.42; }
      .sp-hl-wrap { position: relative; display: inline-block; }
      .sp-hl { position: absolute; inset: 0 -6px; background: #F6E478; z-index: 0; transform-origin: left center; transform: scaleX(0); }
      .sp-hl-wrap b { position: relative; z-index: 1; }
      .sp-cut { font-size: 28px; text-align: right; opacity: 0.65; }
""",
        "gsap_js": """
      tl.fromTo('#spp', { x: '-100%' }, { x: '0%', duration: 0.28, ease: 'power3.out' }, 0.0)
        .to('#sphl', { scaleX: 1, duration: 0.35, ease: 'power2.out' }, 0.28);
"""
    },
    {
        "slug": "contact-sheet-hook",
        "shortcut": "@contact-sheet-hook",
        "rule": "Rule TH50",
        "title": "Forest-Green Numbered 4x5 Contact Sheet + Sequential Frame Stamp",
        "duration": 2.0,
        "sfx": "@asset/audio/sfx/timeline_tick.wav",
        "requires_cutout": False,
        "top_zone": True,
        "default_vars": {
            "bgHex": "#123024",
            "title": "CONTACT SHEET",
            "subtitle": "HOOK",
            "thumbAssets": []
        },
        "body_html": """
      <div class="cs-screen" id="css">
        <div class="cs-head">
          <div class="cs-t1">CONTACT SHEET</div>
          <div class="cs-t2" id="cst2">HOOK</div>
        </div>
        <div class="cs-grid">
          <div class="cs-cell">01</div><div class="cs-cell">02</div><div class="cs-cell">03</div><div class="cs-cell">04</div>
          <div class="cs-cell">05</div><div class="cs-cell">06</div><div class="cs-cell">07</div><div class="cs-cell">08</div>
          <div class="cs-cell">09</div><div class="cs-cell">10</div><div class="cs-cell">11</div><div class="cs-cell">12</div>
          <div class="cs-cell">13</div><div class="cs-cell">14</div><div class="cs-cell">15</div><div class="cs-cell">16</div>
        </div>
      </div>""",
        "extra_css": """
      .cs-screen { position: absolute; inset: 0; background: #123024; padding: 140px 44px; display: flex; flex-direction: column; gap: 36px; }
      .cs-head { width: 62%; text-align: center; font-family: Georgia, serif; }
      .cs-t1 { font-size: 46px; color: #F0EADE; letter-spacing: 0.06em; }
      .cs-t2 { font-size: 112px; color: #C6A254; line-height: 0.95; opacity: 0; }
      .cs-grid { width: 62%; display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
      .cs-cell { aspect-ratio: 1/1.15; border: 2px solid rgba(240,234,222,0.22); border-radius: 8px; background: #183A2C; display: flex; align-items: center; justify-content: center; font-size: 24px; color: #C6A254; font-weight: 700; opacity: 0.25; }
""",
        "gsap_js": """
      tl.to('.cs-cell', { opacity: 1, backgroundColor: '#2A5240', duration: 0.06, stagger: 0.04 }, 0.05)
        .fromTo('#cst2', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.25, ease: 'power3.out' }, 0.35);
"""
    },
    {
        "slug": "keycaps",
        "shortcut": "@keycaps",
        "rule": "Rule TH51",
        "title": "3D Tactile Mac Keyboard Shortcuts Raining & Bouncing Above Head",
        "duration": 1.8,
        "sfx": "@asset/audio/sfx/click.wav",
        "requires_cutout": False,
        "top_zone": True,
        "default_vars": {
            "keys": ["⌘K", "⌘B", "⌘Z", "space", "J", "K", "L"]
        },
        "body_html": """
      <div class="kc k1"><b>⌘K</b><span>ADD EDIT</span></div>
      <div class="kc k2"><b>⌘B</b><span>BLADE</span></div>
      <div class="kc k3"><b>⌘Z</b><span>UNDO</span></div>
      <div class="kc k4 wide"><b>space</b><span>PLAY</span></div>
      <div class="kc k5"><b>J</b></div>
      <div class="kc k6"><b>L</b></div>""",
        "extra_css": """
      .kc { position: absolute; width: 132px; height: 132px; background: #F0EADE; color: #141413; border-radius: 24px; border-bottom: 12px solid #C7BFA8; box-shadow: 0 20px 44px rgba(0,0,0,0.65); display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0; }
      .kc.wide { width: 220px; }
      .kc b { font-size: 42px; font-weight: 900; }
      .kc span { font-size: 16px; font-weight: 700; opacity: 0.55; margin-top: 4px; }
      .k1 { top: 26%; left: 18%; transform: rotate(-6deg); }
      .k2 { top: 14%; left: 36%; transform: rotate(5deg); }
      .k3 { top: 22%; left: 48%; transform: rotate(-4deg); }
      .k4 { top: 18%; left: 26%; transform: rotate(3deg); }
      .k5 { top: 30%; left: 8%; transform: rotate(-8deg); }
      .k6 { top: 28%; left: 54%; transform: rotate(7deg); }
""",
        "gsap_js": """
      tl.fromTo('.kc', { opacity: 0, y: -320, scale: 0.7 }, { opacity: 1, y: 0, scale: 1, duration: 0.42, stagger: 0.06, ease: 'bounce.out' }, 0.0);
"""
    },
    {
        "slug": "nle-timeline",
        "shortcut": "@nle-timeline",
        "rule": "Rule TH52",
        "title": "Floating Dark-Green NLE Multi-Clip Timeline Strip + Sweeping Playhead",
        "duration": 1.8,
        "sfx": "@asset/audio/sfx/timeline_tick.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "timecode": "00:00:15:08",
            "clipCount": 14
        },
        "body_html": """
      <div class="nle-bar" id="nleb">
        <div class="nle-head"><span>Timeline</span><span class="tc">00:00:15:08</span></div>
        <div class="nle-body">
          <div class="clips-row">
            <span class="cl"></span><span class="cl"></span><span class="cl"></span><span class="cl"></span><span class="cl"></span><span class="cl"></span><span class="cl"></span><span class="cl"></span>
          </div>
          <div class="wave-row"></div>
          <div class="phead" id="nph"></div>
        </div>
      </div>""",
        "extra_css": """
      .nle-bar { position: absolute; bottom: 16%; left: 4%; right: 4%; background: rgba(14, 34, 26, 0.94); border: 2px solid #2A5240; border-radius: 24px; padding: 24px 32px; box-shadow: 0 28px 64px rgba(0,0,0,0.8); }
      .nle-head { display: flex; justify-content: space-between; font-size: 24px; color: #F0EADE; margin-bottom: 18px; font-weight: 700; }
      .tc { color: #C6A254; font-family: monospace; }
      .nle-body { position: relative; padding: 14px 0; }
      .clips-row { display: flex; gap: 6px; height: 42px; margin-bottom: 10px; }
      .cl { flex: 1; background: #F0EADE; border-radius: 6px; }
      .wave-row { height: 28px; background: rgba(74, 222, 128, 0.35); border-radius: 6px; }
      .phead { position: absolute; top: -10px; bottom: -10px; left: 0; width: 4px; background: #F0EADE; }
""",
        "gsap_js": """
      tl.fromTo('#nleb', { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.25, ease: 'power3.out' }, 0.0)
        .fromTo('#nph', { x: 60 }, { x: 880, duration: 1.3, ease: 'none' }, 0.15);
"""
    },
    {
        "slug": "serif-stamp",
        "shortcut": "@serif-stamp",
        "rule": "Rule TH53",
        "title": "Editorial Gold Italic Prefix + Letter-by-Letter Giant Cream Serif Stamp",
        "duration": 1.8,
        "sfx": "@asset/audio/sfx/paper_thock.wav",
        "requires_cutout": False,
        "top_zone": False,
        "default_vars": {
            "prefix": "serif",
            "word": "STAMP"
        },
        "body_html": """
      <div class="ss-wrap">
        <div class="ss-pre" id="ssp">serif</div>
        <div class="ss-word">
          <span class="sl">S</span><span class="sl">T</span><span class="sl">A</span><span class="sl">M</span><span class="sl">P</span>
        </div>
      </div>""",
        "extra_css": """
      .ss-wrap { position: absolute; top: 34%; left: 4%; width: 62%; font-family: Georgia, 'Times New Roman', serif; }
      .ss-pre { font-style: italic; font-size: 64px; color: #C6A254; text-align: center; margin-bottom: -12px; opacity: 0; }
      .ss-word { display: flex; justify-content: center; gap: 4px; font-size: 164px; font-weight: 700; color: #F0EADE; text-shadow: 0 16px 40px rgba(0,0,0,0.8); }
      .sl { display: inline-block; opacity: 0; }
""",
        "gsap_js": """
      tl.fromTo('#ssp', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.2 }, 0.0)
        .fromTo('.sl', { opacity: 0, scale: 1.45 }, { opacity: 1, scale: 1, duration: 0.14, stagger: 0.06, ease: 'power4.out' }, 0.16);
"""
    },
    {
        "slug": "icon-strike",
        "shortcut": "@icon-strike",
        "rule": "Rule TH54",
        "title": "Competitor App Icons Slashed with Rose-Pink X-Strike + Gravity Drop",
        "duration": 1.8,
        "sfx": "@asset/audio/sfx/marker_squeak.wav",
        "requires_cutout": False,
        "top_zone": True,
        "default_vars": {
            "icons": ["@asset/logos/apps/capcut.svg", "@asset/logos/apps/edits.svg"],
            "strikeWord": "strike."
        },
        "body_html": """
      <div class="is-title" id="ist">strike.</div>
      <div class="is-box b1" id="ib1"><div class="ic">CC</div><div class="xline" id="xl1"></div></div>
      <div class="is-box b2" id="ib2"><div class="ic ed">ED</div><div class="xline" id="xl2"></div></div>""",
        "extra_css": """
      .is-title { position: absolute; top: 14%; left: 10%; font-family: Georgia, serif; font-style: italic; font-size: 88px; color: #F0EADE; opacity: 0; }
      .is-box { position: absolute; top: 24%; width: 140px; height: 140px; }
      .b1 { left: 8%; } .b2 { left: 26%; }
      .ic { width: 100%; height: 100%; border-radius: 32px; background: #F0EADE; color: #141413; display: flex; align-items: center; justify-content: center; font-size: 54px; font-weight: 900; }
      .ic.ed { background: #1E1B2E; color: #F472B6; }
      .xline { position: absolute; inset: -10px; border-top: 12px solid #C06672; transform: rotate(-38deg) scaleX(0); transform-origin: left center; top: 50%; }
""",
        "gsap_js": """
      tl.fromTo('#ib1, #ib2', { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.2, stagger: 0.08, ease: 'back.out(1.6)' }, 0.0)
        .to('#xl1, #xl2', { scaleX: 1, duration: 0.18, stagger: 0.1 }, 0.24)
        .fromTo('#ist', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.22 }, 0.35)
        .to('#ib1, #ib2', { y: 520, rotation: -28, opacity: 0, duration: 0.45, stagger: 0.08, ease: 'power2.in' }, 0.55);
"""
    },
    {
        "slug": "grease-pencil",
        "shortcut": "@grease-pencil",
        "rule": "Rule TH55",
        "title": "3-Row Film Strip Contact Sheet + Red Grease-Pencil Dead-Air X Slash",
        "duration": 2.0,
        "sfx": "@asset/audio/sfx/marker_squeak.wav",
        "requires_cutout": False,
        "top_zone": True,
        "default_vars": {
            "header": "dead air",
            "strokeColor": "#C06672"
        },
        "body_html": """
      <div class="gp-sheet" id="gps">
        <div class="gp-head">dead air</div>
        <div class="gp-row"><div class="f"></div><div class="f"></div><div class="f"></div><div class="f"></div><div class="gx" id="gx1">✕ ✕ ✕</div></div>
        <div class="gp-row"><div class="f"></div><div class="f"></div><div class="f"></div><div class="f"></div></div>
        <div class="gp-row"><div class="f"></div><div class="f"></div><div class="f"></div><div class="f"></div><div class="gx" id="gx2">✕ ✕</div></div>
      </div>""",
        "extra_css": """
      .gp-sheet { position: absolute; top: 12%; left: 4%; width: 60%; background: #F0EADE; color: #141413; padding: 28px; border-radius: 12px; box-shadow: 0 28px 64px rgba(0,0,0,0.75); }
      .gp-head { font-family: Georgia, serif; font-style: italic; font-size: 46px; color: #C06672; margin-bottom: 14px; }
      .gp-row { position: relative; display: flex; gap: 8px; height: 110px; background: #141413; padding: 12px 8px; margin-bottom: 12px; border-top: 6px dashed #F0EADE; border-bottom: 6px dashed #F0EADE; }
      .f { flex: 1; background: #334155; border-radius: 4px; }
      .gx { position: absolute; inset: 0; display: flex; align-items: center; justify-content: flex-end; padding-right: 24px; font-size: 76px; font-weight: 900; color: #C06672; letter-spacing: 0.25em; opacity: 0; }
""",
        "gsap_js": """
      tl.fromTo('#gps', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: 'power3.out' }, 0.0)
        .to('#gx1, #gx2', { opacity: 1, duration: 0.2, stagger: 0.18 }, 0.28);
"""
    },
    {
        "slug": "video-card",
        "shortcut": "@video-card",
        "rule": "Rule TH56",
        "title": "Split Floating Video Preview Card + Forest-Green Chapter Selector",
        "duration": 2.2,
        "sfx": "@asset/audio/sfx/pop.wav",
        "requires_cutout": False,
        "top_zone": True,
        "default_vars": {
            "cardTitle": "Video card",
            "chapter1": "01 The raw take",
            "chapter2": "02 The finished reel",
            "previewAsset": "@asset/photo/thumbnails/chapter_split.png"
        },
        "body_html": """
      <div class="vc-wrap" id="vcw">
        <div class="vc-top">
          <div class="vc-pane">RAW TAKE</div>
          <div class="vc-pane ed">FINISHED REEL</div>
          <div class="vc-play">▶</div>
        </div>
        <div class="vc-bot">
          <div class="vc-h">Video card</div>
          <div class="vc-sub" id="vcs">02 The finished reel</div>
          <div class="vc-pill">40+ total effects</div>
        </div>
      </div>""",
        "extra_css": """
      .vc-wrap { position: absolute; top: 14%; left: 4%; width: 60%; border-radius: 24px; overflow: hidden; border: 2px solid #2A5240; box-shadow: 0 28px 64px rgba(0,0,0,0.8); }
      .vc-top { position: relative; height: 280px; background: #0F172A; display: flex; }
      .vc-pane { flex: 1; display: flex; align-items: center; justify-content: center; font-size: 26px; font-weight: 800; color: rgba(255,255,255,0.5); border-right: 2px solid rgba(255,255,255,0.12); }
      .vc-pane.ed { background: #183A2C; color: #F0EADE; }
      .vc-play { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 76px; height: 76px; border-radius: 50%; background: #F0EADE; color: #123024; display: flex; align-items: center; justify-content: center; font-size: 32px; }
      .vc-bot { background: #123024; padding: 28px 32px; color: #F0EADE; position: relative; }
      .vc-h { font-family: Georgia, serif; font-size: 52px; margin-bottom: 6px; }
      .vc-sub { font-size: 28px; color: #4ADE80; font-weight: 700; }
      .vc-pill { display: inline-block; margin-top: 14px; background: #C6A254; color: #121414; padding: 8px 20px; border-radius: 10px; font-size: 22px; font-weight: 800; }
""",
        "gsap_js": """
      tl.fromTo('#vcw', { opacity: 0, y: 36, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: 'power3.out' }, 0.0);
"""
    }
]


def to_hf_var_schema(default_vars: dict) -> list:
    decls = []
    for k, v in default_vars.items():
        if isinstance(v, bool):
            vtype = "boolean"
        elif isinstance(v, (int, float)):
            vtype = "number"
        else:
            vtype = "string"
            if not isinstance(v, str):
                v = json.dumps(v)
        decls.append({
            "id": k,
            "type": vtype,
            "label": k,
            "default": v
        })
    return decls


def build_fx_templates():
    os.makedirs(FX_LIB_DIR, exist_ok=True)
    index_manifest = []

    for spec in FX_SPECS:
        slug = spec["slug"]
        comp_dir = os.path.join(FX_LIB_DIR, slug)
        os.makedirs(comp_dir, exist_ok=True)
        gsap = Path(ROOT) / "node_modules/gsap/dist/gsap.min.js"
        if gsap.is_file():
            vendor = Path(comp_dir) / "vendor"
            vendor.mkdir(exist_ok=True)
            shutil.copy2(gsap, vendor / "gsap.min.js")

        hf_schema = to_hf_var_schema(spec["default_vars"])
        vars_json_attr = json.dumps(hf_schema).replace("'", "&#39;")
        dur = spec["duration"]

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>{spec["shortcut"]} — {spec["title"]}</title>
  <script src="vendor/gsap.min.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: transparent;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
      color: #FFFFFF;
    }}
    #stage {{
      width: 1080px;
      height: 1920px;
      position: relative;
      overflow: hidden;
    }}
{spec["extra_css"]}  </style>
</head>
<body>
  <div id="stage"
       data-composition-id="main"
       data-composition
       data-start="0"
       data-width="1080"
       data-height="1920"
       data-fps="60"
       data-duration="{dur}"
       data-composition-variables='{vars_json_attr}'>
{spec["body_html"]}
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    const vars = (window.__hyperframes && typeof window.__hyperframes.getVariables === 'function')
      ? window.__hyperframes.getVariables()
      : {json.dumps(spec["default_vars"])};
{binding_script(slug)}
    const tl = gsap.timeline({{ paused: true }});
{spec["gsap_js"]}
    window.__timelines["main"] = tl;
    window.__hyperframes_timeline = tl;
  </script>
</body>
</html>
"""
        write_text(os.path.join(comp_dir, "index.html"), html)

        params_doc = {
            "shortcut": spec["shortcut"],
            "status": "experimental-demo",
            "unbound_variables": [k for k in spec["default_vars"] if "vars." + k not in binding_script(slug) + spec["gsap_js"]],
            "slug": slug,
            "rule": spec["rule"],
            "title": spec["title"],
            "composition_path": f"animations/_fx_library/{slug}/index.html",
            "duration_sec": dur,
            "fps": 60,
            "canvas": [1080, 1920],
            "requires_person_cutout": spec["requires_cutout"],
            "occupies_top_zone": spec["top_zone"],
            "default_sfx_handle": spec["sfx"],
            "variables": spec["default_vars"],
            "render_command": f"npx hyperframes render animations/_fx_library/{slug} --format mov --output broll/<Project>/{slug}.mov"
        }
        write_text(os.path.join(comp_dir, "params.json"), json.dumps(params_doc, indent=2))
        index_manifest.append(params_doc)

    # Also record the original 14 Notion effects + full index in animations/_fx_library/registry.json
    write_text(os.path.join(FX_LIB_DIR, "registry.json"), json.dumps({
        "total_pack_2_and_3_templates": len(index_manifest),
        "templates": index_manifest
    }, indent=2))
    print(f"✅ Built {len(index_manifest)} HyperFrames templates in {FX_LIB_DIR} and starter assets in {ASSETS_DIR}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Scaffold missing assets/scenes; existing assets are never overwritten")
    parser.add_argument("--refresh-scenes", action="store_true", help="Regenerate scene sources from this generator (review diff afterwards)")
    parser.add_argument("--scaffold-assets", action="store_true", help="Create only missing starter assets")
    args = parser.parse_args()
    REFRESH_SCENES = args.refresh_scenes
    if args.scaffold_assets:
        build_starter_assets()
    build_fx_templates()
