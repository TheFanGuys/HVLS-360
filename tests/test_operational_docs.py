from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class OperationalDocsTests(unittest.TestCase):
    def test_readme_matches_live_workflows(self):
        readme=(ROOT/"README.md").read_text(encoding="utf-8")
        workflow=(ROOT/".github"/"workflows"/"research-desk.yml").read_text(encoding="utf-8")
        self.assertIn("scheduled Tuesdays and Fridays",readme)
        self.assertIn("0 15 * * 2,5",workflow)
        self.assertIn("python office/public_catalog.py --check",readme)
        self.assertIn("Publication Safety Gate",readme)

    def test_no_pretend_published_articles(self):
        readme=(ROOT/"README.md").read_text(encoding="utf-8")
        self.assertIn("none published",readme)
        self.assertIn("do not",readme.lower())
        for a in ((ROOT/"editorial"/"approvals").glob("*.json") if (ROOT/"editorial"/"approvals").exists() else []):
            self.assertTrue((ROOT/"articles"/a.stem/"index.html").exists())

if __name__=="__main__":
    unittest.main()
