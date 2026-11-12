import json,pathlib,sys,tempfile,shutil,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'office'))
from prepare_release_candidate import prepare

class HeldCandidateTests(unittest.TestCase):
 def test_original_approval_retained_without_release(self):
  packet=prepare('hvls-air-movement-vs-ventilation')
  self.assertFalse(packet['publication_authorized'])
  self.assertFalse(packet['approval_record_created'])
  self.assertEqual(len(packet['release_inputs_sha256']),64)
 def test_new_brief_does_not_inherit_old_approval(self):
  with self.assertRaisesRegex(ValueError,'founder text approval'):
   prepare('fan-guarding-working-level')
 def test_reviewed_media_change_blocks_candidate(self):
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td)
   shutil.copytree(ROOT/'editorial',root/'editorial')
   ledger=json.loads((root/'editorial/launch-completion-ledger.json').read_text())
   item=next(x for x in ledger['items'] if x['slug']=='hvls-air-movement-vs-ventilation')
   (root/item['media']['asset_file']).write_bytes(b'changed')
   with self.assertRaisesRegex(ValueError,'Selected media'):
    prepare(item['slug'],root)

class RealCandidateRehearsal(unittest.TestCase):
 def test_held_candidate_through_release_and_discovery_in_temporary_fixture(self):
  from publish_approved import publish
  from render_release import prepare as render
  from public_catalog import write,check,BASE
  from publication_guard import audit
  import xml.etree.ElementTree as ET
  slug='hvls-air-movement-vs-ventilation'
  packet=prepare(slug)
  with tempfile.TemporaryDirectory() as td:
   root=pathlib.Path(td)
   shutil.copytree(ROOT/'editorial',root/'editorial')
   (root/'articles').mkdir()
   shutil.copy(ROOT/'index.html',root/'index.html')
   # Synthetic authorization exists ONLY inside this temporary directory.
   # It exercises the renderer and is never founder evidence or repository output.
   approval={
    'schema_version':1,'slug':slug,'publisher_decision':'approved',
    'technical_review':'complete','editorial_review':'complete','media_rights':'cleared',
    'publisher_name':'CONTROLLED FIXTURE — NOT CHRIS',
    'approved_at_utc':'2026-11-11T00:00:00Z',
    'publisher_attestation':'I explicitly authorize publication of this article.',
    'source_review_notes':'TEMPORARY FIXTURE ONLY; real review in held packet',
    'media_rights_evidence':'TEMPORARY FIXTURE ONLY; selected bytes in held packet',
    'article_sha256':packet['article_sha256'],
    'release_inputs_sha256':packet['release_inputs_sha256']}
   ap=root/'editorial/approvals'/(slug+'.json');ap.parent.mkdir(exist_ok=True);ap.write_text(json.dumps(approval))
   publish(slug,ap,root);page=render(slug,root);write(root)
   text=page.read_text()
   self.assertIn('rel="canonical" href="'+BASE+'articles/'+slug+'/',text)
   self.assertIn('application/ld+json',text)
   self.assertIn('"@type":"Article"',text)
   self.assertIn(packet['media']['asset_file'],text)
   self.assertEqual(ET.parse(root/'rss.xml').find('.//item/link').text,BASE+'articles/'+slug+'/')
   self.assertIn(BASE+'articles/'+slug+'/',[x.text for x in ET.parse(root/'sitemap.xml').findall('.//{*}loc')])
   self.assertEqual(audit(root),[]);self.assertEqual(check(root),[])
   self.assertNotIn('articles/vividair-taz-72-field-guide/',text)
