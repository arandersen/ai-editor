# AI Video Editor — Gemini 4 Argon (Conductor) + Gemini 3 Flash (Editor) Master System

> **Master Reference & `@shortcut` Dictionary**: Always read [`README.md`](./README.md) for the complete `@shortcut` Keyword Dictionary and 3-Category Template structure.

---

## 1. Conductor + Editor Multi-Agent Architecture

```mermaid
flowchart TB
    subgraph START["Step 1: 3-Category Intake"]
        CAT["Ask User to Pick Category:\n[1] Couple Video (9:16 Game)\n[2] Talking Head (Notion 14 Effects)\n[3] Animation / Motion Graphics (HyperFrames / Vox)"]
    end

    subgraph WATCH["Step 2: Watch Video + Local Speech-to-Text"]
        TRANS["🎙️ scripts/transcribe.sh (--lang en|id)\nLocal Apple Silicon Metal Whisper / Parakeet\n+ 10ms RMS Onset + Stereo L/R Speaker Tag"]
        INSPECT["👁️ scripts/inspect_video.sh (--table-crop)\nFull-Duration 5x6 Contact Sheet + <15MB Vision Proxy MP4\n+ Gemini Native view_file Video+Audio Watching"]
    end

    subgraph STORYBOARD["Step 3: Discuss & Storyboard First"]
        SHORTCUTS["⌨️ User & Conductor Align on @shortcut Edits\n(@text-behind-head, @coral-captions, @tool-label, @whip-pan, etc.)"]
        SB_TABLE["📋 Generate Storyboard Table FIRST\n(Researcher Real Assets + Google Flow MCP + HyperFrames)\n⏸️ Wait for User Approval Before Rendering"]
    end

    subgraph EXECUTE["Step 4: Conductor (Argon) + Editor (Flash) Execution"]
        LINT["✅ scripts/lint_edl.py\nPre-Render Flash-Proof Rule Validation"]
        FLASH["⚡ Editor Agent (Gemini 3.8 Flash / Local Scripts)\nExecutes HyperFrames 60fps HTML/CSS/GSAP, Flow MCP,\nperson_cutout.swift (behind-head only) & FFmpeg 4K"]
    end

    subgraph REVISION["Step 5: Post-Render Revision -> Flash-Proof Rule Training"]
        REV_FIX["🔧 Execute User Revision & Re-Render Immediately"]
        REV_RULE["📐 Write Parameterized Rule (Exact px / sec / dB / hex / code)\ninto editing-rules-<category>.md + editing-rules.md + lint_edl.py\nso Gemini 3.8 Flash Never Repeats the Mistake"]
    end

    CAT --> TRANS
    CAT --> INSPECT
    TRANS --> SHORTCUTS
    INSPECT --> SHORTCUTS
    SHORTCUTS --> SB_TABLE
    SB_TABLE --> LINT
    LINT --> FLASH
    FLASH --> REV_FIX
    REV_FIX --> REV_RULE
```

---

## 2. Mandatory Always-On Rules for the AI Conductor & Editor

### Rule A: Every New Project Conversation Starts With the 3-Category Choice & Storyboard First
1. **Step 1 — Offer the 3 Video Categories**:
   Whenever starting a new video project or conversation in this workspace, ask the user which of the **3 Categories** we are building (if not already specified):
   - **`[1] Couple Video`** (`9:16 Vertical Game / Challenge` — loads [`.agents/skills/youtube-edit/references/editing-rules-couple.md`](./.agents/skills/youtube-edit/references/editing-rules-couple.md) & [`templates/01_couple_video/`](./templates/01_couple_video/))
   - **`[2] Talking Head`** (`Solo Creator + FeedMedia Notion 14-Effect System` — loads [`.agents/skills/youtube-edit/references/editing-rules-talking-head.md`](./.agents/skills/youtube-edit/references/editing-rules-talking-head.md) & [`templates/02_talking_head/`](./templates/02_talking_head/))
   - **`[3] Animation / Motion Graphics`** (`HyperFrames 4K & Vox Editorial Collage` — loads [`.agents/skills/youtube-edit/references/editing-rules-animation.md`](./.agents/skills/youtube-edit/references/editing-rules-animation.md) & [`templates/03_animation_motion_graphics/`](./templates/03_animation_motion_graphics/))
