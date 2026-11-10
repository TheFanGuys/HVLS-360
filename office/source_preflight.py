#!/usr/bin/env python3
"""Read-only source verification preflight. HTTP reachability is NOT factual verification."""
import datetime as dt
import json
import pathlib
import urllib.error
import urllib.request
from urllib.parse import urlparse

ROOT=pathlib.Path(__file__).resolve().parents[1]
MAX=20
def classify(url):
    parsed=urlparse(url)
    if parsed.scheme!="https" or not parsed.hostname:return "invalid_url"
    if parsed.hostname in ("news.google.com","www.google.com"):return "aggregator_requires_original"
    return "direct_source_candidate"
def probe(url,opener=urllib.request.urlopen):
    kind=classify(url)
    if kind!="direct_source_candidate":
        return {"status":kind,"reachable":False,"final_url":None}
    try:
        req=urllib.request.Request(url,method="HEAD",headers={"User-Agent":"HVLS360-EditorialSourceCheck/1.0"})
        with opener(req,timeout=8) as res:
            final=res.geturl()
            return {"status":"reachable_unverified" if urlparse(final).scheme=="https" else "unsafe_redirect",
                    "reachable":urlparse(final).scheme=="https","final_url":final}
    except Exception as e:
        return {"status":"probe_inconclusive","reachable":False,"error":type(e).__name__,"final_url":None}
def verify(data,opener=urllib.request.urlopen):
    out=[]
    for b in data.get("briefs",[])[:MAX]:
        url=b.get("lead_url","")
        status=probe(url,opener)
        out.append({"working_title":b.get("working_title",""),"lead_url":url,
                    "source_type":classify(url),"preflight":status,
                    "original_publisher":"unverified","publication_date":"unverified",
                    "us_applicability":"unverified","technical_claims":"unverified",
                    "research_methods":"unverified","funding_and_conflicts":"unverified",
                    "editorial_status":"research_required"})
    return out
def main():
    data=json.loads((ROOT/"office"/"editorial-latest.json").read_text(encoding="utf-8"))
    out={"schema_version":1,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
         "disclaimer":"HTTP reachability does not verify accuracy, authorship, research findings or rights.",
         "sources":verify(data)}
    target=ROOT/"office"/"reports"/"source-preflight.json"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Source preflight:",len(out["sources"]),"leads")
if __name__=="__main__":main()
