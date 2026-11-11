#!/usr/bin/env python3
"""Manufacturer research discovery via public sitemaps; metadata only, no PDF copying."""
import datetime as dt
import json
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

ROOT=pathlib.Path(__file__).resolve().parents[1]
MAX_BYTES=1_500_000
KEYWORDS=("research","study","studies","case-study","white-paper","whitepaper",
          "technical","engineering","destratification","airflow","hvls",
          "resource","application","thermal-comfort","energy-savings")
def candidate(url):
    path=urlparse(url).path.lower()
    return any(k in path for k in KEYWORDS)
def urls(xml):
    root=ET.fromstring(xml)
    out=[]
    for item in root.iter():
        if item.tag.split("}")[-1]!="loc":continue
        if item.text:out.append(item.text.strip())
    return out
def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"HVLS360-ResearchLibrary/1.0 (editorial source discovery)"})
    with urllib.request.urlopen(req,timeout=12) as resp:
        data=resp.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES:raise ValueError("Sitemap too large")
        return data
def discover(sources,fetcher=fetch):
    result=[];errors=[]
    for source in sources:
        host=urlparse(source["url"]).hostname
        if not host:continue
        seeds=[]
        for link in source.get("direct_source_urls",[]):
            parsed=urlparse(link)
            if parsed.scheme=="https" and parsed.hostname==host:
                seeds.append(link)
        sitemap="https://"+host+"/sitemap.xml"
        candidates=list(seeds)
        source_error_start=len(errors)
        try:
            top=urls(fetcher(sitemap))
            nested=[x for x in top if x.lower().endswith(".xml") and urlparse(x).hostname==host][:5]
            candidates.extend(x for x in top if candidate(x) and urlparse(x).hostname==host)
            for child in nested:
                try:
                    candidates.extend(x for x in urls(fetcher(child)) if candidate(x) and urlparse(x).hostname==host)
                except Exception as e:
                    errors.append({"source":source["name"],"sitemap":child,"error":type(e).__name__})
        except Exception as e:
            errors.append({"source":source["name"],"sitemap":sitemap,"error":type(e).__name__})
        unique=list(dict.fromkeys(candidates))[:40]
        result.append({"source":source["name"],"homepage":source["url"],"candidate_urls":unique,
                           "seeded_sources":len(seeds),
                       "sitemap_status":"incomplete" if len(errors)>source_error_start else "parsed",
                       "candidate_status":"unverified_candidates_available" if unique else "no_candidates",
                       "note":"URL discovery only; source content, dates, technical claims and image rights are not verified."})
    return result,errors
def main():
    cfg=json.loads((ROOT/"office"/"primary-sources.json").read_text(encoding="utf-8"))
    sources=[x for x in cfg["sources"] if x["type"] in ("manufacturer_research","controls_research")]
    found,errors=discover(sources)
    output={"schema_version":1,"generated_at":dt.datetime.now(dt.timezone.utc).isoformat(),
            "status":"unverified_url_candidates","sources":found,"errors":errors}
    target=ROOT/"office"/"reports"/"manufacturer-research-candidates.json"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("Manufacturer source discovery:",sum(len(x["candidate_urls"]) for x in found),"candidate URLs;",len(errors),"errors")
    # A successful pipeline must not make incomplete source coverage look healthy.
    if errors:
        import os
        if os.environ.get("GITHUB_ACTIONS")=="true":
            print(f"::warning::Manufacturer discovery incomplete: {len(errors)} sitemap failures. Direct source candidates are unverified; inspect the research artifact.")
        summary=os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary,"a",encoding="utf-8") as stream:
                stream.write(f"\n### Manufacturer discovery warning\n{len(errors)} sitemap failures; fallback URLs are candidates, not verified coverage. See research artifact.\n")
if __name__=="__main__":main()
