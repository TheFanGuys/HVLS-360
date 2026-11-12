"""Revision-bound worker admission; never supplies technical or visual approval."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def safe_path(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('input_outside_repository')
    return path

def admit(fixture, previous=None, root=ROOT):
    """A blocked unchanged input stays blocked; a successful input stays quiet."""
    key = digest(fixture)
    base = {'input_sha256': key, 'publication_allowed': False}
    if fixture.get('cancelled') or not fixture.get('enabled'):
        return dict(base, action='paused', reason='owner_paused_or_cancelled')
    if fixture.get('publication_allowed') is not False:
        raise ValueError('fixture_cannot_authorize_publication')
    if previous and previous.get('input_sha256') == key:
        if previous.get('status') in ('blocked', 'completed'):
            return dict(base, action='suppress', reason='same_input_and_outcome', prior_status=previous['status'])
    source = safe_path(root, fixture['source_path'])
    if not source.is_file():
        return dict(base, action='blocked', reason='missing_source')
    if hashlib.sha256(source.read_bytes()).hexdigest() != fixture['source_sha256']:
        return dict(base, action='blocked', reason='source_hash_mismatch')
    if fixture['recovery_phase'] == 'failure_probe_then_review':
        missing = safe_path(root, fixture['failure_probe']['path'])
        return dict(base, action='blocked', reason='acceptance_missing_input' if not missing.exists() else 'invalid_failure_fixture')
    if fixture['recovery_phase'] != 'visual_review':
        return dict(base, action='blocked', reason='unknown_phase')
    return dict(base, action='inspect', reason='fresh_visual_review_required')

def validate_result(fixture, result, root=ROOT):
    if result.get('input_sha256') != digest(fixture):
        raise ValueError('stale_worker_result')
    if result.get('publication_allowed') is not False:
        raise ValueError('worker_cannot_authorize_publication')
    if result.get('status') not in ('completed', 'blocked'):
        raise ValueError('invalid_status')
    if result['status'] == 'completed':
        if admit(fixture, root=root)['action'] != 'inspect':
            raise ValueError('input_not_ready')
        if not result.get('visual_tool') or not result.get('visual_observations'):
            raise ValueError('missing_visual_evidence')
        if set(result.get('frame_widths', [])) != {390, 768, 1280}:
            raise ValueError('missing_responsive_evidence')
        if result.get('source_sha256') != fixture['source_sha256']:
            raise ValueError('wrong_reviewed_image')
    elif not result.get('blocker') or not result.get('owner'):
        raise ValueError('unrouted_blocker')
    return True

if __name__ == '__main__':
    fixture = json.loads((ROOT / 'office/worker-acceptance/art-director/fixture.json').read_text())
    output = ROOT / fixture['output_path']
    previous = json.loads(output.read_text()) if output.exists() else None
    print(json.dumps(admit(fixture, previous), indent=2))
