import json
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET

ROOT=pathlib.Path(__file__).resolve().parents[1]
DRAFTS=["hvls-air-movement-vs-ventilation","cfei-vs-cfm-per-watt-field-guide"]

class EvidencePackageTests(unittest.TestCase):
    def test_researched_drafts_are_not_live(self):
        for slug in DRAFTS:
            with self.subTest(slug=slug):
                text=(ROOT/"editorial"/"drafts"/(slug+".md")).read_text(encoding="utf-8")
                self.assertIn("publication_allowed: false",text)
                self.assertIn('status: "EDITORIAL DRAFT — NOT APPROVED"',text)
                self.assertNotIn("<!-- fake manufacturer claim",text)
                self.assertGreaterEqual(len(re.findall(r"https://",text)),3)
                self.assertEqual((ROOT/"articles"/(slug+".md")).exists(), (ROOT/"editorial"/"approvals"/(slug+".json")).exists())
                if not (ROOT/"editorial"/"approvals"/(slug+".json")).exists(): self.assertNotIn(slug,(ROOT/"sitemap.xml").read_text(encoding="utf-8"))
    def test_illustration_is_original_recorded_and_valid_svg(self):
        path=ROOT/"editorial"/"media"/"original"/"air-movement-vs-ventilation.svg"
        parsed=ET.parse(path)
        self.assertEqual(parsed.getroot().tag,"{http://www.w3.org/2000/svg}svg")
        self.assertIsNotNone(parsed.find(".//{http://www.w3.org/2000/svg}title"))
        self.assertIsNotNone(parsed.find(".//{http://www.w3.org/2000/svg}desc"))
        data=json.loads((ROOT/"editorial"/"media"/"original"/"asset-register.json").read_text())
        asset=data["assets"][0]
        self.assertEqual(asset["file"],"editorial/media/original/"+path.name)
        self.assertTrue(asset["third_party_material"] is False)
        self.assertFalse(asset["publication_allowed"])
        self.assertEqual(asset["technical_review"],"pending")
    def test_cfei_has_review_file(self):
        review=(ROOT/"editorial"/"reviews"/"cfei-vs-cfm-per-watt-field-guide-review.md").read_text()
        self.assertIn("2026-11-10",review)
        self.assertIn("DOE",review)
        self.assertIn("AMCA",review)
if __name__=="__main__":
    unittest.main()
