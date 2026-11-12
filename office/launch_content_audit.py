"""Validate exact launch evidence bindings; never grants publication approval."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit(root=ROOT):
    root = Path(root)
    errors = []
    ledger = json.loads((root / 'editorial/launch-completion-ledger.json').read_text())
    queue = json.loads((root / 'office/editorial-queue.json').read_text())['items']
    packet = {r['slug']: r for r in json.loads((root / 'office/launch-package.json').read_text())['items']}
    images = json.loads((root / 'editorial/media/article-images.json').read_text())['items']
    approvals = {r['slug']: r for r in json.loads((root / 'editorial/founder-approval-register.json').read_text())['records']}
    technical = {r['slug']: r for r in json.loads((root / 'editorial/reviews/technical-review-register.json').read_text())['records']}
    items = ledger['items']
    slugs = [r['slug'] for r in items]
    if len(slugs) != len(set(slugs)) or set(slugs) != {r['slug'] for r in queue}:
        errors.append('Launch scope differs from queue')
    if ledger.get('release_ready') is not False:
        errors.append('Candidate ledger must retain release hold')

    def bind(path, expected, label):
        target = (root / path).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            errors.append(label + ': missing or unsafe file')
        elif hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            errors.append(label + ': stale evidence binding')

    for item in items:
        slug = item['slug']
        revision = item['manuscript']['sha256']
        bind(item['manuscript']['file'], revision, slug + ' manuscript')
        bind(item['sources_and_claim_checks']['review_file'], item['sources_and_claim_checks']['review_sha256'], slug + ' review')
        bind(item['media']['asset_file'], item['media']['asset_sha256'], slug + ' image')
        if item['voice']['manuscript_sha256'] != revision or not item['voice']['matching_revision_record_present']:
            errors.append(slug + ': missing revision-specific voice evidence')
        if packet[slug]['draft_sha256'] != revision:
            errors.append(slug + ': metadata revision mismatch')
        for key in ('seo_title', 'seo_description', 'related_story_candidates'):
            if item['metadata'][key] != packet[slug][key]:
                errors.append(slug + ': stale ' + key)
        for ledger_key, map_key in (('asset_file', 'file'), ('caption', 'caption'), ('alt', 'alt'), ('presentation', 'presentation')):
            if item['media'][ledger_key] != images[slug][map_key]:
                errors.append(slug + ': stale selected-media mapping')
        if item['technical']['recorded_status'] != technical[slug]['technical_status']:
            errors.append(slug + ': stale technical status')
        founder = item['founder_text_decision']
        if slug in approvals:
            if approvals[slug]['article_sha256'] != revision or founder['approved_sha256'] != revision:
                errors.append(slug + ': founder approval revision mismatch')
            if founder.get('request_repeat_approval') is not False:
                errors.append(slug + ': repeat approval request')
        elif founder['approved_sha256'] is not None:
            errors.append(slug + ': invented founder approval')
        if item['delivery']['release_ready'] is not False:
            errors.append(slug + ': candidate is not release authorization')
    bind(ledger['reference_library']['file'], ledger['reference_library']['sha256'], 'reference library')
    return errors


if __name__ == '__main__':
    errors = audit()
    for error in errors:
        print('LAUNCH EVIDENCE HOLD:', error)
    if errors:
        raise SystemExit(1)
    print('Launch evidence bindings verified; publication remains held.')
