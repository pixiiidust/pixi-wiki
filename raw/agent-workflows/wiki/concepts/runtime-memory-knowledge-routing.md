---
title: Runtime Memory Knowledge Routing
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-workflows, memory, routing, knowledge-management]
sources:
  - Knowledge/concepts/runtime-memory-knowledge-routing.md
confidence: high
---

# Runtime Memory Knowledge Routing

**Runtime memory knowledge routing** is the live decision rule for combining injected memory, Honcho, local Hermes knowledge, Obsidian Knowledge, skills, GitHub/project truth, and session search while doing work.

## Layer model

- Injected memory and user profile are hints, not proof.
- Honcho provides recalled peer context and synthesis.
- Local Hermes knowledge carries reusable agent-operational concepts.
- Obsidian Knowledge carries human-facing durable concepts and source-backed synthesis.
- Projects and GitHub carry current project truth.
- Skills carry procedures.
- Session search recovers prior conversation context, but is never canonical alone.

## Operating pattern

1. Start with injected memory as routing context.
2. Load relevant knowledge/wiki packs when the task touches a durable domain.
3. Verify live project/runtime state before acting on current facts.
4. Promote durable learning to the narrowest correct layer after the work.
5. Never save raw outputs, issue progress, PR numbers, or command logs to memory.

## Source

Compiled from `Knowledge/concepts/runtime-memory-knowledge-routing.md`.
