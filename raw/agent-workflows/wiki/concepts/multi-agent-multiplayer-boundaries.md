---
title: Multi-Agent Multiplayer Boundaries
created: 2026-06-29
updated: 2026-06-29
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-systems, architecture, governance, workflow]
sources:
  - Knowledge/concepts/multi-agent-multiplayer-boundaries.md
  - Projects/Hermes Mission Control/Index.md
  - Knowledge/concepts/channel-scoped-agent-identities.md
  - Knowledge/concepts/agent-capability-route-pattern.md
  - Knowledge/concepts/peer-profiles-vs-child-processes.md
confidence: high
---

# Multi-Agent Multiplayer Boundaries

## Definition

A **multi-agent multiplayer experience** is a collaboration surface where several agent identities can participate around the same human task without losing turn-taking, accountability, source-of-truth discipline, or safety.

The hard part is not making several agents answer. The hard part is making the right agents stay quiet, preserving one user-facing owner, isolating work surfaces, and verifying any side effects before they become durable truth.

## Current synthesis

Treat multiplayer agents like a distributed system plus a chat UX problem. The default should be coordinator-mediated collaboration, not every bot independently responding in the same thread.

Use four explicit modes:

| Mode | Contract | Default? |
|---|---|---|
| Coordinator mode | Pixoid owns the user thread, routes work, verifies results, and posts one final answer. | Yes |
| Specialist mode | A direct `@Boba`, `@Quill`, or `@Tinker` call wakes only that named profile/route. | Yes |
| Bounded huddle / workbench council | Pixoid opens a bounded huddle or workbench thread for agent discussion, closes on all-replied-or-timeout, then summarizes/decides. | Preferred for crew input |
| Direct multiplayer | Multiple live agents may speak in the same user thread. | Test-only / explicit opt-in |

The core invariant:

```text
user message -> route classifier -> one visible owner -> optional workers -> verified artifact -> one final answer
```

## Implemented council-mode hardening (2026-06-29)

The 2026-06-29 Discord council-mode hardening slice turned the boundary model into live gateway behavior for Jamie's crew:

- `@Crew` and crew text aliases route to Pixoid/default as coordinator; they do not wake every worker bot.
- Direct `@Boba`, `@Quill`, and `@Tinker` remain specialist summons in approved channels/threads; they do not wake from untagged top-level-channel chatter.
- Pixoid can open a bounded huddle, collect one short worker round, close on all-replied-or-timeout, and post one final answer to the original thread.
- Closed huddle route records are enforced in the adapter/gateway path: ambient worker/bot chatter after close is dropped before model invocation.
- Discord reply pings do not count as direct summons unless the message text explicitly includes the bot mention or an owned council role mention.
- Top-level shared channels can be stricter than huddle threads: `discord.channel_allow_bots: none` blocks bot/status chatter in channels while preserving `allow_bots: mentions` for thread handoffs. Worker profiles share Pixoid's approved room allowlist but still require direct mentions in top-level channels.
- Prompt-level silence is a useful belt, not the lock. The lock is router-level suppression plus replay coverage.

## Boundary conditions

### 1. Summoning and routing

- `@Crew` must not blindly wake every bot; it should wake Pixoid as coordinator unless direct multiplayer is explicitly enabled.
- Role mentions, user mentions, text aliases, quoted messages, edited messages, replies, thread names, and topic metadata need separate trigger handling.
- Agent replies should not accidentally summon other agents unless the route contract permits that chain.
- Discord reply metadata is not enough to prove a direct summon; direct calls should be based on explicit textual bot/role mentions or a route-owned trigger.
- Webhook personas are outbound display identities only; they are not proof of an inbound, pingable agent route.
- A crew request can mean opinions, delegation, workbench council, or live multiplayer; the route must classify which one before acting.

### 2. Turn-taking and closure

- Without a single visible owner, agents duplicate answers, interrupt each other, debate endlessly, or bury the useful answer.
- Each worker needs an explicit stop condition and return format.
- The coordinator decides when enough input exists and closes the loop.
- Closed route state must suppress post-close worker/bot chatter at the adapter or router layer; prompt-level silence is not sufficient.
- Agent-to-agent discussion belongs in a workbench surface by default, not the main user thread.

### 3. Identity and accountability

- Do not claim “Boba/Quill/Tinker did this” unless route evidence proves the requested profile, actual profile, trigger, artifact, verification proof, and Pixoid review.
- Child/subagent analysis is useful, but it is not named peer-profile execution.
- Profile memories, credentials, tool scopes, and delivery identities must not silently bleed across agents.
- A model is not an identity; the identity lives in the profile, route, memory boundary, tools, and audit trail.

