"""Readback of delivered department artifacts; no autonomous editorial judgment."""
import datetime as dt
import hashlib
import json
import subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def sha(path, root=ROOT):
    p = root / path
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None

def reconcile(root=ROOT):
    ledger = json.loads((root / 'editorial/launch-completion-ledger.json').read_text())
    queue = json.loads((root / 'office/editorial-queue.json').read_text())
    queued = {x['slug']: x for x in queue['items']}
    rows = []
    for item in ledger['items']:
        manuscript = item['manuscript']
        review = item['sources_and_claim_checks']
        actual = sha(manuscript['file'], root)
        current = actual == manuscript['sha256']
        review_current = sha(review['review_file'], root) == review['review_sha256']
        image_current = sha(item['media']['asset_file'], root) == item['media']['asset_sha256']
        rows.append({'issue': item['issue'], 'slug': item['slug'], 'input_sha256': actual,
          'artifact_bindings_current': current and review_current and image_current,
          'research_to_draft_automatic_lineage_verified': False,
          'research_evidence': {'path': review['review_file'], 'sha256': sha(review['review_file'], root), 'source_urls': review['primary_source_urls'], 'recorded_checked': review['recorded_research_checked']},
          'technical': {'path': item['technical']['claim_evidence_file'], 'sha256': sha(item['technical']['claim_evidence_file'], root), 'scope': 'readback_of_Content145_documentary_review_not_new_signoff'},
          'voice': {'path': item['voice']['file'], 'revision_current': current and review_current and item['voice']['manuscript_sha256'] == actual, 'scope': 'readback_of_recorded_assistant_voice_work_not_new_edit'},
          'media': {'path': item['media']['asset_file'], 'sha256': sha(item['media']['asset_file'], root), 'bytes_current': image_current, 'fresh_visual_inspection_by_coo': False},
          'seo': {'path': item['metadata']['file'], 'sha256': sha(item['metadata']['file'], root)},
          'founder_queue': {'path': 'office/editorial-queue.json', 'present': item['slug'] in queued, 'text_decision': queued.get(item['slug'], {}).get('founder_text_decision')},
          'next_owner': 'Content/Workflow for new source-to-assignment production; Art for fresh recurring review; founder decisions remain separate',
          'publication_allowed': False})
    return {'schema_version': 1, 'observed_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
       'observer': 'Agent Operations lead assistant, active session',
       'checkpoint_kind': 'operator_readback_not_background_monitor',
       'ledger_sha256': sha('editorial/launch-completion-ledger.json', root),
       'items': rows, 'current_package_bindings': sum(r['artifact_bindings_current'] for r in rows),
       'complete_automatic_department_handoffs_verified': 0,
       'blockers': ['No demonstrated automatic research-to-finished-draft lineage; actual research96 remains separate evidence work.', 'Recurring Art acceptance fixture pending real worker output; tools/environment inheritance unverified.', 'Technical/voice/SEO are assistant-led, no recurring executor accepted as deferred by founder.', 'No independently recurring whole-newsroom COO reconciliation proven.'],
       'publication_allowed': False}

if __name__ == '__main__':
    out = reconcile()
    out['observed_main_commit'] = subprocess.check_output(['git','rev-parse','origin/main'], cwd=ROOT, text=True).strip()
    (ROOT / 'office/department-runtime.json').write_text(json.dumps(out, indent=2) + '\n')
    print(f"Read back {out['current_package_bindings']}/12 package bindings; automatic handoff acceptance remains open")
