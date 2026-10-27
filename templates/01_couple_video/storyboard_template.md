# Storyboard Template — Category 1: Couple Video (`9:16 Vertical Game / Challenge`)

> **Rulebook**: [`.agents/skills/youtube-edit/references/editing-rules-couple.md`](../../.agents/skills/youtube-edit/references/editing-rules-couple.md)
> **Instructions for AI Conductor (Gemini 4 Argon)**: Always fill out and present this Storyboard Table after transcribing and watching the raw clip. Do NOT start full 4K rendering until the user approves this storyboard.

## Project Summary
- **Project Folder**: `raw/<Project Name>/` $\rightarrow$ `renders/final/<Project Name>/`
- **Brand Kit & Resolution**: [`templates/01_couple_video/brand_kit.json`](./brand_kit.json) — Native 4K (`2160×3840`), `@couple-grade` color grading, **`1.10x` base speed** (`@couple-speed-1.1x`)
- **Players**: Left = **Angel** (`x=610` in 4K) | Right = **Arthur** (`x=1520` in 4K)
- **Hook Title (`0:00`)**: Line 1: `challenge` (`y=380`) | Line 2: `[GAME TITLE] 🔥` (`y=560`, `@hook-bean-boozle` or `@couple-hook-behind-head`)
- **Background Music**: `audio/music/nocturne_op9_in_eb.wav` (Chopin Nocturne in E-flat major, Op. 9, No. 2)
- **Projected Final Duration**: `~2:15` (`< 2:30` / `150.0s` strict ceiling)

---

## Beat-by-Beat Storyboard Table

| Beat # | Raw Time (`s`) | Output Time (`s`) | Speed | Speaker & Exact Spoken Words | `@shortcut` Keyword(s) | Top Header / Head-Pop (`brand_kit.json`) | 🎨 Flow / Cutout / 60fps Animation | Camera & Audio/SFX |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | `0.98–5.20` | `0.00–3.84` | `1.10x` | **Angel**: *"Hari ini kita main challenge..."* | `@hook-bean-boozle`, `@couple-speed-1.1x`, `@wide`, `@couple-grade` | `challenge` (`y=380`) / `NAMA GAME 🔥` (`y=560`, no bottom caption) | Optional `person_cutout.swift` (`@couple-hook-behind-head`) + staggered rise | Steady `1.00x` wide; Chopin `-20dB` |
| **2** | `5.50–35.50` | `3.84–11.34` | `4.00x` | *(30s Card Memorization Phase)* | `@timelapse-4x`, `@clock-tick` | `HAFAL KARTU: 30 DETIK ⏱️` (`#FFD60A`, no bottom caption) | 60fps slide-down header (`180ms`) | `4.0x` timelapse + `clock_ticking.wav` |
| **3** | `36.00–52.00` | `11.34–22.37` | `1.45x` | **Arthur**: *"Aku cari traktor biru... Ini!"* | `@header-cari` $\rightarrow$ `@header-dapat`, `@one-word-captions` | `ARTHUR: CARI TRAKTOR BIRU 🚜` (`#FFFFFF`) $\rightarrow$ `ARTHUR: DAPAT TRAKTOR BIRU! 🚜` (`#4ADE80`) | Optional `@flow-sticker-pop` (`broll/flow/tractor.png`) + 1-word `85ms` spring pop | Uncut search (`1.45x`) + `correct_ding.wav` on flip |
| **4** | `52.20–55.00` | `22.37–25.17` | `1.00x` | **Arthur**: *"Gua tadinya mau bilang santet!"* | `@bw-zoom-arthur`, `@meme-what` | `@head-pop-arthur`: `SANTET?! 💀` (`#38BDF8` at `x=1520, y=1020`) | Optional `@flow-sticker-pop` (`broll/flow/santet.png`) + `5-frame` B&W zoom | Fast zoom `1.15x->2.15x` B&W + `What_ Meme.mp4` (`+14dB`) |
| **5** | `110.0–125.0` | `115.0–126.1` | `1.35x` | **Angel**: *"Satu, dua, tiga... sebelas!"* | `@header-tally` $\rightarrow$ `@winner-parade` | `HITUNG POIN! 🃏` (`#FFD60A`) $\rightarrow$ `ANGEL: 11 POIN — DOUBLE GUYS! ✌️🎉` (`#FFD60A`) | 4K 3D `confetti_loop.mov` (450+ particles, zero emojis over faces) | Steady `1.00x` wide + `party_cheer.wav` (`1.1x`) |
