#!/usr/bin/env python3
"""Outline an attribute-based SVG with installed librsvg; preserve dark colors."""

import argparse
import copy
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)


def dark_rules(css):
    """Accept only dark-media blocks; do not silently discard ordinary styling."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S).strip()
    rules = []
    while css:
        match = re.match(r"@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*\{", css)
        if not match:
            raise ValueError("Styles must contain only dark-mode media rules; put the baseline in SVG attributes.")
        start = pos = match.end()
        depth = 1
        while pos < len(css) and depth:
            depth += (css[pos] == "{") - (css[pos] == "}")
            pos += 1
        if depth:
            raise ValueError("Unbalanced dark-mode CSS block.")
        block = css[start:pos - 1]
        # The exporter reconstructs paints only, never typography or geometry.
        for declarations in re.findall(r"\{([^{}]*)\}", block):
            for declaration in declarations.split(";"):
                if not declaration.strip():
                    continue
                name, _, value = declaration.partition(":")
                if name.strip() not in {"fill", "stroke"} or not re.fullmatch(r"#[0-9a-fA-F]{6}", value.strip()):
                    raise ValueError("Dark overrides must use concrete six-digit hex fill/stroke colors only.")
        rules.append(block)
        css = css[pos:].strip()
    return "\n".join(rules)


def render(root, renderer):
    result = subprocess.run([renderer, "--format=svg"], input=ET.tostring(root),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    if result.stderr:
        sys.stderr.write(result.stderr.decode())
    rendered = ET.fromstring(result.stdout)
    for element in rendered.iter():
        for name in ("fill", "stroke"):
            value = element.get(name, "")
            match = re.fullmatch(r"rgb\(([^)]+)\)", value)
            if match:
                channels = []
                for channel in match[1].split(","):
                    channel = channel.strip()
                    number = float(channel[:-1]) * 255 / 100 if channel.endswith("%") else float(channel)
                    channels.append(round(number))
                if len(channels) != 3 or not all(0 <= channel <= 255 for channel in channels):
                    raise ValueError(f"Unsupported paint color: {value}")
                element.set(name, "#" + "".join(f"{channel:02x}" for channel in channels))
    if any(e.tag in {f"{{{SVG}}}text", f"{{{SVG}}}tspan", f"{{{SVG}}}image"} for e in rendered.iter()):
        raise ValueError("Exporter left text or raster images in the output.")
    return rendered


def outline(source, target):
    if source.resolve() == target.resolve():
        raise ValueError("Keep the editable source: source and output paths must differ.")
    if target.exists():
        raise ValueError(f"Output already exists: {target}; choose a new path or remove the old export explicitly.")
    renderer = shutil.which("rsvg-convert")
    if not renderer:
        raise ValueError("rsvg-convert is not installed; no tools were installed and no output was written.")
    root = ET.parse(source).getroot()
    if root.tag != f"{{{SVG}}}svg":
        raise ValueError("Input is not an SVG document.")
    css = []
    for parent in root.iter():
        for element in list(parent):
            if element.tag == f"{{{SVG}}}style":
                css.append(dark_rules(element.text or ""))
                parent.remove(element)
    for element in root.iter():
        if element.tag in {f"{{{SVG}}}script", f"{{{SVG}}}foreignObject", f"{{{SVG}}}image"}:
            raise ValueError("Input must contain static vector shapes and text only.")
        for key, value in element.attrib.items():
            if key.split("}")[-1] == "href" and not value.startswith("#"):
                raise ValueError("External resources are not supported.")
            if any(token in value for token in ("var(", "context-stroke", "currentColor")):
                raise ValueError("The baseline must use concrete presentation attributes.")
    light = render(root, renderer)
    theme = "\n".join(css).strip()
    overrides = []
    if theme:
        dark_source = copy.deepcopy(root)
        ET.SubElement(dark_source, f"{{{SVG}}}style").text = theme
        dark = render(dark_source, renderer)
        light_nodes, dark_nodes = list(light.iter()), list(dark.iter())
        if len(light_nodes) != len(dark_nodes):
            raise ValueError("Themes produced different structures; export was not written.")
        classes = {}
        for left, right in zip(light_nodes, dark_nodes):
            if left.tag != right.tag or left.text != right.text:
                raise ValueError("Themes produced different content; export was not written.")
            for key in left.attrib.keys() | right.attrib.keys():
                if left.get(key) == right.get(key):
                    continue
                if key not in {"fill", "stroke"} or key not in left.attrib or key not in right.attrib:
                    raise ValueError(f"Themes changed {key}, not just paint colors; export was not written.")
                pair = (key, left.get(key), right.get(key))
                if pair not in classes:
                    name = f"outlined-theme-{len(classes)}"
                    classes[pair] = name
                    overrides.append(f".{name} {{ {key}: {right.get(key)}; }}")
                left.set("class", (left.get("class", "") + " " + classes[pair]).strip())
    # Restore descriptions that the outline renderer does not preserve.
    described = []
    for tag in ("title", "desc"):
        original = root.find(f"{{{SVG}}}{tag}")
        if original is not None:
            item = copy.deepcopy(original)
            item.set("id", f"outlined-{tag}")
            light.insert(len(described), item)
            described.append(item.get("id"))
    if described:
        light.set("role", "img")
        light.set("aria-labelledby", " ".join(described))
    if overrides:
        style = ET.SubElement(light, f"{{{SVG}}}style")
        style.text = "\n@media (prefers-color-scheme: dark) {\n  " + "\n  ".join(overrides) + "\n}\n"
    ET.indent(light, space="  ")
    content = ET.tostring(light, encoding="utf-8", xml_declaration=True)
    target.write_bytes(content + b"\n")
    print(f"Outlined SVG written: {target}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        outline(args.source, args.output)
    except (ValueError, ET.ParseError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
