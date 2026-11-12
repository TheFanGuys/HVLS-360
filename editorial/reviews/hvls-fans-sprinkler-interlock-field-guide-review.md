# HVLS Fans Under Sprinklers — Source Check and Voice Pass

**Article:** editorial/drafts/hvls-fans-sprinkler-interlock-field-guide.md
**Manuscript SHA-256 at voice pass:** eedf31b5a18570aba8c46e641659c46b53128fc4e184530c0e4e04b0dd589dea
**Checked:** 2026-11-12, Weekly Writer (research, writer, editor and source-check desks)

## Why this topic

No COO inbox instructions this week. Open pitch #97 (Greenheck MOA/CPF fan array) was passed over: it covers ducted AHU fan arrays rather than HVLS work, and the pitch itself requires submittal data and engineering review that can't be produced from public sources. Pitch #96 (Optidrive E4) already has draft PR #163. No published or drafted article covers HVLS placement under sprinklers or the fire alarm interlock.

## Claim / source table

| Claim | Source | Checked |
| --- | --- | --- |
| NFPA 13 HVLS language added in 2013 edition (Sec. 11.1.7), based on 2007 FPRF / property insurer tests | [1] https://nfsa.org/2022/01/24/when-hits-the-hvls-fan/ | 2026-11-12 |
| Max 24 ft diameter; centered approx. between four adjacent sprinklers; 3 ft min. vertical clearance to deflectors; interlock to shut down on waterflow per NFPA 72 | [1] and [4] p. 8 https://www.captiveaire.com/manuals/hvls/hvls-oim.pdf | 2026-11-12 |
| Rules apply with ESFR sprinklers | [4] p. 8 | 2026-11-12 |
| CaptiveAire clearances: 60 in blade to deck, 24 in blade to obstructions above/below, 18 in side, 144 in floor to fan | [4] p. 6 Table 2 | 2026-11-12 |
| FM tests: 24 ft six-blade fan, 66 rpm max, 40 ft ceiling, CUP in double-row rack, 30 ft storage (Tests 1–3); fan running without shutdown gave inadequate performance; Test 2 (centered, 10 ft clearance) 12 sprinklers and damage beyond criteria; Test 3 shutdown at 1 min 30 s gave 4 sprinklers; 90 s simulated waterflow alarm; 4.5 m/s (14.8 ft/s) peak downward velocity; half speed ~60% lower peak; no formal installation recommendations | [2] https://fm.com/-/media/project/publicwebsites/fm/files/resources/research-technical-reports/hvls_10611.pdf | 2026-11-12 |
| CaptiveAire emergency input: closing dry contact across IL2A/IL2B stops all HVLS fans, HMI message and alarm; IL2A 24 VDC source, 200 mA PTC; highest-priority command | [4] pp. 35, 38, 60 | 2026-11-12 |
| CaptiveAire restart: default requires CLEAR after contact opens; one HMI releases package; fans return to prior mode; Auto Clr Shtdwn option; vent fans max speed or off per Vent Emg setting | [4] pp. 56, 60 | 2026-11-12 |
| MacroAir: normally closed relay; orange and orange/white CAT5 pair; AirLynk jumper on outside terminal block; VFD terminals only recommended for 0-10 V analog remotes; AirLite standard VFD remote has no fire alarm terminals, needs device dropping 120 V; one relay for several fans only if same model | [5] https://support.macroairfans.com/hc/en-us/articles/27748049512859 | 2026-11-12 |
| NFPA 72 did not address HVLS fans until 2019 edition; requirement to shut down on waterflow in area served by fans | [1]; wording from [3] https://portals7.gomembers.com/wfc-wsafc/DocumentLibrary.aspx?EntryId=2667&Command=Core_Download | 2026-11-12 |
| Dedicated-function FACU recommendation | [1] (Swanson's opinion, attributed as such) | 2026-11-12 |

## Not confirmed / limits

- NFPA 13 and NFPA 72 current-edition text was not read directly (NFPA standards are behind a login). Requirements are taken from NFSA, the 2019 NFPA 72 presentation and CaptiveAire's August 2026 manual, which agree. The article tells readers section numbers vary by edition and names only the 2013 number.
- The NFPA 72 section number (21.8 in the presentation) is left out of the article because the edition it applies to isn't stated clearly in the source.
- MacroAir's support article shows no title or date; cited as undated.
- "Leave that jumper in and the fan runs normally but never sees the alarm" is the writer's reading of MacroAir's AirLynk instruction (relay replaces the jumper on a normally closed loop), not a quoted line.
- The closing advice (get relay details before rough-in, test with the fire alarm contractor at acceptance, record which fans stopped) is editorial advice, not a sourced requirement.

## Voice pass (editor desk, separate from drafting)

- Banned-word grep: zero hits in body. Em dashes: zero. Bold: zero.
- Cut "Two more MacroAir details catch people" lead-in and a Controller 30 detail to stay near 900 words.
- Rewrote three "X, not Y" contrasts ("not the fan crew," "not on install day," "explain the rule, don't replace it") into direct statements.
- Removed a "still" hedge in the FM half-speed sentence.
- Moved the AirLynk jumper warning next to the instruction it belongs to; kept one manual/code line only.
- Opening sentence gives the action (find who supplies the relay and its contact type). No summary close; ends on the acceptance-test step.

## Lead image

Original HVLS 360 illustration, editorial/media/original/hvls-fans-sprinkler-interlock-field-guide.svg. Generic fan, sprinkler line, riser, waterflow switch, fire alarm control unit and fan controller. No brand, logo or product replica. Rendered to PNG and inspected 2026-11-12; downrod moved behind branch line after first render.
