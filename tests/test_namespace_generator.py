#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "build_from_pixi_vault.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("build_from_pixi_vault", GENERATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_fixture_source(base: Path) -> Path:
    source = base / "source" / "wikis"
    ns = source / "sample-namespace"
    (ns / "wiki" / "concepts").mkdir(parents=True)
    (ns / "raw").mkdir(parents=True)
    (ns / "README.md").write_text(
        """---
title: Sample Namespace
created: 2026-06-16
updated: 2026-06-16
type: namespace
status: active
namespace: sample-namespace
category: test
---

# Sample Namespace

A fixture namespace used to test generator behavior.

### Covers

Generator route contracts.

### Not Covered

Production content.

### Current As

2026-06-16
""",
        encoding="utf-8",
    )
    (ns / "CLAUDE.md").write_text("# Sample Namespace Instructions\n", encoding="utf-8")
    (ns / "wiki" / "index.md").write_text(
        """---
title: Sample Index
created: 2026-06-16
updated: 2026-06-16
type: index
status: active
namespace: sample-namespace
---

# Sample Index

- [[concepts/test-concept|Test Concept]]
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "log.md").write_text(
        """---
title: Sample Log
created: 2026-06-16
updated: 2026-06-16
type: log
status: active
namespace: sample-namespace
---

# Sample Log
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "concepts" / "test-concept.md").write_text(
        """---
title: Test Concept
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: sample-namespace
sources:
  - Knowledge/concepts/test-concept.md
---

# Test Concept

This fixture proves raw Markdown and HTML are generated.
""",
        encoding="utf-8",
    )
    return source


def write_legacy_output(base: Path) -> Path:
    output = base / "output"
    (output / "agent").mkdir(parents=True)
    (output / "index.json").write_text(
        json.dumps(
            {
                "name": "Legacy Pixi Wiki",
                "concepts": [{"slug": "legacy-concept"}],
                "documents": [{"path": "legacy-doc"}],
                "packs": [{"slug": "projects-legacy"}],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (output / "llms.txt").write_text("# Legacy llms\n\nLegacy content stays.\n", encoding="utf-8")
    (output / "llms-full.txt").write_text("# Legacy full\n\nLegacy full stays.\n", encoding="utf-8")
    (output / "index.html").write_text(
        "<!doctype html><main><section class=\"card\"><h1>Legacy</h1></section></main>",
        encoding="utf-8",
    )
    (output / "agent" / "styles.css").write_text("body{}\n", encoding="utf-8")
    return output


def test_generator_preserves_legacy_and_adds_namespace_registry(tmp_path: Path) -> None:
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = write_legacy_output(tmp_path)

    generator.build(source, output, ["sample-namespace"])

    data = json.loads((output / "index.json").read_text(encoding="utf-8"))
    assert data["concepts"] == [{"slug": "legacy-concept"}]
    assert data["documents"] == [{"path": "legacy-doc"}]
    assert data["packs"] == [{"slug": "projects-legacy"}]
    assert data["wikis"][0]["slug"] == "sample-namespace"
    assert data["namespace_registry"]["source_path"] == "wikis/<slug>/"

    assert (output / "raw" / "sample-namespace" / "wiki" / "concepts" / "test-concept.md").exists()
    html_path = output / "wiki" / "sample-namespace" / "wiki" / "concepts" / "test-concept.md.html"
    assert html_path.exists()
    assert "Test Concept" in html_path.read_text(encoding="utf-8")


def test_generator_is_idempotent_for_namespace_sections(tmp_path: Path) -> None:
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = write_legacy_output(tmp_path)

    generator.build(source, output, ["sample-namespace"])
    generator.build(source, output, ["sample-namespace"])

    llms = (output / "llms.txt").read_text(encoding="utf-8")
    llms_full = (output / "llms-full.txt").read_text(encoding="utf-8")
    index_html = (output / "index.html").read_text(encoding="utf-8")

    assert llms.count("# Pixi Wiki Namespace Registry") == 1
    assert llms_full.count("AgentWikis namespace registry skeleton") == 1
    assert index_html.count('id="agentwikis-namespace-registry"') == 1
    assert llms.count("## Sample Namespace") == 1
