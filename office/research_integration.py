#!/usr/bin/env python3
"""Controlled real GitHub integration, never news; creates then closes one fixture."""
import json
import os
from pathlib import Path
from coo_issues import api, build_items, sync, verify_existing
from research_failure import record


def main():
    repo = os.environ['GITHUB_REPOSITORY']; token = os.environ['GH_TOKEN']
    run = os.environ['GITHUB_RUN_ID']
    if repo != 'TheFanGuys/HVLS-360' or not run.isdigit():
        raise ValueError('Integration restricted to authorized project')
    item = build_items([{'working_title': 'CONTROLLED FIXTURE HVLS intake — NOT NEWS',
                         'lead_url': 'https://example.org/hvls360-integration/' + run}])[0]
    item['body'] = '**CONTROLLED INTEGRATION FIXTURE — NOT NEWS OR A REPORTING ASSIGNMENT.**\n\n' + item['body']
    created = sync(repo, token, [item])
    evidence = {}
    try:
        if not created:
            verify_existing(repo, token, [item], evidence=evidence)
            number = evidence['matched_existing'][0]['number']
        else:
            number = created[0]['number']
        receipts=[{'number':number,'key':item['key']}]
        read = api(repo, token, 'GET', '/issues/' + str(number))
        if item['key'] not in read.get('body', ''):
            raise RuntimeError('Created fixture marker missing on real readback')
        if verify_existing(repo, token, [item], evidence=evidence, receipts=receipts):
            raise RuntimeError('Repeated real intake created a duplicate')
        # Explicitly labeled simulation on the fixture Issue, never #93's live status.
        failure = record(repo, token, run, '1', 'failure', issue_number=number, controlled=True)
        recovery = record(repo, token, run, '2', 'success', issue_number=number, controlled=True)
        again = record(repo, token, run, '2', 'success', issue_number=number, controlled=True)
        if again != 'already_recorded':
            raise RuntimeError('Failure reporter is not idempotent')
    finally:
        for row in created:
            api(repo, token, 'PATCH', '/issues/' + str(row['number']), {'state': 'closed', 'state_reason': 'completed'})
    closed = api(repo, token, 'GET', '/issues/' + str(number))
    if closed['state'] != 'closed' or verify_existing(repo, token, [item], receipts=receipts):
        raise RuntimeError('Closed fixture deduplication failed')
    result = {'controlled_fixture_only': True, 'issue': number, 'run_id': run,
              'new_create_readback': True, 'repeat_and_closed_deduplication': True,
              'failure_report': failure, 'recovery_report': recovery, 'repeat_recovery': again,
              'genuine_news_intake_verified': False, 'scheduled_trigger_verified': False}
    path = Path('office/reports/research-integration.json'); path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))

if __name__ == '__main__': main()
