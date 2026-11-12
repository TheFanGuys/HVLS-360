import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
spec = importlib.util.spec_from_file_location('department_runtime', Path(__file__).resolve().parents[1] / 'office/department_runtime.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

class DepartmentRuntimeTests(unittest.TestCase):
    def test_revised_manuscript_invalidates_package_without_new_approval(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            ledger = json.loads((r.ROOT / 'editorial/launch-completion-ledger.json').read_text())
            ledger['items'] = [ledger['items'][0]]
            i = ledger['items'][0]
            paths = [i['manuscript']['file'], i['sources_and_claim_checks']['review_file'],
                     i['media']['asset_file'], i['technical']['claim_evidence_file'], i['metadata']['file'],
                     'office/editorial-queue.json']
            for path in paths:
                p = root / path
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes((r.ROOT / path).read_bytes())
            (root / 'editorial/launch-completion-ledger.json').write_text(json.dumps(ledger))
            self.assertEqual(r.reconcile(root)['current_package_bindings'], 1)
            (root / i['manuscript']['file']).write_text('changed claim')
            out = r.reconcile(root)
            self.assertEqual(out['current_package_bindings'], 0)
            self.assertFalse(out['items'][0]['voice']['revision_current'])
            self.assertFalse(out['publication_allowed'])
            self.assertEqual(out['complete_automatic_department_handoffs_verified'], 0)

if __name__ == '__main__': unittest.main()
