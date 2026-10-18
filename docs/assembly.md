# Assembly and first power-up

**Use ST TS391RIYLT for U3:** pin 1 is RX_REF and pin 4 is RX_ISO.
Revision metadata and test-point exclusions are verified; the [maintenance notes](manual-review.md) cover future changes and exports.
The procedure below is a first-power plan for a future assembled Rev E, not a
record that Rev E hardware has already passed physical tests.

Use the BOM exported from the released schematic for **one board**. Distributor
minimum order quantities are purchasing constraints, not the quantity to solder.
Connector, socket, mounting hardware and module choices must match the actual
footprints. Test points and mounting holes are PCB features, not purchased parts.
The grouped BOM contains 35 SMD parts, two connectors and one module position;
test pads are excluded by the schematic's native BOM settings. The module position
also requires two 1×8 female socket strips at 2.54 mm pitch, and matching male
headers if these are not already fitted to the module. Obtain four suitable M2
fixings and spacers separately; check underside clearance and enclosure geometry.

J1 and J2 both use JST **B2B-XH-A**, the vertical XH header at **2.50 mm** pitch.
Use matching XHP-2 cable housings and appropriate XH contacts. J1 carries external
5 V (pin 1 GND, pin 2 +5 V); J2 carries VBus (pin 1 VBUS_B, pin 2 VBUS_A).
Label both cables: these identical housings do not prevent exchanging the two
connections. VBus polarity independence does not make J2 a 5 V power input.

`fabrication/cpl.csv` contains exactly the 35 SMT component positions. TP1–TP9,
J1/J2 and U7 are excluded by the export filter, using the matching IPC-2581 SMT
inventory. TP1–TP9 are now also excluded natively in both schematic and PCB.
The unfiltered native export contains 38 positions (35 SMT plus J1/J2/U7), so
continue using the filtered file for SMT-only assembly.

## Assembly

1. Inspect the bare board for damage, copper bridges and blocked holes. Check the
   revision against the fabrication archive and its checksum manifest.
2. Fit the SMD parts on the front. Use flux and inspect the SOT-23-5/6 pins for
   bridges. Check IC orientation from the pin-1 marker, not the printed marking.
3. Fit **TS391RIYLT** at U3, with physical IN- on pad 1 and OUT on pad 4.
4. Fit C13 before the module sockets; inspect its joints and clearance before
   hiding it under the module. Fit J1/J2 and the two module socket rows.
5. Inspect D2/D3: they must be BAT54S series pairs in the specified SOT-23 pinout.
   Do not substitute another BAT54 suffix based on package appearance.
6. Fit only one supported module. The firmware must hold TX HIGH before VBus is
   connected. Receiving alone does not require granting permission to transmit.

Use U4 ISO7221ADR as the reference BOM part. Do not fit an isolator with default
LOW outputs merely because it has the same footprint. Other isolators and speed
grades require a pin/function/default-state check; they are not blanket-approved
alternates in this release.

## Unpowered checks

Disconnect the module USB, external supply and both VBus wires. Inspect the
assembly, confirm supply polarity and look for supply-to-ground shorts. Capacitors
can produce a temporary low resistance while charging from a meter. Verify that
the two ground domains were not bridged by solder, mounting hardware or test leads.
An ohmmeter continuity check does not prove a certified isolation voltage.

## First power with VBus disconnected

Power from one source only: USB **or** a current-limited, regulated 5 V supply at
J1. The initial limit must accommodate the selected module's startup and radio
peaks; a limit too low can itself cause repeated resets. Observe current and stop
if the supply limits unexpectedly, a component heats or a rail is wrong.

Measure DC with the black lead at the ground shown in each row. Never bridge TP3
and TP9 with a scope, USB adapter or other instrument ground.

| Measurement | Black lead | Expected nominal result |
|---|---|---|
| TP7 / +5V | TP9 / GND | About 5 V |
| TP8 / +3V3_MCU | TP9 / GND | About 3.3 V from the module |
| TP1 / VISO_RAW | TP3 / GND_ISO | About 5 V; use U1 datasheet tolerances |
| TP2 / +3V3_ISO | TP3 / GND_ISO | About 3.3 V |
| C9 pin 1 / RX_REF | TP3 / GND_ISO | About 0.62 V |
| TP4 / RX_ISO | TP3 / GND_ISO | LOW with no bus, typically near 0 V |
| TP5 / TX_GATE | TP3 / GND_ISO | Near 0 V with TX idle HIGH |

These are diagnostic nominal values, not calibrated acceptance limits. A wrong
reference, HIGH RX with no bus, or nonzero gate command must be investigated
before connecting the controller. In particular, do not attempt to compensate
for an incorrect comparator pinout by changing UART inversion.

## Controller connection

After the preceding checks, connect J2 to the controller's designated VBus
terminals, following its manual. Start with firmware that only receives. Verify
valid telemetry and continuing controller operation. Enable TX only with bus
arbitration and a known read command for the specific controller. Do not change
regulation settings as part of a wiring test.

Rev E requires bench checks after assembly. Transient waveforms, EMC, extreme
temperatures, long cables and all power-up/down sequences have not been qualified.
