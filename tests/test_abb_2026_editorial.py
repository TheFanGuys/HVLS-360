import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SLUG="abb-2026-ip66-vfd-field-report"

class ABBNewsroomTests(unittest.TestCase):
    def test_story_is_source_backed_and_unpublished(self):
        article=(ROOT/"editorial"/"drafts"/(SLUG+".md")).read_text(encoding="utf-8")
        self.assertIn("publication_allowed: false",article)
        self.assertIn("2026-05-27",article)
        self.assertIn("2026-09-29",article)
        self.assertIn("5.5 to 22 kW",article)
        self.assertIn("OEM",article)
        self.assertIn("https://new.abb.com/news/detail/136092/",article)
        self.assertIn("https://new.abb.com/news/detail/133088/",article)
        self.assertFalse((ROOT/"articles"/(SLUG+".md")).exists())
        self.assertNotIn(SLUG,(ROOT/"sitemap.xml").read_text(encoding="utf-8"))
    def test_official_media_links_hold_rights(self):
        path=ROOT/"editorial"/"media"/"abb-2026-vfd-candidates.json"
        data=json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["status"],"authentic_source_candidates_rights_not_cleared")
        self.assertGreaterEqual(len(data["candidates"]),2)
        for asset in data["candidates"]:
            self.assertTrue(asset["original_page"].startswith("https://new.abb.com/"))
            self.assertEqual(asset["license"],"not_verified")
            self.assertFalse(asset["publication_allowed"])
            self.assertIsNone(asset["image_url"])
    def test_specialist_queue_exists(self):
        text=(ROOT/"editorial"/"reviews"/(SLUG+"-review.md")).read_text(encoding="utf-8")
        self.assertIn("ABB leaflet",text)
        self.assertIn("Qualified drive engineer",text)
if __name__=="__main__":
    unittest.main()
