# HTML Patterns

Use these patterns to make dense design docs readable in a browser. Adapt labels to the source language.

## Recommended Reading Order

1. Hero with one-sentence thesis
2. Key metrics strip
3. "Core first" summary cards
4. Visual flow or boundary map
5. Responsibility/decision matrix
6. Contracts, APIs, storage, configuration
7. Implementation timeline
8. Review checklist
9. Collapsible appendix for exhaustive details

## Hero + Metrics

Use for first-screen orientation.

```html
<header class="hero">
  <div class="hero-main">
    <p class="eyebrow">Design Document</p>
    <h1>Document Title</h1>
    <p class="hero-copy">One or two sentences that state the thesis and highest-risk decision.</p>
  </div>
  <div class="meta-strip">
    <div><strong>1 route</strong><span>POST /example</span></div>
    <div><strong>3 modules</strong><span>producer / API / frontend</span></div>
    <div><strong>2 stores</strong><span>outbox / notification</span></div>
    <div><strong>4 phases</strong><span>record -> publish -> socket -> UI</span></div>
  </div>
</header>
```

## Source Synchronization Note

Use whenever the HTML is derived from a Markdown/source document.

Place a machine-readable maintenance comment near the top of the file so an agent that opens only the first lines sees the contract:

```html
<!doctype html>
<!--
  Maintenance contract:
  Source Markdown: ./source-file.md
  If editing document content in this HTML, update the source Markdown together.
  Style/layout-only HTML changes do not require a Markdown update.
-->
```

Also place a visible note immediately after the hero/header or in the metadata area:

```html
<p class="source-note">
  원본 Markdown이 존재하는 문서입니다. 내용 수정 시 이 HTML만 고치지 말고 원본 Markdown도 함께 갱신하세요.
</p>
```

Keep the source link in the footer if useful, but do not rely on footer-only guidance. A line-targeted edit may never load the footer into context.

## Flow Cards

Use instead of Mermaid when producing standalone HTML without external scripts.

```html
<div class="flow">
  <div class="flow-step">
    <b>Input</b>
    <span class="chip">Trigger</span>
    <p>What enters the system.</p>
  </div>
  <div class="flow-step">
    <b>Adapter</b>
    <span class="chip warn">Boundary</span>
    <p>What is translated or validated.</p>
  </div>
  <div class="flow-step">
    <b>Store</b>
    <span class="chip good">Durable</span>
    <p>Where state is saved.</p>
  </div>
</div>
```

## Details Appendix

Use for long tables, raw mappings, schemas, examples, and edge cases.

```html
<details>
  <summary>Detailed mapping</summary>
  <div class="details-body">
    <div class="table-wrap">
      <table>
        <thead><tr><th>Input</th><th>Output</th><th>Rule</th></tr></thead>
        <tbody><tr><td>...</td><td>...</td><td>...</td></tr></tbody>
      </table>
    </div>
  </div>
</details>
```

Open only the most important details by default. Keep exhaustive material closed.

## Review Checklist

Use for acceptance criteria, QA gates, and implementation guardrails.

```html
<ul class="checklist">
  <li>Public routes are limited to the documented boundary.</li>
  <li>Secrets are never displayed or logged.</li>
  <li>Source Markdown is updated with content changes.</li>
</ul>
```

## Minimal CSS Classes

Prefer these reusable classes:

- `.page`, `.sidebar`, `.content`
- `.hero`, `.hero-main`, `.meta-strip`
- `.section`, `.grid`, `.panel`
- `.callout`, `.callout.warn`, `.callout.danger`
- `.chips`, `.chip`, `.chip.good`, `.chip.warn`, `.chip.no`
- `.flow`, `.flow-step`
- `.matrix`, `.module`
- `.table-wrap`
- `details`, `summary`, `.details-body`
- `.timeline`, `.checklist`
- `.source-note`, `.footer`

## CSS Constraints

- Make the document standalone.
- Use responsive grids and avoid viewport-scaled font sizes.
- Keep cards at 8px border radius or less.
- Use neutral paper/background colors and semantic accents.
- Use print styles that hide navigation and expand details.
- Ensure tables can scroll horizontally on small screens.
