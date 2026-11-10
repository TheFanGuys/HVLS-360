import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
import technical_advisory as t
CONFIG={"roles":[{"id":x,"name":x,"checks":["verify"]} for x in ["chief","methods","electrical","airflow","mechanical","automation","safety","field"]]}
class Tests(unittest.TestCase):
 def test_vfd_routes_electrical(self):
  r=t.make_review({"working_title":"ABB VFD wiring and commissioning"},CONFIG)
  self.assertIn("electrical",[x["role"] for x in r["specialists"]])
  self.assertFalse(r["engineering_claims_verified"])
 def test_no_fake_approval(self):
  r=t.make_review({"working_title":"HVLS airflow test"},CONFIG)
  self.assertFalse(r["publisher_approval"])
  self.assertTrue(all(not x["approved"] for x in r["specialists"]))
if __name__=="__main__":unittest.main()
