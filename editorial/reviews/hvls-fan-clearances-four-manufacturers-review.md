# Source and technical review: hvls-fan-clearances-four-manufacturers

Checked 2026-11-25. Each manufacturer PDF was read in a research pass, then re-read in an independent claim-by-claim verification pass. Page numbers are the printed page numbers.

## Source check

| Claim | Source | Page | Checked |
|---|---|---|---|
| CaptiveAire: 144 in floor to fan; 60 in top of blade to roof deck; 24 in blade to obstructions above/below; 18 in side of fan to obstruction | https://www.captiveaire.com/manuals/hvls/hvls-oim.pdf (A0025729, August 2026 Rev 26) | 6 | 2026-11-25 |
| CaptiveAire: top fan blade to bottom joist min 24 in | same, Fig. 3 | 7 | 2026-11-25 |
| CaptiveAire: more vertical/horizontal distance between light and blades reduces strobing | same | 6 | 2026-11-25 |
| CaptiveAire: fan at/above diffuser >= 1x diameter; below >= 2x | same | 7 | 2026-11-25 |
| CaptiveAire: 3 ft min to deflector, centered between four sprinklers; max 24 ft diameter in sprinklered buildings incl. ESFR | same | 8 | 2026-11-25 |
| BAF: airfoils >= 10 ft above floor | https://www.cisco-eagle.com/uploads/Big-Ass-Fans-Manuals/basic6-powerfoil8-install-guide.pdf (Rev. B 12/13/2018) | checklist, 2 | 2026-11-25 |
| BAF: winglet-top-to-ceiling table, Basic 6/Powerfoil 8 and Powerfoil 8 Plus | same | 2 | 2026-11-25 |
| BAF: all fan parts >= 2 ft from obstructions, measured from winglet edge; zone free of lights, cables, sprinklers | same | checklist, 2 | 2026-11-25 |
| BAF: diffuser 1x / 2x diameter rule | same | 2 | 2026-11-25 |
| BAF: multiple fans >= 2.5x diameter center to center | same | 2 | 2026-11-25 |
| BAF: no high winds from HVAC or near a large garage door | same | checklist | 2026-11-25 |
| BAF: US sprinkler rule, 3 ft below deflector, centered between four | same | 1 | 2026-11-25 |
| MacroAir: blades >= 10 ft above floor; tips 3 ft from reachable areas | AVD 370 Installation Manual 90-30071-00 Rev A-10, date 031026 | 2, 6, 7 | 2026-11-25 |
| MacroAir: wall/obstruction >= 1.5x diameter | same | 6 | 2026-11-25 |
| MacroAir: drop table by diameter and slope | same | 7, 8 | 2026-11-25 |
| MacroAir: diffusers present, 1.5x diameter from any airflow source; no high winds from large garage doors or HVAC | same | 2 | 2026-11-25 |
| MacroAir: avoid mounting directly under lights/skylights (strobe); 3 ft below sprinkler, central to quadrant | same | 6 | 2026-11-25 |
| Hunter DDI: blade >= 10 ft above floor; 20-24 ft fan best at 20-30 ft | https://ventiladoresindustriales.hunterfan.com/wp-content/uploads/sites/7/2022/09/3.-ddi-install-manual-rev010421-english.pdf (Rev121820) | 6, 10 | 2026-11-25 |
| Hunter: 25% of diameter from ceiling | same | 6 (p. 7 figure says 20-25%) | 2026-11-25 |
| Hunter: tips 5 ft from reachable areas; 2 ft blades to light fixture; avoid under lights/skylights | same | 6 | 2026-11-25 |
| Hunter: 2 ft blade clearance from any obstruction | same | 10 | 2026-11-25 |
| Hunter: vertical discharge rules; horizontal discharge path; no wind exposure | same | 6 | 2026-11-25 |
| Hunter: 3 ft below deflector, centered between 4 sprinklers | same | 6 | 2026-11-25 |
| Hunter: fan power to 5 ft outside swept area; VFD panel 5 ft outside swept area | same | 10, 16 | 2026-11-25 |

## Could not confirm / limits

- Big Ass Fans' own copy of this guide on bigassfans.com could not be fetched this run. The article uses a distributor-hosted copy (Cisco-Eagle) of the Rev. B December 2018 guide. A newer revision may exist.
- MacroAir manual is hosted on MacroAir's Shopify CDN; a link from macroairfans.com to the file was not confirmed this run.
- Hunter's ceiling clearance reads 25% of diameter on p. 6 and 20-25% in the p. 7 figure. The article says "about a quarter."
- Fan-to-fan spacing for CaptiveAire, MacroAir and Hunter not stated in readable text (Hunter's chart is a figure with unlabeled A/B values), so the article gives only the Big Ass Fans rule.
- CaptiveAire's lighting table (Table 2) units and mapping to Figure 1 were unclear; the article does not use those numbers.
- MacroAir's "3 ft minimum blade clearance" note on p. 7 doesn't say clearance to what; not used.

## Technical check

| Claim or element | Source | Change made |
|---|---|---|
| Hunter ceiling clearance "at least 25 percent" | Hunter p. 6 vs p. 7 figure | Changed to "about a quarter," "roughly 6 ft" on a 24 ft fan |
| BAF 2 ft rule applied to "blades" | BAF p. 2 says "all fan parts" | Reworded to "every part of the fan" |
| Hunter "high-discharge unit" | Hunter p. 6 says vertical discharge (AC units, evaporative coolers) | Reworded |
| "Overhead doors" | BAF and MacroAir say "large garage door" | Reworded |
| Sprinkler rule applied to all four identically | MacroAir p. 6 says "central to each sprinkler quadrant," not deflector/four heads | Split MacroAir wording out |
| MacroAir 1.5x airflow rule | MacroAir p. 2 frames it "if diffusers are present" | Added condition |
| Worked examples: 30 ft deck, 24 ft Powerfoil 8 Plus = 22 ft winglet top; CaptiveAire = 25 ft blade top; MacroAir 24 ft fan = 36 ft; 2x of 24 ft = 48 ft; 2.5x of 24 = 60 ft, of 12 = 30 ft | arithmetic on sourced figures | Checked |
| Lead image | Big Fan Guys gallery photo warehouse/IMG_9670: five-blade HVLS fan under a joist deck with high-bay lights. No brand visible. Caption names no manufacturer and no clearance claim | None |
