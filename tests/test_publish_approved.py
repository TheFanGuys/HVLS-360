import hashlib
import json
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
from publish_approved import publish
SLUG="sample-article"
class PublisherTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory()
  self.addCleanup(self.temp.cleanup)
  self.root=pathlib.Path(self.temp.name)
  (self.root/"editorial"/"drafts").mkdir(parents=True)
  (self.root/"editorial"/"approvals").mkdir(parents=True)
  self.body='---\npublication_allowed: false\nstatus: "EDITORIAL DRAFT — NOT APPROVED"\n---\n# Test\n'
  (self.root/"editorial"/"drafts"/(SLUG+".md")).write_text(self.body)
  self.path=self.root/"editorial"/"approvals"/(SLUG+".json")
  self.record={"schema_version":1,"slug":SLUG,"publisher_decision":"approved",
    "technical_review":"complete","editorial_review":"complete","media_rights":"cleared",
    "publisher_name":"Repository publisher","approved_at_utc":"2026-11-10T00:00:00Z",
    "publisher_attestation":"I explicitly authorize publication of this article.",
    "source_review_notes":"Reviewed source references","media_rights_evidence":"License record",
    "article_sha256":hashlib.sha256(self.body.encode()).hexdigest()}
 def test_no_approval_blocks(self):
  with self.assertRaises((ValueError,OSError)):publish(SLUG,self.path,self.root)
 def test_missing_review_blocks(self):
  self.record["media_rights"]="not_verified"
  self.path.write_text(json.dumps(self.record))
  with self.assertRaisesRegex(ValueError,"media_rights"):publish(SLUG,self.path,self.root)
 def test_changed_draft_blocks(self):
  self.path.write_text(json.dumps(self.record))
  (self.root/"editorial"/"drafts"/(SLUG+".md")).write_text(self.body+"changed")
  with self.assertRaisesRegex(ValueError,"changed after approval"):publish(SLUG,self.path,self.root)
 def test_approved_exact_draft_prepares_article(self):
  self.path.write_text(json.dumps(self.record))
  result=publish(SLUG,self.path,self.root)
  self.assertTrue(result.exists())
  self.assertIn("publication_allowed: true",result.read_text())
 def test_wrong_slug_blocks(self):
  with self.assertRaises(ValueError):publish("../other",self.path,self.root)
if __name__=="__main__":unittest.main()
