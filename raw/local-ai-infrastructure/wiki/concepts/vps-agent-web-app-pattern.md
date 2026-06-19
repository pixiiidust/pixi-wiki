---
title: VPS Agent Web App Pattern
created: 2026-06-19
updated: 2026-06-19
type: concept
status: compiled
namespace: local-ai-infrastructure
tags: [local-ai-infrastructure, vps, hermes-agent, agent-workflows, gitops, web-apps]
sources:
  - raw/transcripts/tonbi-vps-agent-web-app-workflow-2026.md
  - https://youtu.be/K8ZTlMaDfmQ?si=IuNRaHVc-fFHZw41
confidence: medium
---

# VPS Agent Web App Pattern

The **VPS Agent Web App Pattern** uses a small always-on VPS plus a resident agent to replace parts of the beginner Vercel/Supabase/Railway stack for simple, operator-controlled web apps. It works best when the app is mostly files, Markdown, static-ish content, or a small service where the agent can safely own the deploy loop.

This is not “VPS beats managed platforms.” The useful distinction is: managed platforms buy convenience and de-risking; a VPS buys control, low recurring cost, direct file access, and an agent that can operate the system where it runs.

## Core shape

```text
git-backed content/app repo
        ↓
VPS workspace with one app clone + one clone per knowledge base
        ↓
local web server / app process
        ↓
Caddy vhost + automatic TLS
        ↓
resident Hermes agent reachable by SSH or gateway
        ↓
cron/scout/research/update loops with human gates
```

For docs, blogs, wikis, and marketing pages, git can be the database, CMS, and deploy pipeline. The server can render Markdown from disk, keep a search index in memory, and rebuild only when files change. In that class of system, a database would answer a question the app does not actually ask.

## What the agent replaces

The resident agent can cover a subset of what Vercel/Supabase/Railway usually provide:

| Managed stack job | VPS-agent equivalent | Boundary |
|---|---|---|
| Frontend deploy | git push/pull, Caddy vhost, local app process | Good for small sites; weak for preview deploy/team workflows. |
| CMS updates | Markdown files in git | Good for docs/wiki/blog content; weak for multi-user editing. |
| Background jobs | Hermes cron / shell cron / systemd timers | Needs explicit logging and recovery. |
| Content freshness | scout agents + source checks + lint + commit | Needs human gates until trust is earned. |
| Admin console | SSH + Hermes CLI/gateway | Powerful but must be scoped. |
| Search/retrieval feedback | aggregate MCP hit/miss demand loop | Must avoid prompt/IP/user logging. |

## Agent Wikis example

The transcript's example is Agent Wikis: a public wiki-of-wikis where each wiki is a folder of Markdown files. The site renders from disk, uses git as the deploy mechanism, and avoids an application database.

That maps closely to Pixi Wiki's source/output model:

- `pixi-vault` holds source truth and compiled namespace source.
- `pixi-wiki` publishes raw Markdown, rendered HTML, `llms.txt`, `llms-full.txt`, `index.json`, and MCP-facing corpus files.
- [[rag-over-agent-wikis|RAG over Agent Wikis]] uses the compiled wiki as retrieval corpus before adding heavier vector infrastructure.
- [[../../../pixi-vault/wiki/syntheses/pixi-vault-to-pixi-wiki-publishing-model|Pixi Vault to Pixi Wiki Publishing Model]] defines the publish boundary.

## Content freshness loop

The durable workflow pattern is:

```text
cron fires
  → scout checks sources
  → deduplicate and score newness
  → research what matters
  → propose page changes
  → human gate approves plan
  → ingest/update Markdown
  → lint and verify
  → commit to git
  → merge/pull makes site live
```

The human gate is important. It keeps the agent from turning noisy sources into public content just because it can write. A second merge/diff gate is useful until the operator trusts the loop.

## Demand loop

The demand loop is the stronger product idea:

```text
agent asks wiki via MCP
  → server records aggregate hit/miss for distilled query
  → repeated misses become backlog candidates
  → scout/research agents propose additions
  → human approves
  → wiki fills real usage gaps
```

The privacy contract matters more than the automation: record aggregate misses, not prompts, IP addresses, or identities. The loop should learn what the knowledge base lacks without becoming surveillance infrastructure.

## When to use this pattern

Use it when:

- the app is a docs/wiki/blog/marketing/content site;
- git can be the source of truth;
- one operator can tolerate SSH/Git-based operations;
- the resident agent can be scoped to the app workspace;
- freshness comes from source monitoring and editorial review;
- downtime or rollback risk is acceptable for a small VPS.

Avoid it, or add managed services, when:

- the app needs real auth, password resets, or user account recovery;
- it stores cannot-lose or regulated data;
- it needs managed Postgres, backups, row-level security, or object storage guarantees;
- it may face global/viral traffic;
- it needs high email deliverability;
- a team needs preview deploys and parallel environments;
- secrets or credentials require stronger isolation than a general-purpose agent workspace.

## Pixi Wiki routing

Primary namespace: `local-ai-infrastructure`, because the reusable pattern is about local/VPS deployment topology, file-backed web apps, Caddy/git operations, and deciding when a single box can replace managed infrastructure.

Crosslinks:

- [[../../../agent-workflows/wiki/syntheses/pixoid-crew-operating-model|Pixoid Crew Operating Model]] — route governance, human gates, verification, and durable state.
- [[../../../hermes-agent/wiki/concepts/source-priority|Hermes Source Priority]] — use official Hermes docs/local source for commands and runtime behavior; this transcript is a pattern source, not command truth.
- [[../../../pixi-vault/wiki/entities/pixi-wiki|Pixi Wiki]] — the public wiki surface where this pattern can inform source→generated publishing.

## Open questions

- Should Pixi Wiki eventually have its own demand-loop telemetry over MCP queries, and if so what aggregate-only privacy contract is acceptable?
- Which parts of the publish workflow are safe to automate beyond the current regenerate/test/push/live-verify loop?
- Should a future `agent-workflows` page split out the human-gated content freshness loop from this infrastructure page?

## Source

Compiled from Tonbi AI's video transcript, “The Autonomous Agentic Workflow that Runs My Web App w/ Hermes + a $6 VPS,” supplied by Jamie on 2026-06-19.
