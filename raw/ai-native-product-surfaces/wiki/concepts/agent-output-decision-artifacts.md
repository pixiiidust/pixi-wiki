---
title: Agent Output Decision Artifacts
created: 2026-06-27
updated: 2026-06-27
type: concept
status: compiled
namespace: ai-native-product-surfaces
tags: [ai-native-product-surfaces, ai-native, product-framing, interaction-design, agent-workflows]
sources:
  - Knowledge/concepts/agent-output-decision-artifacts.md
  - Knowledge/concepts/interaction-mode-routing.md
  - Knowledge/concepts/material-loop-and-glass-interfaces.md
  - Knowledge/concepts/visual-plan-review-surfaces.md
confidence: medium
---

# Agent Output Decision Artifacts

**Agent Output Decision Artifacts** are concise, visual, interactive surfaces that convert verbose AI-agent output into an inspectable decision.

The artifact is not a generic summary. It is a control surface: preserve what matters for the decision, expose evidence where trust is needed, and make the next action obvious.

## Core pattern

1. **Compress** the agent run into decision-critical meaning.
2. **Structure** it around three visible elements: options, risks, actions, evidence cards, or tradeoffs.
3. **Close the loop** with approve, reject, annotate, choose, or steer-back controls.

## Artifact contract

A good decision artifact:

- fits on one screen by default;
- removes repetition, caveats, filler, and process narration;
- uses simple clear sentences;
- uses cards, tables, hierarchy, or diagrams when they carry structure faster than prose;
- keeps details behind progressive disclosure;
- preserves source anchors or expandable evidence;
- makes the next action visible within 5-10 seconds.

## Why it matters

Verbose chat is useful while an agent is working. It is a weak final surface when the user needs to decide.

Decision artifacts let chat remain the command channel while the review/approval work moves into a surface that is easier to scan, compare, and steer.

## Relationship to existing lenses

- [[interaction-mode-routing|Interaction Mode Routing]] decides when chat should give way to generated review/control surfaces.
- [[material-loop-and-glass-interfaces|Material Loop and Glass Interfaces]] explains why judgment-bearing work needs to stay visible, steerable, interruptible, and traceable.
- [[../../agent-workflows/wiki/concepts/visual-plan-review-surfaces|Visual Plan Review Surfaces]] is a workflow-specific subtype for turning PRDs and implementation plans into inspectable MDX/HTML review artifacts.
- [[world-model-control-surfaces|World Model Control Surfaces]] gives the control-loop shape: show state, actions, predicted outcomes, objectives, guardrails, evidence, and next safe step.

## Example surfaces

| Surface | Compresses | User action |
|---|---|---|
| Ideation artifact | long brainstorm or agent proposal | choose, reject, or validate one direction |
| PR review artifact | code-review run and verification output | merge, block, or request changes |
| Research artifact | source-heavy investigation | accept answer, ask follow-up, or inspect evidence |
| Compile/release artifact | source changes and generated outputs | approve publish or fix route gaps |

## Boundaries

- Not every agent output deserves a generated artifact; sometimes a table, diff, or short answer is enough.
- The artifact should point back to stable truth rather than becoming the only source of truth.
- Do not hide uncertainty; make it visible through confidence, evidence, open questions, or expandable detail.

## Source

Compiled from `Knowledge/concepts/agent-output-decision-artifacts.md` and adjacent Pixi Wiki concepts.
