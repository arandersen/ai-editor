# Effect status

Use `python3 -m editor capabilities` as the machine-readable authority.

| Status | Meaning |
| --- | --- |
| Native | Coral/one-word captions, title, tool label, repository card and prompt bar use Swift presets |
| Media | Screenshot card and prepared alpha/video overlays are composited from explicit assets |
| Depth | Behind-head title requires a source-aligned alpha foreground; no implicit segmentation |
| Composition | Explicit HyperFrames project renders through a pinned local adapter |
| Experimental demo | The 31 library scenes expose editable parameters but are not all source-video effect implementations |
| Unsupported | Other named shortcuts fail validation instead of disappearing |

The independent [audit](audits/2026-10-29-system-audit.md) reviews every effect's original state and intended improvements. Each `animations/_fx_library/<slug>/params.json` now reports `status` and `unbound_variables`. Attempting to override an unbound variable fails. Preview experimental library scenes with an explicit `@hyperframes` composition and `demo: true`; do not label those previews as certified production effects.

Generate missing files with `python3 scripts/build_fx_library.py`; explicitly regenerate with `--refresh-scenes`. Asset scaffolding is opt-in with `--scaffold-assets` and preserves existing files. Use `npm ci` before linting/rendering. Store project-specific instances outside the shared catalogue. Verify variables with changed text, light/dark footage, alpha and first/middle/last frames; lint alone cannot establish fidelity.
