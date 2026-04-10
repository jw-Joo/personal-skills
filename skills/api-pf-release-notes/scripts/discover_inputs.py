#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TEXT_EXTENSIONS = {".md", ".markdown", ".txt"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
SKIP_DIR_NAMES = {
    ".git",
    ".next",
    "build",
    "dist",
    "node_modules",
    "release_note_output",
}

TYPE_PATTERNS = {
    "title": ("title", "release title", "release note title", "headline", "subject"),
    "commit": ("commit", "commits", "hash", "hashes", "revision", "revisions"),
    "validation": (
        "validation",
        "walidation",
        "verify",
        "verification",
        "test",
        "tests",
        "qa",
        "checklist",
        "check",
    ),
}


def normalize_name(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", " ", path.stem.lower()).strip()


def compute_score(name: str, patterns: tuple[str, ...]) -> tuple[int, list[str]]:
    score = 0
    matched_terms: list[str] = []
    for pattern in patterns:
        if pattern in name:
            score += len(pattern.replace(" ", "")) + 5
            matched_terms.append(pattern)
    return score, matched_terms


def should_skip(path: Path, root: Path) -> bool:
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in SKIP_DIR_NAMES for part in relative_parts[:-1])


def build_candidate(path: Path, root: Path, score: int, matched_terms: list[str]) -> dict[str, object]:
    return {
        "path": str(path.resolve()),
        "relative_path": path.relative_to(root).as_posix(),
        "filename": path.name,
        "score": score,
        "matched_terms": matched_terms,
    }


def discover(root: Path) -> dict[str, object]:
    categories = {
        "title_candidates": [],
        "commit_candidates": [],
        "validation_candidates": [],
        "image_candidates": [],
    }

    for path in sorted(root.rglob("*")):
        if not path.is_file() or should_skip(path, root):
            continue

        suffix = path.suffix.lower()
        if suffix in IMAGE_EXTENSIONS:
            categories["image_candidates"].append(
                build_candidate(path, root, 1, [suffix.lstrip(".")])
            )
            continue

        if suffix not in TEXT_EXTENSIONS:
            continue

        normalized = normalize_name(path)
        for kind, patterns in TYPE_PATTERNS.items():
            score, matched_terms = compute_score(normalized, patterns)
            if score <= 0:
                continue
            categories[f"{kind}_candidates"].append(
                build_candidate(path, root, score, matched_terms)
            )

    for key, values in categories.items():
        values.sort(key=lambda item: (-int(item["score"]), str(item["relative_path"])))

    return {
        "target_directory": str(root.resolve()),
        "title_candidates": categories["title_candidates"],
        "commit_candidates": categories["commit_candidates"],
        "validation_candidates": categories["validation_candidates"],
        "image_candidates": categories["image_candidates"],
        "counts": {
            "title": len(categories["title_candidates"]),
            "commit": len(categories["commit_candidates"]),
            "validation": len(categories["validation_candidates"]),
            "image": len(categories["image_candidates"]),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Discover flexible input-file candidates for the API-PF release note workflow."
    )
    parser.add_argument("target_directory", help="Directory to scan for input files")
    args = parser.parse_args()

    root = Path(args.target_directory).expanduser().resolve()
    if not root.exists():
        print(json.dumps({"error": f"Directory does not exist: {root}"}), file=sys.stderr)
        return 2
    if not root.is_dir():
        print(json.dumps({"error": f"Not a directory: {root}"}), file=sys.stderr)
        return 2

    print(json.dumps(discover(root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
