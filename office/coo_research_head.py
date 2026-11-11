#!/usr/bin/env python3
"""Head of Research: audit source-checker reports and issue actionable decisions.

This is deterministic triage, not an autonomous AI researcher or factual signoff.
"""
import datetime as dt
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/"office"/"reports"

def decide(audit, routing, now=None):
    now=now or dt.datetime.now(dt.timezone.utc)
    by_id={r.get("lead_id"):r for r in audit.get("results",[])}
    leads={}
    for task in routing.get("assignments",[]):
        lid=task.get("lead_id")
        if lid and lid not in leads:leads[lid]=task
    decisions=[]
    for lid,lead in leads.items():
        source=by_id.get(lid)
        if not source:
            state="blocked_missing_source_audit"
            reason="Source Checker report missing; do not advance downstream work"
            owner="Original Source Checker"
        elif source.get("status")=="blocked_needs_original_source":
            state="hold_original_source"
            reason="No original publisher candidate; investigate original reporting and date"
            owner="Original Source Checker"
        elif source.get("status")=="candidate_found_requires_human_verification":
            state="research_followup"
            reason="Publisher candidate identified but author, date and claims remain unverified"
            owner="Evidence Researcher"
        else:
            state="hold_unrecognized_evidence"
            reason="Unexpected source status; manual Research Head review required"
            owner="Head of Research"
        decisions.append({"lead_id":lid,"title":lead.get("title",""),"decision":state,
            "rationale":reason,"assigned_role":owner,
            "source_candidate":source.get("publisher_candidate") if source else None,
            "outstanding_checks":source.get("blockers",[]) if source else ["Source audit missing"],
            "editorial_handoff":"blocked_pending_verified_primary_evidence",
            "editorial_approval":False,"publication_allowed":False})
    return {"schema_version":1,"generated_at":now.isoformat(),
        "status":"research_head_triage_completed_evidence_unverified",
        "decisions":decisions,
        "counts":{"leads_reviewed":len(decisions),
                  "needs_original":sum(x["decision"]=="hold_original_source" for x in decisions),
                  "needs_evidence":sum(x["decision"]=="research_followup" for x in decisions),
                  "missing_audit":sum(x["decision"]=="blocked_missing_source_audit" for x in decisions)},
        "policy":"No lead advances to the Managing Editor until original-source and claim verification is recorded.",
        "publication_allowed":False}

def main():
    routing=json.loads((REPORTS/"coo-routing-latest.json").read_text(encoding="utf-8"))
    source=json.loads((REPORTS/"coo-source-audit.json").read_text(encoding="utf-8"))
    out=decide(source,routing)
    (REPORTS/"coo-research-head-decisions.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Research Head reviewed",out["counts"]["leads_reviewed"],"leads; none editorially verified")
if __name__=="__main__":main()
