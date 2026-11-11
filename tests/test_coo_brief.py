import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from coo_brief import build
class COOBriefTests(unittest.TestCase):
 def test_manufacturer_errors_reach_public_health_counts_without_private_details(self):
  def fixture(name):
   if name=="research-latest.json":return {"errors":[{}]}
   if name=="reports/manufacturer-research-candidates.json":return {"generated_at":"2026-11-11", "errors":[{"error":"private-detail"}]*3}
   return {}
  with patch('coo_brief.load',side_effect=fixture):d=build()
  self.assertEqual(d["metrics"]["source_errors"],4)
  self.assertEqual(d["metrics"]["manufacturer_source_errors"],3)
  self.assertTrue(any('3 sitemap failures' in w for w in d["warnings"]))
  self.assertNotIn('private-detail',json.dumps(d))
 def test_missing_discovery_is_unknown_not_zero(self):
  with patch('coo_brief.load',return_value={}):d=build()
  self.assertIsNone(d["metrics"]["manufacturer_source_errors"])
  self.assertTrue(any('report unavailable' in w for w in d["warnings"]))
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
 def test_committed_brief_is_unpublished(self):
  data=json.loads((ROOT/"office/coo-latest.json").read_text())
  self.assertFalse(data["publication_allowed"])
  self.assertIn(data["status"],("initial_snapshot_from_existing_research_indices_not_a_new_run","automated_operational_brief_not_autonomous_agent"))
 def test_shared_sync_evidence_is_whitelisted(self):
  def fixture(name):
   return {"status":"synced_unverified_leads","issues_created":2,"eligible_candidates":4,"run_id":"123","deduplication_check":"created_items_rechecked_no_duplicates","private_notes":"DO-NOT-EXPORT"} if name=="reports/coo-issues-sync.json" else {}
  with patch('coo_brief.load',side_effect=fixture):d=build()
  self.assertEqual(d["shared_issue_sync"]["issues_created"],2)
  self.assertEqual(d["shared_issue_sync"]["run_id"],"123")
  self.assertNotIn("DO-NOT-EXPORT",json.dumps(d))
if __name__=="__main__":unittest.main()
