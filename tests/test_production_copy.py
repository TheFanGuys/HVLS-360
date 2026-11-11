import sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from article_page import render_markdown, inline_markup

class ProductionCopyRendererTests(unittest.TestCase):
    def test_internal_notes_with_qualifiers_never_appear(self):
        md="# A technical report\n\nThe test is **sound**.\n\n### Internal research log (exclude from published page)\n\nPRIVATE RESEARCH NOTES"
        out=render_markdown(md)
        self.assertIn("<strong>sound</strong>",out)
        self.assertNotIn("PRIVATE RESEARCH NOTES",out)
        self.assertNotIn("Internal research log",out)

    def test_cfei_editorial_research_notes_stay_private(self):
        raw=(ROOT/"editorial"/"drafts"/"cfei-vs-cfm-per-watt-field-guide.md").read_text()
        body=raw.split("---",2)[-1]
        out=render_markdown(body)
        self.assertIn("Sources",out)
        self.assertNotIn("editorial research notes",out.lower())
        self.assertNotIn("no laboratory testing",out.lower())

    def test_abb_internal_review_notes_stay_private(self):
        raw=(ROOT/"editorial"/"drafts"/"abb-2026-ip66-vfd-field-report.md").read_text()
        out=render_markdown(raw.split("---",2)[-1])
        self.assertIn("What this changes for contractors",out)
        self.assertNotIn("Internal research log",out)
        self.assertNotIn("Final subject-matter review must",out)

    def test_ordered_lists_and_inline_emphasis(self):
        out=render_markdown("# Title\n\n*HVLS 360° | Editorial draft*\n\n1. **Exact** model\n2. *Verified* option\n\n- Safe source")
        self.assertNotIn("Editorial draft",out)
        self.assertIn("<ol>",out)
        self.assertIn("<li><strong>Exact</strong> model</li>",out)
        self.assertIn("<li><em>Verified</em> option</li>",out)
        self.assertIn("</ol>",out)
        self.assertIn("<ul>",out)

    def test_inline_markup_escapes_markup(self):
        out=inline_markup("*safe* <script>alert(1)</script>")
        self.assertIn("<em>safe</em>",out)
        self.assertNotIn("<script>",out)

if __name__=="__main__":
    unittest.main()
