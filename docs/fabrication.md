# Fabricating Rev E

Download `fabrication/Resol_VBus_RevE_Gerbers.zip` from the tagged prototype
release. It contains seven Gerber layers (front/back copper, front/back solder
mask, front/back silkscreen and Edge.Cuts), plated/non-plated Excellon drill
files and a Gerber job file. The NPTH file is valid and empty: the current
mounting holes and connectors use plated holes.

## Board specification

- One 64 x 50 mm board, two copper layers.
- 1.6 mm FR-4, nominal 35 micrometres / 1 oz copper on each side.
- Standard solder mask and silkscreen; tented stitching vias are intended.
- No controlled impedance, gold fingers, castellations or filled/capped vias
  are specified. Check the fabricator's actual preview and process capabilities.
- Four M2 mounting holes have isolated plated annuli; they are not ground
  terminals. Check screw/washer clearance on the assembled board.

Check the archive checksum
against the release manifest before ordering. Inspect the uploaded layer/drill
preview, board outline and mounting holes at the fabricator.

## Assembly files

`bom.csv` gives fitted quantities for one board: 35 SMD parts, two JST
B2B-XH-A connectors and one module position. Female module sockets and mounting
hardware are additional assembly items described in `assembly.md`.
`cpl.csv` is native KiCad CSV filtered to 35 SMT parts; J1/J2/U7 and all bare test
pads are excluded. The format is not a promise that a particular assembly
service accepts the column names or rotations without conversion and preview.

The board is intended for manual assembly. J1 is 5 V power; J2 is VBus despite
using the same keyed connector. Use USB or external power, never both together.
Follow `assembly.md` before connecting a controller.

## Validation boundary

Saved-source ERC/DRC, physical pin checks and regression tests pass. The public
review documents applicability and unverified limits. Rev E has not yet been
manufactured or bench-tested. CAD cleanliness is not thermal, RF, EMC or safety
certification, and an optional missing 3D model is not physical-fit evidence.
