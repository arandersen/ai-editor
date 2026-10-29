"""Project-scoped inspection artifacts and verified-size viewing proxies."""
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile

from .core import ROOT, file_hash
from .history import atomic_json, project_id
from .render import probe


def inspect_video(source, project=None, table_crop=False, max_mb=14, root=ROOT):
    source = Path(source).resolve()
    data = probe(source)
    length = float(data["format"]["duration"])
    if not math.isfinite(length) or length <= 0 or max_mb < 1:
        raise ValueError("Positive duration and proxy size budget >=1 MB required")
    fingerprint = file_hash(source)
    project = project or source.parent.name
    out = Path(root)/"renders/drafts"/project_id(project)/(source.stem+"-"+fingerprint[:10])
    out.mkdir(parents=True, exist_ok=True)
    has_audio = any(s["codec_type"] == "audio" for s in data["streams"])

    def run(cmd):
        result = subprocess.run(list(map(str,cmd)), capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stderr[-2000:])
        return result

    filters = run(["ffmpeg","-hide_banner","-filters"]).stdout
    drawtext = " drawtext " in filters
    stamp = ",drawtext=text='%{pts\\:hms}':x=10:y=10:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.75" if drawtext else ""
    sheet = out/"contact-sheet.jpg"
    base = ["ffmpeg","-y","-v","error","-i",source]
    run([*base,"-vf",f"fps=30/{length:.8f}:start_time=0,scale=360:-1{stamp},tile=5x6","-frames:v","1",sheet])
    if table_crop:
        run([*base,"-vf",f"fps=30/{length:.8f}:start_time=0,crop=iw:ih*0.45:0:ih*0.55,scale=360:-1{stamp},tile=5x6",
             "-frames:v","1",out/"table-sheet.jpg"])
    detect = ["ffmpeg","-hide_banner","-i",source,"-vf","blackdetect=d=0.08:pix_th=0.10"]
    if has_audio:
        detect += ["-af","silencedetect=noise=-35dB:d=0.22"]
    detection = run([*detect,"-f","null","-"]).stderr
    # Split long footage rather than making an unbounded, unwatchable CRF proxy.
    max_bytes = int(max_mb*1_000_000)
    max_part = min(300, max_bytes*8*0.85/(64000+32000))
    count = math.ceil(length/max_part)
    proxies = []
    with tempfile.TemporaryDirectory(prefix="proxy-pass-") as temp:
        for i in range(count):
            start, part_duration = i*length/count, length/count
            path = out/f"proxy-{i+1:03d}.mp4"
            bitrate = max(32000,int(max_bytes*8*0.85/part_duration)-(64000 if has_audio else 0))
            vf = "scale=-2:540,fps=15"
            if drawtext:
                vf += f",drawtext=text='%{{pts\\:hms}}':x=10:y=10:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.75"
            for attempt in range(3):
                common = ["ffmpeg","-y","-v","error","-ss",start,"-t",part_duration,"-i",source,
                          "-vf",vf,"-c:v","libx264","-preset","fast","-b:v",bitrate,
                          "-pix_fmt","yuv420p","-passlogfile",Path(temp)/f"pass-{i}"]
                run([*common,"-pass","1","-an","-f","null","-"])
                run([*common,"-pass","2","-c:a","aac","-b:a","64k","-ac","1","-movflags","+faststart",path])
                if path.stat().st_size <= max_bytes:
                    break
                bitrate = max(16000,int(bitrate*0.7))
            else:
                raise ValueError(f"Proxy exceeds {max_mb}MB after retries; shorten the source or increase budget")
            proxies.append({"path":str(path),"source_start":start,"source_end":start+part_duration,
                            "bytes":path.stat().st_size})
    result = {"schema_version":1,"source":str(source),"source_sha256":fingerprint,"media":data,
              "contact_sheet":str(sheet),"sample_interval":length/30,"burned_timecode":drawtext,
              "proxy_timecode": "part-relative; add source_start", "proxy_max_bytes":max_bytes,"proxies":proxies,
              "silence_starts":[float(s) for s in re.findall(r"silence_start: ([\d.]+)",detection)],
              "black_intervals":[list(map(float,m)) for m in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)",detection)],
              "creative_review":"pending"}
    atomic_json(out/"inspection.json",result)
    return result
