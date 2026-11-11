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

class SourceRepairTests(unittest.TestCase):
    def test_configured_official_path_is_used(self):
        calls=[]
        def fake(url):calls.append(url);return XML
        found,errors=m.discover([{'name':'BAF','url':'https://bigassfans.com/','sitemap_url':'https://bigassfans.com/official/index.xml'}],fake)
        self.assertEqual(calls,['https://bigassfans.com/official/index.xml'])
        self.assertFalse(errors)
        self.assertEqual(found[0]['sitemap_status'],'parsed')

    def test_unsafe_override_not_requested(self):
        calls=[]
        found,errors=m.discover([{'name':'BAF','url':'https://bigassfans.com/','sitemap_url':'https://other.example/sitemap.xml'}],lambda url:calls.append(url))
        self.assertEqual(calls,[])
        self.assertEqual(len(errors),1)
        self.assertEqual(found[0]['sitemap_status'],'incomplete')

    def test_gzip_and_limits(self):
        import gzip
        self.assertEqual(m.bounded_xml(gzip.compress(XML)),XML)
        self.assertEqual(m.bounded_xml(b'x'*1_552_694),b'x'*1_552_694)
        with self.assertRaises(ValueError):m.bounded_xml(b'x'*(m.MAX_BYTES+1))
        with self.assertRaises(ValueError):m.bounded_xml(gzip.compress(b'x'*(m.MAX_BYTES+1)))

    def test_html_is_not_reported_as_parsed_sitemap(self):
        found,errors=m.discover([{'name':'BAF','url':'https://bigassfans.com/'}],lambda url:b'<html><title>404</title></html>')
        self.assertEqual(len(errors),1)
        self.assertEqual(found[0]['sitemap_status'],'incomplete')

    def test_preferred_paths_survive_cap_and_insecure_links_excluded(self):
        links=['https://example.org/de/hvls/'+str(n) for n in range(45)]+['https://example.org/en/am/hvls/target','http://example.org/hvls/insecure']
        xml=('<urlset>'+''.join('<url><loc>'+u+'</loc></url>' for u in links)+'</urlset>').encode()
        found,errors=m.discover([{'name':'Test','url':'https://example.org/','preferred_path_prefixes':['/en/am/']}],lambda url:xml)
        self.assertFalse(errors)
        self.assertEqual(found[0]['candidate_urls'][0],'https://example.org/en/am/hvls/target')
        self.assertTrue(found[0]['candidate_limit_reached'])
        self.assertEqual(found[0]['discovered_candidate_count'],46)
        self.assertFalse(any(x.startswith('http:') for x in found[0]['candidate_urls']))

class TimeoutRetryTests(unittest.TestCase):
    def test_transient_timeout_retries_once(self):
        import io
        class Response(io.BytesIO):
            def geturl(self):return 'https://example.org/sitemap.xml'
        calls=[];waits=[]
        def opener(*args,**kwargs):
            calls.append(1)
            if len(calls)==1:raise TimeoutError('timeout')
            return Response(XML)
        self.assertEqual(m.fetch('https://example.org/sitemap.xml',opener,waits.append),XML)
        self.assertEqual(len(calls),2);self.assertEqual(waits,[1])
    def test_persistent_timeout_stops_after_two_attempts(self):
        calls=[]
        def opener(*args,**kwargs):calls.append(1);raise TimeoutError('timeout')
        with self.assertRaises(TimeoutError):m.fetch('https://example.org/sitemap.xml',opener,lambda n:None)
        self.assertEqual(len(calls),2)
    def test_http_errors_are_not_retried(self):
        from urllib.error import HTTPError
        calls=[]
        def opener(*args,**kwargs):calls.append(1);raise HTTPError('https://example.org',403,'Denied',None,None)
        with self.assertRaises(HTTPError):m.fetch('https://example.org/sitemap.xml',opener,lambda n:None)
        self.assertEqual(len(calls),1)

if __name__=="__main__":unittest.main()
