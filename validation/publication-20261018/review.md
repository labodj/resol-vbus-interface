# Rev E checks and remaining tests

Checked on **18 October 2026**, with KiCad 10.0.6. The design files pass the
checks below. Rev E is still a prototype: I have not yet assembled or bench-tested
this revision.

## CAD results

- ERC and DRC: **0 errors, 0 warnings**.
- No unrouted connections or schematic/PCB mismatches.
- No shorted nets, single-pin nets, orphan items or symbol overlaps found.
- **52 physical pin/net assignments**, **9 critical part numbers** and
  **3 regression tests** checked.
- Schematic and both copper layers visually checked.

U3 uses the TS391RIYLT connections: pin 1 is `RX_REF`, pin 4 is
`RX_ISO`. J1 and J2 both use JST XH B2B-XH-A headers at 2.50 mm pitch. All nine
test points are excluded from BOM and position exports in both the schematic
and PCB. Title blocks and silkscreens identify Rev E.

## Layout

The board is 64 x 50 mm, with two nominal 35 micrometre copper layers and
1.6 mm overall thickness. The MCU and isolated grounds remain separate. The
back ground plane is continuous beneath the local U3 routing. The J1/TP7 supply
branch and connector routing show no obvious new return-path detour.

TP7 is at (21.2, 41.6) mm and TP9 at (3, 37.5) mm. The 0.5 mm branch to TP7
is a test connection rather than a series section of the main supply. The
layout contains 51 footprints, 206 trace segments and 182 vias.

The A3 schematic fits on one sheet. Some supporting connections, including
RX_REF and the C11/C12 bypass branches, use labels rather than continuous
wires. Their electrical connections are checked; their presentation could
still be made clearer.

## Fabrication files

The archive contains seven Gerber layers, PTH/NPTH drills and a Gerber job file.
All ten files have the expected structure and terminators. The NPTH file is
empty because the current holes are plated. Gerbers were exported with
`--check-zones` to check and refill the copper zones before plotting.

The BOM contains fitted quantities for one board. Native positions contain
38 entries with no test points; the SMT-only CPL contains 35 entries with
unchanged coordinates and rotations. File hashes are in the
[manifest](manifest.json), with more check details in [acceptance.json](acceptance.json).

## What these checks do not prove

Rev E still needs first-power, functional and longer-term testing. Thermal
margins, antenna/enclosure behavior, S3 Mini compatibility, EMC and the complete
board's safety-isolation rating are not qualified. There has been no separate
Gerber-viewer render or exhaustive solder-mask/via-in-pad audit.

The [layout check summary](acceptance.json) records which areas have only
partial coverage. CAD checks help catch errors; they do not replace bench tests.
