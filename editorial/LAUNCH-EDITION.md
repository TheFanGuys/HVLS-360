# Launch edition 1 — content inventory and completion standard

Reconciled November 11, 2026, against main checkpoint `7b6727cccbab` (use the full baseline SHA in `launch-completion-ledger.json`). Accountable owner: Content Completion Lead. The machine-readable ledger binds each manuscript, source/voice record, metadata and selected image to exact revisions. It is a candidate manifest, not release authorization.

## Finite scope

Complete the twelve existing original pieces: eight field guides/documentary analyses and four concise source briefings. All twelve have manuscripts and preview pages. These are useful working trade articles; this inventory does not claim twelve reported investigations, operated product tests, interviews or a larger hidden archive.

The edition covers the decisions a US fan project encounters: what air movement can accomplish, how to read efficiency evidence, product documentation, drive/control compatibility, installation access, and the limits of research and regulatory shorthand. It serves installers/electricians, facilities, mechanical specifiers and buyers. Manufacturers/distributors can use its submittal and documentation questions. Editorial planning and evidence comparisons are original analysis; no customer observations, measurements or expert identities are invented.

| Issue | Piece | Field purpose | Text decision |
|---|---|---|---|
| #84 | Air movement vs ventilation | Separate comfort/mixing from outdoor-air exchange | Original exact revision approved |
| #85 | ABB IP66 drives | Check enclosure, environment and OEM compatibility before a retrofit | Original exact revision approved |
| #86 | CFEI vs CFM/W | Read ratings at comparable operating points | Original exact revision approved |
| #87 | Greenheck DS | Match documentation and controls to product generation | Original exact revision approved |
| #88 | Powerfoil 6 | Define electrical, structural and shutdown coordination from the manual | Original exact revision approved |
| #89 | Scissor-lift planning | Match access, loading and component-handling sequence | Original exact revision approved |
| #90 | VividAir/GFY controls | Identify hardware before assuming interchangeability | Original exact revision approved |
| #91 | TAZ 72-inch guide | Distinguish aisle airflow and resolve model/guide inconsistency | Original exact revision approved |
| #133 | Factory fan study evidence | Separate comfort responses and physiological findings | New brief; founder decision pending |
| #134 | Ceiling-fan-integrated HVAC | Coordinate supply, fans and operating modes during design | New brief; founder decision pending |
| #135 | OSHA lift classification | Start with the actual equipment class and applicable reference | New brief; founder decision pending |
| #136 | Fan guarding | Record blade locations and surrounding working levels | New brief; founder decision pending |

Chris's original eight approvals are stored in `founder-approval-register.json`; all eight current manuscript hashes match. Older frontmatter and review checklists saying “not approved” are historical process text, not a reason to ask again. Technical documentary findings, any genuinely required specialist evidence, media acceptance and final release authorization remain separate. No qualified independent reviewer identity/date/findings are currently recorded; this does not automatically require hiring an expert for every descriptive statement. Resolve actual claims before determining that need.

## Where the material lives

| Material | Record | Visibility and meaning |
|---|---|---|
| Twelve manuscripts | `editorial/drafts/` | Public repository files; not released news merely because present |
| Sources, claim checks, voice edits | `editorial/reviews/` | Internal editorial records in a public repository; exact revisions in ledger |
| Twelve reading previews | `office/preview/` | Noindex, publicly accessible review edition; no authentication/privacy claim |
| Metadata and distribution drafts | `office/launch-package.json` | Twelve packets; distribution remains held |
| Selected images and framing | `editorial/media/article-images.json` | Twelve mappings using seven photos and three diagrams; current composition acceptance preserved |
| Source image candidates | `art-library/` | 73 candidate files; excluded from Pages but public through GitHub; not all selected/cleared |
| Public research/reference shelf | `resources/research-index.json` | 24 research, regulatory and technical links, checked November 11; no manufacturer-manual listings |
| Research intake | `office/research-latest.json` and Issues #96/#97 | Unverified leads and accepted evidence assignments, not additional finished articles |

Manuals remain legitimate internal citations for product analysis. The public reference shelf instead distinguishes studies, research programs, rule text, dated interpretations, official standard overviews and technical background. Its check dates describe the recorded checks, not a promise of continuous currency. The factory-study announcement is identified as manufacturer reporting; the laboratory/HVAC material is not a measured guarantee for an industrial building. Before release, recheck any changed, time-sensitive or unresolved claim.

## Verified backlog and coverage gaps

Issues #96 and #97 were fetched directly during this reconciliation. Both are **Researching — accepted for evidence work**, not accepted articles or approved copy. Hold both outside edition 1 while preserving their assignments:

- **#96, Optidrive E4:** valuable service follow-up, but US SKUs/listings, exact communications options and OEM compatibility still need evidence before a retrofit article. The October 29, 2026 update is not the original launch; the manufacturer's index records unveiling November 25, 2025. Do not fill the gap with a supposed drop-in replacement claim.
- **#97, Greenheck MOA/CPF:** useful ducted air-movement coverage, distinct from DS ceiling fans. Exact submittal, mechanical/electrical package boundaries and controls remain unresolved. The release body is October 2026; a June date in its URL does not establish the launch day.

Other gaps are real commissioning results, documented service cases, construction-market effects and rental availability/cost evidence. None has a verified finished assignment in this inventory. They belong to ongoing reporting; they do not justify arbitrary launch article counts or invented field experience. A finite launch can be useful while transparently limiting its reporting depth.

## Release handoff and acceptance

`launch-completion-ledger.json` is the shared reconciliation and per-item completion record. It contains manuscript and selected-asset hashes, source/review pointers, matching voice evidence, audiences, field purposes, metadata, related-story candidates and founder decision states. Website and Workflow owners should consume those exact revisions rather than assume a preview URL is a live article.

Related-story slugs are planned relationships. They must resolve to preview files in preview and only to actually released targets on the public site. Do not insert phantom article URLs. Sponsor/distribution copy remains held for separate destination and copy authorization.

Completion requires every item to have resolved claim-level evidence or a justified narrowed scope, current exact-revision voice evidence, accepted subject-aware imagery, matching metadata and correct founder decision. Original-eight text approval is preserved. The four newer briefs require their first founder decision; all release execution belongs to Workflow. This document does not call the category complete while those decisions or required evidence remain open.

## Current resolution and exact remaining dependencies

All twelve current documentary scopes are resolved in `reviews/LAUNCH-CLAIM-RESOLUTION-2026-11-11.json`; the technical register now distinguishes documentary review from qualified independent signoff. There are still zero professional signoffs. Any later prescriptive or site-specific claim triggers the specific professional review recorded for that story. No manuscript revision was needed; every original-eight approval hash remains intact.

The selected lead/card images retain prior composition acceptance. TAZ needs its second photograph added to match the approved text: Art completed source-size selection, rights, accurate caption/alt and full-frame intent in `media/TAZ-SECOND-PHOTO-HANDOFF.json`; Website must integrate it and record actual desktop/tablet/phone acceptance. Eleven illustrated packages are integrated; TAZ is held for that concrete dependency. The other remaining content decisions are the first founder decisions on #133–136. No repeat approval of #84–91 is requested.

Validation at this checkpoint: 205 Python tests, seven JavaScript suites (rebased onto Website PR #143), exact launch-evidence audit, technical/metadata/editorial audits and publication guard passed. No release artifacts or manuscript bytes changed.
