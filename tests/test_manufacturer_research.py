import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
import manufacturer_research as m
XML=b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://bigassfans.com/research/airflow-study/</loc></url><url><loc>https://bigassfans.com/shop/</loc></url></urlset>'
class ManufacturerTests(unittest.TestCase):
    def test_urls(self):
        self.assertEqual(len(m.urls(XML)),2)
    def test_candidate(self):
        self.assertTrue(m.candidate("https://bigassfans.com/research/airflow-study/"))
        self.assertFalse(m.candidate("https://bigassfans.com/shop/"))
    def test_discovery(self):
        src=[{"name":"Big Ass Fans","url":"https://bigassfans.com/"}]
        found,errors=m.discover(src,lambda url:XML)
        self.assertEqual(len(found[0]["candidate_urls"]),1)
        self.assertEqual(errors,[])
    def test_direct_sources_survive_sitemap_failure(self):
        def unavailable(url):
            raise OSError("sitemap unavailable")
        source=[{"name":"VividAir","url":"https://vividairmovement.com/",
                 "direct_source_urls":["https://vividairmovement.com/product/taz/",
                                       "https://example.com/unsafe/"]}]
        found,errors=m.discover(source,unavailable)
        self.assertEqual(found[0]["candidate_urls"],["https://vividairmovement.com/product/taz/"])
        self.assertEqual(len(errors),1)
        self.assertEqual(found[0]["sitemap_status"],"incomplete")
        self.assertEqual(found[0]["candidate_status"],"unverified_candidates_available")
    def test_failed_sitemap_without_seeds_does_not_claim_coverage(self):
        def unavailable(url):raise ValueError("Sitemap too large")
        found,errors=m.discover([{"name":"Missing","url":"https://example.org/"}],unavailable)
        self.assertEqual(found[0]["candidate_status"],"no_candidates")
        self.assertEqual(found[0]["sitemap_status"],"incomplete")
        self.assertEqual(len(errors),1)
    def test_direct_source_deduped_with_sitemap(self):
        source=[{"name":"VividAir","url":"https://vividairmovement.com/",
                 "direct_source_urls":["https://vividairmovement.com/product/taz/"]}]
        xml=b'<urlset><url><loc>https://vividairmovement.com/product/taz/</loc></url></urlset>'
        found,_=m.discover(source,lambda url:xml)
        self.assertEqual(found[0]["candidate_urls"],["https://vividairmovement.com/product/taz/"])
    def test_external_domain_rejected(self):
        xml=b'<urlset><url><loc>https://example.com/research/study</loc></url></urlset>'
        found,_=m.discover([{"name":"BAF","url":"https://bigassfans.com/"}],lambda url:xml)
        self.assertEqual(found[0]["candidate_urls"],[])
if __name__=="__main__":unittest.main()
