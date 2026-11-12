import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SLUG="greenheck-ds-series-2026-field-report"

class GreenheckEvidenceTests(unittest.TestCase):
    def test_draft_is_researched_and_unpublished(self):
        s=(ROOT/"editorial"/"drafts"/(SLUG+".md")).read_text(encoding="utf-8")
        self.assertIn("publication_allowed: false",s)
        self.assertIn('reported_event_date: "2025-12-31"',s)
        self.assertIn("209,800 cfm",s)
        self.assertIn("281,700 cfm",s)
        self.assertIn("manufacturer claims",s.lower())
        self.assertIn("https://www.greenheck.com/",s)
        self.assertIn("https://www.ecfr.gov/",s)
        self.assertIn("Model DS #487917 IOM",s)
        self.assertIn("Model DS #483568 IOM",s)
        self.assertIn("Shipped prior to 1/1/26",s)
        self.assertIn("DS-QD",s)
        self.assertEqual((ROOT/"articles"/(SLUG+".md")).exists(), (ROOT/"editorial"/"approvals"/(SLUG+".json")).exists())
        if not (ROOT/"editorial"/"approvals"/(SLUG+".json")).exists(): self.assertFalse((ROOT/"articles"/SLUG/"index.html").exists())

    def test_rights_not_cleared(self):
        reg=json.loads((ROOT/"editorial"/"media"/"greenheck-ds-series-2026-candidates.json").read_text())
        self.assertEqual(reg["status"],"authentic_source_candidates_rights_not_cleared")
        self.assertGreaterEqual(len(reg["candidates"]),2)
        for item in reg["candidates"]:
            self.assertEqual(item["license"],"not_verified")
            self.assertFalse(item["publication_allowed"])
            self.assertIsNone(item["image_url"])

    def test_technical_and_editorial_review_remain_open(self):
        text=(ROOT/"editorial"/"reviews"/(SLUG+"-review.md")).read_text()
        self.assertIn("Technical, copy and publisher approval pending",text)
        self.assertIn("Greenheck",text)

if __name__=="__main__":
    unittest.main()
