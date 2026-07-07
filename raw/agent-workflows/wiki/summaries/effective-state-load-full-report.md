---
title: Effective State Load Full Report
created: 2026-07-05
updated: 2026-07-07
type: summaries
status: compiled
namespace: agent-workflows
source: effective-state-load/docs/reports/esl-full-report.html
confidence: high
---

# Effective State Load Full Report

This page routes to the full ESL project report compiled from `pixiiidust/effective-state-load` after Phase 3 completed.

## Read directly

- [Open the standalone HTML report](/pixi-wiki/wiki/agent-workflows/assets/reports/esl-full-report.html)
- [Download the PDF](/pixi-wiki/wiki/agent-workflows/assets/reports/esl-full-report.pdf)

## What the report covers

- Problem: long-horizon agents fail when their internal workflow state drifts from reality, not only when context windows fill.
- Method: stress one model-agent harness across state cardinality (SC) and dependency density (DD).
- Phase 1: StatefulPuzzle shows an SC-led state wall.
- Phase 2: simple `SC × DD` is only partially useful in StatefulPuzzle; weighted calibration ties token count.
- Phase 3: ToolDAG-B shows a DD/provenance-led coupling cliff, where simple `SC × DD` beats token count and separates pass/fail cells cleanly.
- Verdict: ESL is a metric family and measurement recipe, not a portable universal formula.
- Product path: start with provenance guardrails for agent writes, then use the same graph for capacity/load measurement.

## Short verdict

There is no universal ESL exponent or threshold to ship. What transfers is the operating method: define SC/DD for a workflow class, run a cheap calibration grid, map the collapse frontier, operate with margin, and use provenance/binding errors as leading indicators.

## Product one-liner

> Schema validation checks that an ID is valid. Provenance guardrails check that it is the right ID for this task; ESL uses the same provenance graph to learn how much state/dependency load each workflow can safely carry.

## Implementation bridge

The follow-on MVP is a shadow-mode provenance auditor: replay traces, build the entity provenance graph, flag wrong-object/stale/scope-mismatched writes, and score the checker against hidden ToolDAG-B labels before running real traces.

## Related page

- [[../concepts/effective-state-load|Effective State Load]]
