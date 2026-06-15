---
title: Self-Improving Agent Systems
created: 2026-06-12
updated: 2026-06-13
type: concept
description: Model for agent systems that improve through verified durable state, evidence grades, promotion ladders, and future-run retrieval rather than weight updates.
status: active
domain: agent-systems
tags: [agent-systems, governance, ai]
sources: [discord-thread, local-hermes-knowledge]
confidence: high
---

# Self-Improving Agent Systems

## Definition

A self-improving agent system does not update model weights. It improves because each run converts verified evidence into better durable context, skills, rubrics, routing rules, and project state that future runs consult.

Short form: **observe → judge → verify → distill → write → consult next run**.

## What evolves (not the model)

| Layer | What gets better |
|---|---|
| **Agent dossiers** | Role-specific feedback, strengths, gaps, and review patterns |
| **Knowledge concepts** | Reusable frameworks and distinctions agents reason from |
| **Skills** | Repeatable procedures, pitfalls, commands, checks, verification routines |
| **Cron/routing prompts** | Scheduled operating contracts and trigger behavior |
| **Project source of truth** | GitHub issues, PRs, Obsidian project hubs, evidence handles |
| **Hermes memory** | Last-mile compact routing facts only; not the main learning substrate |

This extends [[profile-memory-boundaries]]: full concepts belong in `~/.hermes/knowledge/concepts/`, procedures in skills, and project state in Obsidian/GitHub.

## Evidence grades

Before changing durable state, assign one grade:

- **`jamie-correction`** — Jamie explicitly corrected behavior, framing, or storage location.
- **`verified-regression`** — live evidence proves the system repeated a known failure.
- **`repeated-pattern`** — same success/failure across 2+ runs or artifacts.
- **`single-high-impact`** — one event strong enough to prevent future harm or drift.
- **`weak-signal`** — observe only; do not evolve durable state yet.
- **`no-action`** — no durable lesson.

## Promotion ladder

Use the smallest durable layer that can carry the lesson:

```
raw run/output
→ agent dossier feedback
→ knowledge concept
→ skill patch
→ cron/routing prompt update
→ compact Hermes memory pointer (only if always-injected routing is worth the cost)
```

Do not skip straight from raw output to memory or broad skill rewrites. Dossiers are the normal daily learning surface; skills are for repeated procedures.

## Verifier rule

Makers should not grade their own homework. Prefer independent review when the outcome matters:

- Pixoid reviews Boba/Quill/Tinker output against the current lens and issue scope.
- Quill may draft vault/source-of-truth changes, but Pixoid verifies changed files, issue checkboxes, commits, and pushed state before closure.
- Pixoid self-evolution needs stronger evidence: Jamie correction, concrete worker outcome, repeated pattern, or verified artifact state. Pixoid self-praise alone is not enough.

## Cron maturity model

A mature agent-evolution cron should:

1. Read durable state first: schema, index, log, actionability lens, agent dossiers, recent cron outputs, Kanban/GitHub/profile state, and relevant scratch reports.
2. Make explicit quality calls before editing.
3. Attach an evidence grade to each proposed evolution.
4. Write to the right layer using the promotion ladder.
5. Suppress stale/no-delta findings; speak only for new durable deltas or needed Jamie judgment.
6. Gate risky actions: profile creation, memory pruning, broad skill rewrites, destructive edits, deployments, and merges need explicit approval unless a route contract says otherwise.
7. Never claim perfect future behavior — only increased probability through better state, rubrics, verification, and retrieval.

## Risky-action policy

- **Profile creation** — proposal-only by default. Detect repeated role overload and draft the candidate; do not create/enable gateways/tokens without approval.
- **Memory pruning** — routine crons may propose prune/slim candidates only. Explicit Jamie save/prune requests authorize narrow cleanup.
- **Skill rewrites** — no broad daily rewrites. Patch only from repeated procedural evidence, Jamie correction, or single high-impact recurring risk.
- **Cron changes** — preserve schedule, delivery, model/provider, skills, and toolsets unless the issue explicitly approves the change.
- **Guarantees** — do not promise perfect behavior; use verification gates and live source-of-truth checks.


## `pixoid.evolution` route contract

Pixoid's daily and weekly evolution reviews are a bounded route, not open-ended self-modification.

| Field | Contract |
|---|---|
| **Trigger** | Scheduled Pixoid evolution crons or an explicit Jamie request to review/evolve the crew. |
| **Inputs** | Current actionability lens, recent crew outputs, cron output summaries, Kanban/GitHub state, agent dossiers, relevant skills, and vault/project source-of-truth notes. |
| **Allowed writes** | Agent dossier feedback, small knowledge concept updates, targeted skill patches, and cron prompt proposals or approved prompt edits. |
| **Forbidden without explicit approval** | Profile creation, profile deletion, gateway changes, secret/config mutation, broad memory pruning, broad skill rewrites, deploys, destructive edits, or new autonomous loops. |
| **Evidence gate** | Every durable change needs an evidence grade: Jamie correction, verified regression, repeated pattern, or single high-impact event. Weak signals stay as observations only. |
| **Verifier rule** | Pixoid self-review is not enough. Pixoid self-evolution needs external evidence: Jamie correction, concrete worker outcome, repeated pattern, or verified artifact state. |
| **Output policy** | Stay silent/no-op when no durable learning exists; speak only for durable deltas, blockers, or a specific Jamie decision need. |
| **Stop conditions** | Stop before risky actions, unclear evidence, conflicting source-of-truth state, or changes that would affect another profile's runtime behavior. |

This route mirrors [[agent-capability-route-pattern]] but uses operating-context improvement as the artifact instead of repo code.

## Applications to Jamie's crew

- **Pixoid** — orchestrator/reviewer; owns evidence grading, promotion decisions, issue closure, and scope control.
- **Boba** — explorer; evolves through source-quality, actionability, and no-delta silence feedback.
- **Quill** — scribe; evolves through vault/source-of-truth alignment, MOC routing, provenance, and bounded maintenance.
- **Tinker** — builder; evolves through implementation-readiness, verification discipline, GitHub/live-state reconciliation, and build/run pitfalls.

## Anti-patterns

- Treating self-improvement as model fine-tuning.
- Saving every run outcome to always-injected memory.
- Letting daily sensing become process theatre instead of artifact progress.
- Updating skills from one weak example.
- Creating new profiles because a task is interesting rather than because repeated evidence shows role overload.
- Repeating stale blockers or recommendations after live GitHub/Kanban state changed.
- Adding backlinks or notes just to make a graph look connected instead of improving routing.

## Related pages

- [[profile-memory-boundaries]] — where durable knowledge belongs, and how it relates to memory vs. project truth
- [[agent-capability-route-pattern]] — bounded trigger paths that this self-improvement system refines
- [[matt-pocock-sdlc-rhythm]] — the workflow rhythm that self-improvement loops verify and evolve