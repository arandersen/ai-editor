# AI Video Editor

A local editor for vertical talking-head reels, with model-neutral EDLs, timed captions, FFmpeg rendering, and persistent revision history. Couple-game builders and motion-graphics examples remain available as legacy/reference workflows.

## Setup

Core: macOS, Python 3.9+, FFmpeg/ffprobe with libx264 and qtrle, and Swift. Optional scene renderer: Node 22+ and Chrome. ASR providers are installed separately in a provider-supported Python virtual environment; optional engine pins are in `requirements-asr.txt`. The transcription wrapper discovers `~/.venvs/whisper/bin/python3`. Download/cache a suitable model before offline operation.

```bash
./scripts/setup_tools.sh             # read-only diagnostics
./scripts/setup_tools.sh --install   # install pinned Node tools and prepare folders
python3 -m editor capabilities
```

## One project, from source to review

```bash
./scripts/transcribe.sh "raw/My Reel/clip.MOV" --lang en
./scripts/inspect_video.sh "raw/My Reel/clip.MOV" --project "My Reel"
python3 -m editor init --project "My Reel" --source "raw/My Reel/clip.MOV" --transcript "transcripts/My Reel/clip_acoustic.json"
```

The init command prints the EDL path. Review the transcript, keeper ranges, storyboard and visuals with the user. `editor plan` can propose pause cuts; it does not choose retakes or approve a story.

```bash
python3 -m editor approve --edl <edl.json> --by "user-authorized review"
python3 -m editor validate --edl <edl.json> --check-files
python3 -m editor render --edl <edl.json> --output "renders/drafts/My Reel/rev-001.mp4" --draft-only --model-tag <model>
python3 -m editor handoff --project "My Reel"
```

## Current capabilities

Working core: reviewed cuts, speed/framing, warm/moody grades, a blur-accent cut transition, transcript-driven coral/one-word captions, native label/repo/prompt/title graphics, screenshots, prepared media overlays, foreground alpha compositing, explicit HyperFrames compositions, music ducking and SFX. Technical QC checks the actual output; creative review remains explicit.

The 31 catalogue scenes now bind editable text/layout parameters and use local GSAP. They remain **experimental demos**: some require further source-media/depth work. `capabilities` and each `params.json` expose status and unbound variables. Unknown effects fail rather than disappear.

## Repository map

- `editor/`: shared contract, compiler, renderer, inspection, CLI and history.
- `projects/<id>/`: tracked project metadata, revision EDL snapshots, QC and append-only events.
- `memory/`: scoped lessons and imported historical feedback.
- `assets/`: shared media; `audio` is a compatibility symlink.
- `raw/`, `broll/`, `transcripts/`, `renders/`: source and generated project material.
- `animations/_fx_library/`: generated experimental scenes; instantiate copies per project.
- `scripts/`: wrappers plus legacy project-specific builders; `templates/`: planning examples.
- `tests/`: deterministic contract/history and render regression tests.

## Guides and checks

Read [the agent runbook](docs/agent-runbook.md), [architecture](docs/architecture.md), [effect status](docs/effect-status.md), [the audit](docs/audits/2026-10-29-system-audit.md), and [the historical creative catalogue](docs/reference/creative-catalogue.md).

```bash
python3 -m unittest discover -s tests -v
EDITOR_INTEGRATION=1 python3 -m unittest discover -s tests -v
```

Keep generated video, caches and private source footage out of Git. Review transcript/project metadata before sharing. Captured proxies are split and their size is checked; inspect their JSON manifest for source time offsets.
