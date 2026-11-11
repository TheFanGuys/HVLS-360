# HVLS 360 — Operating readiness

Verified November 11, 2026 against main ebe3ad3, GitHub Actions, repository files and recorded live acceptance. This is a dated snapshot, not a continuously updated dashboard. Owner: COO / Managing Editor. All user-facing checkpoints below are America/New_York.

## Where the project stands

The magazine framework is already hosted on GitHub Pages. Eight drafts, the shared assignment board and Review Studio exist. The publication is not yet an accepted, fully unattended newsroom. Scheduled collection and routing are scripts; they do not invoke AI writers, independent experts or a functioning autonomous editorial staff.

| Area | Verified state | Evidence / remaining limitation |
|---|---|---|
| Hosting/deployment | Working | Pages run 43037866710 succeeded at ebe3ad3 on Nov 11. No domain migration needed to begin the GitHub pilot. |
| Repository checks | Working | 161 Python tests pass; Research Desk Tests 43037766610 and Publication Safety Gate 43037766791 passed for PR #112; safety gate 43037867605 passed on main. |
| Shared assignments | Working for read/coordination | Issue #94 links eight story issues #84–91; shared-assignments.html reads GitHub. Older local note screens are not the canonical board. |
| Manuscript reading | Verified in deployed desktop browser | All eight registered. TAZ was opened live without credentials with matching notes/media. PR #110's focus/scroll behavior observed at top of viewport. Not proof all devices passed. |
| Shared editing/review notes | Implemented; real authenticated device acceptance open | Contents API, optimistic conflicts, readback and revision-bound editorial outcomes are tested with controlled transport. No real authenticated phone save, second-device reopen or founder decision write has been verified. |
| Editorial copy | Full queue revised | PRs #111/#112; eight revision-specific voice records. Sources preserved. Standing all-future-articles voice instruction is in AGENTS.md and COPYDESK-STANDARD.md. Chris's acceptance of the revised voice remains open. |
| Technical evidence | Eight AI review artifacts; zero qualified signoffs | technical_signoff_audit.py: 8 records, 8 AI reviews, 0 qualified completions, no structural errors. Define exact claims needing external evidence instead of assuming every general news item needs an outside engineer. Current eight records remain held. |
| Media | Recovered and organized; final clearance open | 15 inventory records, 2 retained TAZ photos, rejected image excluded, four diagrams reviewed/rendered. Final model applicability, captions, customer privacy and technical/readability checks remain. |
| Research schedule | Prior scheduled execution verified | Research run 42902875397: event schedule, success, Nov 10. Current cron Tue/Fri 15:00 UTC (10 AM Eastern in November; 8 AM Arizona). That older run did not verify all later additions. |
| Research reliability | Incomplete | Three manufacturer-discovery errors across Rite-Hite, ABB and Invertek. Bounded source candidates added in #102; those candidates are not verified coverage. Current COO summary is a dated snapshot. Expanded collection → Issues → committed summary needs real run evidence. |
| Finished article production | On demand, not autonomous | Pipeline prepares briefs/skeletons and task packets; no scheduled model-driven reporting, writing, completed specialist reasoning or voice editing is deployed. |
| Approval/release | Fail-closed code tested; live founder release untested | Studio outcomes are not publication approval. publish_approved.py, render_release.py and catalog tools are manual preparation steps; no publisher Actions workflow exists. Never fabricate founder approval to test live publication. |
| SEO | Metadata prepared | Eight checksum-bound metadata records and renderer/catalog support. No actual ranking, search volume or audience performance verified. |
| Marketing/ads | Planning only | Distribution queue has no placements. No posting integrations, outreach, sponsors, campaigns or spending active. These are not blockers to a small editorial pilot. |
| Custom domain | Not selected/purchased | SEO/Marketing domain brief prepared in DOMAIN-PLAN.md. Availability and actual Namecheap prices unverified. Chris purchases after selection; no DNS changed. |
| Access protection | Unverified administration setting | Branch protection/required-review settings could not be confirmed with the current connector. Tested scripts do not prove that every direct GitHub push is administratively blocked. |
| Legacy PRs | Four old PRs still open | #1, #2, #10, #13. Much work was delivered through later PRs; compare before closing or merging. |

No approved news articles or approval records were found. The editorial-standards page and existing public lead/office files are already online. “No article publication authorized” does not mean the public repository or office pages are private.

## The completion sequence

| Gate | Owner | Concrete acceptance | Internal checkpoint |
|---|---|---|---|
| P0: real editing acceptance | Review Studio Engineer / Mobile QA | Authenticated saved edit; verified commit; reopen same and second device; stale conflict and disconnected behavior; iPhone Safari evidence | Nov 12, 5 PM |
| P0: research acceptance | Research Pipeline Engineer / Research Lead | Expanded run produces deduplicated assignments, bounded source failures, actual summary commits and useful failure handling. Verify next scheduled run, not just cron text. | Nov 13, 5 PM |
| P0: first article clearance | Technical Editor / Media Director / Editorial Director | Resolve exact consequential claims and visual holds for one launch article; current sources and voice revision ready for Chris | Nov 13, 5 PM |
| P0: founder approval and release rehearsal | Chris / Release Engineer | Chris approves exact text/media; prepare isolated release PR; verify output/canonicals/RSS/sitemap and receive release authorization. No automatic merge/publication. | After the prior gates; depends on Chris's decisions |
| P1: domain shortlist | Head of SEO / Marketing | Dated Namecheap availability and first-year/renewal prices; recommend name to Chris | Nov 13, 5 PM |
| P1: cutover | DNS Engineer / SEO Migration Specialist / Chris | After GitHub acceptance and purchase, reviewed configuration and successful HTTPS/URL/indexing checks | After purchase; timing depends on DNS/certificate readiness |
| Later: unattended editorial agents | COO / Technology Lead | Choose and implement a real execution environment/model budget, inputs, credentials, review quality, failure recovery and measured outputs | No defensible completion date yet; not currently built |

Planning target for an accepted GitHub editorial pilot: November 16, 2026, provided the P0 evidence and founder decisions are complete. This is a conditional internal target, not a guaranteed launch date or a claim of work running between chat turns. The next decision-quality checkpoint is November 13 at 5 PM Eastern. If an authenticated device test or article clearance remains blocked, the pilot date moves with that gate.

“Fully automated” is a different milestone from “the site runs on GitHub.” A custom domain will not supply the missing autonomous editorial execution. The low-cost current model is scheduled GitHub discovery plus assistant-led reporting/editing and explicit founder release approval. No paid API/service commitment is authorized.

## Cross-chat reconciliation

Available context summaries corroborate Research, Editorial, Technical, Media and Technology work, and the repository contains their concrete outputs. They do not provide live control of other chat threads. No completed separate Marketing/SEO/Ads final report was recovered from those chats; #103/#104 and the current launch/domain files are the known replacement work. A full previously named staff roster was not recovered, so team-roster.json is the explicit consolidated operating roster, not a claim that unseen chat agents were deployed. The original faulted chat's uncommitted/unretrieved work remains unverified.

## Team chart

team.html is a self-contained clickable organization chart of 79 named roles across nine departments plus founder/COO leadership. Every title opens its duties, deliverables, reporting line, execution status, supporting files and limits. The chart distinguishes assistant-led work, script support and planned roles. Zero continuously running AI staff are verified.
