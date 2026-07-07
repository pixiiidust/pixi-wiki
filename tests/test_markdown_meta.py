#!/usr/bin/env python3
"""Tests for the shared Markdown frontmatter/text-extraction module.

These lock in the canonical (generator) semantics that the shared module
adopts, including the reconciliation decisions documented in
``scripts/markdown_meta.py``.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.markdown_meta import first_heading, first_paragraph, parse_frontmatter


def test_double_quoted_scalar_is_stripped() -> None:
    fm, body = parse_frontmatter('---\ntitle: "Hello World"\n---\nbody\n')
    assert fm["title"] == "Hello World"
    assert body == "body\n"


def test_single_quoted_scalar_keeps_quotes() -> None:
    # Canonical generator behavior: scalars strip only double quotes.
    fm, _ = parse_frontmatter("---\ntitle: 'Hello World'\n---\nx")
    assert fm["title"] == "'Hello World'"


def test_block_list_items_are_not_quote_stripped() -> None:
    # Canonical generator behavior: `  - x` block items keep any quotes.
    fm, _ = parse_frontmatter(
        '---\nsources:\n  - "Knowledge/a.md"\n  - Projects/b.md\n---\nbody'
    )
    assert fm["sources"] == ['"Knowledge/a.md"', "Projects/b.md"]


def test_inline_list_values_strip_both_quote_kinds() -> None:
    fm, _ = parse_frontmatter("---\ntags: [a, \"b\", 'c']\n---\nbody")
    assert fm["tags"] == ["a", "b", "c"]


def test_empty_value_starts_a_list() -> None:
    fm, _ = parse_frontmatter("---\nsources:\n  - one\n---\nbody")
    assert fm["sources"] == ["one"]


def test_value_containing_colon_splits_on_first_colon() -> None:
    fm, _ = parse_frontmatter(
        "---\nresource: https://example.com:8080/path\n---\nbody"
    )
    assert fm["resource"] == "https://example.com:8080/path"


def test_key_with_non_word_characters_still_parses() -> None:
    # Generator splits on the first colon rather than requiring a word-only key.
    fm, _ = parse_frontmatter("---\nsome key: value\n---\nbody")
    assert fm["some key"] == "value"


def test_missing_frontmatter_returns_empty_and_original_text() -> None:
    text = "# Just a heading\n\nBody text."
    fm, body = parse_frontmatter(text)
    assert fm == {}
    assert body == text


def test_unclosed_frontmatter_returns_empty_and_original_text() -> None:
    text = "---\ntitle: Broken\nno closing delimiter\n"
    fm, body = parse_frontmatter(text)
    assert fm == {}
    assert body == text


def test_first_heading_returns_first_h1() -> None:
    assert first_heading("intro\n# First\n# Second\n") == "First"


def test_first_heading_returns_none_when_absent() -> None:
    assert first_heading("no headings here\n## not an h1\n") is None


def test_first_paragraph_skips_headings_and_returns_prose() -> None:
    body = "# Title\n\nThis is the first paragraph.\n\nSecond paragraph.\n"
    assert first_paragraph(body) == "This is the first paragraph."


def test_first_paragraph_skips_code_fences() -> None:
    body = "```\ncode line\n```\n\nReal prose here.\n"
    assert first_paragraph(body) == "Real prose here."


def test_first_paragraph_default_fallback_on_empty_body() -> None:
    assert first_paragraph("# Only a heading\n") == "Compiled namespace."


def test_first_paragraph_stops_after_exceeding_260_chars() -> None:
    body = "a" * 200 + "\n" + "b" * 100 + "\n" + "c" * 100 + "\n"
    result = first_paragraph(body)
    # First two lines join to length 301 (> 260) so the loop stops; the third
    # line is never appended, and the result is truncated to 300 chars.
    assert len(result) == 300
    assert "c" not in result
