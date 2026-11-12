#!/usr/bin/env python3
"""Revision-bound documentary review and independent signoff inventory. Does not approve articles."""
import json
import hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTER=ROOT/"editorial/reviews/technical-review-register.json"
def audit(root=ROOT):
 data=json.loads((root/"editorial/reviews/technical-review-register.json").read_text())
 drafts={p.stem for p in (root/"editorial/drafts").glob("*.md")}
 records=data["records"]
 seen=set()
 errors=[]
 for record in records:
  slug=record["slug"]
  if slug in seen:errors.append("duplicate review: "+slug)
  seen.add(slug)
  if not (root/record["primary_review_file"]).is_file():
   errors.append("missing review: "+slug)
  if record.get("ai_expert_review")=="complete":
   ai_file=root/record.get("ai_expert_review_file","")
   if not ai_file.is_file():errors.append("missing AI expert review: "+slug)
  if record["technical_status"]=="complete" and not all(record.get(k) for k in ("reviewer_identity","review_date","review_evidence")):
   errors.append("unsubstantiated technical completion: "+slug)
  if record["technical_status"]=="documentary_review_complete":
   # Documentary reporting is a different finding from professional signoff.
   # Bind it to the precise manuscript and an explicit claim-level resolution.
   try:
    evidence_path=(root/record["claim_resolution_file"]).resolve()
    if not evidence_path.is_relative_to(root.resolve()):raise ValueError("unsafe evidence path")
    evidence=json.loads(evidence_path.read_text())
    matches=[r for r in evidence["records"] if r["slug"]==slug]
    revision=hashlib.sha256((root/"editorial/drafts"/(slug+".md")).read_bytes()).hexdigest()
    if len(matches)!=1:raise ValueError("missing or duplicate resolution")
    finding=matches[0]
    if finding["draft_sha256"]!=revision or record.get("draft_sha256")!=revision:
     raise ValueError("stale manuscript")
    if finding["disposition"]!="documentary_review_complete" or not finding.get("claim_groups"):
     raise ValueError("unresolved documentary evidence")
    if finding.get("qualified_review_required") is not False or record.get("qualified_review_required") is not False:
     raise ValueError("qualified review required")
   except (KeyError,ValueError,OSError,TypeError) as error:
    errors.append("unsubstantiated documentary review: "+slug+" ("+str(error)+")")
  if record["technical_status"] not in ("awaiting_qualified_review","complete","documentary_review_complete"):
   errors.append("unknown review status: "+slug)
 if seen!=drafts:errors.append("review coverage mismatch: "+", ".join(sorted(seen^drafts)))
 return {"articles":len(records),"technical_signoffs":sum(r["technical_status"]=="complete" for r in records),"documentary_reviews":sum(r["technical_status"]=="documentary_review_complete" for r in records),"ai_expert_reviews":sum(r.get("ai_expert_review")=="complete" for r in records),"errors":errors}
if __name__=="__main__":
 result=audit()
 print(json.dumps(result,indent=2))
 if result["errors"]:raise SystemExit(1)
