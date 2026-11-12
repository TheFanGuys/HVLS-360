import pathlib, sys, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'office'))
from research_failure import record

class ResearchFailureTests(unittest.TestCase):
    def test_failed_run_readback_and_idempotence(self):
        comments = []
        def client(repo, token, method, path, payload=None):
            if method == 'POST':
                comments.append({'id': 8, 'body': payload['body']})
                return comments[-1]
            if path == '/issues/comments/8': return comments[-1]
            return comments
        self.assertEqual(record('owner/repo', 'token', 12, 1, 'failure', client), 'recorded')
        self.assertEqual(record('owner/repo', 'token', 12, 1, 'failure', client), 'already_recorded')
        self.assertEqual(record('owner/repo', 'token', 12, 2, 'success', client), 'recorded')
        self.assertEqual(len(comments), 2)
    def test_clean_success_does_not_spam(self):
        self.assertEqual(record('owner/repo', 'token', 12, 1, 'success', lambda *a: []), 'no_recovery_to_record')
    def test_failed_readback_is_not_success(self):
        def client(repo, token, method, path, payload=None):
            if method == 'POST': return {'id': 1}
            return {} if path == '/issues/comments/1' else []
        with self.assertRaisesRegex(RuntimeError, 'readback'):
            record('owner/repo', 'token', 12, 1, 'failure', client)
