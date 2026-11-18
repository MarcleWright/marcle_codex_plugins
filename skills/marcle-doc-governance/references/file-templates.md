# File Templates

Use these templates only when creating missing documents.

Adapt them to the project instead of copying blindly.

All documents created from these templates must be written in `UTF-8`, preferably `UTF-8 without BOM`.

## `doc/README.md`

```md
# Project Documentation

## Product
Defines what the product is, what it does, and what rules it must satisfy.

## Architecture
Defines the technical skeleton, module boundaries, and data model.

## Design
Defines user interaction rules and visible UI behavior.

## Engineering
Defines setup, testing, release, and operational guidance.

## Material
Stores local or temporary user-provided reference material. Material is not stable project truth until reviewed and promoted into the correct owner layer.

## AI
Defines AI workflow, task records, current context, work history, and reviewer conclusion records when independent review is assigned.
```

## `product/PRODUCT_BRIEF.md`

```md
# Product Brief

## Purpose

## Target Users

## Core Value

## Core Workflows

## Non-goals

## Key Domain Concepts
```

## `product/PRODUCT_REQUIREMENTS.md`

```md
# Product Requirements

## Feature: <name>

### Goal

### User Value

### Scope

### Rules

### Acceptance Criteria

### Non-goals
```

## `product/ROADMAP.md`

```md
# Roadmap

## Current Stage

## Near-Term Priorities

## Medium-Term Priorities

## Deferred Areas
```

## `architecture/ARCHITECTURE_OVERVIEW.md`

```md
# Architecture Overview

## System Purpose

## Main Modules

## Responsibility Boundaries

## Data Flow

## Key Technical Decisions
```

## `architecture/DATA_MODEL.md`

```md
# Data Model

## Overview

## Core Entities

## Relationships

## Important Constraints

## Source Of Truth
```

## `design/UI_GUIDE.md`

```md
# UI Guide

## Main Screens Or Workspaces

## Layout Structure

## Key Visible Behaviors

## Important UI States
```

## `design/INTERACTION_RULES.md`

```md
# Interaction Rules

## Selection Behavior

## Create / Edit Flows

## Delete / Destructive Action Rules

## Drag And Drop Rules

## Error / Confirmation Behavior
```

## `engineering/DEV_SETUP.md`

```md
# Development Setup

## Prerequisites

## Install

## Run

## Common Troubleshooting
```

## `engineering/TESTING.md`

```md
# Testing

## Test Types

## Automated Checks

## Manual Verification

## Release Validation
```

## `engineering/KNOWN_ISSUES.md`

```md
# Known Issues

| ID | Area | Severity | Status | Summary | Related Task |
|---|---|---|---|---|---|
```

## `material/README.md`

```md
# Material

This folder stores local or temporary reference material used during project work.

Material here may include user-provided documents, screenshots, sample files, exports, research snippets, or raw notes.

Material is not stable project truth until it has been reviewed and promoted into the correct owner layer:

- `product`
- `architecture`
- `design`
- `engineering`
- `ai`

By default, contents in this folder are local-first and should not be pushed to the remote unless explicitly requested.
```

## `material/.gitignore`

```gitignore
*
!.gitignore
!README.md
!.gitkeep
```

## `ai/AI_CONTEXT.md`

```md
# AI Context

## Current Priorities

## Current Constraints

## Current Important Decisions

## Suggested Read Order
```

Recommended for projects with ongoing handoffs, multiple agents, or longer-running phases.

## `ai/AI_WORKFLOW.md`

```md
# AI Workflow

## Roles

## Task Lifecycle

## Documentation Update Rules

## Review Rules
```

If the project uses planner/coder/reviewer separation, add rules such as:

- Planner defines scope and acceptance criteria in the task file.
- The implementation agent executes only the task scope and does not expand scope unilaterally.
- The implementation agent writes an execution report into the same task file after implementation.
- The implementation agent drafts the task's Context Delta after implementation.
- Deviations from the original plan are recorded explicitly.
- Planner or Reviewer may make a small in-scope correction during review, but must record it with explicit authorship in the same task file.
- Meaningfully out-of-scope follow-up work gets a new task.
- Planner or Reviewer refines the Context Delta and owns long-term context updates.
- Planner or Reviewer explicitly classifies any non-local Follow-up item before the task is finalized.
- When a separate long-loop review record is needed, the agent acting as Reviewer writes it under `ai/task_review/`; the implementation agent should not author the independent reviewer conclusion for its own work.

If role names differ, map responsibilities by behavior rather than by exact label.

## `ai/DEV_LOG.md`

```md
# Dev Log

## Recent

### YYYY-MM-DD Short Phase Title

Status: Done

Summary:

- short outcome or milestone
- short outcome or milestone

Primary task links:

- `ai/tasks/YYYY-MM-DD_nn_example.md`

## Archive
```

Keep `Recent` continuous when the same active work thread spans a month boundary.

This format should stay concise. Use it as a recent-work index with clear handoff value, not as a replacement for task files.

Prefer relative path text for project-internal references. Use absolute paths only for documents outside the project.

## Encoding and review checklist

Before handing off any document created from these templates, verify:

- file encoding is `UTF-8`
- no system-default or locale-derived encoding was used during writes
- no mojibake appears in the rendered file
- no unnecessary smart quotes or special punctuation were introduced
- any existing corruption was repaired with the smallest semantic change possible

## `ai/tasks/<task>.md`

