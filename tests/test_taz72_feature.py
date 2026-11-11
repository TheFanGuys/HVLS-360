from pathlib import Path
import json
import unittest
ROOT=Path(__file__).resolve().parents[1]
class TAZ72FeatureTests(unittest.TestCase):
 def test_source_backed_unpublished_article(self):
  article=(ROOT/"editorial/drafts/vividair-taz-72-field-guide.md").read_text()
  self.assertGreater(len(article.split()),850)
  self.assertIn("publication_allowed: false",article)
  self.assertIn("vividairmovement.com/product/taz/",article)
  self.assertIn("TAZ_Installation_and_Technical_Operations_Guide_1.2023.pdf",article)
  self.assertTrue((ROOT/"editorial/reviews/vividair-taz-72-field-guide-review.md").exists())
 def test_three_owned_photos_are_registered_without_claiming_upload(self):
  path=ROOT/"editorial/media/publisher/taz-72"
  data=json.loads((path/"media-manifest.json").read_text())
  self.assertEqual(len(data["images"]),3)
  self.assertEqual(data["binary_status"],"pending_import_from_prepared_zip")
  self.assertTrue(all(x["file"].endswith(".webp") for x in data["images"]))
  self.assertIn("Patterson",data["correction"])
if __name__=="__main__":unittest.main()
