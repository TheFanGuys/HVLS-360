#!/usr/bin/env python3
"""Resolve public news links cautiously; redirects do not constitute source verification."""
import datetime as dt
import json
import pathlib
import urllib.parse
import urllib.request
from html.parser import HTMLParser

ROOT=pathlib.Path(__file__).resolve().parents[1]
LIMIT=12
class CanonicalParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.candidates=[]
    def handle_starttag(self,tag,attrs):
        if tag not in ("link","meta"):return
        a=dict(attrs)
        if tag=="link" and a.get("rel","").lower()=="canonical" and a.get("href"):
            self.candidates.append(a["href"])
        if tag=="meta" and a.get("property","").lower()=="og:url" and a.get("content"):
            self.candidates.append(a["content"])
def safe(url):
    p=urllib.parse.urlparse(url)
    return p.scheme=="https" and bool(p.hostname) and p.hostname not in ("localhost","127.0.0.1","0.0.0.0") and not p.hostname.endswith((".local",".internal"))
def original_candidate(url,fetcher=None):
    if not safe(url):return {"status":"invalid_or_unsafe","original_url":None}
    if fetcher is None:fetcher=fetch
    try:
        final,html=fetcher(url)
        if not safe(final):return {"status":"unsafe_redirect","original_url":None}
        parser=CanonicalParser()
        parser.feed(html[:150000])
        options=[urllib.parse.urljoin(final,x) for x in parser.candidates]
        candidates=[x for x in options if safe(x)]
        host=urllib.parse.urlparse(final).hostname or ""
        if host=="news.google.com":
            other=[x for x in candidates if urllib.parse.urlparse(x).hostname not in ("news.google.com","google.com")]
            if not other:return {"status":"aggregator_unresolved","original_url":None}
            return {"status":"publisher_candidate_unverified","original_url":other[0]}
        return {"status":"publisher_candidate_unverified","original_url":candidates[0] if candidates else final}
    except Exception as e:
        return {"status":"resolution_inconclusive","original_url":None,"error":type(e).__name__}
def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"HVLS360-EditorialResearch/1.0"})
    with urllib.request.urlopen(req,timeout=9) as response:
        final=response.geturl()
        data=response.read(150001)
        if len(data)>150000:raise ValueError("Response too large")
        return final,data.decode("utf-8",errors="replace")
def resolve(data,fetcher=None):
    return [{"title":b.get("working_title",""),"lead_url":b.get("lead_url",""),
             "resolution":original_candidate(b.get("lead_url",""),fetcher),
             "fact_check":"not_performed","publication_rights":"not_checked"}
            for b in data.get("briefs",[])[:LIMIT]]
def main():
    data=json.loads((ROOT/"office"/"editorial-latest.json").read_text(encoding="utf-8"))
    out={"schema_version":1,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
         "warning":"Original URL candidates are NOT verified sources, evidence, or publication permissions.",
         "items":resolve(data)}
    path=ROOT/"office"/"reports"/"original-source-candidates.json"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Original source resolution attempted:",len(out["items"]))
if __name__=="__main__":main()
