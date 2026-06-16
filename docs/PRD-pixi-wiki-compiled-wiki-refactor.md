# PRD — Pixi-Wiki Obsidian-Shaped Compiled Wiki Refactor

## Problem Statement

Jamie wants `pixiiidust/pixi-wiki` to work as a public, scalable, agent-readable wiki compiled from her Obsidian vault. The current generated site is functional, but its structure leaks implementation details instead of preserving the vault’s information architecture.

The first organization pass created a flat `agent/` alias layer. That improved URL availability, but exposed confusing duplicate links such as `Agent alias`, `Agent text`, and `Markdown source`. For many pages those links resolve to effectively the same body, so the human UI looks noisy and the agent contract is unclear.

The deeper problem is not just concept pages. The whole wiki needs a consistent model across:

- root overview;
- Knowledge concepts;
- Projects and project packs;
- Maps of Content;
- domain `llms.txt` files;
- `index.json` registry records;
- raw/provenance mirrors;
- compatibility URLs already published through GitHub Pages.

The public wiki should feel like a compiled Obsidian vault, not a separate website architecture. Overview should be the front door. Maps of Content should act as the map room/navigation cortex. Concepts and projects should be durable content nodes. `llms.txt` files should be routing contracts beside those nodes.

## Solution

Refactor `pixi-wiki` into an Obsidian-shaped compiled wiki that preserves the vault’s domain tree while keeping existing public URLs working.

Use this route model:

```text
Obsidian source path
→ public semantic wiki path for humans
→ adjacent llms.txt path for agents
→ raw path for provenance/debugging
```

Example:

```text
ObsidianVault/Knowledge/concepts/ai-native-problem-framing-framework.md
→ /pixi-wiki/wiki/knowledge/concepts/ai-native-problem-framing-framework/
→ /pixi-wiki/wiki/knowledge/concepts/ai-native-problem-framing-framework/llms.txt
→ /pixi-wiki/raw/Knowledge/concepts/ai-native-problem-framing-framework.md
```

Root public entrypoints remain stable:

```text
/pixi-wiki/
/pixi-wiki/llms.txt
/pixi-wiki/llms-full.txt
/pixi-wiki/index.json
/pixi-wiki/raw/**
```

New compiled wiki routes should include:

```text
/pixi-wiki/wiki/knowledge/
/pixi-wiki/wiki/knowledge/llms.txt
/pixi-wiki/wiki/knowledge/concepts/<concept-slug>/
/pixi-wiki/wiki/knowledge/concepts/<concept-slug>/llms.txt
/pixi-wiki/wiki/projects/
/pixi-wiki/wiki/projects/llms.txt
/pixi-wiki/wiki/projects/<project-slug>/
/pixi-wiki/wiki/projects/<project-slug>/llms.txt
/pixi-wiki/wiki/maps-of-content/
/pixi-wiki/wiki/maps-of-content/llms.txt
```

The `agent/` folder may remain as a transitional global alias for root-level agent files, but flat per-document aliases like `agent/concepts/*.txt` and `agent/packs/*.txt` are not the primary scalable model.

Human pages should show one concise agent access path for the local node and keep source/provenance links subtle. `index.json` should carry the full mapping between human route, agent route, and raw source route.

## User Stories

1. As Jamie, I want the public wiki to mirror my Obsidian information architecture, so that I do not have to maintain two competing mental models.
2. As Jamie, I want the root overview to explain the whole wiki, so that humans and agents know where to start.
3. As Jamie, I want Maps of Content to complement the overview, so that MOCs map the whole wiki and its major branches instead of feeling like a mystery folder.
4. As Jamie, I want MOCs to be navigation cortex pages, so that they route readers to concepts, projects, domains, and tags without becoming content dumps.
5. As Jamie, I want Knowledge concepts to compile into stable concept folders, so that each concept has a durable human page and adjacent agent entrypoint.
6. As Jamie, I want project packs to compile into stable project folders, so that public project knowledge scales beyond one-off flat HTML files.
7. As Jamie, I want the public wiki to preserve existing URLs, so that old links, GitHub Pages paths, and prior agent references do not break during the refactor.
8. As Jamie, I want raw Markdown/source mirrors to remain available, so that provenance can be checked without cluttering the main reading path.
9. As a human reader, I want concept pages to show one clear agent access link, so that I am not confused by duplicate-looking `Agent alias`, `Agent text`, and `Markdown source` links.
10. As a human reader, I want source Markdown links to be secondary, so that provenance is available without dominating the page CTA.
11. As a human reader, I want the sidebar and breadcrumbs to show domains, concepts, projects, and MOCs clearly, so that I can understand where I am in the wiki.
12. As an agent, I want root `llms.txt` to route me through the wiki’s domains, so that I can choose the right domain pack before loading detailed content.
13. As an agent, I want every compiled durable node to expose a local `llms.txt`, so that I can load the agent contract for that node without guessing flat alias paths.
14. As an agent, I want Knowledge domain `llms.txt` to route to public concept bundles, so that concepts are discoverable through the domain tree.
15. As an agent, I want Projects domain `llms.txt` to route to public project bundles, so that project truth is discoverable and scoped.
16. As an agent, I want Maps of Content `llms.txt` to describe available map routes, so that I can use MOCs for traversal rather than as source truth.
17. As an agent, I want `index.json` to expose human URL, agent `llms.txt`, raw source, type, domain, and source path, so that tool routing is unambiguous.
18. As an agent, I want `llms.txt` files to remain routing truth, so that they point to canonical sources instead of replacing GitHub issues, PRDs, project hubs, or source files.
19. As Quill, I want the Obsidian source-vault model and public wiki model to align, so that documentation updates do not need translation between two structures.
20. As Quill, I want MOC source notes to have a clear role, so that vault maps can be maintained as traversal maps rather than status logs.
21. As Tinker, I want route-contract tests before generator changes, so that refactoring the generator cannot silently break published URLs.
22. As Tinker, I want generator path helpers to map source paths to public routes deterministically, so that future domains and notes scale without bespoke string hacks.
23. As Boba, I want the refactor to avoid unnecessary infrastructure, so that a static wiki does not turn into a framework, crawler, MCP, vector DB, or search project prematurely.
24. As Pixoid, I want old issues that assume the flat `agent/` model to be superseded, so that agents do not implement the wrong architecture.
25. As Pixoid, I want GitHub issues to encode blockers, stop conditions, and route labels, so that future crew work can proceed safely one slice at a time.
26. As a maintainer, I want dirty/unrelated ObsidianVault changes protected during implementation, so that generator/source commits do not accidentally include unrelated vault edits.
27. As a maintainer, I want live GitHub Pages verification after deploy, so that success means public URLs work, not just local files changed.
28. As a maintainer, I want root cleanup to remain a later HITL decision, so that compatibility is not sacrificed for repo neatness.

