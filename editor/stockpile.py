"""Search and instantiate reusable compositions without modifying shared sources."""
import html
import json
import math
from pathlib import Path
import re
import shutil

from .core import ROOT, file_hash, resolve_asset
from .history import atomic_json, now


def catalogue(root=ROOT):
    path = Path(root)/"animations/_fx_library/registry.json"
    if not path.is_file():
        raise ValueError("Effect stockpile missing; run npm ci")
    return json.loads(path.read_text())


def normalize(value):
    return re.sub(r"[\s_]+", "-", value.strip().lstrip("@").lower())


def find_effect(name, root=ROOT):
    data = catalogue(root)
    wanted = normalize(name)
    by_slug = {e["slug"]:e for e in data["templates"]}
    for effect in data["templates"]:
        if wanted in {normalize(effect["slug"]), *[normalize(a) for a in effect.get("aliases",[])]}:
            return effect
    for reference in data.get("reference_catalogues",[]):
        for entry in reference["effects"]:
            if normalize(entry["label"]) == wanted:
                return by_slug[entry["slug"]]
    raise ValueError(f"Unknown stockpile effect: {name}")


def check_parameters(effect, variables, duration=None):
    """Fail before browser execution for structural/data/media mistakes."""
    if not isinstance(variables,dict):
        raise ValueError("variables must be a JSON object")
    unknown = set(variables)-set(effect["variables"])
    if unknown:
        raise ValueError(f"Unknown variables: {sorted(unknown)}")
    unbound = set(variables)&set(effect.get("unbound_variables",[]))
    if unbound:
        raise ValueError(f"Unimplemented variables: {sorted(unbound)}")
    values = {**effect["variables"],**variables}
    seconds = effect["duration_sec"] if duration is None else duration
    def finite(v):return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)
    minimum=effect.get("min_duration_sec",1)
    if not finite(seconds) or not minimum <= seconds <= 120:
        raise ValueError(f"duration must be {minimum}..120 seconds for this effect")
    for key, default in effect["variables"].items():
        value=values[key]
        if isinstance(default,bool):ok=isinstance(value,bool)
        elif isinstance(default,(int,float)):ok=finite(value)
        elif isinstance(default,list):ok=isinstance(value,list)
        elif isinstance(default,dict):ok=isinstance(value,dict)
        else:ok=isinstance(value,str)
        if not ok:raise ValueError(f"Invalid type for {key}")
    for key in effect.get("required_media_variables",[]):
        if not values.get(key):
            raise ValueError(f"{key} is required to instantiate this effect with actual media")
    slug=effect["slug"]
    for key in ("accent","tint"):
        if key in values and not re.fullmatch(r"#[0-9a-fA-F]{6}",values[key]):
            raise ValueError(f"{key} must be a six-digit hex color")
    if slug=="couch-wall" and not 0.5<=values["spread"]<=1.5:
        raise ValueError("spread must be 0.5..1.5")
    if slug=="glass-type":
        if not 40<=values["fontSize"]<=360:raise ValueError("fontSize must be 40..360")
        if not 1<=len(values["text"])<=32:raise ValueError("text needs 1..32 characters")
    if slug=="cover-story" and not 1<=len(values["masthead"])<=24:
        raise ValueError("masthead needs 1..24 characters")
    if slug=="profile-card" and not 25<=values["widthPercent"]<=80:
        raise ValueError("widthPercent must be 25..80")
    if slug=="chart-grow":
        if not 2<=len(values["values"])<=12 or not all(finite(v) for v in values["values"]):
            raise ValueError("Chart requires 2..12 finite data values")
        if len(values["labels"])!=len(values["values"]) or not all(isinstance(v,str) for v in values["labels"]):
            raise ValueError("Chart requires one text label per value")
        if not 5<=values["yPercent"]<=55:raise ValueError("yPercent must be 5..55")
    if slug=="couch-wall" and not 1<=len(values["cards"])<=9:
        raise ValueError("cards requires 1..9 media entries")
    if slug=="proof-player":
        sequence=values["sequence"]
        if not 1<=len(sequence)<=20:raise ValueError("sequence needs 1..20 entries")
        previous=0
        for entry in sequence:
            if not isinstance(entry,dict) or not isinstance(entry.get("src"),str) or not entry.get("src") or not isinstance(entry.get("label"),str):
                raise ValueError("Every sequence entry requires label and src")
            start,hold=entry.get("start"),entry.get("duration")
            if not finite(start) or not finite(hold) or hold<=0 or start<previous-1e-7 or start+hold>seconds-0.3:
                raise ValueError("Sequence entries must be ordered, non-overlapping, and fit before the exit")
            if not finite(entry.get("mediaStart",0)) or entry.get("mediaStart",0)<0:
                raise ValueError("mediaStart must be non-negative")
            previous=start+hold
    if slug=="checklist":
        times=values["completeTimes"]
        if not 1<=len(values["items"])<=8 or len(times)!=len(values["items"]) or not all(isinstance(v,str) and v for v in values["items"]):
            raise ValueError("checklist needs 1..8 items and one completion time per item")
        if not all(finite(t) and 0.3<=t<seconds-0.3 and (i==0 or t>times[i-1]) for i,t in enumerate(times)):
            raise ValueError("Completion times must increase within the hold interval")
    for key in ("yPercent","mastheadY"):
        if key in values and not 5<=values[key]<=70:raise ValueError(f"{key} must be 5..70")
    return values,seconds


