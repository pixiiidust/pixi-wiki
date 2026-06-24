---
title: Material Loop and Glass Interfaces
created: 2026-06-24
updated: 2026-06-24
type: concept
status: compiled
namespace: ai-native-product-surfaces
tags: [ai-native-product-surfaces, ai-native, product-framing, interaction-design, generative-ui]
sources:
  - Knowledge/concepts/material-loop-and-glass-interfaces.md
  - Knowledge/concepts/interaction-mode-routing.md
  - Knowledge/concepts/ai-native-problem-framing-framework.md
  - https://youtu.be/az6OEZV8iHw
confidence: medium
---

# Material Loop and Glass Interfaces

**Material Loop and Glass Interfaces** is the agency/authorship lens for AI-native product surfaces.

The **Material Loop** is the cycle where a person turns an idea into a visible artifact, inspects what feels wrong, changes it, and develops judgment through contact with the work.

A **Glass Interface** keeps AI-shaped work inspectable, steerable, interruptible, and traceable. It exposes enough plan, state, sources, tools, diffs, commands, constraints, and intermediate artifacts for the user to stay close to the material without micromanaging every step.

Black-box AI optimizes for clean output. Glass AI optimizes for human agency over shapeable material.

## Output vs material

| Output | Material |
|---|---|
| Finished-looking answer | Shapeable intermediate artifact |
| Accept/reject loop | Inspect/steer/edit loop |
| Hides process | Shows relevant state and provenance |
| User becomes approver | User remains author |
| Can weaken judgment | Can build judgment |

## Material closeness test

Before choosing an interaction mode, ask:

1. Is this a taste-bearing or judgment-bearing decision?
2. Would hiding the process make the user less able to learn, steer, or verify?
3. Does the user need to see the plan, sources, diff, trace, or intermediate state?
4. Is the artifact still shapeable, or has the system collapsed it into final output?
5. Can the user interrupt, edit, branch, or take over?

If the work is boring execution, delegate it to an agent with verifiable output. If the work carries judgment, taste, trust, scope, provenance, architecture, or release responsibility, keep the user close to the material through direct UI, generative UI, stable truth surfaces, or visible agent traces.

## Relationship to Interaction Mode Routing

[[interaction-mode-routing|Interaction Mode Routing]] chooses the tactical surface: direct UI, agentic delegation, generative UI, or stable truth/routing.

Material Loop and Glass Interfaces explain why the route matters: the interface should preserve the user's ability to inspect, steer, learn, and care.

## Pixi Wiki implication

Pixi Wiki should keep source/navigation stable while generating temporary review surfaces above the corpus:

- source-to-output trace maps;
- namespace coverage dashboards;
- compile-review reports;
- MCP/live-route visibility reports;
- stale route repair panels.

The goal is not only to publish knowledge, but to keep the knowledge system close enough to the material that humans and agents can inspect, route, correct, and trust it.

## I-know-kungfu implication

[[../entities/i-know-kungfu|I-know-kungfu]] should not become a magic import button. Its strongest surface is a glass fit-check interface over stable wiki truth: source coverage, local overlap, proposed harmonization, serving entrypoint, refusal boundaries, trust/eval state, and provenance.

## Hermes Mission Control implication

Hermes review surfaces should show enough plan, diff, evidence, risk, and next-action state for Jamie to remain the author of the decision instead of merely approving a plausible agent summary.

## Source

Compiled from `Knowledge/concepts/material-loop-and-glass-interfaces.md`, inspired by Ryo Lu's "Closer to the Material" talk for Cursor Compile 26.
