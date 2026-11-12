import copy
import importlib.util
import unittest
from pathlib import Path
import json
spec = importlib.util.spec_from_file_location('worker_contract', Path(__file__).resolve().parents[1] / 'office/worker_contract.py')
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

class WorkerContractTests(unittest.TestCase):
    def setUp(self):
        self.f = json.loads((w.ROOT / 'office/worker-acceptance/art-director/fixture.json').read_text())
        self.f['recovery_phase'] = 'failure_probe_then_review'
    def test_missing_input_routes_block_without_visual_success(self):
        self.assertEqual(w.admit(self.f)['action'], 'blocked')
        with self.assertRaises(ValueError):
            w.validate_result(self.f, dict(input_sha256=w.digest(self.f), status='completed', publication_allowed=False))
    def test_recovery_requires_revision_and_visual_evidence(self):
        prior = dict(input_sha256=w.digest(self.f), status='blocked')
        self.assertEqual(w.admit(self.f, prior)['action'], 'suppress')
        self.f['revision'] += 1
        self.f['recovery_phase'] = 'visual_review'
        self.assertEqual(w.admit(self.f, prior)['action'], 'inspect')
        result = dict(input_sha256=w.digest(self.f), status='completed', publication_allowed=False,
                      source_sha256=self.f['source_sha256'], visual_tool='controlled_test_only',
                      visual_observations='controlled test evidence, not a real image review', frame_widths=[390,768,1280])
        self.assertTrue(w.validate_result(self.f, result))
        self.assertEqual(w.admit(self.f, result)['action'], 'suppress')
        self.f['revision'] += 1
        with self.assertRaises(ValueError): w.validate_result(self.f, result)
    def test_cancel_path_and_content_cannot_expand_authority(self):
        self.f['cancelled'] = True
        self.assertEqual(w.admit(self.f)['action'], 'paused')
        self.f['cancelled'] = False
        self.f['source_path'] = '../outside.webp'
        with self.assertRaises(ValueError): w.admit(self.f)
    def test_hash_change_fails_closed(self):
        self.f['source_sha256'] = '0'*64
        self.assertEqual(w.admit(self.f)['reason'], 'source_hash_mismatch')
    def test_no_silent_publication_or_unowned_failure(self):
        with self.assertRaises(ValueError):
            w.validate_result(self.f,dict(input_sha256=w.digest(self.f), status='blocked',publication_allowed=False))
        self.f['publication_allowed'] = True
        with self.assertRaises(ValueError): w.admit(self.f)

if __name__ == '__main__': unittest.main()
