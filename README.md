# Pixi Wiki

Public, generated AgentWikis-style registry for Jamie's compiled `pixi-vault` namespaces.

- Human site: https://pixiiidust.github.io/pixi-wiki/
- Agent registry: https://pixiiidust.github.io/pixi-wiki/llms.txt
- Machine registry: https://pixiiidust.github.io/pixi-wiki/index.json
- Full corpus: https://pixiiidust.github.io/pixi-wiki/llms-full.txt

## Source of truth

This repository is a **clean generated mirror**. Do not hand-edit generated namespace output here.

Canonical authoring source lives in:

```txt
ObsidianVault/wikis/<namespace>/
```

Build command:

```bash
python3 scripts/build_from_pixi_vault.py --source /root/ObsidianVault/wikis --output /root/work/pixi-wiki
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

## Current namespaces

- `pixi-vault`
- `agent-workflows`
- `eval-trace`
- `ai-native-product-surfaces`
- `rl-sim-labs`
- `curated-tuning-datasets`
- `local-ai-infrastructure`
