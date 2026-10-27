---
name: hyperframes
description: >-
  Author, lint, preview, and render deterministic 4K HTML/CSS/GSAP video animations
  and motion graphics overlays using HeyGen's HyperFrames CLI. Use this skill when
  generating animated titles, lower-thirds, data visualizations, kinetic typography,
  or full-screen explainer scenes for video edits.
---

# HyperFrames — Deterministic HTML/CSS/GSAP Video Animation Skill

HyperFrames (`heygen-com/hyperframes`) renders standard web compositions (HTML, CSS, SVG, Canvas, and GSAP) frame-by-frame in headless Chrome and encodes them into frame-accurate MP4, WebM, or ProRes MOV video files via FFmpeg.

---

## Core CLI Commands

Always ensure `/opt/homebrew/bin` is on `PATH` when invoking `npx hyperframes`:

```bash
export PATH="/opt/homebrew/bin:$HOME/.local/bin:$PATH"

# 1. Initialize a new animation composition in animations/<name>
npx hyperframes init animations/<name> --example blank

# 2. Lint & check layout/accessibility/contrast before rendering
npx hyperframes lint animations/<name>
npx hyperframes check animations/<name>

# 3. Launch live browser preview (interactive Studio UI)
npx hyperframes preview animations/<name>

# 4. Render to MP4 (opaque full-screen scene)
npx hyperframes render animations/<name> --output broll/<name>.mp4

# 5. Render transparent overlay (lower-thirds, badges, callouts)
npx hyperframes render animations/<name> --format webm --output broll/<name>.webm
npx hyperframes render animations/<name> --format mov --output broll/<name>.mov
```

---

## Authoring Rules for HyperFrames Compositions

1. **Standard Composition Structure**:
   Every HyperFrames project in `animations/<scene_name>/` contains an `index.html` with a root container declaring dimensions, frame rate, and duration in seconds:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
     <meta charset="UTF-8" />
     <title>Scene Composition</title>
     <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
     <style>
       :root {
         --bg-dark: #0A0D14;
         --text-primary: #F8FAFC;
         --accent-primary: #38BDF8;
         --accent-highlight: #FACC15;
         --accent-success: #4ADE80;
       }
       * { box-sizing: border-box; margin: 0; padding: 0; }
       body {
         width: 1920px;
         height: 1080px;
         overflow: hidden;
         background: var(--bg-dark);
         font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
         color: var(--text-primary);
       }
       #stage {
         width: 1920px;
         height: 1080px;
         position: relative;
         display: flex;
         align-items: center;
         justify-content: center;
         padding: 108px 192px; /* 10% safe area */
       }
     </style>
   </head>
   <body>
     <div id="stage" data-composition-id="main" data-composition data-start="0" data-width="1920" data-height="1080" data-fps="60" data-duration="4.0">
       <!-- Animated elements here -->
     </div>
     <script>
       // Expose a paused master GSAP timeline on both HyperFrames 0.8.180+ (__timelines["main"]) and legacy (__hyperframes_timeline)
       window.__timelines = window.__timelines || {};
       const tl = gsap.timeline({ paused: true });
       window.__timelines["main"] = tl;
       window.__hyperframes_timeline = tl;
     </script>
   </body>
   </html>
   ```

2. **Deterministic Frame Stepping**:
   - Never rely on `setTimeout`, `requestAnimationFrame` loops with wall-clock `Date.now()`, or unseeded `Math.random()`.
   - Bind all animations to a single GSAP timeline (`gsap.timeline()`) or standard CSS `@keyframes` so headless Chrome can pause and step through every frame deterministically.

3. **Timestamp Synchronization with Parakeet**:
   - Before writing a HyperFrames animation for a video segment, inspect the word-level timestamps in `transcripts/<video>.json`.
   - Calculate the relative offset (`word_timestamp - segment_start_timestamp`) and schedule the GSAP tween at that exact second mark (`tl.to(el, { ... }, relativeOffset)`).

4. **Visual Polish Checklist**:
   - Add subtle background depth (radial gradient glow + subtle grid or noise overlay).
   - Keep text hierarchy clear: maximum 3 font sizes on screen at once, high contrast, and generous padding inside cards.
   - Always include both an **entrance animation** (`0.0s–0.4s`), a **micro-motion hold** (subtle float or highlight sweep while being read), and a clean **exit animation** if it is an overlay.
