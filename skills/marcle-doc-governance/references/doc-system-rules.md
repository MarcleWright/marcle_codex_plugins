# Doc System Rules

These reference rules govern document ownership and maintenance. Execution scheduling and authorization belong to the user and the active workflow, not this document.

This is a generic specification.

It is intentionally not specialized for any single repository, stack, product type, or workflow.

## 1. Objective

Create and maintain a structured `doc/` system for the current project.

The documentation system must:

- support human readers and AI agents
- separate stable truth from temporary execution records
- avoid mixed catch-all documents
- remain maintainable over time
- support project continuity across sessions or contributors

## 2. Core Principle

`doc/` is not a passive file dump.

It is an active project knowledge system.

Every document must have a clear responsibility boundary.

## 3. Default Top-Level Structure

Unless the project already has a strong established convention, prefer this structure under `doc/`:

```text
doc/
  README.md

  product/
  architecture/
  design/
  engineering/
  material/
  ai/
```

These six areas are the default system backbone.

If the project already uses an established equivalent such as `docs/`, preserve that convention unless there is a strong reason to change it.

Sub-files and subfolders may be created as needed, but must respect the ownership rules in this document.

## 4. Top-Level Ownership Rules

### 4.1 `product`

Purpose:

- define what the product is
- define who it is for
- define what problems it solves
- define feature scope and business rules

Belongs here:

- product purpose
- target users
- feature definitions
- business constraints
- acceptance-oriented product rules
- roadmap priorities
- non-goals

Does not belong here:

- implementation details
- code structure
- technical module boundaries
- low-level UI rendering details
- setup, packaging, or release procedures
- task logs

### 4.2 `architecture`

Purpose:

- define how the system is structured technically
- define module and service boundaries
- define data flow and ownership
- define interface and integration boundaries

Belongs here:

- architecture overview
- module responsibilities
- data model
- system boundaries
- internal or external interface boundaries
- major structural decisions

Does not belong here:

- step-by-step contributor instructions
- temporary task execution notes
- product scope prose
- long-form release operation records

### 4.3 `design`

Purpose:

- define how the product behaves for users
- define interaction behavior and UI rules

Belongs here:

- UI structure
- user flows
- interaction rules
- component behavior
- visible states
- modal/menu/inline decisions

Does not belong here:

- business scope definitions already owned by product
- code/module explanations already owned by architecture
- release and setup instructions

### 4.4 `engineering`

Purpose:

- define how the project is developed, tested, packaged, released, and operated

Belongs here:

- setup instructions
- testing instructions
- contributor workflow instructions
- release instructions
- packaging instructions
- known issues
- troubleshooting guidance

Does not belong here:

- product definition
- architecture as primary system truth
- task history
- temporary planning records

### 4.5 `ai`

Purpose:

- define how AI agents collaborate on the project
- store AI-oriented execution records
- preserve current working context and durable work decisions

Belongs here:

- AI workflow rules
- AI current context
- task records
- decision records
- log indexes and archives

Does not belong here:

- stable product truth
- full architecture substitute
- general engineering instructions

### 4.6 `material`

Purpose:

- store user-provided or local reference inputs used during work
- keep temporary source material separate from stable project truth
- provide a safe place for screenshots, pasted briefs, sample files, research notes, and other reference-only artifacts

Belongs here:

- user-supplied reference documents
- screenshots, exports, samples, and input artifacts
- temporary research snippets
- local-only notes that inform a task but should not become durable project truth as-is
- source material waiting to be summarized or promoted into an owner layer

Does not belong here:

- stable product requirements
- architecture decisions
- design rules
- engineering workflow rules
- AI task history, execution ledgers, or durable handoff context

Version-control guidance:

- `doc/material/` contents are local-first and usually should not be pushed to the remote
- when bootstrapping `doc/material/`, prefer adding a local `.gitignore` that ignores contents while allowing an optional `README.md` or `.gitkeep`
- if specific reference material must be shared, promote the stable conclusion to the correct owner layer, or explicitly track that individual file by user request
- do not treat unreviewed material as project truth

