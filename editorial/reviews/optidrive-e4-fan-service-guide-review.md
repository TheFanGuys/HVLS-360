# Optidrive E4 Fan Service Guide — Source Check and Voice Pass

**Article:** editorial/drafts/optidrive-e4-fan-service-guide.md
**Manuscript SHA-256 at voice pass:** 37aaecf71b374582bbaa95b4542eaa6f3e9cc96e958c97c9118c67311120282f
**Checked:** 2026-11-12, Weekly Writer (research, writer, editor and source-check desks)
**Assignment:** Research pitch #96. Supersedes the shorter production brief in PR #163; that packet's ABB image was rejected by Chris and is not used here. Respects Chris's earlier correction that the fan maker's specified drive is the starting point (closing section).

## Claim / source table

| Claim | Source | Checked |
| --- | --- | --- |
| E4 unveiled Nov 25, 2025 at SPS; first release IP20 frame sizes 1 and 2; availability stated as both end of Q2 2026 and Q3 2026 | [1] https://www.invertekdrives.com/news/general-news/invertek-drives-launches-new-optidrive-e4-variable-frequency-drive | 2026-11-12 |
| E3 stays in full production | [1]; [5] https://www.controlengeurope.com/article/222305/Optidrive-E4-from-Invertek-delivers-increased-VFD-capability.aspx | 2026-11-12 |
| Same foot mounts / identical mounting footprint as E3 | [1]; [3] brochure 85-ESERI-IN V3.02 | 2026-11-12 |
| Dimensions: E3 size 1 173×83×123 mm, size 2 221×110×150; E4 size 1 176×82×136, size 2 222×108×168 | [2] spec page (E4); [3] brochure (both) | 2026-11-12 |
| E4 3-phase 110–115 / 200–240 / 380–480 V; 0.37–4 kW, 0.5–5 HP; IP20, NEMA 1 with kit; CE/UL/UL 61800-5-1; -20 to 50 °C | [2] https://www.invertekdrives.com/variable-frequency-drives/optidrive-e4/specification | 2026-11-12 |
| E3 IP66 up to 22 kW; E4 IP20 only; E4 sizes 3–5 "TBC" | [3] https://www.invertekdrives.com/downloads/Invertek%20Drives%202026%2085-ESERI-IN%20E%20Series%20V3.02.pdf | 2026-11-12 |
| USB-C power-up; in-box programming without mains | [6] features page ("USB-C power up & connectivity"); [5] ("in-box programming without the need for mains power") | 2026-11-12 |
| OptiTools Pro over RJ45 or USB-C; Optistick PRO cloning and Bluetooth PC interface | [2]; [6] | 2026-11-12 |
| Spin start (HVAC features); output phases checked at each enable, can be disabled; standby/sleep; internal PI | [2] | 2026-11-12 |
| I/O: 2 digital + 2 analog/digital in; 1 analog/digital out; 1 changeover relay 250 Vac/30 Vdc | [2]; E3 I/O count from [3] | 2026-11-12 |
| 24 V user supply 100 mA (E3) vs 150 mA (E4) | [3] | 2026-11-12 |
| Last 4 trips with time; pre-trip logging of output current, drive temp, DC bus | [2]; E3 equivalent from [3] | 2026-11-12 |
| "Built-in flight recorder" wording | [1] | 2026-11-12 |
| Per-phase input/output loss checks and real-unit readouts listed for E4, not E3 | [3] comparison; [2] for E4 lines | 2026-11-12 |
| Built-in Modbus RTU, CANopen, BACnet MS/TP on E4; Modbus TCP, EtherNet/IP, PROFINET, EtherCAT optional | [2] | 2026-11-12 |
| E3 built-in Modbus RTU and CANopen | [3] | 2026-11-12 |
| STO SIL 3 on both; drive stays connected to mains with STO active | [3]; [4] https://www.invertekdrives.com/news/manufacturing/dual-channel-safe-torque-off-in-e4-provides-s-i-l-level-3-safety | 2026-11-12 |

## Not confirmed / limits

- Invertek's October 29, 2026 update page (cited in pitch #96) could not be opened from this run. The USB-C no-mains claim is supported instead by the features page and the June 2026 Control Engineering Europe report of Invertek's release.
- Dimension order is taken as height × width × depth, Invertek's usual listing order; the third figure is reported as depth.
- E4 sizes 3–5 dimensions are "TBC" in the brochure; the brochure's E4 power column cites up to 37 kW while the spec page covers 0.37–4 kW for released sizes. Article reports only released sizes.
- No US stock, lead time or exact US order codes confirmed. UL approval comes from the spec page, not a UL listing lookup.
- No claim that any HVLS manufacturer ships the E3 or E4. The article is written conditionally ("if a fan package shows up with…").
- Spin start explanation is the general meaning of the feature; Invertek's spec page lists it without describing behavior.

## Voice pass (editor desk, separate from drafting)

- Banned-word grep: zero hits in body. Em dashes: zero. Bold removed from the three list items (now zero).
- Opening rewritten to lead with the depth difference, a concrete measurement a tech can act on.
- Replaced an unsourced line ("covers the motors on a lot of overhead fans") with a nameplate check.
- Corrected an overstatement that the flight recorder was new; the E3 already logged four trips. Article now says what changed.
- Dropped "dairy barn" scenario in favor of a plain enclosure-rating point.
- One safety line (STO is not lockout) kept where it changes what the tech does. No summary close; ends on the fan maker's approval.

## Lead image

Original HVLS 360 illustration, editorial/media/original/optidrive-e4-fan-service-guide.svg. Generic compact drive front with labeled connections and a side-view depth comparison from listed dimensions. No logo, no brand marking on the device, no copied product photo or drawing; model names appear only as comparison labels outside the drawn device. Rendered to PNG and inspected 2026-11-12; corrected the input label to "2 analog/digital" and moved model labels off the device shapes.

## Recheck — front matter only

Added `publisher_approval: "Required"` to the draft front matter so the CI editorial readiness check passes. Body text unchanged, so the voice pass above still applies. SHA-256 fingerprints were updated by `weekly_article.py --revise`.