## Implementation Decisions

- Treat this PRD as superseding the earlier flat-layer PRD for future work. The earlier PRD remains historical context, not the current requirements spine.
- Preserve Obsidian-shaped domain semantics in generated public routes.
- Use `/wiki/...` as the recommended generated route prefix because it matches the AgentWikis reference pattern and keeps root space available for compatibility and site-level assets.
- Keep root public URLs working throughout the refactor.
- Keep `raw/**` as a source-shaped provenance mirror; raw paths may preserve spaces and source capitalization.
- Keep source/provenance links available, but make them secondary in human pages.
- Generate local `llms.txt` files beside durable public nodes: domains, concepts, project packs, and MOC indexes.
- Make root `llms.txt` the whole-wiki agent overview and route contract.
- Make domain `llms.txt` files route to their durable child nodes.
- Make MOCs complement the overview: the overview is the front door; MOCs are the internal map room/navigation cortex.
- Do not use flat `agent/concepts/*.txt` or `agent/packs/*.txt` as the primary organization model. Existing flat aliases may remain temporarily for compatibility but should not be promoted in page CTAs.
- Update `index.json` schema to expose the seams explicitly: source path, human URL path, human HTML path, local `llms.txt` path, raw source path, type, domain, and compatibility paths when present.
- Patch the ObsidianVault generator before relying on any public repo generated output, otherwise manual public repo fixes will be overwritten.
- Keep the generator static and file-based. No runtime service is required.
- Treat route prefix choice, MOC export scope, and root cleanup as explicit decision seams with tracker visibility.
- Protect unrelated ObsidianVault dirty state by staging only intended files during implementation.

## Testing Decisions

Tests should validate route contracts and external behavior, not private implementation details.

Good tests:

- Assert root compatibility files still exist: `/`, `llms.txt`, `llms-full.txt`, `index.json`, old concept HTML pages, and `raw/**` mirrors.
- Assert new domain routes exist for Knowledge, Projects, and Maps of Content.
- Assert each public concept has a bundled human route and local `llms.txt` route.
- Assert each exported project pack has a bundled human route and local `llms.txt` route.
- Assert MOC routes explain traversal/map role instead of behaving like miscellaneous content dumps.
- Parse `index.json` and assert each document record includes human URL, agent `llms.txt`, raw source, type, domain, and source path fields.
- Assert human concept pages do not expose `Agent alias`, `Agent text`, and `Markdown source` as parallel primary CTAs.
- Crawl generated HTML and text files locally for internal missing links.
- Run the ObsidianVault generator check before copying output into `pixi-wiki`.
- Run public repo tests before commit.
- Verify GitHub Pages deploy succeeds.
- Verify live cache-busted new and old URLs return 200 before closing implementation issues.

Existing test surface to evolve:

- Current agent-entrypoint tests should be replaced or expanded into route-contract tests.
- Link checking should cover both compatibility paths and new `/wiki/...` paths.
- Browser/DOM checks should inspect CTA labels and hrefs for concept pages and the MOC index.

## Out of Scope

- No MCP server.
- No RAG/vector database/search index.
- No crawler or link-rot automation beyond local/live link checks.
- No static-site framework migration.
- No custom domain or DNS change.
- No broad visual redesign beyond navigation/CTA clarity required by the route contract.
- No deletion of existing root public URLs in the initial refactor.
- No root cleanup without a later explicit HITL decision.
- No GitHub Pages deploy-mode change unless a later issue explicitly approves it.
- No broad rewrite of unrelated Obsidian vault content.
- No promotion of raw Markdown mirrors as primary human navigation.
- No treating `llms.txt` files as replacements for PRDs, GitHub issues, project hubs, source notes, or live verification.

## Further Notes

AgentWikis reference pattern inspected: `https://agentwikis.com/wiki/llama-cpp/README.md`.

Useful borrowed behavior:

- Human route mirrors wiki path.
- Breadcrumbs show location.
- A subtle `view as markdown` link exposes provenance.
- Agent access row links only to useful agent files.
- Sidebar includes a compact `FOR AGENTS` section.
- Raw Markdown exists but does not clutter primary CTAs.

Recommended next tracker shape:

1. Supersede stale flat-agent issues.
2. Lock route contract and MOC role.
3. Add route-contract tests.
4. Refactor generator path model.
5. Rewrite `llms.txt` hierarchy.
6. Clean human CTA/navigation.
7. Update `index.json` schema.
8. Deploy and live-verify compatibility.
9. Decide root cleanup only after proof.

Implementation should proceed one discrete slice per session. Tinker should not touch the generator until the route contract issue is accepted.
