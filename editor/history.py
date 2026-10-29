"""Append-only project history, immutable revisions and scoped lessons (stdlib only)."""
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import uuid
from functools import lru_cache

from .core import ROOT, digest, file_hash


def now():
    return datetime.now(timezone.utc).isoformat()


def uid(prefix):
    return prefix + "_" + uuid.uuid4().hex[:16]


def check_id(value, prefix):
    if not isinstance(value, str) or not re.fullmatch(prefix + r"_[0-9a-f]{16}", value):
        raise ValueError(f"Invalid {prefix} ID: {value}")
    return value


def project_id(name):
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60] or "project"
    return slug + "-" + digest(name)[:8]


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
        tmp = f.name
    os.replace(tmp, path)


def code_identity(root=ROOT):
    def git(*args):
        r = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
        return r.stdout if r.returncode == 0 else b""
    files = [p for folder in ("editor", "scripts") for p in (Path(root)/folder).glob("*")
             if p.suffix in {".py", ".swift", ".sh", ".mjs"}]
    files += [p for name in ("package-lock.json", "config/toolchain.json", "pyproject.toml") if (p := Path(root)/name).is_file()]
    return {"commit": git("rev-parse", "HEAD").decode().strip(),
            "tracked_diff_sha256": __import__("hashlib").sha256(git("diff", "HEAD", "--binary")).hexdigest(),
            "executable_files": {str(p.relative_to(root)):file_hash(p) for p in sorted(files)},
            "tool_versions": tool_versions()}


@lru_cache(maxsize=1)
def tool_versions():
    result = {}
    for name, flag in (("ffmpeg","-version"),("ffprobe","-version"),("node","--version"),("swift","--version")):
        try:
            r = subprocess.run([name,flag],capture_output=True,text=True,timeout=10)
            result[name] = (r.stdout or r.stderr).splitlines()[0]
        except (OSError, subprocess.TimeoutExpired, IndexError):
            result[name] = "unavailable"
    return result


