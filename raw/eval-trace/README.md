---
title: Eval Trace
created: 2026-06-16
updated: 2026-07-17
type: namespace-overview
status: active
category: evaluation
namespace: eval-trace
confidence: high
---

# Eval Trace

> Active namespace for evidence quality, behavior/workflow evaluation, reliability, and claim boundaries.

## Scope

### Covers

Workflow, agent, and model-behavior evaluation; traces; context-overfitting detection; reliability metrics; evidence gates; style-transfer checks; and quality read-outs.

### Not Covered

General observability unrelated to behavior/workflow quality; product analytics unless used as an evaluation surface; model-training infrastructure except where it changes the evaluation contract.

### Current As

2026-07-17 — active. Includes context-overfitting, the Eval Trace prototype, workflow-quality mapping, LLM style-transfer evaluation, the LKY Voice objective-plus-blind-listening gate, and the LKY Avatar factual-accuracy/persona-quality/fabrication separation.

## Canonical Source Roots

- `Projects/Eval Trace/Index.md`
- `Knowledge/concepts/context-overfitting.md`
- `Knowledge/concepts/style-transfer-evaluation.md`
- `Projects/LKY Avatar/Index.md`

## Crosslinks

- [[../agent-workflows/README|agent-workflows]]
- [[../pixi-vault/README|pixi-vault]]
- [[../ai-native-product-surfaces/README|ai-native-product-surfaces]]
- [[../local-ai-infrastructure/README|local-ai-infrastructure]]

## Public Output Contract

When published to `pixi-wiki`, this namespace should expose:

```text
/raw/eval-trace/README.md
/raw/eval-trace/wiki/index.md
/wiki/eval-trace/README.md
/wiki/eval-trace/wiki/index.md
```

## Maintenance

- Edit canonical source notes first.
- Use `Wiki Compiler Maps/Namespace Wiki Compiler Map.md` for routing decisions.
- Do not compile Daily Notes directly unless promoted or verified.
