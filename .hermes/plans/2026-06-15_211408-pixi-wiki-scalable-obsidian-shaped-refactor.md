# Pixi-Wiki Scalable Obsidian-Shaped Refactor Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task after Jamie approves the route contract. Do not implement from this plan until the stale PRD/issues are replaced or amended.

**Goal:** Refactor `pixiiidust/pixi-wiki` from a flat generated surface into a scalable compiled Obsidian-shaped wiki for humans and agents.

**Architecture:** Preserve Obsidian's domain tree as the public route contract. Generate human pages and agent `llms.txt` files beside each durable wiki node. Keep raw/source mirrors for provenance and root URLs for compatibility until removal is explicitly approved.

**Tech Stack:** Python static generator in `ObsidianVault/Projects/Hermes Mission Control/kpr-render-static-html.py`, generated static files in `pixiiidust/pixi-wiki`, GitHub Pages, `gh` CLI, Python `unittest`.

---

## 0. Current state / why the old plan is stale

The existing PRD at `docs/PRD-pixi-wiki-repo-organization.md` assumes this shape:

```text
agent/concepts/*.txt
agent/packs/*.txt
root concept-*.html
raw/Knowledge/concepts/*.md
raw/Knowledge/concepts/*.txt
```

That is now rejected as too implementation-facing because it exposes duplicate-looking links such as:

```text
Agent alias
Agent text
Markdown source
```

The corrected product shape is:

```text
Obsidian source path -> public semantic wiki path -> adjacent agent entrypoint
```

Example:

```text
ObsidianVault/Knowledge/concepts/ai-native-problem-framing-framework.md
-> /pixi-wiki/wiki/knowledge/concepts/ai-native-problem-framing-framework/
-> /pixi-wiki/wiki/knowledge/concepts/ai-native-problem-framing-framework/llms.txt
```

Reference inspected: `https://agentwikis.com/wiki/llama-cpp/README.md`.

AgentWikis useful pattern:

```text
/wiki/llama-cpp/README.md       # human-rendered source-shaped page
/raw/llama-cpp/README.md        # subtle markdown provenance
/wiki/llama-cpp/llms.txt        # agent entry
/wiki/llama-cpp/llms-full.txt   # full corpus
/wiki/llama-cpp/index.json      # registry
```

Human pages show one concise `Agent access` row for useful agent files, not several duplicate source aliases.

---

## 1. Proposed route contract

### 1.1 Root wiki entrypoints

Keep these stable:

```text
/pixi-wiki/                         # human home, compatibility root
/pixi-wiki/llms.txt                 # root agent routing map, compatibility + canonical root
/pixi-wiki/llms-full.txt            # full exported corpus
/pixi-wiki/index.json               # machine registry
/pixi-wiki/raw/**                   # source/provenance mirror
```

Optional transitional aliases may remain:

```text
/pixi-wiki/agent/llms.txt
/pixi-wiki/agent/llms-full.txt
/pixi-wiki/agent/index.json
```

But `agent/concepts/*.txt` and `agent/packs/*.txt` should not be the main organization model.

### 1.2 Domain routes

Generate a public route for each top-level Obsidian domain included in the public wiki:

```text
/pixi-wiki/wiki/knowledge/
/pixi-wiki/wiki/knowledge/llms.txt
/pixi-wiki/wiki/projects/
/pixi-wiki/wiki/projects/llms.txt
/pixi-wiki/wiki/maps-of-content/
/pixi-wiki/wiki/maps-of-content/llms.txt
```

These should correspond to source packs:

```text
Knowledge/llms.txt
Projects/llms.txt
Maps of Content/llms.txt
```

### 1.3 Concept routes

Each concept gets a bundle:

```text
/pixi-wiki/wiki/knowledge/concepts/<concept-slug>/
/pixi-wiki/wiki/knowledge/concepts/<concept-slug>/index.html
/pixi-wiki/wiki/knowledge/concepts/<concept-slug>/llms.txt
```

