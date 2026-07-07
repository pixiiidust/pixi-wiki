#!/usr/bin/env python3
"""Build-seam tests for the configurable base path and site origin.

These lock two contracts: HTML chrome (stylesheet/logo/sidebar/data-registry),
canonical/OpenGraph URLs, sitemap locs, and recent/404 links all carry the
configured base path, while the registry values in ``index.json``/llms.txt
(``/raw/<slug>/...``, ``/wiki/<slug>/...``) stay site-root-relative and never
gain the prefix.
"""

from __future__ import annotations

import importlib.util
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "build_from_pixi_vault.py"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def load_generator():
    spec = importlib.util.spec_from_file_location("build_from_pixi_vault", GENERATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_fixture_source(base: Path) -> Path:
    source = base / "source" / "wikis"
    ns = source / "base-ns"
    (ns / "wiki" / "concepts").mkdir(parents=True)
    (ns / "README.md").write_text(
        """---
title: Base Namespace
created: 2026-01-02
updated: 2026-01-02
type: namespace
status: active
namespace: base-ns
category: test
---

# Base Namespace

A fixture namespace used to exercise configurable base path and origin.

### Covers

Base-path plumbing.
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
namespace: base-ns
---

# Plain Concept

A concept page whose dated frontmatter surfaces it on the recent feed.
""",
        encoding="utf-8",
    )
    return source


def build_site(tmp_path: Path, **kwargs):
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = tmp_path / "output"
    output.mkdir()
    generator.build(source, output, ["base-ns"], **kwargs)
    return generator, output


def read(output: Path, *parts: str) -> str:
    return output.joinpath(*parts).read_text(encoding="utf-8")


def link_href(html_text: str, rel: str) -> str | None:
    match = re.search(rf'<link rel="{re.escape(rel)}" href="([^"]*)">', html_text)
    return match.group(1) if match else None


def og_content(html_text: str, prop: str) -> str | None:
    match = re.search(rf'<meta property="{re.escape(prop)}" content="([^"]*)">', html_text)
    return match.group(1) if match else None


# ---------------------------------------------------------------------------
# Custom base path + origin
# ---------------------------------------------------------------------------

def test_custom_base_path_covers_all_chrome(tmp_path: Path) -> None:
    generator, output = build_site(
        tmp_path, base_path="/custom-wiki", site_origin="https://example.org"
    )
    page = read(output, "wiki", "base-ns", "wiki", "concepts", "plain-concept.md.html")

    # Stylesheet, logo, sidebar links, and data-registry all carry the base.
    assert '<link rel="stylesheet" href="/custom-wiki/site.css">' in page
    assert '<a class="logo" href="/custom-wiki/">Pixi Wiki</a>' in page
    assert 'data-registry="/custom-wiki/index.json"' in page
    assert 'href="/custom-wiki/wiki/base-ns/README.md.html"' in page
    assert 'href="/custom-wiki/raw/base-ns/wiki/concepts/plain-concept.md"' in page

    # Canonical + og:url = origin + base + path.
    canonical = "https://example.org/custom-wiki/wiki/base-ns/wiki/concepts/plain-concept.md.html"
    assert link_href(page, "canonical") == canonical
    assert og_content(page, "og:url") == canonical


def test_custom_base_registry_values_stay_unprefixed(tmp_path: Path) -> None:
    _generator, output = build_site(
        tmp_path, base_path="/custom-wiki", site_origin="https://example.org"
    )
    registry = json.loads(read(output, "index.json"))
    wiki = registry["wikis"][0]
    # Registry raw/html contracts are site-root-relative and never prefixed.
    assert wiki["raw_base"] == "/raw/base-ns/"
    assert wiki["html_base"] == "/wiki/base-ns/"
    assert wiki["llms_txt"] == "/wiki/base-ns/llms.txt"
    for doc in wiki["documents"]:
        assert doc["raw"].startswith("/raw/base-ns/")
        assert doc["html"].startswith("/wiki/base-ns/")
        assert "/custom-wiki" not in doc["raw"]
        assert "/custom-wiki" not in doc["html"]


def test_custom_base_sitemap_recent_and_404(tmp_path: Path) -> None:
    _generator, output = build_site(
        tmp_path, base_path="/custom-wiki", site_origin="https://example.org"
    )
    # Sitemap locs live under origin + base.
    tree = ET.parse(output / "sitemap.xml")
    locs = [u.find("sm:loc", SITEMAP_NS).text for u in tree.getroot().findall("sm:url", SITEMAP_NS)]
    assert "https://example.org/custom-wiki/" in locs
    assert "https://example.org/custom-wiki/wiki/base-ns/README.md.html" in locs
    assert all(loc.startswith("https://example.org/custom-wiki") for loc in locs)

    # Recent page links carry the base (the entry html is prefixed explicitly).
    recent = read(output, "recent.html")
    assert 'href="/custom-wiki/wiki/base-ns/wiki/concepts/plain-concept.md.html"' in recent
    assert '<link rel="stylesheet" href="/custom-wiki/site.css">' in recent

    # 404 chrome links carry the base.
    not_found = read(output, "404.html")
    assert 'href="/custom-wiki/">Go to the homepage</a>' in not_found
    assert 'href="/custom-wiki/#wikis"' in not_found
    assert 'href="/custom-wiki/llms.txt"' in not_found


# ---------------------------------------------------------------------------
# Root site (empty base path)
# ---------------------------------------------------------------------------

def test_empty_base_path_root_site(tmp_path: Path) -> None:
    generator, output = build_site(
        tmp_path, base_path="", site_origin="https://example.org"
    )
    page = read(output, "wiki", "base-ns", "wiki", "concepts", "plain-concept.md.html")
    assert '<link rel="stylesheet" href="/site.css">' in page
    assert '<a class="logo" href="/">Pixi Wiki</a>' in page
    assert 'data-registry="/index.json"' in page

    canonical = "https://example.org/wiki/base-ns/wiki/concepts/plain-concept.md.html"
    assert link_href(page, "canonical") == canonical
    assert og_content(page, "og:url") == canonical

    # Homepage canonical collapses to origin + "/".
    home = read(output, "index.html")
    assert link_href(home, "canonical") == "https://example.org/"


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def test_invalid_base_path_exits(tmp_path: Path) -> None:
    with pytest.raises(SystemExit) as excinfo:
        build_site(tmp_path, base_path="custom-wiki")
    assert "must be empty or start with" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Default build is unchanged
# ---------------------------------------------------------------------------

def test_default_build_uses_pixi_wiki_base(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    page = read(output, "wiki", "base-ns", "wiki", "concepts", "plain-concept.md.html")
    assert '<link rel="stylesheet" href="/pixi-wiki/site.css">' in page
