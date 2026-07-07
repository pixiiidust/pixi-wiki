#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "build_from_pixi_vault.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("build_from_pixi_vault", GENERATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Direct unit tests of the slug function
# ---------------------------------------------------------------------------

def test_slugify_spaces_and_case() -> None:
    generator = load_generator()
    assert generator.slugify_heading("Tool Buckets") == "tool-buckets"


def test_slugify_punctuation_collapses_to_single_hyphen() -> None:
    generator = load_generator()
    assert generator.slugify_heading("Read / Write & Mutate!") == "read-write-mutate"


def test_slugify_strips_backticks_and_emphasis() -> None:
    generator = load_generator()
    assert generator.slugify_heading("Using `db` for **state**") == "using-db-for-state"


def test_slugify_leading_digits_are_kept() -> None:
    generator = load_generator()
    assert generator.slugify_heading("2024 Roadmap") == "2024-roadmap"
    assert generator.slugify_heading("1. First step") == "1-first-step"


def test_slugify_wikilink_uses_label() -> None:
    generator = load_generator()
    assert generator.slugify_heading("[[concepts/foo|Foo Bar]]") == "foo-bar"
    assert generator.slugify_heading("[[Plain Target]]") == "plain-target"


def test_slugify_empty_falls_back_to_section() -> None:
    generator = load_generator()
    assert generator.slugify_heading("***") == "section"


def test_slugify_is_deterministic_per_call() -> None:
    # The function itself carries no state: repeated calls match.
    generator = load_generator()
    assert generator.slugify_heading("Same Heading") == generator.slugify_heading("Same Heading")


# ---------------------------------------------------------------------------
# markdown_fragment: ids, anchors, dedup, and the headings seam
# ---------------------------------------------------------------------------

def test_fragment_emits_ids_and_hover_anchors() -> None:
    generator = load_generator()
    html_out, headings = generator.markdown_fragment_with_headings(
        "## Tool Buckets\n\ntext\n\n### Read `db`"
    )
    assert '<h2 id="tool-buckets">' in html_out
    assert '<h3 id="read-db">' in html_out
    assert '<a class="heading-anchor" href="#tool-buckets" aria-label="Link to this section">' in html_out
    assert '<a class="heading-anchor" href="#read-db" aria-label="Link to this section">' in html_out
    assert [h["slug"] for h in headings] == ["tool-buckets", "read-db"]


def test_fragment_dedup_suffixes_in_document_order() -> None:
    generator = load_generator()
    html_out, headings = generator.markdown_fragment_with_headings(
        "## Notes\n\n## Notes\n\n## Notes"
    )
    assert [h["slug"] for h in headings] == ["notes", "notes-2", "notes-3"]
    assert '<h2 id="notes">' in html_out
    assert '<h2 id="notes-2">' in html_out
    assert '<h2 id="notes-3">' in html_out
    # each anchor href matches its own id
    assert 'href="#notes-2"' in html_out
    assert 'href="#notes-3"' in html_out


def test_fragment_dedup_scope_is_local_no_leak_across_calls() -> None:
    generator = load_generator()
    first, _ = generator.markdown_fragment_with_headings("## Notes")
    second, _ = generator.markdown_fragment_with_headings("## Notes")
    # A fresh call starts its counter over -> no "-2" leaking in from a prior call.
    assert first == second
    assert '<h2 id="notes">' in second
    assert "notes-2" not in second


def test_markdown_fragment_str_signature_unchanged() -> None:
    generator = load_generator()
    out = generator.markdown_fragment("## Heading One")
    assert isinstance(out, str)
    assert '<h2 id="heading-one">' in out


# ---------------------------------------------------------------------------
# Build-seam test: emitted namespace HTML with a TOC
# ---------------------------------------------------------------------------

CONCEPT_WITH_SECTIONS = """---
title: Anchor Concept
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: sample-namespace
---

# Anchor Concept

Intro paragraph before any section.

## Tool Buckets

Buckets overview.

### Read `db`

Read details.

### Write **state**

Write details.

## Tool Buckets

A duplicated section heading.
"""

