---
title: Petri Eden Project
created: 2026-07-24
updated: 2026-07-24
type: entity
status: active
namespace: petri-eden
sources:
  - Petri Eden project context, v1 delivery plan, UI design, ADRs, tests, issues, and CI
confidence: high
---

# Petri Eden Project

## Identity

Petri Eden is a native desktop artificial-life laboratory built around a deterministic ecology and inherited neural controllers. The user creates or chooses species, launches a seeded world, watches behavior and population dynamics, intervenes, and inspects why outcomes changed.

## Verb-First Product Frame

**Design species, run a world, perturb it, and trace what the ecology and descendants did next.**

The project is not primarily a simulator backend or a visual evolution toy. Its product is the loop between a living world and the evidence needed to understand it.

## Four Coupled Systems

1. **Ecology** - materials, plants, prey, predators, metabolism, reproduction, death, and decay.
2. **Neuroevolution** - deterministic controllers, mutation, structural change, inheritance, and descendant-count selection.
3. **Experiment instrument** - seeds, exact time, telemetry, lineage/species, events, persistence, export, and branching.
4. **Desktop experience** - world canvas, controls, charts, inspectors, design studio, onboarding, and fault recovery.

## Current Status

As of 2026-07-24:

- The native skeleton and CI/toolchain exist.
- Seeded deterministic replay and digest contracts exist.
- Spatial simulation and deterministic parallel perception exist.
- The first ecology and material-flow loop exists.
- Mutation, structural controller changes, and descendant-count selection exist.
- Pause, exact step, speed policies, and terminal/fault handling exist.
- Ecosystem telemetry is the active delivery frontier.
- Predator viability has exposed a human-gated ecology decision.
- Species recognition, neural inspection, intervention, persistence, endurance, scale, onboarding, packaging, and release audit remain planned.

Read [[wiki/summaries/evidence-and-frontier|Evidence and Frontier]] for the claim boundary.

## Hard Boundaries

- No reward signal, value function, or hidden ecosystem-health score in v1.
- No hand-authored organism behavior trees.
- No open-ended evolution claim.
- No claim that controller size equals intelligence.
- No within-lifetime learning in v1.
- No embodied language-model society in v1.
- No distributed simulation or remote client in v1.

## Namespace Topology

Petri Eden earns a standalone namespace because it has an independent audience, multiple document types, a substantial source corpus, an active update lifecycle, and a clear covers/not-covered boundary.

Reusable topics are routed out rather than duplicated:

- [[../../software-architecture-metapatterns/wiki/syntheses/authoritative-simulation-boundary|Authoritative Simulation Boundary]]
- [[../../eval-trace/wiki/concepts/emergence-claim-ladder|Emergence Claim Ladder]]
- [[../../rl-sim-labs/wiki/concepts/neuroevolution-vs-reinforcement-learning|Neuroevolution vs Reinforcement Learning]]

V2 plasticity and V3 cultural-agent ideas remain inside this namespace until implementation and reuse justify another namespace.

## Related

- [[wiki/summaries/v1-system-map|V1 System Map]]
- [[wiki/summaries/product-experience-and-inspection|Product Experience and Inspection]]
- [[wiki/concepts/operational-species|Operational Species]]
- [[wiki/syntheses/v2-v3-research-branches|V2 and V3 Research Branches]]
