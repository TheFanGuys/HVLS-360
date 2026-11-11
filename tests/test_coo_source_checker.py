import pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from coo_source_checker import audit
class SourceCheckerTests(unittest.TestCase):
 def test_resolved_candidate_is_not_claimed_verified(self):
  route={"assignments":[{"id":"lead-1-1","lead_id":"lead-1","title":"HVLS controls","source_url":"https://news.google.com/x","owner_role":"Original Source Checker"}]}
  pre={"sources":[{"lead_url":"https://news.google.com/x","preflight":{"status":"aggregator_requires_original"}}]}
  orig={"items":[{"lead_url":"https://news.google.com/x","resolution":{"status":"publisher_candidate_unverified","original_url":"https://manufacturer.example/news"}}]}
  out=audit(route,pre,orig)
  self.assertEqual(out["completed_audits"],1)
  self.assertEqual(out["verified_articles"],0)
  self.assertEqual(out["results"][0]["evidence_checks"]["original_publisher"],"candidate_only")
  self.assertFalse(out["results"][0]["editorial_release_allowed"])
 def test_unresolved_source_blocks_handoff(self):
  route={"assignments":[{"id":"a-1","lead_id":"a","title":"HVLS update","source_url":"https://news.google.com/a","owner_role":"Original Source Checker"}]}
  out=audit(route,{}, {})
  self.assertEqual(out["results"][0]["status"],"blocked_needs_original_source")
  self.assertFalse(out["publication_allowed"])
 def test_no_fake_results(self):
  self.assertEqual(audit({"assignments":[]},{},{})["completed_audits"],0)
 def test_workflow_runs_checker_and_uploads_private_report(self):
  text=(ROOT/".github/workflows/research-desk.yml").read_text()
  self.assertIn("python office/coo_source_checker.py",text)
  self.assertIn("office/reports/coo-source-audit.json",text)
  self.assertNotIn("git add office/reports/coo-source-audit.json",text)
if __name__=="__main__":unittest.main()
