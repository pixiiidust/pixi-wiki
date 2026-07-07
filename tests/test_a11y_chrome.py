#!/usr/bin/env python3
"""Accessibility chrome + copy-button contracts.

Covers GitHub issue #63. These assert on freshly emitted HTML/CSS via the build
seam (not the committed pages) so they stay green before the #65 regeneration
and guard the regenerated output afterwards.
"""
from __future__ import annotations

import importlib.util
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

A fixture namespace used to test a11y chrome.

### Covers

Accessibility semantics and copy buttons.

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

Body with a code block:

```
echo hi
```
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


# --- Theme toggle accessible name --------------------------------------------


def test_theme_toggle_has_accessible_name(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    text = read(a_wiki_page(output))
    assert '<button class="theme-toggle" data-theme-toggle type="button" aria-label="Toggle color theme">' in text


# --- aria-current on the active sidebar link ---------------------------------


def test_active_sidebar_link_marks_aria_current(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    text = read(a_wiki_page(output))
    # The active link (this very page) carries both the class and aria-current.
    assert (
        '<a class="active" aria-current="page" '
        'href="/pixi-wiki/wiki/sample-namespace/wiki/concepts/test-concept.md.html">' in text
    )
    # Exactly one page marker (the active document); non-active links omit it.
    assert text.count('aria-current="page"') == 1


def test_non_active_sidebar_links_omit_aria_current(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    # The README page is not itself active in the CONCEPTS section, so the
    # concept link must not carry aria-current on that page.
    readme = output / "wiki" / "sample-namespace" / "README.md.html"
    text = read(readme)
    assert (
        '<a href="/pixi-wiki/wiki/sample-namespace/wiki/concepts/test-concept.md.html">' in text
    )
    # README itself is the active document here -> one and only one marker.
    assert text.count('aria-current="page"') == 1
    assert 'concepts/test-concept.md.html" aria-current' not in text


# --- Decorative emoji hidden from assistive tech -----------------------------


def test_sidebar_emoji_wrapped_in_aria_hidden(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    text = read(a_wiki_page(output))
    assert '<span aria-hidden="true">📄 </span>Test Concept</a>' in text
    # The bare emoji-plus-title sequence must no longer appear unwrapped.
    assert "📄 Test Concept" not in text


def test_readme_agent_card_emoji_wrapped(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    text = read(output / "wiki" / "sample-namespace" / "README.md.html")
    assert '<div class="agent-card"><span aria-hidden="true">🤖 </span>Agent access:' in text


# --- Skip link + main landmark id --------------------------------------------


def test_page_shell_body_starts_with_skip_link(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    text = read(a_wiki_page(output))
    assert '</head><body>\n<a class="skip-link" href="#main-content">Skip to content</a>' in text
    assert '<article class="article" id="main-content">' in text


def test_agent_setup_page_has_skip_link_and_main_id(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    text = read(output / "docs" / "AGENT_SETUP.html")
    assert '<a class="skip-link" href="#main-content">Skip to content</a>' in text
    assert '<main id="main-content">' in text


# --- Copy-button script ------------------------------------------------------


def test_copy_script_present_once_on_wiki_page(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    text = read(a_wiki_page(output))
    # The script's aria-label string is a unique marker for a single injection.
    assert text.count("'Copy code'") == 1
    assert 'navigator.clipboard' in text


def test_copy_script_present_on_agent_setup_page(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    text = read(output / "docs" / "AGENT_SETUP.html")
    assert text.count("'Copy code'") == 1


def test_copy_script_present_on_homepage(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    text = read(output / "index.html")
    assert text.count("'Copy code'") == 1


# --- CSS rules ---------------------------------------------------------------


def test_css_has_skip_link_and_copy_button_rules(tmp_path: Path) -> None:
    generator, _ = build_fixture(tmp_path)
    css = generator.site_css()
    assert ".skip-link{" in css
    assert ".skip-link:focus{" in css
    assert ".copy-button{" in css
