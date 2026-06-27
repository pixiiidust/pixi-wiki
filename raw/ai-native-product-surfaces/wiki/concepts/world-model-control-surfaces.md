---
title: World Model Control Surfaces
created: 2026-06-26
updated: 2026-06-26
type: concept
status: compiled
namespace: ai-native-product-surfaces
tags: [ai-native-product-surfaces, ai-native, product-framing, interaction-design, grounded-ai]
sources:
  - Knowledge/concepts/world-model-control-surfaces.md
  - Knowledge/raw/transcripts/yann-lecun-world-models-next-ai-revolution.md
  - https://youtu.be/72Xj8k5WQX4?si=tFQOgcbG-xzmz7WI
confidence: medium
---

# World Model Control Surfaces

**World Model Control Surfaces** translate Yann LeCun's world-model argument into a product/interface lens: expose state, available actions, predicted outcomes, objectives, guardrails, and evidence before recommending action.

Core loop:

```text
observed state -> candidate actions -> predicted outcomes -> objective / guardrail score -> recommended next safe step
```

## Why it matters

The transcript argues that grounded intelligence is not just declarative knowledge or next-token generation. It requires abstract predictive models of the world, planning by optimization, and guardrails that score imagined action/state sequences before execution.

For product surfaces, the useful lesson is not “build a full world model now.” It is: **make the system's action model visible**.

## Product-surface use

Use this lens after [[ai-native-problem-framing-framework|AI-Native Problem Framing Framework]] and before choosing the final interface mode with [[interaction-mode-routing|Interaction Mode Routing]].

A good AI-native control/review surface should show:

1. current state;
2. possible actions;
3. predicted outcomes;
4. task objective;
5. guardrails/constraints;
6. evidence and uncertainty;
7. recommended next safe step.

## Application targets

- **Shifu / I-know-kungfu:** show source coverage, local overlap, route effects, refusal boundaries, provenance risk, and recommended import/serve action.
- **Hermes Mission Control:** show task state, candidate next slices, likely side effects, verification evidence, and approval guardrails instead of only “agent says done.”
- **Pixi Wiki:** show source-to-output trace, namespace coverage, MCP/raw/HTML visibility, stale route risk, and suggested repair or promotion action.
- **RL Sim Labs:** separate environment state, allowed actions, dynamics model, objective/reward, evidence gates, and policy/planner output.

## Boundary

This is a concept, not a standalone namespace and not a claim that current LLM agents already have robust learned world models. Do not create separate entity pages for Yann LeCun, JEPA, V-JEPA, SIGReg, or AMI Labs until those entities recur across more Pixi Wiki sources or become project-critical.

## Related pages

- [[ai-native-problem-framing-framework|AI-Native Problem Framing Framework]]
- [[interaction-mode-routing|Interaction Mode Routing]]
- [[material-loop-and-glass-interfaces|Material Loop and Glass Interfaces]]
