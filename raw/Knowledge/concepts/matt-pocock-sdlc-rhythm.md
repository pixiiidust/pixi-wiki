---
title: Matt Pocock SDLC Rhythm
created: 2026-06-07
updated: 2026-06-07
type: concept
tags: [workflow, agent-systems, product-management, design]
sources: []
confidence: high
---

# Matt Pocock SDLC Rhythm

## Definition

Jamie uses Matt Pocock-style skills as an agent-assisted SDLC rhythm because they counter common agent failure modes: misalignment, missing shared language, weak feedback loops, solution-jumping, and codebase entropy.

The rhythm is pattern-based, not a rigid pipeline. Choose the path based on problem clarity and whether product/UI/workflow surface truth is needed.

## Lock vs key framing

A feature request is a **possible key**. The domain problem, constraint, workflow breakdown, trust gap, or decision bottleneck is the **lock**.

The agent should not rush to compare keys. It should first understand the lock's shape, then prototype or grill the right thing.

## Pattern 1 — Problem seems clear, but surface truth is needed

Use when the problem sounds clear, but product/UI/workflow reality may reveal friction that prose misses.

Sequence:

`/prototype` → `/grill-with-docs` → `/to-prd` → human PRD approval → `/to-issues` → one issue at a time with `/tdd` → verify → PR/review → `/handoff`

Why: visual and interactive surfaces often reveal missing states, bad information hierarchy, trust gaps, awkward workflow loops, or language that sounds right but feels wrong in use.

## Pattern 2 — Problem is unclear or input is a premature key

Use when the input is a proposed solution, feature request, or “key” but the underlying domain problem / “lock” is fuzzy.

Sequence:

`/prototype` as probe to reveal the lock/problem shape → `/grill-with-docs` → `/to-prd` → human PRD approval → `/to-issues` → one issue at a time with `/tdd` → verify → PR/review → `/handoff`

Prototype-as-probe means creating small disposable artifacts where each variant tests a different lock hypothesis, not proving a chosen solution works.

Examples:

- “Build an agent dashboard” → probe visibility, control, and trust/evidence surfaces.
- “Add notifications” → probe state-change indicators, audit trails, and digest/subscription flows.
- “Improve CRM deal view” → probe timeline-first, stage-board, and command-center layouts, as in [[Projects/myAbode/04 - Product/UI Surfaces|myAbode UI Surfaces]] and [[Projects/myAbode/04 - Product/Command Grid|Command Grid]].

## Pattern 3 — Mostly non-visual domain / architecture / rule uncertainty

Use when uncertainty is primarily terminology, bounded contexts, rules, state transitions, architecture, or trade-offs and a visual surface is unlikely to teach much.

Sequence:

`/grill-with-docs` → `/to-prd` → human PRD approval → `/to-issues` → one issue at a time with `/tdd` → verify → PR/review → `/handoff`

If uncertainty becomes experiential or hard to reason about in words, switch back to `/prototype` as a probe or logic/state prototype.

## Operating rules

- Check existing assets before creating new workflows, skills, or docs; prefer adapting useful assets over reinventing them.
- Do not skip `/prototype` just because the problem sounds clear for product/UI/workflow work.
- Use `/prototype` as a probe when the lock/problem shape is unclear.
- Use `/grill-with-docs` for alignment, ubiquitous language, `CONTEXT.md`, and ADR capture.
- Use `/to-prd` as the lean requirements spine; do not proceed to issues until approved.
- Use `/to-issues` for vertical tracer-bullet slices, not horizontal layers.
- Use `/tdd` for red-green-refactor feedback loops.
- Use `/handoff` to keep continuity across fresh contexts.
- Use `/grill-me` for non-code thinking.
- Smart Zone: watch context around 30%, checkpoint/stop before 40%, then continue in a fresh session with handoff.

## Related pages

- [[find-the-lock-problem-first]]
- [[Projects/myAbode/04 - Product/UI Surfaces]]
- [[Projects/myAbode/04 - Product/Command Grid]]
- [[Knowledge/index|Knowledge Wiki Index]]
