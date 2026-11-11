from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class COOOperationsTests(unittest.TestCase):
 def test_coo_page_and_command_link(self):
  page=(ROOT/"office/coo-operations.html").read_text()
  command=(ROOT/"office/command-center.html").read_text()
  self.assertIn('href="./coo-operations.html"',command)
  for department in ("COO","Research","Editorial","Experts","Media & Art","Marketing","SEO & Distribution","Advertising & Sales","Technology","Publisher"):
   self.assertIn("'"+department+"'",page)
  for term in ("localStorage","Export COO handoff JSON","Publisher approval","browser-local"):
   self.assertIn(term,page)
  self.assertIn("coo-latest.json",page)
  self.assertNotIn("editorial/drafts/",page)
  self.assertNotIn("innerHTML",page)
if __name__=="__main__":unittest.main()
