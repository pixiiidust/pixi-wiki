---
title: "Verb-First vs Noun-First: Actions Before Labels"
created: 2026-07-20
updated: 2026-07-20
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-workflows, agent-systems, instruction-design, knowledge-systems, intent]
sources:
  - Knowledge/concepts/verb-first-knowledge.md
  - Knowledge/concepts/verb-first-product-positioning.md
confidence: medium
---

# Verb-First vs Noun-First: Actions Before Labels

**Verb-first knowledge** explains or instructs through actions before relying on category labels. It names who or what acts, what changes, what receives the action, under which conditions, and what observable result should follow.

Verb-first does not mean every sentence must literally begin with a verb. It means the operational meaning comes before the label.

```text
actor → action → object or state → condition → observable result
```

Noun-first language says what something *is*:

> This is an agent-governance framework.

Verb-first language shows what it *does*:

> It routes requests to bounded agents, checks their evidence, and stops unapproved actions before execution.

The category can follow once the action is clear.

## What difference do verbs make?

Nouns are useful compression. They name stable things, roles, domains, and categories. But a noun often asks the reader to supply the mechanism from prior knowledge.

Verbs expose the mechanism. They help a person:

1. **Simulate what happens** — picture a sequence or state change.
2. **Infer less** — rely less on assumptions hidden behind labels such as `platform`, `strategy`, `governance`, or `assistant`.
3. **See responsibility** — identify who acts and who receives the result.
4. **Test the claim** — observe, compare, or falsify an action and outcome.
5. **Choose a next move** — understand what to do, not only which shelf the idea belongs on.

A noun can create recognition without operational understanding. A verb turns recognition into a model of behavior.

## Difference for people

People need more than *what category is this?* They need to know:

- What can I do with it?
- What will it do to my input?
- What changes afterward?
- What am I responsible for?
- What should I expect to observe?

Verb-first language reduces the gap between reading and acting. It also makes intent easier to repeat across domains, teams, or cultures where the same noun may carry different assumptions. `Review`, `governance`, `community`, and `strategy` can each name many incompatible practices. The verbs reveal which practice is intended.

## Difference for an LLM

An LLM predicts continuations from the information and instructions it receives. A noun or role label can activate a broad cloud of associated patterns without selecting the behavior the user wants.

> You are a reviewer.

That leaves the review target, method, evidence standard, output, and authority boundary unspecified.

A verb-first instruction narrows the action space:

> Compare the changed files with the acceptance criteria, identify concrete regressions, cite file paths and evidence, return findings by severity, and do not edit or merge anything.

This supplies:

- an actor and target;
- an action sequence;
- selection and evidence criteria;
- an output contract;
- permission boundaries.

For tool-using agents, verbs also map directly to capabilities such as `search`, `read`, `compare`, `calculate`, `write`, `test`, `publish`, or `stop`. Noun labels help retrieval; action language helps select and sequence tools.

Verb-first wording does not guarantee correct model behavior. Models can still misunderstand, ignore constraints, or fabricate. Examples, evidence, permissions, and verification remain necessary. The advantage is narrower ambiguity, not deterministic control.

## Reusable shapes

For knowledge:

> [Actor or system] [verb] [object or state] under [condition] to produce [observable result].

For instructions:

> When [trigger], [verb] [object] using [evidence or tool], return [artifact], and do not [boundary].

If the actor, action, object, condition, result, or boundary cannot be named, the concept may still be too vague to use.

## Examples

| Noun-first | Verb-first |
|---|---|
| An AI research assistant | Searches named sources, extracts relevant evidence, and returns a cited comparison. |
| A memory system | Stores stable user facts, retrieves relevant context, and keeps temporary task state out of durable memory. |
| A governance framework | Routes decisions by risk, requires approval for protected actions, and records verification evidence. |
| A community strategy | Brings a defined group together to exchange help, contribute work, and return for repeated value. |
| A reviewer | Compares the change with the contract, identifies regressions, cites evidence, and returns findings without editing. |

## Nouns still matter

Verb-first is not anti-noun. Nouns provide identity, indexing, continuity, and shared vocabulary. Useful knowledge needs both:

```text
nouns for retrieval and orientation
verbs for behavior and execution
```

Use the noun to help someone find the concept. Use the verbs to help them understand, apply, test, or delegate it.

## Applied page: product positioning

[[../../ai-native-product-surfaces/wiki/concepts/verb-first-product-positioning|Verb-First Product Positioning]] applies this general rule to product descriptions: name what the product does to a specific input, for whom, with what outcome, and which pain it removes before naming its category.

## Related pages

- [[concepts/agent-tooling-plan|Agent Tooling Plan]]
- [[concepts/agent-skill-routing|Agent Skill Routing]]
- [[../../ai-native-product-surfaces/wiki/concepts/interaction-mode-routing|Interaction Mode Routing]]
- [[../../ai-native-product-surfaces/wiki/concepts/verb-first-product-positioning|Verb-First Product Positioning]]
