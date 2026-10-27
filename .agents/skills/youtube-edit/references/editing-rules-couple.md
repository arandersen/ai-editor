# Couple Video Editing Rules — Vertical 9:16 Couple Games (`Angel` & `Arthur`)

> **Domain**: Vertical 9:16 Reels / TikTok / YouTube Shorts Couple Challenge & Game Videos (`Bikin Kata`, `Match Kartu`, `Hafal Kartu`, `Lengkapin Kata`, `Tebak Kata`, `Nyambung Kata`, `Kartu Pasangan`, `Tebak Snack`).
> **Master Index**: [editing-rules.md](./editing-rules.md) | **Sibling Rulebooks**: [editing-rules-talking-head.md](./editing-rules-talking-head.md) · [editing-rules-animation.md](./editing-rules-animation.md)

---

## I. Couple Identity, Framing & Pacing (Rules C1–C6)

1. **Rule C1 — Creative Director & Couple Identity (`Angel` & `Arthur` — Warm Collaborative Vibe)**:
   - Left Player (Cewek) is **Angel** (`x = 305` on `1080x1920`, `x = 610` on `2160x3840`); Right Player (Cowok) is **Arthur** (`x = 760` on `1080x1920`, `x = 1520` on `2160x3840`).
   - **No Persistent Scoreboards in Casual Word Games**: Keep casual word games warm and focused on playing together—do not display persistent scoreboards (`ANGEL X — 0 ARTHUR`) or point badges (`+1 ANGEL`, `(STEAL)`, `CLEAN SWEEP!`) unless the game itself is a card-counting tally game (`Match Kartu`, `Hafal Kartu`, `Kartu Pasangan`, `Tebak Snack`).
2. **Rule C2 — Zero-Latency Speech Start (`0:00:00` = First Spoken Syllable)**:
   - Videos must begin **instantly on the first spoken syllable** (`0:00:00` on the output timeline = first vocal onset in raw footage, with `0.04s` pre-consonant micro-padding). Never leave `0.5s–1.5s` of dead silence or idle waiting before dialogue begins.
3. **Rule C3 — Steady `1.00x` Wide Framing for Two-Person Dialogue (No Constant Jump-Cut Zooms)**:
   - Do **NOT** alternate `1.00x` and `1.10x` zoom on every jump cut during normal two-person games. Keep a steady `1.00x` wide framing (`mode="normal"`) showing both Angel and Arthur side by side so both partners' facial reactions remain visible.
   - **No Sudden Zoom in Opening**: The opening hook title must be delivered in a single smooth, steady wide shot.
   - **When to Zoom**: Reserve punch-in zooms (`zoom_angel`, `zoom_arthur`, `zoom_both`) strictly for special comedic moments (e.g., fast B&W zoom-in on an absurd guess or funny reaction), dramatic game-ending reveals, or loss reactions.
4. **Rule C4 — Audience Participation Psychology (100% Uncut Gameplay Continuity)**:
   - Psychologically, viewers watch couple challenge games because **they want to participate and play along in the game themselves**.
   - **Never Cut Active Gameplay**: Never cut out cards being placed during matching phases, cards being searched/flipped on the table, or cards being revealed during scoring phases. Both the **matching/searching phase** and the **opening/result phase** must be shown in unbroken continuity from start to finish.
5. **Rule C5 — Phase-Specific Dynamic Speed Modulation & `< 2:30` (`150s`) Ceiling**:
   - All vertical short-form / couple game videos must strictly adhere to a maximum final duration ceiling of **2 minutes 30 seconds (`150.0s`)**.
   - **30-Second Memorization Phase = `3x–5x` (`4.0x`) Timelapse + Clock Ticking SFX + No Bottom Caption**: Fast-forward 30s memorization phases at `4.0x` (`setpts=PTS/4.0`, `atempo=2.0,atempo=2.0`) paired with `audio/sfx/clock_ticking.wav`, and **remove the bottom caption completely** during the timelapse.
   - **Active Gameplay Speed Modulation**: Dynamically modulate playback speeds across phases (`1.25x–1.35x` for card opening/reveals, `1.45x–1.50x` for regular card flipping, `1.65x–1.70x` for table scanning/searching) so 100% uncut gameplay finishes comfortably under `2:30` (e.g. `~2:20–2:24`).
