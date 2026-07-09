---
title: J-Space as Global Workspace
created: 2026-07-08
updated: 2026-07-08
type: concept
status: active
namespace: ai-native-product-surfaces
source: Knowledge/concepts/j-space-global-workspace.md
confidence: medium
---
# J-Space as Global Workspace

J-space is Anthropic's name for the model-internal subspace spanned by Jacobian lens vectors: directions in a language model's residual stream that make a token more likely to be verbalized now or later.

The paper argues that this verbalizable subspace behaves like a **functional global workspace**: content written there can be reported, modulated, used in flexible reasoning, and broadcast to downstream computations. This is a functional claim about accessible representations, not a claim about subjective consciousness.

## Product translation

```text
model activation at a position/layer
  -> project onto J-lens directions
  -> read token/concept directions with high activation
  -> inspect what is available for verbal report or downstream use
  -> optionally intervene to test whether the representation is causal
```

The useful product idea is not "read model thoughts." The useful idea is: **replay what a model is poised to verbalize so humans can inspect intermediate, silent, or weakly expressed content before trusting the answer.**

## What the paper claims

Anthropic reports that J-space has the cluster of properties associated with global workspace theory:

- **Verbal report:** J-lens readouts track what the model will say, and interventions can change reports.
- **Directed modulation:** instructed mental content can appear in J-lens readouts even while the surface output is unrelated.
- **Internal reasoning:** unspoken intermediates can appear in J-space and be causally load-bearing.
- **Flexible generalization / broadcast:** one J-space vector can feed many downstream functions.
- **Selective mediation:** flexible explicit tasks depend on J-space more than routine automatic processing.
- **Structural support:** model components appear arranged to read, write, amplify, and broadcast J-space content.

## Alignment-auditing relevance

The paper applies J-lens readouts to cases where silent strategic or situational assessments appear in J-space before or without appearing in the model output. This makes J-space a promising review surface for evaluation awareness, prompt-injection recognition, self-monitoring, or hidden objective signatures.

The boundary is just as important: the authors do **not** claim J-space monitoring is sufficient for alignment. Automatic or highly practiced behavior can route outside J-space, and single-token limitations can hide multi-token or diffuse concepts.

## Relationship to J-Space-Replay

J-Space-Replay borrows the interaction shape: it lets users replay Qwen2.5-VL logit-lens and fitted J-lens readouts over a video-answer timeline.

Keep the public claim honest:

- the Anthropic paper validates text-model J-space behavior, not VLM video behavior;
- J-Space-Replay is a demo-quality glass-box surface, not a full replication;
- the app's preset traces and UI are useful for inspecting readouts, but upload/local GPU use is required for new videos;
- the honest claim is "inspect VLM readouts," not "read model thoughts."

## Source handles

- Anthropic Transformer Circuits paper: https://transformer-circuits.pub/2026/workspace/index.html
- Canonical Knowledge page: `Knowledge/concepts/j-space-global-workspace.md`
- Source digest: `Knowledge/raw/papers/anthropic-verbalizable-representations-global-workspace-2026.md`
- Related entity: [[../entities/j-space-replay|J-Space-Replay]]
