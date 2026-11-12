---
title: "Optidrive E4: What a Fan Service Tech Will Find Inside Invertek's New Small Drive"
category: "Service & VFDs"
status: "EDITORIAL DRAFT — NOT APPROVED"
publication_allowed: false
publisher_approval: "Required"
primary_market: "United States"
research_checked: "2026-11-12"
seo_title: "Optidrive E4 for Fan Service Techs: E3 vs E4"
seo_description: "Invertek's Optidrive E4 adds USB-C programming, spin start and BACnet. What changes from the E3, and what to check before one shows up on a fan job."
---

# Optidrive E4: What a Fan Service Tech Will Find Inside Invertek's New Small Drive

If a fan package shows up with an Invertek Optidrive E4 where you're used to seeing an E3, measure the panel before anything else. Invertek says the E4 bolts to the same foot mounts as the E3, but its listed dimensions run deeper: 136 mm against 123 mm on frame size 1, and 168 mm against 150 mm on size 2 [2][3]. In a tight control enclosure, that's the difference between the door closing or not.

The E3 isn't going away. Invertek says it stays in full production as its core general-purpose drive [1][5].

## What's out now

Invertek unveiled the E4 in November 2025 and put first availability in mid-2026; its launch page gives both end of Q2 and Q3 [1]. The first release covers frame sizes 1 and 2 only, in IP20 [1]. The brochure still lists sizes 3 to 5 as to be confirmed [3].

The current spec sheet lists [2]:

- Three-phase input at 110 to 115 V, 200 to 240 V and 380 to 480 V
- 0.5 to 5 HP (0.37 to 4 kW)
- IP20, or NEMA 1 with an option kit
- UL approval, including UL 61800-5-1
- Operating range of -20 to 50 °C

Check the fan motor nameplate against that range. Then check where the drive will live. The E3 comes in an IP66 version up to 22 kW, and the E4 brochure lists IP20 only [3]. If the drive has to hang in a washdown area or out in the weather, an E4 needs a separate rated enclosure.

## USB-C and the bench setup

Invertek says the E4 powers up over USB-C, so you can program it in the box with no mains connected [5][6]. Its OptiTools Pro software runs over USB-C or RJ45, and there's an Optistick PRO for cloning parameters and a Bluetooth link to a PC [2][6].

For a service shop, that means a replacement drive can be loaded on the bench from the fan maker's parameter file before the truck leaves. You still check every parameter against the fan's documentation once it's on site.

## Fan features worth knowing

Three items on the E4 spec sheet matter on fan work [2]:

- Spin start. Listed under HVAC features. On a big fan that's still turning from the last run or from a draft through the dock doors, the drive can pick up the rotating motor instead of starting from zero.
- Output phase check. The drive checks all three output phases every time it's enabled. If there's a disconnect at the fan and somebody left it open, the drive will tell you. Invertek lets you turn the check off.
- Standby and sleep, plus an internal PI controller, for fans run from a temperature or pressure signal.

The I/O is the same small count as the E3: two digital inputs, two analog-or-digital inputs, one analog-or-digital output and one changeover relay rated 250 Vac or 30 Vdc [2][3]. The 24 V user supply goes from 100 mA on the E3 to 150 mA on the E4, a little more room if you're powering a sensor off the drive [3].

## Fault history

When an E4 trips, it stores the last four trips with times, plus logged data from just before each trip, including output current, drive temperature and DC bus voltage [2]. Invertek's launch material calls this a built-in flight recorder [1].

The E3 already kept the last four trips with pre-trip logging, so the record itself isn't new [3]. The 2026 brochure adds per-phase input and output loss checks and real-unit readouts like PSI for the E4, which it doesn't list for the E3 [3]. Pull the trip history before you call support. Four trips with current and bus voltage tell a fan maker's support line more than a fault code you read off the keypad.

## BACnet built in

The E3 lists Modbus RTU and CANopen as built in. The E4 adds BACnet MS/TP to that list [2][3]. For a facility that wants its fans on the building automation system, that's one less gateway. Ethernet protocols on the E4 (Modbus TCP, EtherNet/IP, PROFINET and EtherCAT) are optional cards, not standard [2]. Check what was ordered before you promise the controls contractor an Ethernet connection.

## Safe Torque Off

Both drives carry STO rated SIL 3 [3][4]. Invertek states that with STO active, the drive stays connected to mains power [4]. STO stops the drive from making torque. It doesn't make the drive or motor safe to touch, so lock out at the disconnect before you open anything.

## Before you swap one in

Same mounting holes don't make an E4 a drop-in for an E3 on a fan. The fan maker set the motor data, ramps, speed limits and control wiring for the drive it shipped. If you're replacing a failed E3 on an HVLS fan, get the fan maker's approval and parameter file for the E4 first.

### Source record

[1] Invertek Drives, *Invertek Drives unveils new variable frequency drive for hybrid and high-efficiency motor control*, November 25, 2025: https://www.invertekdrives.com/news/general-news/invertek-drives-launches-new-optidrive-e4-variable-frequency-drive

[2] Invertek Drives, *Optidrive E4 specification*, checked November 12, 2026: https://www.invertekdrives.com/variable-frequency-drives/optidrive-e4/specification

[3] Invertek Drives, *E Series brochure*, 85-ESERI-IN V3.02, 2026: https://www.invertekdrives.com/downloads/Invertek%20Drives%202026%2085-ESERI-IN%20E%20Series%20V3.02.pdf

[4] Invertek Drives, *Optidrive E4's dual-channel STO provides SIL3 level safety*, May 18, 2026: https://www.invertekdrives.com/news/manufacturing/dual-channel-safe-torque-off-in-e4-provides-s-i-l-level-3-safety

[5] Control Engineering Europe, *Optidrive E4 from Invertek delivers increased VFD capability*, June 2, 2026: https://www.controlengeurope.com/article/222305/Optidrive-E4-from-Invertek-delivers-increased-VFD-capability.aspx

[6] Invertek Drives, *Optidrive E4 features*, checked November 12, 2026: https://www.invertekdrives.com/variable-frequency-drives/optidrive-e4/features
