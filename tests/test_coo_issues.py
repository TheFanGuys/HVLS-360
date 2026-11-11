import pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from coo_issues import build_items,sync
class SharedIssuesTests(unittest.TestCase):
 def test_relevant_only_and_stable_id(self):
  leads=[{"id":"lead-001","working_title":"HVLS fan VFD controls","lead_url":"https://example.org/a"},
         {"id":"lead-002","working_title":"Unrelated finance headline","lead_url":"https://example.org/b"}]
  out=build_items(leads)
  self.assertEqual(len(out),1)
  self.assertTrue(out[0]["key"].startswith("lead-"))
  self.assertIn("unverified",out[0]["body"])
  self.assertIn("does **not** authorize",out[0]["body"])
  self.assertEqual(out,build_items(leads))
 def test_existing_issues_are_not_duplicated(self):
  item=build_items([{"working_title":"HVLS fans","lead_url":"https://example.org/a"}])[0]
  calls=[]
  def client(repo,token,method,path,payload=None):
   calls.append((method,path))
   return [{"body":"COO intake marker: `"+item["key"]+"`"}] if method=="GET" else {"number":1,"html_url":"https://example.org/1"}
  self.assertEqual(sync("owner/repo","token",[item],client),[])
  self.assertEqual([x[0] for x in calls],["GET"])
 def test_creates_one_issue_when_new(self):
  item=build_items([{"working_title":"HVLS fans","lead_url":"https://example.org/a"}])[0]
  def client(repo,token,method,path,payload=None):
   return [] if method=="GET" else {"number":5,"html_url":"https://example.org/5"}
  self.assertEqual(sync("owner/repo","token",[item],client)[0]["number"],5)
 def test_workflow_and_dashboard(self):
  wf=(ROOT/".github/workflows/research-desk.yml").read_text()
  page=(ROOT/"office/coo-operations.html").read_text()
  self.assertIn("issues: write",wf)
  self.assertIn("python office/coo_issues.py",wf)
  self.assertIn("Shared Managing Editor assignments",page)
if __name__=="__main__":unittest.main()
