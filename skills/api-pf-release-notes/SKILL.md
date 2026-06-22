---
name: api-pf-release-notes
description: Generate API-PF release note packages from a user-provided directory or single release_input.md file. Use when Codex needs to create a new .scratch/RN input template with or without a user-provided name, process title, normal or merge commit hashes, validation or walidation notes, screenshots, inspect API-PF git history, and write the final package under release_note_output.
---

# API-PF Release Notes

## Overview

Create one API-PF release note package from either a single `release_input.md` file or legacy loose input files. Inspect commit history directly with git, normalize validation content into plain bullet points, attach images, and write the final markdown output under `release_note_output/`.

When the user asks for a new template, create a new fill-in template directory under `.scratch/RN/`, tell the user to fill `release_input.md`, and stop. If the user provides non-path text, use that text as the new template directory name after only filename-safety cleanup such as replacing path separators or control characters; preserve spaces, ticket numbers, bracketed labels, and Japanese text in the directory name. Also prefill `## Title` from the same text, but remove leading project-management prefixes that are not part of the user-facing feature title, such as a ticket number (`CC_NTTC-997`) and leading work-type labels (`【実装】`). If the user provides no text, use `TODO` as both the directory name and initial title. Do not draft a release note from an empty template.

## Input Modes

Prefer the single-file mode for new work.

### Single-file mode

Use `release_input.md` with these sections:

```markdown
## Title
Japanese release note title

## Commits
normal-or-merge-commit-hash

## Validation
- verification item

## Images
image.png
```

Parse it with `scripts/parse_release_input.py`. Use the parsed `title`, `commit_hashes`, `validation_items`, and `image_paths`. If the image section is empty, still use discovered image files from the same input directory unless the user says otherwise.

### Legacy loose-file mode

Continue to support separate title, commit, validation, and image files. Use this mode when no single input file exists.

## Quick Start

1. Resolve the user argument.
   - If the user provides an existing file, use it as `release_input.md`.
   - If the user provides an existing directory, scan that directory.
   - If the user asks for a new template and provides non-path text, create a new template directory under `.scratch/RN/<text>`.
   - For non-path text, keep the directory name as close to the user input as the filesystem allows, and prefill `## Title` with a cleaned title that removes leading ticket IDs and work labels such as `【実装】`.
   - If the user asks for a new template without a name, create a new template directory under `.scratch/RN/TODO`.
   - If no argument is available for a release-note generation request, create a `.scratch/RN/TODO` template instead of asking the user to create files manually.
2. If the target directory or input file does not exist, or if the request is specifically for a new template, create a template:
   - Run `python3 scripts/create_release_input_template.py "<name-or-path>"` when a name or path is available.
   - Run `python3 scripts/create_release_input_template.py` when no name or path is available.
   - Tell the user the created `release_input.md` path.
   - Ask the user to fill the template and rerun the skill.
   - Stop without writing `release_note_output/`.
3. Run `python3 scripts/discover_inputs.py "<input-dir>"`.
4. If one single input candidate exists, run `python3 scripts/parse_release_input.py <release_input.md>`.
5. Resolve any blocking ambiguity one question at a time.
6. Normalize commit hashes, expanding merge commits into merged-branch review targets and preserving each merge commit for final-result diff inspection.
7. Inspect commit history from the API-PF repository with `git show --stat --summary <hash>` and, when needed, `git show <hash> -- <path>` or `git show --name-only <hash>`.
8. Draft the release note with the structure from `assets/output_template.md`.
9. Copy images into `<input-dir>/release_note_output/` and reference them with relative paths.

## Template Creation

Use `scripts/create_release_input_template.py` before asking the user to manually create files.

Examples:

```bash
python3 scripts/create_release_input_template.py
python3 scripts/create_release_input_template.py 3977813
python3 scripts/create_release_input_template.py "CC_NTTC-997 【実装】「識別情報テンプレート」と「証明書ポリシー」を1画面にまとめる"
python3 scripts/create_release_input_template.py .scratch/RN/3977813
python3 scripts/create_release_input_template.py .scratch/RN/3977813/release_input.md
```

For no name, the script writes a new directory such as:

```text
.scratch/RN/TODO/release_input.md
```

For non-path text such as `3977813`, the script writes a new directory such as:

```text
.scratch/RN/3977813/release_input.md
```

For non-path text such as `CC_NTTC-997 【実装】「識別情報テンプレート」と「証明書ポリシー」を1画面にまとめる`, the script writes a new directory using that full text and prefills the title as `「識別情報テンプレート」と「証明書ポリシー」を1画面にまとめる`.

If that directory already exists, the script creates a sibling such as `.scratch/RN/3977813-2/release_input.md` or `.scratch/RN/TODO-2/release_input.md`. Do not overwrite an existing `release_input.md` unless the user explicitly asks with force-like intent. If the user is trying to generate a release note from an existing template but required fields are still missing, tell the user which fields are missing and ask them to fill the same file.

## Discover Inputs

Use `scripts/discover_inputs.py` after the target exists. It searches recursively, skips generated output directories, and classifies candidates into:

