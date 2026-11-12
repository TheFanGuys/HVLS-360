"""Protect composition choices across preview and release renderers."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'office'))
from article_page import article_hero,image_presentation,insert_context_images,context_images,render_markdown
class ImageFraming(unittest.TestCase):
 def test_selected_leads_preserve_the_complete_frame_in_both_renderers(self):
  for slug,m in json.loads((ROOT/'editorial/media/article-images.json').read_text())['items'].items():
   with self.subTest(slug=slug):
    self.assertEqual(m['presentation']['lead']['fit'],'contain')
    self.assertIn(image_presentation(m,'lead'),article_hero(ROOT,slug))
    if (ROOT/'office/preview'/f'{slug}.html').exists():  # office previews cover the launch edition
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

 def test_taz_second_image_survives_snapshot_and_matches_exact_source(self):
  import hashlib
  slug='vividair-taz-72-field-guide';images=context_images(ROOT,slug)
  self.assertEqual(len(images),1)
  for m in images:self.assertEqual(hashlib.sha256((ROOT/m['file']).read_bytes()).hexdigest(),m['sha256'])
  snapshot=(ROOT/'office/preview'/f'{slug}.html').read_text()
  self.assertEqual(snapshot.count('class="article-context"'),1)
  self.assertLess(snapshot.index('The two Big Fan Guys installation photos'),snapshot.index('class="article-context"'))
  self.assertIn('object-fit:contain;width:100%;height:auto',snapshot)
  self.assertIn('id="contextMedia"',snapshot)
 def test_missing_context_anchor_fails_instead_of_hiding_second_photo(self):
  with self.assertRaises(ValueError):insert_context_images('<p>Changed manuscript</p>',context_images(ROOT,'vividair-taz-72-field-guide'))
 def test_context_paths_cannot_escape_authorized_media(self):
  media=dict(context_images(ROOT,'vividair-taz-72-field-guide')[0]);media['file']='editorial/media/publisher/../secret.webp'
  with self.assertRaises(ValueError):insert_context_images('<p>The two Big Fan Guys installation photos</p>',[media])
