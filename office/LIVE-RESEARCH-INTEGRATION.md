# One-tap Research Import — Security and Editorial Contract

The research workflow will write a **public** sanitized `office/research-latest.json` containing only unverified news titles, source URLs, publication dates and research department names. This file is publicly readable on GitHub Pages. Do not put confidential leads, customer information, private notes, credentials, sponsor prospects or unpublished business plans into this index.

The Publisher Command Center button **Load latest research** fetches this same-origin JSON and adds unseen URLs to its browser-local review queue. It never approves or publishes articles. Manual Markdown import remains available as a fallback.

The workflow now needs `contents: write` to commit the public index on main; the private Markdown artifact remains available to repository users. This is an intentional, narrowly scoped increase in repository write permissions, and should be reviewed before merging.

The initial JSON contains no invented stories. The first live run must be checked for source quality. Zero leads are displayed as zero leads.

No advertiser outreach, paid campaigns, editorial publication or automatic external sharing is authorized.
