import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class ResearchAutomationEvidence(unittest.TestCase):
 def test_source_seeds(self):
  data=json.loads((ROOT/"office/primary-sources.json").read_text())
  sources={x["name"]:x for x in data["sources"]}
  self.assertIn("VividAir",sources)
  self.assertIn("Go Fan Yourself (legacy)",sources)
  self.assertIn("https://vividairmovement.com/product/taz/",sources["VividAir"]["direct_source_urls"])
  self.assertIn("https://gofanyourself.com/products/z-tech-fan/",sources["Go Fan Yourself (legacy)"]["direct_source_urls"])
 def test_run_evidence_keeps_warnings_visible(self):
  r=json.loads((ROOT/"office/reports/research-automation-verification-2026-11-10.json").read_text())
  self.assertEqual(r["conclusion"],"success")
  self.assertEqual(r["manufacturer_discovery"]["error_count"],3)
  self.assertNotEqual(r["source_configuration"]["actual_candidate_contents"],"verified")
  self.assertIn("does not run autonomous LLM expert agents",r["limitations"][1])
if __name__=="__main__":unittest.main()
