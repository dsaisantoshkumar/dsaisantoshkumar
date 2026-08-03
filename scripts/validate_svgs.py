#!/usr/bin/env python3
"""
validate_svgs.py
-----------------
Parses every SVG under assets/ as XML and reports any file that isn't
well-formed. Run this after editing scripts/build_theme_svgs.py and
regenerating assets, before committing — a broken SVG silently shows as a
blank image on GitHub with no error message, so this is the only real check
you get pre-push.

Usage:
    python3 scripts/validate_svgs.py
"""

import glob
import os
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    pattern = os.path.join(ROOT, "assets", "**", "*.svg")
    files = sorted(glob.glob(pattern, recursive=True))
    if not files:
        print("No SVG files found under assets/ — did you run build_theme_svgs.py?")
        return 1

    invalid = []
    for f in files:
        try:
            tree = ET.parse(f)
            root = tree.getroot()
            if not root.tag.endswith("svg"):
                invalid.append((f, f"root element is <{root.tag}>, not <svg>"))
        except ET.ParseError as e:
            invalid.append((f, str(e)))

    for f, err in invalid:
        print(f"INVALID: {os.path.relpath(f, ROOT)} -> {err}")

    print(f"\nChecked {len(files)} file(s), {len(invalid)} invalid.")
    return 1 if invalid else 0


if __name__ == "__main__":
    sys.exit(main())
