#!/usr/bin/env python3
"""Execute a bounded source-evidence audit for COO-routed research assignments.

Combines existing live source probes and original-publisher resolution.
Never equates a reachable URL or candidate canonical with verified reporting.
"""
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/"office"/"reports"

def read(path):
    try:return json.loads(path.read_text(encoding="utf-8"))
    except (OSError,ValueError):return {}

def audit(routing,preflight,originals,now=None):
    now=now or dt.datetime.now(dt.timezone.utc)
    by_url={x.get("lead_url"):x for x in preflight.get("sources",[]) if x.get("lead_url")}
    orig_by_url={x.get("lead_url"):x for x in originals.get("items",[]) if x.get("lead_url")}
    results=[]
    for task in routing.get("assignments",[]):
        if task.get("owner_role")!="Original Source Checker":continue
        url=task.get("source_url") or ""
        source=by_url.get(url,{})
        original=orig_by_url.get(url,{})
        probe=source.get("preflight",{})
        resolution=original.get("resolution",{})
        candidate=resolution.get("original_url")
        candidate_host=urlsplit(candidate).hostname if isinstance(candidate,str) else None
        unresolved=not candidate or candidate_host in ("news.google.com","www.google.com")
        blockers=[]
        if unresolved:blockers.append("Original publisher unresolved")
        if probe.get("status") not in ("reachable_unverified",):
            blockers.append("Source accessibility not established")
        blockers.extend(["Publication date and authorship not independently confirmed",
                         "Technical claims not checked against primary documentation"])
        results.append({
            "assignment_id":task["id"],"lead_id":task["lead_id"],"title":task["title"],
            "source_url":url,"publisher_candidate":candidate if not unresolved else None,
            "source_probe_status":probe.get("status","not_checked"),
            "publisher_resolution_status":resolution.get("status","not_checked"),
            "status":"blocked_needs_original_source" if unresolved else "candidate_found_requires_human_verification",
            "evidence_checks":{"url_reachability":"checked_not_factual_verification" if probe else "not_checked",
                "original_publisher":"candidate_only" if not unresolved else "unresolved",
                "publication_date":"unverified","technical_claims":"unverified","image_rights":"unverified"},
            "blockers":blockers,
            "next_owner":"Head of Research",
            "next_action":"Verify original article, author, date and relevant technical documents before handing to editor",
            "editorial_release_allowed":False
        })
    return {"schema_version":1,"generated_at":now.isoformat(),
        "status":"source_evidence_audit_executed_no_fact_verification",
        "completed_audits":len(results),
        "verified_articles":0,
        "results":results,
        "publication_allowed":False,
        "disclaimer":"Automated evidence checks are not independent verification of technical or editorial claims."}

def main():
    output=audit(read(REPORTS/"coo-routing-latest.json"),
        read(REPORTS/"source-preflight.json"),
        read(REPORTS/"original-source-candidates.json"))
    REPORTS.mkdir(parents=True,exist_ok=True)
    (REPORTS/"coo-source-audit.json").write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("COO Source Checker:",output["completed_audits"],"evidence audits;",output["verified_articles"],"verified articles")
if __name__=="__main__":main()
