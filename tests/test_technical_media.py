import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
import technical_media as m
class Tests(unittest.TestCase):
 def test_abb_link_without_fake_image(self):
  r=m.requests("Review ABB ACH580 drive wiring")[0]
  self.assertIn("new.abb.com",r["manufacturer_link"])
  self.assertIsNone(r["image_url"])
  self.assertEqual(r["image_rights"],"not_verified")
 def test_no_unrelated_images(self):
  self.assertEqual(m.requests("HVLS destratification study"),[])
if __name__=="__main__":unittest.main()
