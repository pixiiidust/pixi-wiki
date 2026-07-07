#!/usr/bin/env python3
"""Build-seam tests for issue #64: subfolder grouping + sidebar filter box.

Each test drives a fixture vault through ``build`` and inspects the emitted
namespace HTML, mirroring the fixture pattern in ``test_renderer.py``.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "build_from_pixi_vault.py"

FILTER_MARKER = "document.querySelectorAll('.sidebar-filter')"


def load_generator():
    spec = importlib.util.spec_from_file_location("build_from_pixi_vault", GENERATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_scaffold(ns: Path, slug: str) -> None:
    """Write the README + wiki/index the generator requires for every vault."""
    (ns / "wiki").mkdir(parents=True, exist_ok=True)
    (ns / "README.md").write_text(
        f"""---
title: {slug}
created: 2026-06-16
updated: 2026-06-16
type: namespace
status: active
namespace: {slug}
category: test
---

# {slug}

A grouping fixture.

### Covers

Grouping.

### Not Covered

Nothing.

### Current As

2026-06-16
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "index.md").write_text(
        f"""---
title: {slug} Index
created: 2026-06-16
updated: 2026-06-16
type: index
status: active
namespace: {slug}
---

# {slug} Index
""",
        encoding="utf-8",
    )


def _write_concept(ns: Path, rel_path: str, title: str) -> None:
    target = ns / "wiki" / "concepts" / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"""---
title: {title}
created: 2026-06-16
updated: 2026-06-16
type: concept
status: compiled
namespace: {ns.name}
---

# {title}
""",
        encoding="utf-8",
    )


def _build(tmp_path: Path, slug: str) -> Path:
    generator = load_generator()
    source = tmp_path / "source" / "wikis"
    output = tmp_path / "output"
    output.mkdir(parents=True)
    generator.build(source, output, [slug])
    return output / "wiki" / slug


# ---------------------------------------------------------------------------
# Fixture A: flat concepts, at or below threshold -> render exactly as today
# ---------------------------------------------------------------------------

def test_flat_namespace_renders_identically(tmp_path: Path) -> None:
    slug = "ns-a"
    ns = tmp_path / "source" / "wikis" / slug
    _write_scaffold(ns, slug)
    _write_concept(ns, "gamma-concept.md", "Gamma Concept")
    _write_concept(ns, "alpha-concept.md", "Alpha Concept")
    _write_concept(ns, "beta-concept.md", "Beta Concept")

    out_ns = _build(tmp_path, slug)
    # Read the README page: it is not a concept, so the CONCEPTS section stays
    # closed with no active link -> the pure flat shape.
    html = (out_ns / "README.md.html").read_text(encoding="utf-8")

    expected_section = (
        '<details class="sidebar-section"><summary>CONCEPTS 3</summary>'
        '<div class="sidebar-section-body">'
        f'<a href="/pixi-wiki/wiki/{slug}/wiki/concepts/alpha-concept.md.html"><span aria-hidden="true">📄 </span>Alpha Concept</a>'
        f'<a href="/pixi-wiki/wiki/{slug}/wiki/concepts/beta-concept.md.html"><span aria-hidden="true">📄 </span>Beta Concept</a>'
        f'<a href="/pixi-wiki/wiki/{slug}/wiki/concepts/gamma-concept.md.html"><span aria-hidden="true">📄 </span>Gamma Concept</a>'
        '</div></details>'
    )
    assert expected_section in html
    # No grouping/filter markup is emitted (the class names still appear once
    # each in the stylesheet, so match the element form).
    assert 'class="sidebar-subgroup"' not in html
    assert 'class="sidebar-filter"' not in html


# ---------------------------------------------------------------------------
# Fixture B: direct + subfoldered concepts, above threshold -> groups + filter
# ---------------------------------------------------------------------------

def _build_namespace_b(tmp_path: Path) -> Path:
    slug = "ns-b"
    ns = tmp_path / "source" / "wikis" / slug
    _write_scaffold(ns, slug)
    # 2 direct concepts, 20 under patterns/, 5 under other/  -> 27 total (>25)
    _write_concept(ns, "aaa-direct.md", "Aaa Direct")
    _write_concept(ns, "zzz-direct.md", "Zzz Direct")
    for i in range(1, 21):
        _write_concept(ns, f"patterns/pattern-{i:02d}.md", f"Pattern {i:02d}")
    for i in range(1, 6):
        _write_concept(ns, f"other/other-{i:02d}.md", f"Other {i:02d}")
    return _build(tmp_path, slug)


def test_grouped_namespace_has_subgroups_filter_and_total(tmp_path: Path) -> None:
    out_ns = _build_namespace_b(tmp_path)
    html = (out_ns / "README.md.html").read_text(encoding="utf-8")

    # Section summary still shows LABEL <total>, counting subgroup members.
    assert "<summary>CONCEPTS 27</summary>" in html
    # One collapsible group per subfolder, alphabetical, with counts.
    assert '<details class="sidebar-subgroup"><summary>OTHER 5</summary>' in html
    assert '<details class="sidebar-subgroup"><summary>PATTERNS 20</summary>' in html
    # Filter box present for the above-threshold section.
    assert '<input class="sidebar-filter" type="search" placeholder="Filter…" aria-label="Filter pages">' in html

    # Direct files list before the subgroups.
    direct_index = html.index(">Aaa Direct</a>")
    other_index = html.index("<summary>OTHER 5</summary>")
    patterns_index = html.index("<summary>PATTERNS 20</summary>")
    assert direct_index < other_index < patterns_index
    # OTHER sorts before PATTERNS alphabetically.
    assert html.index("<summary>OTHER 5</summary>") < html.index("<summary>PATTERNS 20</summary>")


def test_active_page_inside_subgroup_expands_section_and_group(tmp_path: Path) -> None:
    out_ns = _build_namespace_b(tmp_path)
    html = (out_ns / "wiki" / "concepts" / "patterns" / "pattern-05.md.html").read_text(encoding="utf-8")

    # Outer section is open...
    assert '<details class="sidebar-section" open><summary>CONCEPTS 27</summary>' in html
    # ...and the containing subgroup is open...
    assert '<details class="sidebar-subgroup" open><summary>PATTERNS 20</summary>' in html
    # ...and the active class lands on the active page's link.
    assert (
        '<a class="active" aria-current="page" href="/pixi-wiki/wiki/ns-b/wiki/concepts/patterns/pattern-05.md.html"><span aria-hidden="true">📄 </span>Pattern 05</a>'
        in html
    )
    # A sibling subgroup with no active member stays closed.
    assert '<details class="sidebar-subgroup"><summary>OTHER 5</summary>' in html


def test_filter_script_included_exactly_once(tmp_path: Path) -> None:
    out_ns = _build_namespace_b(tmp_path)
    html = (out_ns / "README.md.html").read_text(encoding="utf-8")
    assert html.count(FILTER_MARKER) == 1


def test_site_css_has_grouping_rules() -> None:
    generator = load_generator()
    css = generator.site_css()
    assert ".sidebar-subgroup" in css
    assert ".sidebar-filter" in css
