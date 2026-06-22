#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TEMPLATE_FILENAME = "release_input.md"
TEXT_FILE_EXTENSIONS = {".md", ".markdown", ".txt"}
DEFAULT_TARGET_NAME = "TODO"
NON_TITLE_PREFIX_LABELS = {
    "実装",
    "対応",
    "修正",
    "改修",
    "追加",
    "変更",
    "開発",
    "調査",
    "不具合修正",
    "バグ修正",
}

TEMPLATE = """# API-PF Release Note Input

<!--
Fill this file, then ask Codex again:
$api-pf-release-notes {target_name}

Put screenshots in this same directory when the change includes frontend behavior.
-->

## Title
<!-- Release note title in Japanese. -->
{title}

## Commits
<!-- Add one normal or merge commit hash per line. -->
TODO

## Validation
<!-- Paste verification results. Keep one item per line. -->
- TODO

## Images
<!-- Optional. List screenshot filenames or Markdown image links. -->

"""


def sanitize_filename(value: str) -> str:
    normalized = re.sub(r"[\x00-\x1f\x7f/\\:]+", "-", value.strip())
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = normalized.strip(" .")
    return normalized or "release-note"


def cleanup_title(value: str) -> str:
    title = value.strip()
    title = re.sub(r"^[A-Za-z][A-Za-z0-9_]*-\d+\s*", "", title)

    while True:
        match = re.match(r"^[\s　]*(?:【([^】]+)】|\[([^\]]+)\]|［([^］]+)］)\s*", title)
        if not match:
            break

        label = next(group for group in match.groups() if group is not None).strip()
        if label not in NON_TITLE_PREFIX_LABELS:
            break

        title = title[match.end() :]

    return title.strip() or value.strip() or DEFAULT_TARGET_NAME


def unique_directory(target_dir: Path) -> Path:
    if not target_dir.exists():
        return target_dir

    parent = target_dir.parent
    stem = target_dir.name or DEFAULT_TARGET_NAME
    index = 2
    while True:
        candidate = parent / f"{stem}-{index}"
        if not candidate.exists():
            return candidate
        index += 1


def resolve_target(raw_target: str | None, base_dir: Path, force: bool) -> tuple[Path, Path, str, str]:
    raw_target = (raw_target or "").strip() or DEFAULT_TARGET_NAME
    raw_path = Path(raw_target).expanduser()
    is_path_like = raw_path.is_absolute() or len(raw_path.parts) > 1
    title = cleanup_title(raw_target)

    if raw_path.suffix.lower() in TEXT_FILE_EXTENSIONS:
        input_file = raw_path
        target_dir = raw_path.parent
        target_name = raw_path.stem
        title = cleanup_title(raw_path.stem)
    elif is_path_like:
        target_dir = raw_path
        input_file = target_dir / TEMPLATE_FILENAME
        target_name = target_dir.name
        title = cleanup_title(target_name)
    else:
        target_name = sanitize_filename(raw_target)
        target_dir = base_dir / target_name
        input_file = target_dir / TEMPLATE_FILENAME

    if not force:
        target_dir = unique_directory(target_dir)
        input_file = target_dir / TEMPLATE_FILENAME
        target_name = target_dir.name

    return target_dir.resolve(), input_file.resolve(), target_name, title


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a single-file API-PF release note input template."
    )
    parser.add_argument(
        "target",
        nargs="?",
        help=(
            "Optional release note name, target directory, or release_input.md path. "
            "When omitted, TODO is used. Simple names are created under .scratch/RN/."
        ),
    )
    parser.add_argument(
        "--base-dir",
        default=".scratch/RN",
        help="Base directory for simple target names. Default: .scratch/RN",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing release_input.md template.",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir).expanduser()
    target_dir, input_file, target_name, title = resolve_target(args.target, base_dir, args.force)

    target_dir.mkdir(parents=True, exist_ok=True)

    if input_file.exists() and not args.force:
        print(
            json.dumps(
                {
                    "created": False,
                    "status": "exists",
                    "template_name": target_name,
                    "title": title,
                    "target_directory": str(target_dir),
                    "input_file": str(input_file),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    input_file.write_text(
        TEMPLATE.format(target_name=target_name, title=title),
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "created": True,
                "status": "created",
                "template_name": target_name,
                "title": title,
                "target_directory": str(target_dir),
                "input_file": str(input_file),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
