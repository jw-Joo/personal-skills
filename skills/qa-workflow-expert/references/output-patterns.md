# Output Patterns

## Recommended file layout

```text
<working-dir>/
  <feature>-commit-summary.md          # user input
  <feature>-qa-checklist.md            # markdown 1
  <feature>-verified-items-ja.md       # markdown 3
  qa-evidence/
    <feature>/
      qa-report.md                     # markdown 2
      target-check.log                 # optional startup / reachability evidence
      startup.log                      # optional local runtime startup evidence
      *.png
      *.json
      *.log
```

## Naming guidance

- Prefer the parent directory of the user-provided change-summary document as the working directory.
- Derive `<feature>` from the summary filename when possible.
- If the directory already contains obvious feature-specific names, reuse them instead of inventing new names.

## Checklist guidance

- Keep it focused on changed behavior, validation, permissions, limits, API exceptions, logging, and regressions.
- Remove trivial checks that are already implied by stronger downstream checks.
- Write the checklist in Korean.

## QA report guidance

- List tested targets, dates, role mapping, and PASS/FAIL/SKIP results.
- Attach evidence links per verified item.
- Note deviations such as role-label mismatches, unavailable tools, or cleanup exceptions.
- Write the QA report in Korean unless the user explicitly requested another language.
- For user-visible PASS items, link at least one screenshot and one raw `playwright-cli` artifact.
- When local startup or recovery was required, record the exact target URL the user requested, the actual reachable URL that was used, and the evidence files that prove the startup state.

## Local target guidance

- If the user gives an exact localhost URL, use that as the first QA target instead of inferring another environment from config files.
- Check the target with the same execution mode that will run `playwright-cli`; a sandbox-only `curl` result is not enough to declare the app down.
- If that localhost target is still unreachable, ask the user to confirm the URL or start the app; do not boot the local stack unless the user explicitly asked for that.
- If startup output shows `EADDRINUSE`, first verify whether the required service is already available before restarting or changing targets.
- Record the real reachable UI/API ports after startup because dev tooling may move from the default port to a fallback port.

## Screenshot guidance

- Capture evidence screenshots at a minimum width of 1600px.
- Increase to 1920px when the UI is too compressed at 1600px or when the wider capture materially improves readability.
- Treat narrow default screenshots as insufficient when important columns, buttons, or status areas are hard to read.
- Prefer consistency across the same feature run unless a wider screenshot is clearly needed for one view.
- Do not mark a user-visible item PASS without a fresh screenshot.

## Japanese summary guidance

- This is the only artifact that should be written in Japanese by default.
- Use `*` bullets only.
- Write concise bullets in the form `【ROLE/権限】...こと`.
- Keep only meaningful verifications.
- Merge related results into one bullet when that improves readability.
- This summary is mandatory and should be treated as the primary submission-ready deliverable.
- Do not substitute English bullets or an English-only close-out for this file.

## Language split guidance

- Default language split:
  - `*-verified-items-ja.md`: Japanese
  - checklist: Korean
  - `qa-report.md`: Korean
  - user-facing approval and completion messages: Korean
- Do not switch the checklist or QA report to Japanese just because the verified-items file is Japanese.

## Example summary lines

```text
* 【ROOT/ADMIN権限】Open APIキーを新規発行でき、発行直後のSecretを確認・コピーできること
* 【ROOT/ADMIN権限/API直接呼び出し】Open APIキーが100件の状態で101件目を発行しようとすると、サーバ側で拒否されること
* 【MEMBER権限】権限を持たないユーザーは、Open APIキーの発行・削除・備考更新が制限されること
```
