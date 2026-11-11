#!/usr/bin/env python3
"""COO status synthesis from sanitized research indexes; no LLM or publishing."""
import datetime as dt
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OFFICE=ROOT/"office"

def load(name):
    path=OFFICE/name
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def build(now=None):
    now=now or dt.datetime.now(dt.timezone.utc)
    research=load("research-latest.json")
    editorial=load("editorial-latest.json")
    media=load("media-latest.json")
    departments=research.get("departments",[])
    leads=sum(len(x.get("leads",[])) for x in departments)
    briefs=editorial.get("briefs",[])
    media_requests=media.get("requests",[])
    errors=research.get("errors",[])
    intake=load("reports/coo-issues-sync.json")
    discovery=load("reports/manufacturer-research-candidates.json")
    discovery_errors=discovery.get("errors",[])
    discovery_missing=not discovery.get("generated_at")
    warnings=["Research headlines and dates are unverified until original sources are checked.","No autonomous LLM agents or publisher approval are executed by this report.","This public JSON contains no unpublished article text or private review notes."]
    if discovery_missing:
        warnings.append("Manufacturer discovery report unavailable; coverage is unverified.")
    elif discovery_errors:
        warnings.append(f"Manufacturer discovery has {len(discovery_errors)} sitemap failures; fallback URLs do not establish complete source coverage.")
    approvals=len(list((ROOT/"editorial"/"approvals").glob("*.json"))) if (ROOT/"editorial"/"approvals").exists() else 0
    published=len(list((ROOT/"articles").glob("*.md"))) if (ROOT/"articles").exists() else 0
    # Only public status counts and generic operational assignments; no draft bodies.
    assignments=[
        {"id":"coo-research","department":"Research","owner":"Head of Research","status":"needs_review" if leads else "blocked","task":"Screen recent research leads and verify original sources","count":leads},
        {"id":"coo-editorial","department":"Editorial","owner":"Managing Editor","status":"needs_review" if briefs else "waiting","task":"Triage research briefs for relevance and assign evidence work","count":len(briefs)},
        {"id":"coo-media","department":"Media & Art","owner":"Head of Media & Art","status":"needs_review" if media_requests else "waiting","task":"Clear image rights, model identity and article-specific media requests","count":len(media_requests)},
        {"id":"coo-experts","department":"Technical Experts","owner":"Head of Experts","status":"waiting","task":"Verify technical claims against primary documentation and flag human signoff needs","count":0},
        {"id":"coo-seo","department":"SEO & Distribution","owner":"Head of SEO","status":"waiting","task":"Prepare search intent and distribution checks for publisher-approved articles","count":0},
        {"id":"coo-marketing","department":"Marketing & Growth","owner":"Head of Marketing","status":"waiting","task":"Prepare newsletter and industry outreach plan; do not send automatically","count":0},
        {"id":"coo-publisher","department":"Publisher","owner":"Publisher","status":"awaiting_approval","task":"Review unpublished drafts; release requires explicit publisher approval","count":max(0,len(list((ROOT/"editorial"/"drafts").glob("*.md")))-published)}
    ]
    return {"schema_version":1,"shared_issue_sync":{key:intake.get(key) for key in ("status","issues_created","eligible_candidates","run_id","deduplication_check")},"generated_at":now.isoformat(),"status":"automated_operational_brief_not_autonomous_agent","research_generated_at":research.get("generated_at"),"metrics":{"research_leads":leads,"editorial_briefs":len(briefs),"media_requests":len(media_requests),"source_errors":len(errors)+len(discovery_errors),"manufacturer_source_errors":None if discovery_missing else len(discovery_errors),"approval_records":approvals,"published_articles":published},"assignments":assignments,"manufacturer_discovery_generated_at":discovery.get("generated_at"),"warnings":warnings,"publication_allowed":False}

def main():
    result=build()
    (OFFICE/"coo-latest.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("COO operational brief:",result["metrics"])
if __name__=="__main__":
    main()
