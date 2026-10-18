#!/usr/bin/env python3
"""Validate saved CAD with KiCad 10; never rewrite the KiCad sources."""

import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "hardware/rev-e/Resol_VBus_RevE"

# Physical lead assignments, not just consistency between schematic and board.
PIN_NETS = {
    "U1": {"1": "GND", "2": "GND", "3": "+5V", "4": "+5V", "5": "GND",
           "6": "GND", "7": "GND", "8": "GND", "9": "GND_ISO", "11": "GND_ISO",
           "12": "GND_ISO", "13": "VISO_RAW", "14": "VISO_RAW", "15": "GND_ISO", "16": "GND_ISO"},
    "U2": {"1": "VISO_RAW", "2": "GND_ISO", "3": "VISO_RAW", "5": "+3V3_ISO"},
    "U3": {"1": "RX_REF", "2": "GND_ISO", "3": "SENSE", "4": "RX_ISO", "5": "+3V3_ISO"},
    "U4": {"1": "+3V3_ISO", "2": "TX_ISO", "3": "RX_ISO", "4": "GND_ISO",
           "5": "GND", "7": "TX_MCU", "8": "+3V3_MCU"},
    "U5": {"1": "GND_ISO", "2": "ISO_READY", "3": "+3V3_ISO"},
    "U6": {"1": "ISO_READY", "2": "GND_ISO", "3": "GND_ISO", "5": "+3V3_ISO", "6": "TX_ISO"},
    "Q1": {"1": "TX_GATE", "2": "GND_ISO", "3": "VBUS_RECT"},
    "D2": {"1": "GND_ISO", "2": "VBUS_RECT", "3": "VBUS_A"},
    "D3": {"1": "GND_ISO", "2": "VBUS_RECT", "3": "VBUS_B"},
    "J1": {"1": "GND", "2": "+5V"},
    "J2": {"1": "VBUS_B", "2": "VBUS_A"},
}
PARTS = {"U1": "R05CTE05S-CT", "U2": "MIC5235-3.3YM5-TR", "U3": "TS391RIYLT",
         "U4": "ISO7221ADR", "U5": "MAX809TEUR+T", "U6": "SN74AUP1G97DBVR",
         "Q1": "NTR4003NT3G", "D2": "BAT54SQ-7-F", "D3": "BAT54SQ-7-F"}


def check_netlist(path):
    """Raise ValueError on a wrong physical pin assignment or part identity."""
    root = ET.parse(path).getroot()
    nets = {f"{node.get('ref')}.{node.get('pin')}": net.get("name").removeprefix("/")
            for net in root.findall("./nets/net") for node in net}
    for ref, pins in PIN_NETS.items():
        for pin, expected in pins.items():
            actual = nets.get(f"{ref}.{pin}")
            if actual != expected:
                raise ValueError(f"{ref}.{pin}: expected {expected}, got {actual}")
    for ref, pin in (("U1", "10"), ("U2", "4")):
        actual = nets.get(f"{ref}.{pin}", "")
        if not actual.startswith("unconnected-"):
            raise ValueError(f"{ref}.{pin} must remain unconnected, got {actual}")
    for left, right in (("U4.6", "R7.1"), ("U6.4", "R10.1")):
        if not nets.get(left) or nets[left] != nets.get(right):
            raise ValueError(f"Required connection missing: {left} to {right}")
    components = {c.get("ref"): c for c in root.findall("./components/comp")}
    for ref, expected in PARTS.items():
        fields = {f.get("name"): f.text for f in components[ref].findall("./fields/field")}
        if fields.get("MPN") != expected:
            raise ValueError(f"{ref}: expected exact MPN {expected}, got {fields.get('MPN')}")
    return {"physical_pin_checks": sum(map(len, PIN_NETS.values())),
            "exact_part_checks": len(PARTS), "components": len(components)}


def run(*args):
    return subprocess.run(["kicad-cli", *map(str, args)], check=True,
                          text=True, capture_output=True, timeout=60).stdout


def main():
    output = ROOT / "build/checks"
    output.mkdir(parents=True, exist_ok=True)
    version = run("version").strip()
    if int(version.split(".")[0]) < 10:
        raise RuntimeError(f"KiCad 10 or newer required, got {version}")
    run("sch", "export", "netlist", "--format", "kicadxml", "--output",
        output / "netlist.xml", PROJECT.with_suffix(".kicad_sch"))
    result = check_netlist(output / "netlist.xml")
    run("sch", "erc", "--format", "json", "--severity-all", "--exit-code-violations",
        "--output", output / "erc.json", PROJECT.with_suffix(".kicad_sch"))
    run("pcb", "drc", "--format", "json", "--severity-all", "--schematic-parity",
        "--refill-zones", "--exit-code-violations", "--output", output / "drc.json",
        PROJECT.with_suffix(".kicad_pcb"))
    result.update(kicad_version=version, erc="PASS", drc="PASS", source_writes=False)
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print(error.stdout, end="", file=sys.stderr)
        print(error.stderr, end="", file=sys.stderr)
        print("Hardware check FAILED. Inspect build/checks/; no release is approved.", file=sys.stderr)
        sys.exit(1)
