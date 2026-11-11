# HVLS 360 — decision and checkpoint log

This durable record belongs to the project, not one chat thread. Append concrete decisions/results and update PROJECT-HANDOFF.md / PROJECT-STATE.json when they change. Never store credentials or confidential customer information here.

## November 11, 2026 — recovered standing decisions

- Chris is final editor/publisher; no news article is approved or released. Exact text/media and final release require explicit approval.
- Serious US-focused trade-magazine reporting. Every current/future article needs a separate voice pass; later edits require recheck. #111/#112 revised all eight and recorded manuscript hashes.
- COO explains the request, approach, responsible roles and checks before execution; no routine extra confirmation for already authorized reversible work. #117.
- Hard $0 additional operating budget; no paid APIs/hosting/credits/top-ups/trial conversions/fallbacks. Stop at free limits; do not ask for a paid budget again. #118. Chris's potential manual Namecheap domain purchase is separate.
- Direct Command Center COO conversation desired; #116. Not operational. A static artifact is not an AI execution service; no independent running agents are verified.
- #113 delivered a complete 79-role chart with truthful execution labels. Named roles are not employees or a deployed autonomous team.
- SEO/Marketing own domain research; #115. Chris purchases himself after GitHub acceptance. No availability/price/purchase/DNS claims.

## November 11, 2026 — chat failure continuity

Trigger: Chris points out that the operating COO still depends on a chat which can fail, repeating the original hours-long recovery.

Action: establish root PROJECT-HANDOFF.md, PROJECT-STATE.json, this log and a Command Center recovery page. Replacement assistants must read durable records before asking for history. Recovery prompt embeds the fetched handoff for portability and includes canonical URLs for verification. API failures must be visible; an offline prompt must not be labeled a fresh snapshot.

Limits: This does not prevent ChatGPT errors, import inaccessible chats, automatically synchronize conversation history, provide an AI runtime, or guarantee that a fresh chat has GitHub access. With connector access, the next assistant verifies the repository directly. Without access, the copied handoff supplies the checkpoint and identifies what remains unverified.

Maintenance: update after meaningful work and before changing focus. A policy without future checkpoint updates will become stale; show the checkpoint date and verification status rather than hiding it.


## November 11, 2026 — conversation link deferred; research repair

Chris said “Don’t worry about the coo conversation link.” Defer #116; no conversation backend was deployed. Continue the original GitHub editorial pilot. Do not keep asking about the link or paid budget.

Reproduced a collector bug: email.utils.parsedate_to_datetime raises on normal Atom/RFC 3339 dates, so the intended ISO fallback was never reached. Recent Atom leads were silently rejected. Added the fallback on RSS parse failure plus timestamp/offset/stale/future/invalid checks and end-to-end Atom collection coverage. 163 Python tests and publication guard passed locally.

Bounded live sitemap recheck: Rite-Hite returned HTML at https://www.ritehite.com/en/am/404; ABB request raised HTTPError; Invertek XML exceeded 1,500,000 bytes. These remain source-coverage blockers, not fixed by the timestamp repair. Local/live checks do not prove the updated scheduled workflow ran. Next: resolve bounded manufacturer retrieval and verify expanded shared intake; retain all article/founder gates.


## November 11, 2026 — manufacturer sitemap retrieval repaired

Official robots files pointed to the correct sitemap indexes. Retrieved Rite-Hite's Americas child (409,794 bytes), ABB's US child (gzip magic bytes, 1,541 compressed / 14,003 expanded bytes), and Invertek's valid 1,552,694-byte sitemap. Configured those regional sources, added bounded gzip decoding, raised the hard limit from 1.5 to 2 MB for wire and expanded bytes, rejected non-sitemap HTML/unsafe source overrides, and prioritized relevant paths before the 40-URL cap.

Actual repaired collector live recheck: Rite-Hite 148 candidate URLs discovered / 40 retained; ABB 25 / 25; Invertek 5,504 / 40. All three parsed with no errors in this scoped check. This is URL discovery, not source-claim verification or exhaustive coverage. The current COO summary records this limited scope and preserves its original research timestamp; other manufacturers were not rechecked. 168 offline tests pass including gzip/expanded-size protection, configured roots, unsafe overrides, HTML rejection and prioritized capped candidates. No paid service or publication. Next: verify the expanded actual research-to-Issues pipeline.


## November 11, 2026 — actual expanded research run inspected

PR #122 fixes intake starvation: all eligible briefs reach deduplication before the five-new-Issue cap. New tasks receive internal checkpoint dates. Exhausted history scans and missing CI authentication fail closed. Newly created keys are rechecked against GitHub before being marked deduplication-tested; sanitized results enter the COO summary and artifact. Research workflow-definition changes trigger a serialized main run, in addition to the existing Tue/Fri schedule.

Actual run 43048487736 (event=push, revision 0e6d8c346a7ace8400f7df807d4348e5314a805e) completed all pipeline steps successfully and committed four public indices at ef2b98180b1dc21cfe701e0be7803dd8c66555e0. GitHub artifact 13868427054 and job logs were inspected. 14 headlines were collected; all held by relevance screening; zero briefs/new Issues. The authenticated Issues read and summary push worked. New Issue creation/readback remains unverified, and no next-schedule claim is made. One intermittent ABB TimeoutError was recorded in the discovery report and surfaced in Actions/COO warnings. Do not hide that warning or weaken filters to force a passing intake demonstration.

