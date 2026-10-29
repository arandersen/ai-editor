import json
from pathlib import Path
import tempfile
import unittest

from editor.core import ROOT
from editor.stockpile import catalogue, check_parameters, find_effect, instantiate


class StockpileTests(unittest.TestCase):
    def test_seventeen_reference_entries_resolve_without_duplicate_templates(self):
        data=catalogue()
        self.assertEqual(len({e["slug"] for e in data["templates"]}),len(data["templates"]))
        reference=data["reference_catalogues"][0]
        self.assertEqual(len(reference["effects"]),17)
        for e in reference["effects"]:
            self.assertEqual(find_effect(e["label"])["slug"],e["slug"])
        self.assertEqual(data["total_pack_2_and_3_templates"],31)
        self.assertEqual(data["total_templates"],38)

    def test_aliases_are_stockpile_names_not_silent_renderer_aliases(self):
        self.assertEqual(find_effect("@magazine_cover")["slug"],"cover-story")
        self.assertEqual(find_effect("pull-back reveal")["slug"],"pull-back")
        self.assertEqual(find_effect("showcase player")["slug"],"proof-player")

    def test_chart_rejects_bad_data(self):
        e=find_effect("chart-grow")
        for variables in ({"values":[1,float('nan')]},{"values":[1,2],"labels":["one"]},
                          {"values":["one",2]},{"madeUp":1}):
            with self.assertRaises(ValueError):check_parameters(e,variables)

    def test_parameter_bounds_match_browser_contract(self):
        for slug,values in [('chart-grow',{'yPercent':60}),('couch-wall',{'spread':20,'cards':['x.png'],'subjectAsset':'x.png'}),
                            ('glass-type',{'fontSize':-1}),('profile-card',{'widthPercent':1,'profileAsset':'x.png'}),
                            ('cover-story',{'subjectAsset':'x.png','masthead':''})]:
            with self.assertRaises(ValueError):check_parameters(find_effect(slug),values)

    def test_short_duration_cannot_truncate_fixed_animation(self):
        with self.assertRaisesRegex(ValueError,'duration'):
            check_parameters(find_effect('chart-grow'),{},duration=1)

    def test_zero_time_proof_entry_is_supported(self):
        values,seconds=check_parameters(find_effect('proof-player'),{'sequence':[
            {'label':'Immediate hook','src':'clip.mp4','start':0,'duration':1}]})
        self.assertEqual(values['sequence'][0]['start'],0)

    def test_media_source_type_is_validated(self):
        with self.assertRaises(ValueError):check_parameters(find_effect('proof-player'),{'sequence':[
            {'label':'Invalid','src':17,'start':0,'duration':1}]})

    def test_checklist_rejects_unsorted_or_outside_times(self):
        e=find_effect("checklist")
        for times in ([1.0,0.5,2.0],[0.1,1.0,2.0],[0.5,1.0,3.0]):
            with self.assertRaises(ValueError):check_parameters(e,{"completeTimes":times})

    def test_proof_player_requires_media_and_non_overlapping_sequence(self):
        e=find_effect("proof-player")
        with self.assertRaises(ValueError):check_parameters(e,{})
        with self.assertRaises(ValueError):check_parameters(e,{"sequence":[
            {"label":"a","src":"a.mp4","start":0.3,"duration":2},
            {"label":"b","src":"b.mp4","start":1.0,"duration":1}]})
        values,d=check_parameters(e,{"sequence":[{"label":"a","src":"a.mp4","start":0.3,"duration":5}]},duration=6)
        self.assertEqual(d,6)

    def test_missing_asset_leaves_no_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"instance"
            with self.assertRaises(ValueError):instantiate("profile-card",out,{"profileAsset":"missing.png"})
            self.assertFalse(out.exists())

    def test_instance_copies_media_and_binds_defaults_without_mutating_library(self):
        source=ROOT/"animations/_fx_library/profile-card/index.html"
        original=source.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            image=Path(tmp)/"image.svg"
            image.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect width="100" height="100" fill="red"/></svg>')
            out=Path(tmp)/"instance"
            result=instantiate("profile-card",out,{"profileAsset":str(image),"creatorHandle":"my-account"})
            variables=json.loads((out/"variables.json").read_text())
            self.assertTrue((out/variables["profileAsset"]).is_file())
            self.assertIn('my-account',(out/"index.html").read_text())
            self.assertEqual(source.read_bytes(),original)
            self.assertEqual(result["edl_effect"]["type"],"@hyperframes")
            with self.assertRaises(FileExistsError):instantiate("profile-card",out,{"profileAsset":str(image)})

    def test_cannot_write_instances_into_shared_stockpile(self):
        with self.assertRaises(ValueError):instantiate("chart-grow",ROOT/"animations/_fx_library/new-scene")

    def test_unsafe_caption_text_remains_text_not_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"chart"
            instantiate("chart-grow",out,{"title":"</script><b>not markup</b>"})
            content=(out/"index.html").read_text()
            self.assertNotIn(': {"title": "</script>',content)
            self.assertIn('not markup',content)


if __name__=="__main__":
    unittest.main()
