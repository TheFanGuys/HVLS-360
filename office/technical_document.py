#!/usr/bin/env python3
"""Extract traceable snippets from public manufacturer HTML pages. No fact verification."""
import datetime as dt
from html.parser import HTMLParser
import json
import pathlib
import re
import urllib.request
from urllib.parse import urlparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
MAX_PAGES=12
MAX_BYTES=350000
class Extractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip=0;self.capture=None;self.parts=[];self.title=[];self.meta={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ("script","style","nav","footer"):self.skip+=1
        if tag=="meta" and a.get("content"):
            k=a.get("name") or a.get("property")
            if k in ("description","article:published_time","citation_title","citation_author"):
                self.meta[k]=a["content"][:500]
        if tag in ("h1","h2","p","title") and not self.skip:self.capture=tag
    def handle_endtag(self,tag):
        if tag in ("script","style","nav","footer") and self.skip:self.skip-=1
        if tag==self.capture:self.capture=None
    def handle_data(self,data):
        if self.skip or not self.capture:return
        t=" ".join(data.split())
        if len(t)<12:return
        if self.capture=="title":self.title.append(t)
        else:self.parts.append({"type":self.capture,"text":t[:1000]})
def extract(url,fetcher=None):
    p=urlparse(url)
    if p.scheme!="https" or not p.hostname:return {"url":url,"status":"invalid_url"}
    if fetcher is None:fetcher=fetch
    try:
        html,final=fetcher(url)
        if urlparse(final).scheme!="https":raise ValueError("unsafe redirect")
        parser=Extractor();parser.feed(html)
        return {"url":url,"final_url":final,"status":"extracted_unverified",
                "page_title":" ".join(parser.title)[:250],
                "metadata":parser.meta,"excerpts":parser.parts[:18],
                "warnings":["Excerpts are source claims, not established facts.",
                            "No technical verification, study methods assessment or publication rights review."]}
    except Exception as e:
        return {"url":url,"status":"extraction_inconclusive","error":type(e).__name__}
def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"HVLS360-TechnicalResearch/1.0"})
    with urllib.request.urlopen(req,timeout=9) as res:
        if "text/html" not in res.headers.get("Content-Type","").lower():raise ValueError("Not an HTML page")
        raw=res.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:raise ValueError("Document exceeds size limit")
        return raw.decode("utf-8",errors="replace"),res.geturl()
def main():
    path=ROOT/"office"/"reports"/"manufacturer-research-candidates.json"
    data=json.loads(path.read_text(encoding="utf-8"))
    records=[]
    for source in data.get("sources",[]):
        for url in source.get("candidate_urls",[]):
            if len(records)>=MAX_PAGES:break
            item=extract(url);item["manufacturer"]=source.get("source","")
            records.append(item)
        if len(records)>=MAX_PAGES:break
    report={"schema_version":1,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
        "status":"unverified_html_excerpts_only","records":records}
    out=ROOT/"office"/"reports"/"manufacturer-excerpts.json"
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Manufacturer HTML pages processed:",len(records))
if __name__=="__main__":main()
