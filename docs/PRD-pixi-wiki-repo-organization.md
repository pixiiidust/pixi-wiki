# PRD — Pixi-Wiki Repo Organization

## Problem Statement

Jamie wants `pixiiidust/pixi-wiki` to be a convenient public entry surface for agents and humans. The current repo works, but it looks disorganized because generated browser pages, machine-readable agent files, registry files, and raw source mirrors all live in the repository root.

This creates three problems:

1. Humans cannot quickly tell which files are the website, which files are agent entrypoints, and which files are source mirrors.
2. Agents have clean text files available, but the canonical entry layer is not visibly organized as a foldered contract.
3. Any naive cleanup that moves files into folders could break existing GitHub Pages URLs and current agent links.

The goal is not to make the repo prettier by shuffling files. The goal is to make the repo's consumption contract obvious while preserving the public URLs that already work.

## Solution

Create a phased repo organization contract with three layers:

1. **`agent/` — clean agent entry layer**
   - Canonical start for agents.
   - Contains `llms.txt`, `llms-full.txt`, `index.json`, pack text aliases, and concept text aliases.
   - Optimized for direct LLM/tool ingestion.

2. **`site/` — human/browser layer**
   - Target home for generated HTML pages and visual assets.
   - Introduced only when the deploy/backward-compat strategy preserves existing root URLs.

3. **`raw/` — source-shaped mirror**
   - Preserves vault/source paths and provenance.
   - May contain spaces and Obsidian-shaped folders because fidelity matters more than aesthetics here.
   - Not the primary discovery surface for agents.

Existing root-level URLs must remain valid during the migration:

- `/pixi-wiki/`
- `/pixi-wiki/llms.txt`
- `/pixi-wiki/llms-full.txt`
- `/pixi-wiki/index.json`
- `/pixi-wiki/concept-*.html`
- `/pixi-wiki/raw/...`

## User Stories

1. As Jamie, I want the repo organized into clear folders, so that I can tell what each file is for at a glance.
2. As Jamie, I want existing public URLs to keep working, so that previous links and agent references do not break.
3. As an agent, I want `/agent/llms.txt` to be the obvious start point, so that I do not have to infer the entrypoint from a cluttered root.
4. As an agent, I want `/agent/concepts/*.txt` aliases, so that I can load durable concepts from stable text paths.
5. As an agent, I want `/agent/index.json` to expose `html_path`, `agent_text_path`, and `raw_source_path`, so that I can choose the right artifact for the job.
6. As a human reader, I want generated HTML pages grouped under a human-site layer eventually, so that browser pages do not dominate the repo root.
7. As a maintainer, I want `raw/` to stay source-shaped, so that generated artifacts remain traceable to their vault/source paths.
8. As Pixoid, I want the generator to enforce this layout, so that manual public-repo edits do not get overwritten later.
9. As Quill, I want the README and PRD to explain the layer boundaries, so that future scribe/source-of-truth updates do not confuse `agent/`, `site/`, and `raw/`.
10. As Tinker, I want acceptance tests for the layout, so that repo cleanup does not silently break GitHub Pages or agent entrypoints.
11. As Boba, I want the migration to avoid unnecessary infrastructure, so that a small static wiki does not become a complex deployment project without need.

## Implementation Decisions

- Use a phased migration rather than a one-shot move.
- Add `agent/` first because it improves agent ergonomics with low URL risk.
- Keep current root files working as compatibility entrypoints until a deploy strategy proves root copies can become artifacts.
- Preserve `raw/` as a source-shaped mirror even if it is less visually tidy.
- Do not rename vault-derived raw folders just for aesthetics.
- Treat `llms.txt` and `index.json` as routing/registry contracts, not canonical project truth.
- Patch the ObsidianVault generator before relying on public-repo layout changes.
- Make the generator capable of producing both root compatibility paths and foldered paths.
- Use tests to verify both the clean foldered paths and the legacy root paths.
- Consider GitHub Actions Pages deployment only when removing root generated files from git tracking becomes necessary.
- Avoid adding a site framework, search engine, crawler, vector DB, or MCP layer as part of this repo-organization work.
- Keep the repo small and static.
- Use GitHub issues in `pixiiidust/pixi-wiki` as the durable coordination truth for this migration.

## Testing Decisions

Testing should verify external behavior and artifact contracts, not implementation details.

Required checks:

- `agent/llms.txt` exists and is the clean agent start.
- `agent/index.json` exists and maps each concept to:
  - `html_path`
  - `agent_text_path`
  - `raw_source_path`
- `agent/concepts/*.txt` exists for every public concept.
- Existing root `llms.txt`, `llms-full.txt`, and `index.json` remain available during migration.
- Existing root concept HTML URLs remain available during migration.
- `raw/Knowledge/concepts/*.md` and `.txt` mirrors remain available.
- Internal links resolve locally before deployment.
- GitHub Pages deployment succeeds before claiming live success.
- Live URLs are verified with cache-busting query strings after deploy.
- Generator checks pass in `ObsidianVault` before public export.

Good tests:

- Read files from the built output and assert required paths exist.
- Parse `index.json` and assert each path points to an existing artifact.
- Crawl generated Markdown/HTML links for internal 404s.
- Verify root compatibility files match or intentionally point to their `agent/`/`site/` equivalents.

## Out of Scope

- No MCP server.
- No RAG/vector database/search index.
- No crawler or link-rot automation beyond local link checks.
- No static-site framework migration.
- No custom domain or DNS changes.
- No broad visual redesign.
- No deletion of existing root URLs during the first implementation slice.
- No renaming of source/vault paths inside `raw/` unless separately approved.
- No rewrite of `README.md`; only targeted documentation updates.
- No change to Obsidian canonical source files except generator/output updates required for this migration.

## Review Gate Before Implementation

Before implementation starts, the GitHub issue tree must make these decisions explicit:

- Whether `agent/` is added before `site/`.
- Whether root compatibility files remain tracked or become deploy artifacts later.
- Which issue, if any, is allowed to introduce GitHub Actions Pages deployment.
- Which issues are safe to run in parallel.
- Which work must stop for Jamie/Pixoid review.

## Further Notes

The repo is not broken. The current flat root is functional and safe for GitHub Pages. The real product problem is that the repository does not clearly communicate its layers.

The first implementation should therefore create the clean agent layer and documentation contract before attempting a full root cleanup. The visible mess can be reduced without breaking URLs by making `agent/` the official start point and documenting `raw/` as the provenance mirror.

A later `site/` migration is useful only if it comes with a tested compatibility strategy. Otherwise, moving HTML into folders would make the repo look cleaner while making the product worse.
