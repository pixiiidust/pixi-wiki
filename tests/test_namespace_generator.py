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


def write_messy_output(base: Path) -> Path:
    output = base / "output"
    (output / "agent").mkdir(parents=True)
    (output / "raw" / "Knowledge").mkdir(parents=True)
    (output / "wiki" / "knowledge").mkdir(parents=True)
    (output / "legacy").mkdir(parents=True)
    (output / "index.json").write_text('{"name":"legacy","concepts":[{"slug":"old"}]}', encoding="utf-8")
    (output / "llms.txt").write_text("# Legacy llms\n", encoding="utf-8")
    (output / "llms-full.txt").write_text("# Legacy full\n", encoding="utf-8")
    (output / "index.html").write_text("<main>Legacy</main>", encoding="utf-8")
    (output / "concept-old.html").write_text("old root clutter", encoding="utf-8")
    (output / "projects-old.html").write_text("old root clutter", encoding="utf-8")
    (output / "knowledge.html").write_text("old root clutter", encoding="utf-8")
    (output / "agent" / "llms.txt").write_text("old agent layer", encoding="utf-8")
    (output / "raw" / "Knowledge" / "old.md").write_text("old raw layer", encoding="utf-8")
    (output / "wiki" / "knowledge" / "index.html").write_text("old wiki layer", encoding="utf-8")
    return output


def test_generator_rebuilds_clean_namespace_registry(tmp_path: Path) -> None:
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = write_messy_output(tmp_path)

    generator.build(source, output, ["sample-namespace"])

    data = json.loads((output / "index.json").read_text(encoding="utf-8"))
    assert data["schema_version"] == "pixi-agentwikis-registry-v1"
    assert "concepts" not in data
    assert "packs" not in data
    assert data["legacy_root_flat_pages"] == "removed"
    assert data["wikis"][0]["slug"] == "sample-namespace"
    assert data["wikis"][0]["documentCount"] == 5

    raw_path = output / "raw" / "sample-namespace" / "wiki" / "concepts" / "test-concept.md"
    html_path = output / "wiki" / "sample-namespace" / "wiki" / "concepts" / "test-concept.md.html"
    assert raw_path.exists()
    assert html_path.exists()
    assert "Test Concept" in html_path.read_text(encoding="utf-8")


def test_generator_removes_legacy_root_and_old_layers(tmp_path: Path) -> None:
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = write_messy_output(tmp_path)

    generator.build(source, output, ["sample-namespace"])

    for name in ["concept-old.html", "projects-old.html", "knowledge.html"]:
        assert not (output / name).exists(), name
    for name in ["agent", "legacy"]:
        assert not (output / name).exists(), name
    assert not (output / "raw" / "Knowledge").exists()
    assert not (output / "wiki" / "knowledge").exists()

    root_html = sorted(path.name for path in output.glob("*.html"))
    assert root_html == ["index.html"]


def test_generator_is_idempotent_for_clean_output(tmp_path: Path) -> None:
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = write_messy_output(tmp_path)

    generator.build(source, output, ["sample-namespace"])
    first = (output / "llms.txt").read_text(encoding="utf-8")
    generator.build(source, output, ["sample-namespace"])
    second = (output / "llms.txt").read_text(encoding="utf-8")

    assert first == second
    assert second.count("# Pixi Wiki Namespace Registry") == 1
    assert second.count("## Sample Namespace") == 1
