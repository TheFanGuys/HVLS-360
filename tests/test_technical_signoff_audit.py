import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from technical_signoff_audit import audit
class SignoffAuditTests(unittest.TestCase):
 def test_all_drafts_have_review_records(self):
  result=audit()
  self.assertEqual(result["errors"],[])
  self.assertEqual(result["articles"],8)
  self.assertEqual(result["technical_signoffs"],0)
 def test_fake_completed_review_fails_closed(self):
  data=json.loads((ROOT/"editorial/reviews/technical-review-register.json").read_text())
  data["records"][0]["technical_status"]="complete"
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)
   (root/"editorial/reviews").mkdir(parents=True)
   (root/"editorial/drafts").mkdir(parents=True)
   for record in data["records"]:
    (root/record["primary_review_file"]).touch()
    (root/"editorial/drafts"/(record["slug"]+".md")).touch()
   (root/"editorial/reviews/technical-review-register.json").write_text(json.dumps(data))
   self.assertTrue(any("unsubstantiated" in x for x in audit(root)["errors"]))
if __name__=="__main__":unittest.main()
