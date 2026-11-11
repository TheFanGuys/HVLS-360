#!/usr/bin/env python3
"""Fail-closed independent technical signoff inventory. Does not approve articles."""
import json
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
  if record["technical_status"]=="complete" and not all(record.get(k) for k in ("reviewer_identity","review_date","review_evidence")):
   errors.append("unsubstantiated technical completion: "+slug)
  if record["technical_status"] not in ("awaiting_qualified_review","complete"):
   errors.append("unknown review status: "+slug)
 if seen!=drafts:errors.append("review coverage mismatch: "+", ".join(sorted(seen^drafts)))
 return {"articles":len(records),"technical_signoffs":sum(r["technical_status"]=="complete" for r in records),"errors":errors}
if __name__=="__main__":
 result=audit()
 print(json.dumps(result,indent=2))
 if result["errors"]:raise SystemExit(1)
