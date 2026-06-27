---
title: Matt Pocock SDLC Rhythm
created: 2026-06-18
updated: 2026-06-27
type: concept
status: compiled
namespace: agent-workflows
tags: [workflow, agent-systems, product-management, design]
sources:
  - /root/.hermes/knowledge/concepts/matt-pocock-sdlc-rhythm.md
  - Knowledge/concepts/matt-pocock-sdlc-rhythm.md
confidence: high
---

# Matt Pocock SDLC Rhythm

## Definition

Jamie uses Matt Pocock-style skills as a pattern-based agent-assisted SDLC rhythm because they counter common agent failure modes: misalignment, missing shared language, weak feedback loops, solution-jumping, and codebase entropy.

Choose the path based on problem clarity and whether product/UI/workflow surface truth is needed. Do not force every request through one rigid pipeline.

## Lock vs key framing

A feature request is a **possible key**. The real user problem, workflow friction, domain constraint, trust gap, or decision bottleneck is the **lock**.

The agent should not rush to compare keys. It should first understand the lock’s shape, then prototype or grill the right thing.

## Pattern 1 — Problem seems clear, but surface truth is needed

Use when the domain problem sounds clear, but product/UI/workflow reality may reveal friction that prose misses.

Sequence:

`/prototype` → `/grill-with-docs` → `/to-prd` → human PRD approval → `/to-issues` → one issue at a time with `/tdd` → verify → PR/review → `/handoff`

Why: visual and interactive surfaces often reveal missing states, wrong information hierarchy, trust gaps, awkward workflow loops, or language that sounds right but feels wrong in use.

## Pattern 2 — Problem is unclear or input is a premature key

Use when the input is a proposed solution, feature request, or “key” but the underlying domain problem / “lock” is fuzzy.

Sequence:

`/prototype` as probe to reveal the lock/problem shape → `/grill-with-docs` → `/to-prd` → human PRD approval → `/to-issues` → one issue at a time with `/tdd` → verify → PR/review → `/handoff`

Prototype-as-probe means creating small disposable artifacts where each variant tests a different lock hypothesis. The goal is not solution polish; the goal is to learn what problem is actually being solved.

Examples:

- “Build an agent dashboard” → probe visibility, control, and trust/evidence surfaces.
- “Add notifications” → probe state-change indicators, audit trails, and digest/subscription flows.
- “Improve CRM deal view” → probe timeline-first, stage-board, and command-center layouts.

## Pattern 3 — Mostly non-visual domain / architecture / rule uncertainty

Use when the uncertainty is primarily terminology, bounded contexts, rules, state transitions, architecture, or trade-offs and a visual surface is unlikely to teach much.

Sequence:

`/grill-with-docs` → `/to-prd` → human PRD approval → `/to-issues` → one issue at a time with `/tdd` → verify → PR/review → `/handoff`

If uncertainty becomes experiential or hard to reason about in words, switch back to `/prototype` as a probe or logic/state prototype.

## Visual plan review gate

Use [[visual-plan-review-surfaces]] when a PRD, implementation plan, or issue plan needs an inspectable artifact before execution. This is an optional review gate between `/to-prd` and `/to-issues`, or between an implementation plan and `/implement`.

Jamie's default is local/private MDX artifacts under `.agent-native/plans/<slug>/`, not hosted share links or comment workflows. The visual plan should preserve durable truth in the PRD/GitHub/vault source while making the plan easier to inspect: file maps, diagrams, UI states, annotated code, open questions, and verification gates.

## Compound Engineering compatibility

[[compound-engineering-skill-layer]] is compatible with this rhythm, but it packages the loop differently. Pocock/Jamie skills are modular gates for prototype, grill, PRD, issue slicing, TDD, review, and handoff. Compound Engineering is an integrated repo-local loop with `ce-brainstorm`, `ce-plan`, `ce-work`, `ce-simplify-code`, `ce-code-review`, and `ce-compound` sharing a unified plan artifact and project-local learning trail. Upstream docs may write these as `/ce-*`; on Discord that is skill shorthand unless a native slash command exists.

Use CE when the active repo should follow that integrated loop. Use this SDLC rhythm when Jamie needs explicit prototype/PRD/issue approval gates, a portfolio/product artifact, or a narrower one-issue implementation path.

## Source-backed best practices

[[matt-pocock-skills-best-practices]] preserves the source-backed pattern from `mattpocock/skills`: small composable skills, grilling for alignment, shared language docs, feedback loops, and architecture discipline. This SDLC rhythm is Jamie's generalized implementation sequence for applying those practices without turning them into a rigid framework.

## Router skill layer

The Pocock skill layer is a router and decomposition toolkit, not a reason to skip current evidence.

Useful routes include:

- `ask-matt` — choose which Matt-style flow fits the situation.
- `grilling` / `grill-me` / `grill-with-docs` — pressure-test the problem, language, and assumptions.
- `decision-mapping` — turn a loose idea into a sequenced investigation map.
- `implement` — implement a bounded piece of work from an approved PRD or issue.
- `codebase-design` — reason about deep modules and vocabulary before changing code.
- `domain-modeling` — sharpen domain language and boundaries.
- `writing-great-skills` — improve reusable skill artifacts.

## Applications

- Use [[find-the-lock-problem-first]] before treating a feature request as the real problem.
- Do not skip `/prototype` just because a product/UI/workflow problem sounds clear.
- Use `/prototype` as a probe when the lock/problem shape is unclear.
- Use `/grill-with-docs` for alignment, ubiquitous language, `CONTEXT.md`, and ADR capture.
- Use `/to-prd` as the lean requirements spine; do not proceed to issues until approved.
- Use `visual-plan` when the PRD or implementation plan needs a richer local review surface before issues or code.
- Use `/to-issues` for vertical tracer-bullet slices, not horizontal layers.
- Use `/tdd` for red-green-refactor feedback loops.
- Use `/handoff` to keep continuity across fresh contexts.
- Use Smart Zone discipline: watch context around 30%, checkpoint/stop before 40%, then continue in a fresh session with handoff.
- Run a [[context-overfitting]] check when a past skill, memory, or project note seems to override current user intent or live evidence.

## Boundaries

- Do not import transient issue, PR, commit, or project milestone state into this concept.
- Do not treat a skill’s existence as authorization to create issues, merge, deploy, change profiles, or trigger worker routes.
- Do not let written SDLC preferences override a current explicit user instruction, live evidence, or the active route contract.

## Related pages

- [[matt-pocock-skills-best-practices]]
- [[compound-engineering-skill-layer]]
- [[visual-plan-review-surfaces]]
- [[find-the-lock-problem-first]]
- [[issue-driven-afk-workflow]]
- [[smart-zone-context-discipline]]
- [[workspace-autonomy-levels]]
- [[context-overfitting]]
- [[agent-capability-route-pattern]]
- [[bounded-context-tree-pattern]]