## 5. Recommended Initial Files

The agent should create a minimal but usable initial set.

Recommended default files:

```text
doc/
  README.md

  product/
    PRODUCT_BRIEF.md
    PRODUCT_REQUIREMENTS.md
    ROADMAP.md

  architecture/
    ARCHITECTURE_OVERVIEW.md
    DATA_MODEL.md

  design/
    UI_GUIDE.md
    INTERACTION_RULES.md

  engineering/
    DEV_SETUP.md
    TESTING.md
    KNOWN_ISSUES.md

  material/
    README.md
    .gitignore

  ai/
    AI_CONTEXT.md
    AI_WORKFLOW.md
    DEV_LOG.md
    tasks/
    task_review/
    decisions/
    logs/
```

Additional files may be added only when the project actually needs them.

Do not create large empty trees without a concrete purpose.

## 6. File Responsibility Guidance

### 6.1 `README.md`

Role:

- entry point into the documentation system
- explain where different kinds of knowledge live

### 6.2 `PRODUCT_BRIEF.md`

Role:

- stable product identity

Typical contents:

- purpose
- target users
- core value
- core workflows
- non-goals

### 6.3 `PRODUCT_REQUIREMENTS.md`

Role:

- stable feature and business rule contract

Typical per-feature contents:

- goal
- user value
- scope
- rules
- acceptance criteria
- non-goals

### 6.4 `ROADMAP.md`

Role:

- priorities and future direction

### 6.5 `ARCHITECTURE_OVERVIEW.md`

Role:

- explain the project's technical skeleton

Typical contents:

- system purpose
- main modules
- responsibilities
- data flow
- key boundaries

### 6.6 `DATA_MODEL.md`

Role:

- explain core entities, relationships, and important constraints

### 6.7 `UI_GUIDE.md`

Role:

- explain visible UI structure and user-facing behavior

### 6.8 `INTERACTION_RULES.md`

Role:

- explain interaction-level decisions and behavior rules

### 6.9 `DEV_SETUP.md`

Role:

- explain how to run and develop the project

### 6.10 `TESTING.md`

Role:

- explain how to validate changes

### 6.11 `KNOWN_ISSUES.md`

Role:

- track known problems in a structured way

### 6.12 `material/README.md`

Role:

- explain that `doc/material/` is for local or temporary reference inputs
- warn that material contents are not stable project truth
- explain when to promote conclusions into owner-layer documents
- document the default local-first version-control policy

### 6.13 `material/.gitignore`

Role:

- keep reference material local by default
- allow a small README or placeholder to be tracked if the project wants the folder structure in git

Typical contents:

```gitignore
*
!.gitignore
!README.md
!.gitkeep
```

### 6.14 `AI_CONTEXT.md`

Role:

- short current working context for incoming AI agents

### 6.15 `AI_WORKFLOW.md`

Role:

- explain how AI agents should work on this project

### 6.16 `DEV_LOG.md`

Role:

- concise recent work index

### 6.17 `tasks/`

Role:

- one file per task with full execution detail

### 6.18 `task_review/`

Role:

- store reviewer conclusion records for long-task execution loops
- preserve review findings, validation results, and follow-up classification without turning task files or execution-loop files into long review transcripts
- make independent review ownership explicit

Writer:

- the agent acting as `Reviewer` writes the review conclusion record
- if there is no independent reviewer, keep ordinary self-review notes in the task file instead of creating a separate `task_review` record
- `Planner` may write the record only when explicitly acting as the reviewer for that review pass
- the implementation agent should not author the final independent review conclusion for its own work

### 6.19 `decisions/`

Role:

- durable work decisions that should remain visible over time

### 6.20 `logs/`

Role:

- archived time-based summaries

## 7. Maintenance Rules

### 7.1 One Primary Home Per Fact

Each important fact should have one primary owner document.

Other documents may reference it, but should not fully duplicate it.

### 7.2 No Catch-All Spec Documents

