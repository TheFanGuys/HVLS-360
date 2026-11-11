import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ResearchShelfTests(unittest.TestCase):
 def test_unique_sources_and_public_rendering(self):
  data=json.loads((ROOT/'resources/research-index.json').read_text());rows=data['items'];page=(ROOT/'resources/index.html').read_text()
  self.assertEqual(len(rows),24);self.assertEqual(len({r['url'] for r in rows}),24)
  for r in rows:
   self.assertTrue(r['url'].startswith('https://'));self.assertIn(r['url'],page)
   self.assertIn(r['group'],['Studies & research','Laws & regulations','Standards & technical information'])
  self.assertNotIn('install-guide.pdf',page)
  self.assertIn('Research &amp; regulation desk',(ROOT/'index.html').read_text())
 def test_original_founder_approvals_stay_revision_bound(self):
  data=json.loads((ROOT/'editorial/founder-approval-register.json').read_text())
  self.assertEqual(len(data['records']),8)
  self.assertFalse(data['technical_signoff_inferred'])
  new={'industrial-fan-heat-study-what-was-measured','ceiling-fans-hvac-air-distribution-research','scissor-lift-osha-classification','fan-guarding-working-level'}
  self.assertFalse(new.intersection(r['slug'] for r in data['records']))
