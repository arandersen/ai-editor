"""Validated talking-head renderer. All subprocesses and outcomes enter project history."""
import copy
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from .core import (ROOT, SUPPORTED, compile_edl, duration, effect_name, effect_range,
                   file_hash, intersections, validate)
from .history import History, atomic_json


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def atempo(speed):
    if not math.isfinite(speed) or speed <= 0:
        raise ValueError("Playback speed must be positive and finite")
    parts = []
    while speed > 2:
        parts.append("atempo=2")
        speed /= 2
    while speed < 0.5:
        parts.append("atempo=0.5")
        speed /= 0.5
    return ",".join(parts + [f"atempo={speed:.8f}"])


def fit_filter(w, h, mode="crop", transparent=False):
    if mode == "contain":
        color = ":color=black@0" if transparent else ""
        return f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2{color},setsar=1"
    return f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1"


def frame_segments(segments, fps):
    result = copy.deepcopy(segments)
    for s in result:
        frames = math.floor((s["end"] - s["start"]) / s.get("speed", 1) * fps + 1e-7)
        if frames < 1:
            raise ValueError("Selection is shorter than one output frame")
        s["frame_count"] = frames
        s["end"] = s["start"] + frames / fps * s.get("speed", 1)
    return result


def segment_filter(s, w, h, fps, fit="crop", incoming=False):
    d = s["frame_count"] / fps
    chain = [f"setpts=(PTS-STARTPTS)/{s.get('speed', 1):.8f}"]
    z = s.get("zoom", 1)
    if z > 1:
        chain.append(f"crop=iw/{z}:ih/{z}:(iw-ow)/2:(ih-oh)*0.42")
    chain += [fit_filter(w, h, fit), f"fps={fps}", f"trim=end_frame={s['frame_count']}", f"setpts=N/({fps}*TB)"]
    if s.get("grade") == "warm":
        chain.append("colorchannelmixer=rr=1.17:gg=1.10:bb=1.03,eq=saturation=1.12")
    if s.get("grade") == "moody":
        chain.append("curves=m='0/0.08 0.25/0.22 0.75/0.72 1/0.90',eq=saturation=0.85,vignette=PI/5")
    # Time belongs in filter enable, never in a boxblur radius expression.
    if s.get("transition_out") in {"@whip-pan", "whip_pan"}:
        window = min(6 / fps, d / 2)
        chain.append(f"gblur=sigma=12:sigmaV=0.1:enable='gte(t,{d-window:.8f})'")
        chain.append(f"rotate='-0.025*max(0,(t-{d-window:.8f})/{window:.8f})':fillcolor=black")
    if incoming:
        window = min(6 / fps, d / 2)
        chain.append(f"gblur=sigma=12:sigmaV=0.1:enable='lt(t,{window:.8f})'")
    return ",".join(chain + ["format=yuv420p"])


def quoted_concat(path):
    return str(path).replace("'", "'\\''")


