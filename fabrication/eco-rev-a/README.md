# Fabricating RESOL VBus ECO Rev A

Use [the ECO fabrication ZIP](RESOL_VBus_ECO_RevA_Gerbers.zip) for a pilot board or top-side stencil. Only the isolated version has field-test history. ECO Rev A passed KiCad 10.0.8 ERC and DRC, including zone refill and schematic parity, and awaits physical qualification.

| Item | ECO Rev A |
|---|---|
| Finished outline | 64 × 50 mm, rounded corners, four plated 2.2 mm M2 holes |
| Stackup | Two copper layers, FR-4, 1.6 mm thick, 35 µm (1 oz) copper per layer |
| Fabrication archive | Front/back copper, solder mask and silkscreen; Edge.Cuts profile; metric PTH and NPTH Excellon files; Gerber job file |
| Stencil | Use the front paste layer (.gtp). All 26 SMT parts are on the front. |
| Assembly | [BOM for one board](../../hardware/eco-rev-a/BOM.csv) · [SMT positions in mm](cpl.csv) |
| Traceability | [Manifest with source hashes, archive contents, drill counts and checks](manifest.json) |

The NPTH file has no drill hits. In the fabricator preview, check the rounded outline, four mounting holes, socket rows and connector drills. For stencil ordering, select the front paste artwork.

The BOM has 29 fitted references including J1, J2 and the selected LOLIN module at U7. Fit two 1×8 female socket strips on 2.54 mm pitch for U7. The CPL includes only the 26 surface-mount placements. It uses native KiCad coordinates and rotations; check pin 1 and diode orientation in the assembler’s preview.

[Wiring and first power-up](../../hardware/eco-rev-a/README.md) · [Isolated version fabrication files](../../docs/fabrication.md)
