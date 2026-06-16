---
title: Hermes SOUL.md Wiring
created: 2026-06-12
updated: 2026-06-12
type: concept
tags: [agent-systems, governance, workflow]
confidence: high
status: active
---

# Hermes SOUL.md Wiring

## Definition

Hermes agent identity is wired through an uppercase `SOUL.md` file, not lowercase `soul.md`. This is a critical distinction on Linux (case-sensitive filesystem) where a lowercase search will return nothing even when the file exists.

## Canonical locations

| Scope | Path |
|---|---|
| Default profile | `$HERMES_HOME/SOUL.md` (typically `~/.hermes/SOUL.md`) |
| Per-profile | `~/.hermes/profiles/<name>/SOUL.md` |

The `SOUL.md` file holds the agent's identity/system prompt. Hermes source confirms this in `agent/prompt_builder.py::load_soul_md()`.

## Correction applied 2026-06-12

An issue was discovered where Pixoid searched for lowercase `soul.md` and incorrectly reported no soul files existed. The fix:

1. **Synced** `config.system_prompt` to `SOUL.md` for default, quill, and pika profiles.
2. **Verified** all five profiles (default, boba, quill, tinker, pika) have `config.system_prompt matches SOUL.md = True`.
3. **Patched** the local `hermes-agent` skill to document the `SOUL.md` convention and warn against lowercase `soul.md` search on Linux.

## Current profile roster (2026-06-12)

- **default** (Pixoid) — `~/.hermes/SOUL.md`
- **boba** — `~/.hermes/profiles/boba/SOUL.md`
- **quill** — `~/.hermes/profiles/quill/SOUL.md`
- **tinker** — `~/.hermes/profiles/tinker/SOUL.md`
- **pika** — `~/.hermes/profiles/pika/SOUL.md`

## Operational rule

When querying or verifying SOUL.md files:
- Always use uppercase `SOUL.md`.
- Search with `find ~/.hermes -name 'SOUL.md'` (not `soul.md`).
- Verify per-profile via `hermes profile show <name>` or directly check `~/.hermes/profiles/<name>/SOUL.md`.

## Related pages

- [[profile-memory-boundaries]] — broader boundary model for USER.md, MEMORY.md, local knowledge, and skills.
- [[agent-capability-route-pattern]] — how profiles are triggered as bounded agent capabilities.