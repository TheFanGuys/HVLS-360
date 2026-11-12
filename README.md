# HVLS 360° — Industry Intelligence

A U.S.-focused industrial air movement magazine from Big Fan Guys. A fast, static, mobile-friendly publication hosted on GitHub Pages, with scheduled research and owner-controlled editorial publication.

**Public site:** https://bigfanguys.com/hvls-360/  
**Editorial office:** https://bigfanguys.com/hvls-360/office/command-center.html  
**All-drafts review desk:** https://bigfanguys.com/hvls-360/office/editorial-queue.html  
**First article review packet:** https://bigfanguys.com/hvls-360/office/first-article-review.html  
**Public reference library:** https://bigfanguys.com/hvls-360/resources/

## What is live

- Responsive magazine homepage, navigation, brand, canonical metadata, social preview metadata, editorial standards and RSS/sitemap.
- Searchable, free public field-reference library linking directly to verified manufacturer manuals, VFD support, AMCA ratings, ASHRAE overviews and federal resources (no copied manuals or licensed photo reuse).
- An approved-only latest-articles section that populates from actual publisher-authorized story releases. No placeholder articles are shown as news.
- GitHub Actions research desk scheduled Tuesdays and Fridays at 08:00 America/Phoenix (15:00 UTC), using public source leads, topical filtering, source preflight, assignments and technical review routing. Raw artifacts remain GitHub Actions artifacts; sanitized lead indexes are separate from publication.
- Editorial office HTML review tools. These are **browser-side workflow aids**, not authenticated publishing accounts or autonomous AI employees.
- Publication scripts that require an explicit recorded owner decision, completed review fields, evidence, and a SHA-256 checksum for the exact draft. Tests reject orphan/tampered article pages, missing approvals, and out-of-sync homepage/RSS/sitemap entries.

## Editorial inventory (November 10, 2026)

Five evidence-backed working drafts, **none published**:

1. **Air movement vs. ventilation** — first full review packet, ASHRAE/DOE/EPA and manufacturer sources, original explanatory SVG pending technical and publisher review.
2. **ABB 2026 IP66/Type 4X drive expansion** — ABB announcements and product leaflet are sourced; drive/OEM compatibility review and photo rights remain open.
3. **CFEI vs. CFM per watt** — AMCA, DOE and eCFR sources, including 2026 verified CFEI thresholds; independent technical copy review and media still pending.
4. **Greenheck revised DS-3/DS-6** — December 2025 announcement and current 2026 manuals; product-specific installation/controls review pending.
5. **Big Ass Fans Powerfoil 6** — official product page and November 2025 installation guide; electrical variants, mounting, fire relay, maintenance and authentic images tracked.

See `editorial/drafts/`, `editorial/reviews/` and `editorial/media/`. Manufacturer photographs linked as candidates **are not cleared for reuse**.

## Weekly articles (current workflow)

A scheduled writer produces one researched article per week and opens a pull request. **Merge to publish, close to reject.** Instructions: `office/WEEKLY-WRITER.md`. Release helper: `office/weekly_article.py`.

The ChatGPT department automations (Art Director, Draft Production, COO) are retired for article production.

## Publishing a reviewed article

Publication does **not** occur from research or from tapping a browser-side approval button. Work in a dedicated release PR:

1. Complete the research, editor and media rights reviews; publisher reviews the exact final Markdown.
2. Store the explicit authorization as `editorial/approvals/<slug>.json` (approval fields, evidence, SHA-256 checksum, owner name and UTC timestamp).
3. Run `python office/publish_approved.py --slug <slug> --approval-file editorial/approvals/<slug>.json`.
4. Run `python office/render_release.py --slug <slug>` and `python office/public_catalog.py --write`.
5. Inspect the generated article HTML and story card, RSS and sitemap, and open the whole release as a PR. GitHub's **Publication Safety Gate** must pass.
6. Authorized owner reviews and merges the entire release through protected `main`.

For exact requirements and caveats, read `office/PUBLISHING_PROTOCOL.md`.

### Owner setup still required

Enable a GitHub ruleset/branch protection for `main` in repository **Settings → Rules → Rulesets** (or Branches, where available): require a PR, require the **Publication Safety Gate / verify** check, restrict bypass and direct pushes, and require authorized editorial review. Review GitHub's semantics for owner-authored versus bot-authored PRs before choosing mandatory review count. The GitHub connection used for this project does **not** have permissions to configure or verify repository protection; these settings are not assumed.

The `office/` HTML tools and `editorial/` files are in a **public repository**. GitHub Pages is not an access-controlled private editorial suite. Do not put unpublished confidential business information, credentials or unlicensed high-resolution media there.

## Tests and release validation

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python office/publication_guard.py
python office/public_catalog.py --check
```

The publication safety workflow runs on relevant PRs and `main` pushes. Research Desk Tests also exercise the offline tools. Browser/iPhone Safari end-to-end manual checks are still needed before declaring the publication complete.

## Editorial direction

Lead with dated, verifiable product developments, applied engineering, original installer knowledge and clean copy. Product review videos are a future department; authentic hands-on tests require real field footage and measurements. Do not present AI-generated simulation as independent testing, reuse photos without rights, pay for services or contact manufacturers without publisher authorization.
