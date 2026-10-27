# Storyboard Template — Category 2: Talking Head (`FeedMedia Notion 14 Effects via HyperFrames + Researcher + Google Flow`)

> **Rulebook**: [`.agents/skills/youtube-edit/references/editing-rules-talking-head.md`](../../.agents/skills/youtube-edit/references/editing-rules-talking-head.md)
> **5-Phase Talking Head Flow**:
> 1. **Understand Raw Video** (`transcribe.sh` + 10ms RMS + `inspect_video.sh` + `view_file`)
> 2. **Discuss Creative Direction** (Align on keeper script, hook, and pacing)
> 3. **Storyboard First** (Fill out this table combining **Researcher**, **Google Flow MCP**, and **HyperFrames** — wait for approval before rendering!)
> 4. **Build Assets & HyperFrames Motion Graphics** (`npx hyperframes` replaces Notion's Remotion 1-to-1; `person_cutout.swift` runs *only* if placing text behind head)
> 5. **Master FFmpeg Assembly & QC** (`<0.22s` jump cuts, `1.00x/1.15x` framing, `-14 LUFS` audio, Native 4K export)

## Project Summary
- **Project Folder**: `raw/<Project Name>/` $\rightarrow$ `renders/final/<Project Name>/`
- **Resolution & FPS**: `2160×3840` (4K 9:16 Vertical) or `3840×2160` (4K 16:9 YouTube) @ `60fps`
- **Motion Graphics Engine**: **HyperFrames (`npx hyperframes` HTML/CSS/GSAP)** *(1-to-1 replacement for Notion's Remotion)*
- **Person Cutout (`person_cutout.swift`)**: Used **only** on beats with `@text-behind-head` or `@magazine-cover`

---

## Unified Beat-by-Beat Talking Head Storyboard Table

| Beat # | Raw Time (`s`) | Output Time (`s`) | Framing (`1.0x`/`1.15x`) | Exact Spoken Words *(Keeper Script)* | `@shortcut` Effect | 🔎 Researcher (`Chrome` / `yt-dlp`) | 🎨 Google Flow MCP (`@flow-image` / `@flow-video`) | ⚡ HyperFrames Motion Graphic (`HTML/CSS/GSAP` Spec) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1 (Hook)** | `0.85–4.40` | `0.00–3.55` | `1.00x` | *"Here is how I edit every effect in my videos automatically..."* | `@text-behind-head`, `@coral-captions` | — | — | **HyperFrames** 2-line title `"TEXT BEHIND / YOUR HEAD"` (`#F4F4F2`, `y=20%, 27%`, 12f `power3.out` rise `2%`, Line 2 delayed 4f) sandwiched behind Apple Vision `person_cutout.mov` |
| **2** | `4.75–8.90` | `3.55–7.70` | `1.15x` (`y=42%`) | *"First, when I mention FFmpeg, its icon pops up..."* | `@tool-label`, `@whip-pan` | Fetch official FFmpeg & HyperFrames SVG logos | — | **HyperFrames** at `5.60s`: Logo (`220px`) fades up at `y=61.5%` (12f) $\rightarrow$ slides left while `"FFmpeg"` slides out right (12f) + `pop.wav`. Whip-pan out (6f `8%` slide + `50px` blur) |
| **3** | `9.30–14.50` | `7.70–12.90` | `1.00x` *(Top Guard)* | *"And for open-source repos, I type a single prompt..."* | `@repo-card`, `@prompt-bar`, `@real-screenshot` | Capture live GitHub metadata & 4K Retina screenshot via `capture_broll.mjs` | — | **HyperFrames** top `85%` `#0D1117` GitHub card (12f rise) + `#2B2B2B` Prompt Bar (`92.6%` width at `y=22.5%`) typing prompt with `#D97757` coral send button |
| **4** | `15.10–19.80` | `12.90–17.60` | Full / PIP | *"Instead of drowning in a messy 50-track timeline at 2 AM..."* | `@flow-video`, `@pause-explain` | — | **Veo 3.1**: *"Cinematic shot of overwhelmed editor at 2am staring at glowing timeline"* | **HyperFrames** frames clip inside `@pause-explain` PIP (`54%` top-left with timecode $\rightarrow$ freeze on `click.wav` $\rightarrow$ 12f shrink to `24%` left) |
