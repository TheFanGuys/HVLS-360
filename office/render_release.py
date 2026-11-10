#!/usr/bin/env python3
"""Manual build step for reviewable, publisher-approved HTML articles.

This command does not publish to GitHub and never creates approval records.
"""
import argparse
import pathlib
import sys
from article_page import build_html
from publication_guard import audit

ROOT=pathlib.Path(__file__).resolve().parents[1]

def prepare(slug,root=ROOT):
    root=pathlib.Path(root)
    issues=audit(root)
    if issues:
        raise ValueError("Publication audit blocked release: "+"; ".join(issues))
    output=root/"articles"/slug/"index.html"
    if output.is_file():
        raise ValueError("Live page already exists; updates require a new reviewed release")
    page=build_html(root,slug)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(page,encoding="utf-8")
    return output

def main():
    p=argparse.ArgumentParser(description="Prepare approved article HTML for an explicitly reviewed release PR")
    p.add_argument("--slug",required=True)
    a=p.parse_args()
    try:
        print("Prepared for publisher review:",prepare(a.slug))
    except (ValueError,OSError,KeyError) as e:
        print("BLOCKED:",e,file=sys.stderr)
        sys.exit(1)

if __name__=="__main__":
    main()
