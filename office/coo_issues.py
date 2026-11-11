#!/usr/bin/env python3
"""Create a deduplicated shared Managing Editor queue using GitHub Issues.

Only public-source lead metadata is sent to Issues. Never upload manuscripts,
private research, draft excerpts, internal expert notes, or approval tokens.
"""
import hashlib,json,os,re,sys
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request,urlopen
ROOT=Path(__file__).resolve().parents[1]
MAX_NEW=5

def eligible(brief):
    title=str(brief.get("working_title","")).strip()
    url=str(brief.get("lead_url","")).strip()
    if not title or not url.startswith("https://"):return False
    return bool(re.search(r"\b(HVLS|large.diameter fan|industrial ventilation|ceiling fan|destratification|air movement|airflow|VFD|fan controls|CFEI)\b",title,re.I))

def build_items(briefs):
    items=[]
    for b in briefs:
        if not eligible(b):continue
        key="lead-"+hashlib.sha256(str(b["lead_url"]).encode()).hexdigest()[:16]
        if not re.fullmatch(r"lead-[a-f0-9]{16}",key):continue
        items.append({"key":key,"title":str(b["working_title"])[:160],
            "source":str(b["lead_url"])[:1500],
            "body":f"""COO research intake — **unverified lead**.

Source lead: {key}
Working headline: {str(b['working_title'])[:160]}
Candidate link: {str(b['lead_url'])[:1500]}

**Assigned role:** Managing Editor / Head of Research
**Status:** Research hold — original source, date and technical claims not verified.

### Required handoffs
- [ ] Identify original publisher, date, author and primary documentation
- [ ] Check relevance to U.S. HVLS installers and facilities
- [ ] Verify technical claims and flag consequential claims for qualified review
- [ ] Determine whether original media rights are available
- [ ] Managing Editor accepts or rejects story

This issue does **not** authorize writing, approval or publication.
COO intake marker: `{key}`
"""} )
    return items[:MAX_NEW]

def api(repo,token,method,path,payload=None):
    data=json.dumps(payload).encode() if payload is not None else None
    req=Request("https://api.github.com/repos/"+repo+path,data=data,method=method,
        headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
                 "X-GitHub-Api-Version":"2022-11-28","User-Agent":"HVLS360-COO"})
    with urlopen(req,timeout=15) as response:return json.load(response)

def sync(repo,token,items,client=api):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",repo):raise ValueError("invalid repository")
    existing=[]
    for page in range(1,5):
        batch=client(repo,token,"GET",f"/issues?state=all&per_page=100&page={page}")
        existing.extend(x for x in batch if "pull_request" not in x)
        if len(batch)<100:break
    known=set()
    for issue in existing:
        match=re.search(r"COO intake marker: `(lead-[a-f0-9]{16})`",issue.get("body") or "")
        if match:known.add(match.group(1))
    created=[]
    for item in items:
        if item["key"] in known:continue
        issue=client(repo,token,"POST","/issues",{"title":"[COO Research] "+item["title"],"body":item["body"]})
        created.append({"key":item["key"],"number":issue["number"],"url":issue["html_url"]})
        known.add(item["key"])
    return created

def main():
    source=json.loads((ROOT/"office"/"editorial-latest.json").read_text(encoding="utf-8"))
    items=build_items(source.get("briefs",[]))
    repo=os.environ.get("GITHUB_REPOSITORY","")
    token=os.environ.get("GH_TOKEN","")
    if not repo or not token:
        print("No authenticated GitHub context; prepared",len(items),"items only")
        return
    created=sync(repo,token,items)
    print("COO shared Managing Editor issues created:",len(created),"eligible:",len(items))
if __name__=="__main__":main()
