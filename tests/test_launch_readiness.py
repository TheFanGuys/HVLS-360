import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'office'))
from launch_readiness import audit

class LaunchPacketTests(unittest.TestCase):
    def test_actual_metadata_packet_is_current_and_unapproved(self):
        self.assertEqual(audit(ROOT),[])
    def test_changed_manuscript_invalidates_distribution_packet(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            shutil.copytree(ROOT/'editorial/drafts',root/'editorial/drafts')
            (root/'office').mkdir()
            for name in ['launch-package.json','editorial-queue.json']:
                shutil.copy(ROOT/'office'/name,root/'office'/name)
            package=json.loads((root/'office/launch-package.json').read_text())
            slug=package['items'][0]['slug']
            path=root/'editorial/drafts'/(slug+'.md')
            path.write_text(path.read_text()+'\nRevised after metadata review.\n')
            self.assertTrue(any('packet stale' in error for error in audit(root)))
            package['items'][0]['related_story_candidates']=['not-a-registered-draft']
            (root/'office/launch-package.json').write_text(json.dumps(package))
            self.assertTrue(any('related-story' in error for error in audit(root)))
