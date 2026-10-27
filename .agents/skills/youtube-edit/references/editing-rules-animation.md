# Animation & Motion Graphics Editing Rules — HyperFrames 4K & Vox Editorial Collage

> **Domain**: Deterministic 4K HTML/CSS/GSAP Motion Graphics (`npx hyperframes`), Full-Screen Data/Architecture Explainers, and Vox-Style Tactile Editorial Paper-Collage Animations (`VOX-TEST_race`).
> **Master Index**: [editing-rules.md](./editing-rules.md) | **Sibling Rulebooks**: [editing-rules-couple.md](./editing-rules-couple.md) · [editing-rules-talking-head.md](./editing-rules-talking-head.md)

---

## I. HyperFrames 4K Core Engineering & Design Standards (Rules AM1–AM6)

1. **Rule AM1 — Data, Comparisons & Multi-Step Lists Always Become Graphics**:
   - Whenever a script or speaker presents a numerical formula, cost breakdown (e.g. `$250 -> $0`), benchmark comparison, system architecture, or multi-step list, author a deterministic HyperFrames composition (`animations/<scene_name>/index.html`) rather than leaving plain talking head or static text.
   - The first 3 seconds (The Hook) of any explainer must feature kinetic typography, an animated visual metaphor, or a choreographed title card.
2. **Rule AM2 — Deterministic Seekable GSAP Timeline Contract (`HyperFrames 0.8.180+`)**:
   - Declare the root composition container with `data-composition-id="main"`, `data-start="0"`, `data-duration="<seconds>"`, `data-width="1080"` (or `2160`/`3840`), and `data-height="1920"` (or `3840`/`2160`).
   - Register a single paused master GSAP timeline on `window.__timelines["main"] = gsap.timeline({ paused: true })` (plus `window.__hyperframes_timeline = tl` for backward compatibility).
   - **Strict Determinism**: Drive 100% of motion and text/counter updates via the master GSAP timeline—never use `setInterval`, `setTimeout`, `requestAnimationFrame` loops, or unseeded `Math.random()`.
3. **Rule AM3 — Brand Typography & High-Contrast Palette**:
   - For dark-mode tech explainers, use a unified CSS variable palette (`--bg-dark: #0A0D14`, `--text-primary: #F8FAFC`, `--accent-primary: #38BDF8`, `--accent-highlight: #FACC15`, `--accent-coral: #D97757`, `--accent-success: #4ADE80`) with geometric sans-serif (`Inter` / `Plus Jakarta Sans`) and monospace (`JetBrains Mono`) for code/metrics.
   - For Vox-style editorial explainers, use warm archival paper tones (`--paper-cream: #F4EDDE`, `--ink-dark: #191713`, `--marker-yellow: #FFD51F`, `--navy-slate: #141B2D`).
4. **Rule AM4 — Safe Title Margins (Zero Mobile UI Clipping)**:
   - Keep all animated typography, cards, and data labels inside a **`10%` title-safe margin** (`192px` horizontal / `108px` vertical on 16:9 1080p; `108px` horizontal / `220px` vertical on 9:16 1080×1920; `216px` / `440px` on 9:16 4K `2160×3840`) so nothing is clipped by YouTube/Reels/TikTok player chrome.
5. **Rule AM5 — Snappy Easing Curves & Stop-Motion Tactility**:
   - Use `power3.out` (`cubic-bezier(0.215, 0.61, 0.355, 1)`) or `back.out(1.4)` for crisp `0.20s–0.35s` entrances and `power2.inOut` for layout transitions.
   - For tactile paper-collage character movements (e.g., runners striding or cards dealing), use stepped easing (`steps(3)` or `steps(4)`) paired with physical rotation wobble (`±3deg`) to achieve authentic stop-motion editorial feel.
6. **Rule AM6 — Mandatory Lint & Contact-Sheet Visual Verification Before Master Render**:
   - Always run `npx hyperframes lint` before rendering to catch overflow, contrast, or timeline errors.
   - After rendering (`npx hyperframes render --output ...`), extract a frame contact sheet (`scripts/make_vox_contact_sheet.swift` or `scripts/inspect_video.sh`) and inspect every beat via `view_file` to verify zero overlapping labels, ghost artifacts, or clipped edges.

