import pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from coo_editorial_handoff import reconcile
class EditorialHandoffTests(unittest.TestCase):
 def test_metadata_does_not_approve_story(self):
  head={"decisions":[{"lead_id":"a","title":"HVLS controls","decision":"research_followup","source_candidate":"https://example.com"}]}
  evidence={"results":[{"lead_id":"a","publisher_candidate":"https://example.com","evidence":{"status":"metadata_extracted_unverified","page_title":"Product update","reported_author":"Jane","reported_date":"2026-11-10"}}]}
  out=reconcile(head,evidence)
  self.assertEqual(out["lead_count"],1)
  self.assertEqual(out["editorial_ready"],0)
  self.assertEqual(out["items"][0]["reported_author"],"Jane")
  self.assertFalse(out["items"][0]["reported_metadata_is_verified"])
  self.assertEqual(out["items"][0]["editorial_intake"],"research_hold")
  self.assertFalse(out["publication_allowed"])
 def test_missing_source_and_evidence_are_blocked(self):
  head={"decisions":[{"lead_id":"a","decision":"hold_original_source"},{"lead_id":"b","decision":"research_followup"}]}
  out=reconcile(head,{"results":[]})
  self.assertEqual([r["research_disposition"] for r in out["items"]],["hold_find_original_publisher","hold_evidence_research_not_run"])
 def test_workflow_integration(self):
  wf=(ROOT/".github/workflows/research-desk.yml").read_text()
  self.assertLess(wf.index("python office/coo_evidence_researcher.py"),wf.index("python office/coo_editorial_handoff.py"))
  self.assertIn("office/reports/coo-managing-editor-intake.json",wf)
  self.assertNotIn("git add office/reports/coo-managing-editor-intake.json",wf)
if __name__=="__main__":unittest.main()
