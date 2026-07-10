---
title: LKY Brain Consumer-GPU QLoRA Case Study
created: 2026-07-10
updated: 2026-07-10
type: summary
status: compiled
namespace: local-ai-infrastructure
tags: [local-ai-infrastructure, qlora, consumer-gpu, wsl2, blackwell, reproducibility]
sources:
  - Projects/LKY Archive/Index.md
  - https://github.com/pixiiidust/lky-brain
confidence: high
---

# LKY Brain Consumer-GPU QLoRA Case Study

`lky-brain` demonstrates a complete Qwen3-14B QLoRA run on one RTX 5070 Ti 16GB GPU under WSL2 Ubuntu 24.04. The useful infrastructure lesson is not one magic config; it is how to isolate the actual failing layer and preserve a working evidence path.

## Successful run

- base: Qwen3-14B, non-thinking mode;
- quantization: 4-bit QLoRA;
- adapter: rank 64 / alpha 128 across linear projections;
- actual trainer: Unsloth;
- maximum sequence length: 2,048;
- assistant-turn-only loss;
- micro-batch 1, gradient accumulation 8;
- three epochs, final train loss 1.247;
- generation: plain Transformers + PEFT;
- judging: separate Claude API pass.

## Portability config vs executed config

The retained Axolotl YAML is not the executed evidence on this machine. It specifies 4,096 sequence length, packing, dropout 0.05, and in-loop eval. The successful Unsloth path used 2,048, `packing=False`, dropout 0.0, and no in-loop eval.

Agents should quote the executed script (`train/train_unsloth.py`) when describing the result and treat `train/lky-qlora.yml` as a portability candidate only.

## Failure isolation pattern

1. Probe raw CUDA allocation, matmul, dtype, and 4-bit load.
2. Reproduce a manual quantized LoRA train step.
3. Compare framework paths.
4. Disable the smallest failing optimization: varlen packing, pinned memory, or custom inference kernel.
5. Preserve diagnostic scripts and working launchers.
6. Decouple GPU generation from API judging.
7. Save intermediate checkpoints because post-hoc quality may peak before final train loss.

## Environment-specific findings

On this WSL2 + Blackwell stack:

- Axolotl crashed during model loading even when plain Transformers/bitsandbytes worked.
- Unsloth import order mattered because it patches TRL/Transformers.
- Triton required a C compiler.
- packed/varlen attention crashed; dense non-packed training worked.
- pinned-memory loading and Unsloth's Qwen3 inference kernel were avoided.

These are verified for this run, not universal prescriptions for every GPU, WSL version, or future package release.

## Portable use and serving path

The public-readability refresh at repo commit `da490f6` replaced machine-specific checkout paths in the setup, training, generation, and upload launchers with paths derived from each script's location.

The repo now documents two downstream paths:

- **Quick local inference:** load Qwen3-14B in 4-bit with Transformers/bitsandbytes, attach `sjsim/lky-qlora` through PEFT, and run with about 16GB VRAM.
- **OpenAI-compatible serving:** run vLLM with LoRA enabled, register the adapter as `lky`, keep maximum LoRA rank at 64, and disable Qwen3 thinking in request metadata.

The serving guide estimates about 28GB for the full-precision 14B base and points readers toward a 40GB card, or a 24GB card with quantization. These examples make the project easier to try and integrate, but they were not executed as part of this VPS review and should not be promoted to verified serving evidence yet.

## Evidence boundary

The repo has no CI or unit-test suite for the data/training pipeline, and the generated datasets/checkpoints are intentionally gitignored. The `uv.lock` covers the data-pipeline environment, but the version-sensitive Unsloth/TRL/Transformers/PEFT/Torch/bitsandbytes training stack is installed separately without exact pins. Reproducibility therefore depends on live sources, external model artifacts, package resolution, and operator-run hydration/training steps. The portable shell paths reduce checkout-specific friction but do not solve dependency or artifact reproducibility. Add training locks, manifests, hashes, schema versions, a small CPU-only pipeline fixture, and GPU smoke checks for the documented inference/serving paths before calling the template fully reproducible.
