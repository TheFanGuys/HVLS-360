# HVLS 360 Weekly Writer

One new article per week. You research, write and fully prepare it. Chris approves by merging the pull request from his phone. Nothing goes live until he merges.

This replaces the ChatGPT "department" automations for article production.

## 1. Pick one topic

Read `articles/` and `editorial/drafts/` first. Never repeat a topic already covered.

Pick the best of, in this order:

1. An open GitHub issue titled `[Research pitch] ...` that hasn't become an article.
2. A real, dated development from the last 60 days that US HVLS fan installers, facility managers or service techs would care about: a new HVLS, directional or industrial fan product; a VFD or controls change; a DOE/AMCA/OSHA/NFPA/NEC change that touches fan installs; a manufacturer manual revision.
3. An evergreen field guide on installing, wiring, commissioning or servicing HVLS fans, VFDs or controls.

Skip anything you can't back with primary sources (manufacturer pages and manuals, eCFR, OSHA, DOE, AMCA, ASHRAE, NFPA). Don't use forums or SEO listicles as evidence.

## 2. Research

Use web search and fetch. Open every source you cite. Note the date you checked each one. Record exact figures only as the source states them, and name them as manufacturer claims where they are.

## 3. Write the draft

Create `editorial/drafts/<slug>.md`. Use lowercase words joined by hyphens for the slug.

Copy this front matter exactly, filling in the quoted values:

```
---
title: "Headline written for an installer or facility manager"
category: "Installation" | "Controls & Engineering" | "Field Intelligence" | "Industry News" | "Service & VFDs"
status: "EDITORIAL DRAFT — NOT APPROVED"
publication_allowed: false
primary_market: "United States"
research_checked: "YYYY-MM-DD"
seo_title: "Under 60 characters"
seo_description: "Under 160 characters"
---
```

Then the body:

- `# Headline` (same as title)
- 600–900 words. Plain, direct, practical. Write the way an experienced installer explains things to another tradesman.
- `##` section headings, short paragraphs, bullet lists where useful. Bold sparingly. No tables or images inside the body.
- Cite sources inline as `[1]`, `[2]`.
- Finish with `### Source record` listing each source as: `[n] Publisher, *Title*, date if known: https://...`

Rules:

- Don't invent tests, measurements, quotes, rankings, prices or customer stories.
- Don't claim Big Fan Guys tested or installed anything unless a source in this repo says so.
- No internal notes in the text. Readers see every word, so never write "this draft", "pending", "TBD", "Chris says" or reviewer notes.
- Don't copy sentences from sources. Write it in your own words.
- No repetitive safety disclaimers or AI mentions. One line telling readers to follow the manufacturer's manual and local code is enough when it matters.

## 4. Source check

Create `editorial/reviews/<slug>-review.md` with a short table: each material claim, its source URL and the date checked. List anything you couldn't confirm. If a central claim can't be confirmed, change or drop it.

## 5. Pick the lead image

Use only Big Fan Guys photos or original illustrations:

- `art-library/bigfanguys-com/<category>/*.webp` (agriculture, automotive, aviation, government, install-service, manufacturing, warehouse)
- `editorial/media/publisher/bfg-field/*.webp`
- `editorial/media/original/*.svg`

Look at the image before choosing it. Pick one that fits the topic and doesn't misrepresent it. A photo of one brand's fan must not illustrate another brand's product. Prefer an image no published article already uses (check `editorial/media/article-images.json`). Write a short factual alt text and caption. Never use manufacturer or web photos.

## 6. Build the release

```
python office/weekly_article.py --slug <slug> --image <path> --alt "<alt text>" --caption "<caption>"
```

This fills in the manifest, review register, approval record, article page, homepage, RSS and sitemap, then runs every check. It must end with `READY`. If it fails, fix the cause and run it again on a clean checkout of `main`. Don't edit tests to get around a failure.

Open `articles/<slug>/index.html` and read the rendered text once for leftover draft wording or broken formatting.

## 7. Open the pull request

- Branch: `weekly/<slug>`
- Title: `New article: <headline>`
- Body, kept short for a phone: a 2-sentence summary, the topic's reason for being timely, any claim you couldn't confirm, and this line: **Merge to publish. Close to reject.**

Don't merge it yourself. Don't change anything outside what the helper and steps 3–4 produce.

## 8. If there's no good topic

If nothing meets the bar this week, don't force an article. Open an issue titled `Weekly writer: no article this week` and list the topics you rejected and why.
