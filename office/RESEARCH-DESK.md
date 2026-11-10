# HVLS 360 — Research Desk V1

## What runs
Eight topic-specific RSS/Atom feed monitors, Tuesday and Friday at **08:00 America/Phoenix** (15:00 UTC). Results are deduplicated, filtered to recent dated entries, and assembled into one COO-style editorial lead report.

## What does NOT run
No autonomous AI reasoning, manufacturer manual verification, article writing, publishing, advertising, social posts or external outreach. The feeds are discovery leads, not verified news. The existing Monday ChatGPT HVLS Industry Brief remains separate; its output is not automatically imported.

## Safety
The workflow has `contents: read` and `issues: write`. It cannot push articles or merge changes. It posts a GitHub Issue with leads for editorial review. **GitHub Issues in a public repository are public**: do not add confidential job/customer data, unpublished business plans, or private research notes. Use a private repository for confidential agent reporting.

## Activate
After publisher review and merge, enable GitHub Actions and Issues. Run `HVLS 360 Research Desk` manually once, check its run logs and resulting Issue, and then confirm scheduled operation. GitHub scheduled workflows may run late.

## Limitations
Google News RSS search feeds may be blocked, sparse or return duplicates. Date and title checks are not factual verification. Feed errors appear in the report. If there are no leads, the script exits 2; the workflow still reports the result. More reliable direct manufacturer feeds can be added after source validation.

## Editorial gate
No lead becomes an article without primary-source verification, copyediting, technical review where needed, visual media review, SEO checks, and explicit publisher approval.
