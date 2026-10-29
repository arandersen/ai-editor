import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from editor.core import (caption_events, compile_edl, intersections, map_time,
                         plan_hash, resolve_asset, validate)
from editor.history import History, atomic_json
from editor.render import atempo, frame_segments, render_project


def approved(**changes):
    edl = {"schema_version": 1, "project": "Fixture", "raw_video": "fixture.mp4",
           "resolution": [270, 480], "fps": 60,
           "segments": [{"start": 0, "end": 0.8}], "effects": [], **changes}
    edl["approval"] = {"plan_hash": plan_hash(edl), "approved_by": "test-fixture"}
    return edl


class ContractTests(unittest.TestCase):
    def test_reject_invalid_speeds(self):
        for speed in (0, -1, float("inf"), "fast", True):
            e = approved()
            e["segments"][0]["speed"] = speed
            self.assertTrue(any("speed" in err for err in validate(e)))

    def test_unknown_effect_not_silently_dropped(self):
        self.assertTrue(validate(approved(effects=[{"type": "@nonexistent"}])))

    def test_approval_invalidated_by_edit(self):
        e = approved()
        self.assertEqual(validate(e), [])
        e["segments"][0]["end"] = 0.7
        self.assertTrue(any("approval" in v for v in validate(e)))

    def test_no_implicit_approval(self):
        e = approved()
        del e["approval"]
        self.assertTrue(validate(e))

    def test_caption_effect_is_validated(self):
        self.assertTrue(validate(approved(effects=[{"type": "@coral-captions", "words": ["a","b","c","d"]}])))

    def test_cutout_is_required(self):
        self.assertTrue(validate(approved(effects=[{"type": "@text-behind-head"}])))

    def test_removed_time_has_no_mapping(self):
        segs = [{"start":10,"end":12},{"start":20,"end":22,"speed":2}]
        self.assertIsNone(map_time(15,segs))
        self.assertEqual(map_time(21,segs),2.5)

    def test_cross_cut_effect_is_split_with_asset_offsets(self):
        pieces = intersections(11,21,[{"start":10,"end":12},{"start":20,"end":22,"speed":2}])
        self.assertEqual([(p["start"],p["end"],p["asset_offset"]) for p in pieces],[(1,2,0),(2,2.5,9)])

    def test_handles_confined_and_workspace_relative(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(resolve_asset("@asset/audio/a.wav",root=tmp),Path(tmp).resolve()/"assets/audio/a.wav")
            self.assertEqual(resolve_asset("@project/raw/clip.mov","Name",tmp),Path(tmp).resolve()/"raw/Name/clip.mov")
            for bad in ("@asset/../../outside", "@project/raw/../../../outside", "@unknown/file"):
                with self.assertRaises(ValueError): resolve_asset(bad,"Name",tmp)

    def test_frames_locked_to_schedule(self):
        s = frame_segments([{"start":1,"end":2.019,"speed":1}],60)[0]
        self.assertEqual(s["frame_count"],61)
        self.assertAlmostEqual(s["end"]-s["start"],61/60)

    def test_subframe_selection_rejected(self):
        e = approved(segments=[{"start":0.99,"end":1.0}],fps=30)
        self.assertTrue(any("one output frame" in err for err in validate(e)))
        with self.assertRaises(ValueError): frame_segments(e["segments"],30)

    def test_repeated_source_captions_retain_segment_identity(self):
        segs=[{"start":0,"end":1},{"start":0,"end":1}]
        events=caption_events([{"word":"a","id":"w1","start":0.1,"end":0.3}],segs,{},[])
        mapped=[v for e in events for v in intersections(*[e[k] for k in ("start_raw","end_raw")],segs)
                if v["segment_index"]==e["segment_index"]]
        self.assertEqual(len(mapped),2)
        self.assertAlmostEqual(mapped[1]["start"],1.1)

    def test_unknown_caption_style_rejected_preflight(self):
        self.assertTrue(any("caption_style.shortcut" in err for err in validate(approved(
            caption_style={"shortcut":"@unknown"},transcript_json="words.json"))))

    def test_unimplemented_geometry_rejected(self):
        self.assertTrue(any("geometry" in err for err in validate(approved(effects=[
            {"type":"@repo-card","y_percent":20}]))))

    def test_label_suppression_is_scoped_to_replay(self):
        words=[{"word":"hello","id":"w1","start":0.1,"end":0.4}]
        ev=caption_events(words,[{"start":0,"end":1},{"start":0,"end":1}],{},[
            {"type":"@tool-label","start_raw":0,"end_raw":1,"segment_index":1}])
        self.assertEqual([e["segment_index"] for e in ev],[0])

    def test_tempo_rejects_zero_instead_of_hanging(self):
        with self.assertRaises(ValueError): atempo(0)
        self.assertIn("atempo=2",atempo(4))

    def test_caption_group_and_label_suppression(self):
        words = [{"word":"hello","id":"w1","start":1,"end":1.4},
                 {"word":"world","id":"w2","start":1.5,"end":1.9}]
        events = caption_events(words,[{"start":1,"end":2}],{},
                                [{"type":"@tool-label","start_raw":1.6,"end_raw":1.8}])
        self.assertEqual(events[0]["words"],["hello","world"])
        self.assertFalse(any(max(e["start_raw"],1.6)<min(e["end_raw"],1.8) for e in events))

    def test_captions_do_not_group_across_edits(self):
        words = [{"word":"a","id":"w1","start":1,"end":1.2},
                 {"word":"b","id":"w2","start":2,"end":2.2}]
        ev = caption_events(words,[{"start":1,"end":1.3},{"start":2,"end":2.3}],{},[])
        self.assertEqual([e["words"] for e in ev],[["a"],["b"]])


class HistoryTests(unittest.TestCase):
    def test_revision_parent_failures_feedback_and_scoped_lessons(self):
        with tempfile.TemporaryDirectory() as tmp:
            h, actor = History("Fixture",tmp), {"role":"editor","model":"model-a"}
            run, rev, folder = h.begin(approved(),actor)
            h.finish(run,rev,folder,actor,error="known failed attempt")
            issue = h.feedback(rev,"Do not repeat this",actor)
            lesson = h.lesson("Check the failure", "project:"+h.path.name, issue["event_id"],actor)
            handoff = History("Fixture",tmp).handoff()
            self.assertEqual(handoff["recent_failures"][0]["error"],"known failed attempt")
            self.assertEqual(handoff["open_feedback"][0]["issue_id"],issue["issue_id"])
            self.assertEqual(handoff["lessons"][0]["lesson_id"],lesson["lesson_id"])
            self.assertEqual(History("Other",tmp).lessons(),[])
            run2,rev2,f2 = h.begin(approved(),actor,parent=rev)
            manifest = json.loads((f2/"manifest.json").read_text())
            self.assertEqual(manifest["parent_revision_id"],rev)
            self.assertEqual(json.loads((folder/"edl.json").read_text()),approved())

    def test_concurrent_events_remain_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            h = History("Fixture",tmp)
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                list(pool.map(lambda n:h.append("test",number=n),range(30)))
            self.assertEqual(len(h.events()),30)
            self.assertEqual(len({e["event_id"] for e in h.events()}),30)

    def test_failed_preflight_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):render_project(approved(),Path(tmp)/"out.mp4",root=tmp)
            self.assertEqual(History("Fixture",tmp).events()[-1]["type"],"run_failed")

    def test_feedback_resolution_requires_descendant_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            h,actor=History("Fixture",tmp),{"role":"reviewer","model":"test"}
            run,rev,folder=h.begin(approved(),actor)
            h.finish(run,rev,folder,actor,qc={"checks":{"test":True}})
            issue=h.feedback(rev,"Fix this",actor)
            evidence=Path(tmp)/"qc.json"
            atomic_json(evidence,{"review":"compared before and after"})
            with self.assertRaises(ValueError):h.resolve(issue["issue_id"],rev,evidence,actor)
            run2,rev2,folder2=h.begin(approved(),actor,parent=rev)
            h.finish(run2,rev2,folder2,actor,qc={"checks":{"test":True}})
            h.resolve(issue["issue_id"],rev2,evidence,actor)
            self.assertEqual(h.handoff()["open_feedback"],[])

    def test_lesson_supersession_rejects_stale_promotions(self):
        with tempfile.TemporaryDirectory() as tmp:
            h,actor=History("Fixture",tmp),{"role":"reviewer","model":"test"}
            e=h.append("review_evidence")
            first=h.lesson("old","universal",e["event_id"],actor)
            h.lesson("new","universal",e["event_id"],actor,first["lesson_id"])
            with self.assertRaises(ValueError):h.lesson("stale","universal",e["event_id"],actor,first["lesson_id"])
            self.assertEqual(len(h.lessons()),1)

    def test_history_ids_cannot_escape_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            h=History("Fixture",tmp)
            with self.assertRaises(ValueError):h.begin(approved(),{},parent="../../outside")
            with self.assertRaises(ValueError):h.feedback("../../outside","bad",{})
            e=h.append("review_evidence")
            with self.assertRaises(ValueError):h.lesson("bad","universal",e["event_id"],{},"../../outside")

    def test_malformed_edl_is_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            for invalid in ([],None):
                with self.assertRaisesRegex(ValueError,"JSON object"):
                    render_project(invalid,Path(tmp)/"out.mp4",root=tmp)


