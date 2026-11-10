import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
import source_preflight as p
class PreflightTests(unittest.TestCase):
    def test_aggregator_not_verified(self):
        self.assertEqual(p.classify("https://news.google.com/rss/articles/abc"),"aggregator_requires_original")
        self.assertFalse(p.probe("https://news.google.com/rss/articles/abc")["reachable"])
    def test_insecure_url(self):
        self.assertEqual(p.classify("http://example.com/a"),"invalid_url")
    def test_no_claims_verified(self):
        data={"briefs":[{"working_title":"US industrial ventilation fan","lead_url":"https://news.google.com/rss/articles/a"}]}
        result=p.verify(data)
        self.assertEqual(result[0]["technical_claims"],"unverified")
        self.assertEqual(result[0]["editorial_status"],"research_required")
if __name__=="__main__":unittest.main()
