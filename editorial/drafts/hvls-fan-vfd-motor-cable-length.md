---
title: "Drive-to-Motor Distance on HVLS Fans: When the Run Needs a Reactor or Filter"
category: "Installation"
status: "EDITORIAL DRAFT — NOT APPROVED"
publication_allowed: false
publisher_approval: "Required"
primary_market: "United States"
research_checked: "2026-11-17"
seo_title: "HVLS Fan Drive-to-Motor Distance: Reactors and Filters"
seo_description: "How far an HVLS fan drive can sit from the motor at 208, 480 and 600 V, when a load reactor or dV/dt filter goes in, and how to pull the motor run."
---

# Drive-to-Motor Distance on HVLS Fans: When the Run Needs a Reactor or Filter

Measure the conduit run from the drive to the fan motor before you pick a spot for the panel. On a 480 V fan, CaptiveAire calls for a load reactor once that run passes 50 ft and a dV/dt filter past 250 ft. At 600 V those numbers drop to 25 ft and 150 ft [1].

The panel has to come down where someone can reach the disconnect. MacroAir wants the VFD panel for its AirVolution, AirLegacy and AVDX fans mounted outside the blade sweep, because a panel above the blades leaves the disconnect out of reach while the fan runs [3]. EPIC says the same and caps its motor cable at 150 linear ft [2]. Hang a fan in the middle of a bay and the run is the drop from the motor, the stretch across the deck to a wall and the drop to the panel. Measure along the conduit path.

## Why the distance matters

A drive feeds the motor a train of fast voltage pulses. On a long run those pulses reflect at the motor terminals and stack. Eaton puts the peak at up to about double the drive's DC bus, close to 1,500 V on a 480 V drive, and reports pulses above 1,690 V on 460 V drives with more than 600 ft of motor cable [4]. DOE reports spikes of 2,150 V on a 480 V system running 10% high [5].

NEMA MG 1 Part 30 says a general-purpose motor shouldn't lose service life if peaks stay at or under 1,000 V with rise times of at least 2 microseconds [5]. A Part 31 inverter-duty motor is built to take 1,600 V spikes on a 600 V base [4]. Under about 15 ft of cable, DOE says reflected waves generally don't hurt the motor [5]. Past that, supply voltage and carrier frequency set how much room you have.

## Voltage changes the answer

Eaton's critical cable lengths for standard NEMA Design B motors [4]:

- 230 V motors: 600 ft at each carrier frequency listed, 3 to 12 kHz.
- 460 V motors: 125 ft at 3 kHz, 100 ft at 6 kHz, 85 ft at 9 kHz, 75 ft at 12 kHz.
- 575 V motors: 40 ft at 3 kHz, down to 15 ft at 12 kHz.

CaptiveAire's thresholds for a drive mounted in its control panel follow the same pattern [1]:

- 208/230 V: load reactor past 250 ft, dV/dt filter past 400 ft.
- 460/480 V: load reactor past 50 ft, dV/dt filter past 250 ft.
- 575/600 V: load reactor past 25 ft, dV/dt filter past 150 ft.

For very long runs, up to 1,000 ft, CaptiveAire calls for the dV/dt filter and a drive 1 HP larger or one size up [1]. Eaton's answer for total cable past 600 ft is a 208/240 V drive and motor, which keeps the reflected peak under 1,000 V [4].

Carrier frequency moves the line too. In Eaton's table the 460 V critical length falls from 125 ft at 3 kHz to 75 ft at 12 kHz, and Eaton calls 3 kHz the best setting for motor life [4]. On a borderline 480 V run, a lower carrier setting buys you length.

## Where the reactor or filter goes

Mount it at the drive. CaptiveAire wants the load reactor and the dV/dt filter both within 10 ft of the drive output [1], so leave wall space beside the panel. Eaton says reactors at the drive are usually 2 to 4% impedance, and that 0.5 to 1% units may raise the peak at the motor [4].

A drive mounted in the fan makes the run short. CaptiveAire recommends a reactor there too, on 460/480 V motors 7.5 HP and up and 208/230 V motors 15 HP and up, and requires one on every 575/600 V motor [1].

## Pulling the motor run

CaptiveAire's rules for the motor circuit [1]:

- Each motor gets its own steel conduit, kept away from control wiring and incoming power. Motors sharing a conduit void the warranty.
- Run an insulated ground from each drive to its motor.
- No contactor between the drive and the motor. If there's a disconnect there, open it only with the drive stopped.

EPIC also keeps motor cables out of the input-power conduit and out of conduit shared with other motor cables [2]. Thresholds vary by maker, so go by the manual for the fan you're hanging.

If the fan ships with a factory motor cable that's longer than you need, MacroAir says you can shorten it. Run the fan on the full factory length first. If it acts up after you cut the cable, the fault is hard to trace and may not be covered under warranty [3].

### Source record

[1] CaptiveAire, *High Volume Low Speed (HVLS) Fan: HVLS and General Ventilation Fan Control Software, Installation, Operation, and Maintenance Manual*, A0025729 Rev 26, August 2026: https://www.captiveaire.com/manuals/hvls/hvls-oim.pdf

[2] EPIC Fans, *Industrial HVLS Fan User's Manual*, Part No. 6021140F, November 19, 2020: https://epicfan.com/wp-content/uploads/2021/08/6021140F-Industrial-5-Blade-HVLS-Fan-UM-November-2020.pdf

[3] MacroAir Support, *Can I Cut the Provided Motor Cable to a Shorter Length?*, undated: https://support.macroairfans.com/hc/en-us/articles/33688796251675-Can-I-Cut-The-Provided-Motor-Cable-To-A-Shorter-Length

[4] Eaton, *The Reflective Wave Phenomena*, AP040013EN, August 2013: https://www.eaton.com/content/dam/eaton/products/industrialcontrols-drives-automation-sensors/variable-frequency-drives/the-reflective-wave-phenomena-ap040013en.pdf

[5] U.S. Department of Energy, Advanced Manufacturing Office, *When Should Inverter-Duty Motors Be Specified?* Motor Systems Tip Sheet #14, November 2012: https://www.energy.gov/sites/prod/files/2014/04/f15/motor_tip_sheet14.pdf
