import pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from coo_evidence_researcher import research,Metadata
class EvidenceResearcherTests(unittest.TestCase):
 def test_extracts_metadata_as_unverified(self):
  parser=Metadata()
  parser.feed('<html><head><title>Fan Launch</title><meta property="article:published_time" content="2026-11-11"><meta name="author" content="Jane Editor"></head></html>')
  self.assertEqual(parser.title,"Fan Launch")
  self.assertEqual(parser.meta["author"],"Jane Editor")
 def test_research_executes_fetcher_and_requires_review(self):
  calls=[]
  def fake(url):
   calls.append(url)
   return {"status":"metadata_extracted_unverified","reported_author":"Jane Editor","reported_date":"2026-11-11"}
  result=research({"decisions":[{"lead_id":"x","decision":"research_followup","source_candidate":"https://publisher.example/story"},{"lead_id":"y","decision":"hold_original_source"}]},fake)
  self.assertEqual(calls,["https://publisher.example/story"])
  self.assertEqual(result["attempted"],1)
  self.assertEqual(result["results"][0]["checks"]["technical_claims"],"not_verified")
  self.assertFalse(result["results"][0]["publication_allowed"])
 def test_no_candidate_no_claims(self):
  self.assertEqual(research({"decisions":[{"decision":"research_followup"}]},lambda u:None)["attempted"],0)
 def test_workflow_includes_private_evidence(self):
  wf=(ROOT/".github/workflows/research-desk.yml").read_text()
  self.assertLess(wf.index("python office/coo_research_head.py"),wf.index("python office/coo_evidence_researcher.py"))
  self.assertIn("office/reports/coo-evidence-research.json",wf)
  self.assertNotIn("git add office/reports/coo-evidence-research.json",wf)
if __name__=="__main__":unittest.main()
