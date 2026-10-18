# Third-party notices and provenance

## KiCad library data

Standard and modified symbols/footprints originate from the KiCad library contributors:
https://gitlab.com/kicad/libraries/kicad-symbols
https://gitlab.com/kicad/libraries/kicad-footprints
https://gitlab.com/kicad/libraries/kicad-packages3D

The local `ResolVBusD.kicad_sym` and `.pretty` library collection includes standard library data and project-specific modifications. Changes include the verified ST TS391RIYLT physical pin assignment, isolated power/header representations, mounting-hole geometry, and custom package representations. These are not asserted to be unmodified upstream KiCad parts. Retained library terms: CC-BY-SA-4.0 with the KiCad exception, reproduced in `LICENSES/KiCad-library-license.md`. Standard 3D assets are referenced through KiCad environment variables and not bundled.

## Manufacturer data and optional models

Manufacturer datasheets are linked, not relicensed or bundled. The RECOM STEP model is **not distributed**, because redistribution permission has not been established. The PCB retains an optional project-relative reference `ResolVBusD.3dshapes/RxxCTExxS.step`; this affects only the 3D view and is not needed to open, edit, check or manufacture the board. The library footprint does not require that model. Obtain any optional model directly from the manufacturer under its applicable terms.

## Design background

The original personal receiver design was informed by the ESPHome VBus documentation (https://esphome.io/components/vbus/) and FatBeard's VBus Arduino PCB project (https://github.com/FatBeard/vbus-arduino-library/tree/master/pcb). Those projects retain their own licenses; this repository does not relicense or bundle their source files. The Rev E layout and documentation are maintained here as a separate project.

RESOL, VBus, LOLIN and the component manufacturers' names are used to identify compatibility and products. There is no endorsement or certification by those organizations.
