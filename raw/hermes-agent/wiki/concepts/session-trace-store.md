---
title: Hermes Session Trace Store
created: 2026-06-18
updated: 2026-06-18
type: concept
status: compiled
namespace: hermes-agent
tags: [hermes-agent, sessions, traces, state-db, insights]
sources:
  - /usr/local/lib/hermes-agent/hermes_state.py
  - /usr/local/lib/hermes-agent/agent/insights.py
  - https://hermes-agent.nousresearch.com/docs/reference/cli-commands
confidence: high
---

# Hermes Session Trace Store

Hermes' built-in trace substrate is the profile-scoped SQLite session store.

## What it stores

`state.db` stores session metadata, full message history, model configuration, tool calls, token usage, costs, source/platform tags, and searchable message text via FTS5.

The local source describes it as replacing older per-session JSONL storage for normal CLI/gateway sessions. Batch runner and RL trajectories are separate systems.

## Useful commands

```bash
hermes sessions list
hermes sessions browse
hermes sessions stats
hermes sessions export out.jsonl
hermes sessions export --source discord discord.jsonl
hermes sessions export --session-id <session_id> one-session.jsonl
```

## Insights

`hermes insights` analyzes `state.db` for token consumption, cost estimates, tool usage patterns, skill usage, activity trends, model/platform breakdowns, and top sessions.

```bash
hermes insights --days 30
hermes insights --days 7 --source cli
```

## Boundary

This is operational telemetry. It is not a correctness judge. Use it to find traces, mine examples, and inspect behavior; pair it with explicit eval prompts or human review when measuring quality.
