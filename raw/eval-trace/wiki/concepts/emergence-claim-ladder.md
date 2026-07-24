---
title: Emergence Claim Ladder
created: 2026-07-24
updated: 2026-07-24
type: concept
status: active
namespace: eval-trace
sources:
  - Petri Eden evidence plan and simulation triage policy
confidence: high
---

# Emergence Claim Ladder

## Definition

The emergence claim ladder is an evaluation discipline for simulations and agent populations. It prevents a visually interesting run from being promoted directly into a claim about evolution, intelligence, learning, communication, or culture.

Each level supports a bounded statement. Higher levels require the lower gates plus new evidence.

## Ladder

| Level | Allowed claim | Evidence gate |
|---|---|---|
| 1 | The system executes | reproducible build and smoke evidence |
| 2 | The timeline is deterministic | repeated digests across runs and supported worker counts |
| 3 | The environment is viable | long-run baselines, conservation, and explained failures |
| 4 | Measured populations or behavior change | retained telemetry, denominators, and fault separation |
| 5 | Change is inherited or learned | lineage/genome or within-lifetime state evidence |
| 6 | The effect is repeatable and causal | multiple seeds, controls, ablations, and competing explanations |
| 7 | A strong emergence claim is warranted | operational definition, broad failure-aware evidence, and independent scrutiny |

## Evidence Depends on the Claim

### Evolution

Requires inheritance, differential reproduction, lineage continuity, and cross-generation change. Population movement or controller growth alone is insufficient.

### Learning

Requires within-lifetime state change tied to experience and improved behavior, with inherited state and environmental shortcuts controlled.

### Communication

Requires evidence that signals transfer information and alter another agent's behavior beyond shared-environment correlation.

### Culture

Requires socially transmitted behavior or information that persists and crosses biological lineage boundaries. Shared prompts and pretrained priors are not culture.

### Intelligence

Requires an operational task and generalization definition. Neural-network size, fluent output, visual complexity, or observer surprise is not enough.

## Reusable Controls

- fixed and unseen seeds;
- no-op, random, and scripted baselines;
- mechanism-on versus mechanism-off ablations;
- worker-count determinism matrices;
- lineage and provenance tracing;
- holdout tasks or environments;
- explicit failures and negative results;
- blinded or independent review for anthropomorphic judgments.

## Anti-patterns

- selecting one spectacular seed after many runs;
- using screenshots as causal evidence;
- changing environment and controller mechanisms together;
- hiding a reward/health score while claiming ecology-only selection;
- treating an operational label as a discovered natural category;
- using fluent language-model output as proof of evolved culture.

## Applied Example

[[../../petri-eden/wiki/summaries/evidence-and-frontier|Petri Eden's Evidence and Frontier]] requires deterministic execution, viable ecology, trustworthy telemetry, lineage evidence, and cross-seed controls before stronger evolutionary claims.

## Related

- [[../../petri-eden/wiki/syntheses/v2-v3-research-branches|Petri Eden V2 and V3 Research Branches]]
- [[../../rl-sim-labs/wiki/concepts/neuroevolution-vs-reinforcement-learning|Neuroevolution vs Reinforcement Learning]]
- [[../../software-architecture-metapatterns/wiki/syntheses/authoritative-simulation-boundary|Authoritative Simulation Boundary]]
