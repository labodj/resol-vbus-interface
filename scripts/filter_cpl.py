#!/usr/bin/env python3
"""Keep only fitted SMT positions using a matching KiCad IPC-2581 export."""

import csv
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


def filter_cpl(positions, board_export, output):
    ns = {"i": "http://webstds.ipc.org/2581"}
    board = ET.parse(board_export).getroot()
    expected = {c.get("refDes") for c in board.findall(".//i:Component", ns)
                if c.get("mountType") == "SMT"}
    if not expected or any(ref.startswith("TP") for ref in expected):
        raise ValueError("Missing SMT inventory or test pads incorrectly classified as SMT")
    with Path(positions).open(newline="") as source:
        reader = csv.DictReader(source)
        fields = reader.fieldnames
        rows = list(reader)
    if fields != ["Ref", "Val", "Package", "PosX", "PosY", "Rot", "Side"]:
        raise ValueError("Unexpected native KiCad position CSV columns")
    refs = [r["Ref"] for r in rows]
    if len(refs) != len(set(refs)) or not expected.issubset(refs):
        raise ValueError("Duplicate positions or missing SMT components")
    selected = [r for r in rows if r["Ref"] in expected]
    with Path(output).open("w", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(selected)
    return {"input_positions": len(rows), "smt_positions": len(selected),
            "excluded": sorted(set(refs) - expected)}


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("Usage: filter_cpl.py native.csv board.xml output.csv")
    print(filter_cpl(*sys.argv[1:]))
