---
title: Effective State Load
created: 2026-07-03
updated: 2026-07-05
type: concept
status: compiled
namespace: agent-workflows
source: Knowledge/concepts/effective-state-load.md
confidence: high
---

# Effective State Load

**Effective State Load (ESL)** is workflow-specific load testing for LLM agents: define state/dependency load for a workflow, map where the model-agent harness loses track of reality, then keep future runs inside the safe operating band.

```txt
SC = state cardinality   # live things the agent must track
DD = dependency density  # simultaneous bindings/preconditions per action
ESL = SC × DD            # metric family; not a universal threshold/formula
```

## Current verdict

`ESL = SC × DD` is **environment-general as a metric family and measurement recipe, not as a portable formula**.

The durable recipe is:

```txt
cheap grid → SC/DD surface → calibrated frontier → operating margin → routing/guardrails
```

Boundary location and axis weights are workload-specific. The useful answer is not “one formula ships in a library”; it is “calibrate the collapse frontier for this model/tool/workflow setup.”

## Evidence summary

### Phase 1 — StatefulPuzzle

- 240 deduped episodes over SC `{5,10,15,20,25,40}` × DD `{1,2,4,6}`.
- StatefulPuzzle is SC-dominant: SC=40 collapses even at DD=1.
- Weighted fallback after simple ESL underperformed: **SC¹ × DD^0.48**.
- Token count was a tough baseline: calibrated ESL Spearman 0.858 vs token count 0.857.

### Phase 3 — ToolDAG-B

- 160 transfer-grid episodes after a 60-episode gate PASS.
- ToolDAG-B tests provenance-checked binding: right type is not enough; the variable/object must come from the correct producer.
- Surface is binary-sharp: every cell is 10/10 or 0/10.
- Dominant axis flips: SC=40 DD=1 passes 10/10; SC=20 DD=4 and SC=40 DD=2 fail 0/10.
- Simple `SC × DD` is the top predictor here: Spearman 0.810 vs token count 0.804, with perfect label separation at ESL≤60 pass / ESL≥80 fail.
- Failure mode: 2,655 wrong-provenance/binding errors vs 1 parse error in 2,811 steps.

## What “world-model collapse” means

The agent can still produce fluent, valid-looking output, but its internal picture of the workflow state has drifted from reality. In production this can show up as:

- valid customer ID, wrong customer;
- valid file path, wrong file;
- valid ticket ID, wrong ticket;
- stale tool output treated as fresh;
- a write action whose arguments came from mismatched upstream contexts.

## Measuring SC/DD in practice

There are three practical scenarios:

1. **Count** from a system of record when objects and rules are already structured: CRM, ERP, PLM, data lineage, ticketing, cloud graphs.
2. **Measure** through tool middleware when every tool call and object ID passes through an interception layer. SC is active provenance nodes; DD is required correct bindings per action.
3. **Estimate** for plain-language tasks using a plan DAG, cheap classifier, or historical template, then correct with realized runtime load.

The key rule: SC/DD units can be arbitrary, but they must be counted the same way during calibration and runtime sizing.

## Product implication

The first product wedge is **object-provenance verification for AI-agent writes**, not a standalone metric dashboard.

> Schema validation checks that it is a customer ID. Provenance guardrails check that it is the right customer for this task.

The same provenance graph then becomes the ESL measurement instrument: it can block or flag wrong-object writes today, then learn which workflows can safely reduce human review or need slicing/routing tomorrow.

## Full report

- [Read the full ESL report as a standalone HTML artifact](/pixi-wiki/wiki/agent-workflows/assets/reports/esl-full-report.html)
- [Download the PDF](/pixi-wiki/wiki/agent-workflows/assets/reports/esl-full-report.pdf)
- [[../summaries/effective-state-load-full-report|Report summary and reading guide]]

## Related pages

- [[agent-tooling-plan]]
- [[world-model-control-surfaces]]
- [[self-improving-agent-systems]]
- [[context-overfitting]]
- [[visual-plan-review-surfaces]]
