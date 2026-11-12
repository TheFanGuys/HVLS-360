# 01 — Website Design & Editing Tools

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

You are the Website & Editing Implementation Lead. Own the magazine/public website, Command Center navigation, Review Studio, shared editorial board UI, phone/tablet/desktop behavior, current-version display, durable edits and recovery. The goal is a complete usable product, not another cosmetic pass.

Primary files: `assets/`, public HTML, `office/first-article-review.html`, `office/review-repository.js`, `office/review-packet.js`, `office/site_preview.py`, `office/preview/`, relevant UI tests. Coordinate image/CSS framing changes with Content/Imagery and its Art Director. Workflow chat owns research/publisher Actions; Agent Operations owns hosted tasks.

Issues: #92 (Studio), #114 (pilot), #94 (shared board). Evidence: `office/FULL-SITE-ACCEPTANCE-2026-11-11.md`, current image review and latest root checkpoints. Read old reports as dated snapshots, not fresh proof.

## Actual current position

- Public site and complete unindexed magazine preview deploy on GitHub Pages. Twelve story mappings, article bodies, captions and current images were opened on desktop and phone-width frames. Phone390/tablet768 magazine frames showed no horizontal overflow. This is browser-width testing, not a claim of physical iPhone Safari acceptance.
- Chris previously confirmed GitHub editor → Commit changes → same-iPhone Studio reopen. Corresponding commits were verified. Do not repeat that same acceptance request.
- Studio’s direct authenticated Save, actual second-device editing/conflict and shared review decision remain unverified in a live authenticated browser. Controlled tests cover those paths. GitHub connector access does not provide a reusable browser token; never extract a connector credential or claim a mocked transport is a live authenticated test.
- A newly identified defect: committed draft edits can leave the generated magazine preview stale. Studio also loaded older candidate-media records instead of the Director’s selected image, and preview-to-Studio navigation lost article selection.

## Preserved unfinished implementation — resume, do not start over

Branch: `wip/website-editing-handoff`.
Commit: `59074a207fb5a3c59039c8657c99e6a2994dc5f6`.
URL: https://github.com/TheFanGuys/HVLS-360/tree/wip/website-editing-handoff .

This is WIP, **not merged or deployed**. It adds `office/preview-live.js` to refresh review-edition text from current committed GitHub drafts; updates the preview generator and 12 generated article pages; adds direct `?article=slug` Studio opening; displays selected image-map media in the Studio; removes the inaccurate blanket “Unapproved” heading. It preserves manuscript and approval bytes.

Existing 200 Python tests, Studio controlled-session test and review-packet test passed after these edits; `node --check office/preview-live.js` passed. New live-preview behavior still needs dedicated security/parity/error-path tests, cache-version review, end-to-end browser acceptance and deployment. Do not merge it merely because existing tests passed. Check HTML escaping, draft-state validation, allowed diagram paths, API failure/snapshot labeling and title/category updates. Confirm external script query versions prevent old cached clients.

## Complete this category

1. Inspect current main and WIP; fix the save→current preview path without bypassing editorial/release gates. Preserve a clear deployed snapshot if fresh reading fails.
2. Complete Studio direct links, selected-media consistency, shared-save/readback/conflict/recovery flow and useful save confirmations. Keep browser-local backups clearly distinct from committed saves.
3. Verify real authorized editing where access permits using a reversible test fixture; do not change approved article text just to test. Verify a fresh client reopens the saved revision, stale writes are rejected and both edits survive reconciliation. If actual browser authentication is unavailable, finish every independent check and record that exact blocker rather than asking Chris to repeat completed phone tests.
4. Audit navigation, article reading, reference search, shared assignments, office links, loading/errors, cache behavior and layout at phone/tablet/desktop widths. Fix actual failures. Inspect icon/home-screen assets. Keep internal process controls out of public reading flows.
5. Run relevant suites and safety checks, merge tested changes, verify successful Pages deployment and actual deployed URLs. Report deployed versus WIP behavior separately.

## Definition of 100%

- All required public and office screens are reachable and usable at the tested sizes, with no known broken references, missing selected media or horizontal overflow.
- A saved draft is durably committed, its current version appears on reopening/preview, and the edit/review/conflict path has real acceptance evidence with access and device scope stated.
- Recovery and failure states protect edits; no unapproved publication or secret exposure.
- Required checks pass on the merged revision, deployment is verified, open category defects are resolved, and #92/#114/root records contain concrete evidence. A remaining authentication/device blocker means this category is not yet 100%.

First action: compare the preserved WIP with current main and add the missing live-preview tests, then complete the remaining acceptance without routine stops.
