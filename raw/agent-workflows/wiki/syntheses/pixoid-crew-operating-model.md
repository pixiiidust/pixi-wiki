---
title: Pika/Pixoid Crew Operating Model
created: 2026-06-16
updated: 2026-07-28
type: synthesis
status: compiled
namespace: agent-workflows
tags: [agent-workflows, pika, pixoid, crew, source-of-truth]
sources:
  - Projects/Hermes Mission Control/Index.md
  - Knowledge/concepts/profile-memory-boundaries.md
  - Knowledge/concepts/runtime-memory-knowledge-routing.md
  - Knowledge/concepts/self-improving-agent-systems.md
  - Knowledge/concepts/peer-profiles-vs-child-processes.md
confidence: high
---

# Pika/Pixoid Crew Operating Model

Jamie's crew operates as bounded peer roles across two hosts. Pika coordinates and final-reviews from the local desktop when available. Pixoid runs the VPS control plane, verifies artifacts, and becomes fallback orchestrator when Pika is unavailable. Tinker builds; Quill maintains source truth; Boba researches and reality-checks.

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
3. **Verify before closing.** Pixoid checks changed files, tests, URLs, branches, issue state, and pushed commits; Pika final-reviews when available.
4. **Promote durable learning carefully.** Evidence must justify whether a lesson belongs in a dossier, concept page, skill, prompt, project hub, or memory pointer.
5. **Separate coordinator mode from specialist routing.** Directly mention Pika for coordination or the intended bot-user for specialist work. Role mentions do not execute routes.

## Discord crew interaction modes

| Mode | Trigger | Contract |
|---|---|---|
| Coordinator | Direct `@Pika` request | Pika owns the user-facing thread and final review while available. |
| Fallback coordinator | Pika unavailable | Pixoid routes, verifies, and returns one final answer from the VPS. |
| Specialist | Direct `@Pixoid`, `@Boba`, `@Quill`, or `@Tinker` | Only the named route replies directly. |
| Shared work thread | Pika-created/reused thread; Pixoid may substitute | Workers respond to bounded direct mentions; one coordinator closes and synthesizes. |
| Direct multiplayer | Shared role assigned to all bots | Not default. It caused duplicate independent investigations and should only be enabled intentionally for tests. |

The 2026-06-29 Discord milestone proved that role mentions and user mentions arrive in different fields and that prompt-level silence fails under reply-ping/runtime-notice loops. The current contract therefore treats role mentions as non-executable, requires direct bot-user mentions, and enforces `DISCORD_ALLOW_BOTS=mentions` plus `DISCORD_BOTS_REQUIRE_INLINE_MENTION=true` for VPS bot handoffs. Reply chips alone cannot wake another bot.

## Cross-namespace links

- [[../../../eval-trace/wiki/concepts/context-overfitting|Context Overfitting]] — evaluation failure mode for stale-context execution.
- `pixi-vault` — namespace compiler and source-class policy.
- `local-ai-infrastructure` — future local/offloaded execution support.
