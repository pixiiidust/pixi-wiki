---
source_url: https://youtu.be/K8ZTlMaDfmQ?si=IuNRaHVc-fFHZw41
ingested: 2026-06-19
sha256: 3718867c216538e104df7998eb758988e9fd4f264cc916a554fb6a36efd339fb
type: transcript
---

# Transcript — The Autonomous Agentic Workflow that Runs My Web App w/ Hermes + a $6 VPS

Source: https://youtu.be/K8ZTlMaDfmQ?si=IuNRaHVc-fFHZw41
Creator/channel: Tonbi AI
Transcript supplied by Jamie in chat on 2026-06-19.

## Video description

When you start vibe-coding apps, the tools push you toward Vercel, Supabase, and Railway — but I run everything on one small VPS with a Hermes agent instead, and I'll show you exactly how. Using my live site Agent Wikis (agentwikis.com — free knowledge bases for agents) as the example, I break down why git is the only "database" a docs/wiki/blog-class site needs, how the agent lives on the box and serves the site through Caddy, and the autonomous Cron pipeline that keeps every wiki fresh behind a single Telegram approval. Then I demo the new "demand loop": agents search the wikis via an MCP server, repeated misses (privacy-preserving, no prompts or IPs stored) become an authoring backlog, and the agent researches and fills those gaps automatically — live on the site in minutes. This is Part 1 (the site that needs no database); Part 2 deploys a game app that does need one, on the same box.

## Chaptered transcript notes

### 1. Replacing Vercel/Supabase/Railway with a VPS + agent

The setup replaces common beginner deployment platforms — Vercel, Supabase, Railway — with a small VPS and one Hermes agent that maintains web apps, content, and business workflows. The video uses Agent Wikis as the live example and promises a later database-backed game app example.

### 2. The usual stack and what it really gives you

Vercel, Railway, and Supabase provide deployment, managed Postgres, backups, auth, realtime, row-level security, storage, and beginner convenience. The core claim is not that they are bad, but that their main value is de-risking and convenience. A VPS can replace the core functions for some project classes, but not all.

### 3. Agent Wikis: when git is your database

Agent Wikis has no application database. It is a folder of Markdown files, one git clone per wiki, rendered from disk. The server renders Markdown on each request and keeps a search index in memory, rebuilding only when files change. For docs, blogs, wikis, marketing pages, and similar content sites, git can act as database, CMS, and deploy pipeline. A git push plus server pull makes content live without app restart or build.

### 4. The VPS setup

The site runs as a tenant on a small VPS that already hosts the Hermes agent. Caddy terminates TLS and adds a virtual host that reverse-proxies the public domain to localhost; Caddy auto-provisions certificates. The operator can SSH into the VPS and run Hermes directly against files on the box. The agent does not receive unrestricted access; the security model should scope it to the site/workspace areas it needs.

### 5. The content pipeline

A cron job fires scout/research agents to check sources such as releases, changelogs, major features, and community notes for each wiki. They deduplicate, research what is genuinely new, and create a plan. A Telegram human gate approves the plan. After approval, the system ingests sources, lints, commits to git, and the site becomes live within roughly 15 minutes. Weekly cadence controls token cost.

### 6. The demand loop

Agent Wikis learns from what agents ask for without storing prompts or identities. Agents query through an MCP server. The server receives a distilled query, records only aggregate hit/miss information, and does not store prompts, IPs, or identity. Repeated misses become an authoring backlog. Research agents turn those misses into candidate updates, propose page-vs-extension decisions, and wait for a human approval gate.

### 7. Live demo: filling demand gaps autonomously

The demo parses five live demand gaps, each asked at least twice in seven days. It creates item files and child cards, routes them through research and verification, and blocks at the human proposal gate. One example adds a webhook route rate limit answer to the messaging gateway page: each webhook route defaults to 30 requests per minute using a fixed window. Lint checks verify formatting and conflicts before commit.

### 8. Two human gates + merging live

The workflow has two gates: proposal approval before writing, then final diff review and merge to main. The author may eventually automate the merge gate after confidence grows, but currently keeps human review before live merge. Once merged, the live site updates automatically.

### 9. When a single box is not enough

The VPS pattern is not universal. Use managed services when the project needs real auth/password resets, cannot-lose or regulated data, managed Postgres, global/viral traffic, email deliverability, team preview deploys, or sensitive credential handling. The video frames the VPS pattern as appropriate for solo/operator-controlled apps and content/wiki-class sites first.
