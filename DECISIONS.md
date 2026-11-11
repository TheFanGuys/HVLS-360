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
