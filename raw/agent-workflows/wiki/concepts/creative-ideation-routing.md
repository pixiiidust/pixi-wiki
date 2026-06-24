---
title: Creative Ideation Routing
created: 2026-06-24
updated: 2026-06-24
type: concept
status: compiled
namespace: agent-workflows
source: Knowledge/concepts/creative-ideation-routing.md
confidence: high
---

# Creative Ideation Routing

Creative ideation routing is the agent-workflow pattern for turning open-ended inspiration requests into method-routed idea generation instead of generic brainstorming.

## Runtime rule

When Jamie asks for inspiration, project ideas, weirdness, options, research questions, or a way out of a stale creative loop:

1. Load the `creative-ideation` Hermes skill.
2. Classify phase, domain, and specificity.
3. Apply overrides for mood, named method, method recommendation, or high-slop terrain.
4. Route to one named method.
5. Generate concrete, non-obvious ideas with mechanisms, tradeoffs, and at least one grounded first step.

## Why this belongs in Agent Workflows

This is not a new Pixi Wiki namespace. It is a reusable skill-routing behavior: Jamie states the creative need, Pixoid chooses the method and skill constraints, then returns any chosen idea to the normal product/build gates.

## Quality bar

Good ideation output:

- names the method used;
- avoids obvious first ideas;
- uses concrete mechanisms and situations;
- states failure modes or tradeoffs;
- includes at least one buildable option;
- stops ideating once Jamie chooses.

Bad output is unrouted LLM slop: generic lists, vague app nouns, no method, no mechanism, no tradeoff, and no first step.

## Relationships

- [[agent-skill-routing|Agent Skill Routing]] chooses when to load `creative-ideation`.
- [[matt-pocock-sdlc-rhythm|Matt Pocock SDLC Rhythm]] takes over after Jamie chooses an idea.
- Cross-namespace product lenses such as [[../../ai-native-product-surfaces/wiki/concepts/interaction-mode-routing|Interaction Mode Routing]] decide which surface should carry a selected idea.

## Source

Canonical source: `Knowledge/concepts/creative-ideation-routing.md`.

Reusable Hermes skill: `~/.hermes/skills/creative/creative-ideation/SKILL.md`.
