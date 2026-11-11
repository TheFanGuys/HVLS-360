import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"office"))
from publish_approved import publish
from render_release import prepare
from publication_guard import audit
from article_page import build_html,frontmatter,inline_markup,render_markdown

SLUG="test-hvls-article"
BODY='''---
title: "HVLS Fan <testing> & Efficiency"
category: "HVLS Technology"
status: "EDITORIAL DRAFT — NOT APPROVED"
publication_allowed: false
---
# HVLS Fan <testing> & Efficiency

*HVLS 360 | Source check*

A field article about **air movement**, with <script>alert("x")</script> [source](https://example.com/docs).

## What we learned

- Read the label and compare the exact model.
- Check [official specifications](https://example.com/manual).

## Sources

[1] Technical data: https://example.com/manual

### Internal research log

This administrative text must never appear on the public page.
'''

class ArticleReleaseTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root=Path(self.t.name)
        for folder in ("articles","editorial/drafts","editorial/approvals"):
            (self.root/folder).mkdir(parents=True,exist_ok=True)
        self.draft=self.root/"editorial"/"drafts"/(SLUG+".md")
        self.draft.write_text(BODY,encoding="utf-8")
        self.record={"schema_version":1,"slug":SLUG,"publisher_decision":"approved",
            "technical_review":"complete","editorial_review":"complete","media_rights":"cleared",
            "publisher_name":"Authorized publisher","approved_at_utc":"2026-11-10T00:00:00Z",
            "publisher_attestation":"I explicitly authorize publication of this article.",
            "source_review_notes":"All references reviewed","media_rights_evidence":"No third-party media used",
            "article_sha256":hashlib.sha256(BODY.encode("utf-8")).hexdigest()}
        self.approval=self.root/"editorial"/"approvals"/(SLUG+".json")
    def approve(self):
        self.approval.write_text(json.dumps(self.record),encoding="utf-8")
        publish(SLUG,self.approval,self.root)
    def test_draft_cannot_be_rendered_directly(self):
        with self.assertRaisesRegex(ValueError,"approved"):
            frontmatter(BODY)
        with self.assertRaises((ValueError,OSError)):
            prepare(SLUG,self.root)
    def test_approved_release_is_escaped_indexed_and_auditable(self):
        self.approve()
        output=prepare(SLUG,self.root)
        page=output.read_text(encoding="utf-8")
        self.assertIn("https://thefanguys.github.io/HVLS-360/articles/"+SLUG+"/",page)
        self.assertIn('property="og:type" content="article"',page)
        self.assertIn('"datePublished":"2026-11-10"',page)
        self.assertIn("&lt;script&gt;",page)
        self.assertNotIn("<script>alert",page)
        self.assertNotIn("This administrative text",page)
        self.assertIn('rel="noopener noreferrer"',page)
        self.assertIn("<li>Read the label",page)
        self.assertEqual(audit(self.root),[])
    def test_tampered_html_blocks(self):
        self.approve()
        output=prepare(SLUG,self.root)
        output.write_text("malicious page",encoding="utf-8")
        self.assertTrue(any("differs" in x for x in audit(self.root)))
    def test_orphan_html_blocks(self):
        orphan=self.root/"articles"/"orphan"/"index.html"
        orphan.parent.mkdir(parents=True)
        orphan.write_text("<p>Not authorized</p>",encoding="utf-8")
        self.assertTrue(any("orphan" in x for x in audit(self.root)))
    def test_repeated_build_does_not_overwrite(self):
        self.approve()
        prepare(SLUG,self.root)
        with self.assertRaisesRegex(ValueError,"already exists"):
            prepare(SLUG,self.root)
    def test_original_illustration_renders_with_accessible_alt(self):
        markup='![HVLS circulation compared with outdoor air](../../editorial/media/original/air-movement-vs-ventilation.svg)'
        rendered=render_markdown(markup)
        self.assertIn('<figure class="article-figure">',rendered)
        self.assertIn('alt="HVLS circulation compared with outdoor air"',rendered)
    def test_original_lift_diagram_renders_safely(self):
        markup='![Lift access planning](../../editorial/media/original/scissor-lift-access-planning.svg)'
        rendered=render_markdown(markup)
        self.assertIn('scissor-lift-access-planning.svg',rendered)
        self.assertIn('alt="Lift access planning"',rendered)
    def test_original_vfd_diagram_renders_safely(self):
        rendered=render_markdown('![VFD selection](../../editorial/media/original/vfd-compatibility-check.svg)')
        self.assertIn('vfd-compatibility-check.svg',rendered)
        self.assertIn('alt="VFD selection"',rendered)
    def test_original_gfy_vividair_diagram(self):
        rendered=render_markdown('![System identification](../../editorial/media/original/fan-system-documentation.svg)')
        self.assertIn('fan-system-documentation.svg',rendered)
        self.assertIn('alt="System identification"',rendered)
    def test_unlisted_local_diagram_is_not_embedded(self):
        rendered=render_markdown('![Unknown](../../editorial/media/original/unknown.svg)')
        self.assertNotIn('<img ',rendered)
    def test_unapproved_external_image_is_not_embedded(self):
        rendered=render_markdown('![fake](https://untrusted.example/photo.png)')
        self.assertNotIn('<img ',rendered)
    def test_illustration_alt_escapes_markup(self):
        rendered=render_markdown('![<script>alert(1)</script>](../../editorial/media/original/air-movement-vs-ventilation.svg)')
        self.assertIn('&lt;script&gt;',rendered)
        self.assertNotIn('<script>alert(1)</script>',rendered)
    def test_unsafe_link_does_not_render_active_anchor(self):
        rendered=inline_markup("[safe](https://example.com) and <img src=x>")
        self.assertIn('href="https://example.com"',rendered)
        self.assertIn("&lt;img src=x&gt;",rendered)

if __name__=="__main__":
    unittest.main()
