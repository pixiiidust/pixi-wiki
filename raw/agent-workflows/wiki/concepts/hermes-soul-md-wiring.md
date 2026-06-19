---
title: Hermes SOUL.md Wiring
created: 2026-06-18
updated: 2026-06-18
type: concept
status: compiled
namespace: agent-workflows
tags: [agent-systems, governance, workflow]
sources:
  - /root/.hermes/knowledge/concepts/hermes-soul-md-wiring.md
  - Knowledge/concepts/hermes-soul-md-wiring.md
confidence: high
---

# Hermes SOUL.md Wiring

## Definition

Hermes agent identity is wired through an uppercase `SOUL.md` file, not lowercase `soul.md`.

This matters on Linux because paths are case-sensitive. A lowercase search can falsely report that profile identity files are missing even when `SOUL.md` exists.

## Current synthesis

| Scope | Canonical path |
|---|---|
| Default profile | `$HERMES_HOME/SOUL.md`, usually `~/.hermes/SOUL.md` |
| Named profile | `~/.hermes/profiles/<name>/SOUL.md` |

`SOUL.md` is the identity/system-prompt surface for a Hermes profile. It should be understood together with profile memory, tools, model/provider configuration, and route contracts. The SOUL file says who the profile is; an [[agent-capability-route-pattern]] says when that profile may act.

## Application

When auditing or debugging profile identity:

1. use uppercase `SOUL.md` in file searches;
2. verify the active profile with Hermes profile/runtime commands when available;
3. distinguish default Pixoid identity from named peer identities;
4. compare requested profile and actual profile before claiming a route ran under a named peer;
5. treat missing/changed SOUL files as profile/config work, not as a generic knowledge-page edit.

## Boundaries

- Do not write lowercase `soul.md` guidance.
- Do not modify `SOUL.md`, profile config, providers, gateways, cron, or secrets from this concept page.
- Do not infer a live route from the presence of a `SOUL.md` file. Profile identity exists separately from trigger/routing proof.
- Do not claim Quill, Boba, Tinker, or another peer profile executed work unless route evidence verifies the actual profile.
- Keep profile-specific persona details in the profile and route artifacts, not in generic concept pages.

## Related pages

- [[agent-capability-route-pattern]]
- [[peer-profiles-vs-child-processes]]
- [[profile-memory-boundaries]]
- [[runtime-memory-knowledge-routing]]
- [[workspace-autonomy-levels]]

## Sources

- `/root/ObsidianVault/Knowledge/concepts/hermes-soul-md-wiring.md`
