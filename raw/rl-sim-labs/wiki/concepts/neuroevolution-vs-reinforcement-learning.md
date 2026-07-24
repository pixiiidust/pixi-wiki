---
title: Neuroevolution vs Reinforcement Learning
created: 2026-07-24
updated: 2026-07-24
type: concept
status: active
namespace: rl-sim-labs
sources:
  - Petri Eden project context and native v1 plan
confidence: high
---

# Neuroevolution vs Reinforcement Learning

## Short Answer

Neuroevolution changes neural controllers across generations through mutation, inheritance, and differential reproduction. Reinforcement learning changes a policy from reward-linked experience, usually through returns, value estimates, or policy gradients.

Both can use simulations and neural networks. They are not interchangeable.

## Comparison

| Dimension | Neuroevolution | Reinforcement learning |
|---|---|---|
| Primary update | mutation/recombination plus selection | reward-linked optimization |
| Persistence unit | genome/controller across descendants | policy parameters/state across training |
| Objective source | survival/reproduction or explicit fitness | explicit reward/return |
| Time scale | generations | steps, episodes, and updates |
| Credit assignment | population/lineage outcome, often indirect | temporal reward credit |
| Structural change | natural fit for topology mutation | often fixed policy structure, with exceptions |
| Main evidence | lineage, inherited change, descendant outcomes | return, policy behavior, generalization, training dynamics |

## Important Nuance

Neuroevolution may use an explicit fitness score. Petri Eden deliberately does not do so in v1. Its selection signal is descendant count under ecological pressure, making ecology part of the causal mechanism rather than a backdrop around a scalar objective.

RL may also use evolutionary search or population-based training as an optimizer. The useful classification asks:

1. What state changes?
2. What signal drives the change?
3. When does it persist?
4. What evidence supports the behavioral claim?

## Hybrid Systems

One system can combine:

- inherited evolutionary priors;
- reward-driven within-lifetime policy learning;
- reward-free local plasticity;
- descendant-based selection;
- social or cultural transmission.

Keep state and provenance separate so outcomes can be attributed to genome, reward, lifetime learning, environment, or social transfer.

## Evaluation Differences

### Neuroevolution

- track genomes and lineages;
- compare descendant outcomes;
- preserve ecology and mutation provenance;
- test across generations and unseen seeds;
- distinguish viable environment from successful adaptation.

### Reinforcement learning

- track return and reward definition;
- separate training from evaluation;
- compare policy behavior and generalization;
- control episode and compute budgets;
- inspect reward hacking and environment shortcuts.

Both need deterministic/reproducible environments where possible, negative baselines, and honest failure reporting.

## Failure Modes

- calling every agent-in-environment system RL;
- calling any parameter search evolution without inheritance or differential reproduction;
- hiding a fitness/reward score while claiming ecology-only selection;
- measuring RL only by training return or evolution only by network size;
- comparing systems with unequal compute or environment budgets.

## Applied Example

[[../../petri-eden/wiki/entities/petri-eden|Petri Eden v1]] is a neuroevolution/artificial-life project. Genomes mutate across generations, organisms act through deterministic neural controllers, and selection is descendant count. It has no reward signal or value function.

## Related

- [[../../petri-eden/wiki/summaries/v1-system-map|Petri Eden V1 System Map]]
- [[../../eval-trace/wiki/concepts/emergence-claim-ladder|Emergence Claim Ladder]]
