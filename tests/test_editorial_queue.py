"""Review queue must never imply publication approval or reference missing drafts."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
class EditorialQueueTests(unittest.TestCase):
 def setUp(self):
  self.page=(ROOT/"office"/"editorial-queue.html").read_text(encoding="utf-8")
  self.queue=json.loads((ROOT/"office"/"editorial-queue.json").read_text(encoding="utf-8"))
 def test_queue_contains_available_unpublished_stories(self):
  entries=self.queue["items"]
  self.assertGreaterEqual(len(entries),5)
  self.assertEqual(len({x["slug"] for x in entries}),len(entries))
  for x in entries:
   self.assertRegex(x["slug"],r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
   self.assertTrue((ROOT/x["draft"]).is_file())
   self.assertTrue((ROOT/x["review"]).is_file())
   self.assertIn("publication_allowed: false",(ROOT/x["draft"]).read_text(encoding="utf-8"))
   if x.get("media"):self.assertTrue((ROOT/x["media"]).is_file())
 def test_read_only_secure_handling(self):
  self.assertIn('noindex,nofollow,noarchive',self.page)
  self.assertIn("read-only",self.page)
  self.assertIn("separate publisher approval",self.page)
  self.assertNotIn("innerHTML",self.page)
  self.assertIn("document.createTextNode",self.page)
  self.assertIn('rel="noopener noreferrer"',self.page)
  self.assertIn('href="./editorial-queue.html"',(ROOT/"office"/"command-center.html").read_text(encoding="utf-8"))
 def test_embedded_javascript_parses(self):
  match=re.search(r"<script>([\s\S]+?)</script>",self.page)
  self.assertIsNotNone(match)
  if not shutil.which("node"):self.skipTest("Node is not installed")
  with tempfile.TemporaryDirectory() as folder:
   path=Path(folder)/"queue.js"
   path.write_text(match.group(1),encoding="utf-8")
   subprocess.run(["node","--check",str(path)],check=True,capture_output=True,text=True)
if __name__=="__main__":unittest.main()
