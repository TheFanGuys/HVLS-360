#!/usr/bin/env python3
"""Route unverified leads to specialist work queues; never claim agents executed."""
import datetime as dt
import json
import pathlib
import re
ROOT=pathlib.Path(__file__).resolve().parents[1]
OFFICE=ROOT/"office"
HVLS=re.compile(r"\b(hvls|high.volume.low.speed|large.diameter fan|ceiling fan|destratification|industrial ventilation|air movement|airflow|vfd|variable.frequency drive|fan control|abb drive|fire.alarm interlock|fan efficiency|cfei)\b",re.I)
SAFETY=re.compile(r"\b(osha|safety|fire|code|nec|nfpa|structural|load|mount|fall protection)\b",re.I)
PRODUCT=re.compile(r"\b(fan|vfd|drive|controller|motor|airflow|product|launch|series)\b",re.I)
def route(briefs):
    tasks=[];rejected=[]
    for item in briefs:
        title=str(item.get("working_title","")).strip()
        identifier=str(item.get("id",""))
        if not title or not identifier:continue
        if not HVLS.search(title):
            rejected.append({"id":identifier,"reason":"no_explicit_hvls_or_ventilation_signal","title":title[:180]})
            continue
        base={"lead_id":identifier,"title":title[:180],"source_url":item.get("lead_url"),"status":"queued_not_executed","source_verification":"required"}
        stages=[
            ("Research","Original Source Checker","Find primary publisher, publication date, original documents and independent corroboration."),
            ("Editorial","Assignment Editor","Confirm newsworthiness, U.S. field relevance, and a distinct trade-journal angle."),
            ("Experts","Electrical & HVAC Reviewer","Check model-specific technical claims, electrical/control constraints and applicable standards."),
            ("Media & Art","Visual Researcher","Request only correctly identified visuals with documented permission."),
            ("SEO & Distribution","SEO Editor","Draft metadata and search-intent notes; do not distribute before approval.")
        ]
        for i,(department,owner,instruction) in enumerate(stages):
            if department=="Experts" and not (PRODUCT.search(title) or SAFETY.search(title)):continue
            tasks.append({**base,"id":identifier+"-"+str(i+1),"department":department,"owner_role":owner,"instruction":instruction,"depends_on":None if i==0 else identifier+"-1","approval":"not_requested"})
    return {"schema_version":1,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),"status":"routing_packets_not_agent_execution","assignments":tasks,"rejected_leads":rejected,"publisher_approval":"required_for_publication","auto_publish":False}
def main():
    source=json.loads((OFFICE/"editorial-latest.json").read_text(encoding="utf-8"))
    output=route(source.get("briefs",[]))
    path=OFFICE/"reports"/"coo-routing-latest.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("COO routed",len(output["assignments"]),"task packets; filtered",len(output["rejected_leads"]),"unrelated leads; no agents executed")
if __name__=="__main__":main()
