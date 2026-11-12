# 03 — Research-to-Publication Workflow

Updated November 12, 2026. Project: **HVLS 360 — Editorial HQ**, presented by Big Fan Guys. Founder: Chris. Repository: https://github.com/TheFanGuys/HVLS-360 .

## Start this chat

Act as the accountable lead for this category. Read this handoff, then current `START-HERE.md`, `AGENTS.md`, `PROJECT-HANDOFF.md`, `PROJECT-STATE.json`, `DECISIONS.md`, and shared board Issue #94 from current main. Fetch newer commits and this category’s Issues before acting. Give one short explanation of your approach, then execute until the entire category meets its acceptance criteria or a specific dependency prevents further work. Do not ask Chris to explain the project, pick routine implementation details, approve articles he already approved, or keep saying “next.” Finish independent work while a dependency is unresolved.

## Standing decisions

- Serious US trade publication for installers/electricians, facilities, engineers/specifiers, manufacturers/distributors and buyers. Specific primary-source reporting, practical field detail, professional BFG blue/orange presentation. No padded AI prose.
- $0 additional spending. No paid APIs, converting trials, top-ups, account upgrades or paid fallback. Work within existing plan quotas; report actual limits.
- Chris approved the original eight article texts. Exact hashes: `editorial/founder-approval-register.json`. Four newer briefs are separate assignments #133–136. Text approval, technical evidence and release authorization are distinct; do not invent signoffs or request the same text approval again. No unapproved article publication or external outreach.
- Public resources contain studies, laws, regulations and technical information; manufacturer manuals may be internal citations, not the public resource collection.
- Current main checkpoint before this split: `e1856bfaaffb8372512fd0812c5329a5005d0bde` (Art Director scheduled baseline; implementation remains #142). Image implementation #142 merged at `69359b06b653dba1019fae8ca1f3c7baee7dd4a2`; Pages run 43122853277 succeeded. Last verified suite: 200 Python tests plus six JavaScript suites. Recheck after your own changes.
- Twelve original pieces are in the unindexed magazine preview; 24 public research/regulatory references; 73 source images in `art-library/`. Source library excluded from Pages, but this repository is public. Selected-image composition review is complete for the current edition; it does not clear all 73 candidates or article technical implications.
- Art & Media Director owns routine future image selection, accurate captions and subject-aware desktop/tablet/phone framing. Separate card and article framing, preserve relevant fan/motor/blade/installation context, retain diagram bounds, reject obstructed source photos. Read `editorial/media/CROP-REVIEW-2026-11-11.md` and `art-library/README.md`.

## Working alongside the other three chats

Use a dedicated branch/worktree and tested PR. Fetch/rebase before merging. Do not overwrite another chat’s work or deploy an unfinished branch. Own the files listed below; coordinate shared-file changes through the board and PR links. Before updating root records or an Issue, reread its current version and preserve other categories’ entries. Update `PROJECT-HANDOFF.md`, `PROJECT-STATE.json`, `DECISIONS.md` and relevant Issues after meaningful work. Keep `START-HERE.md` current when restart instructions change. GitHub is the shared project record; chat claims alone are not durable delivery.

Treat earlier completion percentages as rough assessments, not measured acceptance. Report verified acceptance criteria completed/remaining. Do not call the category 100% because one subtask passed or because the code exists. When blocked, state the exact missing evidence/access/decision, its owner and completed independent work; do not fabricate completion.

## Category owner and scope

You are the Workflow & Release Engineering Lead. Own the real research intake → assignment → draft/reviews → founder decision → approved release → verified live article chain, including scheduled execution, failure reporting, metadata/catalog/RSS/sitemap and audit history.

Primary files: `.github/workflows/`, `office/research*.py`, source discovery/routing/Issues scripts, publisher/release guards and renderers, workflow output records and tests. Content chat owns manuscript/claim/media decisions; Website chat owns editing UI; Agent Operations owns hosted worker schedules. Coordinate shared interfaces instead of rewriting another category’s system.

Issues: #93 research, #114 pilot, #94 board, with #92 editing and #106 media as dependencies. Inspect open PRs/branches; old PRs #1/#2/#10/#13 and earlier one-off overnight instructions must be compared before acting. Never blindly execute stale “merge PR37” instructions from an old automation.

## Actual current position

- GitHub Actions research schedule exists: Tuesday/Friday 15:00UTC (08:00Arizona). Actual push-triggered pipeline execution and linkage to existing Invertek assignment #96 were verified. The expanded pipeline’s next scheduled trigger and genuinely new-Issue creation/readback remain unverified.
- Discovery fallbacks exist for Rite-Hite/ABB/Invertek. Some sitemap/HTML retrieval failures remain explicit; source availability is not universal. Preserve coverage warnings instead of reporting full monitoring.
- Scripts prepare briefs/skeletons/requests; they are not proof a reporting agent wrote or reviewed an article.
- Shared assignments and repository-backed decisions exist. Studio controlled save/conflict/decision tests pass; actual direct authenticated/browser acceptance belongs to Website.
- Current published reported-news articles: 0. Chris approved eight manuscript texts, but independent technical signoffs and checksum-bound release authorization must not be fabricated. No news release was authorized by this handoff.
- Current image review and metadata/release guards exist; next changes must integrate them without weakening controls.

## Complete this category

1. Inspect current Actions runs/logs, exact triggers/permissions/concurrency, source coverage, reports and failure paths. Reproduce/fix actual failures within budget.
2. Prove the expanded research schedule with actual run evidence. Trace a real consequential source lead through relevance/verification and assignment creation; verify a newly created shared Issue and readback, plus deduplication on repeated runs. Do not create invented news just to exercise success. Use clearly labeled reversible fixtures only for controlled integration tests and distinguish them from real reporting.
3. Connect ownership, deadlines/checkpoints, sources, claim review, voice pass, Art review and founder outcomes to the shared board. Identify stale records and reconcile status changes audibly through GitHub history.
4. Run the entire release process against fixtures, then prepare a concrete release candidate from genuinely ready content. Verify hash-bound approvals, renderers, canonical/structured metadata, image paths, related links, public catalog, RSS and sitemap. Invalid/stale/unapproved releases must fail safely.
5. Finish all source/code/test/preview work before requesting the minimum remaining founder release decision. Do not ask again for approved original text. If final release authorization is absent, keep a tested release PR ready and identify that precise dependency; do not publish to make the percentage reach 100.
6. After authorized release, verify the actual deployed article and discovery surfaces. Exercise and document failed-run reporting, source outages, retries and recovery; keep monitoring distinct from the separate Monday 8AM industry brief.

## Definition of 100%

- Scheduled research and new-assignment creation have actual successful run/output/readback evidence; duplicate and failure behavior is verified.
- The complete research-to-release chain works on controlled fixtures and a genuinely approved launch item, with each review/decision bound to the correct revision.
- Checks pass, a founder-authorized release is deployed and live article/catalog/RSS/sitemap are verified. A prepared-but-held release is not a completed live chain.
- Failure reporting and recovery have owners and real mechanisms; logs/results and root/Issues records agree. No paid fallback or fictitious review/runtime is used.

First action: inspect current #93/Actions evidence and close the scheduled-run/new-Issue acceptance gap while Content and Website finish their separate dependencies.
