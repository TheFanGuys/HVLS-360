import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
import article_skeletons as a
class Tests(unittest.TestCase):
 def test_no_invented_article(self):
  x=a.skeleton({"working_title":"HVLS Airflow Study","lead_url":"https://example.com/study"})
  self.assertFalse(x["ready_for_publication"])
  self.assertTrue(all(s["content"] is None for s in x["sections"]))
  self.assertTrue(all(not v for v in x["review_gates"].values()))
 def test_https_only(self):
  with self.assertRaises(ValueError):
   a.skeleton({"working_title":"Bad","lead_url":"http://example.com"})
if __name__=="__main__":unittest.main()
