"""Regression check: the original U3 swap must never pass the netlist guard."""

from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from check_hardware import PROJECT, check_netlist, run


class PhysicalPinGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.netlist = Path(cls.directory.name) / "netlist.xml"
        run("sch", "export", "netlist", "--format", "kicadxml", "--output",
            cls.netlist, PROJECT.with_suffix(".kicad_sch"))

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def test_corrected_export(self):
        check_netlist(self.netlist)

    def test_rejects_original_comparator_swap(self):
        root = ET.parse(self.netlist)
        for node in root.findall("./nets/net/node"):
            if node.get("ref") == "U3" and node.get("pin") in ("1", "4"):
                node.set("pin", "4" if node.get("pin") == "1" else "1")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.xml"
            root.write(path)
            with self.assertRaisesRegex(ValueError, "U3.1"):
                check_netlist(path)

    def test_rejects_a_different_comparator(self):
        root = ET.parse(self.netlist)
        for component in root.findall("./components/comp"):
            if component.get("ref") == "U3":
                for field in component.findall("./fields/field"):
                    if field.get("name") == "MPN":
                        field.text = "TS391IYLT"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong-part.xml"
            root.write(path)
            with self.assertRaisesRegex(ValueError, "exact MPN TS391RIYLT"):
                check_netlist(path)


if __name__ == "__main__":
    unittest.main()
