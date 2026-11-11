import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]

class MediaInventoryTests(unittest.TestCase):
 def setUp(self):
  self.path=ROOT/'editorial/media/field-photo-inventory.json'
  self.data=json.loads(self.path.read_text())
 def test_recovered_review_has_no_private_upload_identifiers_or_approval(self):
  self.assertEqual(len(self.data['assets']),15)
  self.assertEqual(len({a['id'] for a in self.data['assets']}),15)
  self.assertNotIn('libfile_',self.path.read_text())
  self.assertNotIn('/workspace/',self.path.read_text())
  self.assertFalse(self.data['publication_allowed'])
  self.assertTrue(all(a['publication_allowed'] is False for a in self.data['assets']))
 def test_rejection_and_retained_derivatives_remain_distinct(self):
  rejected=[a for a in self.data['assets'] if a['status']=='rejected']
  self.assertEqual(len(rejected),1)
  self.assertIsNone(rejected[0]['story'])
  self.assertNotIn('repository_file',rejected[0])
  retained=[a for a in self.data['assets'] if a['status']=='retained']
  self.assertEqual(len(retained),2)
  for asset in retained:self.assertTrue((ROOT/asset['repository_file']).is_file())
  manifest=json.loads((ROOT/'editorial/media/publisher/taz-72/media-manifest.json').read_text())
  for asset in manifest['images']:
   self.assertFalse(asset['publication_allowed'])
   self.assertTrue(asset['alt_text'])
   self.assertIn('no legible',asset['identity_basis'])

 def test_editorial_diagrams_are_well_formed_and_accessible(self):
  for path in (ROOT/'editorial/media/original').glob('*.svg'):
   tree=ET.parse(path);root=tree.getroot()
   self.assertEqual(root.attrib.get('role'),'img',path.name)
   self.assertTrue(root.find('{http://www.w3.org/2000/svg}title').text,path.name)
