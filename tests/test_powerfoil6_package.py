"""Guardrails for the source-backed but unapproved Powerfoil 6 review package."""
import json
import pathlib
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
SLUG="powerfoil6-field-brief"
class Powerfoil6PackageTests(unittest.TestCase):
    def setUp(self):
        self.article=(ROOT/"editorial"/"drafts"/(SLUG+".md")).read_text(encoding="utf-8")
        self.review=(ROOT/"editorial"/"reviews"/(SLUG+"-review.md")).read_text(encoding="utf-8")
        self.media=json.loads((ROOT/"editorial"/"media"/(SLUG+"-candidates.json")).read_text(encoding="utf-8"))
    def test_draft_is_not_published(self):
        self.assertIn("publication_allowed: false",self.article)
        self.assertIn('publisher_approval: "Required"',self.article)
        self.assertFalse((ROOT/"articles"/(SLUG+".md")).exists())
        self.assertFalse((ROOT/"articles"/SLUG/"index.html").exists())
    def test_product_specific_source_trace(self):
        for url in (
            "https://bigassfans.com/powerfoil-6-hvls-fan/",
            "https://bigassfans.widen.net/view/pdf/7t3u2vurlm/powerfoil6-install-guide.pdf",
        ):
            self.assertIn(url,self.article)
            self.assertIn(url,self.review)
        self.assertIn("November 19, 2025",self.article)
        self.assertIn("600 V",self.article)
        self.assertIn("600 V",self.review)
        self.assertIn("not a claim",self.article.lower())
    def test_image_rights_are_not_assumed(self):
        self.assertEqual(self.media["article"],"editorial/drafts/"+SLUG+".md")
        self.assertEqual(self.media["status"],"authentic_source_candidates_rights_not_cleared")
        self.assertGreaterEqual(len(self.media["candidates"]),2)
        for candidate in self.media["candidates"]:
            self.assertEqual(candidate["license"],"not_verified")
            self.assertIs(candidate["publication_allowed"],False)
            self.assertTrue(candidate["original_page"].startswith("https://bigassfans.com/"))
            self.assertTrue(candidate["image_url"].startswith("https://"))
    def test_video_does_not_claim_testing(self):
        script=(ROOT/"editorial"/"video"/"powerfoil6-field-review-preproduction.md").read_text(encoding="utf-8")
        self.assertIn("No test footage",script)
        self.assertIn("No fabricated",script)
if __name__=="__main__":unittest.main()
