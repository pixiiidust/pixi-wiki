---
title: Profile Memory Boundaries
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-workflows, memory, governance, source-of-truth]
sources:
  - Knowledge/concepts/profile-memory-boundaries.md
confidence: high
---

# Profile Memory Boundaries

**Profile memory boundaries** define where durable knowledge belongs across Jamie's agent system. The core rule is: save facts to the smallest layer that will help future runs without turning memory into a wiki dump.

## Boundary model

- `USER.md` holds universal person-level operating facts and preferences.
- Profile `MEMORY.md` holds compact profile-specific routing facts and durable environment lessons.
- Local Hermes knowledge holds reusable agent-operational concepts and dossiers.
- Obsidian/GitHub hold project state, strategy, PRDs, issues, and long-form truth.
- Skills hold repeatable procedures and pitfalls.

## Agent workflow rule

Before saving knowledge, classify it. Universal preferences go to user memory. Reusable frameworks go to knowledge pages. Project state goes to project hubs or GitHub. Repeatable procedures go to skills. Temporary task progress, PR numbers, command logs, and issue status do not belong in always-injected memory.

## Cross-namespace links

- `pixi-vault` — source classes and Wiki Compiler Maps depend on this boundary.
- `eval-trace` — context-overfit checks verify agents did not trust the wrong layer.

## Source

Compiled from `Knowledge/concepts/profile-memory-boundaries.md`.
