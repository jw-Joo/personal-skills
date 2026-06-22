#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HASH_PATTERN = re.compile(r"\b[0-9a-fA-F]{7,40}\b")
HEADING_PATTERN = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->")
MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[[^\]]*]\(([^)]+)\)")

PLACEHOLDERS = {
    "todo",
    "tbd",
    "n/a",
    "na",
    "none",
    "未入力",
    "未定",
}

SECTION_ALIASES = {
    "title": {
        "title",
        "release title",
        "release note title",
        "headline",
        "subject",
        "タイトル",
        "件名",
    },
    "commits": {
        "commit",
        "commits",
        "hash",
        "hashes",
        "revision",
        "revisions",
        "commit hashes",
        "コミット",
        "コミットハッシュ",
    },
    "validation": {
        "validation",
        "walidation",
        "verification",
        "verify",
        "qa",
        "test",
        "tests",
        "checklist",
        "検証",
        "検証済みの内容",
    },
    "images": {
        "image",
        "images",
        "screenshot",
        "screenshots",
        "capture",
        "captures",
        "画像",
        "スクリーンショット",
    },
}


def normalize_heading(value: str) -> str:
    value = HTML_COMMENT_PATTERN.sub("", value)
    value = re.sub(r"[:：#`*_]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip().lower()


def canonical_section(heading: str) -> str | None:
    normalized = normalize_heading(heading)
    for section, aliases in SECTION_ALIASES.items():
        if normalized in aliases:
            return section
    return None


def strip_wrappers(line: str) -> str:
    line = HTML_COMMENT_PATTERN.sub("", line).strip()
    line = re.sub(r"^>\s?", "", line).strip()
    line = re.sub(r"^[-*+]\s+\[[ xX-]]\s+", "", line).strip()
    line = re.sub(r"^[-*+]\s+", "", line).strip()
    line = re.sub(r"^\d+[.)]\s+", "", line).strip()
    return line


def is_placeholder(line: str) -> bool:
    normalized = strip_wrappers(line).strip().lower()
    normalized = normalized.strip("`*_[](){}<>:：。.!！")
    return not normalized or normalized in PLACEHOLDERS


def split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {
        "title": [],
        "commits": [],
        "validation": [],
        "images": [],
    }
    current_section: str | None = None

    for raw_line in text.splitlines():
        heading_match = HEADING_PATTERN.match(raw_line)
        if heading_match:
            current_section = canonical_section(heading_match.group(1))
            continue

        if current_section is None:
            continue

        sections[current_section].append(raw_line)

    return sections


def parse_title(lines: list[str]) -> str:
    values = [strip_wrappers(line) for line in lines if not is_placeholder(line)]
    return " ".join(values).strip()


def parse_hashes(lines: list[str]) -> list[str]:
    hashes: list[str] = []
    seen_hashes: set[str] = set()

    for line in lines:
        for match in HASH_PATTERN.findall(line):
            commit_hash = match.lower()
            if commit_hash in seen_hashes:
                continue
            seen_hashes.add(commit_hash)
            hashes.append(commit_hash)

    return hashes


def parse_validation(lines: list[str]) -> list[str]:
    items: list[str] = []
    for line in lines:
        if is_placeholder(line):
            continue
        item = strip_wrappers(line)
        if item:
            items.append(item)
    return items


def parse_image_paths(lines: list[str], base_dir: Path) -> tuple[list[str], list[str]]:
    existing_paths: list[str] = []
    missing_paths: list[str] = []

    for line in lines:
        if is_placeholder(line):
            continue

        image_targets = MARKDOWN_IMAGE_PATTERN.findall(line)
        if not image_targets:
            cleaned = strip_wrappers(line)
            if cleaned:
                image_targets = [cleaned]

        for raw_target in image_targets:
            target = raw_target.strip().strip("\"'")
            if not target:
                continue

            path = Path(target).expanduser()
            if not path.is_absolute():
                path = base_dir / path

            resolved = path.resolve()
            if resolved.exists():
                existing_paths.append(str(resolved))
            else:
                missing_paths.append(str(resolved))

    return existing_paths, missing_paths


def parse_input(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    sections = split_sections(text)
    image_paths, missing_image_paths = parse_image_paths(sections["images"], path.parent)

    missing_required: list[str] = []
    title = parse_title(sections["title"])
    commit_hashes = parse_hashes(sections["commits"])

    if not title:
        missing_required.append("title")
    if not commit_hashes:
        missing_required.append("commits")

    return {
        "input_file": str(path.resolve()),
        "target_directory": str(path.parent.resolve()),
        "title": title,
        "commit_hashes": commit_hashes,
        "validation_items": parse_validation(sections["validation"]),
        "image_paths": image_paths,
        "missing_image_paths": missing_image_paths,
        "missing_required": missing_required,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Parse a single-file API-PF release note input document."
    )
    parser.add_argument("input_file", help="Path to release_input.md")
    args = parser.parse_args()

    path = Path(args.input_file).expanduser().resolve()
    if not path.exists():
        print(json.dumps({"error": f"File does not exist: {path}"}), ensure_ascii=False)
        return 2
    if not path.is_file():
        print(json.dumps({"error": f"Not a file: {path}"}), ensure_ascii=False)
        return 2

    print(json.dumps(parse_input(path), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
