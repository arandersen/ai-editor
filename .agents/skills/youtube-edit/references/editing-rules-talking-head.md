# Talking Head Editing Rules — Antigravity (Gemini 4 Argon) + FeedMedia Notion Effect System

> **Domain**: Solo / Creator Talking Head Videos (9:16 Vertical Reels/Shorts & 16:9 YouTube) combining our baseline retention rules, the **14 FeedMedia Notion Talking Head Effects** adapted for Antigravity on Apple Silicon M4, and our battle-tested **Couple Video precision standards** (10ms RMS acoustic onset sync, native 4K CRF 14 Rec.709, Swift CoreText + HyperFrames overlays, and Subagent QC).
> **Master Index**: [editing-rules.md](./editing-rules.md) | **Sibling Rulebooks**: [editing-rules-couple.md](./editing-rules-couple.md) · [editing-rules-animation.md](./editing-rules-animation.md)

---

## I. Collaborative Workflow & Storyboard-First Protocol (Rules TH1–TH3)

1. **Rule TH1 — Storyboard First Before Any Render (Notion Effect #1)**:
   - Before cutting footage or rendering overlays, run `./scripts/transcribe.sh` (with 10ms RMS acoustic onset verification) and `./scripts/inspect_video.sh` + `view_file` to watch the raw delivery.
   - Present a **Beat-by-Beat Storyboard Table** (`Beat # | Raw Time | Output Time | Exact Spoken Words | Visual Effect / What's On Screen | Tool/Engine (FFmpeg / Swift / HyperFrames)`).
   - **Approval Gate**: Wait for user approval or tweaks on the storyboard table before executing the full master render (unless the user explicitly asks to one-shot render).
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
