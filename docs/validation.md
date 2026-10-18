# Validation

Rev E passes the CAD checks below. I have not yet assembled or bench-tested
this revision.

## Checks completed on 18 October 2026

| Check | Result |
|---|---|
| Schematic ERC | 0 errors, 0 warnings |
| PCB DRC | 0 errors, 0 warnings |
| Unrouted connections and schematic/PCB mismatches | 0 |
| Physical pin-to-net assignments | 52 checked |
| Critical component part numbers | 9 checked |
| Regression tests | 3 passed |
| SMT placement file | 35 components |

U3 uses the ST TS391RIYLT pin assignment: pin 1 is `RX_REF` and pin 4 is
`RX_ISO`. The tests reject the original pin swap and an incorrect comparator
variant. Both title blocks and silkscreens identify Rev E.

TP1-TP9 are excluded from the BOM and placement files in both the schematic
and PCB. A native position export contains 38 entries: 35 SMT components,
J1, J2 and U7. The supplied CPL keeps only the 35 SMT entries and preserves
their coordinates and rotations.

The final layout has 51 footprints and 206 trace segments. The ground planes
remain separate across the isolation barrier. Both copper sides and the
schematic have been visually checked.

## Run the checks

From the repository root, with Python 3 and KiCad 10 installed:

```sh
python scripts/check_hardware.py
python -m unittest discover -s scripts -p 'test_*.py' -v
```

The hardware check exports a fresh netlist and runs ERC and DRC, including
schematic/PCB matching and zone refill for the check. It writes results to
`build/checks/` without changing the design files.

To rebuild the SMT-only placement file, export native positions and IPC-2581
from the same saved board, then run:

```sh
python scripts/filter_cpl.py native-positions.csv board.xml fabrication/cpl.csv
```

## Fabrication files

The release contains seven Gerber layers, PTH/NPTH drill files and a Gerber
job file. The Gerber export used `--check-zones` to check and refill zones
before plotting. The NPTH file is valid and empty: all current holes are plated.

[Checks and limitations](../validation/publication-20261018/review.md) describe
the release in more detail. The [manifest](../validation/publication-20261018/manifest.json)
records file sizes and SHA-256 hashes.

## What still needs testing

CAD checks do not replace measurements on an assembled board. Rev E still
needs first-power and functional tests. Thermal performance, RF behavior, EMC,
long-cable operation, enclosure fit and the S3 Mini have not been fully tested.
The complete board has no certified safety-isolation rating.
