"""Exercise publisher approval -> artifact -> HTML -> tamper detection without publishing."""
import hashlib
import json
import pathlib
import sys
import tempfile
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from publish_approved import publish
from render_release import prepare
from publication_guard import audit

class ReleaseWorkflowE2ETests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory()
  self.addCleanup(self.temp.cleanup)
  self.root=pathlib.Path(self.temp.name)
  self.slug="sample-release"
  for folder in ("editorial/drafts","editorial/approvals","articles"):
   (self.root/folder).mkdir(parents=True,exist_ok=True)
  self.body='---\ntitle: "Safe test feature"\ncategory: "Field Intelligence"\npublication_allowed: false\nstatus: "EDITORIAL DRAFT — NOT APPROVED"\n---\n# Safe test feature\n\nThis is a test article, not a real publication.\n\n### Sources\n\n[1] Example: https://example.org/\n'
  self.draft=self.root/"editorial/drafts"/(self.slug+".md")
  self.draft.write_text(self.body,encoding="utf-8")
  self.approval=self.root/"editorial/approvals"/(self.slug+".json")
  self.record={"schema_version":1,"slug":self.slug,"publisher_decision":"approved","technical_review":"complete","editorial_review":"complete","media_rights":"cleared","publisher_name":"Fixture publisher","approved_at_utc":"2026-11-10T00:00:00Z","publisher_attestation":"I explicitly authorize publication of this article.","source_review_notes":"Fixture source check","media_rights_evidence":"Fixture media clearance","article_sha256":hashlib.sha256(self.body.encode()).hexdigest()}
 def authorize_fixture(self):
  self.approval.write_text(json.dumps(self.record),encoding="utf-8")
 def test_no_approval_cannot_publish(self):
  with self.assertRaises((ValueError,OSError)):
   publish(self.slug,self.approval,self.root)
  self.assertFalse((self.root/"articles"/(self.slug+".md")).exists())
 def test_full_authorized_fixture_generates_html_and_audits(self):
  self.authorize_fixture()
  article=publish(self.slug,self.approval,self.root)
  self.assertTrue(article.is_file())
  page=prepare(self.slug,self.root)
  self.assertTrue(page.is_file())
  self.assertIn("Safe test feature",page.read_text())
  self.assertEqual(audit(self.root),[])
  with self.assertRaisesRegex(ValueError,"already exists"):
   prepare(self.slug,self.root)
 def test_changed_draft_after_approval_blocks(self):
  self.authorize_fixture()
  self.draft.write_text(self.body+"post-approval change")
  with self.assertRaisesRegex(ValueError,"changed after approval"):
   publish(self.slug,self.approval,self.root)
 def test_missing_media_clearance_blocks(self):
  self.record["media_rights"]="pending"
  self.authorize_fixture()
  with self.assertRaisesRegex(ValueError,"media_rights"):
   publish(self.slug,self.approval,self.root)
 def test_tampered_html_blocks(self):
  self.authorize_fixture()
  publish(self.slug,self.approval,self.root)
  page=prepare(self.slug,self.root)
  page.write_text(page.read_text()+"<!-- altered -->")
  self.assertTrue(any("HTML differs" in x for x in audit(self.root)))
 def test_unauthorized_html_without_markdown_blocks(self):
  page=self.root/"articles"/"unauthorized"/"index.html"
  page.parent.mkdir(parents=True)
  page.write_text("<html>Not approved</html>")
  self.assertTrue(any("orphan article HTML" in x for x in audit(self.root)))
 def test_draft_edit_after_release_blocks(self):
  self.authorize_fixture()
  publish(self.slug,self.approval,self.root)
  prepare(self.slug,self.root)
  self.draft.write_text(self.body+"edited")
  self.assertTrue(audit(self.root))
if __name__=="__main__":unittest.main()

class SelectedMediaReleaseTests(ReleaseWorkflowE2ETests):
 def setUp(self):
  super().setUp()
  from release_inputs import digest
  media=self.root/'editorial/media'
  media.mkdir()
  (media/'test.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
  (media/'article-images.json').write_text(json.dumps({'items':{self.slug:{'file':'editorial/media/test.svg','caption':'Fixture diagram','alt':'Fixture','credit':'Fixture','kind':'diagram'}}}))
  self.record['release_inputs_sha256']=digest(self.root,self.slug)
 def test_changed_image_bytes_block_release(self):
  self.authorize_fixture()
  (self.root/'editorial/media/test.svg').write_text('<svg>changed</svg>')
  with self.assertRaisesRegex(ValueError,'image bytes'):
   publish(self.slug,self.approval,self.root)
 def test_changed_caption_after_release_blocks_audit(self):
  self.authorize_fixture();publish(self.slug,self.approval,self.root);prepare(self.slug,self.root)
  p=self.root/'editorial/media/article-images.json';data=json.loads(p.read_text());data['items'][self.slug]['caption']='Unapproved caption';p.write_text(json.dumps(data))
  self.assertTrue(any('presentation changed' in x for x in audit(self.root)))
 def test_missing_image_binding_blocks(self):
  del self.record['release_inputs_sha256'];self.authorize_fixture()
  with self.assertRaisesRegex(ValueError,'image bytes'):
   publish(self.slug,self.approval,self.root)
