---
title: Eval Trace
created: 2026-06-16
updated: 2026-06-16
type: entity
status: compiled
namespace: eval-trace
tags: [eval-trace, agent-workflows, evaluation, traces]
sources:
  - Projects/Eval Trace/Index.md
confidence: medium
---

# Eval Trace

**Eval Trace** is Jamie's local prototype for evaluating agent-workflow quality, especially context overfitting. It builds trace packets, runs deterministic prechecks, and can hand ambiguous cases to an LLM judge.

## Current artifact

```text
.hermes/context-overfit/
```

Current status: local prototype. It is not yet a public GitHub repo. The repo decision is deferred until the harness proves review-load reduction on real workflow traces.

## Current capabilities

- Builds segmented trace packets from Hermes session exports.
- Runs deterministic prechecks before any LLM judge.
- Emits compact `judge_packets.jsonl` for reviewable `UNSURE` cases.
- Supports real LLM judge passes when Jamie asks Pixoid to judge.
- Reads `.hermes/knowledge/registry/project-status.json` for done/deprecated/replaced project status.

## Next gate

Before a standalone `pixiiidust/eval-trace` repo exists, prove value on real workflow traces: add sequence-level cron checks, run on recent crew outputs, and show a confirmed real `YES` or useful `UNSURE` clustering.

## Source

Compiled from `Projects/Eval Trace/Index.md`.
