#!/usr/bin/env python3
"""Read-only release audit: fail if a published article lacks matching approval."""
import hashlib
import json
import pathlib
import re
import sys
from article_page import build_html

ROOT=pathlib.Path(__file__).resolve().parents[1]
SLUG=re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
def audit(root=ROOT):
    problems=[]
    articles=root/"articles"
    if not articles.exists():
        # A Markdown approval is not permission to bypass review with an arbitrary
    # static HTML page. Keep every new reader-facing article page byte-for-byte
    # reproducible from the corresponding approved Markdown and approval date.
    for page in sorted(articles.glob("*/index.html")):
        slug=page.parent.name
        if slug=="editorial-standards":
            continue  # Existing publisher policy page, not an article
        if not SLUG.fullmatch(slug) or not (articles/(slug+".md")).exists():
            problems.append(f"{slug}: orphan article HTML (no approved Markdown)")
            continue
        try:
            expected=build_html(root,slug)
            if page.read_text(encoding="utf-8")!=expected:
                problems.append(f"{slug}: article HTML differs from generated approved version")
        except (ValueError,OSError,KeyError,json.JSONDecodeError) as error:
            problems.append(f"{slug}: HTML cannot be verified ({error})")
    return problems
    for article in sorted(articles.glob("*.md")):
        slug=article.stem
        if not SLUG.fullmatch(slug):
            problems.append(f"{article.name}: invalid slug");continue
        approval=root/"editorial"/"approvals"/(slug+".json")
        draft=root/"editorial"/"drafts"/(slug+".md")
        if not approval.is_file() or not draft.is_file():
            problems.append(f"{slug}: missing draft or publisher approval");continue
        try:
            record=json.loads(approval.read_text(encoding="utf-8"))
            body=draft.read_text(encoding="utf-8")
            expected=body.replace("publication_allowed: false","publication_allowed: true",1).replace(
                'status: "EDITORIAL DRAFT — NOT APPROVED"','status: "APPROVED FOR PUBLICATION"',1)
            if article.read_text(encoding="utf-8")!=expected:
                problems.append(f"{slug}: published content differs from approved draft")
            for key,value in {"schema_version":1,"slug":slug,"publisher_decision":"approved",
                "technical_review":"complete","editorial_review":"complete","media_rights":"cleared",
                "publisher_attestation":"I explicitly authorize publication of this article."}.items():
                if record.get(key)!=value:
                    problems.append(f"{slug}: invalid {key}")
            for key in ("publisher_name","approved_at_utc","source_review_notes","media_rights_evidence"):
                if not record.get(key):
                    problems.append(f"{slug}: missing {key}")
            if record.get("article_sha256")!=hashlib.sha256(body.encode("utf-8")).hexdigest():
                problems.append(f"{slug}: draft checksum mismatch")
        except (OSError,ValueError,json.JSONDecodeError) as e:
            problems.append(f"{slug}: invalid approval data ({e})")
    return problems
if __name__=="__main__":
    errors=audit()
    if errors:
        for error in errors:print("PUBLICATION BLOCK:",error,file=sys.stderr)
        sys.exit(1)
    print("Publication guard passed: no unapproved article artifacts found.")
