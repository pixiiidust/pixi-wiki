---
title: Markdown-First Agent Memory
created: 2026-06-16
updated: 2026-06-16
type: synthesis
status: compiled
namespace: agent-workflows
tags: [agent-workflows, memory, markdown, routing]
sources:
  - Projects/Hermes Mission Control/PRD - Knowledge Pack Routing.md
  - Projects/Hermes Mission Control/Knowledge Pack Contract V1.md
  - Knowledge/concepts/runtime-memory-knowledge-routing.md
  - Knowledge/concepts/profile-memory-boundaries.md
confidence: medium
---

# Markdown-First Agent Memory

Markdown-first agent memory is the rule that durable operational knowledge should live in source-controlled notes, packs, issues, and skills before it becomes infrastructure.

The memory layer should help the agent route itself. It should not become a hidden second database of project truth.

## Layer model

- **Injected memory:** compact stable hints, preferences, and environment facts.
- **Knowledge / wiki pages:** durable concepts and synthesis.
- **Project notes:** concrete project state and decisions.
- **GitHub issues:** execution truth and active coordination.
- **Skills:** reusable procedures.
- **Live tools:** current system state and verification.

Markdown-first means the agent can inspect and cite the source. When the source is too volatile, the agent should use live tools instead of freezing it into memory.

## Why this matters

Hidden memory is convenient but hard to audit. Markdown and issues are slower but visible, reviewable, and versioned. For Jamie's crew, that makes them better default truth surfaces.

## Failure mode

The danger is treating written context as commandment. Packs and notes are routing aids. They must be overridden by current GitHub state, live filesystem state, tests, and Jamie's latest instruction.

## Related pages

- [[../concepts/knowledge-pack-routing|Knowledge Pack Routing]]
- [[../concepts/agent-entrypoint-mesh|Agent Entrypoint Mesh]]
- [[../concepts/profile-memory-boundaries|Profile Memory Boundaries]]
- [[../concepts/runtime-memory-knowledge-routing|Runtime Memory Knowledge Routing]]
