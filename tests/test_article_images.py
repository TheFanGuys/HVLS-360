import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ArticleImages(unittest.TestCase):
 def test_every_preview_article_has_captioned_lead_and_card_image(self):
  items=json.loads((ROOT/'office/launch-package.json').read_text())['items'];media=json.loads((ROOT/'editorial/media/article-images.json').read_text())['items']
  self.assertEqual(set(media),{x['slug'] for x in items})
  for slug,m in media.items():
   self.assertTrue((ROOT/m['file']).is_file());self.assertTrue(m['caption']);self.assertTrue(m['alt'])
   article=(ROOT/'office/preview'/f'{slug}.html').read_text()
   self.assertIn('class="article-lead ',article);self.assertIn('<figcaption>',article)
   self.assertIn(m['file'],article)
  self.assertIn('class="trade-header"',(ROOT/'office/preview/index.html').read_text())
 def test_field_photos_have_recorded_provenance(self):
  data=json.loads((ROOT/'editorial/media/publisher/bfg-field/provenance.json').read_text())
  self.assertEqual(len(data['photos']),3)
  for p in data['photos']:self.assertTrue(p['source'].startswith('https://bigfanguys.com/'))
