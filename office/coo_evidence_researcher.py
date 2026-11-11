#!/usr/bin/env python3
"""Evidence Researcher: retrieve publisher candidate metadata with source provenance.

This is bounded public-page metadata extraction, not claim verification or an LLM.
No unpublished drafts, automatic approval, or publishing.
"""
import datetime as dt
from html.parser import HTMLParser
import ipaddress
import json
from pathlib import Path
import re
import socket
from urllib.parse import urlsplit
from urllib.request import Request,build_opener,HTTPRedirectHandler

ROOT=Path(__file__).resolve().parents[1]
REPORTS=ROOT/"office"/"reports"
MAX_PAGES=8
MAX_BYTES=180000

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta={}
        self.title=""
        self.in_title=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="title":self.in_title=True
        if tag=="meta":
            key=(a.get("property") or a.get("name") or "").lower()
            if key in ("article:published_time","datepublished","date","author","article:author","og:title","description","og:description") and a.get("content"):
                self.meta[key]=a["content"][:400]
    def handle_endtag(self,tag):
        if tag=="title":self.in_title=False
    def handle_data(self,data):
        if self.in_title:self.title+=data[:300]

def public_https(url):
    p=urlsplit(url)
    if p.scheme!="https" or not p.hostname or p.username or p.password or p.port not in (None,443):return False
    host=p.hostname.lower().rstrip(".")
    if host in ("localhost",) or host.endswith((".local",".internal",".localhost")):return False
    try:
        addresses=socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)
        if not addresses:return False
        return all(ipaddress.ip_address(x[4][0]).is_global for x in addresses)
    except (socket.gaierror,ValueError,OSError):return False

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None

def fetch_page(url):
    if not public_https(url):return {"status":"unsafe_or_unresolvable_url"}
    try:
        opener=build_opener(NoRedirect)
        with opener.open(Request(url,headers={"User-Agent":"HVLS360-EvidenceResearch/1.0","Accept":"text/html"}),timeout=8) as response:
            final=response.geturl()
            if not public_https(final):return {"status":"unsafe_final_url"}
            if "html" not in response.headers.get("Content-Type","").lower():return {"status":"not_html"}
            raw=response.read(MAX_BYTES+1)
            if len(raw)>MAX_BYTES:return {"status":"page_too_large"}
        parser=Metadata()
        parser.feed(raw.decode("utf-8",errors="replace"))
        return {"status":"metadata_extracted_unverified","retrieved_url":final,
            "page_title":(parser.meta.get("og:title") or parser.title.strip())[:300],
            "reported_author":parser.meta.get("author") or parser.meta.get("article:author"),
            "reported_date":parser.meta.get("article:published_time") or parser.meta.get("datepublished") or parser.meta.get("date"),
            "description":parser.meta.get("description") or parser.meta.get("og:description"),
            "metadata_origin":"publisher_page_self_reported_not_independently_verified"}
    except Exception as exc:
        return {"status":"fetch_inconclusive","error_type":type(exc).__name__}

def research(decisions,fetcher=fetch_page,now=None):
    results=[]
    for d in decisions.get("decisions",[]):
        if d.get("decision")!="research_followup":continue
        candidate=d.get("source_candidate")
        if not candidate:continue
        if len(results)>=MAX_PAGES:break
        evidence=fetcher(candidate)
        results.append({"lead_id":d.get("lead_id"),"assignment_role":"Evidence Researcher",
            "publisher_candidate":candidate,"evidence":evidence,
            "checks":{"publisher_identity":"not_independently_verified",
                "author":"self_reported_unverified" if evidence.get("reported_author") else "missing",
                "publication_date":"self_reported_unverified" if evidence.get("reported_date") else "missing",
                "technical_claims":"not_verified","corroboration":"not_performed"},
            "next_owner":"Head of Research",
            "handoff":"requires_editorial_evidence_review",
            "publication_allowed":False})
    return {"schema_version":1,"generated_at":(now or dt.datetime.now(dt.timezone.utc)).isoformat(),
        "status":"evidence_metadata_collection_completed_no_claim_verification",
        "attempted":len(results),"results":results,"publication_allowed":False}

def main():
    decisions=json.loads((REPORTS/"coo-research-head-decisions.json").read_text(encoding="utf-8"))
    output=research(decisions)
    (REPORTS/"coo-evidence-research.json").write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Evidence Researcher:",output["attempted"],"publisher pages attempted; claims unverified")
if __name__=="__main__":main()