Human page CTA should be small and clear:

```text
🤖 Agent access: llms.txt
Part of: Knowledge / Concepts
View source markdown
```

`View source markdown` should be secondary/subtle, not beside multiple agent aliases.

### 1.4 Project routes

Each public project pack gets a bundle:

```text
/pixi-wiki/wiki/projects/critical-ranger-ffm/
/pixi-wiki/wiki/projects/critical-ranger-ffm/index.html
/pixi-wiki/wiki/projects/critical-ranger-ffm/llms.txt
```

For future project pages beyond packs, the route can extend naturally:

```text
/pixi-wiki/wiki/projects/<project-slug>/<page-slug>/
/pixi-wiki/wiki/projects/<project-slug>/<page-slug>/llms.txt
```

But first slice should only cover currently exported `Projects/**/llms.txt` packs.

### 1.5 Overview + Maps of Content routes

MOCs should complement the Overview, not sit as a separate mystery bucket.

Proposed model:

- **Overview** = the whole-wiki landing map: what this wiki is, top-level domains, how humans/agents should start, and what is public vs private.
- **Maps of Content** = deeper curated traversal maps under that overview: Knowledge MOC, Projects MOC, Agent Operations MOC, Tag Index, and maintenance/process maps.

So the public hierarchy should feel like:

```text
/pixi-wiki/                         # Overview / whole-wiki landing page
/pixi-wiki/llms.txt                 # whole-wiki agent overview + routing map
/pixi-wiki/wiki/maps-of-content/    # MOC index: deeper maps of the whole wiki
/pixi-wiki/wiki/maps-of-content/llms.txt
```

If individual MOC notes are exported later:

```text
/pixi-wiki/wiki/maps-of-content/knowledge/
/pixi-wiki/wiki/maps-of-content/knowledge/llms.txt
/pixi-wiki/wiki/maps-of-content/projects/
/pixi-wiki/wiki/maps-of-content/projects/llms.txt
/pixi-wiki/wiki/maps-of-content/agent-operations/
/pixi-wiki/wiki/maps-of-content/agent-operations/llms.txt
```

Product role:

- Human Overview answers: “What am I looking at, and where should I go first?”
- Human MOCs answer: “How is this part of the wiki organized, and what paths can I traverse?”
- Agent root `llms.txt` answers: “What are the canonical domains and route contracts?”
- MOC `llms.txt` answers: “Which map should I use for this query?”

MOCs are routing/cortex pages. They map the whole wiki and its major branches, but they do not replace concepts, project hubs, or domain packs as source truth.

### 1.6 Raw/provenance routes

Keep source-shaped mirrors:

```text
/pixi-wiki/raw/Knowledge/concepts/foo.md
/pixi-wiki/raw/Knowledge/concepts/foo.txt
/pixi-wiki/raw/Projects/Critical Ranger FFM/llms.txt
/pixi-wiki/raw/Maps of Content/llms.txt
```

Raw paths may contain spaces because fidelity matters here.

Raw/source paths belong in:

- `index.json`
- subtle `view as markdown` link
- verification/debug flows

They should not dominate human navigation.

---

## 2. Required content refactor: align Obsidian MOCs + rewrite the `llms.txt` hierarchy

This refactor is not only paths. The Obsidian source vault should use the same information architecture as the compiled public wiki.

Source-vault model:

- **Home / root Overview** = front door for the whole vault.
- **Knowledge/index.md** = overview for the Knowledge domain.
- **Projects/README.md or Projects/llms.txt** = overview for the Projects domain.
- **Maps of Content/Maps of Content.md** = index of maps, i.e. the vault map room.
- **Individual MOCs** = branch maps: Knowledge MOC, Projects MOC, Agent Operations MOC, Tag Index, etc.
- **Concepts/project hubs** = actual content/source nodes.

So MOCs should be used likewise in Obsidian:

```text
Home / root overview
└── Maps of Content index
    ├── Knowledge MOC
    ├── Projects MOC
    ├── Agent Operations MOC
    ├── Tag Index
    └── MOC Maintenance Process
```

