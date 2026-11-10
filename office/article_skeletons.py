#!/usr/bin/env python3
"""Generate source-citation article SKELETONS; never invent research or finished articles."""
import datetime as dt
import json
import pathlib
import re
ROOT=pathlib.Path(__file__).resolve().parents[1]
def slug(s):
    return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")[:65] or "untitled"
def skeleton(brief):
    title=brief.get("working_title","Untitled assignment").strip()
    source=brief.get("lead_url","")
    if not source.startswith("https://"):raise ValueError("Valid HTTPS source link required")
    return {"working_title":title,"slug":slug(title),
        "status":"research_draft_skeleton_not_article",
        "publisher_approval":False,"ready_for_publication":False,
        "sections":[
            {"heading":"What changed","content":None,"evidence_required":"Original announcement or study"},
            {"heading":"Why it matters in the United States","content":None,"evidence_required":"Documented U.S. relevance"},
            {"heading":"Technical details and evidence","content":None,"evidence_required":"Manufacturer manual, test report or authoritative source"},
            {"heading":"Field implications","content":None,"evidence_required":"Verified installation, commissioning or service impact"},
            {"heading":"Limitations and unanswered questions","content":None,"evidence_required":"Methodology and contrary evidence"}
        ],
        "sources":[{"url":source,"status":"unverified","supports":[],"publisher":None,"date":None}],
        "review_gates":{"original_source_verified":False,"technical_review_complete":False,
                        "image_rights_cleared":False,"editorial_review_complete":False,
                        "publisher_approval":False}}
def generate(data,limit=12):
    result=[]
    for b in data.get("briefs",[])[:limit]:
        try:result.append(skeleton(b))
        except ValueError:continue
    return result
def main():
    d=json.loads((ROOT/"office"/"editorial-latest.json").read_text(encoding="utf-8"))
    drafts=generate(d)
    out={"schema_version":1,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
         "warning":"These are empty, unverified article structures, NOT written or publishable articles.",
         "drafts":drafts}
    path=ROOT/"office"/"reports"/"article-skeletons.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Article skeletons created:",len(drafts))
if __name__=="__main__":main()
