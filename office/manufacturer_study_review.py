#!/usr/bin/env python3
"""Create transparent manufacturer-study review assignments from candidate URLs."""
import datetime as dt
import json
import pathlib
from urllib.parse import urlparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
FIELDS=("study_title","author","publication_date","manufacturer_or_sponsor","funding_disclosure",
        "test_standard","study_design","sample_size","test_conditions","fan_models",
        "baseline_comparator","reported_results","limitations","independent_replication",
        "us_market_applicability","installer_implications")
def review_records(discovery,max_items=60):
    records=[]
    for source in discovery.get("sources",[]):
        for url in source.get("candidate_urls",[]):
            if len(records)>=max_items:return records
            if urlparse(url).scheme!="https":continue
            records.append({"manufacturer":source.get("source",""),"source_url":url,
                "status":"document_not_reviewed","document_type":"unknown",
                "evidence":{k:None for k in FIELDS},
                "verification_questions":[
                    "Is this an actual study, marketing page, case study, or application note?",
                    "Is the complete original document accessible and legally usable?",
                    "Are test methods, measured outcomes, conditions and limitations documented?",
                    "Are findings relevant to U.S. facilities and HVLS installations?",
                    "Can the findings be independently corroborated?"
                ],"publisher_approval":"not_requested"})
    return records
def main():
    source=ROOT/"office"/"reports"/"manufacturer-research-candidates.json"
    discovery=json.loads(source.read_text(encoding="utf-8"))
    report={"schema_version":1,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
        "status":"research_review_assignments_not_verified_studies",
        "disclaimer":"Candidate URLs and blank evidence fields; no studies were read, validated or summarized.",
        "reviews":review_records(discovery)}
    out=ROOT/"office"/"reports"/"manufacturer-study-reviews.json"
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Manufacturer study review assignments:",len(report["reviews"]))
if __name__=="__main__":main()