Do not create or keep expanding a single mixed document that combines:

- product definition
- architecture explanation
- design rules
- engineering operations
- task history

If such a document exists, gradually split it by ownership.

### 7.3 Stable Truth vs Execution History

Stable truth belongs in:

- `product`
- `architecture`
- `design`
- `engineering`

Execution history belongs in:

- `ai/tasks`
- `ai/task_review`
- `ai/logs`
- `ai/DEV_LOG.md`

Reference inputs belong in:

- `material`

Material may inform stable truth, but it is not stable truth until reviewed and promoted into the correct owner layer.

### 7.4 Smallest Necessary Cross-Layer Updates

When one change affects multiple layers:

- update the primary owner layer first
- update only necessary downstream implications elsewhere

Do not duplicate the same full explanation across multiple documents.

### 7.5 Legacy Mixed Documents

If the project already contains mixed legacy docs:

- treat them as source material
- extract content into proper owner documents
- reduce the old file into an index, stub, or deprecation note after replacement exists

Do not keep using the mixed file as the long-term main source.

## 8. Change Routing Rules

When deciding which docs to update, use this logic.

### 8.1 Product Capability Or Business Rule Change

Update:

- `product`

Update `design` only if user behavior changes.

Update `architecture` only if technical boundaries change.

### 8.2 Interaction Or UI Behavior Change

Update:

- `design`

Update `product` only if user-visible behavior changes the product rule or acceptance criteria.

### 8.3 Technical Structure Or Boundary Change

Update:

- `architecture`

Update `engineering` only if contributor workflow or operational steps also change.

### 8.4 Development / Testing / Packaging / Release Change

Update:

- `engineering`

Update `architecture` only if the underlying structural design also changed.

### 8.5 AI Collaboration Or Task-Tracking Change

Update:

- `ai`

### 8.6 User-Provided Or Temporary Reference Material

Store:

- `material`

Promote only reviewed conclusions to:

- `product`
- `architecture`
- `design`
- `engineering`
- `ai`

Do not copy raw reference dumps into stable owner-layer documents.

## 9. `AI_CONTEXT.md` Rules

`AI_CONTEXT.md` is strongly recommended for projects with ongoing multi-step work, multiple agents, or recurring handoffs.

For very small or short-lived projects, it may be omitted if there is no real need for current-phase memory compression.

It is not a replacement for architecture docs.

It is not a long history file.

Its job is to provide current, compressed working context.

It should contain only:

- current priorities
- current constraints
- currently important decisions still affecting work
- suggested read order if useful

It should be updated by:

- removing no-longer-relevant context
- adding newly relevant current-phase context

It is expected to change significantly over time.

## 10. `DEV_LOG.md` And Task History Rules

Relationship:

- `DEV_LOG.md` = short recent work index
- `tasks/` = one full record per task
- `task_review/` = separate reviewer conclusion records when independent review is part of the workflow
- `logs/` = archived summaries

Rule:

- long detail goes into task files
- concise summary goes into logs

Do not copy full task reports into the main dev log.

Recommended `DEV_LOG.md` entry style:

- prefer one entry per meaningful work thread, milestone, or completed phase
- use a short heading such as `### YYYY-MM-DD Short Phase Title`
- include `Status:`
- include a short `Summary:` section with only the most important bullets
- include task links such as `Primary task links:` or `Links:`

This richer block format is allowed when it improves handoff clarity, but it must still behave like an index rather than a second full task report.

Practical limits:

- prefer roughly 2 to 6 summary bullets
- link to task files for execution detail instead of repeating the whole implementation story
- keep only current or high-value recent entries in `DEV_LOG.md`; move older detail into `logs/`

Reference-path rule for `DEV_LOG.md`:

- for files and documents inside the project, prefer relative path text such as `ai/tasks/2026-06-04_01_example.md`
- use absolute paths only when the referenced document is outside the project boundary
- keep log references lightweight and readable rather than using environment-specific project-internal absolute paths by default

Monthly archives are recommended, but they must not break active continuity unnecessarily.

