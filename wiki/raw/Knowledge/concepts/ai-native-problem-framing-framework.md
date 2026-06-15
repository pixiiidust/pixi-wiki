---
title: AI-Native Problem Framing Framework
created: 2026-06-11
updated: 2026-06-11
type: concept
tags: [ai, concept, agent-systems, strategy, product-management]
sources: [discord-thread]
confidence: medium
status: active
---

# AI-Native Problem Framing Framework

## Definition

An **AI-native application** is any device or system that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.

The AI-Native Problem Framing Framework is a reusable framework for deciding how to apply AI natively to a real-world domain: first define the AI system precisely, then test whether the domain resembles known AI success cases, then decompose the hard problem into smaller modules with explicit constraints.

One-line version:

> Frame the AI problem as environment/actions/goals/constraints, test whether the domain matches known AI-success structures, identify where reality breaks the analogy, then decompose into prediction, optimization, and execution under hard constraints.

## Core frame

An AI system can be described as:

- **Environment** — what data describes the world?
- **Actions** — what can the system do?
- **Goal** — what is success or what is optimized?
- **Constraints** — what must never be violated?

Bad framing creates bad AI. The environment, action space, objective, and constraints are not implementation details; they define the intelligence problem.

## Check against known success cases

Before copying a method from a successful AI domain, check whether the domain structure actually matches.

Board games work unusually well for AI because they often have:

- clear rules
- full or near-full state visibility
- deterministic outcomes
- abundant self-play data
- simple win/loss objectives
- opponents that can be modeled through self-play

Real-world markets do **not** fit cleanly:

- state is partially hidden
- outcomes are noisy and path-dependent
- participants have different goals and constraints
- actions can affect the environment
- real data is limited and non-stationary
- simulations miss hidden complexity

Principle: do not blindly apply game-style reinforcement learning to real-world domains unless the structural analogy holds.

## Decompose the hard problem

Avoid one giant end-to-end black box when the real domain is noisy, hidden, or regulated. Use human structure to reduce complexity.

For trading-like domains, decompose into:

### 1. Prediction

Question: **What is likely to happen?**

Forecast prices, returns, volatility, demand, liquidity, or other future states. This is usually closer to supervised learning than reinforcement learning.

### 2. Optimization

Question: **What should we own, choose, or allocate?**

Convert forecasts into decisions while balancing expected return, risk, diversification, exposure, capital limits, and other constraints. This can often be math and decision theory, not necessarily AI.

### 3. Execution

Question: **How should we act?**

Translate a target decision into real action while minimizing cost, slippage, market impact, timing risk, and liquidity risk. This is closest to reinforcement learning, but also the hardest because actions change the environment.

## Principles

1. **AI starts with problem framing.** Define environment, actions, goal, and constraints before picking models.
2. **The real world is not a game.** Markets and many operational domains are noisy, hidden, multi-agent, and path-dependent.
3. **Use human structure to reduce complexity.** Prefer interpretable modules over one giant black-box system.
4. **Separate prediction from decision.** Prediction asks what is likely; optimization asks what to do; execution asks how to act.
5. **Constraints are part of intelligence.** Risk limits, regulation, liquidity, ethics, and capital boundaries shape the system.
6. **Simulation is useful but incomplete.** Synthetic environments test ideas but cannot fully represent hidden real-world complexity.
7. **Progress comes from modular improvement.** Improve signals, forecasts, risk models, execution, and feedback loops separately, then reduce the gap to the full objective.

## Why this matters to Jamie's work

This is a reusable lens for evaluating AI-native products and agent systems. It helps prevent vague "add AI" thinking by forcing the product question into a precise system design question.

It also aligns with Jamie's broader workflow-agent philosophy: use AI where the environment, actions, feedback, and constraints can be made explicit; avoid magical end-to-end claims when the domain needs structure, checkpoints, and human-visible controls.

## Agent skill

The concept has also been turned into the Hermes skill `ai-native-framing`, with the core template plus examples for trading, event operations, and customer-support triage.

## Related pages

- [[profile-memory-boundaries]] — where reusable concepts, projects, memory, and skills belong.
- [[agent-capability-route-pattern]] — route contracts and verification gates for agent work.
- [[matt-pocock-sdlc-rhythm]] — product/SDLC gates before implementation.
- [[bounded-context-tree-pattern]] — organizing knowledge into explicit domains and branches.
