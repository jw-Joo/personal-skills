---
name: qa-workflow-expert
description: Use when the user provides a document summarizing code changes and wants end-to-end QA outputs in the same work directory, including a focused checklist, Playwright-backed evidence, a Korean QA report, and a Japanese verified-items summary.
---

# QA Verification Workflow

## Overview

Turn a change-summary document into a complete QA package: a concise checklist, captured evidence, a verification report, and a short verified-items summary of meaningful checks.

Language rule:

- Write `*-verified-items-ja.md` in Japanese.
- Write every other artifact in Korean:
  - checklist
  - QA report
  - approval request
  - blocker questions
  - final user-facing completion message
- Do not let the Japanese verified-items file influence the language of the other outputs.

Prefer executing the workflow end to end in one pass when the environment is ready, but stop after writing the checklist and wait for user approval before running the actual QA.

Playwright-first rule:

- Treat `playwright-cli` verification as mandatory for every QA run that includes any user-visible flow.
- Do not complete a QA run with only unit tests, integration tests, or source inspection when a user-visible path exists.
- Unit and integration tests are optional supporting evidence only; they never replace required `playwright-cli` evidence for UI or end-to-end checks.
- If `playwright-cli` cannot be used immediately, actively work to make it usable before proceeding.

Local-target-first rule:

- If the user gives an exact target such as `http://localhost:8080/`, treat that URL as the primary QA target.
- Try reaching the user-provided target with `playwright-cli` before restarting servers, switching environments, or investigating remote domains.
- Do not assume the local app is down until the same execution context that will run `playwright-cli` has failed to reach it.
- Never start local servers on the user's behalf unless the user explicitly asked for that startup work.
- If the user-provided localhost target is unreachable, ask the user to confirm the URL or start the app instead of launching the stack yourself.

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
- Ask a concise question only if a required runtime input is still missing after the repository search and file-identity confirmation, such as target URL, environment startup instructions, or credentials.
- A Playwright-reachable target is a required runtime input for any QA run with user-visible behavior.
- If the user provides an explicit local URL, record it immediately as the primary target instead of inferring another target from environment files.

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
- Write the checklist in Korean.

### 3. Pause for checklist approval

- After saving the checklist, stop and ask the user for approval before running any real QA.
- Keep the approval request short and concrete.
- Write the approval request in Korean.
- Do not start UI checks, API checks, data setup, or evidence capture before the user confirms the checklist is acceptable.
- If the user requests checklist changes, update the checklist first and ask for approval again.

### 4. Run the actual QA

- Use `playwright-cli` as the primary and mandatory tool for UI verification.
- Prefer following the `playwright-cli` skill when that skill is available in the current agent environment.
- Before executing the checklist, verify that there is a reachable target for `playwright-cli`.
- Use this local-target preflight order before broader troubleshooting:
  - if the user already gave a URL, try that exact URL with `playwright-cli` first
  - if the target is local, verify reachability from the same privilege/sandbox context that will run `playwright-cli`
  - only if that exact target is unreachable, ask the user to confirm the URL or start the required app
  - after the user confirms or starts it, re-check the actual reachable UI and API URLs before doing any QA steps
- If no reachable target exists yet, stop and ask the user for the missing URL or environment-start instructions instead of downgrading to test-only QA.
- If `playwright-cli` is unavailable, missing browsers, blocked by missing dependencies, or blocked by a stopped local app, try to fix that first.
- When fixing it requires permission or installation, explicitly ask the user and continue once approved.
- Do not interpret a general QA request as permission to start local servers.
- Exhaust reasonable remediation first:
  - confirm whether `playwright-cli` is installed
  - install browsers or dependencies when permitted
  - ask the user to start the local app or confirm the target URL when localhost is not reachable
  - ask the user for target URL, VPN access, credentials, or environment startup help when those are the true blockers
- Treat these cases carefully during remediation:
  - `EADDRINUSE` usually means a port is already occupied, not that QA is impossible; first check whether the needed service is already serving traffic
  - a dev server may bind to a fallback port such as `8081`; record the actual reachable URL instead of assuming the default port won
  - sandbox-local `curl` failures do not prove an outside-sandbox browser or service is unreachable; verify with the same execution mode that will run `playwright-cli`
  - if UI snapshots prove the target is live, do not derail into remote-domain or DB troubleshooting unless a checklist item truly needs it
- When repo config mixes local UI targets and remote backend/domain values, prefer observed reachability and actual runtime behavior over early assumptions from `.env` files alone.
- If the user said "run the local server and check `localhost`", prefer that route over speculative remote-environment investigation.
- If the user did not explicitly ask you to boot the local stack, do not start it just because localhost was unreachable.
- For each checklist item that has a user-visible flow, require fresh `playwright-cli` evidence before considering PASS.
- Use Playwright MCP only as a limited fallback when `playwright-cli` alone cannot complete a check credibly or cannot access the necessary browser capability.
- Use direct API calls when the important behavior is server-side only, such as invalid IDs, boundary limits, or non-UI error responses.
- If a specific UI check cannot be completed with `playwright-cli`, try limited MCP fallback only when it materially improves credibility for that same blocked UI check.
- If both CLI and limited MCP fallback are unavailable or insufficient for a required UI check, mark that check as FAIL or BLOCKED with the blocking reason.
- Do not treat unit tests, integration tests, or source inspection as substitutes for a blocked `playwright-cli` UI check.
- Use unit tests or integration tests only as secondary evidence that supplements a Playwright-verified result, or for server-only checks with no meaningful user-visible path.
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
  - target reachability or startup diagnostics when local environment recovery was needed

