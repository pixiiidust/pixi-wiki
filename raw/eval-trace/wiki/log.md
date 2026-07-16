---
title: Eval Trace — Activity Log
created: 2026-06-16
updated: 2026-07-15
type: log
status: compiled
namespace: eval-trace
---

# Eval Trace — Activity Log

> Append-only namespace log.

## 2026-07-15 update | Extend style-transfer evaluation to tuned voice

- Added the LKY Voice parallel case to `wiki/concepts/style-transfer-evaluation.md`.
- Preserved separate gates for identity similarity, WER intelligibility, realtime factor, blind human preference, same-GPU placement, watermarking, and rollback.
- Recorded GPT-SoVITS as the counterexample where higher similarity did not compensate for failed intelligibility, and kept pronunciation/authenticity/factuality outside the claim.

## 2026-06-16 create | Namespace scaffold initialized

- Created README, CLAUDE instructions, raw folder, index/log, and typed wiki folders.
- Source routing comes from `Wiki Compiler Maps/Namespace Wiki Compiler Map.md`.
- No Daily Notes were copied or compiled.

## 2026-06-16 update | Pilot compiled namespace page

- Added pilot concept `wiki/concepts/context-overfitting.md` and crosslink to Agent Workflows Hermes Mission Control entity.
- Source pages remained in `Knowledge/` and `Projects/`.
- No Daily Notes were copied or compiled.

## 2026-06-16 update | Compile eval-trace content pack v1

- Expanded `wiki/concepts/context-overfitting.md`.
- Added entity `wiki/entities/eval-trace.md`.
- Added synthesis `wiki/syntheses/workflow-quality-evaluation-map.md`.
- Updated namespace index.
- Source pages remain in `Knowledge/` and `Projects/`.
- No Daily Notes were copied or compiled.

## 2026-06-18 update | Crosslink Hermes eval-adjacent imports

- Added cross-namespace pointer to the Hermes Agent external wiki import review for auxiliary-model and trace/eval-adjacent routing.
- No Daily Notes were copied or compiled.
## 2026-06-18 update | Refresh context-overfitting from local Hermes KB closure

- Refreshed `wiki/concepts/context-overfitting.md` with the verified YES/NO/UNSURE rubric and source-layer priority from the local Hermes KB tracker closure.
- Preserved the boundary that context-overfit checks do not bypass safety, approval, profile, cron, or deployment gates.

## 2026-07-10 add | Style-transfer evaluation contract from LKY Brain

- Added `wiki/concepts/style-transfer-evaluation.md` from the completed LKY Brain base/epoch-2/epoch-3 comparison.
- Preserved the strong parts: whole-document holdout, named behavior rubric, matched candidates, checkpoint preservation, and answer-level inspection.
- Tightened the claim boundary around n=24, 10 source documents, stochastic generation, one reference-anchored judge, no confidence intervals, and non-random longest-reference selection.
- Recorded the next gate: all 66 rows, fixed/repeated seeds, document-level uncertainty, blind/no-reference judging, and human calibration.