MOCs should map the vault/wiki graph and route traversal. They should not become content dumps, status logs, or replacements for concept notes and project hubs.

The pack files also need to match the new public wiki contract.

Likely source files to inspect/rewrite:

```text
ObsidianVault/llms.txt
ObsidianVault/Knowledge/llms.txt
ObsidianVault/Projects/llms.txt
ObsidianVault/Projects/*/llms.txt
ObsidianVault/Maps of Content/llms.txt
```

### Root `llms.txt`

Should answer:

- What is this wiki?
- What domains are public?
- Where should an agent start?
- What is source truth vs derived output?
- What is not covered?

It should link to:

```text
/wiki/knowledge/llms.txt
/wiki/projects/llms.txt
/wiki/maps-of-content/llms.txt
/index.json
/llms-full.txt
```

### Knowledge domain pack

Should answer:

- What belongs in Knowledge?
- Difference between concepts, raw sources, MOCs, and projects.
- How to use concepts as durable synthesis.
- When to verify against project packs/GitHub/live tools.

It should link to:

```text
/wiki/knowledge/concepts/<slug>/llms.txt
/wiki/maps-of-content/knowledge/llms.txt     # only if individual MOC route exists later
/raw/Knowledge/...                           # provenance, not primary discovery
```

### Projects domain pack

Should answer:

- What project packs are public.
- Which project is active vs parked vs reference.
- Where durable project truth lives: GitHub issues, PRDs, Obsidian hubs, live demos.
- What an agent should verify live.

### Maps of Content pack

This one needs conceptual cleanup.

Proposed role:

```text
Maps of Content are routing maps for humans/agents. They do not replace concepts or project hubs; they help choose which branch to read next.
```

It should link to:

- Knowledge MOC
- Projects MOC
- Agent Operations MOC
- Tag Index
- MOC Maintenance Process

Only if those notes are public-safe and intentionally exported.

---

## 3. Issue strategy

The current issue tree should be paused/replaced because #4/#5/#6 assume the stale `site/agent/raw` cleanup path.

### Proposed tracker update

Keep:

```text
#1 Organize pixi-wiki into site / agent / raw layers
```

But amend it into:

```text
#1 Refactor pixi-wiki into an Obsidian-shaped compiled wiki
```

Or create a new parent and mark #1 superseded. Prefer amending #1 to avoid tracker sprawl.

### Proposed child issues

#### Issue A — HITL: Lock public route contract

Acceptance:

- Decide whether canonical public routes use `/wiki/...` prefix or no prefix, e.g. `/knowledge/...`.
- Decide whether root `/agent/*` remains as transitional alias or is removed later.
- Decide MOC role in public wiki.
- Decide compatibility policy for old root `concept-*.html` pages.

#### Issue B — AFK: Add route contract tests first

Acceptance:

- Tests assert domain routes exist.
- Tests assert concept bundle routes exist.
- Tests assert project pack bundle routes exist.
- Tests assert MOC route exists.
- Tests assert old URLs still exist as compatibility copies.
- Tests assert concept pages do not include `Agent alias` / `Agent text` / `Markdown source` as primary CTAs.

#### Issue C — AFK: Refactor generator path model

Acceptance:

- Add route helpers mapping source paths to public paths.
- Generate `wiki/knowledge/`, `wiki/projects/`, `wiki/maps-of-content/`.
- Generate per-document `index.html` and `llms.txt` bundles where appropriate.
- Keep root compatibility outputs.

#### Issue D — AFK/HITL hybrid: Rewrite generated `llms.txt` hierarchy

Acceptance:

- Root `llms.txt` routes to domain packs.
- Knowledge `llms.txt` routes to concept bundles.
- Projects `llms.txt` routes to project bundles.
- Maps of Content `llms.txt` defines MOC purpose and routes to public MOC pages if exported.
- Jamie/Pixoid review required before closing because this affects knowledge semantics.

