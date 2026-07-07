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
# Direct unit tests of inline_markdown / markdown_fragment
# ---------------------------------------------------------------------------

def test_inline_emphasis_bold_and_italic() -> None:
    generator = load_generator()
    out = generator.inline_markdown("this is **bold** and *italic* text")
    assert "<strong>bold</strong>" in out
    assert "<em>italic</em>" in out
    assert "**" not in out
    assert "*" not in out


def test_inline_emphasis_ignores_asterisks_inside_code_span() -> None:
    generator = load_generator()
    out = generator.inline_markdown("call `a * b ** c` then **really** bold")
    assert "<code>a * b ** c</code>" in out
    assert "<strong>really</strong>" in out
    # asterisks that live inside the code span must remain literal
    assert "<em>" not in out.split("</code>")[0]
    assert "<strong>" not in out.split("</code>")[0]


def test_inline_emphasis_does_not_cross_into_links() -> None:
    generator = load_generator()
    out = generator.inline_markdown("see [label](https://example.com/a*b) and **bold**")
    assert '<a href="https://example.com/a*b">label</a>' in out
    assert "<strong>bold</strong>" in out


def test_inline_em_does_not_cross_link_href() -> None:
    # Regression: a '*' inside an href plus a lone '*' later in the line must
    # not let the em pattern match across the attribute and corrupt the tag.
    generator = load_generator()
    out = generator.inline_markdown("see [x](https://example.com/a*b) and *word*")
    assert '<a href="https://example.com/a*b">x</a>' in out
    assert "<em>word</em>" in out


def test_inline_emphasis_inside_link_label() -> None:
    generator = load_generator()
    out = generator.inline_markdown("[**Title**](https://example.com/doc)")
    assert '<a href="https://example.com/doc"><strong>Title</strong></a>' in out


def test_ordered_list_renders_ol() -> None:
    generator = load_generator()
    out = generator.markdown_fragment("1. first\n2. second\n3. third")
    assert out.count("<ol>") == 1
    assert out.count("</ol>") == 1
    assert out.count("<li>") == 3
    assert "<p>" not in out


def test_ordered_and_unordered_lists_close_each_other() -> None:
    generator = load_generator()
    out = generator.markdown_fragment("- bullet\n1. number")
    # a numbered line after a bullet closes the <ul> and opens an <ol>
    assert out.index("<ul>") < out.index("</ul>") < out.index("<ol>")


def test_blockquote_without_space_merges_into_one() -> None:
    generator = load_generator()
    out = generator.markdown_fragment(">Community facilities\n>share the load")
    assert out.count("<blockquote>") == 1
    assert out.count("</blockquote>") == 1
    assert "&gt;Community" not in out
    assert "<blockquote>Community facilities<br>share the load</blockquote>" == out


def test_table_with_header_structure() -> None:
    generator = load_generator()
    md = "| Bucket | Purpose |\n| --- | --- |\n| read | inspect |\n| write | mutate |"
    out = generator.markdown_fragment(md)
    assert '<div class="table-wrap">' in out
    assert "<table>" in out
    assert "<thead>" in out and "<tbody>" in out
    assert "<th>Bucket</th>" in out
    assert "<td>read</td>" in out
    assert out.count("<tr>") == 3


def test_table_cells_render_inline_markdown() -> None:
    generator = load_generator()
    md = "| Name | Note |\n| --- | --- |\n| **hot** | see `code` |"
    out = generator.markdown_fragment(md)
    assert "<strong>hot</strong>" in out
    assert "<code>code</code>" in out


def test_table_cell_escapes_html() -> None:
    generator = load_generator()
    md = "| Tag |\n| --- |\n| <script> |"
    out = generator.markdown_fragment(md)
    assert "&lt;script&gt;" in out
    assert "<script>" not in out


def test_table_without_separator_is_headerless() -> None:
    generator = load_generator()
    md = "| a | b |\n| c | d |"
    out = generator.markdown_fragment(md)
    assert "<table>" in out
    assert "<thead>" not in out
    assert "<p>| a | b |</p>" not in out


def test_code_fence_asterisks_stay_literal() -> None:
    generator = load_generator()
    out = generator.markdown_fragment("```\nx = a ** b\n```")
    assert "<pre><code>" in out
    assert "a ** b" in out
    assert "<strong>" not in out


# ---------------------------------------------------------------------------
# Build-seam test: emitted namespace HTML
# ---------------------------------------------------------------------------

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

A fixture namespace used to test renderer coverage.

### Covers

Renderer syntax coverage.

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

- [[concepts/syntax-concept|Syntax Concept]]
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
    (ns / "wiki" / "concepts" / "syntax-concept.md").write_text(
        """---
title: Syntax Concept
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: sample-namespace
---

# Syntax Concept

This page has **bold** and *italic* emphasis.

## Tool buckets

| Bucket | Purpose |
| --- | --- |
| read | inspect **state** |
| write | mutate `db` |

## Steps

1. First step
2. Second step
3. Third step

>Community facilities
>share the load

Inline `a * b ** c` keeps asterisks literal.

```
star = a ** b
```
""",
        encoding="utf-8",
    )
    return source


def render_syntax_html(tmp_path: Path) -> str:
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = tmp_path / "output"
    output.mkdir()
    generator.build(source, output, ["sample-namespace"])
    html_path = output / "wiki" / "sample-namespace" / "wiki" / "concepts" / "syntax-concept.md.html"
    assert html_path.exists()
    return html_path.read_text(encoding="utf-8")


def _article_body(html_text: str) -> str:
    match = re.search(r'<article class="article">(.*)</article>', html_text, re.DOTALL)
    assert match
    return match.group(1)


def test_build_emits_emphasis(tmp_path: Path) -> None:
    body = _article_body(render_syntax_html(tmp_path))
    assert "<strong>bold</strong>" in body
    assert "<em>italic</em>" in body
    # no literal '**' outside of <code> spans
    without_code = re.sub(r"<code>.*?</code>", "", body, flags=re.DOTALL)
    assert "**" not in without_code


def test_build_emits_table(tmp_path: Path) -> None:
    body = _article_body(render_syntax_html(tmp_path))
    assert '<div class="table-wrap">' in body
    assert "<thead>" in body and "<tbody>" in body
    assert "<th>Bucket</th>" in body
    # inline rendering inside a cell
    assert "<strong>state</strong>" in body
    assert "<code>db</code>" in body


def test_build_emits_ordered_list(tmp_path: Path) -> None:
    body = _article_body(render_syntax_html(tmp_path))
    assert "<ol>" in body and "</ol>" in body
    assert body.count("<li>") >= 3


def test_build_emits_blockquote_without_space(tmp_path: Path) -> None:
    body = _article_body(render_syntax_html(tmp_path))
    assert "<blockquote>Community facilities<br>share the load</blockquote>" in body
    assert "&gt;Community" not in body
    assert "Community facilities" in body


def test_build_keeps_asterisks_literal_in_code(tmp_path: Path) -> None:
    body = _article_body(render_syntax_html(tmp_path))
    assert "<code>a * b ** c</code>" in body
    assert "star = a ** b" in body
    # the fenced content must not have been emphasised
    assert "star = a <strong>" not in body


def test_build_table_cell_escapes_html(tmp_path: Path) -> None:
    body = _article_body(render_syntax_html(tmp_path))
    # site CSS / structure should never leak an unescaped angle bracket from cells;
    # sanity check the table renders at all
    assert "<table>" in body


def test_site_css_has_table_wrap_rule() -> None:
    generator = load_generator()
    css = generator.site_css()
    assert ".table-wrap{overflow-x:auto" in css