Use the compact template by default. Add the hardened sections below only when the task involves async ordering, concurrency, persistence, transactions, lifecycle, shared scope, optimistic convergence, or another concrete high-risk mechanism.

```md
# Task

## Status

## Task Brief

## Goal

## Evidence And Root Cause

## Change Contract

### Must change

### Must preserve

### Must not do

## Ownership And Invariants

<!-- Omit when the task has no meaningful ownership boundary. -->

## Frozen Decisions

<!-- Keep only decisions that the implementation agent must not reopen. -->

## Failure And Concurrency Semantics

<!-- Hardened tasks only. Omit for ordinary deterministic work. -->

## Forbidden Implementations And Non-Acceptable Substitutes

<!-- Hardened tasks only. Include only task-specific risks. -->

## Acceptance Scenarios

## Validation

Preset:

- `<repository validation preset name>`

Task-specific evidence:

- `<focused risk test>`

Manual or deferred:

- `<manual check, or reason and owner for deferral>`

## Execution Report

- Outcome:
- Actual boundaries/files changed:
- Deviations:
- Automated validation:
- Manual validation:
- Remaining risk:

## Review Result

<!-- Concise conclusion or link to a separate review record. -->

## Context Delta

<!-- Omit when no durable context changed. -->

### Keep

### Changed

### Avoid

### Follow-up

## Links

### Review Records
```

Keep `Task Brief` to 2-5 sentences that summarize the immediate background, intended change, and expected outcome. Put task-specific technical precision in `Evidence And Root Cause`, `Change Contract`, `Ownership And Invariants`, hardened sections when triggered, and `Acceptance Scenarios`.

Validation economy rules:

- Reference repository-maintained presets instead of copying their command lists.
- Add only tests that target this task's concrete risks.
- Do not use source-text assertions or synchronous implementation-shaped mocks as substitutes for real runtime semantics.
- Record manual checks explicitly, including unrun or deferred status; never infer them from automated success.
- Keep shared commit, contributor, documentation, and reporting policy in the owning workflow document unless this task overrides it.

Recommended task filename pattern:

```text
YYYY-MM-DD_nn_short-task-name.md
```

Use `nn` as the sequence number for that day only.

If parallel branches create the same date and daily sequence number, resolve the collision later with a pragmatic rename or suffix rather than switching to a global counter.

For decomposed long tasks, use the parent task's day-local number plus uppercase letters for ordered sub-tasks:

```text
YYYY-MM-DD_16_parent-task.md
YYYY-MM-DD_16A_first-sub-task.md
YYYY-MM-DD_16B_second-sub-task.md
YYYY-MM-DD_16C_third-sub-task.md
YYYY-MM-DD_16_execution-loop.md
YYYY-MM-DD_16A_task-review.md
YYYY-MM-DD_16_execution-loop-review.md
```

## Execution-loop template ownership

The execution template lives in [marcle-goal-excution](../../marcle-goal-excution/references/execution-loop.md). Use it only for a requested long-task workflow/ledger. This governance skill owns placement and links, not execution order, retry policy or commit permissions.

## `ai/task_review/<task-review>.md`

Use this template when an independent Reviewer needs a separate task review record. One file may contain design and implementation rounds; do not create a new file for every retry.

Do not use this file for ordinary self-review by the implementation agent. Put self-review notes in the task file instead.

Recommended filename patterns:

```text
YYYY-MM-DD_nn_task-review.md
YYYY-MM-DD_16A_task-review.md
YYYY-MM-DD_16_execution-loop-review.md
```

```md
# Task Review

## Status

Draft

## Reviewed Item

- Execution loop: `ai/tasks/YYYY-MM-DD_16_execution-loop.md`
- Task: `ai/tasks/YYYY-MM-DD_16A_first-sub-task.md`
- Review kind: `<plan or implementation>`
- Reviewed revision: `<task revision/hash, commit, or base plus explicit working-tree snapshot>`

## Reviewer

- Role: Reviewer
- Agent: `<agent identity if useful>`

## Review Scope

## Validation Evidence

Automated checks:

- `<command and result>`

Manual checks:

- `<check and result, or explicitly not run>`

## Findings

| ID | Priority | Trigger / mechanism / impact | Evidence | Origin | Narrow remedy | Status |
|---|---|---|---|---|---|---|

Origin: plan defect, execution omission/deviation, shared cause, unverified, pre-existing/out-of-scope. Keep IDs stable across rounds.

## In-Scope Corrections

- `<correction applied by Reviewer, or intentionally empty>`

## Follow-up Classification

- Must fix before task close: `<items or none>`
- Separate follow-up task: `<items or none>`
- Keep task-local only: `<items or none>`
- Promote to durable docs: `<AI_CONTEXT.md, decisions/, product/, architecture/, design/, engineering/, or none>`

## Reviewer Conclusion

`Approved | Approved With Follow-ups | Changes Requested | Blocked`

## Planner Disposition (Planner-authored)

- Accept / rebut / defer, finding IDs and evidence-based rationale:
- Remaining acceptance boundaries:

## Subsequent Review Rounds

- Revision, changed findings, verification and current Reviewer conclusion; preserve earlier conclusions.
- Updated Planner disposition in its own section when needed.

## Links

- Reviewed task: `ai/tasks/...md`
- Execution loop: `ai/tasks/...md`
- Related follow-up: `ai/tasks/...md`
```

## `ai/decisions/ADR-0001_<title>.md`

```md
# Decision

## Context

## Decision

## Reason

## Consequences
```
