"""Protect composition choices across preview and release renderers."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'office'))
from article_page import article_hero,image_presentation
class ImageFraming(unittest.TestCase):
 def test_selected_leads_preserve_the_complete_frame_in_both_renderers(self):
  for slug,m in json.loads((ROOT/'editorial/media/article-images.json').read_text())['items'].items():
   with self.subTest(slug=slug):
    self.assertEqual(m['presentation']['lead']['fit'],'contain')
    self.assertIn(image_presentation(m,'lead'),article_hero(ROOT,slug))
    self.assertIn(image_presentation(m,'lead'),(ROOT/'office/preview'/f'{slug}.html').read_text())
    self.assertIn(image_presentation(m,'card'),(ROOT/'office/preview/index.html').read_text())
 def test_unreviewed_or_injected_styles_are_rejected(self):
  for spec in ({'fit':'fill','position':'50% 50%'},{'fit':'cover','position':'50%;background:red'},{'fit':'cover','position':'101% 50%'}):
   with self.assertRaises(ValueError):image_presentation({'presentation':{'card':spec}},'card')
 def test_portrait_and_diagram_cards_keep_their_full_source_frame(self):
  media=json.loads((ROOT/'editorial/media/article-images.json').read_text())['items']
  for slug,m in media.items():
   if m['kind']=='diagram' or any(name in m['file'] for name in ('fan-hub','taz-72-field','production-floor','elevated-install')):
    with self.subTest(slug=slug):self.assertEqual(m['presentation']['card']['fit'],'contain')
 def test_obscured_image_is_no_longer_selected(self):
  media=json.loads((ROOT/'editorial/media/article-images.json').read_text())['items']
  self.assertFalse(any(m['file'].endswith('industrial-install.webp') for m in media.values()))
