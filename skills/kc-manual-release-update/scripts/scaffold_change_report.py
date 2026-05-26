#!/usr/bin/env python3
"""Scaffold a Markdown report for kc-manual before/after changes."""

from __future__ import annotations

import argparse
import difflib
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp932"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def run_git(repo: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return ""
    return result.stdout


def collect_baseline_diffs(repo: Path, baseline_dir: Path) -> list[tuple[str, str]]:
    diffs: list[tuple[str, str]] = []
    for before in sorted(path for path in baseline_dir.rglob("*") if path.is_file()):
        rel = before.relative_to(baseline_dir)
        after = repo / rel
        before_lines = read_text(before).splitlines(keepends=True)
        after_lines = read_text(after).splitlines(keepends=True) if after.exists() else []
        diff = "".join(
            difflib.unified_diff(
                before_lines,
                after_lines,
                fromfile=f"before/{rel}",
                tofile=f"after/{rel}",
            )
        )
        if diff:
            diffs.append((rel.as_posix(), diff))
    return diffs


def collect_git_diffs(repo: Path, max_files: int, max_diff_chars: int) -> list[tuple[str, str]]:
    names = run_git(repo, ["diff", "--name-only", "--", "source"]).splitlines()
    diffs: list[tuple[str, str]] = []
    for name in names[:max_files]:
        diff = run_git(repo, ["diff", "--", name])
        if diff:
            if len(diff) > max_diff_chars:
                diff = diff[:max_diff_chars] + "\n... diff truncated ...\n"
            diffs.append((name, diff))
    return diffs


def release_package_dir(release_note: Path) -> Path:
    return release_note if release_note.is_dir() else release_note.parent


def default_output_path(release_note: Path) -> Path:
    package_dir = release_package_dir(release_note)
    release_stem = release_note.name if release_note.is_dir() else release_note.stem
    return package_dir / "manual_update_report" / f"{release_stem}-kc-manual-update-report.md"


def path_is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def resolve_output_path(output: Path | None, release_note: Path) -> Path:
    package_dir = release_package_dir(release_note).resolve()
    resolved = (output.resolve() if output else default_output_path(release_note).resolve())
    if not path_is_relative_to(resolved, package_dir):
        raise SystemExit(
            "Report output must be inside the release-note package directory: "
            f"{package_dir}"
        )
    return resolved


def write_report(output: Path, repo: Path, release_note: Path, diffs: list[tuple[str, str]]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines: list[str] = [
        "# kc-manual Manual Update Report",
        "",
        "## Metadata",
        "",
        f"- Release note: `{release_note}`",
        f"- Repository: `{repo}`",
        f"- Generated: `{now}`",
        f"- Changed files: `{len(diffs)}`",
        "- Validation status: `TODO`",
        "",
        "## Executive Summary",
        "",
        "TODO: Summarize which user-facing manual content changed and why.",
        "",
        "## Change Matrix",
        "",
        "| Release item | Manual file | Section | Before | After | Reason | Screenshot action |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    if diffs:
        for file_name, _ in diffs:
            lines.append(
                f"| TODO | `{file_name}` | TODO | TODO | TODO | TODO | keep / replace / add / skip |"
            )
    else:
        lines.append("| None | None | None | None | None | None | None |")

    lines.extend(
        [
            "",
            "## File-by-file Details",
            "",
        ]
    )

    for file_name, diff in diffs:
        lines.extend(
            [
                f"### `{file_name}`",
                "",
                "- Release item: TODO",
                "- Manual section: TODO",
                "- Before: TODO",
                "- After: TODO",
                "- Reviewer note: TODO",
                "",
                "<details>",
                "<summary>Raw diff</summary>",
                "",
                "```diff",
                diff.rstrip(),
                "```",
                "",
                "</details>",
                "",
            ]
        )

    lines.extend(
        [
            "## Skipped Or Deferred Release Items",
            "",
            "- TODO: List release items intentionally not reflected in the manual and why.",
            "",
            "## Validation",
            "",
            "- Sphinx build: TODO",
            "- Targeted keyword checks: TODO",
            "- HTML report validation: TODO",
            "",
            "## Final Flow Summary",
            "",
            "Release note input -> Manual impact triage -> RST/image edits -> Build validation -> HTML report output.",
            "",
        ]
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--release-note", required=True, type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "Markdown report path. Defaults to "
            "<release-note-package>/manual_update_report/<release-stem>-kc-manual-update-report.md. "
            "Explicit paths must stay inside the release-note package."
        ),
    )
    parser.add_argument("--baseline-dir", type=Path)
    parser.add_argument("--use-git-diff", action="store_true")
    parser.add_argument("--max-files", type=int, default=30)
    parser.add_argument("--max-diff-chars", type=int, default=120000)
    args = parser.parse_args()

    repo = args.repo.resolve()
    release_note = args.release_note.resolve()
    output = resolve_output_path(args.output, release_note)
    if args.baseline_dir and args.baseline_dir.exists():
        diffs = collect_baseline_diffs(repo, args.baseline_dir.resolve())
    elif args.use_git_diff:
        diffs = collect_git_diffs(repo, args.max_files, args.max_diff_chars)
    else:
        diffs = []
        print(
            "No baseline directory supplied. Generated an empty scaffold. "
            "Use --baseline-dir for before/after comparisons or --use-git-diff explicitly.",
            file=sys.stderr,
        )

    write_report(output, repo, release_note, diffs)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
