# Beginner-first teaching rules

## Contents

- Reader model
- Evidence and example integrity
- Explanation unit
- Learning boundaries
- Cross-language analogies
- Revision loop
- Human review checklist

## Reader model

Assume the reader may not know:

- which tool runs or compiles the language;
- the difference between source, generated code, dependencies, and build output;
- object, function, method, type, interface, trait, package, module, pointer, reference, async, or component terminology;
- why a framework API can return data without explicit parameters;
- which syntax exists only for type checking and disappears at runtime.

Never interpret “beginner” as “knows the language but not this repository.” State the assumed baseline near the top of the tutorial.

## Evidence and example integrity

Use these provenance labels consistently:

| Label | Meaning | Rule |
|---|---|---|
| Actual code | Faithful repository excerpt | Link the source and verify every named producer/consumer |
| Simplified code | Real behavior with named omissions | Say what was omitted and never call it exact |
| Hypothetical code | Invented teaching example | Keep it separate from repository claims |

Before writing “component X reads value Y” or “handler A calls service B,” inspect both ends. Verify the import, call, context key, route tree, registration, or constructor wiring that connects them.

Do not choose a plausible consumer by name. A component named `Avatar`, for example, may receive props rather than consume authentication context.

## Explanation unit

Use this sequence for one concept:

1. **Plain sentence:** no new jargon.
2. **Service need:** the concrete problem solved here.
3. **Actual location:** source path and relevant lines.
4. **Mechanism:** producer → binding/key → consumer.
5. **Syntax decoder:** only tokens needed for this excerpt.
6. **Runtime result:** what executes or appears.
7. **Boundary:** what to understand now and what to postpone.

Expose framework “magic” by finding its binding mechanism. Examples:

- React Context: the same context object on provider and consumer sides.
- Dependency injection: registration key/type and resolution point.
- HTTP routing: route registration and matched handler.
- Rust traits: concrete implementation selected at the call site or bound.
- Go interfaces: concrete value assigned and method invoked through the interface.

When describing lookup as “nearest,” “matching,” or “resolved,” always name what must
match. For React, say “the nearest ancestor Provider using the exact same Context
object,” not merely “the nearest Provider.” Different Context providers do not compete.
For key- or type-based injection, state the exact key or type with the same precision.
Check whether the repository actually has repeated matching providers; if it does not,
label nesting examples as hypothetical and say the rule is not currently exercised.

## Learning boundaries

Classify each detail:

- **Now:** required to follow the current flow.
- **Soon:** required for the next flow.
- **Later:** implementation detail, optimization, generated code, or unrelated branch.

When an excerpt combines many concepts, first explain its outer shape. For example, a context value object may contain authentication functions whose internals use callbacks, timers, and SDK tokens. Teach “values and functions are grouped and shared” now; defer callback and token mechanics.

Prefer a short file-reading route such as:

```text
context/key declaration
→ public value assembly
→ provider/registration
→ consumer helper
→ one actual consumer
```

Explicitly name ranges to skip and say when to return.

## Cross-language analogies

Map roles, not syntax:

- “React Context object is like a Vue injection key” is useful.
- “React Provider is the same as a Vue component” is too broad.

Knowing a language or framework does not imply knowing every feature in its ecosystem.
Do not use `provide/inject`, Pinia, Redux, dependency injection, or another specialized
mechanism as the main explanation unless the user has shown familiarity with that
specific mechanism. If familiarity is unknown:

1. teach the target concept in plain language first;
2. keep the analogy optional or collapsed;
3. explain the comparison concept from zero before mapping it;
4. distinguish an exact counterpart from a tool that merely solves a similar problem.

For example, Vue `provide/inject` is the closest built-in counterpart to React Context,
while Pinia shares the goal of distant access to shared state but is a fuller state store.
Do not group both under one “same as Context” label.

For each analogy, state:

1. what role is shared;
2. what behavior differs;
3. which target-language term should be retained.

Stop using the analogy once the target mechanism has a stable mental model.

## Revision loop

When the user remains confused:

- do not blame missing fundamentals;
- identify the first unexplained prerequisite;
- verify the current example against source;
- remove visible advanced detail;
- replace side-by-side walls of code with numbered actual excerpts;
- show the actual consumer, not only the provider;
- update the tutorial in the same turn.

Questions that reveal recurring gaps should change the reusable structure, not just one sentence.

## Human review checklist

- [ ] Can a reader identify what command starts the service?
- [ ] Is the true entrypoint distinguished from a root component/module or generated registry?
- [ ] Are developer, generated, dependency, and build-output files visibly separated?
- [ ] Is every term defined before first use?
- [ ] Does each actual code block link to an existing source file?
- [ ] Are simplified and hypothetical snippets labeled visibly?
- [ ] Is every producer paired with a verified consumer?
- [ ] Does every complex excerpt say what can be skipped for now?
- [ ] Can the main learning path be read without expanding details?
- [ ] Does one representative input reach an observable output?
- [ ] Are type-only constructs distinguished from runtime behavior?
- [ ] Are user corrections incorporated into the artifact rather than chat only?
- [ ] Does the final summary agree with the detailed flow?
