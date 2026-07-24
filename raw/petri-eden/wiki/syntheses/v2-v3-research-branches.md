---
title: Petri Eden V2 and V3 Research Branches
created: 2026-07-24
updated: 2026-07-24
type: synthesis
status: speculative
namespace: petri-eden
sources:
  - Petri Eden V2 draft and V3 brainstorm
confidence: medium
---

# Petri Eden V2 and V3 Research Branches

> Future research only. V2 is a draft. V3 is a brainstorm. Neither is a shipped v1 capability.

## V2 - Lifetime Plasticity and the Baldwin Effect

### Question

Can organisms that learn during a lifetime drive evolution toward inherited predispositions that make useful learning faster, cheaper, or more reliable?

### Proposed separation

```text
inherited genome parameters
        +
within-lifetime learned state
        +
environment and experience
        -> behavior and descendant outcome
```

Learned state should not be copied directly into the genome. The Baldwin-effect hypothesis is indirect: organisms with better inherited predispositions learn more effectively, leave more descendants, and shift the inherited population over generations.

### Required controls

- learning enabled versus disabled;
- explicit learning tax enabled versus removed;
- learned state reset and leak tests;
- equal ecology, seed, and run budgets;
- lineage/genome and learned-state measurements kept separate;
- fixed plus unseen seeds;
- holdout behaviors or environments.

### Failure boundary

A controller changing within one lifetime shows plasticity. It does not alone show the Baldwin effect. That requires cross-generation inherited change caused by differential reproduction among learners.

## V3 - Embodied Agents and Cultural Evolution

### Question

Can embodied agents develop and transmit useful information through communication, imitation, teaching, or artifacts in ways that cross genomic lineage?

### Three inheritance systems

1. **Genomic** - parent to descendant.
2. **Lifetime memory** - experience retained by one organism.
3. **Cultural/memetic** - information transmitted socially or through the environment.

Each needs distinct state, provenance, and lineage. Otherwise a result cannot be attributed.

### Required controls

- communication disabled;
- imitation/teaching disabled;
- artifact persistence disabled;
- bounded message cost and bandwidth;
- shared-prompt and memory-leak checks;
- novel-task transfer tests;
- information tracing across non-kin agents;
- comparison against pretrained model priors.

### Failure boundary

Fluent language-model output is not evolved communication. Shared model priors are not culture. Cultural-evolution claims require socially transmitted behavior or information that persists, transfers, and changes outcomes under controlled conditions.

## Namespace Decision

V2 and V3 stay in `petri-eden` now. Creating separate namespaces would overstate draft material and fragment one project's research roadmap.

Reconsider a new namespace only when a branch has:

- active implementation and a reproducible evidence corpus;
- reusable concepts beyond Petri Eden;
- an independent audience and update lifecycle;
- multiple document types;
- a clear covers/not-covered boundary.

## Related

- [[wiki/entities/petri-eden|Petri Eden Project]]
- [[wiki/summaries/evidence-and-frontier|Evidence and Frontier]]
- [[../../eval-trace/wiki/concepts/emergence-claim-ladder|Emergence Claim Ladder]]
- [[../../rl-sim-labs/wiki/concepts/neuroevolution-vs-reinforcement-learning|Neuroevolution vs Reinforcement Learning]]
