"""Build an unindexed image-led founder preview; never approves/releases articles."""
import html,json,re
from pathlib import Path
from article_page import render_markdown
ROOT=Path(__file__).resolve().parents[1]
def build(root=ROOT):
 root=Path(root);out=root/'office/preview';out.mkdir(exist_ok=True)
 items=json.loads((root/'office/launch-package.json').read_text())['items']
 imagery=json.loads((root/'editorial/media/article-images.json').read_text())['items']
 def picture(slug,linked=False):
  m=imagery[slug];src=m['file']
  if not src.startswith('editorial/media/') or '..' in src or not (root/src).is_file():raise ValueError('Unsafe or missing image')
  im=f'<img src="../../{html.escape(src,quote=True)}" alt="{html.escape(m["alt"],quote=True)}" loading="lazy" decoding="async" style="object-position:{m["position"]}">'
  return f'<a class="story-image {m["kind"]}" href="{slug}.html">{im}</a>' if linked else f'<figure class="article-lead {m["kind"]}">{im}<figcaption>{html.escape(m["caption"])} <span>— {m["credit"]}</span></figcaption></figure>'
 def shell(title,body):
  return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><title>{html.escape(title)} | HVLS 360°</title><link rel="stylesheet" href="../../assets/style.css"><link rel="stylesheet" href="../../assets/publication.css"><link rel="icon" href="../../assets/favicon.svg"></head><body class="magazine"><div class="preview-bar">Founder review edition<a href="../command-center.html">Command Center</a><a href="../first-article-review.html">Edit articles</a></div><header class="trade-header"><div class="wrap trade-bar"><a href="./" class="trade-logo">HVLS <b>360°</b><small>THE BIG FAN GUYS JOURNAL</small></a><nav aria-label="Magazine"><a href="./">Features</a><a href="#latest">Latest</a><a href="../../resources/">Research &amp; laws</a><a href="../../articles/editorial-standards/">About</a></nav><a class="field-link" href="https://bigfanguys.com/">Big Fan Guys ↗</a></div></header>{body}<footer class="foot"><div class="wrap">HVLS 360° · Presented by Big Fan Guys</div></footer></body></html>'''
 cards=[]
 for item in items:
  slug=item['slug']
  if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError('Invalid slug')
  raw=(root/'editorial/drafts'/f'{slug}.md').read_text();front=re.match(r'\A---\s*\n([\s\S]*?)\n---\s*\n',raw)
  if not front or 'publication_allowed: false' not in front[1]:raise ValueError('Expected unreleased draft')
  title=re.search(r'^title: "(.+)"$',front[1],re.M)[1];category=re.search(r'^category: "(.+)"$',front[1],re.M)[1]
  content=render_markdown(raw[front.end():]);reading=max(1,round(len(raw.split())/220))
  body=f'<main class="article"><p class="breadcrumbs"><a href="./">Magazine</a> / {html.escape(category)}</p><div class="eyebrow">{html.escape(category)}</div><h1>{html.escape(title)}</h1><p class="meta">HVLS 360° Editorial Desk · {reading} min read</p>{picture(slug)}<div class="article-body">{content}</div><div class="preview-nav"><a href="./">← All stories</a><a href="../first-article-review.html">Review Studio →</a></div></main>'
  (out/f'{slug}.html').write_text(shell(title,body))
  card_title=item.get("seo_title") or title
  cards.append(f'<article class="story-card">{picture(slug,True)}<div class="story-copy"><div class="eyebrow">{html.escape(category)}</div><h3><a href="{slug}.html">{html.escape(card_title)}</a></h3><p>{html.escape(item["seo_description"])}</p><small>{reading} min read</small></div></article>')
 aside='<aside class="magazine-aside"><div class="aside-title">FROM THE FIELD</div><h2>Built around the work.</h2><p>Fans. Drives. Controls. The details that matter between the quote and commissioning.</p><a href="https://bigfanguys.com/">Meet Big Fan Guys →</a><div class="aside-section"><h3>Research &amp; regulation</h3><p>24 studies, laws and technical references from original sources.</p><a href="../../resources/">Browse the research shelf →</a></div><div class="aside-section"><h3>Inside this edition</h3><p>Equipment and controls<br>Studies and engineering<br>Installation and access<br>Laws and field practice</p></div></aside>'
 # Feature story plus a supporting story, then a genuine image-led article grid.
 feature=cards[0];support=cards[8] if len(cards)>8 else cards[1]
 body='<main class="wrap magazine-main"><div class="magazine-layout"><div><section class="featured"><h1 class="desk-heading">Featured</h1><div class="feature-story">'+feature+'</div><div class="support-story">'+support+'</div></section><section id="latest"><h2 class="desk-heading">Latest features &amp; field intelligence</h2><div class="story-grid">'+''.join(cards)+'</div></section></div>'+aside+'</div></main>'
 (out/'index.html').write_text(shell('HVLS 360° — The Big Fan Guys Journal',body));return len(items)+1
if __name__=='__main__':print(f'Built {build()} image-led review pages; public catalog unchanged.')