class Renderer:
    def __init__(self, history, run, revision, actor):
        self.history, self.run, self.revision, self.actor = history, run, revision, actor

    def command(self, cmd, desc):
        cmd = list(map(str, cmd))
        event = self.history.append("command_started", actor=self.actor, run_id=self.run,
                                    revision_id=self.revision, description=desc, command=cmd)
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
        self.history.append("command_completed", actor=self.actor, run_id=self.run,
                            revision_id=self.revision, command_event=event["event_id"],
                            returncode=res.returncode, stderr_tail=res.stderr[-2000:])
        if res.returncode:
            raise RuntimeError(f"{desc}: {res.stderr[-2000:]}\n{res.stdout[-2000:]}")
        return res

    def render(self, edl, output, tmp, draft):
        fps = edl["fps"]
        w, h = edl["resolution"]
        if draft and w > 1080:
            h = round(h * 1080 / w / 2) * 2
            w = 1080
        source = probe(edl["raw_video"])
        if any(s.get("color_transfer") in {"arib-std-b67", "smpte2084"} for s in source["streams"]):
            raise ValueError("HDR source requires an explicitly reviewed SDR conversion before this Rec.709 renderer")
        has_audio = any(s["codec_type"] == "audio" for s in source["streams"])
        source_duration = float(source["format"]["duration"])
        if any(s["end"] > source_duration + 0.001 for s in edl["segments"]):
            raise ValueError("Keeper range exceeds source duration")
        segments = frame_segments(edl["segments"], fps)
        edl["segments"] = segments
        total = duration(segments)
        for fx in edl["effects"]:
            if not intersections(*effect_range(fx), segments):
                raise ValueError(f"Effect {fx.get('type')} lies entirely in removed footage")
        # Subject layers must use the same crop/zoom as the original segment.
        for s in segments:
            for fx in edl["effects"]:
                a, b = effect_range(fx)
                if SUPPORTED[effect_name(fx["type"])]["zone"] == "top" and max(a, s["start"]) < min(b, s["end"]):
                    s["zoom"] = 1.0
        atomic_json(self.history.path / "revisions" / self.revision / "compiled-edl.json", edl)
        seg_files = []
        for i, s in enumerate(segments):
            path = tmp / f"seg_{i:04d}.mov"
            d = s["frame_count"] / fps
            cmd = ["ffmpeg", "-y", "-v", "error", "-ss", s["start"], "-t", s["end"] - s["start"], "-i", edl["raw_video"]]
            if not has_audio:
                cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a"]
            af = f"{atempo(s.get('speed',1))},aresample=48000,afade=t=in:d=0.015,afade=t=out:st={max(0,d-0.015):.8f}:d=0.015,apad=whole_dur={d:.8f},atrim=duration={d:.8f},asetpts=PTS-STARTPTS"
            incoming = i > 0 and segments[i-1].get("transition_out") in {"@whip-pan", "whip_pan"}
            cmd += ["-vf", segment_filter(s, w, h, fps, edl.get("fit", "crop"), incoming), "-af", af,
                    "-t", d, "-c:v", "libx264", "-preset", "ultrafast", "-crf", "12", "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", path]
            self.command(cmd, f"slice segment {i}")
            seg_files.append(path)
        listing = tmp / "concat.txt"
        listing.write_text("".join(f"file '{quoted_concat(p)}'\n" for p in seg_files))
        stitched = tmp / "stitched.mov"
        self.command(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", listing,
                      "-c", "copy", stitched], "stitch segments")

        # Separate visual PNG generation from timing: no per-word input explosion.
        jobs, events, sfx = [], [], []
        for i, fx in enumerate(edl["effects"]):
            name = effect_name(fx["type"])
            a, b = effect_range(fx)
            intervals = intersections(a, b, segments)
            if "segment_index" in fx:
                intervals = [v for v in intervals if v["segment_index"] == fx["segment_index"]]
            path = None
            if SUPPORTED[name]["backend"] == "swift":
                identifier = f"fx_{i:05d}"
                jobs.append({"id": identifier, "type": "coral_pill_3word" if name in {"coral-captions", "one-word-captions"} else name.replace("-", "_"),
                             "words": fx.get("words"), "activeIndex": fx.get("active_index", 0), "lines": fx.get("lines"),
                             "title": fx.get("title") or fx.get("name") or fx.get("repo") or fx.get("prompt_text"),
                             "subtitle": fx.get("description", fx.get("subtitle")), "stars": fx.get("stars"),
                             "forks": fx.get("forks"), "imagePath": fx.get("logo")})
                path = tmp / (identifier + ".png")
            elif name == "hyperframes":
                path = self.hyperframes(fx, i, tmp, fps, w)
            else:
                path = Path(fx["src"])
            for interval in intervals:
                events.append({**interval, "path": path, "name": name, "fx": fx})
            if fx.get("sfx"):
                # One hit at the retained trigger, never accidentally on a removed source interval.
                if intervals and abs(intervals[0]["raw_start"] - a) < 1e-6:
                    sfx.extend((fx["sfx"], v["start"], fx.get("sfx_volume", 0.5)) for v in intervals
                               if abs(v["raw_start"]-a)<1e-6)
        if jobs:
            jobs.append({"id": "transparent", "type": "blank"})
            spec = tmp / "overlays.json"
            atomic_json(spec, {"canvasWidth": w, "canvasHeight": h, "jobs": jobs})
            self.command(["swift", "-module-cache-path", tmp / "swift-cache", ROOT / "scripts/talking_head_overlays.swift",
                          "--spec", spec, "--outdir", tmp], "render native typography")
            missing = [j["id"] for j in jobs if not (tmp / (j["id"] + ".png")).is_file()]
            if missing:
                raise RuntimeError(f"Native typography failed to produce {missing}")
        captions = [e for e in events if e["name"] in {"coral-captions", "one-word-captions"}]
        events = [e for e in events if e not in captions]
        if captions:
            cap_path = self.caption_track(captions, tmp, total, fps)
            events.append({"path": cap_path, "name": "overlay", "start": 0, "end": total,
                           "asset_offset": 0, "speed": 1, "fx": {}})

        inputs = ["-i", stitched]
        fc, current, input_idx = [], "[0:v]", 1
        for e in events:
            p, fx, name = e["path"], e["fx"], e["name"]
            image = p.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg"}
            if image:
                inputs += ["-loop", "1", "-framerate", fps, "-i", p]
            else:
                asset_info = probe(p)
                if float(asset_info["format"]["duration"]) + 1/fps < e["asset_offset"] + fx.get("asset_start",0) + (e["end"]-e["start"])*e["speed"]:
                    raise ValueError(f"Overlay media too short for source-time interval: {p}")
                inputs += ["-i", p]
            label = f"ov{input_idx}"
            size = "format=rgba," + fit_filter(w, h, "contain", transparent=True)
            x, y = "0", "0"
            if name == "real-screenshot":
                width = max(2, round(w * fx.get("width_percent", 90) / 100 / 2) * 2)
                size = f"scale={width}:-2,setsar=1"
                x, y = "(W-w)/2", f"H*{fx.get('y_percent',5)/100}"
            chain = f"[{input_idx}:v]{size},format=rgba"
            if not image:
                asset_offset = e["asset_offset"] + fx.get("asset_start", 0)
                chain += f",trim=start={asset_offset:.8f}:end={asset_offset+(e['end']-e['start'])*e['speed']:.8f},setpts=(PTS-STARTPTS)/{e['speed']:.8f}"
            else:
                chain += ",setpts=PTS-STARTPTS"
            chain += f",setpts=PTS+{e['start']:.8f}/TB[{label}]"
            fc.append(chain)
            next_label = f"[v{input_idx}]"
            fc.append(f"{current}[{label}]overlay=x={x}:y={y}:eof_action=pass:repeatlast=0:enable='gte(t,{e['start']:.8f})*lt(t,{e['end']:.8f})'{next_label}")
            current = next_label
            input_idx += 1
            if name == "text-behind-head":
                matte = fx["cutout_mov"]
                streams = probe(matte)["streams"]
                pix = next(s for s in streams if s["codec_type"] == "video").get("pix_fmt", "")
                if not any(token in pix for token in ("yuva", "rgba", "argb", "bgra", "gbrap")):
                    raise ValueError("cutout_mov does not expose an alpha-capable pixel format")
                inputs += ["-i", matte]
                offset = e["asset_offset"] + fx.get("asset_start", 0)
                fc.append(f"[{input_idx}:v]format=rgba,{fit_filter(w,h,edl.get('fit','crop'),transparent=True)},trim=start={offset:.8f}:end={offset+(e['end']-e['start'])*e['speed']:.8f},setpts=(PTS-STARTPTS)/{e['speed']:.8f}+{e['start']:.8f}/TB[matte{input_idx}]")
                nxt = f"[v{input_idx}]"
                fc.append(f"{current}[matte{input_idx}]overlay=eof_action=pass:repeatlast=0:enable='gte(t,{e['start']:.8f})*lt(t,{e['end']:.8f})'{nxt}")
                current = nxt
                input_idx += 1
        # Always create a genuine video output label, including the no-overlay case.
        fc.append(f"{current}fps={fps},format=yuv420p[vout]")
        fc.append("[0:a]highpass=f=80,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,asplit=2[voice][duck]")
        audio = ["[voice]"]
        if edl.get("music"):
            inputs += ["-stream_loop", "-1", "-i", edl["music"]]
            fc += [f"[{input_idx}:a]aresample=48000,volume={edl.get('music_volume',0.08)}[bgm]",
                   "[bgm][duck]sidechaincompress=threshold=0.025:ratio=6:attack=15:release=250[ducked]"]
            audio.append("[ducked]")
            input_idx += 1
        else:
            fc.append("[duck]anullsink")
        for path, onset, volume in sfx:
            inputs += ["-i", path]
            fc.append(f"[{input_idx}:a]aresample=48000,volume={float(volume)},adelay={round(onset*1000)}:all=1[sfx{input_idx}]")
            audio.append(f"[sfx{input_idx}]")
            input_idx += 1
        fc.append("".join(audio) + f"amix=inputs={len(audio)}:duration=first:normalize=0,alimiter=limit=0.95:level=0:latency=1,atrim=duration={total:.8f}[aout]")
        graph = tmp / "master.ffgraph"
        graph.write_text(";\n".join(fc))
        self.command(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex_script", graph,
                      "-map", "[vout]", "-map", "[aout]", "-t", total, "-r", fps,
                      "-c:v", "libx264", "-preset", "veryfast" if draft else "slow", "-crf", "20" if draft else "14",
                      "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                      "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", output], "encode master")
        data = probe(output)
        video = next(s for s in data["streams"] if s["codec_type"] == "video")
        num, den = map(float, video["avg_frame_rate"].split("/"))
        measured = float(data["format"]["duration"])
        qc = {"resolution": [video["width"], video["height"]], "fps": num / den,
              "duration": measured, "expected_duration": total,
              "checks": {"dimensions": [video["width"],video["height"]] == [w,h],
                         "fps": abs(num / den - fps) < 0.001,
                         "duration": abs(measured-total) <= max(0.06, 2/fps)},
              "creative_review": "pending", "caption_events": len(captions)}
        self.command(["ffmpeg", "-v", "error", "-i", output, "-f", "null", "-"], "verify complete output decode")
        if not all(qc["checks"].values()):
            raise RuntimeError(f"Output failed QC: {qc}")
        return qc

    def caption_track(self, captions, tmp, total, fps):
        rows, cursor = [], 0
        for e in sorted(captions, key=lambda e: e["start"]):
            a, b = round(e["start"] * fps), round(e["end"] * fps)
            if a < cursor:
                raise ValueError("Overlapping caption events; review transcript timing or manual effects")
            if a > cursor:
                rows.append((tmp / "transparent.png", (a-cursor)/fps))
            if b > a:
                rows.append((e["path"], (b-a)/fps))
            cursor = b
        if cursor < round(total * fps):
            rows.append((tmp / "transparent.png", (round(total*fps)-cursor)/fps))
        listing = tmp / "caption-frames.txt"
        listing.write_text("".join(f"file '{quoted_concat(p)}'\noption framerate {fps}\nduration {d:.8f}\n" for p,d in rows)
                           + f"file '{quoted_concat(tmp / 'transparent.png')}'\noption framerate {fps}\n")
        path = tmp / "captions.mov"
        self.command(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", listing,
                      "-vf", f"fps={fps}", "-t", total, "-c:v", "qtrle", "-pix_fmt", "argb", path], "assemble caption track")
        return path

    def hyperframes(self, fx, index, tmp, fps, w):
        # Copy rather than mutate a reusable scene. Explicit compositions expose the same adapter.
        source = Path(fx["composition"])
        if source.is_file():
            source = source.parent
        target = tmp / f"composition-{index}"
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("node_modules", ".hyperframes"))
        html = target / "index.html"
        if not html.is_file():
            raise ValueError("HyperFrames composition must contain index.html")
        # All scene dependencies are project-relative; rewrite local script URLs after copying.
        import re
        def scripts(match):
            value = match.group(1)
            if value.startswith(("http:", "https:", "data:")):
                raise ValueError("Use local, pinned scripts in HyperFrames compositions")
            resolved = (source / value).resolve()
            dest = target / "vendor" / resolved.name
            dest.parent.mkdir(exist_ok=True)
            shutil.copy2(resolved, dest)
            self.history.append("scene_script_resolved", actor=self.actor, run_id=self.run,
                                revision_id=self.revision, source=str(resolved), sha256=file_hash(resolved))
            return 'src="vendor/' + dest.name + '"'
        html.write_text(re.sub(r'src="([^"]+\.js)"', scripts, html.read_text()))
        if fx.get("variables"):
            params = source / "params.json"
            metadata = json.loads(params.read_text()) if params.exists() else {}
            unbound = set(metadata.get("unbound_variables", [])) & set(fx["variables"])
            if unbound:
                raise ValueError(f"Scene parameters are not implemented: {sorted(unbound)}")
            def resolve_variable(value):
                if isinstance(value, str) and value.startswith("@"):
                    from .core import resolve_asset
                    resolved = resolve_asset(value, self.history.project, self.history.root)
                    if not resolved.is_file():
                        raise ValueError(f"Scene variable asset is missing: {value}")
                    dest = target / "media" / (file_hash(resolved)[:12] + resolved.suffix)
                    dest.parent.mkdir(exist_ok=True)
                    shutil.copy2(resolved, dest)
                    self.history.append("scene_asset_resolved", actor=self.actor, run_id=self.run,
                                        revision_id=self.revision, source=str(resolved), sha256=file_hash(resolved))
                    return "media/" + dest.name
                if isinstance(value, list):
                    return [resolve_variable(v) for v in value]
                if isinstance(value, dict):
                    return {k:resolve_variable(v) for k,v in value.items()}
                return value
            fx = {**fx,"variables":resolve_variable(fx["variables"])}
        executable = ROOT / "node_modules/.bin/hyperframes"
        if not executable.exists():
            raise ValueError("Pinned HyperFrames missing; run npm ci")
        self.command([executable, "lint", target], "lint effect composition")
        out = tmp / f"hf-{index}.mov"
        command = [executable, "render", target, "--format", "mov", "--fps", fps, "--output", out]
        if fx.get("variables"):
            var_path = tmp / f"vars-{index}.json"
            # HyperFrames declares array/object variables as JSON strings in these scenes.
            atomic_json(var_path, {k:json.dumps(v) if isinstance(v,(dict,list)) else v for k,v in fx["variables"].items()})
            # Pinned 0.8.214 has a broken JSON-file reader; direct JSON avoids that path.
            command += ["--variables", var_path.read_text(), "--strict-variables"]
        if w == 2160:
            command += ["--resolution", "portrait-4k"]
        self.command(command, "render effect composition")
        return out