173 offline tests pass. Next: add useful verified first-party manufacturer intake, then observe a genuine shared Issue and its deduplication readback; address timeout resilience without unbounded retries. No spending, paid services, article approval or article publication.


## November 11, 2026 — official news reaches an existing shared assignment

PR #124 adds an official Invertek news-index parser: same-host HTTPS article URLs, reported publication dates, 14-day recency and explicit product relevance while preserving US/international holds. Existing manual research pitches are matched by exact primary URL, so already accepted #96 is reused. PR #125 fixes a real-run archive size failure by accepting only a bounded 700 KB prefix with 40 complete dated entries; otherwise error remains visible. Scope is a sample, not the whole archive. Sitemap timeouts retry once only; HTTP failures do not retry.

Actual run 43051318664 at e08a6259be9b378f2bd151af1596baf4910891e8 completed: 18 collected, 1 research brief, existing Issue #96 matched, 0 duplicates/new Issues; summary commit 8435d7bf9c098be58fdd46d007eda3df9b04347f. The first attempt 43050580115 exposed the oversized news archive and did not accept a lead; no false acceptance was claimed. Latest official E4 lead is publisher-reported October 29, 2026, not its original launch; performance and US applicability remain unverified. The Nuremberg exhibition is held. ABB still times out after the retry and is reported in Actions/COO warnings.

188 tests passed. New Issue creation/readback and the next scheduled trigger remain unverified; do not fabricate a test story. Next: prepare the first existing article for specific substantive founder review, keeping technical/media/phone gates intact. No spending or article publication.


## November 11 — first article review packet

Prepared founder-facing review packet in editorial/reviews/hvls-air-movement-vs-ventilation-review.md for unchanged manuscript SHA-256 3e5562a223bfca819a64db283e1268e21e33dbb01419e1c2e387aaba5fe5d7a7. EPA and ASHRAE 62.1 public pages rechecked; remaining source rechecks and phone-width diagram acceptance assigned to assistant roles for next active session. Chris can judge text now. Original diagram means optional third-party photograph permission is not required. Qualified technical signoff remains zero; no release authorized. This is a review packet, not a completed technical/visual clearance.


## November 11 — fresh-chat transition and editorial direction

Chris requested a safe move before thread failure and reaffirmed that AI-sounding copy, AI-looking design and repetitive legal/process warnings are unacceptable throughout the project. Updated AGENTS.md and COPYDESK-STANDARD.md with direct voice/design rules; internal review records remain internal, material qualifications stated once in context. START-HERE.md carries a short restart prompt and exact next task. PR #127 is merged, 188 tests passed; no active mutation is left mid-operation. Next session finishes first-article sources and phone diagram, then pilot acceptance. No COO conversation work unless reopened by Chris.


## November 11 — first-article source and diagram checks completed

Completed first-article BAF/DOE/Standard 55 source rechecks and replaced wide airflow SVG with stacked phone-readable artwork. Inkscape 350px render visually inspected; 15px minimum text at that width. Manuscript and voice hash unchanged. Independent technical signoff, founder decision and real authenticated phone acceptance remain open.

Read the live rendered BAF guide sections 2.1 and 2.4, DOE item 5 (June 8, 2012), and ASHRAE public Standard 55 scope/2023 edition. No numerical performance or standard compliance claim added. Diagram arrows stay indoors for mixing and cross separate walls for outdoor supply/exhaust. Original SVG hash and detailed acceptance are in the companion review. Existing independent-review gate retained; source checking is not qualified signoff. No spending or article release.


## November 11 — Studio conflict comparison and save-state repair

Review Studio now shows the newer GitHub manuscript alongside a retained local edit after a save conflict; explicit reconciliation is required before retrying. Verified saves show local date/time and refresh review history so prior-revision reviews are marked stale. Corrected airflow image dimensions to the new 700×1110 artwork.

Reproduced gaps by code inspection and executable Studio script tests. Added conflict comparison, preserved working edit, explicit reconciled retry against latest blob, save date/time, and review-history refresh. Existing API SHA check still rejects later races. Controlled tests and 188 Python tests pass; editorial/launch/publication audits pass. No repository credential is available to this Studio session, so real browser-authenticated write and physical iPhone/second-device acceptance are not claimed. No article or editorial approval created. Next: deployed layout check and remaining #92 acceptance.


### Studio deployment acceptance — November 11

Pages deployment 43055755724 succeeded for b39c383519216faa86381321ee4513122daf30a6. Live browser reloaded the new Studio, confirmed hidden conflict controls, opened Air Movement, loaded the 700×1110 diagram at its correct aspect ratio, and showed no horizontal overflow in the tested desktop viewport. Guest GitHub Save remained disabled. This is deployed read/UI evidence; real authenticated writes and physical-phone/cross-device acceptance remain open.