CONCEPT_SINGLE_SECTION = """---
title: Thin Concept
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: sample-namespace
---

# Thin Concept

Only one section heading lives here.

## Overview

Nothing more.
"""


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

A fixture namespace used to test heading anchors.

### Covers

Heading anchors and TOC.

### Not Covered

Production content.

### Current As

2026-06-16
""",
        encoding="utf-8",
    )
    (ns / "CLAUDE.md").write_text("# Sample Namespace Instructions\n", encoding="utf-8")
    (ns / "wiki" / "concepts" / "anchor-concept.md").write_text(
        CONCEPT_WITH_SECTIONS, encoding="utf-8"
    )
    (ns / "wiki" / "concepts" / "thin-concept.md").write_text(
        CONCEPT_SINGLE_SECTION, encoding="utf-8"
    )
    return source


def build_namespace(tmp_path: Path):
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = tmp_path / "output"
    output.mkdir()
    generator.build(source, output, ["sample-namespace"])
    return output


def _article_body(html_text: str) -> str:
    match = re.search(r'<article class="article">(.*)</article>', html_text, re.DOTALL)
    assert match
    return match.group(1)


def _page_html(output: Path, name: str) -> str:
    path = output / "wiki" / "sample-namespace" / "wiki" / "concepts" / f"{name}.md.html"
    assert path.exists()
    return path.read_text(encoding="utf-8")


def test_build_emits_ids_dedup_and_anchor_links(tmp_path: Path) -> None:
    body = _article_body(_page_html(build_namespace(tmp_path), "anchor-concept"))
    # ids present and correct, including markup-stripped ones
    assert '<h2 id="tool-buckets">' in body
    assert '<h3 id="read-db">' in body
    assert '<h3 id="write-state">' in body
    # duplicated heading gets a deterministic suffix in document order
    assert '<h2 id="tool-buckets-2">' in body
    # inline rendering still runs inside the heading text
    assert "<code>db</code>" in body
    assert "<strong>state</strong>" in body
    # each id'd heading carries a hover anchor whose href matches its id
    for slug in ("tool-buckets", "read-db", "write-state", "tool-buckets-2"):
        assert f'<a class="heading-anchor" href="#{slug}" aria-label="Link to this section">' in body


def test_build_emits_toc_before_first_h2(tmp_path: Path) -> None:
    body = _article_body(_page_html(build_namespace(tmp_path), "anchor-concept"))
    assert '<nav class="page-toc">' in body
    assert "<div class=\"page-toc-title\">On this page</div>" in body
    # the TOC sits ahead of the first rendered h2
    assert body.index('<nav class="page-toc">') < body.index('<h2 id="tool-buckets">')
    # every TOC link resolves to an emitted id
    for slug in ("tool-buckets", "read-db", "write-state", "tool-buckets-2"):
        assert f'<a href="#{slug}">' in body
    # h3 entries are nested/indented under their h2 via the h3 class
    assert '<li class="page-toc-h3"><a href="#read-db">' in body
    assert '<li class="page-toc-h2"><a href="#tool-buckets">' in body


def test_build_omits_toc_when_fewer_than_two_sections(tmp_path: Path) -> None:
    body = _article_body(_page_html(build_namespace(tmp_path), "thin-concept"))
    assert '<h2 id="overview">' in body
    assert '<nav class="page-toc">' not in body


def test_build_is_deterministic(tmp_path: Path) -> None:
    first = _page_html(build_namespace(tmp_path / "a"), "anchor-concept")
    second = _page_html(build_namespace(tmp_path / "b"), "anchor-concept")
    # tmp paths differ but the rendered article must be byte-identical
    assert _article_body(first) == _article_body(second)


def test_site_css_has_anchor_and_toc_rules() -> None:
    generator = load_generator()
    css = generator.site_css()
    assert ".heading-anchor{" in css
    assert ".page-toc{" in css
    assert "h2:hover .heading-anchor" in css
