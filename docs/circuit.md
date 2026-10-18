# Circuit and interfaces

## Power and isolation

J1 supplies 5 V to the module and U1. J1 pin 1 is `GND`, pin 2 is `+5V`.
U1, RECOM R05CTE05S-CT, transfers power across its internal transformer to
`VISO_RAW` / `GND_ISO`. U2, MIC5235-3.3YM5-TR, supplies the isolated 3.3 V rail.
U4, ISO7221ADR, carries one signal in each direction across a separate digital
isolation barrier. Its bus-side VCC1 uses `+3V3_ISO`; MCU-side VCC2 uses the
module's `+3V3_MCU`.

The two grounds have no conductive connection on the carrier. Connecting an
instrument ground or external wire between them bypasses that separation.
Do not infer a complete board safety rating from either IC's component rating.
Only connect the intended low-voltage controller bus.

The module USB input and J1 share the 5 V rail. There is no reverse-polarity
protection, fuse or USB/external supply power multiplexer. Use a regulated 5 V
supply and verify connector polarity. Disconnect external power before USB.

## Receive path

J2 connects to the two VBus wires; either polarity is accepted. D2 and D3 are
**series-connected dual** Schottky diodes forming a bridge. BAT54S is not
interchangeable with BAT54A, BAT54C or a single BAT54. D1 is a bidirectional TVS.

R2/R3 divide the rectified voltage. U3 compares `SENSE` against `RX_REF`, derived
from R5/R6. R4 adds positive feedback, C10 filters the sense input, and C9 filters
the reference. R12 pulls up the open-collector comparator output. U4 and R7 carry
the result to the module RX pin. The nominal reference is about 0.623 V at a
3.3 V isolated supply. Nominal comparator thresholds at `VBUS_RECT` are around
2.0–2.3 V; these are calculated values, not measured VBus waveform limits.

The TS391RIYLT **R variant** pin assignment is mandatory; see the erratum.
An input above the supply is not by itself evidence of valid operation: the ST
common-mode conditions still apply. The reference input remains in range in the
intended circuit. Most published precision and delay limits are specified at
5 V, so calculations at 3.3 V do not establish worst-case timing performance.

## Transmit path

R8 holds MCU TX HIGH. U4 carries TX to U6, SN74AUP1G97DBVR. With its A input tied
LOW, U6 implements `Y = READY AND NOT TX`. U5, MAX809TEUR+T, keeps READY LOW
during insufficient isolated supply and its startup delay. R9 holds READY LOW
when undriven. R10 drives Q1 through a gate resistor and R11 discharges the gate.
Q1 sinks the rectified bus when enabled.

| READY | TX | Q1 command |
|---:|---:|---|
| 0 | Either | Off |
| 1 | 1 | Off; UART idle |
| 1 | 0 | On; active bus sink |

This hardware inhibit reduces startup/brownout risk; it is not a proof of
glitch-free behavior for every supply ramp. Firmware must start with TX HIGH,
wait for a valid bus grant, observe protocol timing and stop on lost ownership.
The physical sink must never be driven as an ordinary continuously active UART
on a shared VBus without arbitration.

## Module and mechanics

The carrier accepts one module at a time on two 8-pin, 2.54 mm socket rows.
The pin names and GPIO numbers differ between D1 mini and S3 Mini; use the table
in the README and the exact module revision. A board with the same outline is not
automatically electrically compatible. Do not fit two MCU modules together.

The board is 64 × 50 mm, two copper layers, 1.6 mm FR-4, with four isolated plated
2.2 mm M2 mounting holes. Ground stitching joins each domain's own top and bottom
pours. It must not join the two domains. Preserve the antenna copper keepout and
check the enclosure and metal mounting hardware against both domains.

C13 is fitted on the component side near the module socket before the sockets
are soldered. Check physical clearance under the module; its nominal package
height is not a guarantee for an arbitrary substitute.
