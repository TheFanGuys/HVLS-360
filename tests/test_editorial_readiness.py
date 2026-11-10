import pathlib
import sys
import tempfile
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from editorial_readiness import check_article,audit

class ReadinessTests(unittest.TestCase):
 def test_missing_citation_detected(self):
  with tempfile.TemporaryDirectory() as temp:
   root=pathlib.Path(temp)
   folder=root/"editorial"/"drafts"
   folder.mkdir(parents=True)
   p=folder/"sample.md"
   p.write_text('---\ntitle: "Sample"\npublication_allowed: false\npublisher_approval: "Required"\n---\n'+'A word '*110+' [2]\n### Sources\n[1] https://example.org/\n')
   report=check_article(p,root)
   self.assertTrue(any("Unresolved source citations" in x for x in report["errors"]))
   self.assertFalse(report["ready_for_publisher"])
 def test_real_drafts_never_auto_approved(self):
  result=audit(ROOT)
  self.assertGreaterEqual(result["drafts"],6)
  self.assertEqual(result["approved_for_publication"],0)
  self.assertTrue(all(not a["ready_for_publisher"] for a in result["articles"]))
if __name__=="__main__":unittest.main()
