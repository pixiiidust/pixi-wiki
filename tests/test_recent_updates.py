#!/usr/bin/env python3
"""Recent Updates page + feed contracts (GitHub issue #59).

These exercise the build seam on a synthetic two-namespace fixture (not the
committed tree) so they stay green before the #65 regeneration and guard the
regenerated output afterwards. The sort/cap logic is additionally tested
directly against ``sort_recent_entries`` so a >50-entry corpus is unnecessary.
"""
from __future__ import annotations

import importlib.util
import json
import re
from datetime import date, timedelta
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

Recent updates ordering.

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


# Expected feed order: (date DESC, namespace ASC, title ASC).
EXPECTED_ORDER = [
    ("B One", "beta", "2026-07-07", "wiki/concepts/b-one.md"),
    ("A One", "alpha", "2026-07-05", "wiki/concepts/a-one.md"),
    ("Alpha Index", "alpha", "2026-07-05", "wiki/index.md"),
    ("Beta", "beta", "2026-07-05", "README.md"),
    ("Alpha", "alpha", "2026-07-01", "README.md"),
]


# --- recent.html -------------------------------------------------------------


def test_recent_html_exists_and_has_heading(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    recent = output / "recent.html"
    assert recent.exists()
    html = recent.read_text(encoding="utf-8")
    assert "<h1>Recent Updates</h1>" in html


def test_recent_html_groups_by_date_descending(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    html = (output / "recent.html").read_text(encoding="utf-8")
    dates = re.findall(r'<section class="recent-group"><h2>(\d{4}-\d{2}-\d{2})</h2>', html)
    assert dates == ["2026-07-07", "2026-07-05", "2026-07-01"]


def test_recent_html_links_html_raw_and_namespace_badge(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    html = (output / "recent.html").read_text(encoding="utf-8")
    # Title links to the rendered HTML page.
    assert '<a class="recent-title" href="/pixi-wiki/wiki/beta/wiki/concepts/b-one.md.html">B One</a>' in html
    # Raw link points at the Markdown mirror.
    assert '<a class="recent-raw" href="/pixi-wiki/raw/beta/wiki/concepts/b-one.md">raw</a>' in html
    # Namespace badge links to that namespace's README.
    assert '<a class="namespace-badge" href="/pixi-wiki/wiki/beta/README.md.html">Beta</a>' in html
    assert '<a class="namespace-badge" href="/pixi-wiki/wiki/alpha/README.md.html">Alpha</a>' in html


def test_recent_html_body_order_matches_expected(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    html = (output / "recent.html").read_text(encoding="utf-8")
    titles = re.findall(r'<a class="recent-title" [^>]*>([^<]+)</a>', html)
    assert titles == [row[0] for row in EXPECTED_ORDER]


def test_recent_css_badge_rule_appended(tmp_path: Path) -> None:
    generator, _ = build_fixture(tmp_path)
    css = generator.site_css()
    assert ".namespace-badge{" in css
    assert ".recent-group{" in css


def test_all_built_pages_carry_recent_header_link(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    pages = [
        output / "index.html",
        output / "recent.html",
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
        assert '<a href="/pixi-wiki/recent.html">Recent</a>' in header.group(0), page


# --- recent.json -------------------------------------------------------------


def test_recent_json_exists_and_parses(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    data = json.loads((output / "recent.json").read_text(encoding="utf-8"))
    assert data["generated_from"] == "frontmatter updated fields"
    assert data["count"] == len(EXPECTED_ORDER)
    assert len(data["entries"]) == len(EXPECTED_ORDER)


def test_recent_json_entries_order_and_fields(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    data = json.loads((output / "recent.json").read_text(encoding="utf-8"))
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


def test_recent_json_excludes_undated_junk_and_claude(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    data = json.loads((output / "recent.json").read_text(encoding="utf-8"))
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
    assert (out_a / "recent.html").read_bytes() == (out_b / "recent.html").read_bytes()
    assert (out_a / "recent.json").read_bytes() == (out_b / "recent.json").read_bytes()


# --- sort / cap logic (direct, no heavy build) -------------------------------


def test_sort_orders_by_date_then_namespace_then_title() -> None:
    generator = load_generator()
    entries = [
        {"title": "Alpha Index", "namespace": "alpha", "updated": "2026-07-05"},
        {"title": "Beta", "namespace": "beta", "updated": "2026-07-05"},
        {"title": "A One", "namespace": "alpha", "updated": "2026-07-05"},
        {"title": "B One", "namespace": "beta", "updated": "2026-07-07"},
        {"title": "Alpha", "namespace": "alpha", "updated": "2026-07-01"},
    ]
    ordered = generator.sort_recent_entries(entries)
    assert [(e["title"], e["namespace"], e["updated"]) for e in ordered] == [
        ("B One", "beta", "2026-07-07"),
        ("A One", "alpha", "2026-07-05"),
        ("Alpha Index", "alpha", "2026-07-05"),
        ("Beta", "beta", "2026-07-05"),
        ("Alpha", "alpha", "2026-07-01"),
    ]


def test_cap_keeps_the_most_recent_entries() -> None:
    generator = load_generator()
    assert generator.RECENT_LIMIT == 50
    total = 60
    entries = [
        {"title": f"Doc {i:02d}", "namespace": "ns", "updated": (date(2020, 1, 1) + timedelta(days=i)).isoformat()}
        for i in range(total)
    ]
    capped = generator.sort_recent_entries(entries)[: generator.RECENT_LIMIT]
    assert len(capped) == generator.RECENT_LIMIT
    # The newest entry (largest offset) is first; the 10 oldest are dropped.
    assert capped[0]["title"] == "Doc 59"
    dropped = {f"Doc {i:02d}" for i in range(total - generator.RECENT_LIMIT)}
    kept = {e["title"] for e in capped}
    assert kept.isdisjoint(dropped)
