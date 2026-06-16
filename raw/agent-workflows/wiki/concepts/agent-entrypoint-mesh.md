---
title: Agent Entrypoint Mesh
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-workflows, entrypoints, routing, llms-txt]
sources:
  - Projects/Hermes Mission Control/kpr-pixoid-routing-rule.md
  - Projects/Hermes Mission Control/Knowledge Pack Contract V1.md
  - Projects/Hermes Mission Control/PRD - Knowledge Pack Routing V2.md
confidence: medium
---

# Agent Entrypoint Mesh

An **agent entrypoint mesh** is a set of small, typed starting points that route an agent to the right truth surface for the job.

The point is not to make one universal file. The point is to make the first hop cheap, explicit, and hard to confuse.

## Mesh shape

A healthy mesh usually has:

- a root agent registry such as `llms.txt`;
- namespace or domain-level packs;
- project/entity packs for concrete work;
- machine registry metadata such as `index.json`;
- raw provenance mirrors for source inspection;
- issue tracker links for execution truth.

## Why mesh beats dump

A raw dump asks the model to infer structure from volume. A mesh gives it structure first: scope, not-covered boundaries, source paths, freshness, and fallback behavior.

## Pixoid rule

Pixoid should treat entrypoints as routing contracts, not as replacement truth. If a pack points to a GitHub issue, PRD, or source note, the agent verifies the live source before claiming current state.

## Related pages

- [[knowledge-pack-routing]]
- [[static-retrieval-evals]]
- [[runtime-memory-knowledge-routing]]
