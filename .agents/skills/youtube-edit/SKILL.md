---
name: youtube-edit
description: Model-neutral local vertical talking-head editing with reviewed storyboards, versioned EDLs, captions, explicit effects, QC and revision memory; preserves legacy couple and animation reference workflows.
---

# Video editing workflow

Read `AGENTS.md`, `docs/agent-runbook.md` and `docs/architecture.md` at repository root. Use `python3 -m editor` for the executable contract. Any model can plan; commands validate and execute the same files.

1. Diagnose tools and query capabilities. Resume existing projects through `editor handoff` before editing.
2. Inspect source/proxies and transcript. Review takes and keeper script. Never claim to watch/listen when the current model lacks that capability.
3. Present storyboard and obtain the user's authorization. `editor approve` records approval of the exact plan hash. Explicit one-shot authorization is permitted.
4. Validate assets and EDL; render a new revision filename. Inspect actual output; technical QC does not replace creative review.
5. Record feedback, rejected decisions and resolutions through history commands. Fix in a child revision. Store scoped evidence-backed lessons and regression checks.

Read relevant `references/editing-rules-*.md` for creative preferences. Historical rules and the catalogue are not proof of executable effect support. The 31 library scenes remain experimental; use explicit compositions with `demo: true`. Do not silently substitute a demo for a requested source-video effect.

The master feedback changelog remains historical evidence. New revisions belong in project history and scoped memory; this persists context rather than training model weights. Delegate QC to an independent reviewer when authorized and available; otherwise record review as pending.
