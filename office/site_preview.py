"""Build an unindexed founder preview; never writes public articles or approvals."""
import html,json,re
from pathlib import Path
from article_page import render_markdown
ROOT=Path(__file__).resolve().parents[1]
def build(root=ROOT):
 root=Path(root); out=root/'office/preview';out.mkdir(exist_ok=True)
 items=json.loads((root/'office/launch-package.json').read_text())['items']
 def shell(title,body):
  return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>{html.escape(title)} | HVLS 360° Review</title><link rel="stylesheet" href="../../assets/style.css"><link rel="icon" href="../../assets/favicon.svg"><style>.preview-bar{{background:#142d40;color:#fff;padding:12px 18px;font:14px/1.5 system-ui}}.preview-bar a{{color:#fff;margin-left:18px}}.article-figure img{{max-width:100%;height:auto}}.preview-nav{{display:flex;flex-wrap:wrap;gap:16px;padding:16px 0}}.story-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:24px}}.story-card{{min-width:0}}.article-body{{overflow-wrap:anywhere}}</style><link rel="stylesheet" href="../../assets/publication.css"></head><body><div class="preview-bar">Founder preview · Unreleased drafts<a href="./">Magazine</a><a href="../command-center.html">Command Center</a><a href="../first-article-review.html">Edit articles</a></div><header class="masthead wrap"><a href="./"><img src="../../assets/masthead.png" alt="HVLS 360°" width="2048" height="896"></a></header><nav class="nav"><div class="wrap"><a href="./">All stories</a><a href="../../resources/">Resources</a><a href="../../articles/editorial-standards/">Editorial standards</a></div></nav>{body}<footer class="foot"><div class="wrap">HVLS 360° · Presented by Big Fan Guys</div></footer></body></html>'''
 cards=[]
 for item in items:
  slug=item['slug']
  if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError('Invalid slug')
  raw=(root/'editorial/drafts'/f'{slug}.md').read_text()
  front=re.match(r'\A---\s*\n([\s\S]*?)\n---\s*\n',raw)
  if not front or 'publication_allowed: false' not in front[1]:raise ValueError('Expected unreleased draft')
  title=re.search(r'^title: "(.+)"$',front[1],re.M)[1]
  category=re.search(r'^category: "(.+)"$',front[1],re.M)[1]
  content=render_markdown(raw[front.end():])
  body=f'<main class="article"><p class="breadcrumbs"><a href="./">All stories</a> / {html.escape(category)}</p><div class="eyebrow">{html.escape(category)}</div><h1>{html.escape(title)}</h1><div class="article-body">{content}</div><div class="preview-nav"><a href="./">← All stories</a><a href="../first-article-review.html">Open Review Studio →</a></div></main>'
  (out/f'{slug}.html').write_text(shell(title,body))
  cards.append(f'<article class="story-card"><div class="eyebrow">{html.escape(category)}</div><h3><a href="{slug}.html">{html.escape(title)}</a></h3><p>{html.escape(item["seo_description"])}</p><a class="textlink" href="{slug}.html">Read article →</a></article>')
 home='<main><section class="hero"><div class="wrap"><div class="eyebrow">The industrial air movement journal</div><h1>The working journal of industrial air movement.</h1><p>Technology, controls, installation and field service for the people who work with large-diameter fans.</p></div></section><section class="section wrap"><div class="sectionhead"><h2>In this issue</h2></div><div class="story-grid">'+''.join(cards)+'</div></section></main>'
 (out/'index.html').write_text(shell('Full magazine preview',home))
 return len(items)+1
if __name__=='__main__': print(f'Built {build()} unindexed review pages; public catalog unchanged.')
