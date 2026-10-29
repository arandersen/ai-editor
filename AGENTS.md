# Repository Guidelines

## Project Structure & Module Organization
This Apple Silicon video production workspace supports couple videos, talking heads, and motion graphics. `scripts/` contains Python processing/rendering tools, Bash wrappers, Swift overlays, and Node utilities. `templates/01_couple_video/`, `02_talking_head/`, and `03_animation_motion_graphics/` hold storyboard and edit decision list (EDL) templates. `animations/` contains HyperFrames HTML/CSS/GSAP scenes and reusable effects. `.agents/skills/` contains workflow instructions and category rulebooks.

Store footage in `raw/<Project>/`, transcripts in `transcripts/<Project>/`, project assets in `broll/<Project>/`, and outputs in `renders/drafts/<Project>/` or `renders/final/<Project>/`. Reusable media belongs in `assets/`; follow the asset handles documented in `assets/README.md`. `examples/` holds reference videos.

## Build, Test, and Development Commands
Run commands from the repository root; quote paths containing spaces.

- `./scripts/setup_tools.sh`: prepares directories, checks dependencies, and may install tools. Review it before running.
- `./scripts/transcribe.sh "raw/<Project>/clip.MOV" --lang en`: produces local speech transcripts and timing data.
- `./scripts/inspect_video.sh "raw/<Project>/clip.MOV"`: generates contact sheets and a viewing proxy.
- `python3 scripts/lint_edl.py --edl "<path>/edl.json" --category couple`: validates pre-render rules; other categories are `talking_head` and `animation`.
- `npx hyperframes lint animations/<Project>`: checks an animation scene.
- `npx hyperframes render animations/<Project> --output renders/drafts/<Project>/animatic_raw.mp4`: renders a draft animation.

## Coding Style & Naming Conventions
Follow nearby code: four-space indentation for Python and Swift, two spaces for JavaScript and JSON. Use `snake_case` for Python functions and script filenames, and Swift type names such as `OverlaySpec`. Keep reusable utilities in `scripts/` and effect parameters beside their scenes. No repository-wide formatter configuration is present.

## Testing Guidelines
There is no centralized test runner or coverage threshold. Validate the affected EDL and lint changed HyperFrames scenes. Smoke-test processing changes on a short clip, then inspect frames, caption timing, audio sync, and output properties with `ffprobe`. `scripts/test_swift_emoji.swift` is a targeted rendering check.

## Commit & Pull Request Guidelines
History uses imperative summaries and prefixes such as `feat:`, `feat(mcp):`, and `docs:`. Keep commits focused. PRs should describe the affected workflow, commands used for validation, and relevant rule/template changes; link issues when applicable. Include representative frames or preview clips for visual changes. Keep ignored raw footage and rendered masters out of commits.

## Production Workflow
Read `README.md` and the relevant category rulebook before editing. Obtain storyboard approval before rendering production videos. When fixing a recurring editing defect, update its parameterized rule and applicable EDL checks alongside the fix.
