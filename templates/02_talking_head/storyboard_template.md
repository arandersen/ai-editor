# Storyboard Template — Category 2: Talking Head (`FeedMedia Notion Effects + Antigravity M4`)

> **Rulebook**: [`.agents/skills/youtube-edit/references/editing-rules-talking-head.md`](../../.agents/skills/youtube-edit/references/editing-rules-talking-head.md)
> **Notion Rule #1 (`@storyboard-first`)**: Before touching footage or rendering, write this storyboard table (one row per beat with time, exact spoken words, what's on screen, `@shortcut`, and tool). Do NOT render until approved.

## Project Summary
- **Project Folder**: `raw/<Project Name>/` $\rightarrow$ `renders/final/<Project Name>/`
- **Resolution & FPS**: `2160×3840` (4K 9:16 Vertical) or `3840×2160` (4K 16:9 YouTube) @ `60fps`
- **Caption Style**: `@coral-captions` (3 words at `61.5%` height, `#D97757` coral box on active word) OR `@one-word-captions`
- **Jump-Cut Rule**: `@jump-cuts` (strip pauses `> 0.22s`, alternate `1.00x` / `1.15x` at `y=42%` eye-line, auto-lock `1.00x` when top cards appear)

---

## Beat-by-Beat Storyboard Table

| Beat # | Raw Time (`s`) | Output Time (`s`) | Framing | Your Exact Spoken Words | `@shortcut` Effect | What's On Screen (Visual Spec) | Tool / Engine |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `0.85–4.40` | `0.00–3.55` | `1.00x` | *"Here is how I edit every effect in my videos automatically..."* | `@text-behind-head`, `@coral-captions` | 2-line title `"Text behind / your head"` (`#F4F4F2`, `y=20%, 27%`) sandwiched between background and Apple Vision person cutout | `person_cutout.swift` + `talking_head_overlays.swift` |
| **2** | `4.75–8.90` | `3.55–7.70` | `1.15x` (`y=42%`) | *"First, when I mention FFmpeg, its icon pops up..."* | `@tool-label`, `@whip-pan` | At `5.60s`: FFmpeg logo (`220px`) fades up at `y=61.5%` (12f), slides left while `"FFmpeg"` slides out right (12f). Whip-pan out (6f `8%` slide + `50px` blur) | `talking_head_overlays.swift` + FFmpeg `boxblur` + `pop.wav` / `whoosh.wav` |
| **3** | `9.30–14.50` | `7.70–12.90` | `1.00x` *(Top Guard)* | *"And for open-source repos, I type a single prompt..."* | `@repo-card`, `@prompt-bar` | Top `85%` GitHub Dark card (`#0D1117`) at `9.50s`, followed by `#2B2B2B` Prompt Bar (`92.6%` width at `y=22.5%`) with `#D97757` send button at `12.60s` | `talking_head_overlays.swift` + `talking_head_engine.py` |
