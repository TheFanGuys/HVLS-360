#!/usr/bin/env python3
"""Offline editorial release-readiness inventory. Does not approve or publish."""
import json
import pathlib
import re
import sys

ROOT=pathlib.Path(__file__).resolve().parents[1]
URL=re.compile(r"https://[^\s<>]+")
CITATION=re.compile(r"(?<!\!)\[(\d+)\]")
IMAGE=re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
FRONT=re.compile(r"\A---\n(.*?)\n---\n",re.S)

def check_article(path,root=ROOT):
    raw=path.read_text(encoding="utf-8")
    match=FRONT.match(raw)
    errors=[]
    if not match:
        return {"slug":path.stem,"errors":["Missing frontmatter"],"ready_for_publisher":False}
    metadata={}
    for line in match.group(1).splitlines():
        if ":" in line:
            k,v=line.split(":",1)
            metadata[k.strip()]=v.strip().strip('"')
    body=raw[match.end():]
    public=body.split("### Editorial verification record",1)[0]
    sources=public.split("### Sources",1)[1] if "### Sources" in public else ""
    narrative=public.split("### Sources",1)[0]
    referenced=set(CITATION.findall(narrative))
    defined=set(re.findall(r"^\[(\d+)\]\s+",sources,re.M))
    if not defined:
        errors.append("No numbered source references")
    if referenced-defined:
        errors.append("Unresolved source citations: "+", ".join(sorted(referenced-defined)))
    if defined-referenced:
        errors.append("Unused source citations: "+", ".join(sorted(defined-referenced)))
    source_urls=URL.findall(sources)
    if not source_urls:
        errors.append("No HTTPS source links")
    for alt,url in IMAGE.findall(narrative):
        if not alt.strip():
            errors.append("Image lacks alt text")
        if url.startswith(("https://","http://")):
            errors.append("Remote image needs explicit rights review")
        else:
            resolved=(path.parent/url).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                errors.append("Missing or unsafe local image: "+url)
    review=root/"editorial"/"reviews"/(path.stem+"-review.md")
    if not review.is_file():
        errors.append("Missing specialist review record")
    if metadata.get("publication_allowed")!="false":
        errors.append("Draft must be explicitly unpublished")
    if metadata.get("publisher_approval")!="Required":
        errors.append("Publisher approval gate missing")
    word_count=len(narrative.split())
    if word_count<500:
        errors.append("Short feature: under 500 narrative words")
    return {"slug":path.stem,"title":metadata.get("title",""),"word_count":word_count,
        "sources":len(source_urls),"images":len(IMAGE.findall(narrative)),
        "review_record":review.is_file(),"errors":errors,
        "ready_for_publisher":False,
        "status":"draft_quality_checked_not_technically_approved"}

def audit(root=ROOT):
    folder=root/"editorial"/"drafts"
    items=[check_article(p,root) for p in sorted(folder.glob("*.md"))]
    return {"schema_version":1,"drafts":len(items),
        "quality_issues":sum(len(x["errors"]) for x in items),
        "approved_for_publication":0,"articles":items}

def main():
    result=audit()
    output=ROOT/"office"/"reports"/"editorial-readiness.json"
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(f"Audited {result['drafts']} drafts; {result['quality_issues']} editorial issues; zero publication approvals.")
    for item in result["articles"]:
        print(item["slug"]+": "+("; ".join(item["errors"]) if item["errors"] else "static checks passed; specialist review still required"))
    if result["quality_issues"]:
        sys.exit(1)
if __name__=="__main__":
    main()
