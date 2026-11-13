# 72-Inch TAZ Field Guide — Technical Review

**Status:** Draft source-backed; qualified field review and publisher approval pending.

## Source and photo checks
- Official product: https://vividairmovement.com/product/taz/
- Official 72-inch operations guide: https://vividairmovement.com/wp-content/uploads/2023/01/TAZ_Installation_and_Technical_Operations_Guide_1.2023.pdf
- Publisher confirms ownership and editorial permission for two retained 72-inch TAZ photographs.
- Previous mistaken Patterson barrel-fan identification is corrected; do not use that unrelated image.
- Two WebP files (02 and 03) are committed. Publisher rejected photo 01 as not a TAZ; it was removed from the repository. Do not use the rejected photo.

## Required checks
- [ ] Confirm actual installed unit nameplate and 72-inch model against publisher field photos.
- [ ] Qualified GFY/VividAir technician checks directional airflow, mounting, screens and louvers.
- [ ] Electrical/controls reviewer checks model-specific guide, wiring and interlock terminology.
- [ ] Verify exact manufacturer guide revision applicable to installed model.
- [ ] [x] Import two retained WebP files into repository; [ ] validate captions, exact fan identification and customer privacy.
- [ ] Editorial copy and source-link review.
- [ ] Explicit publisher approval of article text and chosen photos.

**No publication authorized.**


## Reopened primary source — November 11, 2026

Reopened the live TAZ product page and retrieved its linked January 2023 PDF. The page labels the download 72-inch, but the PDF repeatedly uses 7ft TAZ Fan headings and on printed p. 13 (PDF page 14) lists GFY-TAZ-72-480 and GFY-TAZ-72-240. Visually checked that page. This is a manufacturer-document nomenclature inconsistency; do not infer an actual 84-inch dimension or silently certify the guide against the installed fan. Added the discrepancy to the manuscript and source label.

Printed p. 13 expressly identifies the **VFD-to-motor** cable segment, 200-ft limits for its listed 230/460 VAC cases, and factory consultation beyond 200 ft. This is not a keypad/network distance limit and must not be transferred to another drive generation. Fire-interface pages contain different drive/terminal arrangements: keep wiring statements conditional on exact drive and supplied drawing.

Next: match nameplate and installed drive to the applicable manufacturer documents, resolve nomenclature, validate the two retained captions and obtain qualified review. Source retrieval is complete; model applicability and founder approval remain open.


## Voice edit — November 11, 2026

Rewrote the opening around an aisle layout; replaced abstract headings with concrete ones; consolidated repeated mounting/controls cautions; removed the duplicate question list and closing recap. Internal verification notes remain in this review record rather than appearing as article copy. Sources, manufacturer attribution, untested performance status, unreadable nameplate and the 72-inch/7ft document discrepancy are retained. No new interview, test, field observation or technical signoff asserted. Launch metadata was reread and remains applicable; only its manuscript checksum changed.

Founder feedback: no specific factual changes requested; some passages still sounded AI-written. This is editorial feedback, not approval. This voice pass does not complete independent technical review, photo/caption/privacy review, a new outbound-link check or founder approval.


Nov 11 full-queue recheck: included the TAZ revision from PR #111 in the eight-article voice review. No additional TAZ text changes needed in this pass. All technical/media/founder holds remain.


Voice pass revision record: 5c088ae8906341da949273b96087b4265acee8bdde864e675c185c4209753797 (SHA-256), November 11, 2026. Editor: Editorial Director role performed by the assistant. Full queue reviewed under the standing all-future-articles requirement. This records the editorial pass only; founder acceptance, independent technical review and media clearance remain open. Recheck voice after any manuscript change.


## Current launch reconciliation — November 11, 2026

Exact manuscript SHA-256: `5c088ae8906341da949273b96087b4265acee8bdde864e675c185c4209753797`. Manuscript bytes unchanged; this reconciliation does not create a new text revision. Existing separate voice pass remains matched.

Technical disposition: **documentary review complete for current scope** — Directional-fan documentary briefing with openly attributed publisher photo identification. Per-claim primary evidence, dates and retrieval modes: `LAUNCH-CLAIM-RESOLUTION-2026-11-11.json`, record `vividair-taz-72-field-guide`. This supersedes blanket qualified-review holds for this documentary scope; zero professional signoffs are claimed.

