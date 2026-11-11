from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class PublisherReadingExperienceTests(unittest.TestCase):
 def test_review_studio_is_private_file_based(self):
  s=(ROOT/"office/first-article-review.html").read_text()
  self.assertIn('file.text()',s)
  self.assertNotIn('fetch(',s)
  self.assertNotIn('innerHTML',s)
  self.assertIn('figure figcaption',s)
  self.assertIn('magazine-style reading experience',s)
 def test_first_feature_source_and_artwork(self):
  article=(ROOT/"editorial/drafts/hvls-air-movement-vs-ventilation.md").read_text()
  self.assertIn("2.1 (Thermal Comfort)",article)
  self.assertIn("air-movement-vs-ventilation.svg",article)
  self.assertIn("publication_allowed: false",article)
if __name__=="__main__":unittest.main()
