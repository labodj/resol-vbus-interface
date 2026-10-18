# Maintaining the design

These notes cover the settings and checks to keep when editing Rev E.

## Test points

Set the following attributes on the **schematic symbols** TP1-TP9:

| Attribute | Setting |
|---|---|
| Exclude from BOM | Enabled |
| Exclude from position files | Enabled |
| Exclude from board | Disabled |
| Do not populate / DNP | Disabled |

KiCad transfers these settings to the PCB with **Update PCB from Schematic
(F8)**. Changing only the PCB attributes can let a later update overwrite them.
The exclusions are already set in both files.

When updating symbols from a library, preserve the instance attributes unless
you intend to reset them. Afterward, export positions and check that TP1-TP9
are absent. Library defaults for newly added symbols may differ.

## Before exporting a changed board

1. Save the schematic and PCB.
2. Refill zones and run ERC/DRC, including schematic/PCB matching.
3. Run the [validation commands](validation.md#run-the-checks).
4. Check both copper layers, the isolation gap, connector orientation and labels.
5. Regenerate the schematic drawing, BOM, CPL, Gerbers and drills.
6. Inspect the fabrication preview and update the file manifest.

For an unchanged Rev E, the SMT-only CPL contains **35 components**. Native
positions contain 38 entries; J1, J2 and U7 are removed by the SMT filter.

## Libraries and 3D models

Use `TS391RIYLT` for U3: pin 1 is `RX_REF`, pin 4 is `RX_ISO`. Keep the symbol
and footprint pin assignments consistent with the exact ST part.

The optional RECOM STEP model is not included. The PCB retains a relative
reference for local 3D viewing; a missing model does not prevent fabrication.
See [third-party notices](../THIRD_PARTY.md).

Rev E remains prototype hardware until it has been assembled and tested.
See [validation](validation.md) for the current results and limits.