---

## II. Vox-Style Editorial Paper Collage Rules (Rules AM7–AM11)

7. **Rule AM7 — Authentic Photographic Human Cutouts, Paper Banner Subtitles & British Neural VO (Rule 58)**:
   - **Authentic Photographic Human Cutouts (Zero Abstract Geometric Placeholders)**: Human subjects (runners, students, historical figures) must **ALWAYS** be authentic photographic cutouts of real humans with vintage/halftone printing texture, torn white paper borders, and real anatomy. Never substitute humans with abstract geometric shapes (circles on pill/block bodies).
   - **Organic Editorial Paper Banner Subtitles**: Render caption containers as warm textured cream paper strips (`#F4EDDE`) with crisp dark ink borders (`#191713`), slight physical rotation (`-0.8deg` to `+0.8deg`), soft drop shadows, and authentic Vox yellow marker highlights (`#FFD51F`, `mix-blend-mode: multiply`) sweeping across active spoken words. Never overlay stark black digital boxes over paper scenes.
   - **Natural British English Neural Voiceover & Zero-Hyphen Phrasing**: Use a natural human British English neural voice (`en-GB-RyanNeural` or equivalent documentary voice). Strictly eliminate hyphens in numbers (write `"twenty two"`, `"twenty nine"`, `"twenty seven"`, `"twenty four"`) and replace em-dashes with conversational punctuation for fluid acoustic cadence and clean line wrapping.
8. **Rule AM8 — Hybrid Asset Sourcing Split & Mandatory Unification Treatment Pass (Rule 59)**:
   - **Search It (Real Material)**: Anything real—archival photos, historical events, real maps, newspaper clippings, exam halls, banknotes, city skylines, starter pistols, and logos-as-evidence—must be **searched and downloaded** from Public Domain / CC0 / CC-BY sources (`Wikimedia Commons`, `Library of Congress`, `Openverse`, `Unsplash`, `Pexels`). Enforce a strict **`1000px` minimum resolution floor** on the short dimension and log every URL + license in `asset-list.md`.
   - **Generate It (Bespoke / Metaphor)**: Only generate bespoke diagrams, recurring stylized props, or abstract metaphors that do not exist in reality.
   - **Mandatory Unification Pass**: Every external photo must pass through an automated treatment pipeline (`grayscale/duotone contrast=1.2 saturation=0.7` + halftone dot pattern + torn white paper edge cutout + soft drop shadow) so all assets read as one cohesive magazine collage world.
9. **Rule AM9 — Empty Canvas Principle & Dynamic Layered Entry (Rule 60)**:
   - **Never Bake Moving Subjects into Background Plates**: Background plates (`beatXX_clean_bg.jpg`) must **NEVER** pre-bake subjects that also animate as DOM elements (runners, desks, graduation caps, phones, notifications, playing cards). Pre-baking causes frozen duplicate ghost artifacts.
   - **Clean Plate Initialization**: Start every beat at `0.00s` on an intentional clean plate (empty 5-lane track, blank cream dotted table with corner tape, or empty navy sheet) and animate every subject entering dynamically via staggered stamps, card deals, or spring slides.
10. **Rule AM10 — Visual Directness & Concrete Reality Over Ambiguous Abstractions (Rule 61)**:
    - Never use ambiguous geometric abstractions (such as blue/white striped bars for classroom desks). Ground every narrative beat in recognizable photographic reality: real exam halls for school, real vintage starter pistols for the starting gun, real banknotes/skylines/handshakes on dealt cards, and real sprinter/runner photography for race laps.
11. **Rule AM11 — Differentiated Multi-Colored Starting Lines for Unequal-Start Metaphors (Rule 62)**:
    - When visualizing the thesis that *"nobody started at the same line"*, animate five distinct, brightly colored horizontal starting lines (**Yellow, Red, Coral, Teal/Cyan, Navy**) sweeping across each runner's lane at their specific staggered depth so the unequal starting premise is viscerally proven at a glance.
