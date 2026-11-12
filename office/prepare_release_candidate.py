#!/usr/bin/env python3
"""Read-only exact-revision release packet. Never creates approval or public output."""
import argparse
import hashlib
import json
from pathlib import Path
from release_inputs import digest
ROOT = Path(__file__).resolve().parents[1]


def prepare(slug, root=ROOT):
    root = Path(root)
    ledger = json.loads((root/'editorial/launch-completion-ledger.json').read_text())
    item = next(x for x in ledger['items'] if x['slug'] == slug)
    article_hash = hashlib.sha256((root/item['manuscript']['file']).read_bytes()).hexdigest()
    if article_hash != item['manuscript']['sha256']:
        raise ValueError('Candidate ledger manuscript is stale')
    if item['founder_text_decision']['status'] != 'approved_exact_revision':
        raise ValueError('Candidate lacks original founder text approval')
    if item['technical']['qualified_review_required'] or item['technical']['recorded_status'] != 'documentary_review_complete':
        raise ValueError('Candidate technical evidence is unresolved')
    founder = json.loads((root/'editorial/founder-approval-register.json').read_text())
    if not any(x['slug'] == slug and x.get('founder_approved') and x['article_sha256'] == article_hash for x in founder['records']):
        raise ValueError('Exact founder approval no longer matches')
    technical = json.loads((root/'editorial/reviews/technical-review-register.json').read_text())
    row = next(x for x in technical['records'] if x['slug'] == slug)
    if row['draft_sha256'] != article_hash or row['technical_status'] != 'documentary_review_complete' or row['qualified_review_required']:
        raise ValueError('Current technical review does not clear this revision')
    selected = json.loads((root/'editorial/media/article-images.json').read_text())['items'][slug]
    media = item['media']
    if selected['file'] != media['asset_file'] or hashlib.sha256((root/media['asset_file']).read_bytes()).hexdigest() != media['asset_sha256']:
        raise ValueError('Selected media no longer matches reviewed candidate')
    if any(selected.get(k) != media.get(k) for k in ('caption', 'alt', 'presentation')):
        raise ValueError('Selected framing or caption changed after review')
    if item['voice']['manuscript_sha256'] != article_hash:
        raise ValueError('Voice pass does not match candidate')
    for part, filename in [('sources_and_claim_checks', 'review_file')]:
        source = item[part]
        if hashlib.sha256((root/source[filename]).read_bytes()).hexdigest() != source['review_sha256']:
            raise ValueError('Candidate review ledger is stale')
    return {'schema_version': 1, 'slug': slug, 'status': 'held_for_founder_release_authorization',
            'article_sha256': article_hash, 'release_inputs_sha256': digest(root, slug),
            'original_text_approval': item['founder_text_decision'],
            'documentary_review': item['technical'], 'source_review': item['sources_and_claim_checks']['review_file'],
            'voice': item['voice'], 'media': item['media'], 'metadata': item['metadata'],
            'preview': 'https://bigfanguys.com/hvls-360/office/preview/'+slug+'.html',
            'canonical_on_authorized_release': 'https://bigfanguys.com/hvls-360/articles/'+slug+'/',
            'related_links': 'No related news targets are released; omit links until a separately reviewed release adds live targets.',
            'publication_authorized': False, 'approval_record_created': False,
            'remaining_decision': 'Chris explicitly authorizes publication of this exact manuscript and selected media package. No repeated text approval required.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--slug', required=True); args = p.parse_args()
    print(json.dumps(prepare(args.slug), indent=2))
