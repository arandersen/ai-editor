# Architecture and migration

## Executable path

`python3 -m editor` is the model-independent entry point. `editor/core.py` defines validation, handles, approval hashes, interval mapping and caption generation. `render.py` executes FFmpeg/Swift/HyperFrames and measures output. `history.py` stores project events, immutable revision inputs/results and scoped lessons. `inspect.py` creates source-identified diagnostics and size-checked proxies. `scripts/talking_head_engine.py`, `inspect_video.sh` and `setup_tools.sh` are compatibility wrappers.

The core Python runtime uses the standard library. Native typography/segmentation require macOS; model choice is independent of this host requirement. Node scene dependencies are pinned in `package-lock.json`; actual system tool versions and executable hashes are recorded in revision manifests. `schemas/edl.schema.json` describes structure; semantic validation in `core.py` is authoritative.

## Storage boundaries

`projects/<name-hash>/project.json` points at the latest successfully rendered revision, which is not necessarily accepted. Its `edl.json` is a mutable working plan. Each `revisions/rev_*/` contains an immutable submitted EDL and manifest, a compiled EDL, input hashes, technical QC and result when available. Append-only history includes commands and failures. Global lessons use a separate lock; project events have per-project locks. Output publication is exclusive.

Raw media, overlays, transcripts and renders remain in their existing folders. No bulk path migration was attempted: older builders still depend on historical project filenames and parameters. The `audio -> assets/audio` symlink preserves compatibility with older relative paths. New reusable code belongs in `editor/`, not another `build_<project>.py`.

The source-to-output compiler intersects effect intervals with retained segments and applies speed. Subframe keeper ranges are rejected. Cut durations are floored to complete frames and the compiled schedule is saved. Captions use one native PNG per active word and a single timed alpha track, avoiding one FFmpeg input per caption.

## Effect boundaries

Native graphics and explicit media/composition adapters are executable capabilities. The 31 generated scene templates remain experimental. Some now bind text, themes, layout and provided media, but full subject-aware transitions, segmentation contours and multi-plane source compositing are not certified. They cannot silently masquerade as built-in effects.

`build_fx_library.py` is the source for generated library HTML/params. Default execution creates missing scenes; `--refresh-scenes` explicitly regenerates them. Existing starter assets and asset documentation are never overwritten. Per-project compositions are copies. GSAP is loaded from the pinned local package. Unimplemented parameters are exposed in each scene's metadata.

## Legacy workflows

Couple-game builders, Vox race utilities and their historical feedback remain preserved. Several still contain personal absolute paths or hardcoded timelines; they are project examples, not portable general engines. Use `docs/reference/creative-catalogue.md` to understand intent and the audit's per-effect table to see gaps. Do not move those scripts until their shared primitives have replacements and their original media can be regression-tested.

## Remaining certification work

- Real creator footage, including iPhone portrait orientation/HDR, segmentation edges, speech accuracy and pacing.
- Full directional whip transitions, magazine covers, source-aware nested PIP, complete multi-reel/depth choreography and the remaining catalogue fidelity work.
- Measured final loudness/true-peak acceptance and automated visual-content QC; current gates cover dimensions, FPS, duration and decode integrity.
- Two distinct model/provider runs on the same approved plan; the contract is model-neutral but this comparison has not been certified.

These are visible limitations, not capabilities inferred from reference prose. They do not block deterministic basic cuts/captions/media overlays, history or explicit composition execution.