ASSET_KEYS={"cards","subjectAsset","backgroundAsset","profileAsset","src","logo","icon","icons",
            "reelAssets","thumbAssets","screenAsset","deviceFrame","gridTexture","grainOverlay",
            "cutoutHandle","reelCards","previewAsset"}


def instantiate(name, output, variables=None, *, project="Default", duration=None, root=ROOT):
    effect=find_effect(name,root)
    values,seconds=check_parameters(effect,variables or {},duration)
    source=Path(root)/Path(effect["composition_path"]).parent
    output=Path(output).resolve()
    library=(Path(root)/"animations/_fx_library").resolve()
    if output==source.resolve() or source.resolve().is_relative_to(output) or output.is_relative_to(library):
        raise ValueError("Create instances outside the shared library")
    # Resolve inputs before creating the destination; a missing asset leaves no partial instance.
    assets={}
    def convert(value,key=""):
        if key in ASSET_KEYS and value and not isinstance(value,(str,list,dict)):
            raise ValueError(f"{key} must contain local media paths or media objects")
        if isinstance(value,dict) and "src" in value:
            if not isinstance(value["src"],str) or not value["src"]:
                raise ValueError("Media src must be a non-empty string")
            offset=value.get("mediaStart",0)
            if not isinstance(offset,(int,float)) or isinstance(offset,bool) or not math.isfinite(offset) or offset<0:
                raise ValueError("mediaStart must be a finite non-negative number")
        if key in {"cards","icons","reelAssets","thumbAssets","reelCards"} and isinstance(value,list):
            if not all((isinstance(v,str) and v) or (isinstance(v,dict) and isinstance(v.get("src"),str) and v["src"]) for v in value):
                raise ValueError(f"{key} entries require a media path or src object")
        if isinstance(value,str) and value and (key in ASSET_KEYS or value.startswith(("@asset/","@project/"))):
            path=resolve_asset(value,project,root)
            if not path.is_file():raise ValueError(f"Missing media asset: {value}")
            fingerprint=file_hash(path)
            local="media/"+fingerprint[:16]+path.suffix.lower()
            assets[local]={"source":str(path),"sha256":fingerprint}
            return local
        if isinstance(value,list):return [convert(v,key) for v in value]
        if isinstance(value,dict):return {k:convert(v,k) for k,v in value.items()}
        return value
    # Defaults in older demo packs use unresolved placeholder handles. Require caller overrides.
    resolved=convert(values)
    output.mkdir(parents=True,exist_ok=False)
    try:
        shutil.copytree(source,output,dirs_exist_ok=True,ignore=shutil.ignore_patterns(".hyperframes"))
        for local,info in assets.items():
            dest=output/local;dest.parent.mkdir(exist_ok=True);shutil.copy2(info["source"],dest)
        page=output/"index.html"
        content=page.read_text()
        match=re.search(r"data-composition-variables='([^']*)'",content)
        if not match:raise ValueError("Composition variable schema missing")
        schema=json.loads(html.unescape(match.group(1)))
        for declaration in schema:
            value=resolved[declaration["id"]]
            declaration["default"]=json.dumps(value) if isinstance(value,(dict,list)) else value
        encoded=html.escape(json.dumps(schema),quote=True)
        content=content[:match.start(1)]+encoded+content[match.end(1):]
        fallback=json.dumps(resolved).replace("</","<\\/")
        content=re.sub(r'(      : )[^\n]+;',lambda m:m.group(1)+fallback+';',content,count=1)
        content=re.sub(r'data-duration="[^"]+"',f'data-duration="{seconds}"',content,count=1)
        page.write_text(content)
        atomic_json(output/"variables.json",resolved)
        atomic_json(output/"instance.json",{"schema_version":1,"effect":effect["slug"],"status":effect["status"],
                    "created_at":now(),"duration_sec":seconds,"source_composition_sha256":file_hash(source/"index.html"),
                    "assets":assets,"variables":resolved,"fidelity_notes":effect["fidelity_notes"]})
        return {"composition":str(output),"effect":effect["slug"],"duration_sec":seconds,
                "render_argv":[str(Path(root)/"node_modules/.bin/hyperframes"),"render",str(output),"--format","mov","--output",str(output.parent/(output.name+".mov"))],
                "edl_effect":{"type":"@hyperframes","composition":str(output),"start_raw":0,"duration":seconds},
                "note":"Set the source trigger explicitly. This is an experimental reference composition, not a fidelity certification."}
    except Exception:
        shutil.rmtree(output)
        raise
