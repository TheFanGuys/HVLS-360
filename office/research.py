#!/usr/bin/env python3
"""Collect research candidates from public RSS/Atom feeds; never publishes."""
import argparse
import datetime as dt
import email.utils
import hashlib
import json
import pathlib
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAX_BYTES = 2_000_000
AGENT = "HVLS360-ResearchDesk/1.0 (+https://github.com/TheFanGuys/HVLS-360)"
def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()
def local(node, tag):
    for child in node:
        if child.tag.split("}")[-1] == tag:
            return (child.text or "").strip()
    return ""
def date_ok(raw, now, days=14):
    if not raw: return False
    try:
        try:
            d=email.utils.parsedate_to_datetime(raw)
        except (ValueError, TypeError):
            # Atom/RFC 3339 dates raise rather than return None in the RSS parser.
            d=None
        if d is None:
            d=dt.datetime.fromisoformat(raw.replace("Z","+00:00"))
        if d.tzinfo is None: d=d.replace(tzinfo=dt.timezone.utc)
        age=(now-d.astimezone(dt.timezone.utc)).total_seconds()
        return -86400 <= age <= days*86400
    except (ValueError, TypeError, OverflowError):
        return False
def fetch(url):
    req=urllib.request.Request(url,headers={"User-Agent":AGENT,"Accept":"application/rss+xml, application/atom+xml, application/xml"})
    with urllib.request.urlopen(req,timeout=18) as resp:
        data=resp.read(MAX_BYTES+1)
        if len(data)>MAX_BYTES: raise ValueError("Feed too large")
        return data
def entries(xml):
    root=ET.fromstring(xml)
    for node in root.iter():
        if node.tag.split("}")[-1] not in ("item","entry"): continue
        title=clean(local(node,"title"))
        link=local(node,"link")
        if not link:
            for child in node:
                if child.tag.split("}")[-1]=="link":
                    link=child.attrib.get("href","")
                    if link: break
        published=local(node,"pubDate") or local(node,"published") or local(node,"updated")
        if title and link.startswith("https://"):
            yield {"title":title,"url":link,"published":published}
def run(now, dry=False):
    cfg=json.loads((ROOT/"office/sources.json").read_text())
    seen=set()
    report=[]
    problems=[]
    diagnostics=[]
    for dept in cfg["departments"]:
        found=[]
        for feed in dept["feeds"]:
            try:
                parsed=list(entries(fetch(feed["url"])))
                recent=sum(1 for item in parsed if date_ok(item["published"],now))
                diagnostics.append("{} / {}: {} parsed, {} recent".format(dept["name"],feed["name"],len(parsed),recent))
                for item in parsed:
                    if not date_ok(item["published"],now): continue
                    key=hashlib.sha256(re.sub(r"\W+","",item["title"].lower()).encode()).hexdigest()
                    if key in seen: continue
                    seen.add(key)
                    item["feed"]=feed["name"]
                    found.append(item)
                    if len(found)>=6: break
            except Exception as e:
                diagnostics.append("{} / {}: FETCH OR PARSE ERROR".format(dept["name"],feed["name"]))
                problems.append(f"{dept['name']}: {type(e).__name__}: {str(e)[:120]}")
        report.append({"department":dept["name"],"leads":found[:6]})
    out=["# HVLS 360 — Research Desk","",f"Run: {now.strftime('%Y-%m-%d %H:%M UTC')}","",
         "**Research leads only — not verified reporting.** Links, dates, product claims and technical details require primary-source verification before an article is drafted. Nothing here is approved for publication.",""]
    for d in report:
        out += [f"## {d['department']}"]
        if not d["leads"]: out += ["No recent candidates found."]
        for x in d["leads"]:
            title=x["title"].replace("[","\\[").replace("]","\\]")
            out += [f"- [{title}]({x['url']}) — {x['published']} ({x['feed']})"]
        out += [""]
    out += ["## Editor-in-Chief review","- [ ] Verify original primary sources and dates","- [ ] Check whether this is genuinely new","- [ ] Determine practical field impact","- [ ] Reject marketing-only or unsupported claims","- [ ] Flag safety-critical topics for expert review","","## COO summary","Research candidate counts: "+", ".join(f"{x['department']} {len(x['leads'])}" for x in report),""]
    out += ["## Feed diagnostics"]+["- "+d for d in diagnostics]+[""]
    if not any(x["leads"] for x in report):
        out += ["## Quality warning", "**No usable leads were collected. This is NOT a successful editorial research result.** Investigate feed accessibility, dates and source selection before trusting the schedule.", ""]
    if problems: out+=["## Feed errors"]+["- "+p for p in problems]
    text="\n".join(out)+"\n"
    if not dry:
        # Public, unverified headlines only. Never include private customer or job data.
        public={"schema_version":1,"generated_at":now.isoformat(),"status":"unverified_research_leads","departments":report,"errors":problems,"disclaimer":"Discovery leads only. Not fact-checked or approved for publication."}
        json_path=ROOT/"office"/"research-latest.json"
        json_path.write_text(json.dumps(public,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if dry:
        print(text[:12000])
    else:
        path=ROOT/"office"/"reports"/(now.strftime("%Y-%m-%d")+"-research.md")
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text,encoding="utf-8")
        print(path)
    return 0 if any(x["leads"] for x in report) else 2
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--dry-run",action="store_true")
    args=ap.parse_args()
    raise SystemExit(run(dt.datetime.now(dt.timezone.utc),args.dry_run))
