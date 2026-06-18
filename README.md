# Pixi Wiki

Pixi Wiki publishes curated Markdown knowledge bases as two connected surfaces: a browsable web wiki for humans and agent-readable entrypoints for AI systems.

It turns each knowledge base into:

- readable HTML pages for people;
- raw Markdown mirrors for source-backed retrieval;
- `llms.txt` routing files for agent onboarding;
- `llms-full.txt` full-corpus exports for long-context agents;
- `index.json` registries for tools, scripts, and retrieval systems;
- a local read-only MCP server so agents can list, search, and read the same Markdown KBs.

- Human site: https://pixiiidust.github.io/pixi-wiki/
- Agent registry: https://pixiiidust.github.io/pixi-wiki/llms.txt
- Machine registry: https://pixiiidust.github.io/pixi-wiki/index.json
- Full corpus: https://pixiiidust.github.io/pixi-wiki/llms-full.txt
- Agent setup guide: https://pixiiidust.github.io/pixi-wiki/docs/AGENT_SETUP.html
- Replicate this approach: https://pixiiidust.github.io/pixi-wiki/docs/REPLICATE_APPROACH.html
- MCP server reference: https://pixiiidust.github.io/pixi-wiki/docs/MCP_SERVER.md

## Deployment status

The web wiki and docs are deployed on GitHub Pages. The MCP server is **not** a hosted web service; it is a local stdio MCP server that runs on the same machine as your agent client.

To use it, clone the repo and point your MCP client at the local script:

```bash
git clone https://github.com/pixiiidust/pixi-wiki.git
cd pixi-wiki
python3 -m pip install mcp
python3 scripts/pixi_wiki_mcp.py --self-test
```

Then configure your MCP client to launch:

```bash
python3 /path/to/pixi-wiki/scripts/pixi_wiki_mcp.py
```

No separate server deploy is needed unless you later want remote/shared HTTP MCP access.

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

## Copy this approach

Pixi Wiki is meant to be reusable. You can adapt the pattern for your own Markdown knowledge bases:

1. Keep your source notes/docs in stable Markdown folders.
2. Generate a human web wiki from those folders.
3. Preserve raw Markdown mirrors for source-backed agent reading.
4. Generate `llms.txt`, `llms-full.txt`, and `index.json` as agent entrypoints.
5. Run the local read-only MCP server so agents can list, search, and read your KBs.

See the replication guide: [`docs/REPLICATE_APPROACH.html`](docs/REPLICATE_APPROACH.html).

## Current namespaces

- `pixi-vault` — vault architecture, Wiki Compiler Maps, source/output boundary, publishing model.
- `agent-workflows` — Pixoid crew workflows, routing, memory boundaries, KPR, agent operations.
- `eval-trace` — evals, traces, workflow quality, context-overfitting checks.
- `ai-native-product-surfaces` — AI-native product framing and project surfaces such as Planned Program Intel and myAbode.
- `rl-sim-labs` — reinforcement-learning simulation projects such as Critical Ranger FFM.
- `curated-tuning-datasets` — source inventories and readiness maps for future tuning datasets, including LKY archive work.
- `local-ai-infrastructure` — local LLMs, retrieval, RAG over AgentWikis, local-first AI setup.

## Local development

### Run the web app locally

Pixi Wiki is a static site. Serve the repository root:

```bash
cd /path/to/pixi-wiki
python3 -m http.server 8000
```

Open `http://localhost:8000/`.

### Run the MCP server locally

The read-only MCP server exposes the generated Markdown KBs to local agent clients.

```bash
cd /path/to/pixi-wiki
python3 scripts/pixi_wiki_mcp.py
```

Self-test without starting MCP stdio:

```bash
python3 scripts/pixi_wiki_mcp.py --self-test
```

Agent workflow guidance is documented in [`docs/AGENT_SETUP.html`](docs/AGENT_SETUP.html). Full setup, tool list, Hermes config, KB editing flow, and assumptions are documented in [`docs/MCP_SERVER.md`](docs/MCP_SERVER.md).

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
