import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from coo_brief import build
class COOBriefTests(unittest.TestCase):
 def test_sanitized_coo_brief(self):
  d=build()
  self.assertFalse(d["publication_allowed"])
  self.assertEqual(d["schema_version"],1)
  self.assertEqual(len(d["assignments"]),7)
  self.assertEqual(d["metrics"]["published_articles"],len(list((ROOT/"articles").glob("*.md"))))
  self.assertNotIn("draft_body",json.dumps(d))
 def test_scheduled_workflow_includes_coo(self):
  workflow=(ROOT/".github/workflows/research-desk.yml").read_text()
  self.assertIn("python office/coo_brief.py",workflow)
  self.assertIn("git add office/research-latest.json office/editorial-latest.json office/media-latest.json office/coo-latest.json",workflow)
 def test_initial_snapshot_is_unpublished(self):
  data=json.loads((ROOT/"office/coo-latest.json").read_text())
  self.assertFalse(data["publication_allowed"])
  self.assertIn("snapshot",data["status"])
if __name__=="__main__":unittest.main()
