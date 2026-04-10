#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HASH_PATTERN = re.compile(r"\b[0-9a-fA-F]{7,40}\b")


def extract_hashes(path: Path) -> tuple[list[str], list[dict[str, object]]]:
    hashes: list[str] = []
    unmatched_lines: list[dict[str, object]] = []

    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1
    ):
        matches = HASH_PATTERN.findall(raw_line)
        if matches:
            hashes.extend(match.lower() for match in matches)
            continue
        if raw_line.strip():
            unmatched_lines.append(
                {
                    "path": str(path.resolve()),
                    "line_number": line_number,
                    "content": raw_line,
                }
            )

    return hashes, unmatched_lines


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract ordered, deduplicated git commit hashes from one or more files."
    )
    parser.add_argument("files", nargs="+", help="Commit-hash source files")
    args = parser.parse_args()

    ordered_hashes: list[str] = []
    seen_hashes: set[str] = set()
    file_reports: list[dict[str, object]] = []
    unmatched_lines: list[dict[str, object]] = []

    for raw_path in args.files:
        path = Path(raw_path).expanduser().resolve()
        if not path.exists():
            print(json.dumps({"error": f"File does not exist: {path}"}), file=sys.stderr)
            return 2
        if not path.is_file():
            print(json.dumps({"error": f"Not a file: {path}"}), file=sys.stderr)
            return 2

        file_hashes, file_unmatched = extract_hashes(path)
        file_reports.append({"path": str(path), "hashes": file_hashes})
        unmatched_lines.extend(file_unmatched)

        for commit_hash in file_hashes:
            if commit_hash in seen_hashes:
                continue
            ordered_hashes.append(commit_hash)
            seen_hashes.add(commit_hash)

    payload = {
        "hashes": ordered_hashes,
        "files": file_reports,
        "unmatched_lines": unmatched_lines,
    }

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if ordered_hashes else 1


if __name__ == "__main__":
    raise SystemExit(main())
