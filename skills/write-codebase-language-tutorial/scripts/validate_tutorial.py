#!/usr/bin/env python3
"""Validate a standalone codebase-language tutorial HTML artifact."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_ROLES = {
    "reader-contract",
    "language-foundation",
    "actual-code-flow",
    "learning-boundary",
    "final-flow",
}
VALID_CODE_KINDS = {"actual", "simplified", "hypothetical"}


class TutorialParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.internal_hrefs: list[str] = []
        self.sections = 0
        self.details = 0
        self.nav_links = 0
        self.code_blocks = 0
        self.code_kind_errors: list[str] = []
        self.actual_paths: list[str] = []
        self.roles: set[str] = set()
        self.levels: set[str] = set()

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}

        if attrs.get("id"):
            self.ids.append(attrs["id"])

        if tag == "a":
            href = attrs.get("href", "")
            if href.startswith("#"):
                self.internal_hrefs.append(href[1:])
                self.nav_links += 1

        if tag == "section":
            self.sections += 1
        elif tag == "details":
            self.details += 1
        elif tag == "pre":
            self.code_blocks += 1
            kind = attrs.get("data-code-kind")
            if kind not in VALID_CODE_KINDS:
                self.code_kind_errors.append(
                    f"pre block {self.code_blocks} needs data-code-kind="
                    f"{'|'.join(sorted(VALID_CODE_KINDS))}"
                )
            if kind == "actual":
                source_path = attrs.get("data-source-path")
                if not source_path:
                    self.code_kind_errors.append(
                        f"actual pre block {self.code_blocks} needs data-source-path"
                    )
                else:
                    self.actual_paths.append(source_path)

        role = attrs.get("data-tutorial-role")
        if role:
            self.roles.add(role)

        level = attrs.get("data-level")
        if level:
            self.levels.add(level)


def validate_source_paths(paths: list[str], source_root: Path) -> list[str]:
    errors: list[str] = []
    root = source_root.resolve()

    for raw_path in paths:
        path = Path(raw_path)
        if path.is_absolute():
            errors.append(f"actual source path must be relative: {raw_path}")
            continue

        resolved = (root / path).resolve()
        try:
            resolved.relative_to(root)
        except ValueError:
            errors.append(f"actual source path escapes source root: {raw_path}")
            continue

        if not resolved.is_file():
            errors.append(f"actual source path does not exist: {raw_path}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html_file", type=Path)
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()

    if not args.html_file.is_file():
        print(f"missing tutorial: {args.html_file}", file=sys.stderr)
        return 2

    html = args.html_file.read_text(encoding="utf-8")
    tutorial = TutorialParser()
    tutorial.feed(html)

    errors: list[str] = []
    id_counts = Counter(tutorial.ids)
    duplicate_ids = sorted(key for key, count in id_counts.items() if count > 1)
    missing_targets = sorted(set(tutorial.internal_hrefs) - set(tutorial.ids))
    missing_roles = sorted(REQUIRED_ROLES - tutorial.roles)

    if duplicate_ids:
        errors.append(f"duplicate ids: {', '.join(duplicate_ids)}")
    if missing_targets:
        errors.append(f"missing internal link targets: {', '.join(missing_targets)}")
    if tutorial.sections < 5:
        errors.append(f"expected at least 5 sections, found {tutorial.sections}")
    if tutorial.nav_links < 5:
        errors.append(f"expected at least 5 internal nav links, found {tutorial.nav_links}")
    if tutorial.details < 1:
        errors.append("expected at least one details block for deferred material")
    if len(tutorial.actual_paths) < 3:
        errors.append(
            f"expected at least 3 actual code blocks with source paths, found {len(tutorial.actual_paths)}"
        )
    if missing_roles:
        errors.append(f"missing tutorial roles: {', '.join(missing_roles)}")
    if "now" not in tutorial.levels or "later" not in tutorial.levels:
        errors.append("expected data-level=now and data-level=later learning boundaries")
    if "REPLACE_" in html:
        errors.append("unresolved template placeholders found")

    errors.extend(tutorial.code_kind_errors)
    if args.source_root:
        errors.extend(validate_source_paths(tutorial.actual_paths, args.source_root))

    report = {
        "sections": tutorial.sections,
        "details": tutorial.details,
        "nav_links": tutorial.nav_links,
        "code_blocks": tutorial.code_blocks,
        "actual_code_blocks": len(tutorial.actual_paths),
        "roles": sorted(tutorial.roles),
        "levels": sorted(tutorial.levels),
        "errors": errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

    if errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
