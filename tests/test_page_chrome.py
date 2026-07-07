#!/usr/bin/env python3
"""Page chrome contracts: shared header, mobile disclosure nav, article-first layout.

Covers GitHub issue #56. These assert on freshly emitted HTML/CSS via the build
seam (not the committed pages) so they stay green before the #65 regeneration and
guard the regenerated output afterwards.
"""
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

A fixture namespace used to test page chrome.

### Covers

Header and layout contracts.

### Not Covered

Production content.

### Current As

2026-06-16
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "index.md").write_text(
        """---
title: Sample Index
type: index
namespace: sample-namespace
---

# Sample Index
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "concepts" / "test-concept.md").write_text(
        """---
title: Test Concept
type: concept
namespace: sample-namespace
---

# Test Concept

Body.
""",
        encoding="utf-8",
    )
    return source


def build_fixture(tmp_path: Path):
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = tmp_path / "output"
    output.mkdir()
    generator.build(source, output, ["sample-namespace"])
    return generator, output


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def a_wiki_page(output: Path) -> Path:
    return output / "wiki" / "sample-namespace" / "wiki" / "concepts" / "test-concept.md.html"


# --- Shared header helper ----------------------------------------------------


def test_site_header_helper_renders_both_link_sets(tmp_path: Path) -> None:
    generator, _ = build_fixture(tmp_path)
    wiki_header = generator.site_header(generator.WIKI_NAV_LINKS)
    home_header = generator.site_header(generator.HOME_NAV_LINKS)

    # Inline nav preserved for wide viewports.
    assert '<nav class="nav">' in wiki_header
    # Disclosure nav present with the same links.
    assert '<details class="nav-menu">' in wiki_header
    assert '<nav class="nav-panel">' in wiki_header
    # Link sets preserved per template.
    assert 'href="/pixi-wiki/docs/SIGNAL_GRAPH.html">Signal Graph</a>' not in wiki_header
    assert 'href="/pixi-wiki/docs/SIGNAL_GRAPH.html">Signal Graph</a>' in home_header
    for href, label in generator.WIKI_NAV_LINKS:
        # Each link appears in both the inline nav and the disclosure panel.
        assert wiki_header.count(f'<a href="{href}">{label}</a>') == 2


def test_theme_toggle_outside_inline_nav_and_present_once(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    pages = [
        a_wiki_page(output),
        output / "index.html",
        output / "docs" / "AGENT_SETUP.html",
        output / "docs" / "SIGNAL_GRAPH.html",
        output / "docs" / "REPLICATE_APPROACH.html",
    ]
    for page in pages:
        text = read(page)
        # Exactly one theme toggle button per page (the theme_script also
        # references [data-theme-toggle], so match the button attribute set).
        assert text.count('data-theme-toggle type="button"') == 1, page
        assert text.count('class="theme-toggle"') == 1, page
        # Toggle must not live inside <nav class="nav">...</nav>.
        nav_block = re.search(r'<nav class="nav">.*?</nav>', text, re.DOTALL)
        assert nav_block, page
        assert "theme-toggle" not in nav_block.group(0), page
        # Contract markers relied on by test_route_contract after #65 regeneration.
        assert "data-theme-toggle" in text, page
        assert "☾" in text, page  # ☾


# --- Emitted pages carry the disclosure nav ----------------------------------


def test_all_page_types_get_disclosure_nav(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    for page in [
        a_wiki_page(output),
        output / "index.html",
        output / "docs" / "AGENT_SETUP.html",
        output / "docs" / "SIGNAL_GRAPH.html",
        output / "docs" / "REPLICATE_APPROACH.html",
    ]:
        text = read(page)
        assert '<nav class="nav">' in text, page
        assert '<details class="nav-menu">' in text, page
        assert '<nav class="nav-panel">' in text, page


def _header(text: str) -> str:
    match = re.search(r"<header class=\"site-header\">.*?</header>", text, re.DOTALL)
    assert match
    return match.group(0)


def test_homepage_and_docs_have_signal_graph_link(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    # Homepage/Signal Graph headers surface Signal Graph in both inline nav and
    # disclosure panel; scope to the header since the page body/footer also link it.
    for page in [output / "index.html", output / "docs" / "SIGNAL_GRAPH.html"]:
        header = _header(read(page))
        assert header.count('href="/pixi-wiki/docs/SIGNAL_GRAPH.html">Signal Graph</a>') == 2, page
    # A plain wiki page must NOT carry the Signal Graph nav link.
    assert "Signal Graph" not in _header(read(a_wiki_page(output)))


# --- CSS: mobile behavior at <=820px -----------------------------------------


def test_css_mobile_rules_present_in_emitted_style(tmp_path: Path) -> None:
    generator, output = build_fixture(tmp_path)
    # The CSS is now served from one shared stylesheet (issue #61) rather than
    # inlined per page, so the mobile rules are asserted against site.css and the
    # page is checked to link it (with the #81 content-hash cache-buster).
    assert f'<link rel="stylesheet" href="/pixi-wiki/site.css?v={generator.SITE_CSS_HASH}">' in read(output / "index.html")
    css = read(output / "site.css")

    media = re.search(r"@media\(max-width:820px\)\{(.*?)\}\s*$", css, re.DOTALL)
    assert media, "expected the <=820px media block"
    block = media.group(1)
    # Inline nav hidden, disclosure shown.
    assert ".nav{display:none}" in block
    assert ".nav-menu{display:block}" in block
    # Article renders first, sidebar second (order in single-column grid).
    assert ".article{order:1}" in block
    assert ".sidebar{order:2}" in block

    # Wide-viewport defaults: disclosure hidden, overlay panel styled.
    assert ".nav-menu{display:none;position:relative}" in css
    assert ".nav-panel{position:absolute" in css
    assert "background:var(--panel)" in css
