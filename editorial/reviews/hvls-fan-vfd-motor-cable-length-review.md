# Drive-to-Motor Distance on HVLS Fans — Source Check, Voice Pass and Technical Check

**Article:** editorial/drafts/hvls-fan-vfd-motor-cable-length.md
**Manuscript SHA-256 at voice and technical pass:** 35e893b7cd315bf74d502248c9f1854cf024ea408a0ed84c2d67fd9992188ac9
**Checked:** 2026-11-17, Weekly Writer (research, writer, editor, source-check and technical desks)

## Why this topic

COO inbox #178 had no comments. Open research pitches #96 (Optidrive E4) and #97 (Greenheck fan array) are already published. Issue #197 links a manufacturer "Top 8" listicle, which is not primary evidence. A search for HVLS, fan-drive and DOE/OSHA developments dated in the last 60 days found nothing usable: the newest items were the VES-Artex HVLS fan (Feb 2026), Vindus FanBrain (Aug 2025), Big Ass Fans Bison (May 2026, residential) and the revised OSHA Heat NEP (April 10, 2026). So this week is an evergreen installation guide. No published article or draft covers drive-to-motor cable length, reactors or dV/dt filters. This is a general wiring topic, not a field guide to one product, so the Nov 13 field-input rule does not apply.

## Claim / source table

| Claim | Source | Checked |
| --- | --- | --- |
| CaptiveAire panel-mounted VFD: load reactor past 250 ft (208/230), 50 ft (460/480), 25 ft (575/600); dV/dt filter past 400 / 250 / 150 ft; up to 1,000 ft use dV/dt and increase drive 1 HP or next size; reactor and filter within 10 ft of drive output | [1] p. 49 https://www.captiveaire.com/manuals/hvls/hvls-oim.pdf | 2026-11-17 |
| CaptiveAire VFD in fan: reactor recommended 15 HP+ (208/230), 7.5 HP+ (460/480), required all HP (575/600) | [1] p. 49 | 2026-11-17 |
| Separate steel conduit per motor away from control and input power; insulated ground drive to motor; no contactor between drive and motor; disconnect only operated with drive stopped | [1] p. 49 | 2026-11-17 |
| Each motor its own conduit or warranty void | [1] p. 34 | 2026-11-17 |
| EPIC: VFD box outside blade arc; max 150 linear ft VFD box to motor; motor cables not with input voltage or other motor cables | [2] p. 25 https://epicfan.com/wp-content/uploads/2021/08/6021140F-Industrial-5-Blade-HVLS-Fan-UM-November-2020.pdf | 2026-11-17 |
| MacroAir: factory motor cable can be shortened; test on full length first, else hard to diagnose and may not be under warranty; AirVolution, AirLegacy, AVDX panel outside blade sweep because disconnect not accessible above blades | [3] https://support.macroairfans.com/hc/en-us/articles/33688796251675-Can-I-Cut-The-Provided-Motor-Cable-To-A-Shorter-Length | 2026-11-17 |
| Peak up to double DC bus, nearly 1,500 V on 480 V drive; pulses above 1,690 V on 460 V drives with >600 ft | [4] https://www.eaton.com/content/dam/eaton/products/industrialcontrols-drives-automation-sensors/variable-frequency-drives/the-reflective-wave-phenomena-ap040013en.pdf | 2026-11-17 |
| Critical cable length table (230 V 600 ft; 460 V 125/100/85/75 ft at 3/6/9/12 kHz; 575 V 40 ft to 15 ft); 3 kHz optimal for motor life | [4] Table 1 | 2026-11-17 |
| NEMA MG 1 Part 31: 1,600 V spikes, 600 V base | [4] | 2026-11-17 |
| Reactor 2–4% typical; 0.5–1% may raise motor peak | [4] | 2026-11-17 |
| 208/240 V drive and motor past 600 ft cumulative keeps reflected peak under 1,000 V | [4] | 2026-11-17 |
| 2,150 V spikes, 480 V system at 10% overvoltage; Part 30 no significant life reduction at ≤1,000 V peak and ≥2 µs rise; reflected waves generally not damaging under 15 ft | [5] https://www.energy.gov/sites/prod/files/2014/04/f15/motor_tip_sheet14.pdf | 2026-11-17 |

## Not confirmed / limits

- NEMA MG 1 itself was not read (paywalled). Part 30 and Part 31 figures are as stated by DOE and Eaton. DOE expresses Part 31 as 3.1× rated voltage (1,426 V for 460 V); the article uses Eaton's 1,600 V on a 600 V base figure only.
- MacroAir support article is undated.
- Eaton's note is from 2013 and DOE's from 2012. The physics and NEMA thresholds they describe are what the article uses; product names from those papers are left out.
- "On a borderline 480 V run, a lower carrier setting buys you length" is the writer's reading of Eaton's table, not a quoted recommendation.
- No Big Fan Guys field note was available for this topic.

## Voice pass (editor desk, separate from drafting)

- Banned-word and em dash grep on body: zero hits. Bold: zero.
- Opening sentence gives the action (measure the conduit run first) with the numbers.
- Rewrote "Measure the conduit path, not the straight line" to a direct instruction.
- Rewrote "shortens the run but doesn't always drop the reactor" (a what-it-isn't sentence) into a direct statement.
- One manual line in the whole article ("go by the manual for the fan you're hanging"). No section about source documents. No summary close; ends on the factory-cable step.
- Body about 810 words.

## Technical check (drive and fan technician pass)

| Claim or element | Source | Change |
| --- | --- | --- |
| 1,690 V pulses on 460 V drives | [4] says the drives "produced" them | "measured" changed to "reports" |
| 0.5–1% reactors and motor peak | [4] says "may" | "can raise" changed to "may raise" |
| 230 V 600 ft critical length | [4] lists 3, 6, 9, 12 kHz only | Reworded to "each carrier frequency listed" |
| CaptiveAire thresholds, 10 ft placement, HP bump, in-fan reactor HP | [1] p. 49 re-read verbatim | No change |
| EPIC 150 ft, blade arc, conduit separation | [2] p. 25 | No change |
| Framing: applies to HVLS fans with remote drives | [1][2][3] are HVLS fan manuals; [4][5] are general drive/motor guidance and are presented that way | No change |

## Lead image

Big Fan Guys field photo art-library/bigfanguys-com/install-service/IMG_5669.webp: a row of wall-mounted fan drive panels, each with its own disconnect, with flex conduit down to an EMT run. Ties directly to the topic (remote drives and their motor runs). No damaged equipment. Panels carry the Go Fan Yourself name; the article is about general wiring and names no brand against it. Not previously used by any article.
