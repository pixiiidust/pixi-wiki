# Pixi-Wiki Repo Organization Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Reorganize `pixiiidust/pixi-wiki` around clear `site/`, `agent/`, and `raw/` layers while preserving existing GitHub Pages URLs and the ObsidianVault generator workflow.

**Architecture:** Use a phased migration. First add a clean `agent/` entry layer and docs without moving public URLs. Then add generator support for layered output. Only move browser HTML into `site/` when a deploy/backward-compat artifact keeps root URLs stable.

**Tech Stack:** Static HTML, GitHub Pages, Python generator in `ObsidianVault`, GitHub issues as coordination truth.

---

## Context

Current `pixi-wiki` works, but the repo root is visually noisy because generated HTML, agent entry files, registry files, and source mirrors live side-by-side. The public site currently serves from the repository root, so direct moves would break existing URLs such as `/pixi-wiki/llms.txt` and `/pixi-wiki/concept-*.html`.

Parallel review findings:

- Tinker: moving files directly is risky; preserve root URLs through deploy artifact or staged copies.
- Quill: PRD should define layer contracts and source-of-truth boundaries.
- Boba: do not overbuild; flat root HTML is ugly but URL-safe. Start with clear contracts/docs and a clean agent layer.

## Proposed Target Contract

```text
/
  README.md
  .nojekyll
  docs/
    PRD-pixi-wiki-repo-organization.md

  agent/
    llms.txt
    llms-full.txt
    index.json
    packs/*.txt
    concepts/*.txt

  site/
    index.html
    packs/*.html
    concepts/*.html
    assets/style.css

  raw/
    Knowledge/
    Projects/
    Maps of Content/
```

Compatibility rule: existing root URLs must keep working until the PRD explicitly removes them in a later approved cleanup.

## Step-by-Step Plan

### Task 1: Add the repo organization PRD and parent tracker issue

**Objective:** Establish durable requirements before implementation.

**Files:**
- Create: `docs/PRD-pixi-wiki-repo-organization.md`
- Create: `.hermes/plans/2026-06-15_203037-pixi-wiki-repo-organization.md`

**Verification:**
- `git diff --check`
- PRD exists and names compatibility, layer contracts, out-of-scope items, and testing gates.

### Task 2: Add a clean `agent/` alias layer without moving existing URLs

**Objective:** Give agents clean foldered entrypoints while preserving current root and `raw/` paths.

**Files likely to change:**
- Generator source: `/root/ObsidianVault/Projects/Hermes Mission Control/kpr-render-static-html.py`
- Generated output: `/root/ObsidianVault/Generated/kpr-static-html/agent/`
- Public repo: `agent/llms.txt`, `agent/index.json`, `agent/concepts/*.txt`, `agent/packs/*.txt`
- Tests: `tests/test_agent_text_entrypoints.py`

**Verification:**
- `python3 Projects/Hermes\ Mission\ Control/kpr-render-static-html.py --check` in `ObsidianVault`
- `python3 -m unittest tests/test_agent_text_entrypoints.py -v` in `pixi-wiki`
- Live curl confirms `/pixi-wiki/agent/llms.txt` and existing `/pixi-wiki/llms.txt` both return 200.

### Task 3: Document the layer contract in README without overwriting existing content broadly

**Objective:** Make the repo understandable at a glance.

**Files likely to change:**
- Modify: `README.md`

**Verification:**
- README explains `agent/`, `raw/`, current root compatibility, and future `site/` plan.
- No broken links.

### Task 4: Add generator support for `site/` output behind a compatibility copy

**Objective:** Prepare human HTML to live under `site/` while preserving root Pages URLs.

**Files likely to change:**
- Generator source in `ObsidianVault`
- Generated output under `Generated/kpr-static-html/site/`
- Public repo `site/`
- Tests for root/site equivalence

**Verification:**
- Root `index.html` and `site/index.html` have matching content or documented redirect/copy behavior.
- Existing root HTML URLs still return 200 locally and after Pages deploy.

### Task 5: Decide deploy strategy before removing root generated files

**Objective:** Avoid breaking GitHub Pages while cleaning root clutter.

**Options:**
- Keep root compatibility copies tracked for now.
- Add GitHub Actions Pages artifact deploy that copies `site/` and `agent/` to root at deploy time.
- Use GitHub Pages `docs/` source only if `site/` naming is not required.

**Verification:**
- If a workflow is added, Pages deploy succeeds and live URLs are verified with cache-busting query strings.

### Task 6: Optional later cleanup — remove root generated files from git tracking

**Objective:** Make the repo root visibly clean after compatibility is proven.

**Blocked by:**
- Successful deploy artifact strategy.
- Explicit approval to remove tracked root generated files.

**Verification:**
- Existing public URLs still work.
- `agent/` remains canonical for agent entry.
- `raw/` remains source-shaped mirror.

## Files Likely to Change

- `docs/PRD-pixi-wiki-repo-organization.md`
- `.hermes/plans/2026-06-15_203037-pixi-wiki-repo-organization.md`
- `README.md`
- `tests/test_agent_text_entrypoints.py`
- `/root/ObsidianVault/Projects/Hermes Mission Control/kpr-render-static-html.py`
- `/root/ObsidianVault/Generated/kpr-static-html/**`
- `agent/**`
- `site/**` later

## Tests / Validation

- PRD and plan committed/pushed before issue creation.
- GitHub issues created in `pixiiidust/pixi-wiki` and verified.
- Generator check passes in `ObsidianVault` before any public export.
- Unit tests verify agent `.txt` mirrors and link contracts.
- Link checker verifies no missing internal links.
- GitHub Pages deployment succeeds.
- Live URLs verified:
  - `/pixi-wiki/`
  - `/pixi-wiki/llms.txt`
  - `/pixi-wiki/agent/llms.txt`
  - `/pixi-wiki/raw/Knowledge/concepts/ai-native-problem-framing-framework.txt`
  - `/pixi-wiki/concept-knowledge-concepts-ai-native-problem-framing-framework.html`

## Risks and Tradeoffs

- Direct file moves can break GitHub Pages URLs.
- Adding GitHub Actions is extra machinery; only justified if root clutter must disappear from tracked files.
- `raw/` should remain vault-shaped even if it looks less tidy, because it is the provenance/source mirror.
- `site/` should be treated as a human surface, not source truth.
- `agent/` should be the clean agent start, not a second canonical knowledge base.

## Open Questions

- Should root generated files remain tracked as compatibility copies, or become deploy artifacts only?
- Is `site/` worth introducing immediately, or should the first slice stop at `agent/` + README?
- Should `agent/index.json` be a simplified alias registry or the full current manifest copied from root?
