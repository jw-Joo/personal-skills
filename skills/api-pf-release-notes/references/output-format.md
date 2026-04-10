# Output Format

Write one markdown file to `<input-dir>/release_note_output/release_note.md`.

Follow this section order:

1. `## <title>`
2. `### 経緯`
3. `### 対応方針`
4. `### 実装内容`
5. `### 検証済みの内容`

## Section Rules

### Title

- Read from the selected title file.
- Ask the user when no title file exists or when multiple title files compete.

### 経緯

- Draft from the product or operational problem visible in the commit history.
- Keep it concise and problem-focused.
- Ask the user when git history does not explain the motivation clearly enough.

### 対応方針

- Summarize the implementation strategy, not every code detail.
- Prefer one short paragraph or a short flat list.

### 実装内容

- Group details by implementation category.
- Attach images under the relevant category subsection.
- Preserve the input image order when multiple images are present.
- Write for readers who may include PM, QA, support, and engineers.
- Explain what changed in behavior, operation, or user experience before explaining how it was implemented.
- Keep technical terms only when they help understanding; avoid raw internal identifiers, exact paths, scheduler expressions, configuration keys, and similarly detailed implementation artifacts.
- Prefer concise statements of capability or outcome over step-by-step engineering narration.

### 検証済みの内容

- Normalize validation input into plain Markdown bullet points only.
- Remove blockquote markers, checklist headers, and similar wrapper formatting.
- Convert every retained validation item into `- ...` while preserving the original item order.
- Concatenate multiple validation files in discovery order.
