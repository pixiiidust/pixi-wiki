---
title: Interaction Mode Routing
created: 2026-06-23
updated: 2026-06-23
type: concept
status: compiled
namespace: ai-native-product-surfaces
tags: [ai-native-product-surfaces, ai-native, product-framing, interaction-design, generative-ui]
sources:
  - Knowledge/concepts/interaction-mode-routing.md
  - Knowledge/concepts/ai-native-problem-framing-framework.md
  - Projects/I-know-kungfu/Index.md
  - Projects/Hermes Mission Control/Index.md
confidence: medium
---

# Interaction Mode Routing

**Interaction Mode Routing** is a product refactor lens for choosing whether a task should use direct UI, agentic delegation, generative UI, or stable truth/routing surfaces.

The question is not "should this use AI?" The question is: **what interaction mode best fits the user's need for speed, control, exploration, inspection, and execution?**

## Four modes

| Mode | Use when | Failure smell |
|---|---|---|
| Direct UI | The human can act faster by manipulating visible objects than by describing the action. | Replacing a faster button, slider, table, or visual control with a slower chatbot. |
| Agentic delegation | The user wants an outcome across repetitive or cross-tool work, not every step. | Hiding judgment, provenance, or approval behind autonomous action. |
| Generative UI | The user needs to compare, inspect, tune, approve, or understand a middle-complexity task. | A prompt box that only feeds a fixed grid, or a generated surface that hides source/constraints. |
| Stable truth/routing | The surface is durable source truth, provenance, or routing. | Generated UI becoming the only place a decision, source, or constraint exists. |

## Product-surface use

Use [[ai-native-problem-framing-framework|AI-Native Problem Framing Framework]] first to define environment, actions, goal, and constraints. Then choose the interaction mode:

- direct manipulation for fast, visual, precise work;
- agents for boring multi-step execution;
- generative UI for review/control surfaces;
- stable truth for PRDs, project hubs, GitHub issues, handoffs, skills, MOCs, `llms.txt`, `index.json`, raw Markdown, and MCP entrypoints.

## I-know-kungfu refactor

For [[../entities/i-know-kungfu|I-know-kungfu]], the strongest next surface is a generated **Fit Check Surface** over stable wiki truth:

- source coverage;
- local overlap;
- recommended serving entrypoint;
- refusal boundaries;
- trust/eval state;
- clearly labeled evidence provenance.

This keeps the product out of two traps: pure chatbot and static card pile.

## Pixi Wiki / vault refactor

Pixi Wiki should keep source/navigation stable and generate temporary review surfaces above the corpus:

- compile-review report;
- source-to-output trace map;
- namespace coverage dashboard;
- MCP/live-route visibility report;
- broken/stale route repair panel.

## Agent workflow connection

For Hermes Mission Control, chat is the command channel, not the whole interface. Review and approval should be shaped as small generated control surfaces while durable truth remains in GitHub, Obsidian, handoffs, skills, and knowledge entrypoints.

## Source

Compiled from `Knowledge/concepts/interaction-mode-routing.md` plus project applications in I-know-kungfu, Pixi Wiki, and Hermes Mission Control.
