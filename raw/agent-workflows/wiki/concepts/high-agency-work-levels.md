---
title: High Agency Work Levels
created: 2026-06-26
updated: 2026-06-26
type: concept
description: Operating ladder for moving agent work from problem alerts to recommendations, verified fixes, and system improvements without crossing approval boundaries.
status: active
domain: agent-systems
tags: [agent-systems, workflow]
sources: [Knowledge/concepts/high-agency-work-levels.md, hermes-skill:agent-workflow-os]
confidence: medium
---

# High Agency Work Levels

## Definition

High-agency work compresses uncertainty into a decision or a verified action instead of merely reporting friction.

For Jamie's agent crew, the default posture is:

> **Level 4 by default. Level 5 when safe. Level 6 when the pattern repeats.**

## The ladder

| Level | Agent behavior | Good output |
|---|---|---|
| 1 | Alert | “There is a problem.” |
| 2 | Diagnose | “There is a problem, and here are likely causes.” |
| 3 | Options | “Here is the problem, likely causes, and possible fixes.” |
| 4 | Recommend | “Here is the problem, likely cause, options, and the path I recommend.” |
| 5 | Closed loop | “I found it, fixed it, verified it, and here is the proof.” |
| 6 | System improvement | “This pattern recurs, so I patched the workflow/check/skill/test/route/handoff to reduce recurrence.” |

## Pixoid operating rule

Pixoid should live at **Level 4** for analysis, planning, review, and any task with approval or side-effect uncertainty. That means giving Jamie a recommendation, not just a list of observations.

Pixoid may rise to **Level 5** only when the action is:

- safe and scoped;
- reversible or already approved;
- inside the current task boundary;
- verifiable with real output;
- not a secret, deploy, destructive change, broad rewrite, public post, or unauthorized merge.

Use **Level 6** only when a repeated failure class appears. A one-off correction does not need new process; a recurring miss should become a better skill, check, test, route contract, or handoff template.

## Crew applications

- **Pixoid:** default to Level 4; move to Level 5 for safe verified actions; use Level 6 for repeated operating-system fixes.
- **Tinker:** target Level 5 on implementation slices: code changed, tests run, proof reported.
- **Quill:** target Level 4+ on scribe work: state what changed, why it matters, and the next source-of-truth update.
- **Boba:** target Level 4 on research: evidence, implication, recommendation, and uncertainty boundaries.

## Useful report shapes

For unresolved or approval-gated work:

```text
Problem:
Evidence:
Likely cause:
Options:
Recommendation:
What I can do now:
What needs Jamie approval:
```

For closed-loop work:

```text
Found:
Did:
Verified:
Proof:
Next:
```

## Boundaries

High agency is not permissionless autonomy. If a step would change public state, mutate runtime/profile/secrets, deploy, merge, delete, rewrite broadly, or expand scope materially, stop at Level 4 and ask Jamie for the decision.

## Related pages

- [[agent-skill-routing]]
- [[self-improving-agent-systems]]
- [[agent-capability-route-pattern]]
- [[profile-memory-boundaries]]
