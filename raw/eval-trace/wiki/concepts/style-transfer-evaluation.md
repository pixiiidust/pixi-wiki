---
title: Style-Transfer Evaluation
created: 2026-07-10
updated: 2026-07-15
type: concept
status: compiled
namespace: eval-trace
tags: [eval-trace, style-transfer, lora, llm-judge, checkpoint-selection, uncertainty, voice-ai]
sources:
  - Knowledge/concepts/style-transfer-evaluation.md
  - Projects/LKY Archive/Index.md
  - Projects/LKY Avatar/Index.md
  - https://github.com/pixiiidust/lky-brain
  - https://pixiiidust.github.io/lora-LKY-report/
confidence: high
---

# Style-Transfer Evaluation

Style-transfer evaluation asks whether an adapter changes named observable behaviors on held-out prompts without confusing persona imitation, lower train loss, or one judge's preference with general reasoning improvement.

## Minimum contract

1. Split by whole source document before creating overlapping windows.
2. Compare base and candidate checkpoints on the same prompts and decoding settings.
3. Score explicit observable traits plus a separate overall voice/style measure.
4. Use deterministic generation or repeated fixed seeds.
5. Blind candidate identity and randomize answer order.
6. Run both reference-free and reference-anchored judge passes when a real answer exists.
7. Calibrate with human review.
8. Aggregate or bootstrap by held-out document, not only by prompt row.

## LKY Brain result

On 24 rows from 10 held-out interviews, the epoch-2 QLoRA checkpoint moved judged behavior relative to base Qwen3-14B:

- voice: 2.04 → 2.88;
- directness: 46% → 88%;
- bounded uncertainty: 8% → 33%;
- concrete analogy: 0% → 25%;
- reframing: 29% → 38%.

Epoch 3 reached voice 2.96 and analogy 38%, but lower reframing and bounded uncertainty. Epoch 2 is a defensible provisional checkpoint preference because it retains the subtler traits while tying on broad voice within likely noise.

## Parallel speech-style evaluation

The LKY Voice run applies the same evidence discipline to speech generation, where identity, intelligibility, deployment speed, and human recognition must remain separate:

| gate | contract | winning Chatterbox LoRA e14 |
|---|---|---:|
| speaker similarity | meet or beat baseline 0.8693 | 0.8900 |
| intelligibility | WER ≤ 0.05 | 0.0390 |
| deployability | RTF ≤ 0.6 | 0.381 |
| human blind listen | tuned preferred ≥ 70% | 18/20 |
| integrated placement | no failures; realtime on the shared GPU | RTF mean/max 0.369/0.397; 0 failures |

The rejected GPT-SoVITS arm is the useful counterexample: similarity improved to 0.9049, but WER degraded to 0.1274. The operator's blind listen can veto a numerically attractive model; no one metric decides shipment.

Integration also preserved a stock-model rollback and PerTh watermark confidence 1.0000. These results support a tuned-voice preference and deployment decision, not authentic speech, semantic correctness, factual fidelity, or robust pronunciation. Singapore proper nouns and mixed acoustic eras remain separate residual risks.

## Claim boundary

The evidence supports a directional behavioral shift. It does not yet establish statistically stable per-trait lift, factual fidelity, general capability gain, or definitive overfitting because:

- the 24 rows are the longest-reference subset of 66 windows rather than a representative random sample;
- generation sampled at temperature 0.8 without reported fixed/repeated seeds;
- those rows are clustered within 10 source documents;
- the same held-out subset selects the checkpoint and reports the final result;
- one Claude judge sees a real LKY reference answer;
- no confidence intervals, judge-reliability study, or human agreement rate is reported.

## Next evidence gate

Evaluate all 66 rows with fixed or repeated seeds, separate checkpoint selection from final testing, publish document-level aggregates and confidence intervals, add a blind/no-reference judge pass, manually review a stratified sample, and check same-event/date leakage across the dialogue and speech streams. Phrase epoch-3 as a possible overfit signal until those checks agree.
