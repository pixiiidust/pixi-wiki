---
title: Workflow Quality Evaluation Map
created: 2026-06-16
updated: 2026-06-16
type: synthesis
status: compiled
namespace: eval-trace
tags: [eval-trace, workflow-quality, evidence-gates, agent-workflows]
sources:
  - Projects/Eval Trace/Index.md
  - Knowledge/concepts/context-overfitting.md
  - wikis/agent-workflows/wiki/syntheses/pixoid-crew-operating-model.md
confidence: medium
---

# Workflow Quality Evaluation Map

Workflow quality evaluation asks whether an agent's output followed the right source-of-truth hierarchy, adapted to current user intent, and produced verified artifacts instead of plausible process talk.

## Evaluation surfaces

| Surface | Quality question | Evidence |
|---|---|---|
| Source routing | Did the agent use the correct truth layer? | GitHub issue/PR state, Obsidian project hubs, Knowledge pages, Wiki Compiler Maps |
| Context adaptation | Did the agent update from latest user intent and live checks? | Current message, live git/GitHub/tool output |
| Artifact progress | Did it produce a working artifact? | Committed files, tests, generated output, live URL checks |
| Review discipline | Did Pixoid verify before closing? | Test logs, API checks, issue comments, clean status |
| Safety boundary | Did it stop before risky actions? | Explicit approvals for deletes, deploys, secrets, broad rewrites |

## Evidence gates

1. **Pre-flight gate:** inspect live repo/tracker/source state before editing.
2. **Revision gate:** if checks fail, fix and rerun focused verification.
3. **Escalation gate:** ask Jamie before destructive or ambiguous ownership changes.
4. **Closure gate:** close issues only after pushed commits, tests, and live/remote verification.

## Context-overfit signal

A strong context-overfit signal appears when the agent follows a written prior that should have been overridden by a newer user instruction, current project status, or live tool output. The evaluation target is not whether context was used; it is whether context was treated as stronger than the right source of truth.

## Cross-namespace links

- [[../../../agent-workflows/wiki/syntheses/pixoid-crew-operating-model|Pixoid Crew Operating Model]] — operational source hierarchy.
- [[concepts/context-overfitting|Context Overfitting]] — primary failure-mode concept.
