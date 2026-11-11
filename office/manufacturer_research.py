#!/usr/bin/env python3
"""Manufacturer research discovery via public sitemaps; metadata only, no PDF copying."""
import datetime as dt
import json
import gzip
import io
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

ROOT=pathlib.Path(__file__).resolve().parents[1]
MAX_BYTES=2_000_000
KEYWORDS=("research","study","studies","case-study","white-paper","whitepaper",
          "technical","engineering","destratification","airflow","hvls",
          "resource","application","thermal-comfort","energy-savings",
          "industrial-fans","optidrive","drives")
def candidate(url):
    path=urlparse(url).path.lower()
    return any(k in path for k in KEYWORDS)
def urls(xml):
    root=ET.fromstring(xml)
    if root.tag.split("}")[-1] not in ("urlset","sitemapindex"):
        raise ValueError("Response is not a sitemap")
    out=[]
    for item in root.iter():
        if item.tag.split("}")[-1]!="loc":continue
        if item.text:out.append(item.text.strip())
    return out
def same_source(url,host):
    parsed=urlparse(url)
    return parsed.scheme=="https" and parsed.hostname==host and not parsed.username and not parsed.password

def bounded_xml(data):
    if len(data)>MAX_BYTES:raise ValueError("Sitemap too large")
    # Some official ABB .xml URLs return gzip bytes without an encoding header.
    if data.startswith(b"\x1f\x8b"):
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as zipped:
            data=zipped.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES:raise ValueError("Expanded sitemap too large")
    return data

def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":"HVLS360-ResearchLibrary/1.0 (editorial source discovery)"})
    with urllib.request.urlopen(req,timeout=12) as resp:
        if not same_source(resp.geturl(),urlparse(url).hostname):
            raise ValueError("Sitemap redirected outside its HTTPS source")
        return bounded_xml(resp.read(MAX_BYTES+1))
def discover(sources,fetcher=fetch):
    result=[];errors=[]
    for source in sources:
        host=urlparse(source["url"]).hostname
        if not host:continue
        seeds=[]
        for link in source.get("direct_source_urls",[]):
            if same_source(link,host):
                seeds.append(link)
        sitemap=source.get("sitemap_url","https://"+host+"/sitemap.xml")
        candidates=list(seeds)
        source_error_start=len(errors)
        try:
            if not same_source(sitemap,host):raise ValueError("Invalid configured sitemap source")
            top=urls(fetcher(sitemap))
            nested=[x for x in top if x.lower().endswith(".xml") and same_source(x,host)][:5]
            candidates.extend(x for x in top if candidate(x) and same_source(x,host))
            for child in nested:
                try:
                    candidates.extend(x for x in urls(fetcher(child)) if candidate(x) and same_source(x,host))
                except Exception as e:
                    errors.append({"source":source["name"],"sitemap":child,"error":type(e).__name__})
        except Exception as e:
            errors.append({"source":source["name"],"sitemap":sitemap,"error":type(e).__name__})
        unique=list(dict.fromkeys(candidates))
        # Keep explicit direct sources first; prefer English/US paths before the cap.
        preferred=source.get("preferred_path_prefixes",[])
        discovered=[x for x in unique if x not in seeds]
        if preferred:
            discovered.sort(key=lambda x:not any(urlparse(x).path.startswith(p) for p in preferred))
        candidate_count=len(unique)
        unique=(list(dict.fromkeys(seeds))+discovered)[:40]
        result.append({"source":source["name"],"homepage":source["url"],"candidate_urls":unique,
                           "seeded_sources":len(seeds),
                       "sitemap_url":sitemap,
                       "discovered_candidate_count":candidate_count,
                       "candidate_limit_reached":candidate_count>40,
                       "sitemap_status":"incomplete" if len(errors)>source_error_start else "parsed",
                       "candidate_status":"unverified_candidates_available" if unique else "no_candidates",
                       "note":"Bounded URL discovery only, not exhaustive coverage; source content, dates, technical claims and image rights are not verified."})
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