- `single_input_candidates`
- `title_candidates`
- `commit_candidates`
- `validation_candidates`
- `image_candidates`

Treat the discovery output as an aid, not as the final answer. Read or parse the candidate files before using them.

## Resolve File Selection

Apply these rules:

- Prefer single-file mode when exactly one `single_input_candidate` exists.
- Ask the user to choose when multiple single input candidates compete.
- In single-file mode, use parsed title, commits, validation items, and listed image paths.
- In single-file mode, also use discovered images from the same directory when the image section is empty.
- In legacy mode, auto-select a title file when there is exactly one title candidate.
- In legacy mode, ask the user to choose when there are multiple title candidates.
- In legacy mode, ask the user for a title when no title file exists.
- Use every discovered commit file unless the user says otherwise.
- Use every discovered validation file unless the user says otherwise.
- Use every discovered image unless the user says otherwise.
- Ask before overwriting an existing `<input-dir>/release_note_output/release_note.md`.

Ask one question at a time. State the fact pattern first, then ask the smallest possible question.

## Extract Commit Hashes

For single-file mode, use the `commit_hashes` returned by `scripts/parse_release_input.py`.

For legacy loose-file mode, run `scripts/extract_commit_hashes.py` on all selected commit files. The script returns ordered, deduplicated hashes and reports non-hash lines for debugging.

If zero hashes are found:

1. Re-open the input and verify whether it contains short or full hashes.
2. Ask the user for corrected commit input if the input truly does not contain usable hashes.

## Normalize Commit Inputs

Normalize extracted commit hashes before drafting. Treat normal commits and merge commits differently so the release note reflects both the feature-side work and the final result that landed on the target branch.

For each extracted hash:

1. Check whether it is a merge commit with `git rev-list --parents -n 1 <hash>`.
2. If the hash has one parent, keep it as a normal inspection target.
3. If the hash has two parents, treat it as a normal merge commit:
   - Treat `<hash>^1` as the pre-merge target branch unless history clearly shows otherwise.
   - Treat `<hash>^2` as the merged branch tip unless history clearly shows otherwise.
   - Extract merged-branch normal commits with `git log --reverse --format=%H --no-merges <hash>^1..<hash>^2`.
   - Check whether the merged branch contains merge commits with `git log --reverse --oneline --merges <hash>^1..<hash>^2`.
   - Preserve the merge commit itself as a final-result inspection target.
4. If the hash has more than two parents, ask the user which parent represents the feature branch unless the intent is obvious from the commit message and graph.
5. If a merge commit appears to have the target branch and merged branch parents reversed, correct the parent interpretation before extracting the merged-branch commits.
6. Deduplicate normalized inspection targets while preserving input order.

For every preserved merge commit, inspect the final landed result with:

- `git diff --stat <hash>^1 <hash>`
- `git diff --name-status <hash>^1 <hash>`

Use this final diff as the source of truth for what actually landed on the target branch. If conflict resolution or manual adjustment exists only in the merge commit, include that behavior in the release-note analysis even though it is not part of the merged-branch normal commit list.

If the input hash is a squash merge commit or a fast-forward result without a merge commit, Git history may not preserve the original feature commit range. In that case, inspect the provided commit directly and ask for PR metadata, original branch history, or corrected commit input only when the commit itself does not explain the release-note content.

## Inspect Git History

Use git history directly from the API-PF repository. Do not rely on commit filenames, template text, or validation text alone.

For each normalized inspection target:

1. Read the commit message with `git show --format=medium --no-patch <hash>`.
2. Inspect changed paths with `git show --stat --summary <hash>`.
3. Read more diff context only where needed to understand behavior.
4. For preserved merge commits, inspect the final first-parent diff with `git diff --stat <hash>^1 <hash>` and `git diff --name-status <hash>^1 <hash>`.
5. Note user-visible changes first, then supporting implementation details.
6. Merge related commits into one coherent feature summary instead of listing commits mechanically.

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

- Read the title from parsed single input or the selected title file.
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
- Use Markdown level-4 headings for implementation category subsections, such as `#### フロントエンド`; do not use bold-only labels such as `**フロントエンド**`.

## Ask Questions Only When Necessary

Ask the user when one of these conditions blocks reliable output:

1. No target name, input file, or input directory is available
2. The target does not exist and template creation fails
3. A required single-file field is missing after the user has filled the template
4. No title exists
5. Multiple title files compete in legacy mode
6. No valid commit hashes can be extracted
7. Git history does not explain the intent well enough to draft `経緯`
8. Implementation category remains unclear
9. Frontend changes are detected but no image is available
10. An existing output file would be overwritten
11. A merge commit has more than two parents and the feature-side parent cannot be inferred safely

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

- Use `scripts/create_release_input_template.py` to create `.scratch/RN` templates.
- Use `scripts/parse_release_input.py` for single-file mode.
- Use `scripts/discover_inputs.py` before asking file-selection questions.
- Use `scripts/extract_commit_hashes.py` for legacy commit files.
- Use `references/implementation-categories.md` for the allowed category names and path heuristics.
- Use `references/output-format.md` for section-by-section output rules.
- Use `assets/output_template.md` as the output shape to mirror.
