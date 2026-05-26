#!/usr/bin/env python3
"""Inventory a release note and suggest kc-manual RST candidates."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


KNOWN_TERMS = [
    "ログアウト",
    "自動ログアウト",
    "セッション",
    "eSIM",
    "eIM",
    "プロファイル",
    "有効化",
    "無効化",
    "eIM Action",
    "最終アクション",
    "Withdrawn",
    "強制適用",
    "SIM",
    "Poller",
    "Poller名",
    "OTA",
    "Displayed after OTA",
    "CSV",
    "iotsafe-client",
    "system diagnose",
    "vpn",
    "get-iccid",
    "download-config",
    "OpenVPN",
    "CA証明書",
    "API",
]


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp932"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def extract_h2_sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        title = re.sub(r"[*_`]+", "", match.group(1)).strip()
        sections.append((title, text[start:end]))
    return sections


def terms_for(title: str, body: str) -> list[str]:
    haystack = f"{title}\n{body}"
    found = [term for term in KNOWN_TERMS if term.lower() in haystack.lower()]
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", title)
    for word in words:
        if word not in found:
            found.append(word)
    return found


def scan_rst(repo: Path, terms: list[str]) -> list[tuple[Path, list[str]]]:
    source = repo / "source"
    root = source if source.exists() else repo
    results: list[tuple[Path, list[str]]] = []
    for path in sorted(root.rglob("*.rst")):
        text = read_text(path)
        matched = [term for term in terms if term and term.lower() in text.lower()]
        if matched:
            results.append((path, matched))
    return sorted(results, key=lambda item: (-len(item[1]), str(item[0])))


def markdown_images(text: str) -> list[str]:
    return re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-note", required=True, type=Path)
    parser.add_argument("--repo", default=Path.cwd(), type=Path)
    args = parser.parse_args()

    release_note = args.release_note.resolve()
    repo = args.repo.resolve()
    text = read_text(release_note)
    sections = extract_h2_sections(text)

    print(f"# Release note inventory: {release_note}")
    print()
    images = markdown_images(text)
    if images:
        print("## Images referenced")
        for image in images:
            print(f"- {image}")
        print()

    print("## Sections and candidate manual files")
    for title, body in sections:
        if title in {"概要", "Overview"}:
            continue
        terms = terms_for(title, body)
        candidates = scan_rst(repo, terms)
        print(f"### {title}")
        print(f"- Terms: {', '.join(terms) if terms else '(none)'}")
        if candidates:
            for path, matched in candidates[:10]:
                rel = path.relative_to(repo) if path.is_relative_to(repo) else path
                print(f"- Candidate: {rel} ({', '.join(matched[:8])})")
        else:
            print("- Candidate: none found")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
