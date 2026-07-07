#!/usr/bin/env python3
"""Updates page + feed contracts (GitHub issue #81).

These exercise the build seam on a synthetic two-namespace fixture (not the
committed tree) so they stay green before the integrator regenerates and guard
the regenerated output afterwards. The surface (formerly "Recent Updates") is a
browsable, uncapped Updates page: a month index strip, per-date sections keyed
by ``data-date``, and per-namespace ``<details>`` roll-ups, closed by default,
with bracketed counts. The clock-free sort is tested directly against
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
    # > 5) exercises the bracketed-count summary on a large group.
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


def test_updates_html_namespace_details_closed_with_bracketed_count(tmp_path: Path) -> None:
    _, output = build_fixture(tmp_path)
    html = (output / "updates.html").read_text(encoding="utf-8")
    # Every roll-up renders CLOSED by default, with the count in brackets.
    assert '<details class="updates-ns"><summary>Alpha (6)</summary>' in html
    assert '<details class="updates-ns"><summary>Beta (1)</summary>' in html
    assert '<details class="updates-ns" open' not in html
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


# --- single-page corpus (the small fixture stays one page) -------------------


def test_single_page_corpus_has_no_pagination_bar(tmp_path: Path) -> None:
    # The small fixture's 11 entries are well under the 60-entry target, so it
    # renders as a single page with no pagination bar and no updates/ subdir.
    _, output = build_fixture(tmp_path)
    html = (output / "updates.html").read_text(encoding="utf-8")
    assert '<nav class="pagination"' not in html
    assert not (output / "updates").exists()


# --- chunking (pure function, no disk) ---------------------------------------


def _groups(*sizes_dates):
    """Build synthetic date sections: each arg is (date, entry_count)."""
    return [
        (date, [{"updated": date, "n": i} for i in range(count)])
        for date, count in sizes_dates
    ]


def test_paginate_never_splits_a_date_section() -> None:
    generator = load_generator()
    # A single import day far larger than the target stays one page.
    groups = _groups(("2026-05-03", 259))
    pages = generator.paginate_update_groups(groups, target=60)
    assert len(pages) == 1
    assert len(pages[0]) == 1
    assert sum(len(items) for _d, items in pages[0]) == 259


def test_paginate_accumulates_whole_sections_to_soft_cap() -> None:
    generator = load_generator()
    # 40 + 40 crosses 60 on the second section -> page 1 = [d1, d2]; the trailing
    # 25-entry section becomes page 2. Newest dates land on page 1.
    groups = _groups(
        ("2026-05-10", 40),
        ("2026-05-09", 40),
        ("2026-05-08", 25),
    )
    pages = generator.paginate_update_groups(groups, target=60)
    dates = [[d for d, _ in page] for page in pages]
    assert dates == [["2026-05-10", "2026-05-09"], ["2026-05-08"]]


def test_paginate_respects_real_constant_over_60_entries() -> None:
    import datetime

    generator = load_generator()
    assert generator.UPDATES_PAGE_ENTRY_TARGET == 60
    # 61 single-entry days (fixed, clock-free) -> the 60th flushes page 1 with
    # exactly 60 sections; the 61st opens page 2. Uses the real default target.
    start = datetime.date(2026, 6, 30)
    dates = [(start - datetime.timedelta(days=i)).isoformat() for i in range(61)]
    groups = _groups(*[(d, 1) for d in dates])
    pages = generator.paginate_update_groups(groups)
    assert len(pages) == 2
    assert len(pages[0]) == 60
    assert len(pages[1]) == 1


def test_paginate_empty_corpus_yields_one_page() -> None:
    generator = load_generator()
    pages = generator.paginate_update_groups([], target=60)
    assert pages == [[]]


# --- pagination window (pure function) ---------------------------------------


def test_pagination_window_shows_all_when_short() -> None:
    generator = load_generator()
    assert generator.pagination_window(3, 9) == list(range(1, 10))
    assert generator.pagination_window(1, 1) == [1]


def test_pagination_window_collapses_middle_for_twelve_pages() -> None:
    generator = load_generator()
    # 12 pages, current 6: first, current +/- 2, last, gaps -> ellipsis (None).
    assert generator.pagination_window(6, 12) == [1, None, 4, 5, 6, 7, 8, None, 12]
    # Near the start only the tail collapses.
    assert generator.pagination_window(2, 12) == [1, 2, 3, 4, None, 12]
    # Near the end only the head collapses.
    assert generator.pagination_window(11, 12) == [1, None, 9, 10, 11, 12]


# --- multi-page build --------------------------------------------------------


def write_paginated_fixture_source(base: Path) -> Path:
    """A corpus large enough to force at least two Updates pages under the cap.

    One namespace, dates chosen so page 1 holds the two newest 2026-05 sections
    and page 2 holds the older 2026-04 section — giving a cross-page month strip.
    """
    source = base / "psource" / "wikis"
    big = source / "big"
    (big / "wiki" / "concepts").mkdir(parents=True)
    (big / "README.md").write_text(
        """---
