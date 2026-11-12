---
title: "HVLS Fans Under Sprinklers: Placement, Clearance and the Fire Alarm Interlock"
category: "Installation"
status: "APPROVED FOR PUBLICATION"
publication_allowed: true
primary_market: "United States"
research_checked: "2026-11-12"
seo_title: "HVLS Fans Under Sprinklers: NFPA 13 and the Interlock"
seo_description: "NFPA 13 placement and clearance rules for HVLS fans, the FM fire tests behind the shutdown rule, and how two manufacturers wire the fire alarm relay."
---

# HVLS Fans Under Sprinklers: Placement, Clearance and the Fire Alarm Interlock

Before you hang an HVLS fan in a sprinklered building, find out who's supplying the waterflow relay and which way its contact has to switch. NFPA 13 requires every HVLS fan under sprinklers to shut down on a waterflow alarm, and two manufacturers' current instructions wire that signal in opposite ways [1][4][5].

## The four NFPA 13 rules

NFPA 13 picked up HVLS language in its 2013 edition, based on a 2007 test program run by the Fire Protection Research Foundation and a group of property insurers [1]. NFSA and CaptiveAire's current manual summarize the requirements the same way [1][4]:

- Fan diameter tops out at 24 ft.
- Center the fan roughly between four adjacent sprinklers.
- Keep at least 3 ft of vertical clearance from the fan to the sprinkler deflectors.
- Interlock every fan to shut down on a waterflow alarm, following NFPA 72.

CaptiveAire states the rules apply with ESFR heads too [4]. The section number has moved between editions (it was 11.1.7 in 2013), so pull the edition your AHJ adopted when you need to cite it on a submittal [1].

The 3 ft sprinkler clearance sits on top of the fan maker's own numbers. CaptiveAire, for example, lists 60 in from the top of the blade to the roof deck, 24 in from the blade to obstructions above or below, 18 in from the side of the fan to any obstruction and 144 in from the floor to the fan [4]. Lay out both sets before you pick a mounting point.

## Why the shutdown rule exists

FM Global ran four large-scale fire tests with a 24 ft, six-blade fan at its full 66 rpm under a 40 ft ceiling, over a double-row rack of cartoned plastic [2]. With the fan running and no shutdown, sprinkler performance was inadequate. The worst case was the fan centered over the rack with 10 ft of clearance above 30 ft storage: 12 sprinklers opened and damage went past the test criteria [2].

Run the same setup with the fan shut off 90 seconds after the first sprinkler opened, and only four sprinklers operated. FM chose that delay to simulate a waterflow alarm [2]. At full speed the fan pushed air down at up to 14.8 ft/s at the top of the rack. Half speed cut that peak by about 60%. FM's conclusion is about shutting the fan off [2].

FM says the results cover only the setups it tested and aren't installation guidance [2]. Read them as the reason the rule exists.

## Check the contact logic before you pull wire

CaptiveAire's control package closes a dry contact to stop the fans. Close a contact across terminals IL2A and IL2B on the control board and every HVLS fan stops, every HMI shows EMERGENCY INPUT ACTIVE and an alarm sounds [4]. IL2A is a 24 VDC source from the panel, fused at 200 mA, so the relay contact you land there has to be dry. The emergency input overrides every other mode [4].

MacroAir wants a normally closed relay that opens to stop the fan [5]. On most of its current fans you land the relay on the orange and orange/white pair in the CAT5 to the remote, usually at ground level. On AirLynk you pull the jumper on the terminal block outside the panel and land the relay there. Leave that jumper in and the fan runs normally but never sees the alarm. MacroAir doesn't recommend landing it on the VFD terminals except with 0-10 V analog remotes [5].

The standard AirLite VFD remote has no fire alarm terminals, so you need a separate device that drops the 120 V feed to the VFD controller. And one relay can shut down several fans only if they're the same model. Mixed models or fan ages mean a call to their tech support first [5]. Follow the manual for the exact model and the code your AHJ enforces.

## Restart and vent fans

On CaptiveAire's system, opening the contact doesn't restart anything by default. Someone has to press CLEAR on an HMI, and one press releases the whole control package. The fans go back to whatever mode they were in before the alarm [4]. An Auto Clear setting skips that step. Ask the owner which they want and write it on the turnover sheet.

The same CaptiveAire panel can run vent fans. With its vent emergency setting on, those fans run at max speed during an emergency input. With it off, they stop [4]. That's the fire protection engineer's call.

## Who supplies the relay

NFPA 72 didn't mention HVLS fans until its 2019 edition, which added a requirement that they shut down on sprinkler waterflow in the area the fans serve [1][3]. That last part matters on a big building with several sprinkler zones. Ask which zone's flow switch drops which fans.

NFSA's John Swanson argues every building with HVLS fans should have a dedicated-function fire alarm control unit watching waterflow [1]. On an older warehouse with no fire alarm panel, raise it with the owner before you bid the job.

Get the relay location and contact type from the fire alarm contractor before rough-in. Then run the shutdown with them during their acceptance test and record which fans stopped.

### Source record

[1] National Fire Sprinkler Association, John Swanson, *HVLS Fans and Fire Sprinklers*, January 24, 2022: https://nfsa.org/2022/01/24/when-hits-the-hvls-fan/

[2] FM Global Research Division, Benjamin Ditch, *Impact of a High Volume Low Speed Fan on Sprinkler Performance in Rack Storage Fires*, January 2011: https://fm.com/-/media/project/publicwebsites/fm/files/resources/research-technical-reports/hvls_10611.pdf

[3] John Swanson, *Significant Changes to NFPA 72*, 2019 Fire Prevention Institute presentation: https://portals7.gomembers.com/wfc-wsafc/DocumentLibrary.aspx?EntryId=2667&Command=Core_Download

[4] CaptiveAire, *HVLS and General Ventilation Fan Control Software Installation, Operation and Maintenance Manual*, Doc. A0025729 Rev 26, August 2026: https://www.captiveaire.com/manuals/hvls/hvls-oim.pdf

[5] MacroAir Technical Support, fire alarm relay wiring article, undated: https://support.macroairfans.com/hc/en-us/articles/27748049512859