6. **Rule C6 — Per-Project Output Folder Structure (Mirroring `raw/<Project Name>/`)**:
   - For every video project in `raw/<Project Name>/`, always create matching per-project folders in `renders/final/<Project Name>/`, `renders/drafts/<Project Name>/`, `transcripts/<Project Name>/`, and `broll/<Project Name>/`, placing the final master MP4 and `*_cover.png` inside `renders/final/<Project Name>/`.

---

## II. Typography, Hook Covers & On-Screen Overlays (Rules C7–C12)

7. **Rule C7 — Reference-Style 2-Line Opening Hook & Cover (`0:00`, No Blue Gradient, Natural Color Grading)**:
   - **Show Both Lines Immediately From `0:00`**: Display the complete 2-line title (`challenge` + `[GAME NAME] 🔥`) right from frame `0:00`.
   - **Typography Spec** (modeled after `yang kena bomb makan / BEAN BOOZLE 🤮`):
     - **Line 1 (Setup / lowercase)**: `HelveticaNeue-Bold` (`68pt` on 1080p / `136pt` on 4K), **Black fill (`#000000`) with a pure crisp White border (`#FFFFFF`)**.
     - **Line 2 (Main Game Title / ALL CAPS + Emoji)**: `Arial-Black` (`96pt` on 1080p / `192pt` on 4K), **Pure White fill (`#FFFFFF`) with a thin dark edge (`-4.5` on 1080p / `-8.0` on 4K) and soft dark drop shadow**.
   - **Zero Blue/Dark Gradient & 100% Consistent Color Grading**: Never put a blue or dark gradient overlay at the top of the hook/cover. Keep natural camera color grading 100% consistent from `0:00` to the end (except intentional B&W comedic zooms).
   - **Suppress Bottom Captions During Hook**: Hide bottom spoken captions while the opening hook title is on screen.
8. **Rule C8 — Unified Borderless Typography & Vibrant Native Emoji Separation**:
   - Use the same clean `Arial-Black` white-fill + thin dark edge + soft drop shadow style across titles, top callouts, above-head letters/words, and bottom captions—**no "Liquid Glass" translucent boxes or borders**.
   - **Emoji Stroke Separation**: Always separate text runs and `AppleColorEmoji` runs when rendering overlays in Swift (`AppKit`/`CoreText`) so negative stroke widths applied to text never strip, clip, or corrupt emoji glyphs.
   - **No Missing Emoji Boxes in `.ass`**: Omit raw emojis from libass `.ass` subtitle strings (which render as `[?]` in `Arial Black`) or render emoji-bearing callouts via the Swift `AppleColorEmoji` overlay layer.
9. **Rule C9 — One-Word-at-a-Time Acoustic-Onset Spoken Captions**:
   - **Strictly One Word at a Time**: Display only **one word at a time** at the bottom of the frame (`PlayRes 2160x3840`, `108pt` `Arial Black`, `MarginV: 330`), popping at the exact millisecond the speaker vocalizes that word and disappearing immediately when the word ends. Never show static full-sentence blocks.
   - **Acoustic Onset Verification (VAD / 10ms RMS Envelope)**: Never trust raw Whisper timestamps after pauses (which bridge silence `0.5s–1.0s` early). Anchor every word's start timestamp to the **acoustic speech energy onset** (`RMS > threshold`).
   - **No Duplicate Captions on Word Completion**: Clear bottom in-progress word trackers the instant a completed word is displayed at the top.
