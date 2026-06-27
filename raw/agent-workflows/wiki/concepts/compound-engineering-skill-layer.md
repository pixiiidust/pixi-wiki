---
title: Compound Engineering Skill Layer
created: 2026-06-27
updated: 2026-06-27
type: concept
status: compiled
namespace: agent-workflows
source: Knowledge/concepts/compound-engineering-skill-layer.md
confidence: high
---

# Compound Engineering Skill Layer

Compound Engineering is an EveryInc plugin that packages a repo-local engineering loop: ideate or brainstorm, plan, work, simplify, review, compound the learning, and repeat with better context.

In Jamie's Hermes setup, it is installed at `/root/.hermes/plugins/compound-engineering-plugin/skills` and exposed as normal Hermes skills such as `ce-setup`, `ce-brainstorm`, `ce-plan`, `ce-work`, `ce-simplify-code`, `ce-code-review`, `ce-debug`, `ce-compound`, and `lfg`.

## Quick start

Run once per target repo:

```text
/ce-setup
```

Then use the standard loop:

```text
/ce-brainstorm describe the feature or problem
/ce-plan
/ce-work
/ce-simplify-code
/ce-code-review
/ce-compound
```

## When to use it

| Situation | Route |
|---|---|
| Need grounded build ideas | `/ce-ideate` -> `/ce-brainstorm` |
| Need requirements before implementation | `/ce-brainstorm` -> `/ce-plan` |
| Need to execute an approved CE plan | `/ce-work` |
| Need to clean fresh implementation work | `/ce-simplify-code` |
| Need plan-aware review | `/ce-code-review` |
| Need bug reproduction/root cause/fix | `/ce-debug` -> `/ce-code-review` -> `/ce-compound` |
| Need project-local learning capture | `/ce-compound` |
| Need bounded autopilot after requirements | `/lfg`, only with explicit scope/approval gates |

## Similar to existing skills

Compound Engineering aligns with [[matt-pocock-sdlc-rhythm]] and [[matt-pocock-skills-best-practices]]: it reduces misalignment through planning, shared artifacts, feedback loops, review, and durable learning.

It also overlaps with [[agent-skill-routing]] because Pixoid should choose the right CE skill automatically instead of making Jamie be the skill librarian.

## Different from existing skills

- CE is an integrated workflow package; Pocock/Jamie skills are modular gates.
- CE's `/ce-brainstorm` and `/ce-plan` write a shared unified plan artifact for downstream CE commands; `/to-prd` and `/to-issues` remain better when the durable deliverable is a PRD/issue tree.
- CE's `/ce-work` assumes the CE plan context; `implement`/`tdd` remain better for one narrow GitHub issue or an existing non-CE plan.
- CE's `/ce-compound` captures project-local engineering learning, usually under `docs/solutions/`; Obsidian/Pixi Wiki remain the home for reusable human-facing knowledge.
- CE's `/lfg` is an autopilot. Jamie's AFK route contracts still govern profile boundaries, handoffs, merge/deploy approval, and route observability.

## Pixoid routing rules

- Use CE for repo-local engineering loops.
- Use `prototype`, `visual-plan`, `grill-with-docs`, `/to-prd`, and `/to-issues` when Jamie needs explicit human review artifacts before execution.
- Use normal `code-review`, `debugging`, `ponytail-code-discipline`, or `test-driven-development` when CE's unified plan artifact is not the active source.
- Do not let `/lfg` bypass destructive-change, deploy, merge, secret, profile/runtime, or public publishing approvals.
- Treat CE skills as procedures, not proof: inspect live state, run tests, and verify outputs before reporting success.

## Related pages

- [[agent-skill-routing]]
- [[matt-pocock-sdlc-rhythm]]
- [[matt-pocock-skills-best-practices]]
- [[visual-plan-review-surfaces]]
- [[profile-memory-boundaries]]
