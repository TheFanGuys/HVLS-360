import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'office'))
from launch_content_audit import audit as launch_audit
from technical_signoff_audit import audit as technical_audit


class LaunchEvidenceTests(unittest.TestCase):
    def fixture(self, target):
        for directory in ('editorial', 'office'):
            shutil.copytree(ROOT / directory, target / directory,
                            ignore=shutil.ignore_patterns('__pycache__', 'preview'), dirs_exist_ok=True)

    def test_exact_launch_bindings(self):
        self.assertEqual(launch_audit(), [])
        result = technical_audit()
        self.assertEqual(result['errors'], [])
        self.assertGreaterEqual(result['documentary_reviews'], 12)  # launch edition; weekly articles are founder-reviewed at merge
        self.assertEqual(result['technical_signoffs'], 0)

    def test_changed_manuscript_invalidates_documentary_and_launch_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.fixture(root)
            path = root / 'editorial/drafts/hvls-air-movement-vs-ventilation.md'
            path.write_text(path.read_text() + '\nChanged technical claim.\n')
            self.assertTrue(any('stale manuscript' in e for e in technical_audit(root)['errors']))
            self.assertTrue(any('stale evidence binding' in e for e in launch_audit(root)))

    def test_required_professional_review_cannot_be_claimed_documentary_complete(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.fixture(root)
            path = root / 'editorial/reviews/LAUNCH-CLAIM-RESOLUTION-2026-11-11.json'
            report = json.loads(path.read_text())
            report['records'][0]['qualified_review_required'] = True
            path.write_text(json.dumps(report))
            self.assertTrue(any('qualified review required' in e for e in technical_audit(root)['errors']))

    def test_changed_selected_asset_invalidates_launch_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.fixture(root)
            ledger = json.loads((root / 'editorial/launch-completion-ledger.json').read_text())
            path = root / ledger['items'][0]['media']['asset_file']
            path.write_bytes(path.read_bytes() + b'changed')
            self.assertTrue(any('image: stale evidence binding' in e for e in launch_audit(root)))


if __name__ == '__main__':
    unittest.main()
