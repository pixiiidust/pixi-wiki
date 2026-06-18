---
title: Ponytail Minimal Code Discipline
created: 2026-06-18
updated: 2026-06-18
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-workflows, code-review, minimalism, verification]
sources:
  - Knowledge/concepts/ponytail-minimal-code-discipline.md
  - /root/.hermes/skills/software-development/ponytail-code-discipline/SKILL.md
confidence: high
---

# Ponytail Minimal Code Discipline

**Ponytail** is a minimal-code discipline for agentic coding work: write only the code the current task needs, prefer native/stdlib/existing-dependency solutions, and run a separate simplification pass during review.

It is a workflow guardrail, not a product spec or always-on personality override.

## Build ladder

1. Does this need to exist?
2. Does stdlib/browser/native platform already do it?
3. Does an existing dependency solve it?
4. Can it be one line or one small function?
5. Only then, write the minimum code that satisfies the current issue.

## Where it belongs

- Coding workflows before implementation.
- Pre-PR checks.
- Pixoid/Tinker PR review passes.
- Reusable Knowledge and skill surfaces.
- Project-specific repo docs only after a concrete project adopts it.

## Boundaries

Ponytail cannot simplify away:

- Jamie's current instruction.
- GitHub issue / PRD acceptance criteria.
- Security, auth, secrets, and trust-boundary validation.
- Accessibility basics.
- Data-loss prevention and persistence/recovery requirements.
- Evidence quality, eval proof, or human decision authority.
- One small runnable check for non-trivial logic.

Current user instruction, issue scope, and safety gates beat memory or generic Ponytail preference.

## Review seam

Run two passes:

1. **Correctness pass:** scope, acceptance criteria, tests, UX, security, accessibility, product/evidence gates.
2. **Ponytail pass:** `delete`, `stdlib`, `native`, `yagni`, and `shrink` findings only.

If there is nothing to cut: `Ponytail: lean already.`

## Source

Compiled from `Knowledge/concepts/ponytail-minimal-code-discipline.md` and the Hermes `ponytail-code-discipline` skill.