title: Big
updated: 2026-04-10
type: namespace
namespace: big
category: test
---

# Big

Big namespace fixture.

### Covers

Pagination.

### Not Covered

Nothing.

### Current As

2026-04-10
""",
        encoding="utf-8",
    )
    plan = [("2026-05-20", 30), ("2026-05-19", 30), ("2026-04-10", 29)]
    for date, count in plan:
        for i in range(count):
            (big / "wiki" / "concepts" / f"{date}-{i:03d}.md").write_text(
                f"""---
title: Doc {date} {i:03d}
updated: {date}
type: concept
namespace: big
---

# Doc {date} {i:03d}

Body.
""",
                encoding="utf-8",
            )
    return source


def build_paginated_fixture(tmp_path: Path):
    generator = load_generator()
    source = write_paginated_fixture_source(tmp_path)
    output = tmp_path / "poutput"
    output.mkdir()
    generator.build(source, output, ["big"])
    return generator, output


def _page_date_map(generator, output: Path):
    """Return (pages, dates_by_page) derived from the generator's own chunker."""
    data = json.loads((output / "updates.json").read_text(encoding="utf-8"))
    groups = generator.group_updates_by_date(data["entries"])
    pages = generator.paginate_update_groups(groups)
    dates_by_page = [[d for d, _ in page] for page in pages]
    return pages, dates_by_page


def test_multipage_layout_paths_and_counts(tmp_path: Path) -> None:
    generator, output = build_paginated_fixture(tmp_path)
    pages, dates_by_page = _page_date_map(generator, output)
    assert len(pages) >= 2
    # Page 1 at /updates.html; page N>=2 at /updates/N.html.
    assert (output / "updates.html").exists()
    for n in range(2, len(pages) + 1):
        assert (output / "updates" / f"{n}.html").exists()
    # No stray page beyond the count.
    assert not (output / "updates" / f"{len(pages) + 1}.html").exists()


def test_multipage_no_date_section_split_and_descending(tmp_path: Path) -> None:
    generator, output = build_paginated_fixture(tmp_path)
    pages, dates_by_page = _page_date_map(generator, output)
    # Every date lives on exactly one page.
    seen: set[str] = set()
    for dates in dates_by_page:
        for d in dates:
            assert d not in seen
            seen.add(d)
    # Page 1 holds the newest dates; each later page continues descending.
    for earlier, later in zip(dates_by_page, dates_by_page[1:]):
        assert min(earlier) > max(later)
    # And the rendered sections on each page match the chunk assignment.
    for n, dates in enumerate(dates_by_page, start=1):
        path = output / "updates.html" if n == 1 else output / "updates" / f"{n}.html"
        html = path.read_text(encoding="utf-8")
        rendered = re.findall(r'<section class="updates-group" id="d-(\d{4}-\d{2}-\d{2})"', html)
        assert rendered == dates


def test_chips_and_filter_script_only_on_page_one(tmp_path: Path) -> None:
    generator, output = build_paginated_fixture(tmp_path)
    page1 = (output / "updates.html").read_text(encoding="utf-8")
    page2 = (output / "updates" / "2.html").read_text(encoding="utf-8")
    assert '<div class="updates-filter"></div>' in page1
    assert "var box=document.querySelector('.updates-filter')" in page1
    # Deeper pages get neither the placeholder nor the filter script.
    assert '<div class="updates-filter"></div>' not in page2
    assert "var box=document.querySelector('.updates-filter')" not in page2


def test_pagination_bar_on_every_page(tmp_path: Path) -> None:
    generator, output = build_paginated_fixture(tmp_path)
    pages, _ = _page_date_map(generator, output)
    total = len(pages)
    for n in range(1, total + 1):
        path = output / "updates.html" if n == 1 else output / "updates" / f"{n}.html"
        html = path.read_text(encoding="utf-8")
        assert '<nav class="pagination" aria-label="Pagination">' in html
        # Current pill carries aria-current and shows this page number.
        assert f'<span class="pagination-pill pagination-current" aria-current="page">{n}</span>' in html
        # Prev present iff not first; Next present iff not last.
        assert ('rel="prev"' in html) == (n > 1)
        assert ('rel="next"' in html) == (n < total)
        # Head rel prev/next mirror the bar.
        head = html.split("</head>")[0]
        assert ('<link rel="prev"' in head) == (n > 1)
        assert ('<link rel="next"' in head) == (n < total)


