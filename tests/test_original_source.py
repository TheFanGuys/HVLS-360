import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
import original_source as o
class SourceResolverTests(unittest.TestCase):
    def test_reject_http(self):
        self.assertFalse(o.safe("http://example.com"))
    def test_google_unresolved(self):
        x=o.original_candidate("https://news.google.com/rss/articles/123",lambda url:(url,"<html></html>"))
        self.assertEqual(x["status"],"aggregator_unresolved")
    def test_canonical(self):
        x=o.original_candidate("https://example.com/story",lambda url:(url,'<link rel="canonical" href="https://publisher.example/story">'))
        self.assertEqual(x["original_url"],"https://publisher.example/story")
        self.assertEqual(x["status"],"publisher_candidate_unverified")
    def test_no_fact_check(self):
        d={"briefs":[{"working_title":"Example","lead_url":"https://example.com/story"}]}
        result=o.resolve(d,lambda url:(url,""))
        self.assertEqual(result[0]["fact_check"],"not_performed")
if __name__=="__main__":unittest.main()
