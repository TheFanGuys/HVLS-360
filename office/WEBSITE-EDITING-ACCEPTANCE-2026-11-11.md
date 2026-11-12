# Website & Editing acceptance — November 11, 2026

Implementation merged in PR #143 at fb248dad3edfb9a57751af74d285cf66ff5764d0. Pages run 43127958015 completed successfully. This report supersedes older website WIP/deployment statements; it does not close live authenticated acceptance.

## Verified acceptance

| Criterion | Result and scope |
| --- | --- |
| Committed edit → current preview | Deployed unindexed article reads current main draft with cache:no-store and reports blob e0d72e2c15c20f49803d63068c0b924e11873f78 for Air Movement. Same current revision observed in all three frames. No approved manuscript was edited for this test. |
| Preview failure/recovery | Executable controlled tests cover API denial, malformed metadata, forbidden publication state, invalid revision, and retention of original deployed snapshot with explicit failure label. Browser-local backups remain clearly distinct from verified GitHub commits. |
| Renderer/security | Exact output parity for all12 current drafts against Python renderer; raw HTML escaping, credential-bearing link rejection, exact diagram allowlist, internal-notes exclusion. Titles/categories must be nonempty strings; updates use textContent. |
| Studio article and media consistency | Actual deployed Edit this article click retained article query; Studio opened the matching GitHub manuscript and warehouse-hvls.webp selected image. Guest Save disabled. Selection errors now reported and invalid/missing image-map records tested. |
| Core responsive screens | Magazine, Air Movement article, Studio, Command Center, shared assignments, reference library and public homepage checked in390/768/1280px frames. Effective content widths375/753/1265px due to scrollbars; scrollWidth equals clientWidth in all21 cases. Browser-width checks, not physical Safari. |
| Navigation/search | Fixed article Latest anchor to edition index.364 local href/src references resolved before proof-page addition; proof paths also opened live. Live OSHA search returned7 of24 sources; shared board loaded21 open assignments and Powerfoil filtering worked. Board text corrected to12 manuscripts/original-eight text approvals/four new briefs. |
| Home-screen identity | Command Center links dedicated SVG and180×180 PNG apple-touch icon; actual PNG visually inspected, labeled HVLS360/COMMAND. No claim of a new physical installation. |
| Merged verification | Clean detached worktree of merged fb248da passed201 Python tests, seven JavaScript suites, launch metadata and publication guard. Exact hosted run IDs appear below. Manuscript/founder-approval bytes unchanged. |

PR check runs: Publisher Command Center Checks43127889924; Research Desk Tests43127889935; both success. Publication guard also run locally on the merged revision; its hosted path filter does not trigger for this office-only change. No workflow settings changed.

## Explicit remaining dependency

Direct authenticated Studio Save, independent fresh-client reopening after that Save, real stale-client rejection/reconciled write retaining both edits, and real shared review write/readback have **not** been accepted in a live authenticated browser. The browser has no Studio repository credential; the GitHub connector does not expose a reusable browser token. A second physical device is unavailable. Owner: Website & Editing Lead for execution once Chris/access owner provides an authorized browser session/device. Do not extract connector credentials, request the already completed GitHub-editor/same-iPhone test again, fabricate signoffs, or change approved article text to simulate acceptance.

Controlled repository/session suites cover Unicode saves, two clients, stale conflict, retained text, explicit reconciliation, verified readback, save timestamp, decision revision races, restricted local storage and failure recovery. These are controlled tests, not live authentication evidence. The prior founder GitHub-editor → same-iPhone Studio reopen acceptance remains valid.

## Acceptance disposition

Implementation, deployment, accessible core UI, tests and release isolation are verified for the scope above. Final real edit/review/conflict criterion is blocked. Category is **not100%**; #92 and the category portion of #114 remain open. No article release, new approval, paid service, credential creation or outreach occurred. Snapshot cards/SEO and imagery remain deployment data; current saved manuscript refresh applies to article body/title/category in the internal unindexed review edition only.