def test_pagination_numbers_link_correct_pages(tmp_path: Path) -> None:
    generator, output = build_paginated_fixture(tmp_path)
    page1 = (output / "updates.html").read_text(encoding="utf-8")
    # Page 2 pill links to the subdir page; Next too.
    assert '<a class="pagination-pill" href="/pixi-wiki/updates/2.html">2</a>' in page1
    assert '<a class="pagination-next" rel="next" href="/pixi-wiki/updates/2.html">Next →</a>' in page1
    page2 = (output / "updates" / "2.html").read_text(encoding="utf-8")
    # Prev on page 2 points back at the root updates.html, and pill 1 too.
    assert '<a class="pagination-prev" rel="prev" href="/pixi-wiki/updates.html">← Prev</a>' in page2
    assert '<a class="pagination-pill" href="/pixi-wiki/updates.html">1</a>' in page2


def test_month_strip_cross_page_hrefs(tmp_path: Path) -> None:
    generator, output = build_paginated_fixture(tmp_path)
    pages, dates_by_page = _page_date_map(generator, output)
    # Determine each month's home page from the chunk assignment.
    month_page: dict[str, int] = {}
    for n, dates in enumerate(dates_by_page, start=1):
        for d in dates:
            month_page.setdefault(d[:7], n)
    assert "2026-05" in month_page and "2026-04" in month_page
    page1 = (output / "updates.html").read_text(encoding="utf-8")
    strip1 = re.search(r'<nav class="updates-months"[^>]*>(.*?)</nav>', page1, re.DOTALL).group(1)
    # 2026-05 lives on page 1 -> bare anchor; 2026-04 lives on page 2 -> cross-page.
    assert 'href="#m-2026-05"' in strip1
    assert 'href="/pixi-wiki/updates/2.html#m-2026-04"' in strip1

    page2 = (output / "updates" / "2.html").read_text(encoding="utf-8")
    strip2 = re.search(r'<nav class="updates-months"[^>]*>(.*?)</nav>', page2, re.DOTALL).group(1)
    # From page 2, its own month is bare and page-1's month cross-links back.
    assert 'href="#m-2026-04"' in strip2
    assert 'href="/pixi-wiki/updates.html#m-2026-05"' in strip2
    # The m- anchor for the page-2 month is physically on page 2.
    assert '<span class="updates-month-anchor" id="m-2026-04"></span>' in page2
    assert '<span class="updates-month-anchor" id="m-2026-05"></span>' in page1


def test_multipage_canonicals(tmp_path: Path) -> None:
    generator, output = build_paginated_fixture(tmp_path)
    page1 = (output / "updates.html").read_text(encoding="utf-8")
    page2 = (output / "updates" / "2.html").read_text(encoding="utf-8")
    assert '<link rel="canonical" href="https://pixiiidust.github.io/pixi-wiki/updates.html">' in page1
    assert '<link rel="canonical" href="https://pixiiidust.github.io/pixi-wiki/updates/2.html">' in page2
    # Page 2 title reflects the page number.
    assert "<title>Updates — page 2 — Pixi Wiki</title>" in page2


def test_sitemap_contains_every_updates_page(tmp_path: Path) -> None:
    generator, output = build_paginated_fixture(tmp_path)
    pages, _ = _page_date_map(generator, output)
    sitemap = (output / "sitemap.xml").read_text(encoding="utf-8")
    assert "<loc>https://pixiiidust.github.io/pixi-wiki/updates.html</loc>" in sitemap
    for n in range(2, len(pages) + 1):
        assert f"<loc>https://pixiiidust.github.io/pixi-wiki/updates/{n}.html</loc>" in sitemap


def test_multipage_rebuild_is_byte_identical(tmp_path: Path) -> None:
    generator = load_generator()
    source = write_paginated_fixture_source(tmp_path)
    out_a = tmp_path / "pa"
    out_b = tmp_path / "pb"
    out_a.mkdir()
    out_b.mkdir()
    generator.build(source, out_a, ["big"])
    generator.build(source, out_b, ["big"])
    assert (out_a / "updates.html").read_bytes() == (out_b / "updates.html").read_bytes()
    assert (out_a / "updates" / "2.html").read_bytes() == (out_b / "updates" / "2.html").read_bytes()
    assert (out_a / "sitemap.xml").read_bytes() == (out_b / "sitemap.xml").read_bytes()


def test_updates_dir_is_cleaned_on_rebuild(tmp_path: Path) -> None:
    generator = load_generator()
    assert "updates" in generator.GENERATED_DIRS
    source = write_paginated_fixture_source(tmp_path)
    output = tmp_path / "clean-out"
    output.mkdir()
    generator.build(source, output, ["big"])
    # Plant a stale page, then confirm a rebuild removes the whole updates/ tree.
    stale = output / "updates" / "999.html"
    stale.write_text("stale", encoding="utf-8")
    generator.build(source, output, ["big"])
    assert not stale.exists()


def test_pagination_css_rules_appended(tmp_path: Path) -> None:
    generator = load_generator()
    css = generator.site_css()
    assert ".pagination{" in css
    assert ".pagination-current" in css
    assert ".pagination-ellipsis" in css
