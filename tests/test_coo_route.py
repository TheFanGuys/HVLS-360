import pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from coo_route import route
class RoutingTests(unittest.TestCase):
 def test_reject_irrelevant_and_route_relevant(self):
  result=route([{"id":"a","working_title":"Pfizer opens office"},{"id":"b","working_title":"New HVLS fan VFD controls and safety","lead_url":"https://example.org/source"}])
  self.assertEqual(len(result["rejected_leads"]),1)
  self.assertEqual(len(result["assignments"]),5)
  self.assertEqual(result["assignments"][0]["owner_role"],"Original Source Checker")
  self.assertTrue(all(t["status"]=="queued_not_executed" for t in result["assignments"]))
  self.assertFalse(result["auto_publish"])
 def test_empty_inputs_do_not_create_fake_work(self):
  self.assertEqual(route([])["assignments"],[])
 def test_pipeline_contains_private_routing(self):
  workflow=(ROOT/".github/workflows/research-desk.yml").read_text()
  self.assertIn("python office/coo_route.py",workflow)
  self.assertIn("office/reports/coo-routing-latest.json",workflow)
  self.assertNotIn("git add office/reports/coo-routing-latest.json",workflow)
 def test_named_drive_product_routes_to_experts(self):
  result=route([{"id":"a","working_title":"Optidrive E4 diagnostics update","lead_url":"https://example.org/source"}])
  self.assertEqual(len(result['assignments']),5)
  self.assertTrue(any(x['department']=='Experts' for x in result['assignments']))
if __name__=="__main__":unittest.main()
