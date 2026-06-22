# Output Format

Write two markdown files under `<input-dir>/release_note_output/`:

- `release_note.md`: the official Japanese release note
- `release_note_ko.md`: a Korean review copy with the same facts, structure, and image references

For `release_note.md`, follow this section order:

1. `## <title>`
2. `### 経緯`
3. `### 対応方針`
4. `### 実装内容`
5. `### 検証済みの内容`

For `release_note_ko.md`, follow the same structure with Korean headings:

1. `## <translated title>`
2. `### 배경`
3. `### 대응 방침`
4. `### 구현 내용`
5. `### 검증한 내용`

## Section Rules

### Title

- Read from parsed `release_input.md` in single-file mode.
- In legacy mode, read from the selected title file.
- Ask the user when no title exists or when multiple legacy title files compete.
- Translate the title faithfully for `release_note_ko.md`; keep quoted UI labels recognizable.

### 経緯

- Draft from the product or operational problem visible in the commit history.
- Keep it concise and problem-focused.
- Ask the user when git history does not explain the motivation clearly enough.

### 対応方針

- Summarize the implementation strategy, not every code detail.
- Prefer one short paragraph or a short flat list.

### 実装内容

- Group details by implementation category using Markdown level-4 headings such as `#### フロントエンド`. Do not use bold-only category labels such as `**フロントエンド**`.
- Attach images under the relevant category subsection.
- Preserve the input image order when multiple images are present.
- Write for readers who may include PM, QA, support, and engineers.
- Explain what changed in behavior, operation, or user experience before explaining how it was implemented.
- Keep technical terms only when they help understanding; avoid raw internal identifiers, exact paths, scheduler expressions, configuration keys, and similarly detailed implementation artifacts.
- Prefer concise statements of capability or outcome over step-by-step engineering narration.
- In `release_note_ko.md`, translate category headings to Korean while preserving grouping: `#### 프론트엔드`, `#### 백엔드`, `#### 인프라`, and `#### 기타(API-PF 자체는 아님)`.
- In `release_note_ko.md`, keep the same image references, for example `![image.png](./image.png)`.

### 検証済みの内容

- Normalize validation input from parsed `release_input.md` or selected validation files into plain Markdown bullet points only.
- Remove blockquote markers, checklist headers, and similar wrapper formatting.
- Convert every retained validation item into `- ...` while preserving the original item order.
- Concatenate multiple validation files in discovery order.
- Translate the normalized validation bullets faithfully for `release_note_ko.md`, preserving the original item order.

## Korean Review Copy Rules

- Treat `release_note.md` as the source of truth, then produce `release_note_ko.md` from the same facts.
- Do not add implementation details, verification items, or caveats that are not present in the Japanese release note or inspected git history.
- Preserve Markdown structure, bullet order, and image placement.
- Keep product names, file-independent technical terms, ticket numbers, and recognizable UI labels clear enough to compare with the Japanese source.
