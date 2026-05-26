# Manual Update Report Requirements

Create this report whenever `kc-manual-release-update` changes manual files.

## Source And Output

- Create a Markdown source report first.
- Generate a standalone HTML report from that Markdown using `$write-readable-html-docs`.
- Keep the Markdown report authoritative. The HTML must include the source-sync maintenance comment and visible source note.
- Report artifacts must live inside the input release-note package, not in the `kc-manual` repository.
- Directory rule:
  - Directory input: `<release-note-directory>/manual_update_report/`
  - File input: `<release-note-file-parent>/manual_update_report/`
- If the release-note package is not writable, ask for another output directory outside the `kc-manual` repository instead of falling back to `<repo>/manual_update_report/`.
- Recommended names:
  - `<release-stem>-kc-manual-update-report.md`
  - `<release-stem>-kc-manual-update-report.html`

## Required Report Sections

1. Title and metadata:
   - Release note path or package path
   - kc-manual repo path
   - Report generation date
   - Changed files count
   - Validation status
2. Executive summary:
   - What changed in the manual
   - Why the change was needed
   - What was intentionally not reflected
3. Change matrix:
   - Release item
   - Manual file
   - Section
   - Before
   - After
   - Reason
   - Screenshot action
4. File-by-file before/after details:
   - Show short "Before" and "After" snippets for each changed section.
   - Explain the user-visible difference in plain language.
   - Include raw diff in a collapsible appendix, not as the first-pass reading path.
5. Skipped or deferred release items:
   - State why each item did not change the manual.
6. Validation:
   - Sphinx build result
   - Targeted keyword checks
   - HTML report validation result
7. Final flow summary:
   - Release note input
   - Manual impact triage
   - RST/image edits
   - Build validation
   - HTML report output

## HTML Shape

When creating the HTML via `$write-readable-html-docs`, use:

- Hero with one-sentence result.
- Metric strip for changed files, reflected items, skipped items, validation.
- Navigation links.
- Summary cards for high-impact changes.
- A comparison table for before/after.
- Collapsible raw diff appendix.
- Checklist for validation.
- Final flow summary graphic near the bottom.

Do not expose secrets, tokens, private keys, or sensitive raw payloads from release notes or diffs.
