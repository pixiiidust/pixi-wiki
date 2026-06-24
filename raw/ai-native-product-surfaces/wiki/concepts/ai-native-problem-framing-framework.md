---
title: AI-Native Problem Framing Framework
created: 2026-06-16
updated: 2026-06-24
type: concept
status: compiled
namespace: ai-native-product-surfaces
tags: [ai-native-product-surfaces, ai-native, product-framing, product-management]
sources:
  - Knowledge/concepts/ai-native-problem-framing-framework.md
  - Knowledge/concepts/material-loop-and-glass-interfaces.md
confidence: high
---

# AI-Native Problem Framing Framework

The **AI-Native Problem Framing Framework** is the reusable lens for deciding whether a product surface is genuinely AI-native or merely has AI attached.

## Core frame

Define the system before picking models:

- **Environment** — what data describes the world?
- **Actions** — what can the system do?
- **Goal** — what is success or what is optimized?
- **Constraints** — what must never be violated?
- **Agency constraints** — what must remain visible, steerable, inspectable, interruptible, or user-owned?

Bad framing creates bad AI. Environment, action space, objective, constraints, and agency boundaries define the intelligence problem.

Agency constraints come from [[material-loop-and-glass-interfaces|Material Loop and Glass Interfaces]]: AI can shorten the path from idea to artifact, but the interface should not hide the judgment-bearing parts of the loop.

## Interface mode after framing

After the environment/actions/goal/constraints frame is clear, use [[interaction-mode-routing|Interaction Mode Routing]] to choose which parts should be direct UI, agentic delegation, generative UI, or stable truth/routing.

This keeps AI-native product work from collapsing into either chatbot theatre or agentic overreach. The interface should preserve provenance, constraints, and human control where the domain requires them.

## Product-surface use

For `ai-native-product-surfaces`, this framework prevents vague “add AI” product thinking. It asks whether the surface perceives a domain, chooses or prepares actions, improves the chance of achieving a goal, and respects hard constraints.

It is especially useful for comparing:

- Planned Program Intel: event-program decision routing and institutional memory;
- myAbode: real-estate prepared next actions under compliance and adoption constraints;
- future surfaces that need prediction, optimization, and execution separated rather than collapsed into a black box.

## Boundary

Do not blindly copy game/RL patterns into product domains. Real-world operational products have partial visibility, noisy outcomes, multiple stakeholders, and constraints that must be represented explicitly.

## Related pages

- [[interaction-mode-routing|Interaction Mode Routing]]
- [[material-loop-and-glass-interfaces|Material Loop and Glass Interfaces]]

## Source

Compiled from `Knowledge/concepts/ai-native-problem-framing-framework.md`.