class History:
    def __init__(self, project, root=ROOT):
        if not isinstance(project, str) or not project.strip():
            raise ValueError("project must be a non-empty name")
        self.root = Path(root)
        self.project = project
        self.path = self.root / "projects" / project_id(project)
        self.path.mkdir(parents=True, exist_ok=True)
        self.events_path = self.path / "history" / "events.jsonl"
        self.events_path.parent.mkdir(exist_ok=True)
        with self.lock():
            if not (self.path / "project.json").exists():
                atomic_json(self.path / "project.json", {"schema_version": 1, "project_id": project_id(project),
                                                       "name": project, "created_at": now(), "current_revision": None})

    @contextmanager
    def lock(self):
        with (self.path / ".lock").open("a") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def events(self):
        with self.lock():
            return [json.loads(line) for line in self.events_path.read_text().splitlines()] if self.events_path.exists() else []

    def append(self, kind, *, actor=None, run_id=None, revision_id=None, **data):
        event = {"schema_version": 1, "event_id": uid("evt"), "timestamp": now(),
                 "project_id": project_id(self.project), "type": kind,
                 "actor": actor or {"role": "editor", "model": "unspecified"},
                 "run_id": run_id, "revision_id": revision_id, **data}
        with self.lock():
            with self.events_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False, allow_nan=False) + "\n")
                f.flush()
                os.fsync(f.fileno())
        return event

    def begin(self, edl, actor, parent=None):
        revision, run = uid("rev"), uid("run")
        with self.lock():
            project = json.loads((self.path / "project.json").read_text())
            parent = parent or project.get("current_revision")
            if parent:
                check_id(parent, "rev")
            if parent and not (self.path / "revisions" / parent / "edl.json").exists():
                raise ValueError(f"Unknown parent revision: {parent}")
            folder = self.path / "revisions" / revision
            folder.mkdir(parents=True)
            atomic_json(folder / "edl.json", edl)
            atomic_json(folder / "manifest.json", {"schema_version": 1, "revision_id": revision,
                        "parent_revision_id": parent, "run_id": run, "actor": actor,
                        "edl_sha256": digest(edl), "code": code_identity(self.root), "created_at": now()})
        self.append("run_started", actor=actor, run_id=run, revision_id=revision,
                    parent_revision_id=parent, edl_sha256=digest(edl))
        return run, revision, folder

    def finish(self, run, revision, folder, actor, *, qc=None, output=None, error=None):
        outcome = {"status": "failed" if error else "rendered", "finished_at": now(),
                   "error": error, "qc": qc, "output": str(output) if output else None,
                   "output_sha256": file_hash(output) if output and Path(output).is_file() else None,
                   "creative_review": "pending"}
        atomic_json(folder / "result.json", outcome)
        self.append("run_failed" if error else "run_completed", actor=actor, run_id=run,
                    revision_id=revision, **outcome)
        if not error:
            with self.lock():
                p = self.path / "project.json"
                project = json.loads(p.read_text())
                project["current_revision"] = revision
                atomic_json(p, project)

    def feedback(self, revision, text, actor, target=None):
        check_id(revision, "rev")
        if not (self.path / "revisions" / revision / "manifest.json").is_file():
            raise ValueError(f"Unknown revision: {revision}")
        return self.append("feedback_recorded", actor=actor, revision_id=revision,
                           issue_id=uid("issue"), feedback=text, target=target, status="open")

    def resolve(self, issue, revision, evidence, actor):
        check_id(revision, "rev")
        check_id(issue, "issue")
        events = self.events()
        if not any(e.get("issue_id") == issue and e["type"] == "feedback_recorded" for e in events):
            raise ValueError(f"Unknown feedback issue: {issue}")
        result = self.path / "revisions" / revision / "result.json"
        if not result.exists() or json.loads(result.read_text())["status"] != "rendered":
            raise ValueError("Resolution requires a successfully rendered revision")
        origin = next(e["revision_id"] for e in events if e.get("issue_id") == issue and e["type"] == "feedback_recorded")
        ancestor = revision
        while ancestor and ancestor != origin:
            manifest = json.loads((self.path / "revisions" / ancestor / "manifest.json").read_text())
            ancestor = manifest.get("parent_revision_id")
            if ancestor:
                check_id(ancestor, "rev")
        if ancestor != origin or revision == origin:
            raise ValueError("Resolving revision must descend from the feedback revision")
        evidence = Path(evidence).resolve()
        if not evidence.is_file():
            raise ValueError("Resolution requires a saved QC evidence file")
        return self.append("feedback_resolved", actor=actor, revision_id=revision, issue_id=issue,
                           evidence={"path": str(evidence), "sha256": file_hash(evidence)}, status="reviewed_by_actor")

    def handoff(self):
        events = self.events()
        resolved = {e["issue_id"] for e in events if e["type"] == "feedback_resolved"}
        return {"project": json.loads((self.path / "project.json").read_text()),
                "open_feedback": [e for e in events if e["type"] == "feedback_recorded" and e["issue_id"] not in resolved],
                "recent_failures": [e for e in events if e["type"] == "run_failed"][-5:],
                "recent_decisions": [e for e in events if e["type"] in {"decision_recorded", "feedback_resolved"}][-10:],
                "recent_runs": [e for e in events if e["type"] in {"run_completed", "run_failed"}][-5:],
                "lessons": self.lessons(),
                "legacy_feedback_source": "memory/legacy-feedback.json",
                "creative_rulebooks": [".agents/skills/youtube-edit/references/editing-rules.md",
                                       ".agents/skills/youtube-edit/references/editing-rules-talking-head.md"]}

    def lessons(self):
        folder = self.root / "memory" / "lessons"
        if not folder.exists():
            return []
        with (folder / ".lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_SH)
            return [v for p in sorted(folder.glob("*.json"))
                    if (v := json.loads(p.read_text())).get("status") == "active"
                    and (v["scope"] == "universal" or v["scope"] == "category:talking_head"
                         or v["scope"] == "project:" + project_id(self.project))]


    def lesson(self, text, scope, evidence_event, actor, supersedes=None):
        events = self.events()
        if not any(e["event_id"] == evidence_event for e in events):
            raise ValueError("A lesson must link an existing evidence event")
        allowed = {"universal", "category:talking_head", "project:" + project_id(self.project)}
        if scope not in allowed:
            raise ValueError(f"scope must be one of {sorted(allowed)}")
        folder = self.root / "memory" / "lessons"
        folder.mkdir(parents=True, exist_ok=True)
        with (folder / ".lock").open("a") as lesson_lock:
            fcntl.flock(lesson_lock, fcntl.LOCK_EX)
            if supersedes:
                check_id(supersedes, "lesson")
                old_path = folder / (supersedes + ".json")
                old = json.loads(old_path.read_text())
                if old["status"] != "active":
                    raise ValueError("Cannot supersede an inactive lesson")
                if old["scope"] != scope:
                    raise ValueError("Superseding lessons must have the same scope")
            lesson = {"schema_version": 1, "lesson_id": uid("lesson"), "text": text,
                      "scope": scope, "status": "active", "evidence_project": project_id(self.project),
                      "evidence_event": evidence_event, "actor": actor, "created_at": now(), "supersedes": supersedes}
            atomic_json(folder / (lesson["lesson_id"] + ".json"), lesson)
            if supersedes:
                old["status"] = "superseded"
                old["superseded_by"] = lesson["lesson_id"]
                atomic_json(old_path, old)
        self.append("lesson_saved", actor=actor, lesson_id=lesson["lesson_id"], scope=scope)
        return lesson
