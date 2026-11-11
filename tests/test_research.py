"""Deterministic offline tests for the HVLS 360 research desk."""
import datetime as dt
import pathlib
import tempfile
import unittest
from unittest import mock
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "office"))
import research

NOW = dt.datetime(2026, 11, 9, 15, 0, tzinfo=dt.timezone.utc)
RSS = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
<item><title>New HVLS drive announced</title><link>https://example.org/story</link><pubDate>Mon, 09 Nov 2026 12:00:00 GMT</pubDate></item>
<item><title>Outdated announcement</title><link>https://example.org/old</link><pubDate>Mon, 01 Jan 2024 12:00:00 GMT</pubDate></item>
</channel></rss>"""
ATOM = b"""<feed xmlns="http://www.w3.org/2005/Atom"><entry>
<title>Fan controls updated</title><link href="https://example.org/atom"/>
<updated>2026-11-09T11:00:00Z</updated>
</entry></feed>"""

class ResearchTests(unittest.TestCase):
    def test_rss_parsing(self):
        items = list(research.entries(RSS))
        self.assertEqual(items[0]["title"], "New HVLS drive announced")
        self.assertEqual(items[0]["url"], "https://example.org/story")
        self.assertEqual(len(items), 2)

    def test_atom_parsing(self):
        items = list(research.entries(ATOM))
        self.assertEqual(items[0]["url"], "https://example.org/atom")

    def test_recency(self):
        self.assertTrue(research.date_ok("Mon, 09 Nov 2026 12:00:00 GMT", NOW))
        self.assertFalse(research.date_ok("Mon, 01 Jan 2024 12:00:00 GMT", NOW))
        self.assertFalse(research.date_ok("not a date", NOW))
        self.assertFalse(research.date_ok("", NOW))

    def test_atom_recency_and_offsets(self):
        self.assertTrue(research.date_ok("2026-11-09T11:00:00Z", NOW))
        self.assertTrue(research.date_ok("2026-11-09T12:00:00-07:00", NOW))
        self.assertFalse(research.date_ok("2024-01-01T12:00:00Z", NOW))
        self.assertFalse(research.date_ok("2026-11-12T12:00:00Z", NOW))
        self.assertFalse(research.date_ok("2026-99-99T12:00:00Z", NOW))

    def test_atom_feed_survives_collection(self):
        import json
        with tempfile.TemporaryDirectory() as td:
            root=pathlib.Path(td)
            (root/"office").mkdir()
            (root/"office/sources.json").write_text(json.dumps({"departments":[{"name":"Controls","feeds":[{"name":"Atom source","url":"https://example.org/atom"}]}]}))
            with mock.patch.object(research,"ROOT",root), mock.patch.object(research,"fetch",return_value=ATOM):
                status=research.run(NOW)
            self.assertEqual(status,0)
            result=json.loads((root/"office/research-latest.json").read_text())
            self.assertEqual(result["departments"][0]["leads"][0]["url"],"https://example.org/atom")
            self.assertFalse(result["errors"])

    def test_end_to_end_with_mock_feed(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "office").mkdir()
            (root / "office" / "sources.json").write_text(
                '{"departments":[{"name":"Manufacturer Watch","feeds":[{"name":"Fixture","url":"https://example.org/feed"}]}]}',
                encoding="utf-8",
            )
            with mock.patch.object(research, "ROOT", root), mock.patch.object(research, "fetch", return_value=RSS):
                status = research.run(NOW)
            self.assertEqual(status, 0)
            report = (root / "office" / "reports" / "2026-11-09-research.md").read_text(encoding="utf-8")
            self.assertIn("New HVLS drive announced", report)
            import json
            public=json.loads((root / "office" / "research-latest.json").read_text(encoding="utf-8"))
            self.assertEqual(public["schema_version"],1)
            self.assertEqual(len(public["departments"][0]["leads"]),1)
            self.assertNotIn("Outdated announcement", report)
            self.assertIn("not verified reporting", report)

    def test_empty_feed_reports_no_candidates(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "office").mkdir()
            (root / "office" / "sources.json").write_text(
                '{"departments":[{"name":"Controls","feeds":[{"name":"Fixture","url":"https://example.org/feed"}]}]}',
                encoding="utf-8",
            )
            with mock.patch.object(research, "ROOT", root), mock.patch.object(research, "fetch", return_value=b"<rss><channel/></rss>"):
                status = research.run(NOW)
            self.assertEqual(status, 2)
            report = (root / "office" / "reports" / "2026-11-09-research.md").read_text(encoding="utf-8")
            self.assertIn("No recent candidates found", report)

if __name__ == "__main__":
    unittest.main()
