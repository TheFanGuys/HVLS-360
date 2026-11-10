#!/usr/bin/env python3
"""Create editorial assignment briefs from research leads; NEVER fabricate articles."""
import datetime as dt
import json
import pathlib
import re
from urllib.parse import urlparse
import research_director

ROOT=pathlib.Path(__file__).resolve().parents[1]
def make_briefs(data, limit=12):
    rows=research_director.audit(data)
    result=[]
    for row in rows:
        if row["triage"]!="review":continue
        title=row["title"].strip()
        url=row["url"]
        if not title or not url.startswith("https://"):continue
        # A headline is a research lead, not an independently substantiated story.
        result.append({
          "id":"lead-"+str(len(result)+1).zfill(3),
          "working_title":title[:180],
          "desk":row["department"],
          "lead_url":url,
          "status":"research_required",
          "us_relevance":"unverified",
          "source_verification":"pending",
          "technical_review":"pending",
          "image_rights_review":"pending",
          "editorial_review":"pending",
          "publisher_approval":"not_requested",
          "assignment_questions":[
            "Find the original primary source, publication date and author.",
            "What changed and why does it matter to U.S. installers or facilities?",
            "Which technical claims can be supported with original documentation?",
            "Are there limitations, commercial interests or contradictory evidence?",
            "What would an HVLS field technician or facility manager do differently?"
          ],
          "notes":row["notes"]
        })
        if len(result)>=limit:break
    return result
def main():
    source=json.loads((ROOT/"office"/"research-latest.json").read_text(encoding="utf-8"))
    briefs=make_briefs(source)
    payload={"schema_version":1,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
      "status":"assignment_briefs_only_not_articles",
      "editorial_policy":"No drafting of factual claims without source verification; no publication without explicit publisher approval.",
      "briefs":briefs}
    target=ROOT/"office"/"reports"/"editorial-assignments.json"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    public={"schema_version":1,"generated_at":payload["generated_at"],"status":"unverified_assignment_briefs_not_articles","briefs":briefs}
    (ROOT/"office"/"editorial-latest.json").write_text(json.dumps(public,ensure_ascii=False,indent=2)+chr(10),encoding="utf-8")
    print("Editorial assignment briefs prepared:",len(briefs))
if __name__=="__main__":main()