#### Issue E — AFK: Clean human page CTA/navigation

Acceptance:

- Concept pages show one clean agent link: local `llms.txt`.
- Project/domain/MOC pages show agent access consistent with AgentWikis pattern.
- `view as markdown` is subtle/provenance, not a primary duplicate agent link.
- Sidebar has clear domain sections and a small For Agents section.

#### Issue F — AFK: Update `index.json` schema

Acceptance:

Each document record exposes:

```json
{
  "source_path": "Knowledge/concepts/foo.md",
  "html_path": "wiki/knowledge/concepts/foo/index.html",
  "url_path": "wiki/knowledge/concepts/foo/",
  "llms_path": "wiki/knowledge/concepts/foo/llms.txt",
  "raw_source_path": "raw/Knowledge/concepts/foo.md",
  "type": "concept",
  "domain": "Knowledge"
}
```

Do not privilege flat `agent_text_path` as the main concept route.

#### Issue G — AFK: Deploy and live-verify compatibility

Acceptance:

- GitHub Pages deploy succeeds.
- Live new routes return 200.
- Live old root routes return 200.
- Live raw routes return 200.
- Browser verifies no duplicate CTA confusion.

#### Issue H — HITL: Decide root cleanup after proof

Acceptance:

- Decide whether old root files stay forever as compatibility copies.
- Decide whether GitHub Actions should generate root copies during deploy.
- No deletion until Jamie approves.

---

## 4. Implementation sequencing

Do not jump straight to generator edits. Use this sequence:

1. Update tracker/PRD to supersede the stale flat-agent model.
2. Write tests for desired route contract while current repo fails.
3. Refactor generator path helpers.
4. Generate new route tree while preserving old files.
5. Update root/domain/project/MOC `llms.txt` content contract.
6. Clean human UI CTAs.
7. Regenerate/copy public output.
8. Run local generator checks, unit tests, and link checks.
9. Commit/push `ObsidianVault` generator/source changes.
10. Commit/push `pixi-wiki` public generated output.
11. Wait for Pages deploy.
12. Live-check new + old URLs.
13. Only then update/close issues.

---

## 5. Files likely to change

### In `ObsidianVault`

Primary generator:

```text
Projects/Hermes Mission Control/kpr-render-static-html.py
```

Likely source packs:

```text
llms.txt
Knowledge/llms.txt
Projects/llms.txt
Projects/Critical Ranger FFM/llms.txt
Projects/Hermes Mission Control/llms.txt
Projects/Planned Program Intel/llms.txt
Maps of Content/llms.txt
```

Possible public-safe MOC source notes later:

```text
Maps of Content/Knowledge MOC.md
Maps of Content/Projects MOC.md
Maps of Content/Agent Operations MOC.md
Maps of Content/Tag Index.md
Maps of Content/MOC Maintenance Process.md
```

Caution: current ObsidianVault working tree has unrelated dirty files. Before implementation, inspect/stage only intended files.

### In `pixi-wiki`

Generated new paths:

```text
wiki/knowledge/index.html
wiki/knowledge/llms.txt
wiki/knowledge/concepts/<slug>/index.html
wiki/knowledge/concepts/<slug>/llms.txt
wiki/projects/index.html
wiki/projects/llms.txt
wiki/projects/<slug>/index.html
wiki/projects/<slug>/llms.txt
wiki/maps-of-content/index.html
wiki/maps-of-content/llms.txt
```

Compatibility paths retained:

```text
index.html
llms.txt
llms-full.txt
index.json
concept-*.html
knowledge.html
projects.html
maps-of-content.html
raw/**
```

Tests:

```text
tests/test_agent_text_entrypoints.py
```

May rename/add:

```text
tests/test_public_route_contract.py
```

Docs:

```text
README.md
docs/PRD-pixi-wiki-repo-organization.md
```

Do not rewrite these without explicit user approval. Prefer a new PRD or targeted amendment after Jamie approves the route contract.

---

