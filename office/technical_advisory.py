#!/usr/bin/env python3
"""Generate specialist review assignments; does not perform engineering review."""
import json
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def make_review(article,config):
    text=" ".join([article.get("working_title",""),article.get("desk","")]).lower()
    chosen=["chief","methods"]
    signals={"mechanical":("mount","vibration","blade","motor","structural"),
             "electrical":("vfd","inverter","electrical","voltage","wiring"),
             "airflow":("hvls","airflow","ventilation","thermal","destratification"),
             "automation":("control","sensor","bms","bacnet","modbus","ai "),
             "safety":("osha","lift","fire","safety","sprinkler","mewp"),
             "field":("install","service","commission","lift","repair")}
    for role,words in signals.items():
        if any(word in text for word in words):chosen.append(role)
    roles={r["id"]:r for r in config["roles"]}
    return {"article_title":article.get("working_title",""),
            "status":"review_not_performed","specialists":[{"role":roles[k]["name"],
            "checklist":roles[k]["checks"],"reviewer_findings":None,"approved":False} for k in chosen],
            "engineering_claims_verified":False,"publisher_approval":False}
def main():
    config=json.loads((ROOT/"office"/"technical-advisory.json").read_text())
    source=json.loads((ROOT/"office"/"editorial-latest.json").read_text())
    report={"schema_version":1,"status":"specialist_review_assignments_not_completed_reviews",
            "assignments":[make_review(b,config) for b in source.get("briefs",[])[:30]]}
    path=ROOT/"office"/"reports"/"technical-review-assignments.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2)+"\n")
    print("Technical specialist assignments:",len(report["assignments"]))
if __name__=="__main__":main()
