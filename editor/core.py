"""One contract for asset resolution, source/output timing and EDL validation."""
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALIASES = {"coral-pill-3word": "coral-captions", "moody-grade-panel": "moody-grade"}
SUPPORTED = {
    "coral-captions": {"backend": "swift", "zone": "caption"},
    "one-word-captions": {"backend": "swift", "zone": "caption"},
    "text-behind-head": {"backend": "swift", "zone": "top", "cutout": True},
    "tool-label": {"backend": "swift", "zone": "caption"},
    "repo-card": {"backend": "swift", "zone": "top"},
    "prompt-bar": {"backend": "swift", "zone": "top"},
    "real-screenshot": {"backend": "media", "zone": "top"},
    "overlay": {"backend": "media", "zone": "custom"},
    "hyperframes": {"backend": "hyperframes", "zone": "custom"},
}


def effect_name(value):
    name = str(value).lstrip("@").replace("_", "-")
    return ALIASES.get(name, name)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     allow_nan=False).encode()).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def plan_hash(edl):
    return digest({k: v for k, v in edl.items() if k not in
                   {"approval", "storyboard_approved", "revision_id"}})


def resolve_asset(value, project="Default", root=ROOT):
    """Relative file paths are workspace-relative; handles cannot escape their roots."""
    root = Path(root).resolve()
    value = str(value)
    if value.startswith("@"):
        parts = value.split("/")
        if parts[0] == "@asset":
            base, tail = root / "assets", parts[1:]
        elif parts[0] == "@project" and len(parts) >= 3:
            folders = {"raw": "raw", "cutout": "broll", "broll": "broll", "transcript": "transcripts"}
            if parts[1] not in folders or Path(project).name != project or project in {".", ".."}:
                raise ValueError(f"Invalid project asset handle: {value}")
            base, tail = root / folders[parts[1]] / project, parts[2:]
        else:
            raise ValueError(f"Unknown asset handle: {value}")
        path = base.joinpath(*tail).resolve()
        if not path.is_relative_to(base.resolve()):
            raise ValueError(f"Asset handle escapes its root: {value}")
        return path
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def duration(segments):
    return sum((s["end"] - s["start"]) / s.get("speed", 1) for s in segments)


def intersections(start, end, segments):
    """Split a raw-time interval at every edit, preserving local asset offsets."""
    acc = 0.0
    result = []
    for i, s in enumerate(segments):
        speed = s.get("speed", 1.0)
        lo, hi = max(start, s["start"]), min(end, s["end"])
        if hi > lo:
            result.append({"start": acc + (lo - s["start"]) / speed,
                           "end": acc + (hi - s["start"]) / speed,
                           "raw_start": lo, "raw_end": hi,
                           "asset_offset": lo - start, "speed": speed, "segment_index": i})
        acc += (s["end"] - s["start"]) / speed
    return result


def map_time(raw_time, segments):
    acc = 0.0
    for s in segments:
        if s["start"] <= raw_time < s["end"]:
            return acc + (raw_time - s["start"]) / s.get("speed", 1)
        acc += (s["end"] - s["start"]) / s.get("speed", 1)
    return None


def effect_range(fx):
    start = fx.get("start_raw", fx.get("trigger_raw", fx.get("start", 0)))
    end = fx.get("end_raw", fx.get("end", start + fx.get("duration", 2.5)))
    return start, end


def number(value, minimum=None, maximum=None):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and (minimum is None or value >= minimum)
            and (maximum is None or value <= maximum))


