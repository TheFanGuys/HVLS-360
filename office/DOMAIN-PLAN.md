# HVLS 360 — Domain selection and migration

Updated November 11, 2026. This is an assignment and purchase handoff, not a purchase authorization. Chris uses Namecheap and will make the actual purchase. No domain, price, availability, trademark clearance or account access is claimed.

## Ownership

- Domain & Naming Researcher / Head of SEO: investigate live registrar availability, spelling, readability, first-year price, renewal price and any premium/aftermarket classification. Record dated evidence.
- Marketing & Growth Director: check brand fit and obvious confusion with existing industry publications; propose a clear preferred name.
- Chris: choose the exact domain and purchase it in his own Namecheap account. No credentials or billing details belong in GitHub.
- Domain Migration SEO Specialist: prepare base URL, canonical, sitemap, RSS, structured data, social metadata and internal-link changes.
- Domain / DNS & HTTPS Engineer: after purchase and authorization, coordinate GitHub verification, Namecheap DNS, HTTPS, root/www behavior and rollback.

## Shortlist to investigate

| Candidate | Editorial fit | Registrar status |
|---|---|---|
| hvls360.com | First choice if available at an acceptable ordinary price; exact publication name | Not checked live; no reservation |
| hvls360.net | Short fallback | Not checked live |
| hvls360.news | Clearly signals publication | Not checked live; renewal price must be compared |
| hvls360magazine.com | Longer, explicit trade-publication identity | Not checked live |

Do not infer availability from a missing website or search result. Do not promise SEO rankings from a domain extension. Compare actual registration and renewal totals, not a promotional headline price. Potential name conflicts require separate review; this is not legal clearance.

## Purchase handoff

Give Chris one preferred candidate plus up to two alternatives, dated Namecheap results, first-year and renewal amounts, any premium classification, and the reason for the recommendation. Chris purchases; no auto-renewal or add-ons are authorized here. Selection checkpoint: November 13, 2026, 5 PM Eastern, an internal work target rather than a promised background run. Acquisition can wait until GitHub pilot acceptance as Chris requested.

## Migration follows GitHub acceptance

The site already uses GitHub Pages. A custom domain changes its address, not its hosting platform. Keep Pages while moving the public address.

1. Pass the GitHub pilot acceptance gates in PROJECT-STATUS-2026-11-11.md.
2. Confirm the exact purchased domain and preferred root/www address with Chris.
3. Verify ownership with GitHub before cutover. Prepare DNS using GitHub's current official instructions; do not invent records before the selected hostname is known.
4. Replace the hard-coded Pages base URL in office/article_page.py and dependent catalog output, audit every /HVLS-360/ path and absolute URL, and prepare CNAME only for the chosen domain.
5. Review canonicals, Article structured data, Open Graph, sitemap, RSS, navigation, icon/manifest paths and any indexed URLs.
6. Obtain authorization for the cutover; apply DNS and Pages settings, verify HTTPS and root/www behavior, then test article and Studio URLs on phone.
7. Recheck search-console setup and actual indexing after launch. No ranking, redirect behavior or traffic result is assumed.

## Primary references checked November 11, 2026

- Namecheap domain search: https://www.namecheap.com/domains/domain-name-search/
- GitHub custom domains: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site
- GitHub ownership verification: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
- GitHub DNS/domain configuration: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

No purchase, external contact, DNS change or article publication performed.