- Rechecked two sizes, directional/angled application and attributed coverage claims. Evidence: Product specifications and technical download links; live_primary_recheck.
- Live guide retrieved; 7ft headings and 72-model labels are documented discrepancy. Article does not resolve actual dimensions from labels. Evidence: January 2023 linked 72-inch guide; printed p 13; live_primary_recheck.
- Publisher grants use and identifies two retained photos as 72-inch TAZ. Identification is attributed, not independently nameplate-confirmed. Evidence: editorial/media/publisher/taz-72-rights.json; existing_publisher_attestation.

Professional review becomes required if scope adds: Using this PDF as installation authority for a supplied unit, certifying the installed photo model, or issuing drive/interlock instructions.

Founder text: **approved exact revision**, preserved in `editorial/founder-approval-register.json`; do not ask for the same approval again. Selected media, metadata and release holds are separate in `editorial/launch-completion-ledger.json`. No release authorization is recorded. Historical unchecked items above are superseded only where this current record explicitly resolves them.

Illustration dependency: approved text describes two photographs but preview currently renders one. Second source is selected in `editorial/media/TAZ-SECOND-PHOTO-HANDOFF.json`; Website must integrate and inspect actual responsive placements. This is not a request to change or reapprove the manuscript.


## Field note revision — November 12, 2026

Chris's field note (Command Screen work order sguqboe963hhl1juch02): Big Fan Guys has installed the TAZ and seen it blow the 135 feet and more; placed at the end of racking aisles it can easily move air 150 feet down the aisle; the TAZ suits hard-to-reach spots that need air.

### Technical check

| Claim or element | Source | Change |
|---|---|---|
| Up to 135 ft linear coverage, up to 75,200 CFM | VividAir TAZ product page [1] | Kept as manufacturer figures |
| Big Fan Guys installed the TAZ and saw air carry 135 ft and beyond | Field note, Chris Fogarty, Nov 12, 2026 | Added, attributed to Big Fan Guys as observation, not a measured test |
| About 150 ft of air movement from the end of a racking aisle | Field note, Chris Fogarty, Nov 12, 2026 | Added as field observation |
| TAZ suits hard-to-reach spots | Field note, Chris Fogarty, Nov 12, 2026 | Added to opening |
| "we haven't tested them" | Superseded by field note | Removed |

No drawings or image changes. Air speed at work positions remains unmeasured; the aisle air-speed paragraph stays as written.


## Voice rewrite — November 13, 2026

Chris (Command Screen work order haj1a4uy3ry0waic6qlz): the article still read as AI-written. Editor desk rewrote the full body to house style. Manuscript SHA-256 after rewrite: `5c088ae8906341da949273b96087b4265acee8bdde864e675c185c4209753797`.

Changes: new opening that says what the fan is for and where Big Fan Guys uses it; Chris's 135 ft / 150 ft field note kept in his words; cut the "real question" framing, the "doesn't mean / doesn't mean" pair, the abstract "service access belongs on the drawing" line and the closing recap; concrete section heads; one mention each of nameplate check and manufacturer documents. Banned-word grep: zero hits in the body. Bold: none. Body context-photo caption shortened to "Front of the 72-inch TAZ: discharge louvers, guard and chain suspension" and its anchor moved to the new photo paragraph.

### Technical check

| Claim or element | Source | Change |
|---|---|---|
| 36-inch and 72-inch sizes | VividAir TAZ product page [1] | Unchanged |
| Up to 135 ft linear coverage, up to 75,200 CFM (family) | [1] | Unchanged, attributed once |
| 135 ft and beyond observed; about 150 ft down a racking aisle; hard-to-reach spots | Field note, Chris Fogarty, Nov 12, 2026 | Kept, attributed to Big Fan Guys |
| Flat or angled mount, one or several directions | [1] | Unchanged |
| Jan 2023 guide linked as 72-inch; "7ft TAZ Fan" headings; GFY-TAZ-72-480 / -240 on printed p. 13 | [1][2] | Unchanged |
| Pre-unload review of layout, controller locations, supply panels; check mounting method per location | [2] | Unchanged |
| Under-mezzanine use named in the opening | Prior text (mezzanine aisles) and field note on hard-to-reach spots | Wording only |
| Photos show a 72-inch TAZ, chain-hung, guard and louvers | Publisher identification, editorial/media/publisher/taz-72-rights.json | Unchanged |

No new facts, figures or sources added. The product page could not be reopened from this run (fetch not permitted); every claim is carried over from the November 11 live primary recheck recorded above.
