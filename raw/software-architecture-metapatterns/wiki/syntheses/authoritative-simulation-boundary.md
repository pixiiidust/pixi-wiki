---
title: Authoritative Simulation Boundary
created: 2026-07-24
updated: 2026-07-24
type: synthesis
status: active
namespace: software-architecture-metapatterns
sources:
  - Petri Eden native architecture decisions and deterministic simulation plan
confidence: high
---

# Authoritative Simulation Boundary

## Pattern

Place one component in sole control of canonical simulation mutation. External systems submit typed ordered commands and consume immutable snapshots, events, telemetry, or persisted artifacts.

```text
commands -> authoritative host -> pure simulation step -> canonical state
                                 -> snapshots
                                 -> events/telemetry
                                 -> persistence/export
```

The boundary turns thread schedules, frame timing, UI interaction, and metrics collection into external concerns rather than hidden domain inputs.

## Forces

- Interactive applications need responsive rendering and controls.
- Simulations need stable causal order and reproducibility.
- Expensive sensing or physics may need parallel work.
- Observability must explain state without becoming state authority.
- Save/resume and branch comparison need exact identity.
- Failures in the view layer must not corrupt domain truth.

## Resolution

### One mutation authority

Only the host/authority thread commits world changes. UI, renderer, workers, exporters, and inspectors cannot write directly to live domain state.

### Ordered command ingress

Every intervention has a typed payload, validation rule, sequence position, and recorded provenance. Commands are domain inputs; mouse events and frame callbacks are not.

### Pure or explicit step boundary

The simulation step consumes canonical state, ordered commands, and deterministic random streams. It produces new canonical state plus events/snapshots through explicit contracts.

### Snapshot egress

Readers receive immutable versioned snapshots. A reader may be stale or degraded without changing the world. Backpressure and retention are observable policies.

### Deterministic parallelism

Parallel workers receive read-only inputs and preassigned output slots. They do not mutate shared world state or consume one shared PRNG. The authority commits results in stable order and verifies equivalent digests across worker counts.

## Failure State Taxonomy

Keep these distinct:

- normal domain outcome, including simulated collapse;
- degraded observation or performance with valid authority;
- faulted authority or invariant failure;
- terminal simulated state.

This prevents an empty ecosystem from being mistaken for a crashed application and a frozen chart from being mistaken for a stable ecosystem.

## Quality Attributes

| Attribute | Benefit | Cost |
|---|---|---|
| Determinism | replay, comparison, debugging, scientific confidence | stricter data structures and math choices |
| Testability | headless core and digest-based contracts | more explicit schemas and fixtures |
| Concurrency safety | workers cannot race domain mutation | authority commit can become a bottleneck |
| UI resilience | rendering/inspection failures stay outside truth | snapshot freshness needs policy |
| Persistence | exact save/resume/branch semantics | migration and provenance burden |

## When to Use

Use this pattern when domain causality matters more than maximum distributed throughput: artificial life, strategy simulation, digital twins, reproducible games, training environments, and scientific desktop tools.

Avoid pretending it is free. If the world must scale across machines with independent writers, the authority model needs partitioning, consensus, or a different consistency contract.

## Applied Example

[[../../petri-eden/wiki/summaries/v1-system-map|Petri Eden's V1 System Map]] applies the pattern with a pure simulation core, one simulation host, deterministic parallel perception, and snapshot-driven native UI.

## Related

- [[../../petri-eden/wiki/entities/petri-eden|Petri Eden Project]]
- [[../../eval-trace/wiki/concepts/emergence-claim-ladder|Emergence Claim Ladder]]