10. **Rule C10 — Horizontally Aligned Above-Head Letter & Guess Pops (`1.4s–1.8s` Max)**:
    - Anchor Left Player (Angel) above-head pops at `x = 305` (`610` in 4K) and Right Player (Arthur) at `x = 760` (`1520` in 4K) on the **exact same aligned horizontal Y-coordinate** (`y = 510` in 1080p / `y = 1020` in 4K), paired with `pop.wav`.
    - **Strict No-Countdown Spoiler & Transient Duration**: Keep above-head pops hidden during countdowns (`"Satu, dua, tiga..."`), trigger them at the exact acoustic onset when spoken, and automatically clear them after **`1.4s–1.8s`** (never merge repeating guesses like `MANIS!` into a stuck multi-segment overlay).
    - **Verify Speaker Attribution**: Always verify lip-sync and stereo L/R audio before assigning above-head letters to Angel vs. Arthur.
11. **Rule C11 — Anti-Spoiler Top Callout & Turn-Based (`CARI` vs. `DAPAT`) Header Protocol**:
    - **Word Games**: Completed word headers (`API! 🔥`, `GANAS`, `MANDI UANG 💸`) must appear **strictly at the exact millisecond the word is solved and vocalized** (never during countdowns or deliberation) and auto-hide after **`3.0s–4.0s`**.
    - **Turn-Based Card Games (`CARI` vs. `DAPAT`)**:
      - Display `[PLAYER]: CARI [TARGET] [EMOJI]` the exact millisecond a player draws/announces their target card and keep it active across their table search.
      - Transition to `[PLAYER]: DAPAT [TARGET]! [EMOJI]` **ONLY** when the matching card on the table is physically flipped and revealed to the camera. Never pre-score on banter when a search fails.
      - **Physical Artwork & Color-Variant Verification**: Visually inspect the physical cards on the table (e.g., `TRAKTOR BIRU` vs. `TRAKTOR MERAH`, `GUDANG/BARN` vs. `JERAMI/HAY`, both `DOMBA` cards face up) before assigning headers.
12. **Rule C12 — Delayed Point-Tally vs. Winner Party Celebration (`confetti_loop.mov` + `party_cheer.wav`)**:
    - **Point Tally Phase**: While players count their cards (`"Satu... dua... tiga..."`), display `HITUNG POIN! 🃏` or `[PLAYER]: HITUNG KARTU 🃏`. **Never** prematurely display the final score or winner header before the final card pair is opened or counted.
    - **Winner Reveal Trigger**: At the exact millisecond the final count is vocalized and confirmed, trigger the victory header (`ANGEL: 11 POIN — DOUBLE GUYS! ✌️🎉`) accompanied by:
      1. **Audio**: `audio/sfx/party_cheer.wav` at `1.1x` full festive volume (confetti cannon pop + party horn + brass fanfare).
      2. **Visuals**: Native 4K 3D fluttering multi-colored paper confetti & streamers (`confetti_loop.mov`, 450+ particles, **strictly ZERO floating emoji glyphs** like 🎉 🥳 🏆 over player faces).

---

## III. Comedic Reactions, Memes & Signature Sound Design (Rules C13–C15)

13. **Rule C13 — Fast B&W Zoom-In + Loss-Only Reaction Meme Cutaways**:
    - **Punchline Face Zoom**: On a wild admission, blunder, or loss reaction, execute a fast animated zoom-in (`1.15x -> 2.15x` over `~0.17s`) onto the speaker's face and switch to **Black & White (grayscale)** before cutting to the reaction meme.
    - **Losses Only**: Limit reaction meme cutaways (`What_ Meme.mp4`, `Hi! Okay,,,.mp4`) **strictly to when a player loses or makes a major blunder**—never insert memes mid-search or on a tie (`SERI`).
    - **Comfortable 9:16 Portrait Meme Framing & `+14 dB` Boost**: Frame 16:9 memes at `1080x1440` (`2160x2880` in 4K) centered over a blurred backdrop so head and shoulders fit comfortably. Play `Hi! Okay,,,` from `4.00s` to `6.64s`, boost meme dialogue by **`+14 dB`** (`volume=4.5,alimiter=limit=0.92`), and dip background music to `0.03`.