If work at the end of one month and the start of the next month is clearly part of the same active thread, `DEV_LOG.md` should keep a concise continuous summary for that thread even if some detailed entries have already moved into `logs/YYYY-MM.md`.

Treat monthly archives as historical organization, not as a hard boundary for ongoing context.

## 10.1 Implementation Task Specification Rules

An implementation task is an executable contract, not a transcript or a generic checklist. Keep it short where shared project rules already apply, but make task-specific technical boundaries mechanically testable.

### Compact task by default

An ordinary implementation task should normally contain only:

- goal and current evidence
- change contract: must change, must preserve, and must not do
- ownership or source-of-truth rule when relevant
- acceptance scenarios
- validation preset names, task-specific evidence, and manual checks or deferrals
- a short execution report and review result after implementation
- `Context Delta` only when durable context changed

Do not copy full repository test commands, standard contributor rules, commit policy, documentation policy, or report boilerplate into every task. Link to the owning engineering or AI workflow document and state only task-specific overrides.

### Hardened specification trigger

Add hardened technical sections when correctness depends on one or more of:

- asynchronous ordering or retry
- concurrent or competing writers
- transactions, revisions, idempotency, or persistence
- framework scheduling, lifecycle, mount/unmount, or disposal
- shared caches or cross-project/profile/tenant scope
- optimistic state and canonical convergence
- destructive behavior or recovery after partial failure

For these tasks, freeze only the relevant items:

1. **Ownership and invariants**: name the source of truth, allowed writers, and conditions that must remain true during success, failure, retry, cancellation, and disposal.
2. **Execution boundary**: name the modules or paths the task may change, what must remain owned by existing infrastructure, and which legacy/general paths may not be reused.
3. **Frozen decisions**: record decisions already made so the implementation agent does not silently choose a different architecture.
4. **Forbidden implementations and non-acceptable substitutes**: prohibit known forms of superficial compliance when they would violate semantics. State the mechanism, not merely a preferred code shape.
5. **Failure and concurrency matrix**: distinguish only the outcomes relevant to the task, such as success, definitive rejection, uncertain transport result, conflict, cancellation, disposal, and stale completion. Define visible state, retained local data, persistence behavior, and retry behavior for each.
6. **Identity and scope checks**: enumerate fields that must match when correctness depends on confirming an intended resource. Do not use vague wording such as "verify the correct target" when exact identity is available.
7. **Evidence requirements**: require tests at the layer where the risk exists. A synchronous mock does not prove real framework scheduling; a source-text assertion does not prove runtime behavior; unit tests do not replace an explicitly required desktop/manual interaction check.

Do not universalize one historical bug. Add a prohibition or adversarial scenario only when the current task has evidence of that risk or the mechanism is inherently fragile.

### Acceptance and validation economy

Write acceptance criteria as observable scenarios and invariants, not as a restatement of the implementation plan. Each identified high-risk mechanism should have at least one corresponding piece of evidence.

Use three validation buckets:

- **Preset**: names of repository-maintained validation groups; their command definitions belong in the project testing documentation or scripts.
- **Task-specific**: focused tests for the risks introduced or repaired by this task.
- **Manual or deferred**: user-visible checks that automation does not cover, including owner and reason when deferred.

Passing a preset proves only that the preset ran successfully. The task and execution report must not claim unrun manual behavior or use an implementation-shaped mock as proof of the real runtime contract.

## 10.2 Encoding and character rules

All documentation files must be written in `UTF-8`, preferably `UTF-8 without BOM`.

This applies to:

- `.md`
- `.txt`
- `.json`
- `.yml`
- `.yaml`
- all generated task documents
- all execution documents
- all review documents
- all `DEV_LOG.md` documents
- all `AI_CONTEXT.md` documents

Do not rely on:

- system default encoding
- ANSI
- GBK
- GB2312
- editor default save encoding

On Windows, any script or command that writes files must explicitly specify `UTF-8`.

Recommended write patterns:

