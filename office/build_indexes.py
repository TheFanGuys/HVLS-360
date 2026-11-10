#!/usr/bin/env python3
"""Manual, approval-verified release indexing for HVLS 360.

Writes homepage latest articles, RSS, and sitemap together after a publisher-
approved article has been rendered; not invoked from unattended research.
"""
import argparse
from datetime import datetime, timezone
from email.utils import format_datetime
import html
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

from article_page import BASE, frontmatter
from publication_guard import audit

ROOT=pathlib.Path(__file__).resolve().parents[1]
START="<!-- APPROVED_ARTICLES_START -->"
END="<!-- APPROVED_ARTICLES_END -->"
SITE_TITLE="HVLS 360 Industry Intelligence"
SITE_DESCRIPTION="HVLS fan news, technical analysis and industrial ventilation intelligence."

def short_description(body, fallback):
    for line in body.splitlines():
        t=line.strip()
        if not t or t.startswith(("#","*","[","-")):
            continue
        if t.startswith("http"):
            continue
        t=re.sub(r"<[^>]*>","",t)
        t=re.sub(r"\[([^\]]+)\]\(https://[^\s)]+\)",r"\1",t)
        t=re.sub(r"\*+","",t)
        t=re.sub(r"https://\S+","",t)
        if t:
            return t[:220]
    return fallback

def approved_items(root):
    root=pathlib.Path(root)
    items=[]
    for md in sorted((root/"articles").glob("*.md")):
        slug=md.stem
        page=root/"articles"/slug/"index.html"
        if not page.is_file():
            raise ValueError(f"{slug}: approved HTML page must be rendered first")
        fields,body=frontmatter(md.read_text(encoding="utf-8"))
        import json
        record=json.loads((root/"editorial"/"approvals"/(slug+".json")).read_text(encoding="utf-8"))
        date=datetime.fromisoformat(record["approved_at_utc"].replace("Z","+00:00"))
        if date.utcoffset() is None:
            raise ValueError(f"{slug}: approval timestamp must include a timezone")
        items.append({"slug":slug,"title":fields["title"],"category":fields["category"],
            "description":short_description(body,fields["title"]),"published":date,
            "url":BASE+"articles/"+slug+"/"})
    return sorted(items,key=lambda x:(x["published"],x["slug"]),reverse=True)

def render_home(current,items):
    if current.count(START)!=1 or current.count(END)!=1 or current.index(END)<current.index(START):
        raise ValueError("Homepage is missing unique approved article markers")
    cards=[]
    for item in items[:6]:
        name=html.escape(item["title"])
        category=html.escape(item["category"])
        date=html.escape(item["published"].strftime("%b %d, %Y"))
        target=html.escape("articles/"+item["slug"]+"/",quote=True)
        excerpt=html.escape(item["description"])
        cards.append(f'<a class="card" href="{target}"><small>{category} · {date}</small><strong>{name}</strong><p>{excerpt}</p></a>')
    section=(
        '<section class="section wrap" id="latest"><div class="sectionhead"><h2>Latest analysis</h2></div>'
        '<div class="cards">'+"".join(cards)+'</div></section>'
    ) if cards else ""
    a=current.index(START)+len(START)
    b=current.index(END)
    return current[:a]+"\n"+section+"\n"+current[b:]

def render_sitemap(items):
    root=ET.Element("urlset",{"xmlns":"http://www.sitemaps.org/schemas/sitemap/0.9"})
    for url in (BASE,BASE+"articles/editorial-standards/")+tuple(item["url"] for item in items):
        entry=ET.SubElement(root,"url")
        ET.SubElement(entry,"loc").text=url
    ET.indent(root,space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding="unicode")+"\n"

def render_rss(items):
    rss=ET.Element("rss",{"version":"2.0"})
    channel=ET.SubElement(rss,"channel")
    for key,value in [("title",SITE_TITLE),("link",BASE),("description",SITE_DESCRIPTION),("language","en-us")]:
        ET.SubElement(channel,key).text=value
    for item in items[:30]:
        entry=ET.SubElement(channel,"item")
        for key,value in [
            ("title",item["title"]),("link",item["url"]),("description",item["description"]),
            ("pubDate",format_datetime(item["published"].astimezone(timezone.utc),usegmt=True)),
        ]:
            ET.SubElement(entry,key).text=value
        ET.SubElement(entry,"guid",{"isPermaLink":"true"}).text=item["url"]
    ET.indent(rss,space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(rss,encoding="unicode")+"\n"

def prepare(root=ROOT):
    root=pathlib.Path(root)
    problems=audit(root)
    if problems:
        raise ValueError("Release audit failed: "+"; ".join(problems))
    items=approved_items(root)
    homepage=root/"index.html"
    if not homepage.exists():
        raise ValueError("Missing homepage index.html")
    original=homepage.read_text(encoding="utf-8")
    updated=render_home(original,items)
    rss=render_rss(items)
    sitemap=render_sitemap(items)
    # All files prepared before writing. Every release change is for manual PR review.
    homepage.write_text(updated,encoding="utf-8")
    (root/"rss.xml").write_text(rss,encoding="utf-8")
    (root/"sitemap.xml").write_text(sitemap,encoding="utf-8")
    return len(items)

def main():
    p=argparse.ArgumentParser(description="Rebuild approved-only article homepage, RSS and sitemap")
    p.parse_args()
    try:
        count=prepare()
        print(f"Updated approved-only indexes for {count} article(s). Review changes in a PR before merging.")
    except (OSError,ValueError,KeyError) as error:
        print("BLOCKED:",error,file=sys.stderr)
        sys.exit(1)

if __name__=="__main__":
    main()