14. **Rule C14 — Chopin's Nocturne in E-flat Major, Op. 9, No. 2 (Mandatory Default Channel Theme)**:
    - The permanent default background track across **ALL** Couple Game videos is **Chopin's Nocturne in E-flat major, Op. 9, No. 2** (`audio/music/nocturne_op9_in_eb.wav` — authentic original E-flat major key from Musopen, never transposed to D major).
    - **Dynamic Envelope**: Duck to `0.10` (`-20 dB`) under active dialogue, swell to `0.48` during dramatic B&W face zooms, and dip to `0.03` during spoken meme cutaways.
15. **Rule C15 — Dedicated Caption & Header QC Subagent + Native 4K Studio Master Export**:
    - **Mandatory QC Subagent (`caption-qc-reviewer`)**: Cross-examine 100% of transcribed dialogue against the `.ass` and header schedule to guarantee zero dropped banter words and exact sub-second sync.
    - **Native 4K Ultra HD (`2160×3840`) Studio Master**: Never downscale 4K raw footage. Encode at `2160×3840`, H.264 High@L5.2, `-preset slow -crf 14`, target `45–50 Mbps` (`-maxrate 65M -bufsize 90M`), explicit Rec.709 color tags (`-color_primaries bt709 -color_trc bt709 -colorspace bt709`), and `320k` 48kHz AAC stereo audio normalized to `-14 LUFS`.

---

## IV. Couple Video 2.0: `1.10x` Base Speed, `@couple-grade` 4K Color Grading, Locked Brand Kit & Google Flow Integration (Rules C16–C20)

16. **Rule C16 — Default `1.10x` Base Speed (`@couple-speed-1.1x`) & Frame-Quantized Timestamp Mapping**:
    - **Anti-Pattern**: Running normal dialogue at `1.00x` (feels slightly sluggish on short-form Reels/Shorts) or computing segment durations as unrounded floats `(end - start) / speed` (which drifts up to `0.5s` across 35 segments).
    - **Exact Parameterized Standard**:
      - **Hook / Dialogue / Banter / Guess Segments**: Default to **`1.10x` playback speed** (`setpts=PTS/1.1000` + pitch-preserving `atempo=1.1000`).
      - **Card Opening / Point Tally Segments**: Run at **`1.25x–1.35x`**.
      - **Uncut Card Searching / Placing Segments**: Run at **`1.45x–1.70x`** so total duration finishes under `< 150.0s` (`2:30`).
      - **30s Card Memorization**: Run at **`4.00x`** (`@timelapse-4x` + `clock_ticking.wav`).
      - **B&W Loser Zooms & Reaction Memes**: Run at **`1.00x`** for natural comedic timing.
      - **Frame-Quantized Timestamp Math**: For every segment $k$ with raw duration $\Delta r_k = r_{k,1} - r_{k,0}$ and nominal speed $v_k$ at $F=30.0\text{ fps}$, quantize to integer frames $N_k = \max(1, \operatorname{round}((\Delta r_k / v_k) \cdot 30.0))$, set exact segment duration $D_k = N_k / 30.0$, and effective speed $\hat{v}_k = \Delta r_k / D_k$. Map any raw word/event $t_{\text{raw}} \in [r_{k,0}, r_{k,1}]$ to $t_{\text{out}} = T_k + (t_{\text{raw}} - r_{k,0}) / \hat{v}_k$ where $T_k = \sum_{j<k} D_j$.
17. **Rule C17 — Mandatory 4K Warm Studio Color Grade (`@couple-grade`)**:
    - **Anti-Pattern**: Exporting ungraded raw indoor iPhone `yuv420p` footage (leaving shadows muddy and tabletop cards flat).
    - **Exact Parameterized Standard**: Apply `@couple-grade` across 100% of gameplay segments and the `*_cover.png` thumbnail from `0:00` to end:
      ```text
      curves=m='0/0.015 0.20/0.21 0.50/0.52 0.78/0.80 1/0.985',colorbalance=rs=0.010:gs=0.000:bs=-0.010:rm=0.035:gm=0.008:bm=-0.025:rh=0.015:gh=0.005:bh=-0.010,eq=contrast=1.05:brightness=0.010:saturation=1.12:gamma=0.98,unsharp=5:5:0.45:3:3:0.0
      ```
