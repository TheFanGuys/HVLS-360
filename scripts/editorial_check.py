#!/usr/bin/env python3
"""Offline editorial QA. Does not publish content or call external APIs."""
import json
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[1]
errors = []
warnings = []

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = False
        self.titles = []
        self.meta = {}
        self.images = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.title = True
        if tag == "meta" and a.get("name"):
            self.meta[a["name"]] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.meta["canonical"] = a.get("href", "")
        if tag == "img":
            self.images.append(a)
        if tag == "a":
            self.links.append(a.get("href", ""))
    def handle_endtag(self, tag):
        if tag == "title":
            self.title = False
    def handle_data(self, data):
        if self.title:
            self.titles.append(data)

pages = list((ROOT / "articles").rglob("*.html")) if (ROOT / "articles").exists() else []
pages += list((ROOT / "categories").rglob("*.html")) if (ROOT / "categories").exists() else []
if not pages:
    warnings.append("No article or category HTML pages found yet.")
for path in pages:
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    label = str(path.relative_to(ROOT))
    if not "".join(p.titles).strip():
        errors.append(f"{label}: missing title")
    if not p.meta.get("description"):
        errors.append(f"{label}: missing meta description")
    if not p.meta.get("canonical", "").startswith("https://"):
        errors.append(f"{label}: missing absolute canonical URL")
    for img in p.images:
        if not img.get("alt"):
            errors.append(f"{label}: image missing meaningful alt text")
        if img.get("src", "").startswith("data:"):
            warnings.append(f"{label}: embedded data URI image may harm performance")
    for href in p.links:
        if href.startswith("javascript:"):
            errors.append(f"{label}: javascript: link forbidden")
manifest = ROOT / "media" / "assets.json"
if manifest.exists():
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for item in data.get("assets", []):
        for field in ("id", "source", "rights", "caption", "alt", "review_status"):
            if not item.get(field):
                errors.append(f"Media {item.get('id','unknown')}: missing {field}")
        if item.get("review_status") not in ("pending", "approved", "rejected"):
            errors.append(f"Media {item.get('id','unknown')}: invalid review_status")
print(f"Checked {len(pages)} pages and media manifest.")
for w in warnings:
    print("WARNING:", w)
for e in errors:
    print("ERROR:", e)
sys.exit(1 if errors else 0)
