from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class PublisherManualEditingTests(unittest.TestCase):
 def test_edit_save_export_restore_without_publish(self):
  html=(ROOT/"office/first-article-review.html").read_text()
  for name in ("editToggle","editorText","saveLocal","downloadEdit","restoreEdit","updateEdit(raw)","localStorage.setItem","new Blob"):
   self.assertIn(name,html)
  self.assertNotIn("fetch(",html)
  self.assertNotIn("innerHTML",html)
  self.assertIn("GitHub manuscript unchanged",html)
  self.assertIn("No approval control is provided",html)
if __name__=="__main__":unittest.main()
