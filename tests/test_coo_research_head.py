import pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from coo_research_head import decide
class ResearchHeadTests(unittest.TestCase):
 def test_blocks_missing_original_and_assigns_followup(self):
  routing={"assignments":[{"lead_id":"a","title":"HVLS drive"},{"lead_id":"b","title":"HVLS safety"}]}
  source={"results":[{"lead_id":"a","status":"blocked_needs_original_source","blockers":["No publisher"]},{"lead_id":"b","status":"candidate_found_requires_human_verification","publisher_candidate":"https://example.com","blockers":["No author"]}]}
  out=decide(source,routing)
  self.assertEqual(out["counts"]["leads_reviewed"],2)
  self.assertEqual(out["counts"]["needs_original"],1)
  self.assertEqual(out["counts"]["needs_evidence"],1)
  self.assertTrue(all(x["editorial_handoff"].startswith("blocked") for x in out["decisions"]))
  self.assertFalse(out["publication_allowed"])
 def test_missing_audit_is_not_approved(self):
  out=decide({},{"assignments":[{"lead_id":"a","title":"HVLS"}]})
  self.assertEqual(out["decisions"][0]["decision"],"blocked_missing_source_audit")
 def test_workflow_order(self):
  wf=(ROOT/".github/workflows/research-desk.yml").read_text()
  self.assertLess(wf.index("python office/coo_source_checker.py"),wf.index("python office/coo_research_head.py"))
  self.assertIn("office/reports/coo-research-head-decisions.json",wf)
if __name__=="__main__":unittest.main()
