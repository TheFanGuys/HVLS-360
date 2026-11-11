#!/usr/bin/env python3
"""Reconcile Evidence Researcher findings into Head of Research decisions.

Generates a private Managing Editor intake register. This does NOT fact-check
technical claims, promote unverified leads, or publish manuscripts.
"""
import datetime as dt
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/"office"/"reports"

def reconcile(head, evidence, now=None):
    findings={r.get("lead_id"):r for r in evidence.get("results",[]) if r.get("lead_id")}
    rows=[]
    for decision in head.get("decisions",[]):
        lead_id=decision.get("lead_id")
        if not lead_id:continue
        result=findings.get(lead_id)
        observed=(result or {}).get("evidence",{})
        if decision.get("decision")=="hold_original_source":
            disposition="hold_find_original_publisher"
            owner="Original Source Checker"
        elif decision.get("decision")=="research_followup" and not result:
            disposition="hold_evidence_research_not_run"
            owner="Evidence Researcher"
        elif result and observed.get("status")=="metadata_extracted_unverified":
            disposition="hold_verify_metadata_and_technical_claims"
            owner="Head of Research"
        else:
            disposition="hold_incomplete_or_inconclusive_evidence"
            owner="Evidence Researcher"
        rows.append({
            "lead_id":lead_id,
            "working_title":decision.get("title",""),
            "research_disposition":disposition,
            "next_owner":owner,
            "publisher_candidate":(result or {}).get("publisher_candidate") or decision.get("source_candidate"),
            "reported_title":observed.get("page_title"),
            "reported_author":observed.get("reported_author"),
            "reported_publication_date":observed.get("reported_date"),
            "reported_metadata_is_verified":False,
            "technical_claims_verified":False,
            "independent_corroboration":False,
            "editorial_intake":"research_hold",
            "editorial_action":"Do not assign a reported feature until primary documents and claims are checked",
            "publisher_approval":"not_requested",
            "publication_allowed":False
        })
    return {
        "schema_version":1,
        "generated_at":(now or dt.datetime.now(dt.timezone.utc)).isoformat(),
        "status":"research_head_reconciliation_and_managing_editor_intake",
        "lead_count":len(rows),
        "editorial_ready":0,
        "research_holds":len(rows),
        "items":rows,
        "disclaimer":"Publisher metadata is self-reported. No technical claims or article drafts have been approved.",
        "publication_allowed":False
    }

def main():
    head=json.loads((REPORTS/"coo-research-head-decisions.json").read_text(encoding="utf-8"))
    evidence=json.loads((REPORTS/"coo-evidence-research.json").read_text(encoding="utf-8"))
    out=reconcile(head,evidence)
    (REPORTS/"coo-managing-editor-intake.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Managing Editor intake:",out["lead_count"],"leads;",out["research_holds"],"held pending verification")
if __name__=="__main__":main()
