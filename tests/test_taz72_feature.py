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
 def test_two_retained_photos_are_committed(self):
  path=ROOT/"editorial/media/publisher/taz-72"
  data=json.loads((path/"media-manifest.json").read_text())
  self.assertEqual(len(data["images"]),2)
  self.assertEqual(data["binary_status"],"two_files_committed_to_main")
  self.assertTrue(all(x["file"].endswith(".webp") for x in data["images"]))
  self.assertIn("Patterson",data["correction"])
  self.assertFalse(any(x["file"]=="taz-72-field-01.webp" for x in data["images"]))
  self.assertTrue(all((path/x["file"]).is_file() for x in data["images"]))
  self.assertFalse((path/"taz-72-field-01.webp").exists())
if __name__=="__main__":unittest.main()