### 5. Write the QA report

- Save `qa-report.md` inside the feature-specific evidence directory.
- Write the QA report in Korean unless the user explicitly requested another language.
- Record:
  - test date
  - target URLs
  - role/account mapping when relevant
  - PASS/FAIL/SKIP by check
  - links to concrete evidence files
- Only mark an item as PASS when there is a fresh artifact or direct observed result supporting it.
- For a user-visible PASS item, that fresh artifact must include `playwright-cli` evidence and at least one readable screenshot.

### 6. Write the final Japanese summary

- Save a short Japanese markdown summary in the working directory.
- This file alone is the mandatory Japanese deliverable; it does not change the required language of the other outputs.
- Use `*` bullets.
- Write each bullet in the style `【ROLE/権限】...こと`.
- Keep only meaningful checks.
- Merge overlapping items instead of repeating obvious consequences.
- Prefer short, submission-ready sentences over detailed explanations.
- Do not replace this file with English bullets or an English-only conclusion.
- In the final user-facing completion message, write in Korean and lead with the Japanese summary file as the primary deliverable.

## Evidence Rules

- Keep one evidence subdirectory per tested feature.
- Preserve raw artifacts; do not replace them with prose summaries only.
- Treat `playwright-cli` screenshots, snapshots, `run-code` results, console output, and network output as first-class evidence when they directly support a check.
- For every Playwright-verified UI item, save at least one screenshot and one raw `playwright-cli` artifact.
- A user-visible checklist item cannot be PASS without fresh `playwright-cli` evidence.
- When MCP is used, record why CLI was not sufficient for that check.
- Do not rely on narrow default screenshots when key UI evidence is clipped or compressed.
- Prefer 1600px-wide screenshots by default, and move to 1920px when wider capture materially improves readability.
- Unit and integration test logs are supplementary only; they do not satisfy the Playwright evidence requirement for UI or end-to-end checks.
- If no Playwright-reachable target exists, pause and ask for the missing runtime instead of finishing the QA package with test-only evidence.
- Do not give up on `playwright-cli` at the first failure; attempt setup, installation, startup, or user-assisted remediation first.
- When the target is local, preserve enough startup or reachability evidence to show whether the app was already up, newly started, or blocked by environment issues.
- Clean up generated test data when possible and record the final state.
- If cleanup cannot be completed, state that explicitly in the report.

## Output Rules

- Keep the checklist and final Japanese summary in the same directory as the input change-summary document.
- Keep the QA report and raw evidence inside `qa-evidence/<feature-slug>/`.
- Follow the concrete naming and content patterns in [references/output-patterns.md](references/output-patterns.md).
- Only `*-verified-items-ja.md` may be written in Japanese by default.
- The checklist, QA report, and final close-out message must be written in Korean by default.
- Do not treat an English QA report, English bullet list, or English close-out message as fulfilling the mandatory Japanese summary requirement.

## Common Mistakes

- Writing a bloated checklist before understanding what actually changed.
- Trusting the first account-like file without confirming that it is the file the user intended to provide.
- Starting QA immediately after writing the checklist instead of waiting for user approval.
- Reporting PASS without preserving evidence.
- Falling back to unit tests, integration tests, or source inspection when `playwright-cli` verification was required.
- Completing a QA package without any Playwright screenshots for user-visible checks.
- Treating a missing browser, missing target URL, stopped app, or missing permission as a reason to skip Playwright without first trying to fix it.
- Ignoring the exact local URL the user provided and exploring a different environment first.
- Declaring `localhost` unreachable from a sandbox-only check when the actual browser and dev servers are running outside that sandbox.
- Starting the local stack without explicit user approval after a localhost reachability failure.
- Treating `EADDRINUSE` as a startup failure instead of checking whether an existing process already satisfies the QA target.
- Assuming the default dev port is correct after startup instead of recording the real reachable port.
- Letting remote `.env` values drive the investigation before checking whether the user-requested local route already works.
- Using Playwright MCP by default when `playwright-cli` could credibly perform the same check.
- Using UI checks for cases that are more reliably verified through direct API calls.
- Aborting the entire QA run because one check could not be completed with CLI or fallback MCP.
- Keeping screenshots at a narrow default width even when the resulting evidence is hard to read.
- Filling the final Japanese summary with obvious checks like “screen opened normally” when later functional success already proves that.
- Delivering the final summary or completion package only in English when Japanese delivery was expected.
- Forgetting to record account-role mismatches discovered during testing.