- PowerShell file writes should pass an explicit UTF-8 encoding
- Python file writes should use `encoding="utf-8"`
- JSON/YAML emitters should be configured to write UTF-8 rather than inheriting the host locale

Character policy:

- allow Chinese content normally when the project needs it
- prefer ASCII punctuation by default
- prefer plain `" "` and `' '` for quotes
- avoid smart quotes such as `“ ”` and `‘ ’`
- avoid unnecessary special Unicode punctuation unless it has a clear purpose

If you see mojibake or encoding corruption such as `鈥`, `锟`, or `�`, treat it as a document quality defect and fix it.

When repairing existing documents with encoding damage, make the smallest semantic change that removes the corruption. Do not rewrite the whole document just to refresh encoding unless that is actually necessary.

## 11. Context Delta Rule

Task files should include a `Context Delta` section when the task produces durable lessons, future follow-up items, or changes to project rules, structure, ownership, or workflow.

Purpose:

- capture what the task changed in the project's long-term working memory
- compress durable lessons without copying the whole execution log

`Context Delta` is not:

- a full task summary
- a command transcript
- a replacement for the execution report

It should capture only information that may matter to future tasks.

If a task is very small and produces no durable memory change, the section may be omitted.

Useful categories include:

- `Keep` = durable facts worth remembering
- `Changed` = structure, responsibility, or rule changes
- `Avoid` = incorrect paths or rejected directions to avoid repeating
- `Follow-up` = future work that remains open

Authorship guidance:

- if the project uses separate planner/coder/reviewer roles, the agent that actually performed the implementation work should draft the `Context Delta` inside the task file because that agent knows the concrete execution findings best
- `Planner` or `Reviewer` should then refine it and decide what, if anything, should be promoted into longer-lived documents
- do not require `Planner` alone to write all `Context Delta` content when `Planner` did not directly perform the implementation work
- do not let the implementation agent alone decide all long-term memory promotion when broader project context is needed

Promotion guidance:

- if it affects current active work repeatedly, it may be promoted into `AI_CONTEXT.md`
- if it is a durable principle or important decision, it may be promoted into `decisions/`
- if it is a bug or persistent risk, it may be promoted into `KNOWN_ISSUES.md`
- if it is only relevant to this one task, keep it inside the task file only

Follow-up handling rule:

- if `Context Delta -> Follow-up` contains an item that is expected to matter beyond this single finished task, `Planner` or `Reviewer` must explicitly decide whether it should be promoted into `AI_CONTEXT.md`, `decisions/`, `KNOWN_ISSUES.md`, or `ROADMAP.md`
- such items must not be left silently buried only inside the closed task file
- if an item is intentionally kept task-local, the reviewer should record that decision briefly

## 12. Decision Record Rules

Use `decisions/` for durable decisions that should remain visible over time.

Typical examples:

- important workflow rules
- scope boundary decisions
- architecture decisions
- important rejected approaches

Recommended format:

- context
- decision
- reason
- consequences

## 13. AI Workflow Rules

If the project uses multiple agent roles, document them in `AI_WORKFLOW.md`.

Examples may include:

- planner
- coder
- reviewer

But these roles are optional.

Do not assume every project uses the same AI collaboration model.

The agent should only define role-specific rules when they actually apply to the project.

Role recognition should be based primarily on behavior, not only on labels.

Examples:

- an agent acting mainly through implementation, debugging, validation, and direct code changes is functionally acting as the coding/implementation role
- an agent acting mainly through task planning, decomposition, orchestration, review coordination, and long-horizon documentation maintenance is functionally acting as the planning role
- an agent acting mainly through review, scope control, result validation, and follow-up classification is functionally acting as the review role

Role labels and aliases may help, but behavior should take precedence when deciding which responsibilities apply.

If the project explicitly uses a `planner / coder / reviewer` workflow, add and maintain role-specific rules such as:

