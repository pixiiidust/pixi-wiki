---
title: Building Software Is Learning
created: 2026-06-11
updated: 2026-06-11
type: concept
tags: [concept, workflow, product-management, customer-discovery]
sources: [raw/articles/building-software-is-learning-thorsten-ball.md]
confidence: high
status: active
---

# Building Software Is Learning

## Definition

Building new software is a learning process, not a clean execution process. When the team does not yet know exactly how a feature, workflow, interface, or API should work, implementation is how the unknowns become visible.

The core operating principle: **minimize the time between “let me try something” and reality correcting you.**

## Current synthesis

Thorsten Ball's note argues that the common loop — “we need this feature” → “done” → “that's not what I meant / I don't like it / there are trade-offs” — is not a failure of discipline. It is the normal shape of building under uncertainty.

Because programming is fully specifying behavior, a team cannot fully specify novel software before learning what it should be. The useful move is not to avoid surprise. The useful move is to shorten and improve feedback loops so surprise arrives while the cost of change is still low.

This turns shipping from a one-shot delivery event into a sequence of learning probes.

## Operating rules

1. **Treat ambiguity as expected, not embarrassing.** If the desired behavior is not already known, misalignment will appear somewhere. Pull it forward.
2. **Optimize for feedback latency.** Ask: what is the fastest artifact that can hit reality and teach us something?
3. **Optimize for feedback quality.** Do not ship something so buggy, hard to access, or incomplete that feedback collapses into setup pain or bug reports.
4. **Probe the uncertain part first.** Skip the parts that are already known. Spend effort where learning is needed.
5. **Slice so each increment has one main learning question.** Smaller slices reduce the number of possible causes when CI, users, or teammates react.
6. **Match the artifact to the question.** A deck can test concept clarity; example README code can test API shape; a clickable prototype can test workflow feel; production/CI can test integration reality.

## Fast feedback artifacts

Use the cheapest artifact that can answer the live uncertainty:

- **1-hour prototype** — tests interaction, shape, or “is this what you meant?”
- **30-minute spec / approach note** — tests understanding and trade-offs before implementation.
- **Daily vertical slices** — force reality contact every day instead of hiding complexity on a branch.
- **Reduced-scope probe** — isolates unknown behavior rather than building the obvious surrounding machinery.
- **Fake demo video** — tests story, flow, and reaction before building.
- **News post / launch blurb** — tests whether the idea can be explained crisply.
- **README example code** — tests API taste before building the SDK.
- **CI-on-main feedback** — tests integration continuously instead of after a 27-commit merge bomb.

## Feedback-quality checks

Before calling something a feedback loop, check:

- Can the right person experience or review it without jumping through hoops?
- Is the artifact complete enough for the kind of feedback requested?
- Is the artifact narrow enough that feedback points to a clear cause?
- Are we asking for usefulness/design/API/workflow feedback, or will testers only report bugs?
- Did this artifact hit a real constraint: user, teammate, CI, production, or our own hands-on use?

## Anti-patterns

- **Four-week cave build** — disappearing with a vague request and returning with expensive misalignment.
- **Spec fantasy** — assuming everything can be fully known before programming when the product behavior is novel.
- **MVP-as-junk** — shipping something so broken that it only teaches that it is broken.
- **Feedback obstacle course** — making reviewers install, configure, or infer too much before they can react.
- **Long-lived branch learning debt** — merging many commits at once, then treating CI failure as mysterious.
- **Building known parts first** — polishing login, scaffolding, or generic infrastructure when the live uncertainty is elsewhere.

## Use in Jamie's workflow

This concept strengthens [[matt-pocock-sdlc-rhythm]]: `/prototype`, `/grill-with-docs`, `/to-prd`, and `/tdd` are not ceremony. They are different feedback-loop shapes for different unknowns.

It also pairs with [[find-the-lock-problem-first]]: if the lock is fuzzy, use the cheapest probe that can reveal whether the proposed key fits.

For product positioning, it pairs with [[verb-first-product-positioning]]: write the launch blurb, README snippet, or user-facing verbs early to test whether the idea is clear before building the full thing.

## Diagnostic questions

Use these before starting or continuing a build:

1. What are we trying to learn next?
2. What is the cheapest artifact that can teach it?
3. Who or what must react for the feedback to count?
4. How soon can this hit that reality?
5. What would make the feedback low-quality or misleading?
6. Are we building known parts instead of probing the unknown part?
7. When was the last valuable feedback on this work? Why is the interval that long?

## Related pages

- [[matt-pocock-sdlc-rhythm]]
- [[find-the-lock-problem-first]]
- [[verb-first-product-positioning]]
- [[agent-capability-route-pattern]]
