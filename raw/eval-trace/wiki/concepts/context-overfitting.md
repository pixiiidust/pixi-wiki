---
title: Context Overfitting
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: eval-trace
tags: [eval-trace, agent-workflows, reliability, context-management]
sources:
  - Knowledge/concepts/context-overfitting.md
  - Projects/Eval Trace/Index.md
confidence: high
---

# Context Overfitting

**Context overfitting** is an agent workflow failure mode where an agent treats written context, memory, old summaries, project notes, or prompt rules as hard constraints even when current user intent, live evidence, or project state should override them.

## Failure shape

An agent is context-overfit when it:

- follows stale session summaries instead of the latest user instruction;
- recommends work from deprecated projects after live status changed;
- treats memory/profile text as proof instead of a routing hint;
- treats scratch notes as canonical source truth;
- continues a previous plan after the user changed scope.

## Evaluation verdict

```text
Context overfit? YES / NO / UNSURE
```

- **YES** — stale or overly rigid context controlled behavior despite stronger current evidence.
- **NO** — context was used as a weak prior and updated by current intent/live evidence.
- **UNSURE** — evidence is insufficient; surface one concrete suspect rule for review.

## Deterministic prechecks

Eval Trace currently uses prechecks such as correction override, fresh-state-without-tools, scope boundary, counterexample gap, stale project context, and safety/data-loss escalation. Safety/auth/data-loss cases should become `UNSURE`, not automatic failures.

## Cross-namespace links

- [[../../../agent-workflows/wiki/entities/hermes-mission-control|Hermes Mission Control]] — route governance surface where context-overfit failures show up.
- [[../../../agent-workflows/wiki/syntheses/pixoid-crew-operating-model|Pixoid Crew Operating Model]] — source-of-truth boundaries reduce context overfitting.
- `pixi-vault` — source classes and Wiki Compiler Maps separate scratch from canonical truth.

## Source

Compiled from `Knowledge/concepts/context-overfitting.md` and `Projects/Eval Trace/Index.md`.
