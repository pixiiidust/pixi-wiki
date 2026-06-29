---
title: Pixoid Crew Operating Model
created: 2026-06-16
updated: 2026-06-29
type: synthesis
status: compiled
namespace: agent-workflows
tags: [agent-workflows, pixoid, crew, source-of-truth]
sources:
  - Projects/Hermes Mission Control/Index.md
  - Knowledge/concepts/profile-memory-boundaries.md
  - Knowledge/concepts/runtime-memory-knowledge-routing.md
  - Knowledge/concepts/self-improving-agent-systems.md
  - Knowledge/concepts/peer-profiles-vs-child-processes.md
confidence: high
---

# Pixoid Crew Operating Model

The Pixoid crew operates as a set of bounded peer roles coordinated through durable source-of-truth surfaces. Pixoid is the control plane; Tinker builds; Quill maintains vault/source truth; Boba explores public sources and reality-checks signals.

## Operating contract

- GitHub issues and PRs are coordination truth.
- Obsidian/Git is knowledge and project truth.
- Discord is notification, not durable truth.
- Cron output is context, not canonical state.
- Daily Notes are scratch chronology, not compiled truth.

## Why this belongs in agent-workflows

The model is about how work moves through the crew: route selection, source-of-truth checks, memory boundaries, evidence gates, and review. It links to `pixi-vault` where the same rules affect namespace compilation, and to `eval-trace` where workflow quality gets measured.

## Core patterns

1. **Route by source of truth.** Use GitHub for work coordination, Obsidian for knowledge/project truth, skills for procedures, and memory only for compact stable routing facts.
2. **Prefer peer profiles for named crew work.** Use child/subagent execution only as a local fallback and label it honestly.
3. **Verify before closing.** Pixoid checks changed files, tests, live URLs, issue state, and pushed commits before reporting success.
4. **Promote durable learning carefully.** Evidence must justify whether a lesson belongs in a dossier, concept page, skill, prompt, project hub, or memory pointer.
5. **Separate coordinator mode from multiplayer mode.** `@Crew` is a Pixoid coordinator call by default, not a request for every live bot gateway to solve the same user message independently.

## Discord crew interaction modes

| Mode | Trigger | Contract |
|---|---|---|
| Coordinator | `@Crew`, `crew:`, `get the crew`, `calling the crew` | Pixoid handles the user-facing thread, creates/reuses a topic workbench thread when useful, gathers crew input, and posts one final answer. |
| Specialist | `@Boba`, `@Quill`, `@Tinker` | Only the named profile replies directly. |
| Workbench council | Pixoid-created topic thread in `#agent-workbench` | Worker profiles discuss a bounded prompt away from the user thread; Pixoid summarizes/decides. |
| Direct multiplayer | Shared role assigned to all bots | Not default. It caused duplicate independent investigations and should only be enabled intentionally for tests. |

The live 2026-06-29 Discord milestone proved that role mentions and human mentions arrive in different Discord fields (`message.role_mentions` vs `message.mentions`). The adapter fix made role mentions count as calls, but the operating fix is still route governance: shared crew summons should not wake all peer profiles into the same user thread unless the desired mode is deliberately direct multiplayer.

## Cross-namespace links

- [[../../../eval-trace/wiki/concepts/context-overfitting|Context Overfitting]] — evaluation failure mode for stale-context execution.
- `pixi-vault` — namespace compiler and source-class policy.
- `local-ai-infrastructure` — future local/offloaded execution support.
