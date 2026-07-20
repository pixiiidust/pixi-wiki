#!/usr/bin/env python3
"""Build-seam + committed-artifact tests for the client search results page (#85).

``/search.html`` is a JavaScript-dependent enhancement surface: the build emits
an empty ``.search-page`` placeholder plus a ``search_page_script`` that fills it
on DOMContentLoaded (prominent input, ranked/highlighted results, client-side
pagination). Because search is JS-only, the page carries ``robots: noindex`` and
is excluded from ``sitemap.xml``; its ``<noscript>`` fallback routes agents/no-JS
readers to the Markdown entrypoints.

The build-seam tests assert on freshly emitted HTML/JS/CSS via the fixture build
so they stay green before the committed-tree regeneration and guard the output
afterwards. The single ``CommittedSearchPage`` contract asserts on the PUBLISHED
tree and is EXPECTED to fail until ``search.html`` is regenerated (see PR body).
"""
from __future__ import annotations

import importlib.util
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "build_from_pixi_vault.py"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

REGISTRY_URL = "/pixi-wiki/index.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("build_from_pixi_vault", GENERATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_fixture_source(base: Path) -> Path:
    source = base / "source" / "wikis"
    ns = source / "search-ns"
    (ns / "wiki" / "concepts").mkdir(parents=True)
    (ns / "README.md").write_text(
        """---
title: Search Namespace
created: 2026-01-02
updated: 2026-01-02
type: namespace
status: active
namespace: search-ns
category: test
---

# Search Namespace

A fixture namespace used to exercise the search results page.

### Covers

Search page contracts.
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "concepts" / "test-concept.md").write_text(
        """---
title: Test Concept
type: concept
namespace: search-ns
updated: 2026-01-03
---

# Test Concept

Body.
""",
        encoding="utf-8",
    )
    return source


def build_site(tmp_path: Path, **kwargs):
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = tmp_path / "output"
    output.mkdir()
    generator.build(source, output, ["search-ns"], **kwargs)
    return generator, output


def read(output: Path, *parts: str) -> str:
    return output.joinpath(*parts).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Build seam: page shell, meta, placeholder, noscript
# ---------------------------------------------------------------------------

def test_search_page_emitted_with_standard_chrome(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    page = output / "search.html"
    assert page.exists()
    html_text = page.read_text(encoding="utf-8")
    assert "<h1>Search</h1>" in html_text
    assert 'class="skip-link"' in html_text
    assert 'class="site-header"' in html_text
    assert "data-theme-toggle" in html_text
    assert '<footer class="footer">' in html_text
    assert "<title>Search — Pixi Wiki</title>" in html_text


def test_search_page_has_noindex_meta(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    html_text = read(output, "search.html")
    assert '<meta name="robots" content="noindex">' in html_text


def test_search_page_placeholder_is_empty_with_registry(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    html_text = read(output, "search.html")
    assert f'<div class="search-page" data-registry="{REGISTRY_URL}"></div>' in html_text


def test_search_page_has_exactly_one_results_script(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    html_text = read(output, "search.html")
    # Stable interior token unique to search_page_script.
    assert html_text.count("var box=document.querySelector('.search-page')") == 1
    # The header dropdown search still loads on this page too (standard chrome).
    assert html_text.count("var box=document.querySelector('.site-search')") == 1


def test_search_page_noscript_links_agent_entrypoints(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    html_text = read(output, "search.html")
    start = html_text.index("<noscript>")
    end = html_text.index("</noscript>")
    block = html_text[start:end]
    assert "JavaScript" in block
    assert 'href="/pixi-wiki/llms.txt"' in block
    assert 'href="/pixi-wiki/index.json"' in block


def test_search_page_is_excluded_from_sitemap(tmp_path: Path) -> None:
    generator, output = build_site(tmp_path)
    tree = ET.parse(output / "sitemap.xml")
    locs = [u.find("sm:loc", SITEMAP_NS).text for u in tree.getroot().findall("sm:url", SITEMAP_NS)]
    assert generator.SITE_ORIGIN + "/pixi-wiki/search.html" not in locs


def test_search_page_is_in_fresh_build_root_allowlist(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    root_html = sorted(path.name for path in output.glob("*.html"))
    assert "search.html" in root_html
    assert root_html == ["404.html", "index.html", "recent.html", "search.html", "updates.html"]


def test_custom_base_path_reaches_placeholder_and_noscript(tmp_path: Path) -> None:
    _generator, output = build_site(
        tmp_path, base_path="/custom-wiki", site_origin="https://example.org"
    )
    html_text = read(output, "search.html")
    assert '<div class="search-page" data-registry="/custom-wiki/index.json"></div>' in html_text
    assert 'href="/custom-wiki/llms.txt"' in html_text
    assert 'href="/custom-wiki/index.json"' in html_text


# ---------------------------------------------------------------------------
# Results script (containment on the emitted string)
# ---------------------------------------------------------------------------

def test_results_script_reads_url_params_and_replaces_state(tmp_path: Path) -> None:
    generator, _ = build_site(tmp_path)
    js = generator.search_page_script()
    assert "URLSearchParams" in js
    assert "params.get('q')" in js
    assert "params.get('page')" in js
    assert "history.replaceState" in js


def test_results_script_ranks_and_highlights(tmp_path: Path) -> None:
    generator, _ = build_site(tmp_path)
    js = generator.search_page_script()
    # Word-token matching avoids substring noise, while exact/containing title
    # phrases outrank incidental metadata matches.
    assert "match(/[a-z0-9]+/g)||[]" in js
    assert "function unique(tokens)" in js
    assert "var tokens=unique(tokenize(q))" in js
    assert "function search(tokens){if(!tokens.length)return []" in js
    assert "if(title===phrase)score+=100" in js
    assert "if(title.indexOf(phrase)>=0)score+=60" in js
    assert "if(path.indexOf(phrase)>=0)score+=25" in js
    assert "var titleTokens=tokenize(title)" in js
    assert "_titleTokens:titleTokens" in js
    assert "var titleTokens=e._titleTokens" in js
    assert "_allTokens:titleTokens.concat(pathTokens,metaTokens)" in js
    assert "var hay=e._allTokens" in js
    # Escape-safe <mark> highlighting built via DOM text nodes, never innerHTML.
    assert "createElement('mark')" in js
    assert "createTextNode" in js
    assert "var word=/[a-z0-9]+/gi" in js
    assert "wanted[m[0].toLowerCase()]" in js
    assert "slice(last)));}function sync" in js
    assert "textContent" in js
    assert ".innerHTML=tokens" not in js


def test_results_script_paginates_at_20_per_page(tmp_path: Path) -> None:
    generator, _ = build_site(tmp_path)
    js = generator.search_page_script()
    assert "PER=20" in js
    assert "search-pagination" in js
    assert "search-pagination-current" in js
    assert "aria-current" in js


def test_results_script_is_lazy_and_failure_safe(tmp_path: Path) -> None:
    generator, _ = build_site(tmp_path)
    js = generator.search_page_script()
    assert "getAttribute('data-registry')" in js
    assert "fetch(url)" in js
    # Debounced live search (~150ms) and base-prefixed result links.
    assert "150" in js
    assert "a.href=base+e.url" in js
    # Fetch-failure row like the dropdown's.
    assert "Search unavailable" in js


def test_results_script_has_no_dropdown_see_all(tmp_path: Path) -> None:
    generator, _ = build_site(tmp_path)
    js = generator.search_page_script()
    # "See all" is the header dropdown's affordance, not the results page's.
    assert "See all" not in js


# ---------------------------------------------------------------------------
# Dropdown script changes (containment on the emitted string)
# ---------------------------------------------------------------------------

def test_dropdown_caps_at_8_and_appends_see_all(tmp_path: Path) -> None:
    generator, _ = build_site(tmp_path)
    js = generator.search_script()
    assert "var CAP=8" in js
    assert "i<CAP" in js
    # See-all row links the results page with the encoded query and the true N.
    assert "'/search.html?q='+encodeURIComponent(q)" in js
    assert "See all '+list.length+' results" in js


def test_dropdown_enter_navigates_to_results_without_selection(tmp_path: Path) -> None:
    generator, _ = build_site(tmp_path)
    js = generator.search_script()
    # Bare Enter (no arrow-selected option) navigates to the results page.
    assert "'/search.html?q='+encodeURIComponent(qq)" in js
    # It no longer opens the first row on a bare Enter.
    assert "active>=0?rows[active]:rows[0]" not in js


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

def test_css_has_search_page_rules(tmp_path: Path) -> None:
    generator, _ = build_site(tmp_path)
    css = generator.site_css()
    assert ".search-page-input{" in css
    assert ".search-count{" in css
    assert ".search-result-row{" in css
    # Highlight uses the shared active-bg token.
    assert ".search-page-results mark{background:var(--active-bg)" in css
    # Pagination pills use the collision-free search-pagination prefix.
    assert ".search-pagination{" in css
    assert ".search-pagination-current{" in css


# ---------------------------------------------------------------------------
# Committed-artifact contract (regenerated post-merge; expected to fail now)
# ---------------------------------------------------------------------------

def test_committed_search_page_is_published_and_noindexed() -> None:
    """Committed-artifact contract (regenerated post-merge, like #65/#81).

    EXPECTED to fail until ``search.html`` is regenerated into the committed
    tree; listed in the PR body as a pre-regeneration expected failure.
    """
    page = ROOT / "search.html"
    assert page.exists(), "search.html not yet regenerated into the committed tree"
    html_text = page.read_text(encoding="utf-8")
    assert "<h1>Search</h1>" in html_text
    assert '<meta name="robots" content="noindex">' in html_text
    assert f'<div class="search-page" data-registry="{REGISTRY_URL}"></div>' in html_text
    # noindex → stays out of the committed sitemap.
    tree = ET.parse(ROOT / "sitemap.xml")
    locs = [el.text for el in tree.iter() if el.tag.endswith("loc")]
    assert "https://pixiiidust.github.io/pixi-wiki/search.html" not in locs

def test_load_queues_latest_callback_instead_of_dropping() -> None:
    # Regression: a focus-triggered load raced typing; input callbacks issued
    # while the fetch was in flight were dropped, so a query typed entirely
    # during the fetch rendered nothing until the next keystroke.
    generator = load_generator()
    js = generator.search_page_script()
    assert 'pending=cb;if(loading)return;' in js
    assert 'var p=pending;pending=null;if(p)p();' in js
