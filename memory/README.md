# Editorial memory

`legacy-feedback.json` preserves the original revision table as historical evidence.
`lessons/` stores active/superseded, scoped lessons with evidence-event references.
Project execution and feedback events live under `projects/<id>/history/events.jsonl`.

Use `editor feedback`, `decision`, `resolve`, `lesson` and `handoff` instead of editing
event files. Project lessons do not automatically become global preferences. Supersede
conflicting lessons explicitly. Keep raw feedback, failed attempts and rejected choices;
do not erase them after fixing a render. Mechanical lessons also need validation or tests.

This is persistent context and recorded process evidence, not model-weight training.
Review memory/project metadata before publishing and never store credentials or private
chain-of-thought. See `docs/agent-runbook.md` for examples and limits.
