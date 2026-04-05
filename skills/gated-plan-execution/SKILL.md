---
name: gated-plan-execution
description: Use when implementing work from a markdown plan, checklist, or stepwise task list and the user expects a summary of each completed step plus explicit approval before the next step begins
---

# Gated Plan Execution

## Overview

Execute markdown plans one approved step at a time. After each completed step, report what changed, how it was verified, and ask whether the next step may proceed.

## Execution Loop

1. Read the markdown plan and identify the current step boundary before writing code.
2. Execute only the current approved step.
3. Finish the work needed for that step, including required verification.
4. Check the check box for the finished task.
5. Send a step-completion report.
6. Ask for approval to continue.
7. Stop until the user explicitly approves the next step.

If the plan has checkboxes or numbered items, treat each listed item as a separate gate unless the user clearly redefines the boundaries.

## Step-Completion Report

Every completed step report must include:
- what changed
- what verification ran and what it showed
- whether the planned step is now complete
- any remaining risk, ambiguity, or follow-up inside that step
- a direct approval request for the next step

Use a short, concrete checkpoint report. Do not hide the approval request inside a status paragraph.

## Hard Stop Rules

- Do not start the next plan step before the user replies with explicit approval.
- Do not batch two adjacent plan steps into one implementation burst.
- Do not treat silence, delay, or positive sentiment as approval.
- Do not continue just because the next step looks small or touches the same files.
- Do not drift outside the plan unless the user changes scope.

If the current step is ambiguous, stop and clarify before implementing it.

## Exceptions

Lift the approval gate only when the user explicitly tells you to keep going without waiting between steps.

If unexpected sub-work is required to finish the current approved step, do it only if it is necessary for that step. Include it in the report before asking to continue.

## Red Flags

Stop if you catch yourself thinking:
- "I can finish the next step quickly before reporting"
- "The user probably wants momentum more than checkpoints"
- "This is basically the same step"
- "I'll report both steps together after I'm done"
- "They did not say yes, but they also did not object"

Those are all attempts to bypass the approval gate.
