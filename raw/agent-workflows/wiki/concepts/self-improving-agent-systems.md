---
title: Self-Improving Agent Systems
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-workflows, governance, agent-evolution, evidence]
sources:
  - Knowledge/concepts/self-improving-agent-systems.md
confidence: high
---

# Self-Improving Agent Systems

A **self-improving agent system** improves through verified durable state, not model-weight updates. Each run can make future runs better by distilling evidence into knowledge, skills, routing contracts, project truth, and compact memory pointers.

Short form:

```text
observe → judge → verify → distill → write → consult next run
```

## What evolves

- Agent dossiers: role-specific feedback and review patterns.
- Knowledge concepts: reusable frameworks and distinctions.
- Skills: repeatable procedures, pitfalls, and verification routines.
- Cron/routing prompts: scheduled operating contracts and trigger behavior.
- Project source of truth: GitHub issues, PRs, project hubs, and evidence handles.
- Memory: compact last-mile routing facts only.

## Evidence gate

Durable changes need evidence: Jamie correction, verified regression, repeated pattern, or a single high-impact event. Weak signals should stay as observations.

## Verifier rule

Makers should not grade their own homework. Pixoid verifies worker output before closing issues or treating changes as durable truth.

## Source

Compiled from `Knowledge/concepts/self-improving-agent-systems.md`.
