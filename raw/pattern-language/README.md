---
title: Pattern Language
created: 2026-07-01
updated: 2026-07-01
type: namespace-overview
status: active
category: spatial-design
namespace: pattern-language
confidence: medium
source_repository: https://github.com/zenodotus280/apl-md
source_license_note: Non-commercial reuse with attribution; see source LICENSE.md.
---

# Pattern Language

> Spatial-design pattern reference for agents, compiled from the abridged `zenodotus280/apl-md` Markdown manifestation of Christopher Alexander's *A Pattern Language*.

## Scope

### Covers

The `pattern-language` namespace covers the abridged, hyper-textual pattern corpus from `apl-md`: 253 built-environment patterns, their Problem/Solution framing, related-pattern graph, provenance, license guardrails, and agent-facing retrieval guidance for spatial design and worldbuilding.

### Not Covered

This namespace does not cover generic architecture theory outside the imported corpus, commercial training-data clearance, complete republication of the original book beyond the `apl-md` abridged material, or implementation of an Unreal MCP adapter. Unreal/worldbuilding adapter design is tracked as a deferred follow-up.

### Current As

2026-07-01 — Initial namespace release imports 253 pattern documents from `zenodotus280/apl-md`, preserves related-pattern wikilinks, and adds agent retrieval/worldbuilding guidance plus deferred Unreal MCP adapter notes.

## Canonical Source Roots

- External source repo: `https://github.com/zenodotus280/apl-md`
- Source permission note: `https://github.com/zenodotus280/apl-md/blob/master/LICENSE.md`
- Imported corpus path: `Patterns/*.md` in the source repo
- Pixi Wiki tracker: `https://github.com/pixiiidust/pixi-wiki/issues/42`

## Provenance and License Guardrail

**Non-commercial reuse with attribution** is the governing guardrail. The source repo states that permission was granted on 2024-04-14 to reproduce and reuse portions of text from `patternlanguage.com` for non-commercial purposes and with proper attribution to Christopher Alexander and *A Pattern Language*. This namespace keeps that guardrail visible.

Use this corpus for private/internal/non-commercial reference, retrieval, critique, education, and design experiments. Do not present it as a commercial-clean training dataset or as unrestricted source material for redistribution.

## Agent Use Contract

- Start with [[summaries/for-agents-spatial-pattern-retrieval|For Agents — Spatial Pattern Retrieval]].
- Retrieve a bounded set of patterns, usually 5–12, before proposing a design.
- Translate pattern Problem/Solution text into constraints, adjacency rules, scale cues, layout moves, and verification checks.
- Cite pattern names/numbers in the design brief so a human can inspect the rationale.
- Avoid quoting long source passages unless the user explicitly needs the source wording.

## Public Output Contract

When published to `pixi-wiki`, this namespace should expose:

```text
/raw/pattern-language/README.md
/raw/pattern-language/wiki/index.md
/wiki/pattern-language/README.md.html
/wiki/pattern-language/wiki/index.md.html
/wiki/pattern-language/llms.txt
```
