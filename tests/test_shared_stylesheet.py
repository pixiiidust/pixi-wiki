#!/usr/bin/env python3
"""Build-seam tests for the single shared stylesheet (issue #61).

Every generated page links one ``/pixi-wiki/site.css`` instead of inlining the
full site CSS in a per-page ``<style>`` block. The theme-boot script and the
other progressive-enhancement scripts stay inline in each page's head. These
tests drive a real build over a tiny fixture namespace and assert the seam.
"""

from __future__ import annotations

import importlib.util
import inspect
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
    ns = source / "css-ns"
    (ns / "wiki" / "concepts").mkdir(parents=True)
    (ns / "README.md").write_text(
        """---
title: CSS Namespace
created: 2026-01-02
updated: 2026-01-02
type: namespace
status: active
namespace: css-ns
category: test
---

# CSS Namespace

A fixture namespace used to exercise the shared stylesheet seam.

### Covers

Shared stylesheet extraction.
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "concepts" / "plain-concept.md").write_text(
        """---
title: Plain Concept
created: 2026-01-03
updated: 2026-01-03
type: concept
status: compiled
namespace: css-ns
---

# Plain Concept

A concept page used to check the wiki page type links the stylesheet.
""",
        encoding="utf-8",
    )
    return source


def build_site(tmp_path: Path):
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = tmp_path / "output"
    output.mkdir()
    generator.build(source, output, ["css-ns"])
    return generator, output


def read(output: Path, *parts: str) -> str:
    return output.joinpath(*parts).read_text(encoding="utf-8")


# The stylesheet link now carries a content-hash cache-buster (issue #81), so
# it is computed from the generator's own hash rather than hardcoded.
_GENERATOR = load_generator()
STYLESHEET_LINK = f'<link rel="stylesheet" href="/pixi-wiki/site.css?v={_GENERATOR.SITE_CSS_HASH}">'

# Every built page type that carries full chrome: wiki concept page, README,
# homepage, the three docs chrome pages, updates.html, and 404.html. The
# recent.html redirect stub carries no stylesheet and is asserted separately.
PAGE_PARTS = [
    ("wiki", "css-ns", "wiki", "concepts", "plain-concept.md.html"),
    ("wiki", "css-ns", "README.md.html"),
    ("index.html",),
    ("docs", "AGENT_SETUP.html"),
    ("docs", "REPLICATE_APPROACH.html"),
    ("docs", "SIGNAL_GRAPH.html"),
    ("updates.html",),
    ("404.html",),
]


# ---------------------------------------------------------------------------
# The stylesheet file itself
# ---------------------------------------------------------------------------

def test_site_css_written_at_output_root(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    assert (output / "site.css").is_file()


def test_site_css_holds_dark_theme_tokens_and_feature_rules(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    css = read(output, "site.css")
    # Dark-theme variables that the route contract asserts.
    assert "[data-theme=dark]" in css
    assert "--bg:#0d1117" in css
    assert "--accent:#58a6ff" in css
    # Feature rules appended by recent work must all live in the one file.
    assert ".table-wrap{" in css
    assert ".site-search{" in css
    assert ".skip-link{" in css


def test_site_css_is_byte_identical_to_site_css_helper(tmp_path: Path) -> None:
    generator, output = build_site(tmp_path)
    # Extraction only: the file content must equal site_css() exactly, LF-only.
    written = (output / "site.css").read_bytes()
    assert written == generator.site_css().encode("utf-8")
    assert b"\r\n" not in written


def test_site_css_is_a_generated_root_file(tmp_path: Path) -> None:
    generator, _output = build_site(tmp_path)
    assert "site.css" in generator.GENERATED_ROOT_FILES


def test_stylesheet_link_carries_hash_of_emitted_site_css(tmp_path: Path) -> None:
    import hashlib

    generator, output = build_site(tmp_path)
    written = (output / "site.css").read_bytes()
    expected_hash = hashlib.sha256(written).hexdigest()[:8]
    # The generator's published hash matches the emitted stylesheet content.
    assert generator.SITE_CSS_HASH == expected_hash
    # Every full-chrome page links /site.css?v=<that hash>.
    link = f'<link rel="stylesheet" href="/pixi-wiki/site.css?v={expected_hash}">'
    for parts in PAGE_PARTS:
        assert link in read(output, *parts), parts


# ---------------------------------------------------------------------------
# Per-page linking / no inline CSS
# ---------------------------------------------------------------------------

def test_every_page_links_the_shared_stylesheet_exactly_once(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    for parts in PAGE_PARTS:
        html_text = read(output, *parts)
        assert html_text.count(STYLESHEET_LINK) == 1, parts


def test_no_page_inlines_root_css(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    for parts in PAGE_PARTS:
        html_text = read(output, *parts)
        # The base CSS line begins with the light-theme :root color-scheme block;
        # its absence proves the stylesheet is no longer inlined.
        assert ":root{color-scheme" not in html_text, parts
        assert "<style>" not in html_text, parts


# ---------------------------------------------------------------------------
# Theme boot script stays inline
# ---------------------------------------------------------------------------

def test_theme_script_remains_inline_on_every_page(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    for parts in PAGE_PARTS:
        html_text = read(output, *parts)
        # Inline theme-boot script must stay in the head to avoid a theme flash.
        assert "localStorage.getItem" in html_text, parts


# ---------------------------------------------------------------------------
# Dead parameter removal
# ---------------------------------------------------------------------------

def test_make_sidebar_no_longer_accepts_counts() -> None:
    generator = load_generator()
    params = inspect.signature(generator.make_sidebar).parameters
    assert "counts" not in params


def test_page_shell_no_longer_accepts_counts() -> None:
    generator = load_generator()
    params = inspect.signature(generator.page_shell).parameters
    assert "counts" not in params
