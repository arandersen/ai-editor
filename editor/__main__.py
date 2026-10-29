"""Run `python3 -m editor --help` from the repository root."""
import argparse
import importlib.util
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

from .core import ROOT, SUPPORTED, plan_hash, read_words, validate, resolve_asset
from .history import History, atomic_json, now, project_id


def doctor():
    required = {name: shutil.which(name) for name in ("ffmpeg", "ffprobe", "swift", "node")}
    checks = {name: bool(path) for name, path in required.items()}
    checks["macOS native overlays"] = platform.system() == "Darwin"
    checks["python >=3.9"] = sys.version_info >= (3, 9)
    if required["ffmpeg"]:
        filters = subprocess.run([required["ffmpeg"], "-hide_banner", "-filters"], capture_output=True, text=True).stdout
        for name in ("overlay", "gblur", "loudnorm", "sidechaincompress"):
            checks["filter:" + name] = name in filters
        encoders = subprocess.run([required["ffmpeg"], "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
        checks["encoder:libx264"] = "libx264" in encoders
        checks["encoder:qtrle"] = "qtrle" in encoders
    optional = {"hyperframes_pinned": (ROOT / "node_modules/.bin/hyperframes").exists(),
                "local_gsap": (ROOT / "node_modules/gsap/dist/gsap.min.js").exists(),
                "parakeet": shutil.which("parakeet-mlx"),
                "whisper_python": str(Path.home() / ".venvs/whisper/bin/python3")
                if (Path.home() / ".venvs/whisper/bin/python3").exists() else None,
                "chrome": Path("/Applications/Google Chrome.app").exists()}
    return {"ok": all(checks.values()), "required": checks, "paths": required,
            "optional": optional, "platform": platform.platform(),
            "note": "Optional ASR/provider readiness and creative review are not certified by this check."}


def parser():
    p = argparse.ArgumentParser(description="Model-neutral reels editor")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Read-only dependency checks")
    inspect = sub.add_parser("inspect", help="Scoped contact sheets and bounded viewing proxies")
    inspect.add_argument("source")
    inspect.add_argument("--project")
    inspect.add_argument("--table-crop", action="store_true")
    inspect.add_argument("--proxy-max-mb", type=float, default=14)
    sub.add_parser("capabilities", help="List executable effects and experimental scenes")
    init = sub.add_parser("init", help="Create project metadata and an unapproved EDL")
    init.add_argument("--project", required=True)
    init.add_argument("--source", required=True)
    init.add_argument("--transcript")
    init.add_argument("--fps", type=int, default=30)
    plan = sub.add_parser("plan", help="Generate pause-cut candidates for editorial review")
    plan.add_argument("--edl", required=True)
    plan.add_argument("--transcript", required=True)
    plan.add_argument("--output", required=True)
    plan.add_argument("--max-pause", type=float, default=0.22)
    approve = sub.add_parser("approve", help="Record user-authorized approval of this exact EDL")
    approve.add_argument("--edl", required=True)
    approve.add_argument("--by", required=True)
    check = sub.add_parser("validate")
    check.add_argument("--edl", required=True)
    check.add_argument("--check-files", action="store_true")
    render = sub.add_parser("render")
    render.add_argument("--edl", required=True)
    render.add_argument("--output", required=True)
    render.add_argument("--draft-only", action="store_true")
    render.add_argument("--model-tag", default="unspecified")
    render.add_argument("--parent")
    for name in ("history", "handoff", "feedback", "resolve", "decision", "lesson"):
        s = sub.add_parser(name)
        s.add_argument("--project", required=True)
        if name in {"feedback", "resolve"}:
            s.add_argument("--revision", required=True)
        if name in {"feedback", "decision", "lesson"}:
            s.add_argument("--text", required=True)
        if name == "feedback":
            s.add_argument("--target", help="Effect/word/beat ID")
        if name == "resolve":
            s.add_argument("--issue", required=True)
            s.add_argument("--evidence", required=True)
        if name == "decision":
            s.add_argument("--status", choices=["accepted", "rejected", "pending"], required=True)
        if name == "lesson":
            s.add_argument("--scope", default="project", help="project, category:talking_head or universal")
            s.add_argument("--evidence-event", required=True)
            s.add_argument("--supersedes")
        s.add_argument("--model-tag", default="unspecified")
    return p


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "doctor":
            result = doctor()
            print(json.dumps(result, indent=2))
            return 0 if result["ok"] else 1
        if args.command == "inspect":
            from .inspect import inspect_video
            result = inspect_video(args.source, args.project, args.table_crop, args.proxy_max_mb)
        elif args.command == "capabilities":
            registry = ROOT / "animations/_fx_library/registry.json"
            result = {"schema_version": 1, "effects": SUPPORTED,
                      "library_scenes": [{"shortcut": e["shortcut"], "status": "experimental-demo",
                                          "composition": e["composition_path"]}
                                         for e in json.loads(registry.read_text())["templates"]] if registry.exists() else []}
        elif args.command == "init":
            from .render import probe
            source = resolve_asset(args.source, args.project)
            data = probe(source)
            h = History(args.project)
            path = h.path / "edl.json"
            if path.exists():
                raise ValueError(f"Project EDL already exists: {path}")
            edl = {"schema_version": 1, "category": "talking_head", "project": args.project,
                   "raw_video": str(source), "resolution": [2160, 3840], "fps": args.fps, "fit": "crop",
                   "segments": [{"start": 0, "end": float(data["format"]["duration"]), "speed": 1, "zoom": 1}],
                   "effects": []}
            if args.transcript:
                edl.update(transcript_json=str(resolve_asset(args.transcript, args.project)),
                           caption_style={"shortcut": "@coral-captions"})
            atomic_json(path, edl)
            result = {"edl": str(path), "handoff": h.handoff(), "next": "Review keeper script/storyboard, then approve the exact EDL"}
        elif args.command in {"approve", "validate", "render", "plan"}:
            path = Path(args.edl)
            edl = json.loads(path.read_text())
            if not isinstance(edl, dict):
                raise ValueError("EDL must be a JSON object")
            if args.command == "approve":
                edl["approval"] = {"plan_hash": plan_hash(edl), "approved_by": args.by, "approved_at": now()}
                errors = validate(edl)
                if errors:
                    raise ValueError("Cannot approve invalid EDL: " + "; ".join(errors))
                atomic_json(path, edl)
                History(edl["project"]).append("plan_approved", actor={"role": "reviewer", "model": args.by},
                                                plan_hash=plan_hash(edl), edl_path=str(path.resolve()))
                result = edl["approval"]
            elif args.command == "validate":
                errors = validate(edl, args.check_files)
                print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
                return 1 if errors else 0
            elif args.command == "plan":
                if args.max_pause < 0:
                    raise ValueError("max-pause must be non-negative")
                words = read_words(json.loads(Path(args.transcript).read_text()))
                words.sort(key=lambda w: w["start"])
                groups = []
                for word in words:
                    if not groups or word["start"] - groups[-1][-1]["end"] > args.max_pause:
                        groups.append([])
                    groups[-1].append(word)
                edl.pop("approval", None)
                edl["transcript_json"] = str(Path(args.transcript).resolve())
                source_end = max(s["end"] for s in edl["segments"])
                edl["segments"] = [{"start": max(0,g[0]["start"]-0.04), "end": min(source_end,g[-1]["end"]+0.06),
                                    "speed": 1, "zoom": 1, "notes": " ".join(w["word"] for w in g)} for g in groups]
                # Clip padding to neighbor boundaries so candidates do not repeat source audio.
                for a, b in zip(edl["segments"], edl["segments"][1:]):
                    if a["end"] > b["start"]:
                        boundary = (a["end"] + b["start"]) / 2
                        a["end"], b["start"] = boundary, boundary
                if Path(args.output).exists():
                    raise ValueError("Plan output exists; choose a new filename")
                atomic_json(args.output, edl)
                result = {"output": args.output, "status": "candidates_need_editorial_review", "segment_count": len(groups)}
            else:
                from .render import render_project
                result = render_project(edl, args.output, draft=args.draft_only, model=args.model_tag, parent=args.parent)
        else:
            h = History(args.project)
            actor = {"role": "editor", "model": args.model_tag}
            if args.command == "history":
                result = h.events()
            elif args.command == "handoff":
                result = h.handoff()
            elif args.command == "feedback":
                result = h.feedback(args.revision, args.text, actor, args.target)
            elif args.command == "resolve":
                result = h.resolve(args.issue, args.revision, args.evidence, actor)
            elif args.command == "decision":
                result = h.append("decision_recorded", actor=actor, summary=args.text, status=args.status)
            else:
                scope = "project:" + project_id(args.project) if args.scope == "project" else args.scope
                result = h.lesson(args.text, scope, args.evidence_event, actor, args.supersedes)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
