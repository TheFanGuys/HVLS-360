"""Check that the public HVLS technical library is useful, navigable and rights-safe."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[];self.cards=0;self.ids=set();self.duplicate_ids=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:self.duplicate_ids.append(attrs["id"])
            self.ids.add(attrs["id"])
        if tag=="a":self.links.append(attrs)
        if tag=="article" and "resource-card" in attrs.get("class","").split():
            self.cards+=1
class ReferenceLibraryTests(unittest.TestCase):
    def setUp(self):
        self.page=(ROOT/"resources"/"index.html").read_text(encoding="utf-8")
        self.links=Links();self.links.feed(self.page)
    def test_library_is_discoverable(self):
        home=(ROOT/"index.html").read_text(encoding="utf-8")
        self.assertIn('href="resources/"',home)
        self.assertIn('href="https://thefanguys.github.io/HVLS-360/resources/"',home)
        self.assertIn("https://thefanguys.github.io/HVLS-360/resources/",(ROOT/"sitemap.xml").read_text())
        self.assertIn('<link rel="canonical" href="https://thefanguys.github.io/HVLS-360/resources/"',self.page)
    def test_13_official_citable_sources(self):
        self.assertGreaterEqual(self.links.cards,13)
        official={"bigassfans.com","www.greenheck.com","www.ritehite.com",
          "www.invertekdrives.com","new.abb.com","www.amca.org",
          "www.ashrae.org","www.energy.gov","www.ecfr.gov"}
        external=[x for x in self.links.links if x.get("target")=="_blank"]
        self.assertEqual(len(external),self.links.cards)
        for link in external:
            self.assertIn(urlparse(link["href"]).netloc,official)
            self.assertEqual(link.get("rel"),"noopener noreferrer")
        self.assertFalse(self.links.duplicate_ids)
    def test_filter_is_static_first_and_accessible(self):
        self.assertIn('id="resource-search"',self.page)
        self.assertIn('aria-pressed="true"',self.page)
        self.assertIn("card.hidden=!match",self.page)
        self.assertIn('aria-live="polite"',self.page)
        self.assertNotIn("/editorial/drafts/",self.page)
        self.assertNotIn("permission pending",self.page.lower())
if __name__=="__main__":unittest.main()
