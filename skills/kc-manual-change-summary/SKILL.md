---
name: kc-manual-change-summary
description: Create concise Japanese kc-manual "マニュアル変更箇所" Markdown summaries from manual_update_report HTML or Markdown files. Use when the user provides or references a kc-manual manual update report and wants a short Japanese change-summary file matching the prior PDF-style format, including brief old/new descriptions without validation metadata or long explanations.
---

# KC Manual Change Summary

## Purpose

Turn a completed kc-manual manual update report into a concise Japanese Markdown file named like `vX.XXマニュアル変更箇所.md` or `<id>_vX.XXマニュアル変更箇所.md`.

The output should match the compact prior-report style: title, menu sections, change headings, and short `旧:` / `新:` summaries.

Language boundary: this skill's output summary is Japanese-only. This rule does not apply to the `manual_update_report` Markdown/HTML produced by `$kc-manual-release-update`; that review report follows the active user/repository response language while preserving source UI strings and raw snippets.

## Required Input

Require one source report before writing the summary:

- `manual_update_report/*.html`, or
- `manual_update_report/*.md`

The source must be a completed kc-manual manual update report with a change matrix, file-by-file details, or equivalent before/after descriptions. Do not require a specific filename. If the user only references `manual_update_report`, inspect that directory and choose the latest or most relevant report source.

If neither HTML nor Markdown source exists, ask for the report path. Do not reconstruct the summary only from memory.

## Workflow

1. Read the source report.
   - Prefer Markdown when both Markdown and HTML exist.
   - If using HTML, extract the change matrix first; then use file-by-file details only to clarify unclear rows.
2. Extract only user-facing manual changes:
   - release item or short change title
   - target manual file
   - before description
   - after description
   - added screenshots count, only when relevant
3. Group rows by manual area using the target file mapping below.
4. Write concise Japanese Markdown.
5. Validate by rereading the output and checking that it stayed compact.

## Output Format

Use this structure:

```markdown
# vX.XXマニュアル変更箇所

## 「SIM」メニューの操作

### Poller名の `Displayed after OTA` 表示を追加(console_sim)

旧: Poller名は OTA メニューで設定した Poller の名称として説明。

新: Poller OTA 未実行で Poller 名を取得できない場合の `Displayed after OTA` 表示を、SIM一覧、SIM詳細、絞り込み、OTA実行確認画面に追加。
```

Rules:

- Keep one change item per change-matrix row unless two rows are inseparable in the manual.
- Keep each `旧:` and `新:` to one short sentence when possible.
- Preserve Japanese UI strings and code literals exactly.
- Use Japanese output only, except code/file identifiers.
- Include screenshots only as a short phrase such as `キャプチャ3件を追加` when the report indicates screenshots were added.
- Do not include metadata, validation results, raw diffs, implementation history, source-sync notes, final flow summaries, or related-output tables.
- Do not list every edited line or every image path unless the compact source format clearly does so.

## Manual Area Mapping

Use these headings when the target file is known:

| Target file pattern | Heading |
| --- | --- |
| `console_sim.rst` | `## 「SIM」メニューの操作` |
| `console_esim.rst` | `## 「eSIM」メニューの操作` |
| `console_ota.rst` | `## 「OTA」メニューの操作` |
| `console_setting*.rst` | `## 「設定」メニューの操作` |
| `console_logout.rst` | `## 「ログアウト」メニューの操作` |
| `iot_safe_client.rst` | `## 「IoT SAFE Client」コマンドの操作` |

For unmapped files, derive a concise Japanese heading from the manual title or path. Keep the original kc-manual terminology.

## Compression Guidance

Aim for a report that feels like a review handout, not an audit trail.

Good:

```markdown
旧: eIM Action Status は作成日時とメッセージ中心の表示説明。

新: `操作`、未完了 Action の `取消`、確認ダイアログ、`Withdrawn` 表示、eSIM Info の最終アクション反映を説明。キャプチャ3件を追加。
```

Too detailed:

- multi-paragraph procedure descriptions
- raw RST snippets
- full validation logs
- every screenshot filename
- repeated notes copied from the manual

## Validation Checklist

Before finishing, check:

- The output has `# vX.XXマニュアル変更箇所`.
- Each change has both `旧:` and `新:`.
- The document is grouped by menu/command area.
- There is no Korean prose, except the user request context outside the artifact.
- There are no sections named `Metadata`, `Validation`, `関連成果物`, `反映フロー`, `変更一覧`, or `確認ポイント`.
- The summary is close to the change matrix in granularity.
