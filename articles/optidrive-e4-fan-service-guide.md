---
title: "Invertek's Optidrive E4: What the New General-Purpose Drive Is Built For"
category: "Service & VFDs"
status: "APPROVED FOR PUBLICATION"
publication_allowed: true
publisher_approval: "Required"
primary_market: "United States"
research_checked: "2026-11-12"
seo_title: "Invertek Optidrive E4: Applications, Setup and E3 Changes"
seo_description: "What Invertek built the Optidrive E4 for, how you set one up without a display, and what changed from the E3 for HVAC, fan and pump work."
---

# Invertek's Optidrive E4: What the New General-Purpose Drive Is Built For

The Optidrive E4 is Invertek's new small general-purpose drive, the step up from its E3 [1][7]. It isn't a fan drive. Invertek's 2026 brochure gives it three application modes [3]:

- Industrial: conveyors, mixers, treadmills
- Fan: air handling units, ventilation fans, circulating fans, kitchen extract, air curtains
- Pump: dosing, transfer and borehole pumps, pools, spas and fountains

So the places a fan or HVAC contractor is likely to meet one are air handlers, exhaust fans and air curtains. Invertek doesn't list overhead HVLS fans for it, and most HVLS fans ship with a drive and controls the fan maker picked and programmed.

## There's no screen to read

Look at the front of an E4 and you'll find start, stop and up/down buttons, an RJ45 port and two status lights marked error and run [7]. Invertek's product images of sizes 1 and 2 show no numeric readout. Its spec tables still list a built-in 7-segment display [2][3], so check the unit in front of you, but don't plan on reading speed or fault codes off the drive.

You set it up and read it with other tools. Invertek says the E4 powers up over USB-C for setup with no mains connected, and works with a phone app [1][5][6]. OptiTools Pro runs on a PC over USB-C or RJ45, and the Optistick PRO handles Bluetooth and parameter cloning [2][6]. Basic setup is 14 parameters, with up to 50 available [6]. If you want a readout at the panel, the brochure lists an optional TFT remote keypad [3].

## What's out now

Invertek unveiled the E4 in November 2025. Its launch page gives first availability as both end of Q2 and Q3 2026 [1]. The first release is frame sizes 1 and 2, IP20, 0.5 to 5 HP (0.37 to 4 kW) [1][2]. Sizes 3 to 5 are still marked to be confirmed [3].

Input options in the brochure's order tables [3]:

- 110 to 115 V single-phase, using a voltage doubler, up to 1.5 HP
- 200 to 240 V single-phase or three-phase
- 380 to 480 V three-phase

It's UL approved, including UL 61800-5-1, and runs from -20 to 50 °C [2]. It's IP20, or NEMA 1 with an option kit [2]. The E3 comes in an IP66 version and the E4 doesn't yet [3], so a wet or outdoor spot still needs a rated enclosure.

## Same footprint, deeper box

Invertek says the E4 uses the same mounting as the E3 [1]. It's deeper, though: 136 mm against 123 mm on size 1, and 168 mm against 150 mm on size 2 [3]. Measure the panel depth before you swap one for an E3.

## What Fan mode brings

The brochure's HVAC features are spin start, variable torque and belt failure detection, plus a bidirectional fire mode [2][3]. Spin start picks up a motor that's already turning, like an exhaust fan windmilling in a draft. Belt failure detection matters on belt-drive air handlers. There's also an internal PI controller and a sleep function for fans run off a temperature or pressure signal [2].

BACnet MS/TP is built in, next to Modbus RTU and CANopen [2]. The E3 doesn't list BACnet, so an E4 on an air handler can talk to the building system without a gateway. Ethernet protocols are optional cards [2].

## Faults and safety

The E4 keeps its last four trips with times, plus logged current, drive temperature and DC bus voltage from just before each one [2]. Invertek calls it a flight recorder [1]. With no readout on the drive, you pull that history with OptiTools or the app [2][6].

Both the E3 and E4 have Safe Torque Off rated SIL 3 [3][4]. Invertek notes the drive stays connected to mains with STO active [4]. STO stops torque. It doesn't make anything safe to touch, so lock out at the disconnect.

## If someone proposes one for a fan

An E4 makes sense where you'd use an E3 or another small general-purpose drive: an exhaust fan, an air curtain, a small air handler. On a fan that came with its own drive package, including an HVLS fan, the fan maker's drive and settings come first. Get their approval and parameter file before you put any other drive on it.

### Source record

[1] Invertek Drives, *Invertek Drives unveils new variable frequency drive for hybrid and high-efficiency motor control*, November 25, 2025: https://www.invertekdrives.com/news/general-news/invertek-drives-launches-new-optidrive-e4-variable-frequency-drive

[2] Invertek Drives, *Optidrive E4 specification*, checked November 12, 2026: https://www.invertekdrives.com/variable-frequency-drives/optidrive-e4/specification

[3] Invertek Drives, *E Series brochure*, 85-ESERI-IN V3.02, 2026: https://www.invertekdrives.com/downloads/Invertek%20Drives%202026%2085-ESERI-IN%20E%20Series%20V3.02.pdf

[4] Invertek Drives, *Optidrive E4's dual-channel STO provides SIL3 level safety*, May 18, 2026: https://www.invertekdrives.com/news/manufacturing/dual-channel-safe-torque-off-in-e4-provides-s-i-l-level-3-safety

[5] Control Engineering Europe, *Optidrive E4 from Invertek delivers increased VFD capability*, June 2, 2026: https://www.controlengeurope.com/article/222305/Optidrive-E4-from-Invertek-delivers-increased-VFD-capability.aspx

[6] Invertek Drives, *Optidrive E4 features*, checked November 12, 2026: https://www.invertekdrives.com/variable-frequency-drives/optidrive-e4/features

[7] Invertek Drives, *Optidrive E4 Variable Frequency Drive* (product page and product images), checked November 12, 2026: https://www.invertekdrives.com/variable-frequency-drives/optidrive-e4