- `Planner` defines the task file, scope boundary, and acceptance criteria
- the implementation agent executes only the task scope defined in the task file and does not expand scope without approval
- after implementation, the implementation agent updates the same task file with an execution report
- after implementation, the implementation agent drafts the task's `Context Delta`
- any deviation from the original task plan is recorded explicitly
- `Planner` or `Reviewer` may apply a small in-scope correction during review when it is faster or clearer to do so directly
- such planner/reviewer corrections must be recorded explicitly in the same task file with clear authorship
- if the follow-up change is meaningfully out of scope, create a new task instead of silently extending the old one
- `Planner` or `Reviewer` refines the `Context Delta` if needed
- `Planner` or `Reviewer` decides whether any `Context Delta` should be promoted into `AI_CONTEXT.md`, `decisions/`, or other long-term documents
- before closing the task, `Planner` or `Reviewer` explicitly classifies any non-local `Follow-up` item so it does not remain only in the task file by accident
- `Reviewer` or `Planner` decides whether durable conclusions should update `AI_CONTEXT.md` or `decisions/`

General rule regardless of role naming:

- any agent that materially contributes implementation, correction, or validation work to a task should record the relevant result back into the same task file with clear authorship

Review record rule:

- a separate `doc/ai/task_review/` record is for an agent acting as `Reviewer` to record review conclusions for a long-task execution loop or a loop sub-task
- the reviewer record should contain findings, validation status, scope judgment, required fixes, follow-up classification, and the final review conclusion
- the implementation agent may link to a reviewer record after it exists, but should not write the independent reviewer conclusion for its own implementation
- if the same agent only performs self-review before closing its own task, record that in the task file and execution ledger instead of creating a separate reviewer conclusion record

## 13.1 Execution Records: Location, Not Scheduling

Long-task orchestration, plan-review gates, retry escalation and the execution-loop template belong to [marcle-goal-excution](../../marcle-goal-excution/SKILL.md). This document does not start that workflow or grant commit/push authority.

