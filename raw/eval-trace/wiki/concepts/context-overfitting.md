---
title: Context Overfitting
created: 2026-06-16
updated: 2026-06-16
type: concept
status: pilot
namespace: eval-trace
tags: [eval-trace, agent-workflows, reliability, context-management]
sources:
  - Knowledge/concepts/context-overfitting.md
confidence: medium
---

# Context Overfitting

**Context overfitting** is an agent workflow failure mode where the agent optimizes for the immediate conversation, handoff, or prompt context instead of the durable source of truth. Its primary namespace is `eval-trace` because it is best treated as a quality/evaluation failure mode.

## Why it matters

Context overfitting can make an agent:

- follow stale chat summaries over live repo or issue state;
- treat scratch notes as canonical truth;
- continue an old plan after the latest user message changed direction;
- duplicate work because it did not inspect current files or tracker state.

## Evaluation read-out

A workflow is healthier when agents verify current truth before acting:

- live GitHub issue/PR state for coordination;
- current git status and diffs for repo work;
- canonical `Knowledge/`, `Projects/`, and Wiki Compiler Map files for vault work;
- scratch Daily Notes only as context hints.

## Cross-namespace links

- `agent-workflows` — context overfitting affects route execution in [[../../../agent-workflows/wiki/entities/hermes-mission-control|Hermes Mission Control]].
- `pixi-vault` — source classes and compiler routing reduce context-overfit risk.

## Source

Compiled from `Knowledge/concepts/context-overfitting.md`.
