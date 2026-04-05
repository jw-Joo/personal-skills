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

## QA report guidance

- List tested targets, dates, role mapping, and PASS/FAIL/SKIP results.
- Attach evidence links per verified item.
- Note deviations such as role-label mismatches, unavailable tools, or cleanup exceptions.

## Screenshot guidance

- Capture evidence screenshots at a minimum width of 1600px.
- Increase to 1920px when the UI is too compressed at 1600px or when the wider capture materially improves readability.
- Treat narrow default screenshots as insufficient when important columns, buttons, or status areas are hard to read.
- Prefer consistency across the same feature run unless a wider screenshot is clearly needed for one view.

## Japanese summary guidance

- Use `*` bullets only.
- Write concise bullets in the form `【ROLE/権限】...こと`.
- Keep only meaningful verifications.
- Merge related results into one bullet when that improves readability.

## Example summary lines

```text
* 【ROOT/ADMIN権限】Open APIキーを新規発行でき、発行直後のSecretを確認・コピーできること
* 【ROOT/ADMIN権限/API直接呼び出し】Open APIキーが100件の状態で101件目を発行しようとすると、サーバ側で拒否されること
* 【MEMBER権限】権限を持たないユーザーは、Open APIキーの発行・削除・備考更新が制限されること
```
