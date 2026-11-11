#!/usr/bin/env python3
"""Create a deduplicated shared Managing Editor queue using GitHub Issues.

Only public-source lead metadata is sent to Issues. Never upload manuscripts,
private research, draft excerpts, internal expert notes, or approval tokens.
"""
import hashlib,json,os,re,sys
import datetime as dt
from zoneinfo import ZoneInfo
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

def build_items(briefs,now=None):
    now=now or dt.datetime.now(dt.timezone.utc)
    due=(now.astimezone(ZoneInfo("America/New_York"))+dt.timedelta(days=2)).strftime("%Y-%m-%d")+" 17:00 America/New_York (internal triage target)"
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
**Next checkpoint:** {due}
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
    return items

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
    else:
        raise RuntimeError("Issue history exceeds bounded scan; refusing unsafe deduplication")
    known=set()
    for issue in existing:
        match=re.search(r"COO intake marker: `(lead-[a-f0-9]{16})`",issue.get("body") or "")
        if match:known.add(match.group(1))
    created=[]
    for item in items:
        if item["key"] in known:continue
        if len(created)>=MAX_NEW:break
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
        if os.environ.get("GITHUB_ACTIONS")=="true":
            raise RuntimeError("Shared assignment sync missing authenticated GitHub context")
        print("No authenticated GitHub context; prepared",len(items),"items only")
        return
    created=sync(repo,token,items)
    # Exercise real idempotence against GitHub after actual creates, not fixture data.
    keys={x["key"] for x in created}
    duplicates=sync(repo,token,[x for x in items if x["key"] in keys]) if keys else []
    if duplicates:raise RuntimeError("Duplicate assignment detected during readback check")
    report={"schema_version":1,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
            "status":"synced_unverified_leads","eligible_candidates":len(items),
            "issues_created":len(created),"created_issues":created,
            "deduplication_check":"created_items_rechecked_no_duplicates" if keys else "no_new_items_to_recheck",
            "run_id":os.environ.get("GITHUB_RUN_ID"),"publication_allowed":False}
    path=ROOT/"office/reports/coo-issues-sync.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(report,indent=2)+"\n")
    print("COO shared Managing Editor issues created:",len(created),"eligible:",len(items))
    print("Shared intake readback:",report["deduplication_check"])
    summary=os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary,"a") as stream:
            stream.write(f"\n### Shared research intake\n{len(items)} eligible candidates; {len(created)} assignments created. Readback: {report['deduplication_check']}. Leads remain unverified, no publication approval.\n")
if __name__=="__main__":main()