@unittest.skipUnless(os.environ.get("EDITOR_INTEGRATION") == "1", "Set EDITOR_INTEGRATION=1 for FFmpeg/Swift render tests")
class RenderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root/"source.mp4"
        subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i","color=c=navy:s=270x480:r=30:d=1.5",
                        "-f","lavfi","-i","sine=frequency=440:sample_rate=48000:duration=1.5",
                        "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac",str(self.source)],check=True)

    def render(self, **changes):
        e = approved(raw_video=str(self.source),**changes)
        return render_project(e,self.root/"out.mp4",draft=True,root=self.root,model="test")

    def test_plain_render_60fps_and_no_overwrite(self):
        result = self.render()
        self.assertEqual(result["qc"]["fps"],60)
        self.assertTrue(all(result["qc"]["checks"].values()))
        with self.assertRaises(ValueError):self.render()

    def test_speed_changes_and_whip_pan(self):
        result = self.render(segments=[{"start":0,"end":0.6,"speed":2,"transition_out":"@whip-pan"},
                                       {"start":0.7,"end":1.3,"speed":1}])
        self.assertAlmostEqual(result["qc"]["expected_duration"],0.9)

    def test_transcript_captions_and_repo_card(self):
        transcript = self.root/"words.json"
        atomic_json(transcript,{"words":[{"word":"Hello","start":0.1,"end":0.3},
                                          {"word":"editor","start":0.4,"end":0.6}]})
        result = self.render(transcript_json=str(transcript),caption_style={"shortcut":"@coral-captions"},
                             effects=[{"type":"@repo-card","start_raw":0,"end_raw":0.7,"repo":"Fixture/repo"}])
        self.assertEqual(result["qc"]["caption_events"],2)

    def test_missing_source_audio_gets_silence(self):
        silent=self.root/"silent.mp4"
        subprocess.run(["ffmpeg","-v","error","-i",str(self.source),"-an","-c:v","copy",str(silent)],check=True)
        self.source=silent
        self.assertTrue(self.render()["qc"]["checks"]["duration"])

    def test_inspection_proxies_respect_byte_budget_and_source_identity(self):
        from editor.inspect import inspect_video
        result=inspect_video(self.source,project="Fixture",max_mb=1,root=self.root)
        self.assertTrue(Path(result["contact_sheet"]).is_file())
        self.assertTrue(all(p["bytes"] <= 1_000_000 for p in result["proxies"]))
        self.assertIn(result["source_sha256"][:10],result["contact_sheet"])

    def test_media_overlay_and_sfx_music_mix(self):
        image=self.root/"card.png"
        subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i","color=c=red:s=100x100","-frames:v","1",str(image)],check=True)
        music=self.root/"music.wav"
        subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i","sine=frequency=220:duration=1","-ar","48000",str(music)],check=True)
        self.assertTrue(self.render(music=str(music),effects=[{"type":"@real-screenshot","src":str(image),
                            "start_raw":0.1,"end_raw":0.7,"sfx":str(music)}])["qc"]["checks"]["duration"])

    def test_behind_head_composites_alpha_foreground(self):
        matte=self.root/"foreground.mov"
        subprocess.run(["ffmpeg","-y","-v","error","-f","lavfi","-i",
                        "color=c=red@0.5:s=270x480:r=60:d=0.8,format=rgba",
                        "-c:v","qtrle","-pix_fmt","argb",str(matte)],check=True)
        result=self.render(effects=[{"type":"@text-behind-head","start_raw":0,"end_raw":0.7,
                                   "cutout_mov":str(matte),"lines":["HELLO","WORLD"]}])
        px=subprocess.check_output(["ffmpeg","-v","error","-ss","0.2","-i",result["output"],
                                    "-vf","format=rgb24,crop=1:1:230:400","-frames:v","1","-f","rawvideo","-"])
        self.assertGreater(px[0],90)
        self.assertGreater(px[2],30)

    def test_hyperframes_adapter_preserves_alpha_and_variables(self):
        from editor.core import ROOT
        if not (ROOT/"node_modules/.bin/hyperframes").exists():
            self.skipTest("npm ci required")
        scene=self.root/"scene"
        scene.mkdir()
        (scene/"index.html").write_text('''<!DOCTYPE html><html><head><script src="''' + str(ROOT/"node_modules/gsap/dist/gsap.min.js") + '''"></script></head>
<body style="margin:0;background:transparent"><div id="stage" data-composition-id="main" data-composition data-start="0" data-width="270" data-height="480" data-fps="30" data-duration="0.4" data-composition-variables='[{"id":"label","label":"Label","type":"string","default":"old"},{"id":"color","label":"Color","type":"string","default":"green"}]'>
<div id="label" style="background:red;color:white;font-size:30px;width:200px;height:100px"></div></div>
<script>const vars=window.__hyperframes.getVariables();document.querySelector('#label').textContent=vars.label;document.querySelector('#label').style.background=vars.color;
window.__timelines={main:gsap.timeline({paused:true}).fromTo('#label',{opacity:0},{opacity:1,duration:0.1})};</script></body></html>''')
        result=self.render(effects=[{"type":"@hyperframes","composition":str(scene),"variables":{"label":"new","color":"red"},"start_raw":0,"end_raw":0.4}])
        self.assertTrue(all(result["qc"]["checks"].values()))
        def pixel(x,y):
            return subprocess.check_output(["ffmpeg","-v","error","-ss","0.2","-i",result["output"],"-vf",f"format=rgb24,crop=1:1:{x}:{y}","-frames:v","1","-f","rawvideo","-"])
        red=pixel(190,80)
        self.assertGreater(red[0],150)
        blue=pixel(230,400)
        self.assertGreater(blue[2],80)
        self.assertLess(blue[0],30)


if __name__ == "__main__":
    unittest.main()
