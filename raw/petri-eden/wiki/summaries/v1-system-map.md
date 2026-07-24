---
title: Petri Eden V1 System Map
created: 2026-07-24
updated: 2026-07-24
type: summary
status: active
namespace: petri-eden
sources:
  - Petri Eden native v1 plan and architecture decisions
confidence: high
---

# Petri Eden V1 System Map

## Architecture

```text
Desktop shell
  SFML window, input, rendering, ImGui-SFML controls
       |
       v typed commands

Simulation host
  one authoritative thread, lifecycle, command order, time policy
       |
       v deterministic step

Simulation core
  world, ecology, perception inputs, neural controllers,
  actions, materials, birth/death, genome, mutation, lineage
       |
       +--> immutable snapshots --> renderer and inspectors
       +--> events/telemetry ----> charts and evidence views
       +--> saved authority -----> resume, export, branch
```

## Module Boundaries

| Module | Owns | Must not own |
|---|---|---|
| Contracts | IDs, commands, snapshots, persistence/export schemas | domain behavior |
| Simulation core | canonical world state and deterministic tick transitions | window/UI timing |
| Simulation host | authority thread, queues, time policy, snapshot publication | product rendering |
| Renderer | world pixels from snapshots | live state mutation |
| UI | commands and explanations | direct world writes |
| Acceptance | cross-module proof, golden digests, endurance | production authority |

## Deterministic Parallel Perception

Petri Eden parallelizes expensive spatial perception without parallelizing authority:

1. the authority thread captures a read-only world view;
2. organisms are ordered by stable ID;
3. workers compute into preassigned result slots;
4. workers do not mutate the world or consume shared random state;
5. results commit in canonical order;
6. supported worker counts must produce matching authoritative digests.

The reusable form of this pattern lives in [[../../software-architecture-metapatterns/wiki/syntheses/authoritative-simulation-boundary|Authoritative Simulation Boundary]].

## V1 Domain Loop

```text
sense -> controller -> act -> ecology/material transfer
      -> birth/death -> inherit/mutate -> lineage/species
      -> telemetry/snapshot -> inspect/intervene
```

Selection is descendant count under ecological pressure. There is no reward signal or value function. See [[../../rl-sim-labs/wiki/concepts/neuroevolution-vs-reinforcement-learning|Neuroevolution vs Reinforcement Learning]].

## Delivery Sequence

The native plan is deliberately sequential:

1. skeleton and toolchain;
2. deterministic timeline;
3. spatial world and parallel perception;
4. ecology and material accounting;
5. evolution and mutation;
6. time control;
7. telemetry;
8. species/lineages;
9. perception and neural inspection;
10. interventions;
11. persistence/export/branching;
12. unattended-run resilience;
13. scale/performance;
14. onboarding and keyboard access;
15. desktop/visual certification;
16. private packaging;
17. release-candidate audit.

As of 2026-07-24, steps 1-6 are implemented and step 7 is active. The remaining steps are planned, not shipped.

## Integrity Boundary

A healthy simulation can contain ecological collapse. Product state must distinguish:

- **normal**: authority and observations are current;
- **degraded**: observation or performance is reduced but truth remains valid;
- **faulted**: an invariant or authority path failed;
- **terminal ecology**: the simulated world reached an ordinary terminal condition.

A population crash is not automatically a technical fault, and a frozen chart must not be interpreted as stable ecology.

## Related

- [[wiki/summaries/evidence-and-frontier|Evidence and Frontier]]
- [[wiki/summaries/product-experience-and-inspection|Product Experience and Inspection]]
- [[wiki/concepts/operational-species|Operational Species]]
