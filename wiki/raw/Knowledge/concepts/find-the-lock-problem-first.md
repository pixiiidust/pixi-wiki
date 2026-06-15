---
title: Find the Lock: Problem-First Approach
created: 2026-06-11
updated: 2026-06-11
type: concept
tags: [concept, product-management, customer-discovery, workflow]
sources: [discord-thread]
confidence: high
status: active
---

# Find the Lock: Problem-First Approach

## Definition

Find the Lock is Jamie's problem-first approach for turning solution-shaped ideas into crisp problem understanding before committing to a build.

The metaphor:

- **Key** — the proposed solution, feature, product, automation, agent capability, or implementation idea.
- **Lock** — the real problem, constraint, friction, job, risk, missing trust, or blocked behavior that the key is supposed to unlock.

Problem-first means the agent must identify the lock before polishing the key.

## Core rule

When the input arrives as a proposed key, slow down and ask: **what lock is this key supposed to open?**

Do not treat the proposed solution as validated just because it is concrete. Concrete keys can still fit the wrong lock.

## Good lock criteria

A good lock is:

1. **Owned by a specific user or actor** — someone experiences the friction.
2. **Observable in behavior** — it shows up in delays, errors, avoidance, workaround tools, repeated questions, manual cleanup, missed decisions, or money/time loss.
3. **Costly enough to matter** — it creates pain, risk, churn, lost revenue, blocked progress, or cognitive load.
4. **Specific enough to probe** — a prototype, interview, workflow trace, or data check can test whether it exists.
5. **Independent from one favorite key** — multiple possible keys could plausibly open it.

## Anti-patterns

- **Key-first building** — implementing the feature before naming the user friction.
- **Category-first thinking** — starting with a noun like "dashboard", "agent", "platform", or "CRM" before naming the blocked behavior.
- **Vibe lock** — vague pain such as "people need visibility" without specifying visibility into what, for whom, at what decision point.
- **One-key tunnel vision** — defending the first solution instead of comparing alternative keys.
- **Fake validation** — treating excitement about the key as evidence that the lock is real.

## How to use it

Use Find the Lock when Jamie or an agent proposes:

- a feature
- a product idea
- an AI agent capability
- a workflow automation
- a dashboard or UI surface
- a startup wedge
- a PRD direction
- a technical implementation that may be premature

The output should name:

1. Proposed key
2. Suspected lock
3. Lock owner / affected actor
4. Observable evidence
5. Competing keys
6. Fastest probe
7. Recommended next move: prototype, grill, PRD, issue, or discard

## Relationship to `/find-lock`

The reusable Hermes skill is `find-lock`, exposed conversationally as `/find-lock`. The skill is the operating procedure; this note is the durable human-facing concept.

The skill's compact output shape is:

1. Proposed key
2. Suspected lock
3. Lock owner
4. Observable evidence
5. Competing keys
6. Fastest probe
7. Decision

## Relationship to other concepts

- [[matt-pocock-sdlc-rhythm]] — Find the Lock explains why `/prototype` can be used as a probe when a proposed key hides a fuzzy lock.
- [[verb-first-product-positioning]] — Once the lock is found, verb-first positioning describes the action/outcome in concrete user language.
- [[ai-native-problem-framing-framework]] — For AI-native products, the lock helps define the environment, actions, goal, and constraints.

## Short form

Before building the key, find the lock.
