> Current execution contract: `docs/agent-runbook.md` and `python3 -m editor capabilities`. These creative/historical specifications do not certify all effects. New feedback is also persisted in project history and scoped memory.

# Talking Head Editing Rules — Antigravity (Gemini 4 Argon) + FeedMedia Notion Effect System

> **Domain**: Solo / Creator Talking Head Videos (9:16 Vertical Reels/Shorts & 16:9 YouTube) combining our baseline retention rules, the **14 FeedMedia Notion Talking Head Effects** adapted for Antigravity on Apple Silicon M4, and our battle-tested **Couple Video precision standards** (10ms RMS acoustic onset sync, native 4K CRF 14 Rec.709, Swift CoreText + HyperFrames overlays, and Subagent QC).
> **Master Index**: [editing-rules.md](./editing-rules.md) | **Sibling Rulebooks**: [editing-rules-couple.md](./editing-rules-couple.md) · [editing-rules-animation.md](./editing-rules-animation.md)

---

## I. The 5-Phase Collaborative Workflow & Storyboard-First Protocol (Rules TH1–TH3)

1. **Rule TH1 — 5-Phase Collaborative Flow & Storyboard First (Notion Effect #1)**:
   - Every Talking Head project follows our **5-Phase Flow**:
     1. **Phase 1 — Understand Raw Video**: Run `./scripts/transcribe.sh` (with 10ms RMS onset verification) and `./scripts/inspect_video.sh` + `view_file` to watch the raw delivery and identify **Last-Take Wins** keeper lines.
     2. **Phase 2 — Discuss & Align**: Present the cleaned keeper script, hook strategy, and suggested visual beats to the user for quick creative alignment.
     3. **Phase 3 — Unified Storyboard First**: Present the **Unified Storyboard Table** (`templates/02_talking_head/storyboard_template.md`) mapping every beat to its spoken words, **Researcher real captures** (`capture_broll.mjs` / `yt-dlp`), **Google Flow MCP AI B-roll** (`@flow-image` / `@flow-video`), and **HyperFrames Motion Graphics** (`npx hyperframes` HTML/CSS/GSAP — replacing Notion's Remotion 1-to-1). **Wait for user approval before rendering.**
     4. **Phase 4 — Asset Sourcing & HyperFrames Rendering**: Researcher fetches real screenshots/logos/reels, Google Flow MCP generates bespoke visual metaphors, **HyperFrames (`npx hyperframes`)** renders all 60fps animated overlays/scenes, and `scripts/person_cutout.swift` (Apple Vision) runs **strictly only** if `@text-behind-head` or `@magazine-cover` is used.
     5. **Phase 5 — Master FFmpeg Assembly & QC**: Assemble `<0.22s` jump cuts, `1.00x / 1.15x` smart framing, `-14 LUFS` voice + ducked BGM + 48kHz SFX, and verify via `view_file` + `caption-qc-reviewer`.
2. **Rule TH2 — Last-Take Wins & Retake Stripping**:
   - Creators frequently record multiple takes of the same sentence back-to-back. Read the word-level transcript from bottom to top—select the **final complete take** of repeated lines unless visual inspection via `view_file` reveals a stumble or eye-line break.
   - Strip all leading/trailing black frames, setup slates, and frames where the speaker looks down at the mouse/keyboard/phone to start or stop recording.
3. **Rule TH3 — Zero-Latency Speech Start (`0:00:00` = First Vocal Syllable)**:
   - Cross-pollinated from Couple Rule C2: Start the video at `0:00:00` on the **exact first spoken syllable** (with `0.04s` pre-consonant micro-padding) and display the opening hook visual (**Text Behind Head** or **Magazine Cover** or **Hook Title**) immediately from frame `0`.

---

## II. Jump Cuts, Pacing & Smart Layout-Aware Framing (Rules TH4–TH8)

4. **Rule TH4 — `< 0.22s` Tight Silence Stripping & Micro-Padding (Notion Effect #14)**:
   - Cut every pause longer than **`0.20s–0.22s`** in hooks (and `> 0.25s` in body explanations), never cutting inside a word.
   - Leave **`0.04s`** (`1–2` frames at 30/60fps) of padding before the first consonant and **`0.06s`** after the last syllable of every kept segment, paired with a **`15ms–25ms` audio crossfade (`afade` / `acrossfade`)** so cuts never click or clip breaths.
   - Strip standalone filler words (`um`, `uh`, `er`, `ah`, `like` as a pause, throat clearing, and audible breaths `> 0.25s`).
5. **Rule TH5 — Smart Layout-Aware `1.00x / 1.15x` Framing Alternation (Notion Effect #14 + Couple Rule C3)**:
   - On consecutive talking-head jump cuts where no upper-frame card is active, alternate instantaneously between **`1.00x` (normal)** and **`1.12x–1.15x` (tight framing)** on the cut frame to disguise the jump cut without distracting zoom tweens.
   - **Eye-Line Preservation**: When cropped to `1.12x–1.15x`, anchor the vertical crop at **`y = 42%`** of frame height (`crop=w=iw/z:h=ih/z:x=(iw-ow)/2:y=(ih-oh)*0.42`) so the speaker's eyes stay on the upper third line.
   - **Top-Overlay Collision Guard**: Whenever an upper-frame visual card (`repo-card`, `prompt-bar`, `real-screenshot`, `lr-panel`) occupies the top `15%–40%` above the speaker's head, automatically lock framing to `1.00x` (or shift the vertical anchor so the speaker's head never collides with the card).
6. **Rule TH6 — 3-Second Visual Change Rule (Hook) & 8-Second Max Static Shot**:
   - During the first 15 seconds, the visual state on screen must change every **`2.5s–3.5s`** (via Text Behind Head, Tool Label, Prompt Bar, Color Wipe, or framing cut).
   - Never leave an unedited, static talking-head shot on screen for more than **8 consecutive seconds** anywhere in the video. For continuous monologues `> 5s`, apply a subtle creep zoom (`1.00x -> 1.05x`).
7. **Rule TH7 — J-Cuts on Scene Transitions**:
   - Start incoming dialogue audio **`0.10s–0.15s` before** the visual cut when transitioning from a full-screen B-roll/animation clip back to the talking head.
8. **Rule TH8 — Local Screen Recording Framing (Zero Tella Needed)**:
   - Trim silences/fillers and apply dynamic punch-in zooms (`1.15x–1.35x` on active UI regions) directly via Parakeet/Whisper word timestamps + FFmpeg. If compositing a PIP speaker bubble, place it in the bottom-left or bottom-right corner (`18%–22%` width, `24px` corner radius).

---

## III. The 14 FeedMedia Notion Talking Head Effects (Antigravity Apple M4 Specifications)

9. **Rule TH9 — Person Segmentation Prerequisite (`Apple Vision` Hardware Cutout)**:
   - For any depth-layered effect behind the speaker's head (**Text Behind Head**, **Magazine Cover**), use macOS native `Vision` (`VNGeneratePersonSegmentationRequest` at `.qualityLevel = .accurate` in `scripts/person_cutout.swift`) to generate a 4K feathered foreground alpha matte (`ProRes 4444` `yuva444p10le`) sandwiching graphics between `[0:v]` (background footage) and `[2:v]` (person cutout).
10. **Rule TH10 — Text Behind Your Head (Notion Effect #2)**:
    - Place a 2-line title between the background video and the speaker's person cutout so the speaker's head naturally overlaps part of the letters.
    - **Spec**: `Geist Pixel Square` (or `Arial-Black` / display font), `150px` on 1080p (`300px` on 4K), `#F4F4F2`, horizontally centered at **`20%` and `27%`** of frame height.
    - **Motion**: Each line fades up over **12 frames** (`ease-out cubic` / `power3.out`, rising `2%` of frame height), with Line 2 delayed by **4 frames** after Line 1.
11. **Rule TH11 — Selective Coral Pill Captions vs. One-Word Pop Captions (Notion Effect #3 + Couple Rule C9)**:
    - Support two selectable caption modes anchored to **10ms RMS-verified acoustic word onsets**:
      - **Mode A — Selective Coral Pill (`coral_pill_3word`, Notion Default)**: `Helvetica Neue Bold`, `64px` on 1080p (`128px` on 4K), pure white (`#FFFFFF`), soft drop shadow, centered at **`61.5%`** of frame height. Group up to **3 words at a time**, cutting on the exact acoustic onset of the chunk's first word. **Highlight ONLY the currently spoken word** on a rounded coral box (`#D97757`, `8px` radius on 1080p / `16px` on 4K) while the other words in the 3-word group have no box.
      - **Mode B — One-Word Kinetic Pop (`one_word_pop`, Couple Game Style)**: Show strictly one word at a time with an `85ms` scale pop (`128% -> 100%`) that disappears during silence.
    - **No Caption Overlap**: Automatically suppress lower captions whenever a full-screen graphic or `61.5%`-height `tool-label` is active.
12. **Rule TH12 — Tool Labels: Logo Fade-Up + Sliding Name Reveal (Notion Effect #4)**:
    - Whenever a software tool, model, or library is named out loud, trigger its Tool Label at **`61.5%`** of frame height on the exact acoustic onset of the tool's name:
      - **Phase 1 (Frames 0–12, `ease-out cubic`)**: App logo (`110px` on 1080p / `220px` on 4K, rounded corners) fades up at center (`y: +2% -> 0%`, `opacity: 0 -> 1`).
      - **Phase 2 (Frames 12–24, `ease-out cubic`)**: Logo slides left while the tool name (`bold white, 92px` on 1080p / `184px` on 4K) slides out from behind the logo to the right so the combined logo + name lockup ends horizontally centered, paired with `pop.wav`.
13. **Rule TH13 — GitHub Dark-Theme Repo Cards (Notion Effect #5)**:
    - Whenever an open-source repository is mentioned, animate a GitHub dark-theme card (`#0D1117` fill, `#30363D` border) at the top of the frame: **`85%` of frame width**, rising `2%` and fading in over **12 frames** (`ease-out cubic`), displaying `owner/name`, `Public` pill badge, repository description, star count, and fork count.
14. **Rule TH14 — Reusable Vector Prompt Bar Component (Notion Effect #6)**:
    - Whenever demonstrating an AI prompt, render the standardized reusable Prompt Bar component at **`22.5%` of frame height** and **`92.6%` of frame width**:
      - Dark fully-rounded pill bar (`#2B2B2B`, `border-radius: 999px`), white `Inter` text typing in deterministically, and a right-aligned coral (`#D97757`) circular send button with a white up-arrow that clicks (`click.wav`) upon completion.
15. **Rule TH15 — Colour Change with a Slider: Warm-to-Natural Wipe (Notion Effect #7)**:
    - When illustrating color grading or before/after visual states, generate a warm pass with FFmpeg (`colorchannelmixer=rr=1.17:gg=1.10:bb=1.03,eq=saturation=1.12`), start on the warm version, and wipe right-to-left over **30 frames** (`ease-in-out cubic`) with a thin white vertical divider line (`4px–6px`) to reveal the natural grade underneath, paired with `whoosh.wav`.
16. **Rule TH16 — Stressed-Word Magazine Cover Layout (Notion Effect #8)**:
    - Transform a talking-head shot into a print magazine cover using the speaker's person cutout:
      - **Behind Head**: Cream serif masthead (`"CLAUDE"` or topic title, `#F5F0E6`).
      - **In Front of Cutout**: Thin gold inset border frame (`#D4AF37`), editorial cover lines in the top corners, and a vector barcode on the left.
      - **Synchronization**: Pop each element onto the canvas on a **stressed spoken word** (`rms_onset_ms`) paired with subtle `pop.wav` / `click.wav` hits.
17. **Rule TH17 — Real Screenshots Over Mockups + Research B-Roll Standards (Notion Effect #9 + Rules 14–19)**:
    - **Always Use Real Screenshots**: Capture authentic editor timelines, papers, benchmarks, or web pages via `scripts/capture_broll.mjs` at `2560x1440` (`deviceScaleFactor: 2`), dismissing cookie banners and navbars.
    - **Fade-Up Framing Above Head**: Display the screenshot above the speaker's head at **`90%` of frame width**, rounded corners (`16px–32px`), soft drop shadow, fading up over **12 frames** (`ease-out cubic`).
    - **Yellow Marker Highlight**: When showing an article or research paper, sweep a warm yellow highlight (`rgba(255, 230, 0, 0.45)`) across the exact sentence being discussed (`2.0s–4.5s` duration bounds) with a clean source attribution badge.
18. **Rule TH18 — Whip-Pan Transition (Preferred) & Recursive 3-Level PIP Zoom (Notion Effects #10A & #10B)**:
    - **Whip-Pan Transition (Default Scene Transition)**: In the last **6 frames** of Shot A, slide it left by **`8%` of frame width** while ramping horizontal motion blur up to **`50px`** (`ease-in`). Cut. Start Shot B **`8%` to the right**, fully blurred (`50px`), settling into center over **6 frames** (`ease-out cubic`) with `whoosh.wav` centered on the cut so it feels like a single fast camera whip.
    - **Recursive 3-Level PIP Zoom (Use Sparingly on Self-Referential Beats)**: On a trigger word like `"this"`, shrink the active shot into a picture-in-picture of itself **3 levels deep** landing above the speaker's head, hold briefly, then push through into the next shot.
19. **Rule TH19 — Live Moody Film Grade + Interactive Lightroom Panel (Notion Effect #11)**:
    - Apply an FFmpeg film grade (`curves` pulling highlights down and lifting blacks, `eq=saturation=0.85`, soft `vignette`) while displaying a floating Lightroom-style grading inspector (`Tone Curve`, `Basic`, `Effects`) above the speaker's head. Animate each UI control/slider at the exact millisecond the speaker names it while live-interpolating the video grade on screen.
20. **Rule TH20 — 3×3 Wall of Reels with `yt-dlp` Sourcing (Notion Effect #12)**:
    - Download reference vertical reels via `yt-dlp`, shrink the active talking-head shot into the **center tile (`row 2, col 2`) of a `3×3` grid** (`33.3%` width/height), and pop the other 8 reels into the surrounding 8 tiles at **1 tile per frame**.
21. **Rule TH21 — Pause and Explain: PIP Window + Timecode Freeze + Shrink (Notion Effect #13)**:
    - Play a reference clip inside a top-left window (**`54%` of frame width**, rounded corners) with a live corner timecode readout.
    - On a mouse-click SFX (`click.wav`), **freeze both the video frame and the corner timecode**.
    - **10 frames later**, shrink the frozen window to the left side (**`24%` of frame width**, rounded corners) over **12 frames** (`ease-out cubic`) while the speaker explains, then grow it back to `54%` and resume playback.

---

## IV. Audio Mixing, Studio Master Export & Self-Improving Loop (Rules TH22–TH25)

22. **Rule TH22 — Voice Loudness (`-14 LUFS`) & Dynamic BGM Ducking**:
    - Normalize isolated dialogue to **`-14 LUFS`** (`true peak -1.5 dBTP`, `80 Hz` high-pass filter) **before** mixing (`amix=normalize=0`).
    - Duck royalty-free background music (`free-audio` MCP) to **`-20 dB`** under speech, ramping smoothly (`0.3s` attack, `0.6s` release) to `-11 dB` during non-speaking B-roll beats, and drop music completely for `0.5s–1.0s` right before major punchlines or contrarian reveals.
23. **Rule TH23 — Restrained 48kHz Studio SFX Placement**:
    - Layer subtle, 48kHz-resampled SFX (`-14 dB` to `-18 dB`) on visual entrances: `whoosh.wav` on whip-pans/slides, `pop.wav` on tool labels/repo cards/stressed magazine words, `click.wav` on prompt bar send and pause-and-explain freezes, and `sub_drop.wav` on major hook pattern interrupts. **Never stack more than 2 SFX within a 1.5s window.**
24. **Rule TH24 — Native 4K Studio Master Delivery & Two-Stage Render**:
    - Render fast preview drafts to `renders/drafts/<Project>/` and final masters to `renders/final/<Project>/` in **Native 4K (`2160×3840` vertical or `3840×2160` horizontal)** at `H.264 High@L5.2 -preset slow -crf 14`, explicit Rec.709 color tags (`bt709`), and `320k` 48kHz AAC audio.
25. **Rule TH25 — QC Subagent Verification & Permanent Rule Update**:
    - Verify every render via `inspect_video.sh` + `view_file` + `caption-qc-reviewer` subagent, and permanently log every user revision into this file and the master [editing-rules.md](./editing-rules.md) changelog.

---

## V. Strict Dual-Handle Asset Resolution (`@asset/...` & `@project/...` — Rule TH25A)

25A. **Rule TH25A — Mandatory Two-Handle Asset System (`@asset/...` vs. `@project/...`)**:
    - **Anti-Pattern**: Never hardcode ad-hoc paths in `/tmp`, root folders, or ambiguous relative strings when referencing background videos, reference reels, photos, textures, app icons, device mockups, or SFX.
    - **Handle 1 — Global Reusable Studio Library (`@asset/<category>/<subcategory>/<file>`)**:
      Maps directly to [`assets/`](../../../../assets/README.md) (`assets/manifest.json`):
      - `@asset/video/backgrounds/<file>` $\rightarrow$ `assets/video/backgrounds/` (Loopable studio plates & `@green-screen` replacement videos)
      - `@asset/video/reels/<file>` $\rightarrow$ `assets/video/reels/` (9:16 vertical reels for `@orbit`, `@reel-grid`, `@wall-of-reels`)
      - `@asset/video/broll/<file>` $\rightarrow$ `assets/video/broll/` (Cinematic B-roll & reusable Veo 3.1 clips)
      - `@asset/video/memes/<file>` $\rightarrow$ `assets/video/memes/` (Reaction memes & green-screen comedy clips)
      - `@asset/video/overlays/<file>` $\rightarrow$ `assets/video/overlays/` (ProRes 4444 confetti, 16mm film grain, light leaks, glass shards)
      - `@asset/video/screen_recordings/<file>` $\rightarrow$ `assets/video/screen_recordings/` (Scrolling UI & screen captures for `@phone-mockup` & `@pause-explain`)
      - `@asset/photo/backgrounds/<file>` $\rightarrow$ `assets/photo/backgrounds/` ($\ge 1000\text{px}$ architectural/wall/room plates)
      - `@asset/photo/screenshots/<file>` $\rightarrow$ `assets/photo/screenshots/` (4K Retina browser/GitHub captures from `scripts/capture_broll.mjs`)
      - `@asset/photo/textures/<file>` $\rightarrow$ `assets/photo/textures/` (`cream_editorial_paper.svg` `#F0EADE`, `notebook_grid_paper.svg`, halftone/torn paper)
      - `@asset/photo/headlines/<file>` $\rightarrow$ `assets/photo/headlines/` (Newspaper clippings for `@headline-wall`)
      - `@asset/photo/thumbnails/<file>` $\rightarrow$ `assets/photo/thumbnails/` (Vertical reel cover frames for `@reel-grid` & `@contact-sheet-hook`)
      - `@asset/logos/apps/<file>` $\rightarrow$ `assets/logos/apps/` (`capcut.svg`, `edits.svg`, `inshot.svg`, `premiere.svg`, `ffmpeg.svg`, `claude.svg`, `hyperframes.svg`)
      - `@asset/mockups/devices/<file>` $\rightarrow$ `assets/mockups/devices/` (`iphone_16_pro_frame.svg`)
      - `@asset/audio/sfx/<file>` $\rightarrow$ `assets/audio/sfx/` (`pop.wav`, `whoosh.wav`, `click.wav`, `sub_drop.wav`, `paper_thock.wav`, `paper_slide.wav`, `marker_squeak.wav`, `timeline_tick.wav`)
      - `@asset/audio/music/<file>` $\rightarrow$ `assets/audio/music/` (`nocturne_op9_in_eb.wav` & royalty-free beds)
    - **Handle 2 — Per-Project Scoped Handle (`@project/<type>/<file>`)**:
      Maps to the active `<Project Name>` directory:
      - `@project/raw/<file>` $\rightarrow$ `raw/<Project Name>/<file>`
      - `@project/cutout/<file>` $\rightarrow$ `broll/<Project Name>/<file>` (ProRes 4444 alpha matte from `scripts/person_cutout.swift`)
      - `@project/broll/<file>` $\rightarrow$ `broll/<Project Name>/<file>` (Project-specific rendered `.mov` / `.webm` overlays & Flow outputs)
      - `@project/transcript/<file>` $\rightarrow$ `transcripts/<Project Name>/<file>`

---

## VI. Talking Head Effects Pack 2 & 3 — 31 Reusable HyperFrames Motion Skills (Rules TH26–TH56)

> **Template Library Location**: Every effect below has a ready-to-render, lint-verified 60fps HyperFrames HTML/CSS/GSAP template in [`animations/_fx_library/<slug>/index.html`](../../../../animations/_fx_library/registry.json) + `params.json`.
> **Brand Palette Extracted from Reference Reels (`De25fKeTRl7` & `De4UDEqM1f5`)**:
> - **Pack 2 Dark Studio Accent**: Warm Butter Yellow `#F6E478`, Dark Glass `rgba(18, 18, 20, 0.72)`, Pure White `#FFFFFF`, Ink Black `#141413`.
> - **Pack 3 Editorial Forest & Cream**: Forest Green `#123024` (border `#2A5240`), Editorial Cream Paper `#F0EADE`, Antique Gold `#C6A254`, Rose-Pink Marker `#C06672`.

### A. Global HUD & Caption Layers (Rules TH26–TH27)

26. **Rule TH26 — On-Screen Effect Checklist HUD (`@effect-hud`, Template: `animations/_fx_library/effect-hud/`)**:
    - Syncs the active row highlight to the **10ms RMS acoustic onset** of each spoken effect name (`@asset/audio/sfx/timeline_tick.wav`).
    - **`theme: "split-dark"`**: Centered header at `y=6%` (`72px` bold sans on 1080p / `144px` on 4K, number in `#F6E478`), with two `44%`-width translucent dark glass columns (`01–08` left, `09–16` right, `rgba(18,18,20,0.72)`, `28px` radius). Active item highlights in `#F6E478` bold (`background: rgba(246,228,120,0.14)`).
    - **`theme: "sidebar-green"`**: Top gold italic serif header (`#C6A254`) + right-docked forest-green card (`#123024` fill, `#2A5240` border, `x=68%–96%`, `y=12%–58%`) where the active row flips to an inverted cream pill (`#F0EADE` fill, `#123024` bold text).
    - **Top-Zone Lock**: Automatically locks underlying talking-head framing to `1.00x` (`Rule TH5`) while visible.
27. **Rule TH27 — Dual-Theme Hook/CTA Keyword Captions (`@keyword-captions`, Template: `animations/_fx_library/keyword-captions/`)**:
    - **`theme: "yellow-glow"`**: Centered at `y=52%`. Line 1 in white heavy sans (`84px` @ 1080p / `168px` @ 4K); Line 2 emphasis word in oversized `#F6E478` yellow (`124px` @ 1080p / `248px` @ 4K) animating `filter: blur(18px) -> blur(0px)` and `scale: 0.84 -> 1.0` over `0.28s` (`back.out(1.6)`).
    - **`theme: "white-pill-stack"`**: Stacked cream-white rounded pills (`#F6F0E4` bg, `#121414` text, `16px` radius, `y=60%–66%`) popping in line-by-line with `@asset/audio/sfx/pop.wav`.

### B. Effects Pack 2 — `De25fKeTRl7` 17 Core Effects (Rules TH28–TH44)

28. **Rule TH28 — Torn-Paper Newspaper Headline Wall (`@headline-wall`, Template: `animations/_fx_library/headline-wall/`)**:
    - Slams 3–4 torn-paper newspaper clippings (`#F0EADE` bg, Georgia bold serif, dashed torn top/bottom borders, `±1.5°–4.0°` tilt) around the speaker (`stagger: 0.10s`, `scale: 1.45 -> 1.0`, `power3.out` + `@asset/audio/sfx/paper_thock.wav`), followed by a `#F6E478` yellow marker sweep (`scaleX: 0 -> 1` over `0.32s`) across the hero headline at `y=53%`.
29. **Rule TH29 — Camera Zoom-Through Punch Cut (`@zoom-through`, Template: `animations/_fx_library/zoom-through/`)**:
    - Punches into the active card/subject (`scale: 1.0 -> 6.5` over `0.28s`, `power3.in`) with radial zoom blur, triggers a 2-frame warm white exposure flash (`#FFFDF5` @ `0.95` alpha), and settles into the incoming shot (`scale: 1.8 -> 1.0` over `0.28s`, `power3.out`) paired with `@asset/audio/sfx/whoosh.wav`.
30. **Rule TH30 — Vertigo Dolly-Zoom (`@vertigo`, Template: `animations/_fx_library/vertigo/`)**:
    - **Requires `person_cutout.swift` (`@project/cutout/...`)**: Keeps foreground speaker cutout locked at `1.00x–1.02x` while scaling the background plate from `1.00x -> 1.38x` (or `1.38x -> 1.00x`) over `1.20s` (`sine.inOut`) with `eq=saturation=0.88` cool shift + `@asset/audio/sfx/whoosh.wav`.
31. **Rule TH31 — Person-Cutout Background Replacement (`@green-screen`, Template: `animations/_fx_library/green-screen/`)**:
    - **Requires `person_cutout.swift` (`@project/cutout/...`)**: Replaces background behind the speaker with `@asset/video/backgrounds/<clip>` or `@asset/video/memes/<clip>` via a 6-frame horizontal flash wipe (`clip-path: inset(0 100% 0 0) -> inset(0 0% 0 0)`), adding a top dark vignette (`0.45` alpha) so HUD text stays legible.
32. **Rule TH32 — 3D Tilted iPhone Mockup (`@phone-mockup`, Template: `animations/_fx_library/phone-mockup/`)**:
    - Slides in `@asset/mockups/devices/iphone_16_pro_frame.svg` at `left=5%`, `top=30%`, `width=38%` with 3D perspective (`rotateY(14deg) rotateZ(-4deg)`, `0.42s back.out(1.4)` + `@asset/audio/sfx/whoosh.wav`) while scrolling internal screen content (`@asset/photo/screenshots/...` or `@asset/video/screen_recordings/...`) vertically (`y: 0 -> -260px` over `1.4s`).
33. **Rule TH33 — Camera Viewfinder & Lens-Ring Zoom (`@digital-zoom`, Template: `animations/_fx_library/digital-zoom/`)**:
    - Creeps video scale `1.00x -> 1.30x` anchored at `y=42%` while rendering one of two HUD styles (`@asset/audio/sfx/timeline_tick.wav`):
      - **`style: "camcorder"`**: White corner brackets (`44px`, `5px` stroke) around the face (`left=26%, top=20%, width=48%, height=34%`), blinking red `● REC` + timecode bottom-left, tick ruler center, and live `#F6E478` zoom readout (`1.00× -> 1.30×`) bottom-right.
      - **`style: "lens-ring"`**: Forest-green focal-length ruler (`#123024`, border `#2A5240`, `top=14%, left=4%, width=58%`) sliding `85 | 70 | 50 | 35 | 24 mm` ticks right-to-left (`x: 0 -> -120px`) with active `24` highlighted in `#C6A254` gold.
34. **Rule TH34 — Stop-Motion Paper-Cutout & Ransom Letters (`@paper-cut`, Template: `animations/_fx_library/paper-cut/`)**:
    - **Requires `person_cutout.swift` (`@project/cutout/...`)**: Composites a `14px` white torn-paper outline around the speaker over `@asset/photo/textures/notebook_grid_paper.svg`, stamps in mixed-font ransom-note letter chips (`108×124px` @ 1080p, `#F0EADE` / `#2563EB` / `#141413` / `#F6E478`, `stagger: 0.06s`, `back.out(2.0)` + `@asset/audio/sfx/paper_thock.wav`), and exits via a vertical paper-tear wipe (`@asset/audio/sfx/paper_slide.wav`).
35. **Rule TH35 — Floating 3D Glassmorphism UI World (`@ui-world`, Template: `animations/_fx_library/ui-world/`)**:
    - Darkens background video (`brightness=0.72`) and animates 3 translucent cards (`rgba(16,18,22,0.84)`, `2px` border `rgba(255,255,255,0.16)`, `28px` radius):
      1. `PROMPT` card (`top=28%, left=4%, width=38%`) with `#F6E478` progress bar animating `scaleX: 0 -> 1` over `0.9s`.
      2. `TIMELINE` strip (`top=48%, left=4%, width=52%`) with playhead sweeping `x: 40 -> 460px` (`none` ease).
      3. `PREVIEW ● LIVE` card (`top=38%, right=4%, width=36%`) + `@asset/audio/sfx/click.wav`.
36. **Rule TH36 — 3D Carousel Orbit of Vertical Reels (`@orbit`, Template: `animations/_fx_library/orbit/`)**:
    - **Requires `person_cutout.swift` (`@project/cutout/...`)**: Places 4–6 vertical reel cards (`260×420px` @ 1080p, `28px` radius, sourced from `@asset/video/reels/`) on a 3D ring (`perspective: 1400px`, `translateZ(380px)`) rotating `rotationY: -35deg -> 145deg` over `2.0s` (`power2.inOut` + `@asset/audio/sfx/whoosh.wav`), depth-sorted behind and in front of the speaker cutout.
37. **Rule TH37 — IG Reel Frame Break & Glass Shatter (`@frame-break`, Template: `animations/_fx_library/frame-break/`)**:
    - Scales the video into a centered Instagram Reel UI frame (`width=64%, height=64%, top=20%, left=18%, border-radius=38px` with heart/comment/share icons and `@handle · Follow`), while 4–18 polygonal glass shards (`clip-path: polygon(...)`) explode radially outward over `0.7s` (`power3.out` + `@asset/audio/sfx/sub_drop.wav`).
38. **Rule TH38 — Hand-Drawn Neon Doodle Boil (`@doodle-boil`, Template: `animations/_fx_library/doodle-boil/`)**:
    - **Requires `person_cutout.swift` (`@project/cutout/...`)**: Self-traces dual hand-drawn SVG strokes (`#FFFFFF` `14px` + `#F6E478` `8px`, `stroke-dashoffset: 1800 -> 0` over `0.45s`) around the speaker's silhouette + multi-colored spark rings (`#F6E478`, `#FF7EB6`, `#38BDF8`) jittering with `steps(2)` at `12fps` (`@asset/audio/sfx/marker_squeak.wav`).
39. **Rule TH39 — HUD-to-Laptop Sticky Text Slap (`@sticky-text`, Template: `animations/_fx_library/sticky-text/`)**:
    - Flies the active label out of the top HUD (`x: 140 -> 0, y: -520 -> 0, scale: 0.45 -> 1.0, rotation: 18deg -> -5.5deg` over `0.38s`, `back.out(1.7)`) landing at `top=58%, left=48%` as a `#F6E478` yellow sticker pill (`#141413` text, `22px` radius) with a 3-cycle damped wobble + `@asset/audio/sfx/pop.wav`.
40. **Rule TH40 — Vertical Light-Leak Before + After Wipe (`@before-after`, Template: `animations/_fx_library/before-after/`)**:
    - Sweeps a vertical glowing light-leak beam (`14px` `#FFFDF5` core + `48px` `#F6E478` bloom) from `x: 40 -> 1020px` over `1.35s` (`power2.inOut` + `@asset/audio/sfx/whoosh.wav`), transitioning from flat ungraded footage (`"before"` pill at `left=8%, top=56%`) to warm graded footage (`"• after"` pill at `right=8%, top=56%`).
41. **Rule TH41 — 3D Pull-Back into NLE Timeline Window (`@pull-back`, Template: `animations/_fx_library/pull-back/`)**:
    - Pulls the full frame back in 3D perspective (`scale: 1.75 -> 1.0, rotationX: 8deg, rotationY: -10deg` over `0.55s`, `power3.out` + `@asset/audio/sfx/whoosh.wav`) inside a `92%×78%` `#0B0D12` NLE window (`"effects reel"`), sequentially lighting up `✓ cut pauses`, `✓ add effects`, `✓ export` (`#4ADE80`, `stagger: 0.22s`) above a colored multi-track timeline and green waveform.
42. **Rule TH42 — Multi-Plane 3D Z-Depth Letter Scatter (`@depth-scatter`, Template: `animations/_fx_library/depth-scatter/`)**:
    - **Requires `person_cutout.swift` (`@project/cutout/...`) & Top-Zone `1.00x` Lock**:
      - **Behind Head (`top=24%`)**: Word 1 (`"depth"`, `210px` @ 1080p / `420px` @ 4K white heavy sans) assembles letter-by-letter from `scale: 1.8, y: -90, filter: blur(20px) -> scale: 1, y: 0, blur(0px)` (`0.38s power3.out`, `stagger: 0.04s`).
      - **In Front of Cutout (`top=44%`)**: Word 2 (`"scatter"`, `196px` @ 1080p / `392px` @ 4K `#F6E478` yellow) assembles from `scale: 0.4, y: 110, filter: blur(22px) -> scale: 1, y: 0, blur(0px)` (`0.42s back.out(1.5)` + `@asset/audio/sfx/whoosh.wav`).
43. **Rule TH43 — Unified Multi-Reel Grid Engine (`@reel-grid`, Template: `animations/_fx_library/reel-grid/`)**:
    - Sources vertical reels from `@asset/video/reels/` or thumbnails from `@asset/photo/thumbnails/` across 4 modes:
      - `mode: "background"`: 4×4 scrolling wall behind `@project/cutout/...` (`brightness=0.55`).
      - `mode: "collapse"`: 3×3 full-screen grid where outer 8 tiles fly out radially leaving center speaker tile full-screen.
      - `mode: "playing"`: 3×2 live-playing grid (`top=12%, left=5%, width=58%`) popping in (`stagger: 0.06s`).
      - `mode: "cascade"`: 4×2 rounded portrait cards cascading left-to-right (`y: 48 -> 0, scale: 0.82 -> 1.0, stagger: 0.06s, back.out(1.5)` + `@asset/audio/sfx/pop.wav`).
44. **Rule TH44 — Automated Comment-to-DM Funnel (`@comment-bubble`, Template: `animations/_fx_library/comment-bubble/`)**:
    - At `bottom=14%–16%`, animates a 3-stage social conversion sequence:
      1. `0.00s–0.95s`: Dark pill input (`border: 3px solid #F6E478`) slides up (`y: 60 -> 0`) displaying typed keyword (`"STUDIO"` / `"EDIT"`).
      2. `1.05s`: Morphs (`back.out(1.6)` + `@asset/audio/sfx/click.wav`) into a white posted comment bubble (`"you · STUDIO"` + floating `❤️` badge).
      3. `1.45s`: Slides in creator reply bubble (`"Sent you the link"` + `#F6E478` `"🔗 Open link"` pill button).

### C. Effects Pack 3 — `De4UDEqM1f5` 12 Editorial & NLE Effects (Rules TH45–TH56)

45. **Rule TH45 — Knocked-Out Stencil Display Captions (`@knockout-captions`, Template: `animations/_fx_library/knockout-captions/`)**:
    - **Top-Zone `1.00x` Lock**: At `top=10%, left=4%, width=60%`, shows `#123024` green intro pills (`0.0s–0.5s`), then slams a `#F0EADE` cream block (`scale: 1.18 -> 1.0` over `0.22s`, `power4.out` + `@asset/audio/sfx/sub_drop.wav`) with `168px` Georgia Black `"KNOCK / OUT"` knocked out via `mix-blend-mode: screen` (or alpha stencil) so live video shows through the letters.
46. **Rule TH46 — Self-Tracing Rose-Pink Live Markup (`@live-markup`, Template: `animations/_fx_library/live-markup/`)**:
    - Draws a hand-drawn `#C06672` rose-pink SVG ellipse (`cx=460, cy=690, rx=185, ry=225`, `stroke-width: 12`, `stroke-dashoffset: 1400 -> 0` over `0.45s`, `power2.inOut`) around the speaker's head with a curved arrow and italic `"markup"` label (`@asset/audio/sfx/marker_squeak.wav`).
47. **Rule TH47 — Top-to-Bottom Scanline Film Look (`@film-look`, Template: `animations/_fx_library/film-look/`)**:
    - Sweeps a `6px` `#F0EADE` horizontal scanline from `y: 120 -> 1760px` over `1.10s` (`power2.inOut` + `@asset/audio/sfx/whoosh.wav`), wiping in an FFmpeg 16mm Kodak grade (`curves=m='0/0.06 0.25/0.20 0.75/0.78 1/0.94',eq=saturation=0.88`) + `@asset/video/overlays/film_grain_16mm.mov`.
48. **Rule TH48 — iOS Edit-Mode Jiggle Delete (`@jiggle-delete`, Template: `animations/_fx_library/jiggle-delete/`)**:
    - Displays a `#F0EADE` cream card at `top=56%, left=6%, right=6%` (`"EDIT MODE · 4 apps"`) with 4 app icons (`@asset/logos/apps/capcut.svg`, `edits.svg`, `inshot.svg`, `premiere.svg`) oscillating `rotation: -3deg <-> 3deg` (`0.09s yoyo`), then pops each icon to `scale: 0, opacity: 0` (`stagger: 0.14s, back.in(2.0)` + `@asset/audio/sfx/pop.wav`).
49. **Rule TH49 — Courier Screenplay Page Slide & Highlight (`@screenplay-page`, Template: `animations/_fx_library/screenplay-page/`)**:
    - **Top-Zone `1.00x` Lock**: Slides a full-height `#F0EADE` cream page (`width=66%`, `Courier New 32px`) from `x: -100% -> 0%` over `0.28s` (`power3.out` + `@asset/audio/sfx/paper_slide.wav`) showing `INT. GREEN ROOM - DAY`, character cue, and dialogue while sweeping a `#F6E478` highlight bar (`scaleX: 0 -> 1` over `0.35s`) across the active phrase.
50. **Rule TH50 — Forest-Green 4×5 Contact Sheet Hook (`@contact-sheet-hook`, Template: `animations/_fx_library/contact-sheet-hook/`)**:
    - **Top-Zone `1.00x` Lock**: Displays a `#123024` forest-green 4×4/4×5 grid (`width=62%`) with `#F0EADE` serif `"CONTACT SHEET"` and `#C6A254` gold `"HOOK"`, stamping thumbnails (`@asset/photo/thumbnails/`) sequentially into cells `01 -> 16` (`stagger: 0.04s` + `@asset/audio/sfx/timeline_tick.wav`).
51. **Rule TH51 — 3D Tactile Mac Keycaps Drop (`@keycaps`, Template: `animations/_fx_library/keycaps/`)**:
    - **Top-Zone `1.00x` Lock**: Drops 6 bevelled `#F0EADE` 3D keycaps (`132×132px`, `12px` `#C7BFA8` bottom bevel: `⌘K`, `⌘B`, `⌘Z`, `space`, `J`, `L`) from `y: -320 -> 0` over `0.42s` (`bounce.out`, `stagger: 0.06s` + `@asset/audio/sfx/click.wav`) above the speaker's head (`top=14%–30%`).
52. **Rule TH52 — Dark-Green NLE Timeline Bar (`@nle-timeline`, Template: `animations/_fx_library/nle-timeline/`)**:
    - Pops up a floating `#0E221A` NLE timeline bar (`bottom=16%, left=4%, right=4%, border: 2px solid #2A5240`) with `#F0EADE` clip blocks and a green waveform while sweeping the white playhead `x: 60 -> 880px` over `1.30s` (`@asset/audio/sfx/timeline_tick.wav`).
53. **Rule TH53 — Editorial Gold + Cream Serif Stamp (`@serif-stamp`, Template: `animations/_fx_library/serif-stamp/`)**:
    - At `top=34%, left=4%, width=62%`, fades in `#C6A254` gold italic `"serif"` (`64px`), then stamps `#F0EADE` cream uppercase Georgia letters (`"S T A M P"`, `164px` @ 1080p / `328px` @ 4K) from `scale: 1.45 -> 1.0` (`0.14s power4.out`, `stagger: 0.06s` + `@asset/audio/sfx/paper_thock.wav`).
54. **Rule TH54 — App Icon Rose-Pink X-Strike & Drop (`@icon-strike`, Template: `animations/_fx_library/icon-strike/`)**:
    - **Top-Zone `1.00x` Lock**: Pops competitor icons (`@asset/logos/apps/capcut.svg`, `edits.svg`) at `top=24%, left=8%–26%`, slashes each with a `12px` `#C06672` diagonal line (`scaleX: 0 -> 1` over `0.18s` + `@asset/audio/sfx/marker_squeak.wav`), reveals italic `"strike."` at `top=14%`, and drops the slashed icons off-screen (`y: 0 -> 520, rotation: -28deg, power2.in`).
55. **Rule TH55 — 3-Row Film Strip Grease-Pencil Sheet (`@grease-pencil`, Template: `animations/_fx_library/grease-pencil/`)**:
    - **Top-Zone `1.00x` Lock**: Displays a `#F0EADE` contact sheet (`top=12%, left=4%, width=60%`) with `#C06672` italic header `"dead air"` and 3 sprocketed film-strip rows, slashing dead-air frames with `#C06672` grease-pencil `✕` marks (`stagger: 0.18s` + `@asset/audio/sfx/marker_squeak.wav`).
56. **Rule TH56 — Split Video Preview & Chapter Card (`@video-card`, Template: `animations/_fx_library/video-card/`)**:
    - **Top-Zone `1.00x` Lock**: Renders a `60%`-width card at `top=14%, left=4%` (`24px` radius, `#2A5240` border): top half shows a split raw-vs-finished video pane (`280px` height) with a centered `#F0EADE` play button; bottom half (`#123024` forest green) shows Georgia title `"Video card"`, `#4ADE80` active chapter `"02 The finished reel"`, and a `#C6A254` gold pill badge (`@asset/audio/sfx/pop.wav`).

## Rule TH57 — Executable Plan and Capability Contract

Use schema version 1 and `editor validate --check-files` before rendering. Approval must identify the reviewed plan hash. Unknown effects, non-positive speeds, subframe keeper ranges, missing assets and unsupported geometry/depth combinations fail. Catalogue demos require explicit composition and `demo: true`; they are not certified source-video effects.

## Rule TH58 — Revision Evidence and Scoped Memory

Open `editor handoff` before editing. Record commands, submitted/compiled EDLs, failures, feedback, rejected decisions and fixes in project history. A resolution must reference a rendered descendant and saved review evidence. Save specific lessons at project/category/universal scope with evidence; never turn a one-off preference into a universal default automatically.
