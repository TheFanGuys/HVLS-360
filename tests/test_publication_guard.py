import hashlib
import json
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
from publication_guard import audit
class GuardTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
  self.root=pathlib.Path(self.t.name)
  for d in ("articles","editorial/drafts","editorial/approvals"):(self.root/d).mkdir(parents=True)
  self.slug="sample-article"
  self.body='---\npublication_allowed: false\nstatus: "EDITORIAL DRAFT — NOT APPROVED"\n---\n# Sample\n'
  self.draft=self.root/"editorial"/"drafts"/(self.slug+".md")
  self.published=self.root/"articles"/(self.slug+".md")
  self.approval=self.root/"editorial"/"approvals"/(self.slug+".json")
  self.draft.write_text(self.body)
  self.published.write_text(self.body.replace("publication_allowed: false","publication_allowed: true").replace("EDITORIAL DRAFT — NOT APPROVED","APPROVED FOR PUBLICATION"))
  self.record={"schema_version":1,"slug":self.slug,"publisher_decision":"approved",
    "technical_review":"complete","editorial_review":"complete","media_rights":"cleared",
    "publisher_attestation":"I explicitly authorize publication of this article.",
    "publisher_name":"Publisher","approved_at_utc":"2026-11-10T00:00:00Z",
    "source_review_notes":"Source reviewed","media_rights_evidence":"Licensed original image",
    "article_sha256":hashlib.sha256(self.body.encode()).hexdigest()}
 def test_empty_articles_ok(self):
  self.published.unlink();self.assertEqual(audit(self.root),[])
 def test_no_approval_blocks(self):
  self.assertTrue(audit(self.root))
 def test_valid_record_passes(self):
  self.approval.write_text(json.dumps(self.record));self.assertEqual(audit(self.root),[])
 def test_tampered_article_blocks(self):
  self.approval.write_text(json.dumps(self.record))
  self.published.write_text("tampered")
  self.assertTrue(audit(self.root))
 def test_missing_media_rights_blocks(self):
  self.record["media_rights"]="not_verified"
  self.approval.write_text(json.dumps(self.record))
  self.assertTrue(audit(self.root))
if __name__=="__main__":unittest.main()
