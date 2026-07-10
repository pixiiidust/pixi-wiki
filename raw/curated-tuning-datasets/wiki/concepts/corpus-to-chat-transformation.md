---
title: Corpus-to-Chat Transformation
created: 2026-07-10
updated: 2026-07-10
type: concept
status: compiled
namespace: curated-tuning-datasets
tags: [curated-tuning-datasets, corpus-curation, instruction-backtranslation, temporal-persona]
sources:
  - Knowledge/concepts/corpus-to-chat-transformation.md
  - Projects/LKY Archive/Index.md
confidence: high
---

# Corpus-to-Chat Transformation

A corpus-to-chat transformation converts real dialogue and monologic source material into supervised chat rows while preserving which text is observed, which text is synthetic, which speaker is the loss target, and which temporal context conditions each answer.

## Two-stream contract

### Real dialogue

- Parse and validate speaker attribution.
- Preserve bounded multi-turn windows.
- Train only on the target speaker's assistant turns.
- Hold out whole documents before creating overlapping windows.

### Monologic speeches

- Clean and paragraph-chunk real passages deterministically.
- Generate one project-owned question that the passage directly answers.
- Keep the source passage as the answer; do not synthesize the expert's response.
- Store source ID, normalized-passage hash, date/title, and generation provenance.

The reusable instruction-backtranslation rule is: **synthesize the prompt, not the expert's answer**.

## Temporal conditioning

Put normalized date, role/title, and setting in the system prompt when a speaker's role and views evolve over time. The mapping must be inspectable and malformed dates must fail or normalize explicitly. Temporal context is a label, not proof of historical fidelity.

## LKY Brain instance

- 1,142 interview/press-conference windows;
- 2,895 speech passages with synthetic questions;
- 404 generic-instruction rows;
- 4,441 total training rows;
- 66 windows from 10 whole held-out interviews.

Qwen3 non-thinking mode and assistant-turn-only loss keep the objective on visible LKY-style answers rather than interviewer text or hidden scratchpad behavior.

## Main risks

- stale questions silently rejoining shifted chunks;
- generator-model framing bias in synthetic questions;
- same-event/date leakage across dialogue and speech streams;
- interview-only holdout coverage;
- title/speaker attribution and translation errors;
- style transfer being mistaken for belief or factual fidelity.

Hash-bound joins, explicit stream provenance, document-level splits, cross-stream leakage checks, and the `eval-trace` evidence contract are required before strong generalization claims.