2. **Step 2 — Watch the Video + Run Local Speech-to-Text First**:
   - Run `./scripts/transcribe.sh "raw/<Project>/<clip>.MOV" --lang en|id` (runs local Apple Silicon Metal Whisper `small.en` / `base` or `parakeet-mlx` offline + [`scripts/acoustic_onset.py`](./scripts/acoustic_onset.py) for 10ms RMS onset snapping and Left/Right speaker tagging).
   - Run `./scripts/inspect_video.sh "raw/<Project>/<clip>.MOV"` (adding `--table-crop` for card/prop games), which generates **both** `renders/drafts/<clip>_contact_sheet.jpg` **and** a lightweight `< 15 MB` `renders/drafts/<clip>_vision_proxy.mp4` (`540p H.264 + AAC` with burned timecode).
   - **Always call `read_file` on both `<clip>_contact_sheet.jpg` AND `<clip>_vision_proxy.mp4`** so you genuinely watch and hear the full video (even when the raw 4K `.MOV` exceeds `100 MB`).
   - Present a crisp summary of the raw footage takes and timestamps so the user can discuss and specify edits using the `@shortcut` keywords in [`README.md`](./README.md).
3. **Step 3 — ALWAYS Present the Storyboard Table Before Rendering**:
   - Translate the user's requested `@shortcut` edits into the category's **Beat-by-Beat Storyboard Table** (`templates/0X_.../storyboard_template.md`) so the user can visualize every beat, spoken line, Researcher screenshot, Google Flow asset, and HyperFrames motion graphic before rendering.
4. **Step 4 — Conductor (`Gemini 4 Argon`) + Editor (`Gemini 3 / 3.8 Flash`) Division of Labor**:
   - **Gemini 4 Argon (The Conductor / Creative Director)** watches the video, designs the Storyboard and EDL JSON, runs `python3 ./scripts/lint_edl.py`, and verifies the final render.
   - **Gemini 3 / 3.8 Flash (The Editor)** can be invoked via `invoke_subagent(Model="flash")` (or run directly) to execute the deterministic HyperFrames/Swift/Python/FFmpeg scripts following the exact `@shortcut` specifications in [`README.md`](./README.md).

### Rule B: Image & Video Generation via Google Flow MCP (`GTAI-1/flow-mcp`)
Whenever bespoke B-roll images (**Nano Banana / Imagen 4K**) or AI video clips (**Veo 3.1**) are needed (`@flow-image` / `@flow-video`), use the configured **Google Flow MCP** (`tools/flow-mcp`) to generate assets at $0 API cost into `broll/flow/`, applying the mandatory unification pass when used in Vox-style explainers.

### Rule C: Mandatory End-of-Video Revision $\rightarrow$ Flash-Proof Rule & Linter Training Protocol (NEVER SKIP)
Because **Gemini 3.8 Flash** is a lighter, faster model than **Gemini 4 Argon**, it cannot rely on vague aesthetic judgment—it requires **explicit, parameterized rules and automated linter checks**. Therefore, at the end of every video when the user gives a revision or fix:
1. **Execute the Revision Immediately** and re-render the video.
2. **Write a Flash-Proof Parameterized Rule** into the matching domain rulebook ([`editing-rules-couple.md`](./.agents/skills/youtube-edit/references/editing-rules-couple.md), [`editing-rules-talking-head.md`](./.agents/skills/youtube-edit/references/editing-rules-talking-head.md), or [`editing-rules-animation.md`](./.agents/skills/youtube-edit/references/editing-rules-animation.md)):
   - Never write vague advice (*"make captions look better"* or *"don't overlap"*).
   - Always write **Anti-Pattern vs. Exact Numbers** (exact pixel coordinates, font size, hex color, duration in seconds, dB level, or exact FFmpeg/GSAP formula).
3. **Add a Mechanical Check to [`scripts/lint_edl.py`](./scripts/lint_edl.py)** whenever the revision involves a measurable constraint (duration, zoom vs. top-card collision, word count, safe zone, audio level) so Flash is blocked from repeating the mistake pre-render.
4. **Log in the Master Feedback Changelog & `@shortcut` Dictionary**:
   - Append the revision to the **Master Feedback Changelog** at the bottom of [`.agents/skills/youtube-edit/references/editing-rules.md`](./.agents/skills/youtube-edit/references/editing-rules.md) and update [`README.md`](./README.md) if a new `@shortcut` was added or refined.

### Rule D: Environment PATH & Per-Project Folder Organization
- Always ensure Homebrew and local binaries are on `PATH`:
  ```bash
  export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"
  ```
- Always mirror `raw/<Project Name>/` across `renders/final/<Project Name>/`, `renders/drafts/<Project Name>/`, `transcripts/<Project Name>/`, and `broll/<Project Name>/`.