## November 11 — founder iPhone save/reopen acceptance

Chris verified iPhone GitHub editor commit and same-device Review Studio reopen. Current manuscript SHA-256 6558329823c2e6521c5d030bc05acfc105b06001dfd5cb624856d921e3b0448b; founder edits preserved, voice/technical delta rechecked, SEO packet checksum refreshed. Studio direct Save and second physical device remain unverified; qualified technical review and final founder approval remain open. Repository evidence: commits c170cbb and 84c39bf, blob e0d72e2c15c20f49803d63068c0b924e11873f78. Technical delta is capitalization/whitespace only; prior source and diagram findings still apply. Next: qualified review evidence for the first article; continue other accessible pilot tasks while direct Studio/second-device acceptance remains open.


## November 11 — full-site acceptance and magazine preview

Full-site acceptance: 190 Python tests, six JavaScript suites, editorial/metadata/publication checks and 191 local HTML references passed. Live homepage/reference search/shared board inspected; board loaded 17 tasks and search worked. Added nine-page unindexed full magazine preview of all eight current drafts, fixed airflow renderer dimensions, stale Powerfoil reference and personal-note labeling. Report: office/FULL-SITE-ACCEPTANCE-2026-11-11.md. Preview deployment/browser acceptance follows. Public catalog/RSS/sitemap remain unchanged; founder release and qualified review are still outstanding. Direct Studio physical-device and second-device acceptance remain open.


## Deployed full-preview acceptance

PR #131 merged at 80c2464b35aebcb7d8b3ba31f577d76d4f3cfea5. All three PR checks and main Publication Safety Gate passed. Pages deployment 43059631543 succeeded. Live browser verified eight magazine cards and opened all eight article pages: content rendered, zero broken loaded images and no horizontal overflow in the tested desktop viewport. Preview noindex confirmed; Air Movement diagram loaded. Team/COO/editorial/technical/media screens also opened without displayed loading errors. Full preview: https://thefanguys.github.io/HVLS-360/office/preview/ . Physical full-site iPhone acceptance is not claimed.


## November 11 — founder approval and resource direction

Chris reaffirmed approval of all eight current articles. Recorded revision hashes in editorial/founder-approval-register.json; do not keep asking for founder article approval. Independent technical/media findings are separate and are not fabricated by this record. Public resources now focus on studies, laws, regulations and technical information; removed manufacturer manual/product-support listings. Manuals may remain internal source citations.


## November 11 — content depth and trade-publication redesign

Delivered content/design expansion: twelve original pieces in the full preview (eight existing plus four sourced briefings); twenty-four research/regulatory/technical source entries; six-source research rail on the public homepage. New subjects: industrial-fan study evidence, CFIAC research, OSHA lift classification and fan guarding. Compact masthead, paper-toned reading surface, serif headlines and restrained source cards replace the oversized dark presentation. Original eight founder approvals preserved; four new assignments #133–136 remain separate. No manufacturer manual listings restored. Source and voice reviews carry exact hashes; new briefs are concise and not padded to feature length. Technical register coverage and launch metadata updated. New public items are source-library entries, not falsely labeled original reporting. Preview and library deployment acceptance follows.


## Expanded publication — deployed acceptance

Content/design deployment verified November 11: PR #137 merged at 2eb6044e8afb179cc2ad569b9b39d6cf87f658c1; Pages run 43062393678 succeeded; all three GitHub checks passed. Live browser observed 12 preview cards, opened all four new briefings with rendered bodies/no horizontal overflow, confirmed the public homepage's six-source research rail, and tested OSHA search: 7 of 24 reference entries. Paper-toned design and compact masthead visually inspected. 192 Python tests, six JavaScript suites and 267 local references passed. Existing eight founder approvals remain recorded; four new briefings remain distinct review assignments.


## November 11 — image-led magazine direction

Construction Today reference inspected in live browser. Rebuilt review edition as an image-led trade magazine: black compact masthead, BFG blue/orange, featured + supporting story, image grid, useful sidebar and captioned article headers. All twelve pieces have an image mapping; authentic publisher-authorized field photos used where applicable, original diagrams for technical subjects. Three site-owned photos visually checked, resized/compressed with metadata stripped; source/model/caption provenance recorded. Public research rail also has clearly labeled illustrations. Founder article approval remains unchanged. Tests: 194 Python cases, six executable JavaScript suites pass. Publish renderer consumes the same safe media map. No borrowed Construction Today content/images or unlicensed manufacturer photographs. Deployment verification follows.


## Image-led edition — deployed visual acceptance

Image-led BFG magazine accepted live November 11. PRs #138/#139 merged; versioned stylesheet commit 40e1af1b479f633f387df2528725de0aecb1ff36 deployed successfully in Pages run 43065072180. Fresh preview URL ?v=20261111-image-led verified: black BFG masthead, blue/orange branding, 320px feature photograph, concise card headlines, distinct supporting photograph and sidebar. All twelve article header images/captions previously opened live with no broken images or tested desktop overflow. Final homepage overflow false. 194 Python tests, six JavaScript suites and 280 local references passed. Existing founder approvals unchanged.