## 6. Validation plan

### Local generator

```bash
cd /root/ObsidianVault
python3 'Projects/Hermes Mission Control/kpr-render-static-html.py' --check
```

Expected:

```text
## PASS
```

### Public repo tests

```bash
cd /root/work/pixi-wiki
python3 -m unittest discover -s tests -v
git diff --check
```

Expected:

```text
OK
```

### Link check

Run a local script that crawls generated HTML/Markdown/JSON paths and asserts all internal links exist.

Required coverage:

- `wiki/knowledge/llms.txt`
- `wiki/projects/llms.txt`
- `wiki/maps-of-content/llms.txt`
- one concept bundle
- one project bundle
- old root `concept-*.html`
- `raw/...` provenance paths

### Live Pages checks

After deploy, verify cache-busted URLs:

```text
https://pixiiidust.github.io/pixi-wiki/wiki/knowledge/
https://pixiiidust.github.io/pixi-wiki/wiki/knowledge/llms.txt
https://pixiiidust.github.io/pixi-wiki/wiki/knowledge/concepts/ai-native-problem-framing-framework/
https://pixiiidust.github.io/pixi-wiki/wiki/knowledge/concepts/ai-native-problem-framing-framework/llms.txt
https://pixiiidust.github.io/pixi-wiki/wiki/projects/
https://pixiiidust.github.io/pixi-wiki/wiki/maps-of-content/
https://pixiiidust.github.io/pixi-wiki/llms.txt
https://pixiiidust.github.io/pixi-wiki/concept-knowledge-concepts-ai-native-problem-framing-framework.html
```

Browser verification:

- Concept page has one clean agent CTA.
- Sidebar makes domains understandable.
- MOC page explains its role instead of feeling like a mystery bucket.

---

## 7. Risks and tradeoffs

### Route prefix choice

`/wiki/knowledge/...` matches AgentWikis and avoids root clutter.

`/knowledge/...` mirrors Obsidian more directly and is prettier.

Recommendation: use `/wiki/...` for generated public wiki pages because it leaves room for top-level site/docs/assets later and matches AgentWikis mental model.

### MOCs may need source cleanup

The public generated wiki can only be as clear as the source MOCs. If `Maps of Content/llms.txt` does not clearly define what MOCs do, the generated page will remain confusing.

### Compatibility cost

Keeping root compatibility files means the repo remains somewhat cluttered. That is acceptable until GitHub Pages/deploy strategy is proven.

### Scope creep

Do not add search, RAG, MCP, custom domains, or a framework in this refactor. This is a static route/content contract refactor.

### Dirty ObsidianVault state

Implementation must not accidentally include unrelated dirty changes currently present in the vault:

```text
Knowledge/index.md
Knowledge/llms.txt
Knowledge/log.md
Maps of Content/Knowledge MOC.md
Maps of Content/Projects MOC.md
Projects/llms.txt
Knowledge/concepts/context-overfitting.md
Projects/Eval Trace/
```

Inspect before staging.

---

## 8. Open questions for Jamie

1. Canonical public route prefix: `/wiki/knowledge/...` or `/knowledge/...`?
2. Should `/agent/*` remain as a global alias layer, or should root `llms.txt`/`index.json` be enough?
3. Should MOCs be public pages now, or only a domain-level routing pack until the MOC source notes are cleaner?
4. Should old root concept HTML pages stay forever as compatibility copies, or only until a later cleanup gate?
5. Should the stale PRD be amended in place or replaced with a new `docs/PRD-pixi-wiki-compiled-wiki-refactor.md`?

---

## 9. Recommended next slice

Do one non-code slice first:

```text
Update the PRD + issue tree to lock the corrected Obsidian-shaped route contract.
```

Deliverables:

- New or amended PRD.
- Parent issue #1 updated with the new contract.
- Current child issues #4/#5/#6 marked blocked/superseded if they assume the stale model.
- New child issues A-H published in dependency order.

Only after that should Tinker touch the generator.
