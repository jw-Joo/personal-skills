---
name: api-pf-release-notes
description: Generate API-PF release note packages from a user-provided input directory. Use when Codex needs to create or update an API-PF release note from title files, commit-hash files, validation or walidation files, and screenshot images, then inspect API-PF git history directly and write the final package into the input directory's release_note_output folder.
---

# API-PF Release Notes

## Overview

Create one API-PF release note package from one user-provided input directory. Discover loose input files flexibly, inspect commit history directly with git, normalize validation content into plain bullet points, attach images, and write the final markdown output under `release_note_output/`.

## Quick Start

1. Ask for the target input directory path when the user has not already provided it.
2. Run `python3 scripts/discover_inputs.py "<input-dir>"` to find title, commit, validation, and image candidates.
3. Resolve any blocking ambiguity one question at a time.
4. Run `python3 scripts/extract_commit_hashes.py <commit-file>...` for every selected commit file.
5. Inspect commit history from the API-PF repository with `git show --stat --summary <hash>` and, when needed, `git show <hash> -- <path>` or `git show --name-only <hash>`.
6. Draft the release note with the structure from `assets/output_template.md`.
7. Copy images into `<input-dir>/release_note_output/` and reference them with relative paths.

## Run The Workflow

### 1. Discover Inputs

Use `scripts/discover_inputs.py` first. It searches the provided directory recursively, skips generated output directories, and classifies candidates into:

- `title_candidates`
- `commit_candidates`
- `validation_candidates`
- `image_candidates`

Treat the discovery output as an aid, not as the final answer. Read the candidate files before using them.

### 2. Resolve File Selection

Apply these rules:

- Auto-select a title file when there is exactly one title candidate.
- Ask the user to choose when there are multiple title candidates.
- Ask the user for a title when no title file exists.
- Use every discovered commit file unless the user says otherwise.
- Use every discovered validation file unless the user says otherwise.
- Use every discovered image unless the user says otherwise.
- Ask before overwriting an existing `<input-dir>/release_note_output/release_note.md`.

Ask one question at a time. State the fact pattern first, then ask the smallest possible question.

### 3. Extract Commit Hashes

Run `scripts/extract_commit_hashes.py` on all selected commit files. The script returns ordered, deduplicated hashes and reports non-hash lines for debugging.

If the script returns zero hashes:

1. Re-open the commit files and verify whether they contain short or full hashes.
2. Ask the user for corrected commit input if the files truly do not contain usable hashes.

### 4. Inspect Git History

Use git history directly from the API-PF repository. Do not rely on commit filenames or validation text alone.

For each hash:

1. Read the commit message with `git show --format=medium --no-patch <hash>`.
2. Inspect changed paths with `git show --stat --summary <hash>`.
3. Read more diff context only where needed to understand behavior.
4. Note user-visible changes first, then supporting implementation details.
5. Merge related commits into one coherent feature summary instead of listing commits mechanically.

## Determine Implementation Categories

Read `references/implementation-categories.md` before assigning categories.

Use only these category names:

- `インフラ`
- `フロントエンド`
- `バックエンド`
- `その他(API-PF 自体ではない)`

Use these heuristics:

- Prefer `フロントエンド` when changes are centered in `client/` or UI behavior.
- Prefer `バックエンド` when changes are centered in `server/`, `functions/`, `iotsafe/api/`, service logic, or API schemas.
- Prefer `インフラ` when changes are centered in deployment, CDK, docker, infrastructure configuration, or environment plumbing.
- Prefer `その他(API-PF 自体ではない)` only when the main deliverable is not an API-PF code change.
- Use multiple categories when the same feature spans multiple layers.

If category confidence is low after reading the diff, ask the user instead of guessing.

## Draft The Release Note

Read `references/output-format.md` and use `assets/output_template.md` as the structural template.

Write the sections in this order:

1. Title
2. `### 経緯`
3. `### 対応方針`
4. `### 実装内容`
5. `### 検証済みの内容`

Follow these rules:

- Read the title from the selected title file.
- Draft `経緯` from the product problem the commits are solving.
- Draft `対応方針` from the implementation strategy, not from low-level code details.
- Group `実装内容` bullets by implementation category, not by commit hash.
- Write `実装内容` for mixed technical and non-technical readers.
- Prioritize functional or operational change over implementation detail.
- Use concrete technical terms only when they materially improve understanding.
- Avoid raw internal details such as function names, environment variable names, exact file paths, scheduler expressions, or storage key formats unless the meaning would be lost without them.
- Prefer wording like "時間単位で管理できるようにした" over step-by-step implementation narration.
- Normalize validation content into plain Markdown bullet points only.
- Remove blockquote markers, checklist headers, and similar wrapper formatting from validation input.
- Keep the original item order, but rewrite every retained validation item as `- ...`.
- Attach every image under the relevant `実装内容` category section.
- When multiple categories exist, create a subsection for each category.

## Ask Questions Only When Necessary

Ask the user when one of these conditions blocks reliable output:

1. No input directory path is available
2. No title file exists
3. Multiple title files compete
4. No valid commit hashes can be extracted
5. Git history does not explain the intent well enough to draft `経緯`
6. Implementation category remains unclear
7. Frontend changes are detected but no image is available
8. An existing output file would be overwritten

For frontend changes without images:

- Tell the user that frontend changes were detected.
- Ask whether to proceed without images or wait for additional screenshots.
- Continue without images only after the user confirms.

## Write The Output Package

Create `<input-dir>/release_note_output/`.

Write:

- `<input-dir>/release_note_output/release_note.md`

Copy every selected image into the same directory and reference it with a relative path such as `![image.png](./image.png)`.

Keep the final document in Japanese to match the bundled template and existing release-note examples.

## Resources

- Use `references/implementation-categories.md` for the allowed category names and path heuristics.
- Use `references/output-format.md` for section-by-section output rules.
- Use `assets/output_template.md` as the output shape to mirror.
- Use `scripts/discover_inputs.py` before asking file-selection questions.
- Use `scripts/extract_commit_hashes.py` before inspecting git history.
