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
10. Actual request/processing flow near the bottom
11. Final flow summary graphic

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

## Actual Request / Processing Flow

Use near the bottom of API, QA, deployment, workflow, lifecycle, or architecture documents to show what actually happens for one representative run. Place it after detailed evidence/appendix and before the final flow summary graphic.

The section should answer these questions at a glance:

- What request, event, command, or trigger starts the flow?
- What payload/body/config is sent, and in what shape?
- Which public boundary receives it?
- Which internal modules, adapters, stores, queues, or external systems handle it?
- What logs, audit entries, status changes, or side effects prove it happened?
- What response, artifact, or final state is returned?

Use concrete values from the source when available, but redact sensitive values. Put long raw payloads, tokens, SQL, certificates, private keys, or very large JSON/hex behind `details`, or summarize them when they are not safe to expose.

```html
<section id="actual-processing" class="section">
  <h2>실제 요청 처리 흐름</h2>
  <p class="section-intro">대표 요청이 어디서 시작해 어떤 내부 처리를 거쳐 어떤 응답으로 돌아오는지 보여줍니다.</p>

  <div class="wire-visual">
    <div class="wire-row">
      <article class="http-card">
        <h3>1. 들어온 요청</h3>
        <div class="kv">
          <b>Method</b><span><code>POST</code></span>
          <b>Path</b><span><code>/example</code></span>
          <b>Header</b><span><code>X-Request-Id: qa-example</code></span>
        </div>
        <div class="payload-box">
          <p>Payload shape. Keep secrets redacted.</p>
          <code class="hex">{"example":"shape-only"}</code>
        </div>
      </article>

      <div class="wire-arrow" aria-hidden="true">→</div>

      <article class="http-card">
        <h3>최종 응답</h3>
        <div class="kv">
          <b>Status</b><span><code>200 OK</code></span>
          <b>Body</b><span><code>{"ok":true}</code></span>
        </div>
      </article>
    </div>

    <div class="process-lane">
      <article class="process-step">
        <span class="chip blue">Boundary</span>
        <strong>Public entry</strong>
        <p>How the request enters the system.</p>
      </article>
      <article class="process-step">
        <span class="chip good">Module</span>
        <strong>Internal processing</strong>
        <p>How the core module validates, translates, or persists it.</p>
      </article>
      <article class="process-step">
        <span class="chip warn">External call</span>
        <strong>Adapter / store</strong>
        <p>Which adapter, database, queue, or service is called.</p>
      </article>
      <article class="process-step">
        <span class="chip violet">Evidence</span>
        <strong>Observable proof</strong>
        <p>Which log, status, artifact, or response proves success.</p>
      </article>
    </div>

    <details>
      <summary>Raw request/response or command output</summary>
      <div class="details-body">
        <pre><code>Keep long but safe raw evidence here.</code></pre>
      </div>
    </details>
  </div>
</section>
```

Pair the structure with compact CSS classes such as `.wire-visual`, `.wire-row`, `.http-card`, `.kv`, `.payload-box`, `.process-lane`, `.process-step`, and `.wire-arrow`. Keep the request and response cards visually close enough that junior readers can compare “what went in” and “what came back” without scrolling.

## Final Flow Summary Graphic

Add a bottom-of-document graphic when the document describes a workflow, lifecycle, architecture path, request/response path, deployment, QA run, or implementation sequence. Place it after the appendix or the actual processing flow section, just before the footer, so readers finish with a compact mental model.

Use inline SVG or CSS/HTML blocks, not Mermaid runtime, so the document stays standalone. The graphic should show:

- the trigger or input
- the major modules or boundaries
- storage or no-storage policy
- delivery or output
- loss, retry, security, or rollback policy when those decisions matter
- the final observable result or response when the source includes one

```html
<section id="final-flow" class="section">
  <h2>Flow At A Glance</h2>
  <div class="diagram-shell" role="figure" aria-label="End-to-end flow graphic">
    <svg class="flow-graphic" viewBox="0 0 960 360" role="img" aria-labelledby="flow-title flow-desc">
      <title id="flow-title">End-to-end flow</title>
      <desc id="flow-desc">Compact final summary of the processing flow.</desc>
      <!-- Draw module boxes, arrows, and policy callouts here. -->
    </svg>
  </div>
</section>
```

Keep labels short and domain-specific. Do not use the graphic to introduce new decisions that are absent from the source document.

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
- `.wire-visual`, `.wire-row`, `.wire-arrow`, `.http-card`, `.kv`, `.payload-box`, `.process-lane`, `.process-step`
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
