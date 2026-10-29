# Agent Entry Point

Read `AGENTS.md`, then `docs/agent-runbook.md`. The same file/command contract applies to every model.

1. Run `python3 -m editor doctor` and `python3 -m editor capabilities`.
2. Open `python3 -m editor handoff --project "<Project>"` before changing an existing edit.
3. Review source, transcript and keeper script; show a storyboard and obtain the user’s authorization before recording approval.
4. Validate the exact approved EDL, render into a new artifact, inspect the output, and record feedback/decisions through the CLI.
5. Store revisions, unresolved feedback and evidence-backed lessons. Do not claim visual QC was completed when the model cannot inspect it.

Library scenes marked `experimental-demo` require explicit `demo: true` for previews. Never substitute a demo silently for a source-video effect. Use `@overlay` for an already prepared asset or `@hyperframes` for an explicit composition.

Historical creative reference: `docs/reference/creative-catalogue.md`. Domain rulebooks describe creative preferences; executable validation takes precedence over outdated tool/model-specific instructions.
