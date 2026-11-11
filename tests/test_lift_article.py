from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class LiftArticleTests(unittest.TestCase):
 def test_unpublished_source_backed(self):
  text=(ROOT/"editorial"/"drafts"/"scissor-lift-planning-hvls-installations.md").read_text()
  self.assertIn("publication_allowed: false",text)
  self.assertIn("https://www.osha.gov/sites/default/files/publications/OSHA3842.pdf",text)
  self.assertIn("publisher_approval: \"Required\"",text)
 def test_review_exists(self):
  review=(ROOT/"editorial"/"reviews"/"scissor-lift-planning-hvls-installations-review.md").read_text()
  self.assertIn("Access-equipment specialist",review)
  self.assertIn("publisher approval pending",review)
if __name__=="__main__":unittest.main()
