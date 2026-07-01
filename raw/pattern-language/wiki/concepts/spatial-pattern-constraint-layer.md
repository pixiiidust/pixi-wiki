---
title: Spatial Pattern Constraint Layer
created: 2026-07-01
updated: 2026-07-01
type: concept
status: compiled
namespace: pattern-language
sources:
  - README.md
  - wiki/summaries/for-agents-spatial-pattern-retrieval.md
---

# Spatial Pattern Constraint Layer

A spatial pattern constraint layer turns *A Pattern Language* retrieval into concrete design moves and verification checks for agents.

The goal is not to ask an agent to “make a cozy city.” The goal is to retrieve patterns whose Problem/Solution framing can be converted into constraints the agent must satisfy.

## Formula

```text
intent → selected patterns → constraints → layout moves → verifier checklist
```

## Constraint Types

- **Scale:** region, neighborhood, street, building, room, detail.
- **Adjacency:** what should be near, visible, connected, or separated.
- **Gradient:** public/private, quiet/active, open/enclosed, light/dark.
- **Activity:** what people do there and why the space invites it.
- **Verification:** how to tell whether the design move actually satisfied the pattern.

## Guardrail

This namespace is reference material with non-commercial attribution constraints. It should guide internal/private/non-commercial design experiments and evaluation, not unrestricted training-data packaging.
