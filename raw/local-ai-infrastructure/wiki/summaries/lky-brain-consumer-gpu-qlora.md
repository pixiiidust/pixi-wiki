---
title: LKY Brain Consumer-GPU QLoRA Case Study
created: 2026-07-10
updated: 2026-07-17
type: summary
status: compiled
namespace: local-ai-infrastructure
tags: [local-ai-infrastructure, qlora, consumer-gpu, wsl2, blackwell, reproducibility, llama-cpp, voice-ai]
sources:
  - Projects/LKY Archive/Index.md
  - Projects/LKY Avatar/Index.md
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

## Interactive chat path and sampling correction

Repo commit `3a9f6a5` added a streaming Transformers + PEFT chat REPL with conversation history, `/date` era switching, and `/reset`. The documented interactive defaults are temperature 0.7 with repetition penalty 1.1 after temperature 0.8 without a penalty produced degenerate loops in field use.

This is an executed local interaction path, not evidence for the unexecuted vLLM example. It also does not rewrite the historical n=24 style-evaluation contract, which used its original stochastic generation settings.

## Executed downstream serving in LKY Avatar

The separate `lky-avatar` product has now executed a different serving route on the same RTX 5070 Ti:

- merge the published epoch-2 LoRA into Qwen3-14B;
- quantize the merged model to Q4_K_M GGUF;
- serve through llama.cpp's OpenAI-compatible `llama-server`;
- use the same client seam as the slower 4-bit Transformers + PEFT fallback.

Measured warm brain performance was 80.5 tok/s p50 decode and about 0.05 s time to first token. The brain plus the fine-tuned Chatterbox voice then completed a ten-turn same-GPU placement run with zero failures; TTS RTF mean/max was 0.369/0.397 and total-card VRAM peaked at 15,813 MiB of 16,303 MiB.

This verifies one local product-serving path. It does not validate the README's vLLM example, establish multi-user serving capacity, or make the style adapter factually reliable. Live use exposed confident biography/date/place hallucinations.

The application layer now adds a small audited fact sheet, deterministic section retrieval per turn, a source-over-memory and uncertainty block immediately before the latest question, and Singapore proper-noun input boosts without changing llama-server. A 12-question eval separates factual accuracy, persona quality, and fabrication and supports matched grounding-on/off runs.

Repository verification passed 148 root tests and 199 voice-agent tests with 3 live-service skips. That proves the retrieval, prompt, config, STT-construction, and eval seams as code; it does not prove the model-quality lift. Real-microphone STT and a local-brain grounding-on/off run remain the acceptance evidence.

## Evidence boundary

The repo has no CI or unit-test suite for the data/training pipeline, and the generated datasets/checkpoints are intentionally gitignored. The `uv.lock` covers the data-pipeline environment, but the version-sensitive Unsloth/TRL/Transformers/PEFT/Torch/bitsandbytes training stack is installed separately without exact pins. Reproducibility therefore depends on live sources, external model artifacts, package resolution, and operator-run hydration/training steps. The portable shell paths reduce checkout-specific friction but do not solve dependency or artifact reproducibility. Add training locks, manifests, hashes, schema versions, a small CPU-only pipeline fixture, and GPU smoke checks for the documented inference/serving paths before calling the template fully reproducible.
