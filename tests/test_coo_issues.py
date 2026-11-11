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
 def test_known_first_five_do_not_starve_later_candidates(self):
  items=build_items([{"working_title":"HVLS fans "+str(n),"lead_url":"https://example.org/"+str(n)} for n in range(8)])
  self.assertEqual(len(items),8)
  existing=[{"body":"COO intake marker: `"+x["key"]+"`"} for x in items[:5]]
  created=[]
  def client(repo,token,method,path,payload=None):
   if method=="GET":return existing
   created.append(payload);return {"number":len(created),"html_url":"https://example.org/issues/"+str(len(created))}
  self.assertEqual(len(sync("owner/repo","token",items,client)),3)
  self.assertTrue(all("Next checkpoint" in x["body"] for x in created))
 def test_new_issue_budget_is_applied_after_deduplication(self):
  items=build_items([{"working_title":"HVLS fans "+str(n),"lead_url":"https://example.org/"+str(n)} for n in range(9)])
  posts=[]
  def client(repo,token,method,path,payload=None):
   if method=="GET":return []
   posts.append(payload);return {"number":len(posts),"html_url":"https://example.org/issue"}
  self.assertEqual(len(sync("owner/repo","token",items,client)),5)
  self.assertEqual(len(posts),5)
 def test_saturated_history_scan_refuses_creates(self):
  calls=[]
  def client(repo,token,method,path,payload=None):
   calls.append(method);return [{"body":"existing"}]*100
  with self.assertRaisesRegex(RuntimeError,"bounded scan"):
   sync("owner/repo","token",build_items([{"working_title":"HVLS fans","lead_url":"https://example.org/a"}]),client)
  self.assertNotIn("POST",calls)
 def test_ci_without_auth_does_not_report_success(self):
  import tempfile,json,os
  from unittest.mock import patch
  import coo_issues
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td);(root/"office").mkdir();(root/"office/editorial-latest.json").write_text(json.dumps({"briefs":[]}))
   with patch.object(coo_issues,"ROOT",root),patch.dict(os.environ,{"GITHUB_ACTIONS":"true"},clear=True):
    with self.assertRaisesRegex(RuntimeError,"authenticated"):
     coo_issues.main()
if __name__=="__main__":unittest.main()
