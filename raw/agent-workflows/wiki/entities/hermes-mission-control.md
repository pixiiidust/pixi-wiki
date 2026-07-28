---
title: Hermes Mission Control
created: 2026-06-16
updated: 2026-07-28
type: entity
status: compiled
namespace: agent-workflows
tags: [agent-workflows, hermes, pika, pixoid, route-governance]
sources:
  - Projects/Hermes Mission Control/Index.md
  - Projects/Hermes Mission Control/kpr-pixoid-routing-rule.md
  - Projects/Hermes Mission Control/PRD - Knowledge Pack Routing.md
confidence: medium
---

# Hermes Mission Control

**Hermes Mission Control** is Jamie's agent-ops coordination hub for Pika, Pixoid, Tinker, Quill, and Boba across a local-desktop/VPS topology.

Its primary namespace is `agent-workflows` because the durable knowledge is not the public wiki itself. The durable knowledge is how agents coordinate work: route governance, persona boundaries, issue-backed execution, handoffs, review gates, and durable truth routing.

## Crew roles

- **Pika:** local-desktop primary user-facing coordinator and final reviewer when available.
- **Pixoid:** VPS control plane, route verifier, and fallback orchestrator when Pika is unavailable.
- **Tinker:** builder for bounded implementation slices.
- **Quill:** scribe for vault/docs updates and compiled knowledge pages.
- **Boba:** researcher and reality checker for external signal.

## What it controls

- Crew role boundaries and operating surfaces.
- GitHub issue/PR coordination as durable work truth.
- Obsidian/Git as knowledge and project truth.
- Discord as notification surface, not durable truth.
- Discord routing/onboarding: direct bot-user mentions call the named route; role mentions do not execute; `Onboard <Discord user ID>` uses one shared thread and active-profile verification.
- Cron output as context, not canonical project state.
- Verification gates before tracker closure.


## Pika/Pixoid Review Surface

Interaction Mode Routing clarifies that chat is the command channel, not the whole Hermes interface. Pixoid generates inspectable VPS artifacts and review branches; Pika performs final review when available. Durable truth remains in GitHub issues/PRs, Obsidian hubs, handoffs, skills, and knowledge entrypoints.

The standard review surface includes status, evidence, risks, files/handles, verification run, options, and Pixoid's recommended next slice.

## Discord council-mode hardening milestone

The 2026-06-29 slice established anti-dogpile and closed-loop protections. The current 2026-07-28 contract is topology-aware and direct-mention-only:

- Direct `@Pika` calls use Pika as primary coordinator/final reviewer while available.
- Direct `@Pixoid`, `@Boba`, `@Quill`, and `@Tinker` calls wake only the named bot-user route.
- Role mentions such as `@Crew` are labels, not executable bot routes.
- Pika may open/reuse one shared work thread; Pixoid does so only in fallback mode. Onboarding never creates one thread per bot.
- Closed huddle threads suppress ambient worker/bot chatter before model invocation; prompt-level silence is not the enforcement layer.
- Discord reply pings are not direct summons unless the message text explicitly mentions the target bot-user.
- Active VPS profiles use `DISCORD_ALLOW_BOTS=mentions` plus `DISCORD_BOTS_REQUIRE_INLINE_MENTION=true`; YAML presence alone is not runtime proof.
- Outbound webhooks provide display identity only and do not prove inbound execution.

## Routing significance

Hermes Mission Control feeds `pixi-vault` when compiler/publication rules are affected, and it feeds `eval-trace` when route quality or workflow evidence needs evaluation.

The project should not become a standalone namespace unless it grows an independent audience, source corpus, document types, and freshness lifecycle beyond the broader `agent-workflows` domain.

## Cross-namespace links

- `pixi-vault` — source/output repo boundaries and namespace compiler rules.
- `eval-trace` — route-quality checks and failure-mode evaluation, including [context overfitting](../../../eval-trace/wiki/concepts/context-overfitting.md).

## Related pages

- [[../concepts/knowledge-pack-routing|Knowledge Pack Routing]]
- [[../concepts/agent-entrypoint-mesh|Agent Entrypoint Mesh]]
- [Interaction Mode Routing](../../../ai-native-product-surfaces/wiki/concepts/interaction-mode-routing.md)
- [[../syntheses/pixoid-crew-operating-model|Pixoid Crew Operating Model]]

## Source

Compiled from `Projects/Hermes Mission Control/Index.md` and related KPR operating docs.
