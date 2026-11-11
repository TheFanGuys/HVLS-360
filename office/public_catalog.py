#!/usr/bin/env python3
"""Build/check the public story index, RSS and sitemap from publisher-approved releases.

Run only on a reviewed release branch. Never imports the research-lead index:
research, drafts and manufacturer media candidates are never publishable here.
"""
import argparse
from datetime import datetime, timezone
from email.utils import format_datetime
import html
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

from article_page import BASE, frontmatter
from publication_guard import audit

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- HVLS360:STORIES START -->"
END = "<!-- HVLS360:STORIES END -->"
SITE_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

def published_stories(root):
    rows = []
    for path in sorted((root / "articles").glob("*.md")):
        slug = path.stem
        # Guard verifies the same Markdown, approval record and generated HTML.
        raw = path.read_text(encoding="utf-8")
        fields, body = frontmatter(raw)
        record = json.loads((root / "editorial" / "approvals" / (slug + ".json")).read_text(encoding="utf-8"))
        published = datetime.fromisoformat(record["approved_at_utc"].replace("Z", "+00:00"))
        if published.tzinfo is None:
            raise ValueError(f"{slug}: approval time must contain a UTC offset")
        desc = ""
        for paragraph in re.split(r"\n\s*\n", body):
            value = " ".join(paragraph.strip().split())
            if value and not value.startswith(("#", "*", "[", "-")):
                desc = re.sub(r"\[([^\]]+)\]\(https://[^\s)]+\)", r"\1", value)
                desc = re.sub(r"<[^>]+>", "", desc)
                desc = re.sub(r"\*+", "", desc)
                desc = re.sub(r"https?://\S+", "", desc).strip()[:220]
                break
        desc=fields.get("seo_description") or desc
        rows.append({"slug": slug, "title": fields["title"], "category": fields["category"],
                     "description": desc or fields["title"], "published": published,
                     "url": BASE + "articles/" + slug + "/"})
    rows.sort(key=lambda item: (item["published"], item["slug"]), reverse=True)
    return rows

def story_section(rows):
    lines = ['<section class="section wrap" id="latest" aria-labelledby="latest-title">',
             '  <div class="sectionhead"><h2 id="latest-title">Latest reporting</h2></div>']
    if not rows:
        lines += ['  <div class="latest-empty"><span class="eyebrow">Publication desk</span>',
                  '    <h3>Industry reporting is on the way.</h3>',
                  '    <p>Follow our coverage of large-diameter fans, drives, controls and field service as the first articles go live.</p>',
                  '    <a href="rss.xml" class="textlink">Subscribe via RSS →</a>',
                  '  </div>']
    else:
        lines.append('  <div class="story-grid">')
        for row in rows[:12]:
            title = html.escape(row["title"])
            cat = html.escape(row["category"])
            description = html.escape(row["description"])
            slug = row["slug"] # guard verifies slugs
            day = row["published"].date().isoformat()
            lines.extend([
                '    <article class="story-card">',
                '      <div class="story-card-meta"><span>'+cat+'</span><time datetime="'+day+'">'+day+'</time></div>',
                '      <h3><a href="articles/'+slug+'/">'+title+'</a></h3>',
                '      <p>'+description+'</p>',
                '      <a class="textlink" href="articles/'+slug+'/">Read article →</a>',
                '    </article>'])
        lines.append('  </div>')
    lines.append('</section>')
    return "\n".join(lines)

def homepage_expected(content, rows):
    if content.count(START) != 1 or content.count(END) != 1:
        raise ValueError("Homepage missing unique story catalog markers")
    before, rest = content.split(START, 1)
    _, after = rest.split(END, 1)
    return before + START + "\n" + story_section(rows) + "\n" + END + after

def make_rss(rows):
    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    for tag, value in [
        ("title", "HVLS 360 Industry Intelligence"),
        ("link", BASE),
        ("description", "HVLS fan news, technical analysis and industrial ventilation intelligence."),
        ("language", "en-us")]:
        ET.SubElement(channel, tag).text = value
    for row in rows[:30]:
        item = ET.SubElement(channel, "item")
        for tag, value in [
            ("title", row["title"]), ("link", row["url"]),
            ("description", row["description"]),
            ("guid", row["url"]),
            ("pubDate", format_datetime(row["published"].astimezone(timezone.utc), usegmt=True))
        ]:
            if tag == "guid":
                ET.SubElement(item, tag, {"isPermaLink": "true"}).text = value
            else:
                ET.SubElement(item, tag).text = value
    return ET.tostring(rss, encoding="unicode", xml_declaration=True) + "\n"

def make_sitemap(rows):
    ET.register_namespace("", SITE_NS)
    site = ET.Element("{"+SITE_NS+"}urlset")
    base_urls = [BASE, BASE+"articles/editorial-standards/", BASE+"resources/"]
    for link in base_urls + [row["url"] for row in rows]:
        url = ET.SubElement(site, "{"+SITE_NS+"}url")
        ET.SubElement(url, "{"+SITE_NS+"}loc").text = link
    return ET.tostring(site, encoding="unicode", xml_declaration=True) + "\n"

def expected_files(root):
    # Prevent building indexes from drafts, forged approval rows or changed articles.
    errors = audit(root)
    if errors:
        raise ValueError("Release audit failed: "+"; ".join(errors))
    rows = published_stories(root)
    homepage = root/"index.html"
    return {homepage: homepage_expected(homepage.read_text(encoding="utf-8"), rows),
            root/"rss.xml": make_rss(rows),
            root/"sitemap.xml": make_sitemap(rows)}

def check(root=ROOT):
    expected = expected_files(Path(root))
    return [str(p.relative_to(root)) for p,content in expected.items()
            if not p.exists() or p.read_text(encoding="utf-8") != content]

def write(root=ROOT):
    for path, content in expected_files(Path(root)).items():
        path.write_text(content, encoding="utf-8")

def main():
    p=argparse.ArgumentParser(description="Build or verify approval-only public article discovery")
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true", help="Update files on a reviewed release branch")
    group.add_argument("--check", action="store_true", help="Fail if any public index is stale")
    args=p.parse_args()
    try:
        if args.write:
            write()
            print("Updated homepage story catalog, RSS and sitemap")
        else:
            stale=check()
            if stale:
                raise ValueError("Public discovery files out of sync: "+", ".join(stale))
            print("Public discovery matches approved articles")
    except (OSError, ValueError, KeyError, ET.ParseError) as e:
        print("PUBLICATION BLOCK:", str(e), file=sys.stderr)
        sys.exit(1)

if __name__=="__main__":
    main()
