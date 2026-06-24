#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.build_signal_graph import build_signal_graph


def write_fixture(raw: Path) -> None:
    namespace = raw / "sample"
    (namespace / "wiki" / "concepts").mkdir(parents=True)
    (namespace / "README.md").write_text(
        """---
title: Sample Namespace
type: namespace-overview
status: active
namespace: sample
tags: [sample, workflow, specific-tag]
sources:
  - Projects/Sample/Index.md
---

# Sample Namespace

## Rules

This generic heading should be filtered.

## Useful Lens

A meaningful section should remain.
""",
        encoding="utf-8",
    )
    (namespace / "wiki" / "index.md").write_text(
        """---
title: Sample Index
type: index
status: compiled
namespace: sample
---

# Sample Index

- [[concepts/target-concept|Target Concept]]
""",
        encoding="utf-8",
    )
    (namespace / "wiki" / "concepts" / "target-concept.md").write_text(
        """---
title: Target Concept
type: concept
status: compiled
namespace: sample
tags: [sample, governance]
sources:
  - Knowledge/concepts/target-concept.md
  - https://github.com/example/project
---

# Target Concept

## Boundaries

Generic heading.

## Decision Surface

Specific heading.
""",
        encoding="utf-8",
    )


def test_signal_graph_filters_metadata_and_generic_glue(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    out = tmp_path / "graphify-out"
    write_fixture(raw)

    summary = build_signal_graph(raw, out)
    graph = json.loads((out / "graph.json").read_text(encoding="utf-8"))
    labels = {node["label"] for node in graph["nodes"]}
    edges = {(edge["source"], edge["target"], edge["relation"]) for edge in graph["links"]}

    assert summary["docs"] == 3
    assert "type" not in summary["kind_counts"]
    assert "status" not in summary["kind_counts"]
    assert "type: concept" not in labels
    assert "status: compiled" not in labels
    assert "Rules" not in labels
    assert "Boundaries" not in labels
    assert "Useful Lens" in labels
    assert "Decision Surface" in labels
    assert "#workflow" not in labels
    assert "#specific-tag" in labels
    assert "Source: Knowledge" in labels
    assert "Source: Projects" in labels
    assert "Source: GitHub repo" in labels
    assert (
        "doc:sample/wiki/index.md",
        "doc:sample/wiki/concepts/target-concept.md",
        "references_document",
    ) in edges


def test_signal_graph_writes_summary_and_graph(tmp_path: Path) -> None:
    raw = tmp_path / "raw"
    out = tmp_path / "graphify-out"
    write_fixture(raw)

    build_signal_graph(raw, out)

    assert (out / "graph.json").exists()
    assert (out / "SIGNAL_MARKDOWN_GRAPH_SUMMARY.json").exists()
    summary = json.loads((out / "SIGNAL_MARKDOWN_GRAPH_SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["edge_counts"]["references_document"] == 1
