"""Release index contract: no drafts or leads are discoverable; approved releases are."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "office"))
from publish_approved import publish
from render_release import prepare
from public_catalog import check, write, START, END, BASE

SLUG = "sample-approved-fan-story"
DRAFT = """---
title: "Fan Drive <Release> & Commissioning"
category: "Controls & VFDs"
status: "EDITORIAL DRAFT — NOT APPROVED"
publication_allowed: false
---
# Fan Drive Release

The test article has **measured information** and a cited manufacturer's spec.
"""

class PublicCatalogTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for folder in ("articles", "editorial/drafts", "editorial/approvals"):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        (self.root / "index.html").write_text(
            "<!doctype html><main>\n" + START + "\nplaceholder\n" + END + "\n</main>\n",
            encoding="utf-8")
        (self.root / "editorial/drafts" / (SLUG+".md")).write_text(DRAFT, encoding="utf-8")
        self.approval = self.root / "editorial/approvals" / (SLUG+".json")
        self.record = {
            "schema_version": 1, "slug": SLUG, "publisher_decision": "approved",
            "technical_review": "complete", "editorial_review": "complete",
            "media_rights": "cleared", "publisher_name": "Publisher",
            "approved_at_utc": "2026-11-10T10:00:00Z",
            "publisher_attestation": "I explicitly authorize publication of this article.",
            "source_review_notes": "Independent sources checked",
            "media_rights_evidence": "No third-party images",
            "article_sha256": hashlib.sha256(DRAFT.encode("utf-8")).hexdigest(),
        }

    def approve_and_render(self):
        self.approval.write_text(json.dumps(self.record), encoding="utf-8")
        publish(SLUG, self.approval, self.root)
        prepare(SLUG, self.root)

    def test_draft_not_discovered(self):
        write(self.root)
        home = (self.root / "index.html").read_text()
        rss = ET.parse(self.root / "rss.xml")
        site = ET.parse(self.root / "sitemap.xml")
        self.assertNotIn("Fan Drive", home)
        self.assertEqual(len(rss.findall(".//item")), 0)
        self.assertEqual(len(site.findall(".//{*}loc")), 2)
        self.assertEqual(check(self.root), [])

    def test_approved_release_in_all_three_discovery_outputs(self):
        self.approve_and_render()
        write(self.root)
        self.assertEqual(check(self.root), [])
        home = (self.root / "index.html").read_text()
        self.assertIn("Fan Drive &lt;Release&gt; &amp; Commissioning", home)
        self.assertIn("articles/"+SLUG+"/", home)
        self.assertIn('datetime="2026-11-10"', home)
        item = ET.parse(self.root/"rss.xml").find(".//item")
        self.assertEqual(item.find("link").text, BASE+"articles/"+SLUG+"/")
        self.assertEqual(item.find("title").text, "Fan Drive <Release> & Commissioning")
        self.assertEqual(len(ET.parse(self.root/"sitemap.xml").findall(".//{*}loc")), 3)

    def test_manual_spoofed_feed_item_detected(self):
        write(self.root)
        feed = self.root/"rss.xml"
        feed.write_text(feed.read_text().replace("</channel>", "<item><link>https://example.com/fake</link></item></channel>"))
        self.assertIn("rss.xml", check(self.root))

    def test_article_change_blocks_index(self):
        self.approve_and_render()
        original = self.root/"articles"/(SLUG+".md")
        original.write_text(original.read_text()+"\nUnauthorized edit.")
        with self.assertRaisesRegex(ValueError, "Release audit failed"):
            write(self.root)

    def test_unapproved_html_blocks_index(self):
        (self.root/"articles"/"unapproved"/"index.html").parent.mkdir()
        (self.root/"articles"/"unapproved"/"index.html").write_text("not approved")
        with self.assertRaisesRegex(ValueError, "orphan"):
            write(self.root)

if __name__ == "__main__":
    unittest.main()
