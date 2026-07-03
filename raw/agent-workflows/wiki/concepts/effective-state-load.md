---
title: Effective State Load
created: 2026-07-03
updated: 2026-07-03
type: concept
status: compiled
namespace: agent-workflows
source: Knowledge/concepts/effective-state-load.md
confidence: medium
---

# Effective State Load

**Effective State Load** is a practical metric for estimating when an LLM agent is carrying too much structured state to keep its world model reliable.

Current first-test hypothesis:

```txt
ESL = SC × DD
```

- `SC`: state cardinality — live entities/state variables the agent must keep jointly addressable.
- `DD`: dependency density — preconditions or constraints that must hold at once.

The project first measures the two-dimensional SC/DD collapse surface, then tests whether `SC × DD` compresses that surface well enough to guide task slicing.

## Why this matters

Context length says what an agent can see. Effective State Load asks what the model-agent harness can **hold correctly**: live, mutually dependent state that must survive updates across a long-horizon task.

The key failure mode is fluent reasoning over a corrupted world model. The official paper frames SC and DD as governing control parameters, task success as the order parameter, and world-state fidelity as the precursor signal. ESL is the orchestration-facing attempt to turn that boundary into a usable state-load budget.

## Experiment shape

The current repo reuses the official `Hik289/world-model-collapse` implementation rather than starting from a custom ToolDAG simulator.

### Phase 1 — Measure the SC/DD surface

Run `stateful_puzzle` through OpenRouter and collect:

- final success,
- world-state accuracy,
- action validity,
- collapse onset (`tau_w`, `tau_a`, lag),
- token and cost telemetry,
- sample traces where world-state failure precedes invalid action.

### Phase 2 — Test simple ESL

Evaluate whether:

- equal-ESL cells such as `(SC=5, DD=4)`, `(SC=10, DD=2)`, and `(SC=20, DD=1)` behave similarly,
- collapse cliffs follow constant `SC × DD` contour lines,
- `SC × DD` predicts collapse better than SC alone, DD alone, token count, or `SC + DD`.

Fallback only if simple ESL fails:

```txt
ESL_weighted = SC^a × DD^b
```

### Phase 3 — Transfer to ToolDAG

After StatefulPuzzle works, reuse the official repo's `tool_dag` environment to test whether `ESL = SC × DD` transfers to typed tool-use workflows.

## Orchestration implication

If ESL boundaries can be measured per model-agent harness, a runtime orchestrator can ingest a task spec, estimate ESL, and slice work into state-machine/statechart stages below the safe boundary.

Statechart guards can enforce:

- split again when `slice_ESL` exceeds safe budget,
- re-ground when state fidelity drops,
- require human review for high-risk transitions,
- continue only after verifier-backed state updates.

## Related pages

- [[agent-tooling-plan]]
- [[world-model-control-surfaces]]
- [[self-improving-agent-systems]]
- [[context-overfitting]]
- [[visual-plan-review-surfaces]]
