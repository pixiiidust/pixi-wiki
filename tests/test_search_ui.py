#!/usr/bin/env python3
"""Client-side registry search contracts (GitHub issue #58).

The search UI is pure progressive enhancement: ``site_header`` emits an EMPTY
``.site-search`` placeholder and a ``search_script`` builds the input + results
panel inside it on DOMContentLoaded. These assert on freshly emitted HTML/CSS
via the build seam (not the committed pages) so they stay green before the #65
regeneration and guard the regenerated output afterwards.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "build_from_pixi_vault.py"

REGISTRY_URL = "/pixi-wiki/index.json"


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

A fixture namespace used to test client search.

### Covers

Search UI contracts.

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
updated: 2026-06-20
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


def a_readme_page(output: Path) -> Path:
    return output / "wiki" / "sample-namespace" / "README.md.html"


def built_pages(output: Path) -> list[Path]:
    return [
        a_wiki_page(output),
        a_readme_page(output),
        output / "index.html",
        output / "docs" / "AGENT_SETUP.html",
        output / "updates.html",
    ]


# --- Build seam: placeholder + script on every page type ---------------------


def test_every_page_type_has_one_placeholder_and_one_script(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    for page in built_pages(output):
        text = read(page)
        placeholder = f'<div class="site-search" data-registry="{REGISTRY_URL}"></div>'
        assert text.count(placeholder) == 1, page
        # Exactly one search script tag (identify it by a stable interior token
        # unique to search_script, not shared with the other inline scripts).
        assert text.count("var box=document.querySelector('.site-search')") == 1, page


def test_placeholder_is_empty_no_server_rendered_input(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    for page in built_pages(output):
        text = read(page)
        # The placeholder div is emitted empty; the input is built by JS only.
        assert f'data-registry="{REGISTRY_URL}"></div>' in text, page
        # No server-rendered search input inside the header markup.
        header = text.split("</header>", 1)[0]
        assert '<input type="search"' not in header, page
        assert 'class="search-input"' not in header, page


def test_data_registry_points_at_root_registry(tmp_path: Path) -> None:
    generator, _ = build_fixture(tmp_path)
    header = generator.site_header(generator.WIKI_NAV_LINKS)
    assert f'data-registry="{REGISTRY_URL}"' in header
    # Placeholder sits between the logo and the header-nav.
    logo_at = header.index('class="logo"')
    search_at = header.index('class="site-search"')
    nav_at = header.index('class="header-nav"')
    assert logo_at < search_at < nav_at


# --- Search script JS behaviour (containment on the emitted string) ----------


def test_search_script_has_keyboard_affordances(tmp_path: Path) -> None:
    generator, _ = build_fixture(tmp_path)
    js = generator.search_script()
    # `/` focuses search from anywhere.
    assert "ev.key!=='/'" in js
    # Arrow navigation over results.
    assert "ArrowDown" in js
    assert "ArrowUp" in js
    # Enter opens, Escape clears/closes.
    assert "Enter" in js
    assert "Escape" in js


def test_search_script_is_lazy_and_null_safe(tmp_path: Path) -> None:
    generator, _ = build_fixture(tmp_path)
    js = generator.search_script()
    # Fetch is keyed off the placeholder's data-registry, only on focus/input.
    assert "getAttribute('data-registry')" in js
    assert "fetch(url)" in js
    assert "addEventListener('focus'" in js
    # No fetch on page load: the only trigger is load(...) from focus/input.
    assert "DOMContentLoaded" in js
    # Failure path renders a single non-crashing row, not an exception.
    assert "Search unavailable" in js
    # AND-token substring filter; the dropdown renders at most CAP (8) rows and
    # is no longer hard-capped at 20 in the filter itself.
    assert "var CAP=8" in js
    assert "res.length<20" not in js
    # Results are role=listbox options with a namespace badge.
    assert "role" in js
    assert "search-badge" in js


def test_dropdown_search_uses_word_tokens_and_relevance_ranking(tmp_path: Path) -> None:
    generator, _ = build_fixture(tmp_path)
    js = generator.search_script()
    # Punctuation and hyphens split into searchable words, so "verb-first" and
    # "verb first" behave the same without substring matches such as ai/maintain.
    assert "match(/[a-z0-9]+/g)||[]" in js
    assert "function unique(tokens)" in js
    assert "var tokens=unique(tokenize(q))" in js
    # Exact and containing title phrases beat incidental path/namespace hits.
    assert "if(title===phrase)score+=100" in js
    assert "if(title.indexOf(phrase)>=0)score+=60" in js
    assert "res.sort(function(a,b)" in js
    # The registry is static after load, so document fields are tokenized once
    # in flatten() rather than again for every keystroke.
    assert "var titleTokens=tokenize(title)" in js
    assert "_titleTokens:titleTokens" in js
    assert "var titleTokens=e._titleTokens" in js
    assert "_allTokens:titleTokens.concat(pathTokens,metaTokens)" in js
    assert "var hay=e._allTokens" in js


# --- CSS ---------------------------------------------------------------------


def test_css_has_site_search_rules(tmp_path: Path) -> None:
    generator, _ = build_fixture(tmp_path)
    css = generator.site_css()
    assert ".site-search{" in css
    assert ".search-input{" in css
    assert ".search-results{" in css
    assert ".search-result{" in css
    assert ".search-result:hover,.search-result.active{" in css
    assert ".search-badge{" in css
    # Overlay uses the panel custom property, layered above the header nav.
    assert "z-index:40" in css
    assert "background:var(--panel)" in css
    # Shrinks but stays usable on narrow viewports.
    assert ".site-search{max-width:190px" in css
    # Regression: display:flex on .search-results defeats the UA [hidden] rule,
    # leaving an empty panel permanently visible under the input.
    assert ".search-results[hidden]{display:none}" in css


def test_result_hrefs_are_prefixed_with_site_base(tmp_path: Path) -> None:
    # Regression: registry `html` values are site-root-relative (/wiki/...)
    # WITHOUT the /pixi-wiki base; the script must derive the base from
    # data-registry and prefix it, or every result link 404s on Pages.
    generator = load_generator()
    js = generator.search_script()
    assert "var base=url.replace(/\\/index\\.json$/,'');" in js
    assert "a.href=base+e.url;" in js
    assert "a.href=e.url;" not in js

def test_load_queues_latest_callback_instead_of_dropping() -> None:
    # Regression: a focus-triggered load raced typing; input callbacks issued
    # while the fetch was in flight were dropped, so a query typed entirely
    # during the fetch rendered nothing until the next keystroke.
    generator = load_generator()
    js = generator.search_script()
    assert 'pending=cb;if(loading)return;' in js
    assert 'var p=pending;pending=null;if(p)p();' in js
