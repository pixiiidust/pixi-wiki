---
title: Context Overfitting
created: 2026-06-18
updated: 2026-06-18
type: concept
status: compiled
namespace: eval-trace
tags: [agent-systems, governance, workflow, ai]
sources:
  - /root/.hermes/knowledge/concepts/context-overfitting.md
  - Knowledge/concepts/context-overfitting.md
confidence: high
---

# Context Overfitting

## Definition

**Context overfitting** is when an agent over-weights written context — memory, skills, dossiers, project notes, cron prompts, prior suggestions, or old issue state — and treats it as a hard constraint even when current user intent, live evidence, or scope boundaries should override it.

The written rule may still be useful. The failure is the weighting and scope.

## Current synthesis

Use the compact test:

```text
Context overfit? YES / NO / UNSURE
Suspect source: <memory / skill / dossier / prompt / project note / issue / none>
Evidence:
- <1-2 concrete observations>
Recommended action: <demote / scope / patch / update truth / keep / ask Jamie>
```

Verdicts:

| Verdict | Meaning | Action |
|---|---|---|
| YES | Written context or stale truth overrode current user intent, live evidence, or scope boundaries. | Demote the rule, scope it, patch the source, update the canonical truth surface, or remove the stale consumer. |
| NO | Context was used as a weak prior and the agent stayed steerable. | Keep the rule; no durable change unless another defect appears. |
| UNSURE | Evidence is insufficient, or Jamie must judge whether the rule should generalize. | Ask Jamie, inspect the suspect source, or gather better trace evidence before changing durable state. |

## Source-layer priority

When context conflicts, prefer current and canonical truth in this order:

1. current user instruction and explicit scope;
2. safety, secrets, data-loss, and approval boundaries;
3. live filesystem/GitHub/runtime evidence;
4. current PRD, issue, route contract, or handoff;
5. project/vault source of truth;
6. local Hermes knowledge concepts;
7. skills and procedures;
8. memory, dossiers, cron prompts, and older session recalls as weak priors.

This is a routing rule, not a license to ignore durable context. Written context is useful when it is current, scoped, and backed by live evidence.

## Application

Run this check when:

- an agent refuses a reasonable correction because an older rule says otherwise;
- project-local advice leaks into another project;
- stale issue or repo state drives a current recommendation;
- a self-improvement loop tries to promote a one-off suggestion into global behavior;
- memory or a dossier sounds authoritative but live evidence disagrees;
- a route/profile rule is treated as automatic approval when it is only a recommendation.

For self-improvement, pair this page with [[self-improving-agent-systems]]: promote only evidence-graded, reversible, layer-fit lessons. For memory and knowledge routing, pair it with [[runtime-memory-knowledge-routing]] and [[profile-memory-boundaries]].

## Boundaries

- Do not use this rubric to bypass safety, secrets, destructive-action, merge, deploy, or live-posting approvals.
- Do not patch memory, cron, profiles, providers, gateways, MCP, RAG, or GitHub state merely because a context-overfit risk exists; verify and use the correct change process.
- Do not store raw eval traces, issue progress, PR numbers, or command logs in concept pages.
- Do not call every stale page context overfitting. Ordinary knowledge rot is stale content; context overfitting is stale or over-scoped content being weighted too strongly during action.

## Related pages

- [[self-improving-agent-systems]]
- [[runtime-memory-knowledge-routing]]
- [[profile-memory-boundaries]]
- [[agent-ops-harness-health]]
- [[agent-capability-route-pattern]]
- [[matt-pocock-sdlc-rhythm]]

## Sources

- `/root/ObsidianVault/Knowledge/concepts/context-overfitting.md`
