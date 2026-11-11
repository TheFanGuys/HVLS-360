# Full-site acceptance — November 11, 2026

Baseline: main 834841dc4c250c162ae3dd69f5c0096bb2966cb1. This report records actual checks, not a claim of unattended editorial production.

| Area | Result | Evidence / limit |
| --- | --- | --- |
| Python suite | Passed | 190 tests, including two new preview-boundary/rebuild tests |
| JavaScript suites | Passed | All six executable suites: recovery, shared assignments, repository saves, decisions, companion packets, Studio session |
| Editorial / metadata / publication | Passed | Eight draft audit; revision-matched metadata; publication guard; approved-only catalog; Python compile |
| Local HTML links/assets | Passed | 191 references resolved; no missing local targets across public site, office and nine new preview pages |
| Live homepage | Working | Browser loaded masthead, navigation, empty release catalog, departments, references and editorial-standards link |
| Live reference search | Working | 13 references; ABB search returned one ACH580 entry; no horizontal overflow in tested desktop viewport |
| Live shared board | Working | 17 open assignments fetched from GitHub; Powerfoil search returned assignment #88; no horizontal overflow in tested viewport |
| iPhone commit/reopen | Founder confirmed | GitHub editor commit then same-iPhone Review Studio reopening; actual commits inspected in previous checkpoint |
| Direct Studio Save/conflicts | Controlled tests passed | Real Studio script tested with controlled transport. No direct authenticated physical-iPhone or second-device acceptance claimed |
| Magazine preview | Built; deploy check follows | Nine noindex office pages, eight current draft manuscripts, same publication stylesheet. No approval records, publication dates, RSS entries or public catalog changes |
| Article release | Awaiting editorial gates | No founder release authorization, qualified signoffs or approved news articles |
| Scheduled research | Partial acceptance | Actual push execution/linkage previously verified; next expanded scheduled trigger and genuine new-Issue creation/readback still open |

## Repairs in this acceptance pass

- Added a complete browsable magazine preview under `office/preview/` and linked it prominently from Command Center. Eight articles are readable without tokens, file imports or GitHub editing. One preview label identifies the unreleased workspace.
- Generator uses the existing safe Markdown renderer, current draft text and current metadata. A deterministic test detects stale generated preview pages; all previews are unindexed and excluded from public release catalog/RSS/sitemap.
- Fixed the renderer's airflow image dimensions from 1200×650 to 700×1110. Other original artwork dimensions remain unchanged.
- Replaced the reference library's known failed legacy Powerfoil PDF endpoint with the current official Powerfoil 6 support page, reopened during this pass.
- Relabeled browser-local Command Center queue as personal notes; it is not the canonical shared assignment system.

## Remaining acceptance

Direct Studio authenticated physical-device writes, real second-device reopening, expanded scheduled research/new-Issue path, revision-specific qualified technical review, and founder authorization for an article release. No paid service, external outreach, new credential or release was performed.
