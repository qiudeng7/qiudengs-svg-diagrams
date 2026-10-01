"""Regression checks using an already installed rsvg-convert."""

import contextlib
import copy
import io
from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from outline_svg import SVG, dark_rules, outline, render


SOURCE = '''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="120" viewBox="0 0 240 120">
<title>Compilation</title><desc>Text becomes paths while colors remain theme aware.</desc>
<style>@media (prefers-color-scheme: dark) {
.canvas {fill:#141a21;} .label {fill:#e3eaf0;} .arrow {stroke:#94b8da;}
}</style>
<rect width="240" height="120" fill="#ffffff" class="canvas"/>
<text x="20" y="50" fill="#25313a" font-family="sans-serif" font-size="22" class="label">Compile 编译</text>
<path d="M20 80 H200 L190 70 M200 80 L190 90" fill="none" stroke="#426b91" stroke-width="2" class="arrow"/>
</svg>'''


@unittest.skipUnless(shutil.which("rsvg-convert"), "rsvg-convert is not installed")
class OutlineTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.source = Path(self.folder.name) / "source.svg"
        self.output = Path(self.folder.name) / "output.svg"
        self.source.write_text(SOURCE)

    @staticmethod
    def render_mode(root, dark=False):
        root = copy.deepcopy(root)
        css = []
        for parent in root.iter():
            for element in list(parent):
                if element.tag == f"{{{SVG}}}style":
                    css.append(dark_rules(element.text or ""))
                    parent.remove(element)
        if dark:
            ET.SubElement(root, f"{{{SVG}}}style").text = "\n".join(css)
        return render(root, shutil.which("rsvg-convert"))

    @staticmethod
    def painted_geometry(root):
        return [dict(element.attrib) for element in root.iter() if element.tag.endswith("}path")]

    def test_outline_preserves_geometry_and_paints_in_both_modes(self):
        with contextlib.redirect_stdout(io.StringIO()):
            outline(self.source, self.output)
        original = ET.parse(self.source).getroot()
        exported = ET.parse(self.output).getroot()
        self.assertFalse(any(e.tag.endswith(("}text", "}tspan", "}image")) for e in exported.iter()))
        self.assertEqual(exported.find(f"{{{SVG}}}title").text, "Compilation")
        self.assertEqual(self.source.read_text(), SOURCE)
        for dark in (False, True):
            expected = self.painted_geometry(self.render_mode(original, dark))
            actual = self.painted_geometry(self.render_mode(exported, dark))
            self.assertEqual(actual, expected)

    def test_refuses_overwriting_editable_source_or_existing_export(self):
        with self.assertRaises(ValueError):
            outline(self.source, self.source)
        self.output.write_text("Existing user file")
        with self.assertRaises(ValueError):
            outline(self.source, self.output)
        self.assertEqual(self.output.read_text(), "Existing user file")

    def test_refuses_css_baseline_or_geometry_theme_changes(self):
        for css in (".label {fill:#25313a;}",
                    "@media (prefers-color-scheme: dark) {.label {font-size:40px;}}"):
            with self.assertRaises(ValueError):
                dark_rules(css)
        self.source.write_text(SOURCE.replace('fill="#ffffff"', 'fill="var(--background)"'))
        with self.assertRaises(ValueError):
            outline(self.source, self.output)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
