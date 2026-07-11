---
name: write-codebase-language-tutorial
description: Create or revise a zero-assumption programming-language tutorial grounded in an existing service codebase. Use when a user wants to learn Go, Rust, TypeScript/React, or another unfamiliar language through real service code; needs a beginner onboarding guide that traces entrypoints and actual data/control flow; or is iteratively asking basic questions that must be incorporated into an existing codebase tutorial rather than answered only in chat.
---

# Write Codebase Language Tutorial

Create a tutorial that teaches only the language and framework concepts needed to read one real service. Treat repository code as the primary source and assume the reader knows nothing about the target language unless the user states otherwise.

## Required references

Read [references/beginner-pedagogy.md](references/beginner-pedagogy.md) before designing or revising the tutorial.

After detecting the target language, read only the relevant section of [references/language-entrypoints.md](references/language-entrypoints.md). Search its headings first; do not load unrelated language sections.

## Workflow

### 1. Establish the reader contract

- Record the target service, target language, known languages, and output path.
- Assume zero knowledge of the target language, runtime, build tool, framework, and standard project layout when the baseline is absent.
- Use a known language only to compare roles. State where the analogy stops.
- Default to a standalone HTML document under `.scratch/` when the user does not choose a format or path.
- When continuing an existing tutorial, edit that artifact as part of every substantive answer. Do not answer in chat only.

### 2. Inspect before teaching

- Read repository guidance files first.
- Identify manifests, toolchain files, run/build/test commands, generated directories, and dependency/vendor directories.
- Find the actual program entrypoint. Do not infer it only from a familiar filename.
- Classify the service as HTTP server, worker, CLI, scheduled job, library, frontend, or a combination.
- Trace one representative vertical flow from external trigger to observable result.
- Build a private evidence map with: concept, actual file and line, producer, consumer, prerequisites, and whether the code is generated.
- Verify every named producer and consumer in the repository. Never invent an “actual” component, handler, type, or call path.

### 3. Separate three kinds of code

Label every code block as one of:

- `actual`: copied faithfully from the repository, with a source path.
- `simplified`: behavior-preserving excerpt with omissions explicitly named.
- `hypothetical`: invented only to teach a concept.

Never present simplified or hypothetical code as the service’s implementation. Prefer actual code, then simplify only after showing what was omitted.

For HTML output, add `data-code-kind="actual|simplified|hypothetical"` to every `pre` element. Add `data-source-path="relative/path"` to actual-code blocks.

### 4. Build the learning ladder

Teach in this order unless the service demands a different prerequisite:

1. What runs the service: language, runtime/compiler, package/build tool.
2. Which files are developer-authored, generated, dependency-owned, or build output.
3. Minimum syntax needed to read the entrypoint.
4. Startup flow from process launch to ready state.
5. One representative request, message, command, or job from input to output.
6. Shared language/framework mechanisms encountered on that path.
7. Domain-specific implementation and advanced internals.

Do not teach step 7 while explaining step 3. When a source block mixes levels, explain only its outer purpose, decode prerequisite syntax, and mark the rest as “later.”

### 5. Write each concept as a closed loop

For each concept:

1. State one plain-language sentence.
2. Say why the service needs it.
3. Show the smallest relevant actual excerpt.
4. Identify the actual producer and consumer.
5. Decode unfamiliar syntax line by line.
6. Show the runtime/control-flow result.
7. Separate `understand now` from `learn later`.

Define a term before using it. If a sentence needs two unexplained terms, split it or add a prerequisite section.

### 6. Design the tutorial artifact

For standalone HTML, copy [assets/tutorial-template.html](assets/tutorial-template.html) and replace all placeholders. Keep it dependency-free and responsive.

Include:

- a first-screen reader contract and one-sentence mental model;
- a developer/generated/dependency file ownership map;
- an entrypoint and startup flow;
- a syntax decoder tied to actual code;
- at least one actual end-to-end service flow;
- visible `understand now / learn later` boundaries;
- source links or paths beside actual examples;
- collapsible advanced details;
- a final flow summary.

Do not lead with repository metrics, dependency lists, or large code blocks. Put the first useful mental model before the first detailed excerpt.

### 7. Incorporate user questions

Treat every “I do not understand” question as tutorial evaluation data.

1. Re-open the exact tutorial section and actual source.
2. Classify the failure: missing prerequisite, unexplained syntax, inaccurate example, mixed abstraction levels, unlabeled simplification, or too much visible detail.
3. Replace the confusing explanation instead of merely appending another paragraph.
4. Move premature detail into a closed `details` block.
5. Answer the user briefly and report the artifact change.

If the question reveals a factual error, correct the tutorial and explicitly identify the correction.

When the current session is also evaluating or developing this skill, promote reusable
feedback into the appropriate bundled reference, validator, or template. Updating only
the current `.scratch` tutorial is not sufficient. Synchronize the installed skill copy,
validate it, and report the global skill path separately from the tutorial artifact path.

### 8. Validate

Run:

```bash
python3 scripts/validate_tutorial.py path/to/tutorial.html --source-root path/to/repo
```

Then apply the human review checklist in `references/beginner-pedagogy.md`.

Verify additionally:

- every actual code path exists;
- every actual producer/consumer relationship is supported by imports, calls, or tree structure;
- no generated or dependency file is presented as developer-authored;
- the first reading path works without opening advanced details;
- the final flow matches the earlier detailed flow.

## Language variants

Use the same teaching workflow for every language. Do not turn the tutorial into a generic language textbook.

- For Go, ground syntax in `main`, one handler/job, explicit error flow, and the service’s real package boundaries.
- For Rust, introduce ownership, borrowing, `Result`, traits, macros, and async only at the first actual line that requires them.
- For TypeScript/React, separate JavaScript syntax, TypeScript-only types, React component behavior, router/build-tool conventions, and generated files.
- For any other language, derive an equivalent entrypoint-to-result path and consult primary official documentation only when the repository cannot establish semantics.

## Handoff

Report:

- the tutorial path;
- target language and representative flow;
- important assumptions;
- validation command and result;
- advanced areas intentionally deferred.

Do not end with a generic offer for more work.
