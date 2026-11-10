#!/usr/bin/env python3
"""Conservative research triage; heuristic flags are NOT factual verification."""
import json
import pathlib
import re
from urllib.parse import urlparse

ROOT=pathlib.Path(__file__).resolve().parents[1]
BAD=("market size","market forecast","market to 2035","market to 2033","market report",
     "market growth","market share report","supermarket fridges","cryptocurrency",
     "stock price","market research report")
FIELD=("hvls","large diameter fan","industrial ceiling fan","scissor lift","boom lift",
       "aerial lift","mewp","equipment rental","warehouse construction","industrial ventilation",
       "destratification","fire sprinkler","industrial fan","manufacturing facility")
INTERNATIONAL=("european","europe","nigeria","kenya","india","china","czech","gombe","homa bay","nyandiwa","uk market","britain","germany","france")
USA=("united states","u.s.","usa","american","arizona","utah","texas","california",
     "ohio","florida","georgia","north america")
OFFICIAL=("osha.gov","amca.org","ashrae.org","nfpa.org","ul.com","icc-safe.org")
def triage(title,department,url):
    t=title.lower()
    host=urlparse(url).hostname or ""
    reasons=[]
    if any(k in t for k in INTERNATIONAL) and not any(k in t for k in USA):
        return "hold",["International story without demonstrated U.S. impact; editor may override with evidence"]
    if any(k in t for k in BAD):
        return "hold",["Generic market promotion or off-topic headline; requires editor review"]
    if not any(k in t for k in FIELD) and not any(k in department.lower() for k in ("lift","rental","construction")):
        return "hold",["No explicit HVLS or field relevance in headline"]
    if not any(k in t for k in USA):
        reasons.append("U.S. applicability not established from headline")
    if "news.google.com" in host:
        reasons.append("News aggregator URL; find and verify original publisher")
    if any(x in host for x in OFFICIAL):
        reasons.append("Official-looking source; verify exact page, date and applicability")
    return "review",reasons or ["Potential U.S. field relevance; verify primary source"]
def audit(data):
    rows=[]
    for dept in data.get("departments",[]):
        for lead in dept.get("leads",[]):
            status,reasons=triage(lead.get("title",""),dept.get("department",""),lead.get("url",""))
            rows.append({"department":dept.get("department",""),"title":lead.get("title",""),
                         "url":lead.get("url",""),"triage":status,"notes":reasons})
    return rows
def render(data,rows):
    review=[r for r in rows if r["triage"]=="review"]
    hold=[r for r in rows if r["triage"]=="hold"]
    out=["# HVLS 360 — Research Director Quality Audit","",
         "Run: "+str(data.get("generated_at","unknown")),"",
         "**Heuristic screening only. No lead has been fact-checked, verified as U.S.-applicable or approved as an article.**","",
         f"Collected: {len(rows)} | Further review: {len(review)} | Hold: {len(hold)}","",
         "## Candidates for primary-source verification"]
    for r in review:
        out += ["- "+r["title"],"  - Desk: "+r["department"],"  - Source: "+r["url"],
                "  - Checks: "+"; ".join(r["notes"])]
    out+=["","## Hold / low relevance"]
    for r in hold:
        out+=["- "+r["title"]+" — "+"; ".join(r["notes"])]
    out+=["","## Director's next actions","- Locate original manufacturer or authoritative source for each candidate",
          "- Seek U.S. application and exact publication date",
          "- Search Big Ass Fans and other manufacturers' studies and application libraries",
          "- Record research methodology, funding and limitations",
          "- Propose new sources and content angles for publisher review",
          "- Never auto-publish, auto-contact, or incur expense",""]
    return "\n".join(out)
def main():
    path=ROOT/"office"/"research-latest.json"
    data=json.loads(path.read_text(encoding="utf-8"))
    rows=audit(data)
    out=ROOT/"office"/"reports"/"research-director-latest.md"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(render(data,rows),encoding="utf-8")
    print(f"Research director audit: {len(rows)} leads, {sum(r['triage']=='review' for r in rows)} to review")
if __name__=="__main__":
    main()
