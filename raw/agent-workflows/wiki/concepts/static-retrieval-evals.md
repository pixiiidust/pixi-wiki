---
title: Static Retrieval Evals
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-workflows, evals, retrieval, quality-gates]
sources:
  - Projects/Hermes Mission Control/KPR Static Retrieval Eval - 2026-06-15.md
  - Projects/Hermes Mission Control/kpr-v1-validation-report.md
  - Projects/Hermes Mission Control/PRD - Knowledge Pack Routing V2.md
confidence: medium
---

# Static Retrieval Evals

**Static retrieval evals** are small question sets that test whether the current markdown/wiki routing surface answers important agent questions before heavier retrieval infrastructure is justified.

They are a build/no-build gate.

## What they test

A good static retrieval eval asks questions that reveal routing failures:

- Does the agent find the active repo or project?
- Does it distinguish canonical source truth from derived output?
- Does it understand what the pack does not cover?
- Does it preserve provenance and source boundaries?
- Does it avoid leaking secrets or relying on scratch notes?
- Does it know when to escalate to live tools or GitHub?

## Gate behavior

If the static eval passes, do not build search/RAG/MCP just because it feels sophisticated. Improve the markdown route only when the eval exposes a concrete failure.

If the eval fails, fix the cheapest layer first: source wording, index coverage, scope boundaries, crosslinks, or freshness metadata. Only then consider infrastructure.

## Related pages

- [[knowledge-pack-routing]]
- [[agent-entrypoint-mesh]]
- [Context Overfitting](../../../eval-trace/wiki/concepts/context-overfitting.md)