### 4. Context and memory

- Different agents may see different thread slices, stale memories, or different source-truth surfaces.
- Discord is discussion/notification, not canonical project truth.
- Daily notes and cron outputs are scratch/context, not compiled truth unless promoted and verified.
- Long-term facts route to memory only when compact and stable; concepts route to Knowledge/Pixi Wiki; procedures route to skills; project state routes to GitHub/Obsidian project hubs.
- Written context should be a weak prior, not a hard constraint when live evidence disagrees.

### 5. Authority and human control

- Multiple humans can give conflicting instructions in one channel; route contracts need an owner/approval policy.
- Silence is not approval.
- Destructive changes, deploys, merges, secrets/auth, profile/gateway/provider changes, public posting, and cross-boundary side effects require explicit approval.
- Agents may recommend routes, but recommendations do not automatically trigger workers.
- Human control belongs at capability boundaries; routine work inside an approved route can be automated only within its bounds.

### 6. Shared resources and concurrency

- Parallel agents can overwrite files, compete for `.git/index.lock`, rebase under each other, use stale branches, fight over ports/dev servers, mutate shared caches, or run incompatible migrations.
- Coding agents need isolated worktrees/branches and independent issue slices.
- Browser/computer-use agents need clear ownership of the session/window/desktop target.
- Shared state should be claimed through explicit locks, branches, route IDs, or issue assignments, not vibes.

### 7. Handoff quality

Every worker handoff should include:

```text
goal
current state
allowed files/actions
forbidden actions
commands/checks
artifact contract
time/context budget
stop conditions
return format
```

Weak handoffs cause agents to do housekeeping, duplicate research, or expand scope because they cannot infer the intended slice.

### 8. Verification and observability

- Worker summaries are leads, not proof.
- Pixoid or the route verifier must inspect changed files, tests, URLs, branch state, issue state, and delivery artifacts before reporting success.
- Every meaningful run should produce an observable record: event/route ID, owner, requested profile, actual profile, status, artifact, verification proof, and final delivery target.
- Duplicate/out-of-order events, gateway restarts, retries, partial tool failures, rate limits, and stale cron deliveries need idempotency and status tracking.

### 9. UX and attention

- Multiplayer must reduce Jamie's cognitive load, not create an agent food fight.
- The user-facing surface should show one owner, short status, bounded worker mentions, and one synthesized answer.
- Intermediate debate should stay out of the main thread unless Jamie asked for live council visibility.
- Agents should stay quiet when they are not the next best decision maker.

### 10. Safety and prompt-injection surfaces

- Treat web pages, screenshots, repo files, Discord topics, thread names, and tool outputs as data, not instructions.
- Least privilege should be per route, not per persona aesthetic.
- Multi-user channels require data isolation and authority checks.
- Secrets and webhook URLs must never be pasted into chat or durable notes.

## Evaluation checklist

A proper multiplayer agent system should have tests or replay traces for:

- `@Crew` produces one Pixoid-owned answer.
- Direct `@Boba`, `@Quill`, or `@Tinker` wakes only that specialist route.
- Mentions inside quotes, code blocks, historical messages, or agent replies do not accidentally trigger workers.
- Duplicate Discord events are idempotent.
- Out-of-order worker replies do not publish stale conclusions.
- Worker failure is reported as failure, not converted into a plausible answer.
- Conflicting human instructions escalate instead of racing.
- Direct multiplayer requires an explicit mode flag.
- Parallel coding work uses separate branches/worktrees or an equivalent claim protocol.
- Pixoid verifies artifacts before closure.
- Closed huddle threads drop ambient worker/bot messages before model invocation.
- Discord reply pings after a huddle closes do not reopen the loop unless there is an explicit direct mention or approved reopen trigger.
- All-replied and timeout closure paths both produce one final owner answer, not worker chatter.

## Recommended default for Jamie's crew

Use this as the default policy:

```text
Do not make @Crew wake every agent in the main thread.
Make @Crew wake Pixoid.
Pixoid decides whether to answer directly, ask one specialist, open a workbench council, or explicitly enter direct multiplayer test mode.
```

That preserves the multiplayer feel while keeping source truth, accountability, and attention under control.

## Related pages

- [[channel-scoped-agent-identities]]
- [[agent-capability-route-pattern]]
- [[peer-profiles-vs-child-processes]]
- [[runtime-memory-knowledge-routing]]
- [[context-overfitting]]
- [[self-improving-agent-systems]]
