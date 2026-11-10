from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
DRAFT=ROOT/"editorial"/"drafts"/"cfei-vs-cfm-per-watt-field-guide.md"
REVIEW=ROOT/"editorial"/"reviews"/"cfei-vs-cfm-per-watt-field-guide-review.md"

class CFEIPrimarySourceTests(unittest.TestCase):
    def test_primary_thresholds_and_sources(self):
        text=DRAFT.read_text(encoding="utf-8")
        self.assertIn("publication_allowed: false", text)
        self.assertIn("**at least 1.00 at high speed**", text)
        self.assertIn("**at least 1.31 at 40% speed**", text)
        self.assertIn("10 CFR 430.32(s)(2)(ii)", text)
        self.assertIn("Appendix U", text)
        self.assertIn("https://www.ecfr.gov/current/", text)
    def test_review_records_pending_engineering_and_publisher(self):
        review=REVIEW.read_text(encoding="utf-8")
        self.assertIn("eCFR 10 CFR", review)
        self.assertIn("Qualified technical reviewer", review)
        self.assertIn("Publisher explicitly approves", review)

if __name__=="__main__":
    unittest.main()
