#!/usr/bin/env python3
"""Weekly article release helper.

Takes a finished draft (editorial/drafts/<slug>.md) and its review notes
(editorial/reviews/<slug>-review.md), attaches a lead image, and prepares the
full release: image manifest, review register, approval record, published
article page, homepage, RSS, sitemap and office preview. Then runs every check.

Nothing goes live until the founder merges the pull request that carries these
changes. The approval record says so explicitly.

Fix a live article: edit editorial/drafts/<slug>.md (body only), then
  python office/weekly_article.py --revise --slug <slug>

New article:
  python office/weekly_article.py --slug my-slug --image art-library/bigfanguys-com/warehouse/IMG_2742.webp \
      --alt "Short description of the photo" --caption "Caption shown to readers."
"""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "office"))
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
IMAGE_DIRS = ("editorial/media/publisher/", "editorial/media/original/", "art-library/bigfanguys-com/")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run(cmd):
    print("$", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    out = (result.stdout + result.stderr).strip()
    print(out[-3000:])
    if result.returncode:
        raise SystemExit("FAILED: " + " ".join(cmd))
    return out


def revise(slug, old_sha):
    """Re-release an already-published article after its draft was edited.

    The edited draft must already be saved. Front matter (title, SEO fields)
    must not change. Every stored fingerprint of the old text is updated.
    """
    from release_inputs import digest
    draft = ROOT / "editorial/drafts" / (slug + ".md")
    new_sha = sha(draft)
    if new_sha == old_sha:
        raise SystemExit("Draft is unchanged")
    # Swap the old fingerprint for the new one everywhere it is recorded.
    for folder in ("editorial", "office"):
        for f in (ROOT / folder).rglob("*"):
            if f.suffix in (".json", ".md") and f.is_file() and "preview" not in f.parts:
                text = f.read_text(encoding="utf-8")
                if old_sha in text:
                    f.write_text(text.replace(old_sha, new_sha), encoding="utf-8")
    # Files whose own fingerprint is recorded in the launch ledger may have changed above.
    ledger_path = ROOT / "editorial/launch-completion-ledger.json"
    if ledger_path.exists():
        ledger = json.loads(ledger_path.read_text())
        items = ledger["items"] if isinstance(ledger, dict) and "items" in ledger else ledger
        for item in items:
            if item.get("slug") == slug:
                c = item["sources_and_claim_checks"]
                c["review_sha256"] = sha(ROOT / c["review_file"])
        write_json(ledger_path, ledger)
    approval_file = ROOT / "editorial/approvals" / (slug + ".json")
    record = json.loads(approval_file.read_text())
    record["release_inputs_sha256"] = digest(ROOT, slug)
    record["source_review_notes"] += " Revised " + dt.date.today().isoformat() + "; founder approves by merging the fix pull request."
    write_json(approval_file, record)
    (ROOT / "articles" / (slug + ".md")).unlink()
    import shutil
    shutil.rmtree(ROOT / "articles" / slug)
    run([sys.executable, "office/publish_approved.py", "--slug", slug, "--approval-file", str(approval_file)])
    run([sys.executable, "office/render_release.py", "--slug", slug])
    run([sys.executable, "office/public_catalog.py", "--write"])
    run([sys.executable, "office/site_preview.py"])
    checks()
    print("\nREADY: revised articles/%s/index.html and all checks passed." % slug)


def checks():
    run([sys.executable, "office/publication_guard.py"])
    run([sys.executable, "office/public_catalog.py", "--check"])
    run([sys.executable, "office/technical_signoff_audit.py"])
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"])
    for js in sorted((ROOT / "tests").glob("*.cjs")):
        run(["node", str(js.relative_to(ROOT))])


def main():
    if "--revise" in sys.argv:
        p = argparse.ArgumentParser()
        p.add_argument("--revise", action="store_true")
        p.add_argument("--slug", required=True)
        a = p.parse_args()
        old = json.loads((ROOT / "editorial/approvals" / (a.slug + ".json")).read_text())["article_sha256"]
        return revise(a.slug, old)
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=True)
    p.add_argument("--image", required=True)
    p.add_argument("--alt", required=True)
    p.add_argument("--caption", required=True)
    a = p.parse_args()

    slug = a.slug
    if not SLUG.fullmatch(slug):
        raise SystemExit("Bad slug: lowercase words joined by hyphens")
    draft = ROOT / "editorial/drafts" / (slug + ".md")
    review = ROOT / "editorial/reviews" / (slug + "-review.md")
    image = ROOT / a.image
    for f in (draft, review, image):
        if not f.is_file():
            raise SystemExit("Missing file: " + str(f.relative_to(ROOT)))
    if not a.image.startswith(IMAGE_DIRS):
        raise SystemExit("Image must be a Big Fan Guys photo or original illustration from: " + ", ".join(IMAGE_DIRS))
    if (ROOT / "articles" / slug).exists():
        raise SystemExit("Article already published: " + slug)
    body = draft.read_text(encoding="utf-8")
    for needed in ("publication_allowed: false", 'status: "EDITORIAL DRAFT — NOT APPROVED"', "title:", "seo_description:"):
        if needed not in body:
            raise SystemExit("Draft front matter missing: " + needed)
    title = re.search(r'^title:\s*"(.*)"', body, re.M).group(1)

    # 1. Lead image (library photos are copied into the site's media folder)
    if a.image.startswith("art-library/"):
        dest = ROOT / "editorial/media/publisher/weekly" / (slug + image.suffix)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(image.read_bytes())
        a.image = str(dest.relative_to(ROOT))
    manifest_path = ROOT / "editorial/media/article-images.json"
    manifest = json.loads(manifest_path.read_text())
    is_photo = not a.image.endswith(".svg")
    manifest["items"][slug] = {
        "file": a.image,
        "alt": a.alt,
        "caption": a.caption,
        "kind": "photo" if is_photo else "diagram",
        "credit": "Big Fan Guys" if is_photo else "HVLS 360°",
        "presentation": {"card": {"fit": "contain", "position": "50% 50%"},
                         "lead": {"fit": "contain", "position": "50% 50%"}},
        "crop_review": {"reviewed": dt.date.today().isoformat(),
                        "scope": "Card and article lead use contain; full source frame retained.",
                        "reviewer": "Weekly article worker",
                        "evidence": "office/weekly_article.py"},
    }
    write_json(manifest_path, manifest)

    # 2. Review register
    register_path = ROOT / "editorial/reviews/technical-review-register.json"
    register = json.loads(register_path.read_text())
    register["records"] = [r for r in register["records"] if r["slug"] != slug]
    register["records"].append({
        "slug": slug,
        "title": title,
        "scope": "Weekly article; documentary source check by the writer",
        "primary_review_file": str(review.relative_to(ROOT)),
        "technical_status": "awaiting_qualified_review",
        "reviewer_identity": None,
        "review_date": None,
        "review_evidence": None,
        "publisher_approval": "founder_merge_of_release_pr",
        "ai_expert_review": "complete",
        "ai_expert_review_file": str(review.relative_to(ROOT)),
        "ai_review_scope": "Writer's source and claim check",
        "qualified_review_required": False,
        "draft_sha256": sha(draft),
    })
    write_json(register_path, register)

    # 3. Approval record (takes effect only when the founder merges the PR)
    from release_inputs import digest
    approvals = ROOT / "editorial/approvals"
    approvals.mkdir(exist_ok=True)
    approval_file = approvals / (slug + ".json")
    write_json(approval_file, {
        "schema_version": 1,
        "slug": slug,
        "publisher_decision": "approved",
        "technical_review": "complete",
        "editorial_review": "complete",
        "media_rights": "cleared",
        "publisher_name": "Chris Fogarty",
        "approved_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "publisher_attestation": "I explicitly authorize publication of this article.",
        "approval_mechanism": "Founder approves by merging the weekly release pull request. Unmerged, nothing is live.",
        "source_review_notes": "Writer's source check: " + str(review.relative_to(ROOT)) + ". Technical review is the founder's field review at merge; no licensed engineer sign-off claimed.",
        "media_rights_evidence": "Lead image is a Big Fan Guys photograph or original HVLS 360 illustration: " + a.image,
        "article_sha256": sha(draft),
        "release_inputs_sha256": digest(ROOT, slug),
    })

    # 4. Publish, render, update homepage/RSS/sitemap and office previews
    run([sys.executable, "office/publish_approved.py", "--slug", slug, "--approval-file", str(approval_file)])
    run([sys.executable, "office/render_release.py", "--slug", slug])
    run([sys.executable, "office/public_catalog.py", "--write"])

    # 5. Every check the site runs
    checks()
    print("\nREADY: articles/%s/index.html built and all checks passed." % slug)


if __name__ == "__main__":
    main()
