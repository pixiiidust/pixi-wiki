---
title: Critical Ranger FFM
created: 2026-06-16
updated: 2026-06-16
type: entity
status: compiled
namespace: rl-sim-labs
tags: [rl-sim-labs, reinforcement-learning, pufferlib, zone-control, simulation]
sources:
  - Projects/Critical Ranger FFM/Index.md
confidence: high
---

# Critical Ranger FFM

**Critical Ranger FFM** is the first concrete project under the `rl-sim-labs` namespace. It is a toy forest-fire / PufferLib reinforcement-learning experiment focused on zone-control policies, not a standalone namespace yet.

## Current role in this namespace

Critical Ranger is the seed RL simulation lab:

- environment: forest-fire simulation with self-organized dynamics;
- action model: no-op or thin one selected zone at a decision tick;
- evaluation target: reduce mega-fire frequency versus honest simple baselines;
- constraints: preserve acceptable tree density and stay within intervention budget;
- evidence posture: metrics and anti-cheat gates decide belief, not training reward alone.

## Active roadmap

The active path is the **Zone-Control RL MVP**. The prior switch-point / single-cell efficacy path is parked as diagnostic infrastructure.

Current next implementation gate from the source note:

```text
#54 — zone-control action contract fixtures
```

That slice is intentionally narrow: deterministic zone indexing, no-op action, one-zone thinning contract, decision interval semantics, and CPU-safe fixture tests.

## Promotion boundary

Do not promote Critical Ranger to its own namespace yet. It should remain an entity/project inside `rl-sim-labs` until it has an independent audience, raw experiment corpus, recurring reports, multiple durable document types, and a clear covers/not-covered boundary.

## Source

Compiled from `Projects/Critical Ranger FFM/Index.md`.
