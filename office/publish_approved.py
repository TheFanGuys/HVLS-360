#!/usr/bin/env python3
"""Fail-closed HVLS 360 article publisher. Only runs on explicit CLI invocation.

Approval is a repository-maintainer action, not a checkbox in public Pages.
No automation invokes this script. It never approves an article.
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
SLUG=re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
def publish(slug,approval_path,root=ROOT):
    if not SLUG.fullmatch(slug):
        raise ValueError("Invalid article slug")
    draft=root/"editorial"/"drafts"/(slug+".md")
    if not draft.is_file():
        raise ValueError("Draft not found")
    body=draft.read_text(encoding="utf-8")
    if "publication_allowed: false" not in body:
        raise ValueError("Draft must remain explicitly unpublished")
    approval_file=pathlib.Path(approval_path).resolve()
    allowed_dir=(root/"editorial"/"approvals").resolve()
    if approval_file.parent!=allowed_dir or approval_file.name!=slug+".json":
        raise ValueError("Approval file must be stored in editorial/approvals under matching slug")
    approval=json.loads(approval_file.read_text(encoding="utf-8"))
    expected={"schema_version":1,"slug":slug,"publisher_decision":"approved",
        "technical_review":"complete","editorial_review":"complete","media_rights":"cleared"}
    for k,v in expected.items():
        if approval.get(k)!=v:
            raise ValueError("Publication blocked: missing "+k)
    if not approval.get("publisher_name") or not approval.get("approved_at_utc"):
        raise ValueError("Publication blocked: publisher identity and timestamp required")
    # The approval record must be authored/reviewed by the publisher in GitHub;
    # these fields are gates, not cryptographic authentication.
    if not approval.get("publisher_attestation")=="I explicitly authorize publication of this article.":
        raise ValueError("Explicit publisher attestation required")
    if not approval.get("source_review_notes") or not approval.get("media_rights_evidence"):
        raise ValueError("Source review and media permission evidence required")
    if not approval.get("article_sha256"):
        raise ValueError("Draft checksum required")
    import hashlib
    digest=hashlib.sha256(body.encode("utf-8")).hexdigest()
    if approval["article_sha256"]!=digest:
        raise ValueError("Article changed after approval")
    output=root/"articles"/(slug+".md")
    if output.exists():
        raise ValueError("Article already published; revisions require separate review")
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(body.replace("publication_allowed: false","publication_allowed: true",1)
        .replace('status: "EDITORIAL DRAFT — NOT APPROVED"','status: "APPROVED FOR PUBLICATION"',1),encoding="utf-8")
    return output
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--slug",required=True)
    p.add_argument("--approval-file",required=True)
    a=p.parse_args()
    try:print("Publication artifact prepared:",publish(a.slug,a.approval_file))
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print("BLOCKED:",exc,file=sys.stderr);sys.exit(1)
if __name__=="__main__":main()
