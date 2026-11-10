"""Deterministic, dependency-free HTML renderer for verified approved articles.

This module does not write files. Run office/render_release.py to check the
publisher approval record and create a candidate HTML page in a PR.
"""
from datetime import datetime
import html
import json
import pathlib
import re
from urllib.parse import urlsplit

BASE="https://thefanguys.github.io/HVLS-360/"
INTERNAL=(
    "editorial research notes",
    "editorial verification record",
    "internal research log",
)
SLUG_RE=re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

def frontmatter(raw):
    match=re.match(r"\A---\s*\n([\s\S]*?)\n---\s*\n",raw)
    if not match:
        raise ValueError("Article frontmatter missing")
    fields={}
    for line in match.group(1).splitlines():
        if ":" not in line:
            raise ValueError("Unexpected metadata line")
        key,value=line.split(":",1)
        key=key.strip()
        if not re.fullmatch(r"[a-z_]+",key) or key in fields:
            raise ValueError("Invalid metadata key")
        fields[key]=value.strip().strip('"')
    if fields.get("publication_allowed")!="true" or fields.get("status")!="APPROVED FOR PUBLICATION":
        raise ValueError("Article is not in the publisher-approved state")
    if not fields.get("title") or not fields.get("category"):
        raise ValueError("Missing title or category")
    return fields,raw[match.end():]

def safe_anchor(url,label):
    parts=urlsplit(url)
    if parts.scheme!="https" or not parts.netloc or "@" in parts.netloc:
        return html.escape(label)
    return '<a href="'+html.escape(url,quote=True)+'" rel="noopener noreferrer" target="_blank">'+html.escape(label)+'</a>'

TOKENS=re.compile(r"(\*\*[^*]+\*\*|\[[^\]]+\]\(https://[^\s)]+\)|https://[^\s<>]+)")
def inline_markup(s):
    result=[]
    pos=0
    for match in TOKENS.finditer(s):
        result.append(html.escape(s[pos:match.start()]))
        token=match.group(0)
        if token.startswith("**"):
            result.append("<strong>"+html.escape(token[2:-2])+"</strong>")
        elif token.startswith("["):
            i=token.index("](")
            result.append(safe_anchor(token[i+2:-1],token[1:i]))
        else:
            url=token.rstrip(".,;")
            result.append(safe_anchor(url,url))
            result.append(html.escape(token[len(url):]))
        pos=match.end()
    result.append(html.escape(s[pos:]))
    return "".join(result)

def render_markdown(text):
    lines=text.splitlines()
    result=[]
    para=[]
    in_list=False
    def flush():
        if para:
            result.append("<p>"+inline_markup(" ".join(para))+"</p>")
            para.clear()
    def close_list():
        nonlocal in_list
        if in_list:
            result.append("</ul>")
            in_list=False
    skip_title=True
    for line in lines:
        t=line.strip()
        if not t:
            flush()
            close_list()
            continue
        if re.match(r"^#{2,3} ",t) and t.lstrip("# ").lower() in INTERNAL:
            break
        if re.match(r"^# ",t) and skip_title:
            skip_title=False
            continue
        head=re.match(r"^(#{1,4})\s+(.+)$",t)
        if head:
            flush()
            close_list()
            level=max(2,min(4,len(head.group(1))))
            result.append(f"<h{level}>"+inline_markup(head.group(2))+f"</h{level}>")
        elif t.startswith("- "):
            flush()
            if not in_list:
                result.append("<ul>")
                in_list=True
            result.append("<li>"+inline_markup(t[2:])+"</li>")
        else:
            close_list()
            para.append(t)
    flush()
    close_list()
    return "\n".join(result)

def build_html(root,slug):
    root=pathlib.Path(root)
    if not SLUG_RE.fullmatch(slug):
        raise ValueError("Invalid slug")
    publication=root/"articles"/(slug+".md")
    raw=publication.read_text(encoding="utf-8")
    fields,body=frontmatter(raw)
    title=fields["title"]
    category=fields["category"]
    description=""
    for line in body.splitlines():
        clean=line.strip()
        if clean and not clean.startswith(("#","*","[","-")):
            description=re.sub(r"https?://\S+","",clean)
            description=re.sub(r"\*+","",description)[:155]
            break
    if not description:
        description=title+" — HVLS 360° industrial air movement."
    approval_file=root/"editorial"/"approvals"/(slug+".json")
    approval=json.loads(approval_file.read_text(encoding="utf-8"))
    date=datetime.fromisoformat(approval["approved_at_utc"].replace("Z","+00:00"))
    date_iso=date.date().isoformat()
    display_date=date.strftime("%B %-d, %Y")
    url=BASE+"articles/"+slug+"/"
    heading=html.escape(title)
    desc=html.escape(description,quote=True)
    canon=html.escape(url,quote=True)
    org=html.escape(category)
    schema={"@context":"https://schema.org","@type":"Article","headline":title,
        "description":description,"datePublished":date_iso,"dateModified":date_iso,
        "mainEntityOfPage":{"@type":"WebPage","@id":url},
        "publisher":{"@type":"Organization","name":"Big Fan Guys","url":"https://bigfanguys.com/"},
        "author":{"@type":"Organization","name":"HVLS 360° Editorial Desk"}}
    ld=json.dumps(schema,ensure_ascii=False,separators=(",",":")).replace("</","<\\/")
    body_html=render_markdown(body)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{heading} | HVLS 360°</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{canon}"><meta property="og:type" content="article"><meta property="og:title" content="{heading}">
<meta property="og:description" content="{desc}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE}assets/masthead.png"><meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="HVLS 360 RSS" href="{BASE}rss.xml">
<link rel="stylesheet" href="../../assets/style.css"><link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{ld}</script></head><body>
<div class="top"><div class="wrap"><span>HVLS 360° / Industry Intelligence</span><span>Presented by Big Fan Guys</span></div></div>
<header class="masthead wrap"><a href="../../" aria-label="HVLS 360 home"><img src="../../assets/masthead.png" alt="HVLS 360 Industry Intelligence" width="2048" height="896"></a></header>
<nav class="nav" aria-label="Primary"><div class="wrap"><a href="../../">Home</a><a href="../../#departments">Industry News</a><a href="../../#departments">Technology</a><a href="../../#departments">Installation</a><a href="../../#departments">Service &amp; VFDs</a></div></nav>
<main class="article"><p class="breadcrumbs"><a href="../../">Home</a> / {org}</p>
<div class="eyebrow">{org}</div><h1>{heading}</h1><p class="meta">HVLS 360° Editorial Desk · {display_date}</p>
<div class="article-body">{body_html}</div></main>
<footer class="foot"><div class="wrap">© HVLS 360° · Published by Big Fan Guys · <a href="../../rss.xml">RSS</a></div></footer>
</body></html>
'''
