# HVLS 360° — Publisher approval protocol

**This feature does not publish automatically.** It is a guarded artifact-preparation script for a future release workflow.

1. Technical and editorial reviewers must finish their work. All source and media-rights evidence must be documented. Manufacturer-hosted photos are not automatically licensed.
2. The publisher must review the **exact** final article and explicitly approve it, ideally through a GitHub protected-branch pull-request review by the authorized repository owner.
3. A maintainer creates an approval JSON in `editorial/approvals/<slug>.json` containing the required review fields, a SHA-256 digest of the exact draft bytes, source review notes, media permission evidence, publisher name, timestamp and the literal attestation `I explicitly authorize publication of this article.`
4. On a dedicated release-review branch, the maintainer runs `python office/publish_approved.py --slug <slug> --approval-file editorial/approvals/<slug>.json`. This prepares a verified `articles/<slug>.md` file.
5. On that same branch, run `python office/render_release.py --slug <slug>` to generate `articles/<slug>/index.html`, including canonical URL, Open Graph metadata and Article structured data. The rendering step verifies the current publication guard before writing and refuses to overwrite an existing HTML page.
6. On the same release-review branch run `python office/public_catalog.py --write` to update the homepage story rail, RSS feed, and XML sitemap exclusively from approved, audited article artifacts. The script does not read unapproved drafts or unverified research leads.
7. Verify the final HTML visually, audit links and accessibility, and explicitly approve the **entire** release PR. The automated Publication Safety Gate rejects generated HTML or public discovery files that do not match the approved artifacts. All homepage, feed and sitemap changes must be committed in the same publisher-approved release PR.
8. Merge only through branch protection that **requires Publication Safety Gate**, restricts direct pushes and restricts or prohibits bypass. No GitHub account settings have been changed by this repository work.

**Security limitation:** The JSON file is not an identity verification mechanism. Someone with repository write access could forge it. Enforce protected branches, restricted write permissions and publisher-controlled pull-request approval before enabling an automated deployment. Never expose GitHub tokens in public GitHub Pages or browser localStorage.

**Current status:** Editorial article drafts have no publisher approval. The scripts are not wired into unattended research or live publishing. GitHub Pages hosting is not a private approval environment; browser-local review does not authenticate the publisher.

**Current limits:** The renderer is intentionally simple and deterministic rather than a fully fledged Markdown engine. It supports headings, paragraphs, lists, emphasis and HTTPS links; intricate tables, images, footnotes and typography need a separately tested rendering upgrade. Editorial review should remove internal research logs and notes before approval; the renderer also omits known internal note sections. The approval JSON supplies the published date; it is not a cryptographic signature.


## Shared editorial outcomes in Review Studio

The connected Studio can record `revisions_requested` or `editorial_text_reviewed` in `editorial/decisions/<slug>.json`. Notes are shared repository content; do not put private customer information in them. The Contents API commit records the event and exact manuscript blob SHA. Studio checks that the displayed text equals the saved draft and rereads the decision after committing it. Concurrent decision writes conflict instead of replacing history. A draft change during the operation is explicitly reported; prior reviews remain bound to the prior revision.

Opening the same article on another connected device reads its shared review history. The existing Contents read/write permission is sufficient; no new Issues permission is needed. Credentials remain in memory only. These outcomes never create `editorial/approvals` records, mark technical review complete or authorize publication. A GitHub commit is the audit trail; the client timestamp or free-text notes are not independent identity or technical certification.

Actual authenticated browser/device acceptance remains outstanding; controlled-transport tests verify the new path without creating real founder decisions.
