# Pixi Wiki

Pixi Wiki turns Jamie's private `pixi-vault` notes into a public, AgentWikis-style wiki-of-wikis that humans can browse and agents can read directly.

It compiles curated vault namespaces into:

- readable HTML pages for people;
- raw Markdown mirrors for provenance and source inspection;
- `llms.txt` routing files for agents;
- `llms-full.txt` full-corpus exports for long-context agents;
- `index.json` registries for tools, scripts, and future retrieval systems.

- Human site: https://pixiiidust.github.io/pixi-wiki/
- Agent registry: https://pixiiidust.github.io/pixi-wiki/llms.txt
- Machine registry: https://pixiiidust.github.io/pixi-wiki/index.json
- Full corpus: https://pixiiidust.github.io/pixi-wiki/llms-full.txt

## How it works

```txt
pixi-vault/                         private source of truth
├── Knowledge/                       reusable concepts
├── Projects/                        project source notes
├── Wiki Compiler Maps/              source-to-namespace routing
└── wikis/<namespace>/               compiled namespace source
        ↓
pixi-wiki/                          generated public mirror
├── llms.txt                         compact registry for agents
├── llms-full.txt                    full concatenated corpus
├── index.json                       machine-readable wiki registry
├── raw/<namespace>/**               raw Markdown pages
└── wiki/<namespace>/**              rendered HTML pages
```

The source vault stays messy enough for real thinking. The public wiki is the cleaned, compiled layer: scoped namespaces, page metadata, sidebar navigation, raw Markdown, and agent entrypoints.

## Why this is useful

Pixi Wiki is meant to make personal/project knowledge easier for both humans and AI agents to use.

Potential uses:

- **Reduce hallucinations:** agents retrieve from maintained wiki pages instead of guessing from stale chat context or raw dumps.
- **RAG over wiki pages:** compiled pages become a better retrieval corpus than unstructured notes because they include scope, frontmatter, source links, freshness, and namespace boundaries.
- **Agent onboarding:** `llms.txt` gives agents a small routing contract before they read the full corpus.
- **Project memory:** decisions, concepts, entities, summaries, and syntheses stay findable across sessions.
- **Public portfolio surface:** selected work can be shown as a coherent knowledge system, not scattered repo files.
- **Evaluation target:** retrieval/eval tools can test whether agents answer from the right namespace and cite the right source.

## Current namespaces

- `pixi-vault` — vault architecture, Wiki Compiler Maps, source/output boundary, publishing model.
- `agent-workflows` — Pixoid crew workflows, routing, memory boundaries, KPR, agent operations.
- `eval-trace` — evals, traces, workflow quality, context-overfitting checks.
- `ai-native-product-surfaces` — AI-native product framing and project surfaces such as Planned Program Intel and myAbode.
- `rl-sim-labs` — reinforcement-learning simulation projects such as Critical Ranger FFM.
- `curated-tuning-datasets` — source inventories and readiness maps for future tuning datasets, including LKY archive work.
- `local-ai-infrastructure` — local LLMs, retrieval, RAG over AgentWikis, local-first AI setup.

## Source of truth

This repository is a **clean generated mirror**. Do not hand-edit generated namespace output here unless you are also updating the generator/source so the change survives rebuilds.

Canonical authoring source lives in:

```txt
/root/ObsidianVault/wikis/<namespace>/
```

Build command:

```bash
python3 scripts/build_from_pixi_vault.py --source /root/ObsidianVault/wikis --output /root/pixi-wiki
```

Verification:

```bash
pytest -q
```

## Public contract

```txt
pixi-wiki/
├── README.md          # repo explanation
├── .nojekyll          # GitHub Pages serves raw Markdown files
├── index.html         # human namespace registry
├── index.json         # machine namespace registry
├── llms.txt           # compact agent registry
├── llms-full.txt      # concatenated namespace corpus
├── raw/<namespace>/** # raw Markdown provenance mirror
└── wiki/<namespace>/**# rendered HTML pages
```

## What is intentionally gone

Old flat root HTML artifacts are not canonical and should not reappear:

```txt
concept-*.html
projects-*.html
knowledge.html
projects.html
maps-of-content.html
root.html
agent/
legacy/
```

If compatibility shims are ever reintroduced, they must live behind an explicit documented compatibility policy and have regression coverage.
