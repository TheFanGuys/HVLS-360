#!/usr/bin/env python3
"""Idempotent durable failure/recovery record on research Issue #93; no outreach."""
import os
from coo_issues import api


def record(repo, token, run_id, attempt, outcome, client=api, issue_number=93, controlled=False):
    if outcome not in ('failure', 'success'):
        raise ValueError('Unsupported research outcome')
    if not str(run_id).isdigit() or not str(attempt).isdigit():
        raise ValueError('Invalid Actions run identity')
    if issue_number != 93 and not controlled:
        raise ValueError('Alternate issue is for controlled fixtures only')
    marker = f'<!-- research-outcome:{run_id}:{attempt} -->'
    comments = []
    for page in range(1, 6):
        batch = client(repo, token, 'GET', f'/issues/{issue_number}/comments?per_page=100&page={page}')
        comments.extend(batch)
        if len(batch) < 100:
            break
    else:
        raise RuntimeError('Failure history exceeded bounded read; refusing duplicate write')
    if any(marker in x.get('body', '') for x in comments):
        return 'already_recorded'
    # Success is logged only when this run previously failed, documenting rerun recovery.
    prior_failure = any(f'research-outcome:{run_id}:' in x.get('body', '') and '**failure**' in x.get('body', '') for x in comments)
    if outcome == 'success' and not prior_failure:
        return 'no_recovery_to_record'
    prefix = '**CONTROLLED FAILURE/RECOVERY FIXTURE — NOT AN ACTUAL PIPELINE FAILURE.**\n\n' if controlled else ''
    body = prefix + (f'{marker}\nResearch execution **{outcome}**: '
            f'https://github.com/{repo}/actions/runs/{run_id}/attempts/{attempt}\n\n'
            'Owner: Workflow & Release Engineering Lead. Inspect failed steps and retained research artifact; '
            'preserve source-coverage warnings, repair the cause, rerun failed jobs, then verify Issue readback and public-index commit. '
            'A successful rerun does not establish complete source coverage or article approval.')
    result = client(repo, token, 'POST', f'/issues/{issue_number}/comments', {'body': body})
    saved = client(repo, token, 'GET', '/issues/comments/' + str(result['id']))
    if saved.get('body') != body:
        raise RuntimeError('Research outcome readback mismatch')
    return 'recorded'


if __name__ == '__main__':
    print(record(os.environ['GITHUB_REPOSITORY'], os.environ['GH_TOKEN'],
                 os.environ['GITHUB_RUN_ID'], os.environ['GITHUB_RUN_ATTEMPT'],
                 os.environ['RESEARCH_OUTCOME']))