def validate(edl, check_files=False, root=ROOT):
    errors = []
    if not isinstance(edl, dict):
        return ["EDL must be a JSON object"]
    if edl.get("schema_version") != 1:
        errors.append("schema_version must be 1; migrate legacy EDLs explicitly")
    if not isinstance(edl.get("project"), str) or not edl["project"].strip():
        errors.append("project must be a non-empty name")
    res = edl.get("resolution")
    if not (isinstance(res, list) and len(res) == 2 and all(
            isinstance(v, int) and not isinstance(v, bool) and v >= 64 and v % 2 == 0 for v in res)):
        errors.append("resolution must contain two even integer dimensions >= 64")
    if not number(edl.get("fps"), 1, 120):
        errors.append("fps must be between 1 and 120")
    if edl.get("fit", "crop") not in {"crop", "contain"}:
        errors.append("fit must be crop or contain")
    if "jump_cuts" in edl:
        errors.append("jump_cuts is not executable EDL data; use editor plan to propose and review explicit keeper segments")
    if not isinstance(edl.get("raw_video"), str) or not edl.get("raw_video"):
        errors.append("raw_video is required")
    approval = edl.get("approval", {})
    try:
        current_hash = plan_hash(edl)
    except (TypeError, ValueError):
        current_hash = None
        errors.append("EDL must contain finite, JSON-compatible values")
    if not isinstance(approval, dict) or current_hash is None or approval.get("plan_hash") != current_hash or not approval.get("approved_by"):
        errors.append("approval must identify approved_by and match the current plan_hash; run editor approve after review")
    segs = edl.get("segments")
    if not isinstance(segs, list) or not segs:
        errors.append("segments must be a non-empty array of reviewed keeper ranges")
        segs = []
    for i, s in enumerate(segs):
        if not isinstance(s, dict):
            errors.append(f"segment {i}: must be an object")
            continue
        a, b, sp = s.get("start"), s.get("end"), s.get("speed", 1)
        if not number(a, 0) or not number(b, 0) or b <= a:
            errors.append(f"segment {i}: invalid start/end")
        if not number(sp, 0.05, 16):
            errors.append(f"segment {i}: speed must be 0.05..16")
        elif number(a, 0) and number(b, 0) and number(edl.get("fps"), 1, 120) and (b-a)/sp*edl["fps"] < 1-1e-7:
            errors.append(f"segment {i}: selection is shorter than one output frame")
        if not number(s.get("zoom", 1), 1, 3):
            errors.append(f"segment {i}: zoom must be 1..3")
        if s.get("transition_out", "none") not in {"none", "@whip-pan", "whip_pan"}:
            errors.append(f"segment {i}: unsupported transition_out")
        if s.get("grade", "none") not in {"none", "warm", "moody"}:
            errors.append(f"segment {i}: grade must be none, warm or moody; wipe effects are separate")
    effects = edl.get("effects", [])
    if not isinstance(effects, list):
        errors.append("effects must be an array")
        effects = []
    for i, fx in enumerate(effects):
        if not isinstance(fx, dict):
            errors.append(f"effect {i}: must be an object")
            continue
        name = effect_name(fx.get("type", ""))
        if name not in SUPPORTED:
            errors.append(f"effect {i}: unsupported {name!r}; run editor capabilities. Library demos require explicit @hyperframes composition")
        try:
            a, b = effect_range(fx)
            if not number(a, 0) or not number(b, 0) or b <= a:
                errors.append(f"effect {i}: invalid raw-time interval")
        except (TypeError, ValueError):
            errors.append(f"effect {i}: invalid raw-time interval")
        if name in {"coral-captions", "one-word-captions"}:
            words = fx.get("words")
            limit = 1 if name == "one-word-captions" else 3
            if not isinstance(words, list) or not 1 <= len(words) <= limit or not all(isinstance(w, str) and w.strip() for w in words):
                errors.append(f"effect {i}: requires 1..{limit} words")
            elif not isinstance(fx.get("active_index", 0), int) or not 0 <= fx.get("active_index", 0) < len(words):
                errors.append(f"effect {i}: active_index out of bounds")
        if name == "text-behind-head" and not fx.get("cutout_mov"):
            errors.append(f"effect {i}: text-behind-head requires cutout_mov with source-aligned alpha")
        if name == "text-behind-head":
            try:
                a,b = effect_range(fx)
                for j,s in enumerate(segs):
                    if not isinstance(s,dict) or not number(s.get("start"),0) or not number(s.get("end"),0):
                        continue
                    incoming = j > 0 and isinstance(segs[j-1],dict) and segs[j-1].get("transition_out") in {"@whip-pan","whip_pan"}
                    if number(a,0) and number(b,0) and max(a,s["start"]) < min(b,s["end"]) and (s.get("grade","none") != "none" or s.get("transition_out","none") != "none" or incoming):
                        errors.append(f"effect {i}: graded/transitioned foreground depth is not implemented; use a precomposited @overlay or ungraded hook segment")
            except (TypeError, ValueError):
                pass
        if name in {"overlay", "real-screenshot"} and not fx.get("src"):
            errors.append(f"effect {i}: src is required")
        if name == "hyperframes" and not fx.get("composition"):
            errors.append(f"effect {i}: composition is required")
        if name == "hyperframes" and fx.get("demo") is not True and "_fx_library" in str(fx.get("composition", "")):
            errors.append(f"effect {i}: library scene is experimental; set demo=true to preview, not a certified source-video effect")
        if "segment_index" in fx and (not isinstance(fx["segment_index"], int) or not 0 <= fx["segment_index"] < len(segs)):
            errors.append(f"effect {i}: segment_index out of bounds")
        if "sfx_volume" in fx and not number(fx["sfx_volume"], 0, 2):
            errors.append(f"effect {i}: sfx_volume must be 0..2")
        if "asset_start" in fx and not number(fx["asset_start"], 0):
            errors.append(f"effect {i}: asset_start must be non-negative")
        for key in ("x_percent", "y_percent"):
            if key in fx and not number(fx[key], 0, 100):
                errors.append(f"effect {i}: {key} must be 0..100")
        if "width_percent" in fx and not number(fx["width_percent"], 1, 100):
            errors.append(f"effect {i}: width_percent must be 1..100")
        if "x_percent" in fx:
            errors.append(f"effect {i}: x_percent is not implemented; screenshots are centered")
        if name != "real-screenshot" and any(k in fx for k in ("y_percent", "width_percent")):
            errors.append(f"effect {i}: geometry overrides are only supported on @real-screenshot")
    for key in ("captions", "caption_style", "jump_cuts"):
        if key in edl and not isinstance(edl[key], dict if key != "captions" else list):
            errors.append(f"{key}: invalid type")
    if edl.get("caption_style") and not (edl.get("transcript_json") or edl.get("captions")):
        errors.append("caption_style requires transcript_json or timed captions")
    if isinstance(edl.get("caption_style"), dict) and effect_name(edl["caption_style"].get("shortcut", "@coral-captions")) not in {"coral-captions", "one-word-captions"}:
        errors.append("caption_style.shortcut must be @coral-captions or @one-word-captions")
    if isinstance(edl.get("caption_style"), dict) and set(edl["caption_style"]) - {"shortcut"}:
        errors.append("caption_style currently supports shortcut only; typography uses the documented native preset")
    if not number(edl.get("music_volume", 0.08), 0, 1):
        errors.append("music_volume must be 0..1")
    if check_files:
        refs = [("raw_video", edl.get("raw_video")), ("music", edl.get("music")),
                ("transcript_json", edl.get("transcript_json"))]
        refs += [(f"effect {i}.{k}", fx.get(k)) for i, fx in enumerate(effects) if isinstance(fx, dict)
                 for k in ("src", "logo", "sfx", "cutout_mov", "composition")]
        for label, value in refs:
            if value:
                try:
                    p = resolve_asset(value, edl.get("project", "Default"), root)
                    if not p.exists() or (p.is_file() and not p.stat().st_size):
                        errors.append(f"{label}: missing/empty asset {p}")
                except ValueError as exc:
                    errors.append(str(exc))
    return errors


