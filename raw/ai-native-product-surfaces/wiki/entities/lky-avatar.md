---
title: LKY Avatar / Voice Persona Stack
created: 2026-07-15
updated: 2026-07-15
type: entity
status: working-demo
namespace: ai-native-product-surfaces
tags: [ai-native-product-surfaces, voice-ai, avatar, local-ai, evaluation]
sources:
  - Projects/LKY Avatar/Index.md
  - Projects/LKY Archive/Index.md
  - https://github.com/pixiiidust/lky-brain
confidence: high
---

# LKY Avatar / Voice Persona Stack

LKY Avatar is a working local fictional-interview product that turns the `lky-brain` reasoning-style adapter into a voice-first, interruptible experience with an animated elderly-statesman portrait, a tuned watermarked voice, and a transcript designed as the record of proceedings.

It is a separate applied product from the completed [[../../curated-tuning-datasets/wiki/entities/lky-archive|LKY Brain / LKY Archive]] corpus-and-adapter case study. The brain supplies the reasoning-style model; the avatar product owns the interaction, serving, disclosure, failure handling, and public-experience gates. The source avatar and voice-training repos are private. This page records a public-safe system summary, not private launch instructions.

## Product frame

```text
speak or type a question
  -> streaming transcription
  -> local LKY-style language model
  -> fine-tuned elder voice
  -> animated portrait + spoken reply
  -> transcript/export as inspectable record
```

The web surface uses a broadcast-interview hierarchy rather than a generic chat layout:

- portrait stage and session-state lamp;
- persistent fictional-AI disclosure;
- `TRANSCRIPT OF RECORD` for spoken and written turns;
- voice input, typed-note fallback, and free interruption;
- transcript export, visible reset, and explicit busy/rate-limit states;
- text-only continuation when voice synthesis is unavailable.

The current default avatar is a bundled illustrated elderly-statesman portrait sprite with state-mapped expressions, mouth motion, blink, and breathing. It replaced an earlier anime placeholder. A separate Live2D path remains for a future full custom rig.

## Architecture

- LiveKit Cloud carries realtime rooms and WebRTC media.
- Deepgram provides streaming speech-to-text.
- A Python voice agent owns persona prompting, history, interruption, TTS state, and degraded text delivery.
- The brain is a merged epoch-2 `lky-brain` LoRA served as Q4_K_M GGUF through llama.cpp behind an OpenAI-compatible seam.
- The voice is a Chatterbox t3 model with a merged rank-16 LoRA overlay, served through a loopback-only HTTP adapter.
- A Vite/TypeScript client renders the interview surface and keeps transcript export client-side.
- A small token server mints short-lived room tokens and enforces unique rooms, one active session, and per-IP limits.

## Evidence gates reached

### Brain and interaction

- Warm brain decode: 80.5 tok/s p50; warm time to first token about 0.05 s.
- End-of-speech to first audio: 3.96 s p50, 5.95 s worst observed over 10 live turns.
- Agent-side playback stops about 18–21 ms after interruption detection; about 270 ms from raw speech onset including the deliberate detection window.
- Thirty-minute soak: 37/37 turns with no failures.

### Fine-tuned voice

The voice-training project compared two arms against a frozen Chatterbox baseline:

| arm | blind preference | similarity | WER | outcome |
|---|---:|---:|---:|---|
| baseline | 2/20 in final LoRA pack | 0.8693 | 0.0324 | retained rollback |
| GPT-SoVITS | 13/20 tuned | 0.9049 | 0.1274 | failed intelligibility gate |
| **Chatterbox LoRA epoch 14** | **18/20 tuned** | **0.8900** | **0.0390** | **integrated** |

The integrated voice kept the existing HTTP contract, passed a ten-turn same-GPU placement run at RTF mean 0.369 / max 0.397 with zero failures, and preserved Chatterbox's PerTh watermark at confidence 1.0000 on served output.

## Trust and honesty boundary

- This is a fictional simulation. Generated answers are not authentic quotations and the portrait is illustrative, not an authentic photo or endorsement.
- The style adapter is not a factual database. Live testing found invented constituencies, dates, and historical events. Fact grounding is now the main quality gate.
- Voice data and weights remain local. The generated audio stays watermarked.
- Singapore proper nouns remain a weak point across STT and TTS. The tuned voice improved identity and pacing but did not solve out-of-vocabulary pronunciation.
- The demo is not publicly deployed as of 2026-07-15. Home-GPU hosting is a measured recommendation, not a verified live service.

## Next gate

Add a small audited fact sheet, retrieve relevant sections into each turn, guard against invented specifics, boost Singapore proper nouns in STT/TTS, and evaluate factual accuracy separately from persona quality. Only after that trust gate passes should the project choose between the full Live2D rig and public hosting.

## Related

- [[../../curated-tuning-datasets/wiki/entities/lky-archive|LKY Brain / LKY Archive]]
- [[../../local-ai-infrastructure/wiki/summaries/lky-brain-consumer-gpu-qlora|LKY Brain Consumer-GPU QLoRA Case Study]]
- [[concepts/material-loop-and-glass-interfaces|Material Loop and Glass Interfaces]]
- [[concepts/interaction-mode-routing|Interaction Mode Routing]]
