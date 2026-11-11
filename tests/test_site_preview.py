import json,sys,tempfile,unittest,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'office'))
from site_preview import build
class PreviewTests(unittest.TestCase):
 def test_current_drafts_generate_only_unindexed_office_pages(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)
   shutil.copytree(ROOT/'editorial/drafts',root/'editorial/drafts')
   (root/'office').mkdir()
   shutil.copy(ROOT/'office/launch-package.json',root/'office/launch-package.json')
   self.assertEqual(build(root),len(json.loads((root/"office/launch-package.json").read_text())["items"])+1)
   for p in (root/'office/preview').glob('*.html'):
    self.assertEqual(p.read_text(),(ROOT/'office/preview'/p.name).read_text(),'Preview stale; rebuild')
    self.assertIn('noindex,nofollow,noarchive',p.read_text())
    self.assertIn('Founder preview',p.read_text())
    self.assertNotIn('datePublished',p.read_text())
   self.assertFalse((root/'articles').exists())
   self.assertFalse((root/'editorial/approvals').exists())
   article=(root/'office/preview/hvls-air-movement-vs-ventilation.html').read_text()
   self.assertIn('width="700" height="1110"',article)
 def test_rejects_unexpected_publishable_input(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'office').mkdir();(root/'editorial/drafts').mkdir(parents=True)
   (root/'office/launch-package.json').write_text(json.dumps({'items':[{'slug':'test'}]}))
   (root/'editorial/drafts/test.md').write_text('---\npublication_allowed: true\n---\n# Test')
   with self.assertRaises(ValueError):build(root)
