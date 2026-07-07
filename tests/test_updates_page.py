#!/usr/bin/env python3
"""Updates page + feed contracts (GitHub issue #81).

These exercise the build seam on a synthetic two-namespace fixture (not the
committed tree) so they stay green before the integrator regenerates and guard
the regenerated output afterwards. The surface (formerly "Recent Updates") is a
browsable, uncapped Updates page: a month index strip, per-date sections keyed
by ``data-date``, and per-namespace ``<details>`` roll-ups that open at five or
fewer entries. The clock-free sort is tested directly against
``sort_update_entries`` so a heavy corpus is unnecessary.
"""
from __future__ import annotations

import importlib.util
import json
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

    alpha = source / "alpha"
    (alpha / "wiki" / "concepts").mkdir(parents=True)
    (alpha / "README.md").write_text(
        """---
title: Alpha
updated: 2026-07-01
type: namespace
namespace: alpha
category: test
---

# Alpha

Alpha namespace fixture.

### Covers

Updates ordering.

### Not Covered

Nothing.

### Current As

2026-07-01
""",
        encoding="utf-8",
    )
    (alpha / "wiki" / "index.md").write_text(
        """---
title: Alpha Index
updated: 2026-07-05
type: index
namespace: alpha
---

# Alpha Index
""",
        encoding="utf-8",
    )
    # Six concept pages all dated 2026-06-15 so their namespace roll-up (count 6,
    # > 5) renders CLOSED, exercising the open/closed threshold.
    for i in range(6):
        (alpha / "wiki" / "concepts" / f"june-{i}.md").write_text(
            f"""---
title: June {i}
updated: 2026-06-15
type: concept
namespace: alpha
---

# June {i}

Body.
""",
            encoding="utf-8",
        )
    (alpha / "wiki" / "concepts" / "a-one.md").write_text(
        """---
title: A One
updated: 2026-07-05
type: concept
namespace: alpha
---

# A One

Body.
""",
        encoding="utf-8",
    )
    # No `updated` field — must be excluded from the feed.
    (alpha / "wiki" / "concepts" / "no-date.md").write_text(
        """---
title: No Date
type: concept
namespace: alpha
---

# No Date
""",
        encoding="utf-8",
    )
    # Non-date `updated` value — must be excluded from the feed.
    (alpha / "wiki" / "concepts" / "junk-date.md").write_text(
        """---
title: Junk Date
updated: soon
type: concept
namespace: alpha
---

# Junk Date
""",
        encoding="utf-8",
    )
    # CLAUDE.md carries a valid date but must never appear in the feed.
    (alpha / "CLAUDE.md").write_text(
        """---
title: Alpha Instructions
updated: 2026-07-09
---

# Alpha Instructions
""",
        encoding="utf-8",
    )

    beta = source / "beta"
    (beta / "wiki" / "concepts").mkdir(parents=True)
    (beta / "README.md").write_text(
        """---
title: Beta
updated: 2026-07-05
type: namespace
namespace: beta
category: test
---

# Beta

Beta namespace fixture.

### Covers

Cross-namespace ordering.

### Not Covered

Nothing.

### Current As

2026-07-05
""",
        encoding="utf-8",
    )
    (beta / "wiki" / "concepts" / "b-one.md").write_text(
        """---
title: B One
updated: 2026-07-07
type: concept
namespace: beta
---

# B One

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
    generator.build(source, output, ["alpha", "beta"])
    return generator, output


# Every qualifying fixture doc, in feed order (date DESC, namespace ASC, title ASC).
# 10 entries total: excludes no-date, junk-date, and CLAUDE.md.
EXPECTED_ORDER = [
    ("B One", "beta", "2026-07-07", "wiki/concepts/b-one.md"),
    ("A One", "alpha", "2026-07-05", "wiki/concepts/a-one.md"),
    ("Alpha Index", "alpha", "2026-07-05", "wiki/index.md"),
    ("Beta", "beta", "2026-07-05", "README.md"),
    ("Alpha", "alpha", "2026-07-01", "README.md"),
    ("June 0", "alpha", "2026-06-15", "wiki/concepts/june-0.md"),
    ("June 1", "alpha", "2026-06-15", "wiki/concepts/june-1.md"),
    ("June 2", "alpha", "2026-06-15", "wiki/concepts/june-2.md"),
    ("June 3", "alpha", "2026-06-15", "wiki/concepts/june-3.md"),
    ("June 4", "alpha", "2026-06-15", "wiki/concepts/june-4.md"),
    ("June 5", "alpha", "2026-06-15", "wiki/concepts/june-5.md"),
]


# --- updates.html ------------------------------------------------------------


def test_updates_html_exists_and_has_heading(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    updates = output / "updates.html"
    assert updates.exists()
    html = updates.read_text(encoding="utf-8")
    assert "<h1>Updates</h1>" in html


def test_updates_html_date_sections_have_id_and_data_date(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    html = (output / "updates.html").read_text(encoding="utf-8")
    sections = re.findall(
        r'<section class="updates-group" id="d-(\d{4}-\d{2}-\d{2})" data-date="(\d{4}-\d{2}-\d{2})">',
        html,
    )
    # Date DESC; id and data-date agree.
    assert sections == [
        ("2026-07-07", "2026-07-07"),
        ("2026-07-05", "2026-07-05"),
        ("2026-07-01", "2026-07-01"),
        ("2026-06-15", "2026-06-15"),
    ]


def test_updates_html_month_index_strip(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    html = (output / "updates.html").read_text(encoding="utf-8")
    # One link per distinct month, newest first, jumping to m- anchors.
    months = re.findall(r'<nav class="updates-months"[^>]*>(.*?)</nav>', html, re.DOTALL)
    assert months, "expected a month index strip"
    links = re.findall(r'href="#m-(\d{4}-\d{2})"', months[0])
    assert links == ["2026-07", "2026-06"]
    # The anchor targets exist, one per month, on that month's first date section.
    assert '<span class="updates-month-anchor" id="m-2026-07"></span>' in html
    assert '<span class="updates-month-anchor" id="m-2026-06"></span>' in html


def test_updates_html_namespace_details_open_closed_threshold(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    html = (output / "updates.html").read_text(encoding="utf-8")
    # The 2026-06-15 alpha roll-up has 6 entries (> 5) and renders CLOSED with a
    # count in its summary.
    assert '<details class="updates-ns"><summary>Alpha 6</summary>' in html
    # A small roll-up (<= 5) renders OPEN. 2026-07-07 has one beta entry.
    assert '<details class="updates-ns" open><summary>Beta 1</summary>' in html
    # No per-entry namespace badge inside the group (redundant); the old class
    # is gone.
    assert 'class="namespace-badge"' not in html


def test_updates_html_entries_link_html_and_raw(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    html = (output / "updates.html").read_text(encoding="utf-8")
    assert '<a class="updates-title" href="/pixi-wiki/wiki/beta/wiki/concepts/b-one.md.html">B One</a>' in html
    assert '<a class="updates-raw" href="/pixi-wiki/raw/beta/wiki/concepts/b-one.md">raw</a>' in html


def test_updates_html_body_order_matches_expected(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    html = (output / "updates.html").read_text(encoding="utf-8")
    titles = re.findall(r'<a class="updates-title" [^>]*>([^<]+)</a>', html)
    assert titles == [row[0] for row in EXPECTED_ORDER]


def test_updates_filter_script_injected_only_on_updates_page(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    updates = (output / "updates.html").read_text(encoding="utf-8")
    # The chip-bar script builds into the empty placeholder (no-JS safe).
    assert '<div class="updates-filter"></div>' in updates
    assert "var box=document.querySelector('.updates-filter')" in updates
    # Not present on other pages.
    home = (output / "index.html").read_text(encoding="utf-8")
    assert "var box=document.querySelector('.updates-filter')" not in home


def test_updates_css_rules_appended(tmp_path: Path) -> None:
    generator, _ = build_fixture(tmp_path)
    css = generator.site_css()
    assert ".updates-group{" in css
    assert ".updates-chip{" in css
    assert ".updates-ns " in css


def test_all_built_pages_carry_updates_nav_link(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    pages = [
        output / "index.html",
        output / "updates.html",
        output / "docs" / "AGENT_SETUP.html",
        output / "docs" / "REPLICATE_APPROACH.html",
        output / "docs" / "SIGNAL_GRAPH.html",
        output / "wiki" / "beta" / "wiki" / "concepts" / "b-one.md.html",
        output / "wiki" / "alpha" / "README.md.html",
    ]
    for page in pages:
        text = page.read_text(encoding="utf-8")
        header = re.search(r'<header class="site-header">.*?</header>', text, re.DOTALL)
        assert header, page
        assert '<a href="/pixi-wiki/updates.html">Updates</a>' in header.group(0), page


# --- recent.html redirect stub ----------------------------------------------


def test_recent_html_is_redirect_stub_to_updates(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    recent = output / "recent.html"
    assert recent.exists()
    html = recent.read_text(encoding="utf-8")
    assert '<meta http-equiv="refresh" content="0;url=/pixi-wiki/updates.html">' in html
    # A fallback link keeps the redirect usable if meta-refresh is disabled.
    assert '<a href="/pixi-wiki/updates.html">' in html
    # It is a stub: no full chrome (no site header / search placeholder).
    assert '<header class="site-header">' not in html


def test_recent_json_is_not_generated(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    assert not (output / "recent.json").exists()


def test_recent_and_updates_are_in_generated_root_files(tmp_path: Path) -> None:
    generator = load_generator()
    files = generator.GENERATED_ROOT_FILES
    # recent.html is still generated (as a stub); recent.json stays listed so a
    # rebuild removes the now-orphaned committed file.
    assert "recent.html" in files
    assert "recent.json" in files
    assert "updates.html" in files
    assert "updates.json" in files


# --- updates.json ------------------------------------------------------------


def test_updates_json_exists_and_carries_all_entries_uncapped(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    data = json.loads((output / "updates.json").read_text(encoding="utf-8"))
    assert data["generated_from"] == "frontmatter updated fields"
    # No cap: the feed count equals every qualifying fixture doc.
    assert data["count"] == len(EXPECTED_ORDER)
    assert len(data["entries"]) == len(EXPECTED_ORDER)


def test_no_recent_limit_constant(tmp_path: Path) -> None:
    generator = load_generator()
    assert not hasattr(generator, "RECENT_LIMIT")


def test_updates_json_entries_order_and_fields(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    data = json.loads((output / "updates.json").read_text(encoding="utf-8"))
    observed = [(e["title"], e["namespace"], e["updated"], e["path"]) for e in data["entries"]]
    assert observed == EXPECTED_ORDER

    first = data["entries"][0]
    assert first == {
        "title": "B One",
        "path": "wiki/concepts/b-one.md",
        "namespace": "beta",
        "namespace_title": "Beta",
        "updated": "2026-07-07",
        "raw": "/raw/beta/wiki/concepts/b-one.md",
        "html": "/wiki/beta/wiki/concepts/b-one.md.html",
    }


def test_updates_json_excludes_undated_junk_and_claude(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    data = json.loads((output / "updates.json").read_text(encoding="utf-8"))
    paths = {e["path"] for e in data["entries"]}
    assert "wiki/concepts/no-date.md" not in paths
    assert "wiki/concepts/junk-date.md" not in paths
    assert "CLAUDE.md" not in paths


# --- determinism -------------------------------------------------------------


def test_rebuild_is_byte_identical(tmp_path: Path) -> None:
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    out_a = tmp_path / "a"
    out_b = tmp_path / "b"
    out_a.mkdir()
    out_b.mkdir()
    generator.build(source, out_a, ["alpha", "beta"])
    generator.build(source, out_b, ["alpha", "beta"])
    assert (out_a / "updates.html").read_bytes() == (out_b / "updates.html").read_bytes()
    assert (out_a / "updates.json").read_bytes() == (out_b / "updates.json").read_bytes()
    assert (out_a / "recent.html").read_bytes() == (out_b / "recent.html").read_bytes()


# --- sort logic (direct, no heavy build) -------------------------------------


def test_sort_orders_by_date_then_namespace_then_title() -> None:
    generator = load_generator()
    entries = [
        {"title": "Alpha Index", "namespace": "alpha", "updated": "2026-07-05"},
        {"title": "Beta", "namespace": "beta", "updated": "2026-07-05"},
        {"title": "A One", "namespace": "alpha", "updated": "2026-07-05"},
        {"title": "B One", "namespace": "beta", "updated": "2026-07-07"},
        {"title": "Alpha", "namespace": "alpha", "updated": "2026-07-01"},
    ]
    ordered = generator.sort_update_entries(entries)
    assert [(e["title"], e["namespace"], e["updated"]) for e in ordered] == [
        ("B One", "beta", "2026-07-07"),
        ("A One", "alpha", "2026-07-05"),
        ("Alpha Index", "alpha", "2026-07-05"),
        ("Beta", "beta", "2026-07-05"),
        ("Alpha", "alpha", "2026-07-01"),
    ]
