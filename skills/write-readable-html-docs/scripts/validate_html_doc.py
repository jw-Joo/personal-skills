#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a readable standalone HTML doc.")
    parser.add_argument("html_file", type=Path)
    parser.add_argument("--require-source-note", action="store_true")
    parser.add_argument("--min-sections", type=int, default=4)
    args = parser.parse_args()

    if not args.html_file.exists():
        print(f"missing file: {args.html_file}", file=sys.stderr)
        return 2

    html = args.html_file.read_text(encoding="utf-8")
    ids = re.findall(r'id="([^"]+)"', html)
    hrefs = re.findall(r'href="#([^"]+)"', html)

    missing = [href for href in hrefs if href not in ids]
    duplicates = sorted({id_ for id_ in ids if ids.count(id_) > 1})

    counts = {
        "sections": len(re.findall(r"<section\b", html)),
        "details": len(re.findall(r"<details\b", html)),
        "tables": len(re.findall(r"<table\b", html)),
        "code_blocks": len(re.findall(r"<pre><code", html)),
        "nav_links": len(hrefs),
        "callouts": len(re.findall(r'class="[^"]*\bcallout\b', html)),
        "checklists": len(re.findall(r'class="[^"]*\bchecklist\b', html)),
    }

    errors = []
    if missing:
        errors.append(f"missing internal link targets: {', '.join(missing)}")
    if duplicates:
        errors.append(f"duplicate ids: {', '.join(duplicates)}")
    if counts["sections"] < args.min_sections:
        errors.append(f"expected at least {args.min_sections} sections, found {counts['sections']}")
    if args.require_source_note:
        top = html[:1600]
        if "Maintenance contract" not in top or "Source Markdown:" not in top:
            errors.append("top maintenance contract comment not found in first 1600 characters")
        source_note_patterns = [
            "원본 Markdown",
            "source Markdown",
            "source document",
            "원본 문서",
        ]
        if not any(pattern in html for pattern in source_note_patterns):
            errors.append("source synchronization note not found")

    print({"counts": counts, "missing_links": missing, "duplicate_ids": duplicates})

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
