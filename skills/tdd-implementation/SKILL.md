---
name: tdd-implementation
description: Practical test-driven development workflow for code implementation. Use when the user asks for TDD, test-first development, safer bug fixes, or when Codex is implementing core logic, business rules, validation, state transitions, shared utilities, API contracts, security-sensitive code, or behavior with meaningful regression risk. Classify the change first, write or update a failing test before production code when TDD applies, implement the smallest passing change, rerun tests, and report red/green results.
---

# TDD Implementation

## Overview

Use this skill to make code changes with a practical TDD loop. Prefer TDD for behavior that matters, but avoid forcing it onto documentation, copy, styling-only tweaks, simple configuration edits, or exploratory spikes where the behavior is not settled yet.

## Classify The Change

Before editing production code, classify the request:

- **Use TDD** for business rules, calculations, validation, permissions, parsing, persistence, state transitions, API contracts, shared utilities, bug fixes, and regressions.
- **Use focused implementation plus verification** for documentation, comments, copy, formatting, simple configuration, dependency metadata, or styling-only changes.
- **Lean toward TDD when unsure**, especially if the changed code is shared, user-facing, hard to reason about manually, or likely to regress.

If TDD does not fit, state the reason briefly in a progress update or final response and still run the most relevant validation.

## TDD Workflow

1. Inspect nearby code, tests, fixtures, factories, and existing test commands.
2. Define the smallest observable behavior that should change.
3. Add or update the focused test before changing production code.
4. Run the focused test and confirm it fails for the expected reason.
5. If the test passes immediately, tighten the assertion or explain why existing behavior already satisfies the request.
6. Implement the smallest production change needed to pass the failing test.
7. Rerun the focused test and confirm it passes.
8. Run broader relevant tests when the code is shared or the blast radius is unclear.
9. Refactor only after tests are green, then rerun the affected tests.

## Guardrails

- Do not change production code before the failing test when TDD applies, unless the test harness or build is already broken.
- Prefer behavior-focused tests over tests that lock in implementation details.
- Use the repository's existing test style, helpers, naming conventions, and command patterns.
- Keep the red step narrow. One clear failing test is better than a broad test batch with an unclear failure.
- Do not expand into unrelated refactors while red.
- If a failing test cannot be produced, explain the blocker and choose the safest available validation path.

## Bug Fixes

For bug fixes, first write or update a test that reproduces the bug. Confirm the test fails because of the bug, not because of setup, fixtures, or an unrelated error. Then implement the smallest fix and rerun the same test.

## Final Response

Include:

- the classification decision
- the test added or updated
- the initial failing result, if TDD applied
- the final passing result
- any broader tests run
- any tests not run and why
