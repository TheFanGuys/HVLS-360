# Powerfoil 6 — Technical and Copy Review Desk

**Article:** `editorial/drafts/powerfoil6-field-brief.md`  
**Desk review performed:** November 10, 2026  
**Disposition:** Working draft; no technical sign-off or publisher approval recorded.

## Verified source inventory

| ID | Primary source | Verified observations | Scope |
| --- | --- | --- | --- |
| PF6-01 | [Big Ass Fans, Powerfoil 6 product page](https://bigassfans.com/powerfoil-6-hvls-fan/) | Eight diameter choices, web product configuration options, onboard VFD, standard OLED control, BAFCon upgrade and advertised 24-fan control | Manufacturer's current marketing/product listing, reviewed 2026-11-10 |
| PF6-02 | [Big Ass Fans, Powerfoil 6 Installation Guide Rev. D](https://bigassfans.widen.net/view/pdf/7t3u2vurlm/powerfoil6-install-guide.pdf) | Dated 2025-11-19; electrical supply and protection, mount rules, relay arrangements, inspection requirements | Product-specific original manual; parsed text cross-checked, diagrams and supply variants need independent final examination |

## Findings worth carrying into release

1. **Web configurator vs. manual:** Product page currently displays three nominal voltage/phase choices (200–250 V 1Φ, 200–250 V 3Φ, 400–480 V 3Φ). Rev. D manual includes a 575–600 V 3Φ minimum-circuit category. This may be a manual broader than current product selector; **do not interpret as evidence of a current 600 V SKU.** Confirm with submittal or manufacturer before publishing model-order advice.
2. **Wording control:** A lifetime-lubricated gearbox is not maintenance-free fan hardware. Annual inspection requirements are explicit in manual pp. 26–30.
3. **Mounting:** Manual p. 2 rules out single truss/joist/purlin suspension; for bar joists, strut in place of angle iron would require qualifying engineering analysis. Do not generalize these model-specific requirements to other fans.
4. **Fire relay:** Rev. D pp. 23–24 shows both a normally-open and optional normally-closed stop interface. Final interpretation needs fire-alarm designer/field specialist verification and a diagram-based review, not just parsed PDF text.
5. **Source independence:** Both sources are authored by Big Ass Fans. They establish what the company currently sells and instructs—not independently measured performance. No airflow/efficiency comparison is made.

## Expert review assignments

- **HVLS installer/commissioning specialist:** Validate that the draft's practical sequence tracks real install and handoff workflow without implying field testing.
- **Commercial electrical/VFD reviewer:** Read original guide pp. 1, 21–24, especially input supply, isolation and relay logic. Confirm that the written summary does not prescribe a feeder/conductor schedule.
- **Structural/mounting reviewer:** Check bar-joist, beam and Z-purlin descriptions against Rev. D diagrams and mounting kits.
- **Fire systems reviewer:** Check NO/NC relay summary, supervision terminology and acceptance-test framing. Do not treat this desk note as fire protection design approval.
- **Copy editor:** Remove generic claims, ensure all specific assertions carry citations, and inspect manufacturer's latest live links.
- **Media editor:** Choose original photography with permission, or original commissioned technical diagram; do not reproduce product-page photos without license.

## Suggested copy-edit pass
- [x] Reopened the live Big Ass Fans Powerfoil 6 product page; technical documentation remains linked. Verify any changing model options against the actual submittal before release.


- Preserve the field perspective; no unsupported first-person hands-on testing.
- Keep the 2025 manual revision and November 2026 web review clearly distinguished.
- Preserve distinction between manufacturer instructions and regulatory design requirements.
- Avoid a pricing claim; online configurator and quote conditions may change.
- Consider replacing the draft's closing editorial notes with a clean end-of-article source section in the approved release.

**Remaining:** Expert reviews, final source recheck, image rights, publisher sign-off. No article release authorized.


## Primary-document recovery — November 11, 2026

The previous `/docs/powerfoil6/powerfoil6-install-guide.pdf` citation failed with a redirect loop. Recovered the current manual link from the original HTML of [Big Ass Fans Powerfoil 6 Support](https://bigassfans.com/support/hvls-fans/powerfoil-6/). The Widen URL above is its linked document viewer; retrieved the actual PDF from the viewer-provided asset and checked its title/revision and printed pages. No manufacturer PDF or screenshot is republished in this repository.

- Confirmed Rev. D, November 19, 2025. Printed p. 1 and p. 21 include the 575–600 VAC three-phase category; this still does not prove an orderable SKU.
- Confirmed printed p. 2: prescribed angle irons, restriction on strut substitution and prohibition on a single purlin/truss/bar-joist attachment.
- Visually inspected the original diagrams on printed pp. 23–24 (PDF pages 25–26). The normally-open arrangement energizes the relay coil for shutdown; the optional normally-closed arrangement keeps the coil energized for operation. The article's distinction is supported by these manufacturer pages; it is not a generic wiring instruction for other fans.
- Maintenance begins on printed p. 26; the Annual Maintenance Checklist is printed p. 31. Updated manuscript source page range.

The missing-manual retrieval blocker is resolved. Independent specialist judgment, applicability to the supplied equipment, image rights and founder approval remain open. This is a primary-source verification record, not an independent licensed engineering attestation.