18. **Rule C18 — Locked 4K Brand Kit (`templates/01_couple_video/brand_kit.json`) & 2-Pass CoreText Renderer (`scripts/couple_overlays.swift`)**:
    - **Anti-Pattern**: Drawing text in a single pass with `.strokeWidth: -8.0` (which swallows the white interior fill and turns titles hollow dark-gray/black), using `text.count` instead of `(str as NSString).length` (which drops or shrinks emojis), or leaving a wide blank space before emojis.
    - **Exact Parameterized Standard**:
      - Always use [`scripts/couple_overlays.swift`](../../../../scripts/couple_overlays.swift) and [`templates/01_couple_video/brand_kit.json`](../../../../templates/01_couple_video/brand_kit.json).
      - **2-Pass Text + Tight Emoji Rendering**: Pass 1 draws outer black stroke (`-9.0`) + drop shadow + `AppleColorEmoji` run (with `-18.0` kerning on the preceding space); Pass 2 draws pure unstroked solid interior fill (`#FFFFFF` White for `CARI`/neutral, `#4ADE80` Green for `DAPAT`/correct, `#FFD60A` Gold for tally/winner, `#FF453A` Red for blunder, `#FF6FAE` Pink for Angel, `#38BDF8` Blue for Arthur) directly on top.
      - **Safe-Zone Coordinates at 4K (`2160×3840`)**:
        - Hook Line 1 (`challenge`): `HelveticaNeue-Bold 136pt`, `y_from_top = 380` (`NSRect(80, 3365, 2000, 190)`).
        - Hook Line 2 (`GAME NAME 🔥`): `Arial-Black 176pt`, `y_from_top = 560` (`NSRect(40, 3140, 2080, 280)`).
        - Top Turn/Action Header: `Arial-Black 116pt`, `y_from_top = 470` (`NSRect(40, 3230, 2080, 260)`).
        - Above-Head Pops: `Arial-Black 240pt` (letter) / `148pt` (word) at `Angel = (610, 1020)` and `Arthur = (1520, 1020)` (`NSRect` `y=2670`).
        - Bottom 1-Word Captions: `Arial-Black 116pt`, `PlayRes 2160×3840`, `y = 3120` (`MarginV = 720`, shifting to `y = 3180` when a table word tracker is active at `y = 2880`).
19. **Rule C19 — 60fps Kinetic Spring Animations on Captions, Head-Pops & Top Headers**:
    - **Bottom 1-Word Captions (`@one-word-captions`)**: Include the 3-frame scale pop tag `{\fscx72\fscy72\t(0,95,\fscx106\fscy106)\t(95,150,\fscx100\fscy100)}` on every single-word `.ass` event so each word bounces in on its 10ms RMS onset.
    - **Above-Head Pops (`@head-pop-angel` / `@head-pop-arthur`)**: Animate entrance (`0.65 -> 1.10 -> 1.00` over `140ms`) and smooth exit (`110ms` fade-out) so head-pops never hard-cut off screen.
    - **Top Headers (`@header-cari` / `@header-dapat` / `@top-word`)**: Animate a `180ms` slide-down entrance (`y = -50 -> 0`).
20. **Rule C20 — Talking Head & Google Flow MCP Integration (`@couple-hook-behind-head`, `@flow-sticker-pop`, `@flow-cutaway`)**:
    - **`@couple-hook-behind-head`**: Optionally run `swift ./scripts/person_cutout.swift` on the opening `0.0s–3.5s` hook to sandwich the giant Game Title **behind Angel & Arthur's heads** for a 3D depth cover & intro.
    - **`@flow-sticker-pop` & `@flow-cutaway`**: Use Google Flow MCP (`tools/flow-mcp`) to generate 3D die-cut sticker illustrations (`420×420px` @ 4K) of funny guessed words/animals (`SANTET`, `ANJINGS`, `TRAKTOR BIRU`, `DUBAI CHOCOLATE`) or 2-second Veo 3.1 comedic cutaways on major punchlines.
