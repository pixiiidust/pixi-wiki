---
title: Hermes Source Priority
created: 2026-06-18
updated: 2026-06-18
type: concept
status: compiled
namespace: hermes-agent
tags: [hermes-agent, source-priority, docs, agentwikis]
sources:
  - https://hermes-agent.nousresearch.com/docs
  - /usr/local/lib/hermes-agent
  - https://agentwikis.com/wiki/hermes/llms.txt
confidence: high
---

# Hermes Source Priority

Hermes reference work should separate **truth** from **maps**.

## Priority order

1. **Official Hermes docs** — commands, setup, configuration, current documented behavior.
2. **Local installed Hermes source** — what this VPS actually has installed and can run.
3. **AgentWikis Hermes** — curated topic map, release summaries, ecosystem inventory, and explanation layer.
4. **Web search** — freshness checks for new releases, open issues, and current community state.

## AgentWikis role

AgentWikis is useful as a discovery map. It surfaces topics such as MCP integration, configuration, profiles, subagents, release summaries, providers, memory backends, and community projects. It should not override official docs or live source when commands differ.

## Use policy

Use AgentWikis to decide what to read next. Use official docs or live source to decide what to run.

```text
Question: "What Hermes features exist?"          → AgentWikis is useful.
Question: "What command should I run now?"       → Official docs/live CLI first.
Question: "Why is this VPS failing?"             → Inspect live state first.
Question: "Is this still current upstream?"      → Official docs + web/GitHub check.
```

## Import boundary

Do not mirror the whole AgentWikis Hermes corpus into Pixi Wiki. Import only pages that support Jamie/Pixoid operations, and preserve source metadata plus freshness dates.