def render_project(edl, output, *, draft=False, model="unspecified", parent=None, root=ROOT):
    if not isinstance(edl, dict):
        raise ValueError("EDL must be a JSON object")
    project = edl.get("project")
    history = History(project if isinstance(project,str) and project.strip() else "Invalid EDL", root)
    actor = {"role": "editor", "model": model}
    run, revision, folder = history.begin(edl, actor, parent)
    output = Path(output).resolve()
    try:
        errors = validate(edl, check_files=True, root=root)
        if errors:
            raise ValueError("\n".join(errors))
        if output.exists():
            raise ValueError(f"Refusing to overwrite existing artifact: {output}; choose a new revision filename")
        compiled = compile_edl(edl, root)
        inputs = {compiled["raw_video"], *[compiled[k] for k in ("music", "transcript_json") if compiled.get(k)]}
        inputs |= {fx[k] for fx in compiled["effects"] for k in ("src", "logo", "sfx", "cutout_mov") if fx.get(k)}
        for fx in compiled["effects"]:
            if fx.get("composition"):
                scene = Path(fx["composition"])
                inputs |= {str(p) for p in (scene.parent if scene.is_file() else scene).rglob("*")
                           if p.is_file() and not any(v in p.parts for v in ("node_modules", ".hyperframes"))}
        atomic_json(folder / "inputs.json", {p: file_hash(p) for p in sorted(inputs)})
        history.append("lessons_loaded", actor=actor, run_id=run, revision_id=revision,
                       lesson_ids=[v["lesson_id"] for v in history.lessons()])
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="ai-editor-") as tmp:
            temp_output = Path(tmp) / "output.mp4"
            qc = Renderer(history, run, revision, actor).render(compiled, temp_output, Path(tmp), draft)
            # Publish complete bytes exclusively, even if another run won a race.
            with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".publishing-", delete=False) as staged:
                staging_path = Path(staged.name)
                with temp_output.open("rb") as src:
                    shutil.copyfileobj(src, staged)
                staged.flush()
                os.fsync(staged.fileno())
            try:
                os.link(staging_path, output)
            finally:
                staging_path.unlink(missing_ok=True)
        atomic_json(folder / "qc.json", qc)
        history.finish(run, revision, folder, actor, qc=qc, output=output)
        return {"run_id": run, "revision_id": revision, "output": str(output), "qc": qc, "history": str(history.path)}
    except Exception as exc:
        history.finish(run, revision, folder, actor, error=str(exc))
        raise
