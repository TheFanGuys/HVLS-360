from pathlib import Path
import json
import unittest
ROOT=Path(__file__).resolve().parents[1]
class VividAirTests(unittest.TestCase):
 def test_dedicated_draft_and_review(self):
  name="vividair-gfy-ztech-taz-controls-field-guide"
  article=(ROOT/"editorial"/"drafts"/(name+".md")).read_text()
  self.assertIn("publication_allowed: false",article)
  self.assertIn("gofanyourself.com",article)
  self.assertIn("vividairmovement.com",article)
  self.assertIn("fan-system-documentation.svg",article)
  self.assertGreater(len(article.split()),850)
  self.assertTrue((ROOT/"editorial"/"reviews"/(name+"-review.md")).exists())
 def test_manufacturer_watch_sources(self):
  data=json.loads((ROOT/"editorial"/"manufacturer-watch"/"vividair-gfy.json").read_text())
  self.assertEqual(data["manufacturer"],"VividAir")
  self.assertEqual(data["legacy_brand"],"Go Fan Yourself")
  self.assertGreaterEqual(len(data["product_families"]),4)
if __name__=="__main__":unittest.main()
