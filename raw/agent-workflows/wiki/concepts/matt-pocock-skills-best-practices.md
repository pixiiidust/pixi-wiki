---
title: Matt Pocock Skills Best Practices
created: 2026-06-19
updated: 2026-06-19
type: concept
description: Best-practice pattern from Matt Pocock's skills repo for reducing agent misalignment through small composable skills, grilling, shared language, feedback loops, and architecture discipline.
status: compiled
namespace: agent-workflows
domain: agent-systems
tags: [workflow, agent-systems, architecture]
sources:
  - Knowledge/concepts/matt-pocock-skills-best-practices.md
  - Knowledge/raw/articles/matt-pocock-skills-readme.md
  - https://github.com/mattpocock/skills
confidence: high
---

# Matt Pocock Skills Best Practices

## Definition

Matt Pocock's `skills` repo is a reusable best-practice pattern for reducing agent misalignment while keeping the human in control. The key move is not “let a framework own the process”; it is “give the agent small, composable operating skills that make alignment, shared language, feedback, and design discipline repeatable.”

For Jamie's workflow, this page is the source-backed best-practices concept. [[matt-pocock-sdlc-rhythm]] is the generalized implementation rhythm that translates those practices into Pixoid/Tinker execution gates.

## Misalignment reducers

1. **Keep skills small and composable.** Avoid monolithic process frameworks that hide control flow. Use focused skills that can be adapted per repo and per problem.
2. **Grill before building.** Misalignment is the default failure mode. Use `grill-me` / `grill-with-docs` to ask detailed questions before turning a vague request into implementation.
3. **Write shared language.** Use domain docs such as `CONTEXT.md` and ADRs so humans, agents, files, functions, and tests reuse the same domain terms instead of re-decoding jargon every run.
4. **Tighten feedback loops.** Red-green-refactor tests, static types, browser/runtime checks, and diagnosis loops are the guardrails that stop aligned intent from becoming broken code.
5. **Care about codebase shape.** Agent speed can accelerate entropy. Use architecture/design review skills to keep modules deep, names consistent, and boundaries navigable.
6. **Separate orchestration from discipline.** User-invoked skills route and orchestrate; model-invoked skills hold reusable discipline. A router should not recursively invoke another user-invoked router.

## Implementation pattern

Use the repo as a menu of practices, not as a rigid mandatory pipeline:

- run setup once per repo so tracker labels and docs locations are explicit;
- choose the smallest skill that matches the current failure risk;
- preserve human approval gates before PRDs become issues and before merge/deploy actions;
- verify with real tests/checks before claiming completion;
- capture durable learning in docs, issues, or skills rather than hidden chat memory.

## Relationship to Jamie's SDLC rhythm

[[matt-pocock-sdlc-rhythm]] generalizes the upstream repo into Jamie's default flow:

`/prototype` when surface truth or lock discovery is needed → `/grill-with-docs` for alignment and language → `/to-prd` for a lean requirements spine → `/to-issues` for vertical slices → `/tdd` and verification → PR/review → `/handoff`.

This concept explains **why** those gates reduce misalignment. The SDLC rhythm explains **when** to apply them.

## Boundaries

- Do not use a skill repo as evidence that the agent may create issues, merge, deploy, or mutate runtime configuration without explicit scope and approval.
- Do not let a preferred workflow override current user intent, issue acceptance criteria, live evidence, or safety constraints.
- Do not copy upstream process wholesale when Jamie's repo already has a clearer source of truth; adapt the practice to the active project contract.

## Related pages

- [[matt-pocock-sdlc-rhythm]]
- [[find-the-lock-problem-first]]
- [[building-software-is-learning]]
- [[bounded-context-tree-pattern]]
- [[context-overfitting]]
- [[ponytail-minimal-code-discipline]]
