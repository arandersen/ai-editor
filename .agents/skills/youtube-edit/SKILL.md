---
name: youtube-edit
description: >-
  End-to-end automated AI video editing pipeline organized into 3 categories:
  (1) Couple Video (9:16 games), (2) Talking Head (FeedMedia Notion 14-effect system),
  and (3) Animation / Motion Graphics (HyperFrames 4K & Vox Editorial Collage).
  Uses a Storyboard-First flow, @shortcut keywords in README.md, Conductor (Gemini 4 Argon) +
  Editor (Gemini 3 Flash) multi-agent execution, Parakeet/Whisper + 10ms RMS acoustic onset,
  Apple Vision person cutouts, Swift CoreText overlays, Free Audio MCP, Google Flow MCP, and FFmpeg 4K.
---

# YouTube Edit — 3-Category Storyboard-First AI Video Editing Skill

> [!IMPORTANT]
> **Before starting any edit**, always read:
> 1. [`README.md`](../../../README.md) — For the **Master `@shortcut` Keyword Dictionary** and **4-Step Storyboard-First Flow**.
> 2. [`references/editing-rules.md`](./references/editing-rules.md) — Master Router & Universal Rules (`U1–U8`).
> 3. The **Domain Rulebook & Template** matching the chosen category:
>    - **Category 1 — Couple Video**: [`references/editing-rules-couple.md`](./references/editing-rules-couple.md) (`C1–C15`) + [`templates/01_couple_video/`](../../../templates/01_couple_video/)
>    - **Category 2 — Talking Head**: [`references/editing-rules-talking-head.md`](./references/editing-rules-talking-head.md) (`TH1–TH25`) + [`templates/02_talking_head/`](../../../templates/02_talking_head/)
>    - **Category 3 — Animation / Motion Graphics**: [`references/editing-rules-animation.md`](./references/editing-rules-animation.md) (`AM1–AM11`) + [`templates/03_animation_motion_graphics/`](../../../templates/03_animation_motion_graphics/)

---

## The Mandatory 4-Step Storyboard-First Execution Runbook

### Step 1: Select Video Category (3 Options)
If the user has not yet specified the video type, present the 3 options:
1. **`[1] Couple Video`** (`9:16 Vertical Game / Challenge` — `Angel` & `Arthur`)
2. **`[2] Talking Head`** (`Solo Creator / Tutorial` — **FeedMedia Notion 14-Effect System**)
3. **`[3] Animation / Motion Graphics`** (`HyperFrames 4K HTML/CSS/GSAP & Vox Editorial Collage`)

### Step 2: Ingest, Acoustic Transcribe & Watch Raw Video
1. **Transcribe with 10ms RMS Acoustic Onset & Stereo Diarization**:
   ```bash
   # English / Tech Talking Head:
   ./scripts/transcribe.sh "raw/<Project>/<clip>.MOV" --lang en

   # Indonesian / Bilingual Couple Game:
   ./scripts/transcribe.sh "raw/<Project>/<clip>.MOV" --lang id
   ```
   Inspect `transcripts/<Project>/<clip>_acoustic.json` (which contains `first_speech_onset_sec`, 10ms RMS-snapped `start`/`end`, `is_stressed`, and `speaker`).
2. **Inspect Full-Duration Contact Sheet & Watch Natively via Vision Proxy MP4**:
   ```bash
   ./scripts/inspect_video.sh "raw/<Project>/<clip>.MOV" [--table-crop]
   ```
   Always call `read_file` on **both** `renders/drafts/<clip>_contact_sheet.jpg` **and** `renders/drafts/<clip>_vision_proxy.mp4` (`< 15 MB` 540p H.264+AAC with burned timecode) so you genuinely watch and hear the full video even when the raw 4K `.MOV` exceeds `100 MB`.
3. **Summarize Raw Takes & Discuss With User**:
   Report the key takes, retakes, timestamps, and structure so the user can discuss creative direction and specify their desired edits using the `@shortcut` keywords in [`README.md`](../../../README.md).

### Step 3: Translate `@shortcut` Edits into the Visual Storyboard Table FIRST
- Never jump straight to a final render without showing the storyboard first (unless explicitly told to one-shot render).
- Fill out the category's storyboard template ([`templates/01_couple_video/storyboard_template.md`](../../../templates/01_couple_video/storyboard_template.md), [`templates/02_talking_head/storyboard_template.md`](../../../templates/02_talking_head/storyboard_template.md), or [`templates/03_animation_motion_graphics/storyboard_template.md`](../../../templates/03_animation_motion_graphics/storyboard_template.md)) mapping every beat to its exact spoken words, `@shortcut` keyword, Researcher real asset, Google Flow AI asset, and HyperFrames motion graphic.

### Step 4: Lint EDL, Execute Build (Conductor + Flash Editor) & Run QC
1. **Lint the EDL JSON**:
   ```bash
   python3 ./scripts/lint_edl.py --edl renders/drafts/<Project>/edl.json --category couple|talking_head|animation
   ```
2. **Execute Category Engine (Directly or via `invoke_subagent(Model="flash")`)**:
   - **Category 1 (Couple Video)**: Run the project builder (`scripts/build_<project>.py`) with Swift 4K overlays, 1-word acoustic captions, Chopin Nocturne in E-flat major (`audio/music/nocturne_op9_in_eb.wav`), and 4K ProRes 4444 confetti (`confetti_loop.mov`).
   - **Category 2 (Talking Head)**:
     - Extract Apple Vision person cutouts **only** when `@text-behind-head` or `@magazine-cover` is used:
       ```bash
       swift ./scripts/person_cutout.swift --input "raw/<Project>/<clip>.MOV" --start 0.85 --end 4.40 --output "broll/<Project>/cutout.mov"
       ```
     - Render all 14 FeedMedia Notion motion graphics (`@coral-captions`, `@tool-label`, `@repo-card`, `@prompt-bar`, `@color-slider`, `@moody-grade`, `@wall-of-reels`, `@pause-explain`) via **HyperFrames (`npx hyperframes` HTML/CSS/GSAP)** + FFmpeg master assembly (`scripts/talking_head_engine.py`).
   - **Category 3 (Animation / Motion Graphics)**:
     - Source real archival photos ($\ge 1000\text{px}$) via `scripts/fetch_real_assets.py` or generate bespoke visuals via **Google Flow MCP** (`@flow-image` / `@flow-video`), run the unification pass (`scripts/prepare_runner_cutouts.py`), lint with `npx hyperframes lint`, and render via `npx hyperframes render`.
3. **Step 5: Post-Render Revision $\rightarrow$ Flash-Proof Rule & Linter Training Loop (Mandatory)**:
   - Run `./scripts/inspect_video.sh "renders/final/<Project>/<name>.mp4"` + `read_file` on the `<15MB` Vision Proxy MP4 & Contact Sheet + `caption-qc-reviewer` subagent check.
   - Whenever the user gives a revision or fix at the end of a video:
     1. **Fix & Re-Render Immediately**.
     2. **Write a Flash-Proof Parameterized Rule** (exact px, seconds, hex colors, dB, FFmpeg/GSAP formulas—never vague prose) into the category rulebook (`editing-rules-couple.md`, `editing-rules-talking-head.md`, or `editing-rules-animation.md`).
     3. **Add a Pre-Render Check in `scripts/lint_edl.py`** so **Gemini 3.8 Flash** cannot repeat the error on future videos.
     4. **Log in the Master Feedback Changelog** ([`references/editing-rules.md`](./references/editing-rules.md)) and [`README.md`](../../../README.md).