def read_words(payload):
    if not isinstance(payload, dict):
        raise ValueError("Transcript must be a JSON object")
    if isinstance(payload.get("words"), list):
        words = payload["words"]
    else:
        words = [w for seg in payload.get("segments", payload.get("sentences", []))
                 for w in seg.get("words", seg.get("tokens", []))]
    result = []
    for i, w in enumerate(words):
        if not isinstance(w, dict):
            raise ValueError(f"Transcript word {i} must be an object")
        text, a, b = w.get("word", w.get("text", "")).strip(), w.get("start"), w.get("end")
        if not text or not number(a, 0) or not number(b, 0) or b <= a:
            raise ValueError(f"Transcript word {i} has invalid text/start/end")
        result.append({**w, "word": text, "id": w.get("id", f"w_{i:05d}")})
    if not result:
        raise ValueError("Transcript has no timed words")
    return result


def caption_events(words, segments, style, effects):
    mode = effect_name(style.get("shortcut", "@coral-captions"))
    if mode not in {"coral-captions", "one-word-captions"}:
        raise ValueError(f"Unsupported automatic caption style: {mode}")
    result = []
    # Group within each retained segment, never across a cut, a speaker or a long pause.
    for segment_index, seg in enumerate(segments):
        kept = [w for w in words if seg["start"] <= w["start"] < seg["end"]]
        chunks, chunk = [], []
        for w in kept:
            if chunk and (len(chunk) >= (1 if mode == "one-word-captions" else 3)
                          or sum(len(v["word"])+1 for v in chunk)+len(w["word"]) > 24
                          or w["start"] - chunk[-1]["end"] > 0.3
                          or w.get("speaker") != chunk[-1].get("speaker")):
                chunks.append(chunk)
                chunk = []
            chunk.append(w)
        if chunk:
            chunks.append(chunk)
        for group in chunks:
            for index, w in enumerate(group):
                a, b = max(w["start"], seg["start"]), min(w["end"], seg["end"])
                if b <= a:
                    continue
                # A label occupies the caption zone: split around it rather than overlap.
                intervals = [(a, b)]
                for fx in effects:
                    if effect_name(fx.get("type")) == "tool-label":
                        if "segment_index" in fx and fx["segment_index"] != segment_index:
                            continue
                        f0, f1 = effect_range(fx)
                        intervals = [(lo, hi) for x, y in intervals for lo, hi in
                                     [(x, min(y, f0)), (max(x, f1), y)] if hi > lo]
                for lo, hi in intervals:
                    result.append({"type": "@" + mode, "start_raw": lo, "end_raw": hi,
                                   "words": [v["word"] for v in group], "active_index": index,
                                   "word_id": w["id"], "segment_index": segment_index})
    return result


def compile_edl(edl, root=ROOT):
    result = copy.deepcopy(edl)
    project = result["project"]
    for key in ("raw_video", "music", "transcript_json"):
        if result.get(key):
            result[key] = str(resolve_asset(result[key], project, root))
    for fx in result.setdefault("effects", []):
        for key in ("src", "logo", "sfx", "cutout_mov", "composition"):
            if fx.get(key):
                fx[key] = str(resolve_asset(fx[key], project, root))
    if result.get("caption_style"):
        if result.get("transcript_json"):
            words = read_words(json.loads(Path(result["transcript_json"]).read_text()))
        else:
            words = read_words({"words": result.get("captions", [])})
        result["effects"] += caption_events(words, result["segments"], result["caption_style"], result["effects"])
    return result
