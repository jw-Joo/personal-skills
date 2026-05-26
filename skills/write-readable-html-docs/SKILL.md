---
name: write-readable-html-docs
description: Create or update standalone, review-friendly HTML versions of dense Markdown or text design documents. Use when Codex is asked to turn a design doc, architecture note, specification, QA report, implementation plan, or long Markdown file into a human-readable HTML document that actively uses HTML affordances such as navigation, summary panels, flow diagrams, comparison tables, callouts, collapsible details, timelines, and checklists instead of merely rendering the original Markdown.
---

# Write Readable HTML Docs

## Goal

Transform dense source documents into standalone HTML documents that help humans decide quickly:

- Put the core story first.
- Use visual structure to separate overview from details.
- Preserve source meaning without copying the original section order blindly.
- Make the result easy to scan, review, print, and maintain.

## Core Rule: Source Stays Authoritative

When the HTML is derived from an existing Markdown/source file, treat the source file as the canonical content.

- Include a visible note in the generated HTML: if the HTML content is later changed and the original Markdown/source still exists, update the source file together with the HTML.
- Put the source-sync rule near the top of the HTML, not only in the footer:
  - Add a maintenance HTML comment within the first 20 lines.
  - Add a visible note immediately after the hero/header or in the metadata area.
- If a user asks for a content change to the HTML and the source Markdown exists, edit both files unless the user explicitly says HTML-only.
- If a user asks for layout/style-only changes, keep the source Markdown unchanged.
- Keep a link to the source document in the HTML footer or metadata strip when possible.

Use wording like:

```html
<!--
  Maintenance contract:
  Source Markdown: ./source-file.md
  If editing document content in this HTML, update the source Markdown together.
  Style/layout-only HTML changes do not require a Markdown update.
-->
<p class="source-note">
  원본 Markdown이 존재하는 문서입니다. 내용 수정 시 이 HTML만 고치지 말고 원본 Markdown도 함께 갱신하세요.
</p>
```

## Workflow

1. Read the source document structure.
   - Use `rg -n '^(#{1,4}) '` for Markdown headings.
   - Read enough content to understand purpose, decisions, interfaces, risks, and implementation phases.
   - Do not assume the original order is the best reading order.

2. Identify the reader path.
   - What should a reviewer understand in the first 30 seconds?
   - What decisions are already made?
   - What details should be hidden until needed?
   - What implementation or QA gates should be easy to check?

3. Design the HTML information architecture.
   - Hero: title, concise summary, 3-4 key metrics.
   - Sticky/early navigation: short section labels.
   - Main sections: overview, flow, responsibility, contract/API, storage/config, implementation, validation, decisions.
   - Appendix: long mappings, schemas, raw examples, edge cases, detailed TODOs.
   - Final flow summary: add a bottom-of-document graphic that lets readers understand the end-to-end processing flow at a glance.

4. Write standalone HTML.
   - Embed CSS in the file unless the user asks for shared assets.
   - Use semantic elements: `header`, `nav`, `main`, `section`, `article`, `details`, `summary`, `table`.
   - Prefer CSS grids, flow cards, callouts, chips, timelines, and checklists over long paragraphs.
   - Add the final flow summary near the bottom, before the footer or after the appendix. Use inline SVG or CSS/HTML blocks so it works without external runtimes.
   - Keep colors restrained and not one-note. Use neutral base with a few semantic accents.
   - Preserve code blocks and exact identifiers with `code`/`pre`.

5. Validate.
   - Check internal anchor links and duplicate ids.
   - Check that the top maintenance comment and visible source-sync note exist when a source file exists.
   - Check that the document has enough structural affordances: sections, details, tables, callouts, or checklists.
   - Run `scripts/validate_html_doc.py` when available.

## HTML Patterns

Read `references/html-patterns.md` when building or revising a document. It contains concise patterns for:

- hero + metadata strip
- flow diagrams
- final flow summary graphic
- responsibility matrix
- source synchronization note
- collapsible appendix
- implementation timeline
- review checklist

## Output Rules

- Create a separate `.html` file next to the source unless the user requests another path.
- Name it after the source file stem, usually `source-name.html`.
- Preserve the source language. For Korean docs, write Korean UI labels and notes.
- Do not expose private secrets, full tokens, private keys, or sensitive raw payloads.
- If the source has Mermaid, do not rely on Mermaid runtime unless the user wants external scripts. Recreate the meaning with HTML/CSS flow blocks.
- When the source document exists and the final flow summary changes document content, update the source with an equivalent text, Mermaid, or diagram description.
- Avoid turning every original heading into a top-level HTML section. Reorganize by reader usefulness.
- Put long raw mappings, SQL, OpenAPI snippets, and exhaustive tables behind `details` unless they are central to first-pass understanding.
- Mention in the final response where the file was created and what validation was run.

## Validation Command

Use:

```bash
python3 /home/user/.codex/skills/write-readable-html-docs/scripts/validate_html_doc.py path/to/document.html --require-source-note
```

Omit `--require-source-note` only when there is no source document or the output is intentionally standalone.
