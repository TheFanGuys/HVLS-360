from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
class OneTapArticleLibraryTests(unittest.TestCase):
 def test_eight_real_drafts_available_for_one_tap_selection(self):
  html=(ROOT/"office/first-article-review.html").read_text()
  slugs=re.findall(r"\['([a-z0-9-]+)','[^']+'\]",html)
  self.assertEqual(len(slugs),8)
  for slug in slugs:
   self.assertTrue((ROOT/"editorial/drafts"/(slug+".md")).is_file(),slug)
   self.assertTrue((ROOT/"editorial/reviews"/("ai-expert-"+slug+".md")).is_file(),slug)
 def test_editor_keeps_per_article_saves_and_does_not_publish(self):
  html=(ROOT/"office/first-article-review.html").read_text()
  self.assertIn("encodeURIComponent(slug)+'.md'",html)
  self.assertIn("hvls360:publisher-draft-edit:v2:",html)
  self.assertIn("localStorage.setItem(editKey()",html)
  self.assertIn("No approval control is provided",html)
  self.assertNotIn("innerHTML",html)
if __name__=="__main__":unittest.main()
