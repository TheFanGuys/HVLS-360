# HVLS 360 — Launch operations

Prepared November 11, 2026. Owner: Managing Editor with Marketing & SEO. This package does not authorize article publication, outreach, spending or sponsorship.

## Deliverables and status

`launch-package.json` contains the eight article-specific search titles, descriptions, audiences, related-story candidates and distribution drafts. Its SHA-256 values bind the copy review to the current manuscript bytes. Metadata is also stored in each manuscript, so the normal founder approval checksum covers it.

`python office/launch_readiness.py` reports stale packets or incomplete metadata. After a Studio edit, the Managing Editor must reread the manuscript and recheck the title, description, audience and distribution copy before updating that packet's checksum. Never refresh a checksum merely to suppress a failure. The length ranges are house editing limits, not a promise of search-result display or ranking. No keyword volume, ranking or traffic research is claimed.

The approved-article renderer consumes the manuscript's search title and description, while retaining its editorial headline on the page and in Article structured data. The approved-only catalog uses the same description for homepage/RSS discovery. The approval gate, canonical URL generation, RSS, sitemap and checksum checks remain in place. No draft URL goes into those public discovery files.

## Release sequence

| Stage | Responsible role | Evidence required |
|---|---|---|
| Source and technical checks | Research Lead / Technical Editor | Current primary documents, exact model applicability, recorded remaining limits and required specialist review |
| Image and caption clearance | Media & Art | Correct fan identity, permission, caption, privacy and visual accuracy |
| Final copy and metadata | Editorial / Marketing & SEO | Exact manuscript plus current launch-packet checksum; source links and related-story candidates checked |
| Founder review | Chris | Explicit approval of exact final text; editing, saving or closing an Issue is not approval |
| Release preparation | Implementation lead | Checksum-bound approval record; isolated release branch; safety, HTML, links and catalog checks |
| Final release authorization | Chris | Approval of the complete release PR and chosen article/visuals |
| Channel distribution | Marketing / Chris | Live article verified, destination/account identified, exact post approved separately |
| Follow-up | COO / Marketing | Record actual placement URL, date and results; no invented impressions or readership |

No publication date is committed until the editorial and founder gates clear. Candidate relationships are held in the packet; add related links in a later reviewed manuscript only when the target article is approved and actually live. Do not expose draft paths or create dead public links.

## Distribution copy and placement

All eight short post drafts remain in `launch-package.json` with `{approved_article_url}` as an intentionally unresolved placeholder. They are drafting material, not live social posts. Replace it only after verifying the approved article URL. No account is connected or posting schedule active.

Initial owned placement: a relevant editorial link on Big Fan Guys, subject to Chris's authorization and site access. Optional professional social placement: a Chris-authorized company or personal LinkedIn post. These are proposed destinations, not claims that accounts are available. Trade media, associations, newsletters and community submissions require destination-specific research, permission/rules checks and separate authorization. No messages have been sent.

`distribution-queue.json` separates eight draft campaigns from actual `placements`, which remains empty. After authorized distribution, record the real destination, owner, approval reference, copy revision, date, URL and results. Collect only the measurement data actually available; no paid analytics service is needed for launch. Search visibility and traffic performance remain unmeasured until real pages are approved and indexed.

## Sponsorship and disclosure

No sponsor inventory is sold and no revenue, readership or reach figures are verified. Proposed future placements are a clearly labeled article-page sponsor position or newsletter sponsor block, introduced only after separate founder approval of the format and terms. Never sell favorable technical conclusions or allow sponsorship to bypass fact checks. Keep independent reporting, manufacturer claims, paid placements and affiliate relationships distinguishable. Prepare actual rates only after scope and audience evidence exist; no price or campaign commitment is made here.

## Outstanding launch gates

- Complete real authenticated phone-save/reopen acceptance.
- Finish model-specific technical and visual clearance for the selected first article.
- Recover or recreate the missing media deliverables.
- Obtain founder review and explicit release authorization.
- Confirm the expanded scheduled research-to-Issues workflow runs successfully after its implementation.

This closes preparation of the launch metadata and distribution plan. It does not close the above gates or authorize outreach.
