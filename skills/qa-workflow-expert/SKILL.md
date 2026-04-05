---
name: qa-workflow-expert
description: Use when the user provides a document summarizing code changes and wants end-to-end QA outputs in the same work directory, including a focused checklist, Playwright-backed evidence, a QA report, and a concise Japanese verification summary.
---

# QA Verification Workflow

## Overview

Turn a change-summary document into a complete QA package: a concise checklist, captured evidence, a verification report, and a short Japanese summary of meaningful checks.

Prefer executing the workflow end to end in one pass when the environment is ready, but stop after writing the checklist and wait for user approval before running the actual QA.

## Workflow

### 1. Establish the QA working context

- Treat the user-provided change-summary markdown as the source of truth for what changed.
- Use the parent directory of that document as the QA working directory.
- Derive a feature slug from the summary filename when the user did not provide explicit names.
- Reuse existing filenames if the directory already contains prior QA artifacts for the same feature.
- Search the repository for account-information files before asking the user for credentials.
- Use this filename priority when multiple candidates exist:
  - `Account.md`
  - `account.md`
  - `*account*.md`
  - `*credential*.md`
  - `*login*.md`
  - other clearly account-related files
- Select only one highest-priority candidate file for initial reference.
- Before using that file's contents for QA, ask the user to confirm that the selected file is the account-information file they prepared for you.
- Do not ask the user to verify the credential values themselves at this stage; confirm the file identity only.
- If the user says the file is not the intended source, continue with the next candidate or ask for credentials only when no credible candidate remains.
- Ask a concise question only if a required runtime input is still missing after the repository search and file-identity confirmation, such as target URL or credentials.

### 2. Write the checklist first

- Read the change summary and extract only meaningful checks:
  - new behavior
  - validation rules
  - permissions
  - limits and boundary values
  - API error handling
  - logging or audit effects
  - important regressions
- Do not pad the checklist with obvious prerequisite checks whose success is already implied by later functional checks.
- Save the checklist as markdown in the working directory.
- Use the naming pattern in [references/output-patterns.md](references/output-patterns.md).

### 3. Pause for checklist approval

- After saving the checklist, stop and ask the user for approval before running any real QA.
- Keep the approval request short and concrete.
- Do not start UI checks, API checks, data setup, or evidence capture before the user confirms the checklist is acceptable.
- If the user requests checklist changes, update the checklist first and ask for approval again.

### 4. Run the actual QA

- Use `playwright-cli` as the primary tool for UI verification.
- Prefer following the `playwright-cli` skill when that skill is available in the current agent environment.
- Use Playwright MCP only as a limited fallback when `playwright-cli` alone cannot complete a check credibly or cannot access the necessary browser capability.
- Use direct API calls when the important behavior is server-side only, such as invalid IDs, boundary limits, or non-UI error responses.
- If a specific UI check cannot be completed with `playwright-cli`, try limited MCP fallback only when it materially improves credibility.
- If both CLI and limited MCP fallback are unavailable or insufficient for a check, mark that check as FAIL or SKIP with the blocking reason and continue the remaining checks.
- Capture screenshots at a minimum width of 1600px.
- Increase screenshot width up to 1920px when the default view is too narrow to serve as credible evidence.
- Create a feature-specific evidence directory under `qa-evidence/`.
- Save raw evidence while testing:
  - screenshots
  - `playwright-cli` snapshots or command outputs
  - API responses
  - logs
  - cleanup results
  - role mapping notes when labels and actual roles differ

### 5. Write the QA report

- Save `qa-report.md` inside the feature-specific evidence directory.
- Record:
  - test date
  - target URLs
  - role/account mapping when relevant
  - PASS/FAIL/SKIP by check
  - links to concrete evidence files
- Only mark an item as PASS when there is a fresh artifact or direct observed result supporting it.

### 6. Write the final Japanese summary

- Save a short Japanese markdown summary in the working directory.
- Use `*` bullets.
- Write each bullet in the style `【ROLE/権限】...こと`.
- Keep only meaningful checks.
- Merge overlapping items instead of repeating obvious consequences.
- Prefer short, submission-ready sentences over detailed explanations.

## Evidence Rules

- Keep one evidence subdirectory per tested feature.
- Preserve raw artifacts; do not replace them with prose summaries only.
- Treat `playwright-cli` screenshots, snapshots, `run-code` results, console output, and network output as first-class evidence when they directly support a check.
- When MCP is used, record why CLI was not sufficient for that check.
- Do not rely on narrow default screenshots when key UI evidence is clipped or compressed.
- Prefer 1600px-wide screenshots by default, and move to 1920px when wider capture materially improves readability.
- Clean up generated test data when possible and record the final state.
- If cleanup cannot be completed, state that explicitly in the report.

## Output Rules

- Keep the checklist and final Japanese summary in the same directory as the input change-summary document.
- Keep the QA report and raw evidence inside `qa-evidence/<feature-slug>/`.
- Follow the concrete naming and content patterns in [references/output-patterns.md](references/output-patterns.md).

## Common Mistakes

- Writing a bloated checklist before understanding what actually changed.
- Trusting the first account-like file without confirming that it is the file the user intended to provide.
- Starting QA immediately after writing the checklist instead of waiting for user approval.
- Reporting PASS without preserving evidence.
- Using Playwright MCP by default when `playwright-cli` could credibly perform the same check.
- Using UI checks for cases that are more reliably verified through direct API calls.
- Aborting the entire QA run because one check could not be completed with CLI or fallback MCP.
- Keeping screenshots at a narrow default width even when the resulting evidence is hard to read.
- Filling the final Japanese summary with obvious checks like “screen opened normally” when later functional success already proves that.
- Forgetting to record account-role mismatches discovered during testing.
