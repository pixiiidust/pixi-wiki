---
title: Discord Crew Onboarding Contract
created: 2026-07-28
updated: 2026-07-28
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-systems, discord, onboarding, governance, workflow]
sources:
  - Knowledge/concepts/discord-crew-onboarding.md
  - Projects/Hermes Mission Control/Index.md
confidence: high
---

# Discord Crew Onboarding Contract

Discord crew onboarding is an idempotent route that turns one validated Discord user ID into verified access to an active Hermes crew, then welcomes that person in one shared thread.

## Crew and topology

- **Pika:** local-desktop, primary user-facing coordinator, and final reviewer when available.
- **Pixoid:** VPS control plane, verifier, and fallback orchestrator when Pika is unavailable.
- **Tinker:** builder.
- **Quill:** scribe.
- **Boba:** researcher and reality checker.
- The canonical vault and generated wiki build environment live on the VPS; cross-host review uses pushed review branches rather than assumed shared filesystem access.

## Routing invariants

- Direct bot-user mentions are executable routes; role mentions are labels, not bot routes.
- Webhooks provide outbound display identity, not inbound execution.
- YAML presence alone does not prove bot-authored intake is enabled in the running adapter.
- Bot-authored handoffs require an explicit inline mention. A reply chip alone must not wake another bot.
- Create one shared onboarding thread, not one thread per bot. Never depend on a fixed or previously observed thread ID.

## Effective VPS safety pair

```env
DISCORD_ALLOW_BOTS=mentions
DISCORD_BOTS_REQUIRE_INLINE_MENTION=true
```

Apply the pair to each affected active VPS profile, preserve existing users/tokens/unrelated settings, restart gateways sequentially, and verify fresh process IDs plus safe config readback.

## Reusable trigger

```text
Onboard <Discord user ID>
```

Default route:

1. Validate the ID and channel access for the person and active crew bots.
2. Enumerate active profiles for the current topology.
3. Append the ID exactly once to every active profile's `DISCORD_ALLOWED_USERS`.
4. Confirm the effective safety pair.
5. Restart affected gateways sequentially and verify fresh process IDs.
6. Stop if a matching active onboarding thread already exists.
7. Create exactly one shared onboarding thread.
8. Pika welcomes the person, directly summons each crew bot, and reviews the complete introduction package. Every bot gives a distinct practical example.
9. Rewrite generic, repetitive, unclear, or example-free copy. Pixoid substitutes only when Pika is unavailable.
10. Report actual verification and the shared thread link.

## Boundaries

- Use placeholders in public documentation. Never publish real human IDs, bot IDs, tokens, or ephemeral thread IDs.
- Preserve existing authorization entries and unrelated profile settings.
- A role assignment, webhook, profile name, YAML key, or passing repo test is not by itself proof of live inbound routing.
- For cross-host documentation work, push review branches for the local coordinator to inspect before merge or deploy.

## Related

- [[concepts/multi-agent-multiplayer-boundaries|Multi-Agent Multiplayer Boundaries]]
- [[concepts/peer-profiles-vs-child-processes|Peer Profiles vs Child Processes]]
- [[concepts/agent-capability-route-pattern|Agent Capability Route Pattern]]
- [[entities/hermes-mission-control|Hermes Mission Control]]
- [[syntheses/pixoid-crew-operating-model|Pika/Pixoid Crew Operating Model]]