When the user requests the execution workflow or an execution ledger, store its control record under `doc/ai/tasks/YYYY-MM-DD_nn_execution-loop.md` (or the project's established equivalent). Link parent, active tasks and reviews; do not duplicate the complete procedure in every task. Ordinary documentation maintenance does not create a loop. Existing historical names and layouts may be preserved.

## 13.2 Task Review Records

Use `doc/ai/task_review/` when an independent task review needs its own record. This is also useful for long-task sub-stages; it does not itself enable a loop.

Default location:

```text
doc/ai/task_review/
```

Recommended filename patterns:

```text
YYYY-MM-DD_nn_task-review.md
YYYY-MM-DD_16A_task-review.md
YYYY-MM-DD_16_execution-loop-review.md
```

Use the parent or sub-task identifier when the review maps to a numbered long-task decomposition.

Responsible writer:

- the agent acting as `Reviewer` owns the reviewer conclusion record
- `Planner` may own it only when explicitly acting as reviewer
- the implementation agent should update the task execution report and fix in-scope findings, but should not author the independent reviewer conclusion for its own work

Required contents:

- reviewed execution-loop document or task link
- reviewer identity or role
- review scope
- validation evidence
- findings by severity or priority
- required fixes and whether they are in-scope
- follow-up classification for out-of-scope items
- final conclusion such as `Approved`, `Approved With Follow-ups`, `Changes Requested`, or `Blocked`

Record review kind (plan/implementation) and the reviewed revision. A task revision/hash identifies a plan; a commit or base plus explicit change snapshot identifies implementation. Preserve stable finding IDs across rounds. Necessary P1/P2 findings state trigger, mechanism, impact, evidence, narrow remedy and origin: plan defect, execution omission/deviation, shared cause, unverified, or pre-existing/out-of-scope. Unknown origin is allowed.

Keep Reviewer-authored conclusions distinct from a Planner-authored disposition section. Planner may accept, rebut with evidence, or defer findings; record the rationale without rewriting Reviewer approval. A material revision must not inherit an old approval silently. Counting retry rounds and deciding escalation are the execution workflow's responsibility. One review file can hold both kinds and append compact round deltas with a clear current result.

Review records are AI workflow records. They are not stable product, architecture, design, or engineering truth by themselves. Promote durable conclusions to the correct owner layer only after review.

## 14. Naming Guidance

Use clear, stable, descriptive file names.

Avoid names such as:

- `temp`
- `misc`
- `notes2`
- `final_final`
- `project_spec` as a catch-all

For task files, recommended pattern:

```text
YYYY-MM-DD_nn_short-task-name.md
```

Where:

- `YYYY-MM-DD` is the task date
- `nn` is the sequence number for that day only

Use day-local numbering such as:

```text
2026-06-04_01_fix-import-flow.md
2026-06-04_02_update-task-log-rules.md
```

Do not use one global continuous task counter across the whole project.

If parallel branches independently create the same day-local number, resolve the collision pragmatically when histories meet. Prefer renaming the less-established task record or adding a short suffix rather than introducing a global counter system.

For decomposed long tasks, use the parent task's day-local number plus uppercase letters for ordered sub-tasks:

```text
YYYY-MM-DD_16_parent-task.md
YYYY-MM-DD_16A_first-sub-task.md
YYYY-MM-DD_16B_second-sub-task.md
YYYY-MM-DD_16C_third-sub-task.md
```

Rules:

- the parent task keeps the numeric id, such as `16`
- child tasks append uppercase letters without an extra separator, such as `16A`, `16B`, `16C`
- preserve alphabetical order as execution order unless the execution-loop document explicitly says otherwise
- do not rename unrelated day-local tasks just to make room for child letters
- if a decomposition grows beyond `Z`, prefer creating a new parent task or a second-phase parent rather than inventing ambiguous suffixes
- execution-loop documents that control a decomposed parent should use the parent id, for example `YYYY-MM-DD_16_execution-loop.md`
- reviewer conclusion records for a sub-task should usually use the reviewed child id, for example `YYYY-MM-DD_16A_task-review.md`
- reviewer conclusion records for the whole loop should usually use the parent id, for example `YYYY-MM-DD_16_execution-loop-review.md`

For decision files, recommended pattern:

```text
ADR-0001_short-title.md
```

## 15. Optional Metadata

If useful, the agent may add lightweight front matter such as:

```md
---
title: Product Brief
status: active
owner: product
last_updated: YYYY-MM-DD
---
```

Use metadata only if it will actually be maintained.

Do not add noisy metadata by default.

## 16. Bootstrap Procedure

When initializing or standardizing docs for a project, the agent should:

1. inspect current docs
2. identify mixed, duplicated, or missing documentation areas
3. create the top-level `doc/` structure if missing
4. create the recommended initial files if missing
5. route existing content into the correct owner layers
6. reduce mixed legacy documents after replacements exist
7. establish AI workflow and task-record structure
8. add `doc/material/` with local-first ignore rules when user-provided reference material is expected
9. keep the system small and useful rather than over-expanding it

## 17. Quality Checklist

Before finishing documentation work, verify:

1. Every active document has a clear owner layer.
2. No new catch-all spec was introduced.
3. Stable truth and execution history remain separated.
4. `AI_CONTEXT.md` is short and current.
5. `DEV_LOG.md` remains concise.
6. New or modified documents were checked for mojibake or encoding corruption.
7. Document writes used explicit UTF-8 where files were created or rewritten.
8. `Context Delta` is used only for durable memory changes, not general summaries.
9. Durable decisions are not buried only in task files.
10. Separate reviewer conclusion records, when used, live under `ai/task_review/` and are written by the agent acting as `Reviewer`.
11. Raw or temporary reference material stays in `material` and is not mistaken for stable truth.
12. The structure is not more detailed than the project currently needs.

## 18. Execution Instruction

If asked to initialize, normalize, or maintain a project documentation system, the agent should:

- use this specification directly
- create the minimum useful structure
- maintain ownership boundaries
- keep docs readable for later AI agents
- prefer gradual cleanup over disruptive rewrites unless instructed otherwise
