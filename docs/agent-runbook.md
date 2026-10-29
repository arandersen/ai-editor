# Model-neutral editing runbook

Use this contract with any agent/model. The execution host currently needs macOS for native typography/segmentation. A model without native video/audio input must use proxies, frames, transcripts and an explicit human review handoff; it must not report that it watched footage it could not inspect.

## Start or resume

Read `AGENTS.md`, run `python3 -m editor doctor`, then `python3 -m editor capabilities`. For an existing project, run `python3 -m editor handoff --project "Name"` **before** making decisions. Read open feedback, recent failures/rejected decisions, current revision and relevant lessons. Historical creative specifications are not proof that a renderer supports an effect.

Put footage in `raw/Name/`; run `scripts/transcribe.sh` and `scripts/inspect_video.sh`. Inspection prints the project/media-scoped manifest, sheets and proxy parts; proxy timestamps are part-relative, with source offsets in JSON. ASR/RMS timing is heuristic and requires review. Use `--speakers Angel,Arthur` only when stereo channels actually correspond to those speakers.

`python3 -m editor init --project "Name" --source "raw/Name/clip.MOV" --transcript "transcripts/Name/clip_acoustic.json"` creates a project ID and an unapproved working EDL. Copy the EDL before proposing alternative plans. A project's display name and stable ID are separate from filenames.

## Plan and authorize

Create a keeper script and beat-by-beat storyboard with source/output times, exact words, cut reasons, asset references and intended effects. Remove retakes by meaning, not by silence alone. `editor plan --edl <working.json> --transcript <words.json> --output <candidate.json>` proposes pause-based ranges with padding; review it for semantic errors and boundaries.

Only after user authorization, run `editor approve --edl <plan.json> --by "<review identity>"`. Approval is a content hash: changing source, cuts, captions or effects requires recording approval of the new plan. Never infer authorization from a stale `storyboard_approved` boolean. Explicit one-shot authorization can be named as the review basis.

Use schema version 1. All segments are source seconds. Effect `start_raw`/`end_raw` or `trigger_raw`/`duration` are also source seconds; generated captions preserve segment identity when footage repeats. Video overlays and cutouts are local-time assets starting at the effect's raw start; `asset_start` adds an offset. Do not mix output time into those fields.

## Execute and verify

```bash
python3 -m editor validate --edl <plan.json> --check-files
python3 -m editor render --edl <plan.json> --output "renders/drafts/Name/rev-001.mp4" --draft-only --model-tag <model>
```

Rendering creates a run/revision even for ordinary preflight failures, snapshots the EDL, records input/code hashes and command outcomes, and writes technical QC. Outputs cannot overwrite existing artifacts. Copy an EDL to edit it; do not edit immutable revision snapshots. Pass `--parent <revision-id>` to branch deliberately from a prior attempt; otherwise the latest successfully rendered revision is the parent.

Inspect captions, faces, readability, alpha edges, rhythm, audio and content manually. Technical QC is not creative approval. Draft mode caps width at 1080; resolution/FPS in the EDL control final delivery. Render a master without `--draft-only` only when the storyboard/draft review supports it.

`@whip-pan` currently means a six-frame blur-accent cut, not the full reference's directional two-shot camera move. `@text-behind-head` needs a source-aligned alpha cutout and uses the same crop as the source. Graded/transitioned depth combinations are rejected until matching matte transforms are implemented; use an ungraded hook or a prepared composite. HDR input is rejected until explicitly converted and reviewed for SDR. Screenshot cards use `src`, optional `width_percent` (default 90) and top `y_percent` (default 5). Prepared `@overlay` assets are fit to the canvas. Swift typography uses fixed presets; arbitrary font/position parameters are not supported by `caption_style`.

## Record feedback and prevent recurrence

```bash
python3 -m editor feedback --project "Name" --revision <revision> --text "Label covers my face" --target <effect-id>
python3 -m editor decision --project "Name" --status rejected --text "Dense effect HUD obscured the hook"
python3 -m editor resolve --project "Name" --issue <issue-id> --revision <child-revision> --evidence <qc-evidence.json>
python3 -m editor lesson --project "Name" --text "<specific constraint and verification>" --scope project --evidence-event <event-id>
```

Keep the feedback event, fix it in a child revision, compare before/after and save evidence. Resolution requires a rendered descendant and names the reviewing actor; it is not an automatic guarantee. User acceptance is a separate `decision --status accepted` record. Do not close issues merely because rendering succeeded.

Lessons default to project scope. Promote only with evidence to `category:talking_head` or `universal`; `--supersedes <lesson-id>` retires a conflicting lesson. The next render records relevant lesson IDs; the next agent's handoff includes them. Mechanical constraints belong in validation/tests as well as memory. This is persistent agent context, not weight training.

## Optional effects and providers

Run `npm ci` for pinned HyperFrames/GSAP. Use an explicit `@hyperframes` effect with `composition`, `variables` and source interval; it renders an isolated copy. Library scenes additionally require `demo: true` and remain experimental. The registry lists unbound parameters, which the adapter rejects if supplied. Arrays/objects are serialized to the scene variable format. Use `@asset/...` handles for media-valued variables; dependencies are copied into the instance. Do not call a blank placeholder a completed effect.

Optional MCP config assumes repository working directory; clients launched elsewhere should use an absolute path to `scripts/mcp_server.sh`. Flow must be installed separately at `tools/flow-mcp` or configured with `FLOW_MCP_ENTRY`. Chrome DevTools remains an optional externally versioned provider. Record generated/downloaded assets and source/license/cost information; account availability and free credits are not guaranteed.

## Git and privacy

Track code, rules, small revision metadata and evidence manifests. Media/caches stay local. Inspect transcripts, event text, asset licenses and project metadata before publishing. Do not store tokens or private reasoning. Historical project-specific builders still exist under `scripts/`; consult architecture notes before using them on a new project.
