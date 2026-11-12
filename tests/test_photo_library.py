import json,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PhotoLibraryTests(unittest.TestCase):
 def test_all_collected_files_exist_and_stay_out_of_public_build(self):
  catalog=json.loads((ROOT/'art-library/catalog.json').read_text())
  self.assertGreaterEqual(len(catalog['assets']),73)
  self.assertEqual(len({a['repository_file'] for a in catalog['assets']}),len(catalog['assets']))
  for a in catalog['assets']:
   self.assertTrue((ROOT/a['repository_file']).is_file())
   if a['repository_file'].startswith(('art-library/uploads/','art-library/generated/')):
    self.assertEqual(a['source_url'],'https://github.com/TheFanGuys/HVLS-360/blob/main/'+a['repository_file'])
    self.assertTrue(a['rights_basis'])
    import hashlib
    self.assertEqual(hashlib.sha256((ROOT/a['repository_file']).read_bytes()).hexdigest(),a['sha256'])
   else:
    self.assertTrue(a['source_url'].startswith('https://bigfanguys.com/'))
  self.assertIn('- art-library',(ROOT/'_config.yml').read_text())
  self.assertNotIn('art-library/',(ROOT/'index.html').read_text())
  self.assertNotIn('art-library/',(ROOT/'sitemap.xml').read_text())
  self.assertIn('noindex,nofollow,noarchive',(ROOT/'office/photo-library.html').read_text())
 def test_new_uploads_discovered_and_existing_catalog_kept(self):
  subprocess.run(['node','-e',"""
const assert=require('node:assert/strict');require('./office/photo-library.js');
const merge=globalThis.HVLSPhotoLibrary.merge;
const rows=merge([{repository_file:'art-library/bigfanguys-com/warehouse/a.webp',description:'Known'}],[
 {type:'blob',path:'art-library/uploads/new.jpg'},
 {type:'blob',path:'art-library/bigfanguys-com/warehouse/a.webp'},
 {type:'blob',path:'art-library/uploads/raw.HEIC'},
 {type:'blob',path:'art-library/uploads/script.js'},
 {type:'blob',path:'other/private.jpg'},
 {type:'blob',path:'art-library/../bad.jpg'}]);
assert.equal(rows.length,3);assert.equal(rows[0].description,'Known');
assert.equal(rows[1].review_status,'new_upload_not_reviewed');
"""],cwd=ROOT,check=True)
