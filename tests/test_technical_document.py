import pathlib
import sys
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"office"))
import technical_document as d
class ExtractionTests(unittest.TestCase):
    def test_excerpts_are_unverified(self):
        page='<html><head><title>HVLS Study</title><meta name="description" content="Manufacturer claims"></head><body><h1>Airflow performance research</h1><p>Measurements were conducted under test conditions at a facility.</p></body></html>'
        result=d.extract("https://example.com/research",lambda u:(page,u))
        self.assertEqual(result["status"],"extracted_unverified")
        self.assertEqual(result["metadata"]["description"],"Manufacturer claims")
        self.assertTrue(result["excerpts"])
        self.assertIn("not established facts",result["warnings"][0])
    def test_invalid_url(self):
        self.assertEqual(d.extract("http://example.com")["status"],"invalid_url")
    def test_no_claims_in_script(self):
        page="<script>Fabricated scientific result</script><p>Manufacturer testing was performed.</p>"
        result=d.extract("https://example.com",lambda u:(page,u))
        self.assertNotIn("Fabricated",str(result["excerpts"]))
if __name__=="__main__":unittest.main()
