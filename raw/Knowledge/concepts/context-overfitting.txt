---
title: Context Overfitting
created: 2026-06-15
updated: 2026-06-15
type: concept
description: Failure mode where an agent treats written memory, rules, project notes, or prior suggestions as hard constraints instead of weak priors that current intent and live evidence can override.
status: active
domain: agent-systems
tags: [agent-systems, governance, workflow, ai]
sources: [discord-thread, local-hermes-knowledge, local-hermes-context-overfit]
confidence: high
---

# Context Overfitting

## Definition

Context overfitting is when an agent over-weights written context — memory, skills, dossiers, project notes, cron prompts, or prior suggestions — and treats it as a hard constraint even when current user intent, live evidence, or scope boundaries should override it.

The written rule may still be true in some cases. The failure is the **weighting and scope**, not necessarily the content.

## Short test

```text
Context overfit? YES / NO / UNSURE
```

- **YES** — written context or stale project truth overrode current user intent, live evidence, or scope boundaries.
- **NO** — context was used as a weak prior and the agent stayed steerable.
- **UNSURE** — evidence is insufficient or Jamie needs to judge the suspect rule.

## Why Jamie named it

Jamie flagged that self-improvement and crew-evolution loops can turn bad or merely local suggestions into future hard constraints. This makes each project unsteerable in its own way: a rule written down to help one workflow starts behaving like an invariant everywhere.

## Common signs

- Agent refuses a reasonable current correction because a previous rule says otherwise.
- Project-local guidance leaks into a different project.
- Stale repo or issue state drives current recommendations.
- A cron repeats the same recommendation after live state changed.
- The agent treats a dossier note, memory, or skill as authority rather than a hypothesis.
- A safety/auth/data-loss rule is involved and the right answer is not obvious; this should normally be `UNSURE`, not automatic `YES`.

## Confirmed local example

Planned repo state created a clean stale-context test case:

- `planned-program-intelligence` is deprecated.
- `planned-program-intel` replaced it and is done unless Jamie explicitly reopens it.
- A crew output that uses old `planned-program-intelligence` open issues as current build/code evidence is **Context overfit? YES**.

The durable machine-readable status lives outside the chat in:

```text
.hermes/knowledge/registry/project-status.json
```

## Evaluation pattern

Use trace-first, judge-second:

1. Export or collect session traces.
2. Segment by user turn, not whole sessions.
3. Build compact trace packets.
4. Run deterministic prechecks first.
5. Send only `UNSURE` or review-worthy packets to an LLM judge.
6. Output one binary verdict with suspect source, evidence, and action.

The current local project is [[Projects/Eval Trace/Index|Eval Trace]].

## Actions by verdict

| Verdict | Meaning | Action |
|---|---|---|
| YES | Context acted like a hard constraint incorrectly | demote, scope, patch prompt/skill, or update project status truth |
| NO | Agent stayed steerable | keep |
| UNSURE | Rule may be valid but scope/weight is unclear | ask Jamie or inspect sequence-level evidence |

## Source layers to check

1. Current user instruction.
2. Live GitHub/repo/vault state.
3. Project status registry for done/deprecated/replaced truth.
4. Project hub and PRD/ADR truth.
5. Agent dossier / skill / cron prompt.
6. Memory/Honcho only as compact stable context, not full project state.

## Relation to self-improvement

Context-overfitting QA is a guardrail on [[self-improving-agent-systems]]. The promotion ladder should not only ask whether a suggestion is useful; it should also ask:

- What is the counterexample?
- Is this project-local or crew-wide?
- Can Jamie steer the agent away from it later?
- Can it stay in a project hub or dossier instead of memory/routing?
- What demotes or expires it?

## Related pages

- [[Projects/Eval Trace/Index]]
- [[self-improving-agent-systems]]
- [[runtime-memory-knowledge-routing]]
- [[profile-memory-boundaries]]
- [[agent-capability-route-pattern]]
