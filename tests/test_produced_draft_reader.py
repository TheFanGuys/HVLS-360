"""Exercise actual browser module with deterministic repository transport."""
import subprocess
import unittest
from pathlib import Path
class ProducedDraftReader(unittest.TestCase):
    def test_saved_revision_and_failure_contract(self):
        root=Path(__file__).resolve().parents[1]
        result=subprocess.run(['node','tests/test_produced_draft_reader.cjs'],cwd=root,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
