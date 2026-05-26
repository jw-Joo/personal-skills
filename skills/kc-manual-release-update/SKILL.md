---
name: kc-manual-release-update
description: Update the kc-manual Sphinx/RST documentation from a complete release note package and produce a review HTML report explaining before/after manual changes. Use when the user provides or references a full release note, exported release-note directory, Markdown/PDF release notes, screenshots, or asks which release changes require manual updates for kc-manual. Require the complete release note as input before editing; compare release items against existing manuals and update only existing user-facing documentation, not every implementation detail.
---

# KC Manual Release Update

## Purpose

Use this skill to turn a full project release note into a focused kc-manual documentation update. The goal is not to publish the release note itself, but to update existing manual content where the released behavior changes what users see, operate, configure, or troubleshoot.

When any manual file is changed, also create a separate review HTML report that explains what changed from before to after and why.

## Required Input

Require the complete release note before editing. Accept a release-note directory, Markdown file, PDF, text export, and any accompanying screenshots.

If the user only summarizes changes or omits the release note, ask for the full release note path or attachment first. If the user provides a directory, inspect all text files and images in that directory.

## Workflow

1. Read repository instructions first, including `AGENTS.md` or user-provided repository instructions.
2. Inventory the release package:
   - Use `rg --files` or `find` for release files.
   - Read the release note fully enough to list all top-level change items.
   - Note image references and decide later whether screenshots are actually needed.
3. Map release items to manual impact:
   - `Update`: user-facing UI, commands, visible states, labels, CSV/export fields, errors, validation, workflows, configuration users must set, or troubleshooting behavior.
   - `Usually skip`: runtime upgrades, dependency swaps, backend refactors, SDK migrations, build/deploy internals, private infrastructure, and API internals not documented for users.
   - `Confirm`: customer-facing configuration, environment variables, security/network restrictions, or operational behavior that may belong in a separate admin manual.
4. Locate existing manual sections:
   - Search with `rg` for feature names, labels, commands, status strings, API names, and screenshot filenames.
   - Prefer editing existing `.rst` files over creating new pages.
   - Use `references/kc-manual-map.md` when the repository is the standard kc-manual layout.
5. Draft a concise update plan before editing when more than one file is affected:
   - Release item
   - Decision: update / skip / confirm
   - Target manual file and section
   - User-facing wording to add or change
   - Screenshot action: keep / replace / add / skip
6. Capture pre-edit snapshots for every target file:
   - Store snapshots outside the repo, for example `/tmp/kc-manual-release-update-baseline/<relative-path>`.
   - Preserve repo-relative paths so the report can compare the exact before/after files.
   - If a target file already has user changes, treat the snapshot as the "before this manual update" baseline and do not revert it.
7. Edit manuals in the existing style:
   - Preserve the document language and terminology already used in the `.rst` file.
   - Do not paste implementation-heavy release-note prose into user manuals.
   - Describe observable behavior: what the user clicks, sees, enters, exports, or checks.
   - Keep notes short; avoid adding release-history narration unless the manual already uses it.
   - Copy images into the existing `source/applet/images/...` area only when they improve the manual.
8. Create the change report:
   - First create a Markdown source report, then use `$write-readable-html-docs` to create a standalone HTML report from that source.
   - Put all report artifacts in the input release-note package, not in the `kc-manual` repository:
     - If the input is a directory, use `<release-note-directory>/manual_update_report/`.
     - If the input is a single file, use `<release-note-file-parent>/manual_update_report/`.
   - Do not create `manual_update_report/` under the `kc-manual` repo. If the release-note package is not writable, ask the user for another output directory outside the repo.
   - Use `references/manual-update-report.md` for required report content.
   - The HTML report must compare before vs after for each modified manual section and explain the release-note reason for the change.
   - The HTML report must include a top maintenance comment and visible source-sync note because the Markdown report is authoritative.
   - Use `scripts/scaffold_change_report.py` with the captured baseline directory to scaffold the Markdown report when helpful, then fill in human-readable explanations before generating HTML.
9. Validate:
   - Run `make html` from the repo root when practical.
   - Run targeted `rg` checks for new visible terms from the release note.
   - Review `git diff` for accidental broad rewrites, broken RST indentation, or image path mistakes.
   - Validate the report HTML with `/home/user/.codex/skills/write-readable-html-docs/scripts/validate_html_doc.py <report.html> --require-source-note`.

## kc-manual Heuristics

The kc-manual repo is a Sphinx/RST manual. Common targets:

- Applet Console eSIM behavior: `source/applet/console_esim.rst`
- Applet Console SIM list/detail/OTA behavior: `source/applet/console_sim.rst`
- Logout behavior: `source/applet/console_logout.rst`
- IoT SAFE Client commands and troubleshooting: `source/applet/iot_safe_client.rst`
- OTA applet management: `source/applet/console_ota.rst`
- Console settings: `source/applet/console_setting.rst`

When the release note contains screenshots, first compare them with existing image references near the target section. Replace an image only if the current screenshot would mislead the reader; otherwise add text-only clarification.

## Optional Script

Use `scripts/release_note_inventory.py` to produce a first-pass list of release sections and candidate `.rst` matches:

```bash
python3 /home/user/.codex/skills/kc-manual-release-update/scripts/release_note_inventory.py \
  --release-note /path/to/release.md \
  --repo /path/to/kc-manual
```

Treat the script output as a starting point, not the final decision.

Use `scripts/scaffold_change_report.py` after editing to create a Markdown report source from captured baselines:

```bash
python3 /home/user/.codex/skills/kc-manual-release-update/scripts/scaffold_change_report.py \
  --repo /path/to/kc-manual \
  --release-note /path/to/release.md \
  --baseline-dir /tmp/kc-manual-release-update-baseline
```

Use its `--use-git-diff` fallback only in a clean, small worktree. In kc-manual, the worktree may contain broad pre-existing changes, so baseline snapshots are the reliable default.

The scaffold script prints the Markdown report path it created under the release-note package's `manual_update_report/` directory. Use `--output` only when the explicit path is still inside that same release-note package. Edit the generated Markdown to replace placeholders with reviewer-friendly before/after explanations, then invoke `$write-readable-html-docs` to create the `.html` next to it.

## Final Response

Summarize:

- Which release items were reflected
- Which were intentionally skipped and why
- Files changed
- Markdown and HTML report paths
- Validation run and result

Follow the repository's response language instructions.
