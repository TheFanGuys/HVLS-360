# HVLS 360° — Publisher approval protocol

**This feature does not publish automatically.** It is a guarded artifact-preparation script for a future release workflow.

1. Technical and editorial reviewers must finish their work. All source and media-rights evidence must be documented. Manufacturer-hosted photos are not automatically licensed.
2. The publisher must review the **exact** final article and explicitly approve it, ideally through a GitHub protected-branch pull-request review by the authorized repository owner.
3. A maintainer creates an approval JSON in `editorial/approvals/<slug>.json` containing the required review fields, a SHA-256 digest of the exact draft bytes, source review notes, media permission evidence, publisher name, timestamp and the literal attestation `I explicitly authorize publication of this article.`
4. The maintainer runs `python office/publish_approved.py --slug <slug> --approval-file editorial/approvals/<slug>.json` in a reviewed publication branch, then reviews the resulting `articles/<slug>.md` and merges via the protected release process.

**Security limitation:** The JSON file is not an identity verification mechanism. Someone with repository write access could forge it. Enforce protected branches, restricted write permissions and publisher-controlled pull-request approval before enabling an automated deployment. Never expose GitHub tokens in public GitHub Pages or browser localStorage.

**Current status:** The first article has no publisher approval and no cleared image rights. It must not be published. The script is not wired into the research workflow or site navigation.
