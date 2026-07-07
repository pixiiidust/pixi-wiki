#!/usr/bin/env python3
"""Build-seam tests for SEO/social metadata, sitemap.xml, and the 404 page."""

from __future__ import annotations

import html as htmllib
import importlib.util
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "build_from_pixi_vault.py"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def load_generator():
    spec = importlib.util.spec_from_file_location("build_from_pixi_vault", GENERATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The namespace README first paragraph — used for the namespace description and
# for every README page's meta description.
NAMESPACE_DESCRIPTION = "A fixture namespace used to exercise SEO surface metadata."
PLAIN_FIRST_PARAGRAPH = "This concept page has a clean first paragraph that becomes its meta description."
# A first paragraph containing characters that MUST be HTML-escaped in attributes.
ESCAPED_FIRST_PARAGRAPH = 'He said "hello" and used <script> tags in prose.'
# 40 space-separated 6-char words ~= 279 chars, comfortably over the ~200 cap.
LONG_FIRST_PARAGRAPH = " ".join(f"word{i:02d}" for i in range(40))


def write_fixture_source(base: Path) -> Path:
    source = base / "source" / "wikis"
    ns = source / "seo-ns"
    (ns / "wiki" / "concepts").mkdir(parents=True)
    (ns / "README.md").write_text(
        f"""---
title: SEO Namespace
created: 2026-01-02
updated: 2026-01-02
type: namespace
status: active
namespace: seo-ns
category: test
---

# SEO Namespace

{NAMESPACE_DESCRIPTION}

### Covers

SEO metadata coverage.
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "concepts" / "plain-concept.md").write_text(
        f"""---
title: Plain Concept
created: 2026-01-03
updated: 2026-01-03
type: concept
status: compiled
namespace: seo-ns
---

# Plain Concept

{PLAIN_FIRST_PARAGRAPH}
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "concepts" / "escaped-concept.md").write_text(
        f"""---
title: Escaped Concept
created: 2026-01-04
updated: 2026-01-04
type: concept
status: compiled
namespace: seo-ns
---

# Escaped Concept

{ESCAPED_FIRST_PARAGRAPH}
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "concepts" / "long-concept.md").write_text(
        f"""---
title: Long Concept
created: 2026-01-05
updated: 2026-01-05
type: concept
status: compiled
namespace: seo-ns
---

# Long Concept

{LONG_FIRST_PARAGRAPH}
""",
        encoding="utf-8",
    )
    (ns / "wiki" / "concepts" / "undated-concept.md").write_text(
        """---
title: Undated Concept
created: 2026-01-06
updated: TBD
type: concept
status: compiled
namespace: seo-ns
---

# Undated Concept

A page whose updated field is not a strict ISO date, so it gets no lastmod.
""",
        encoding="utf-8",
    )
    return source


def build_site(tmp_path: Path):
    generator = load_generator()
    source = write_fixture_source(tmp_path)
    output = tmp_path / "output"
    output.mkdir()
    generator.build(source, output, ["seo-ns"])
    return generator, output


def read(output: Path, *parts: str) -> str:
    return output.joinpath(*parts).read_text(encoding="utf-8")


def meta_content(html_text: str, attr: str, name: str) -> str | None:
    match = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)">', html_text)
    return match.group(1) if match else None


def link_href(html_text: str, rel: str) -> str | None:
    match = re.search(rf'<link rel="{re.escape(rel)}" href="([^"]*)">', html_text)
    return match.group(1) if match else None


def og_content(html_text: str, prop: str) -> str | None:
    match = re.search(rf'<meta property="{re.escape(prop)}" content="([^"]*)">', html_text)
    return match.group(1) if match else None


# ---------------------------------------------------------------------------
# Head metadata
# ---------------------------------------------------------------------------

def test_document_page_has_description_canonical_and_og(tmp_path: Path) -> None:
    generator, output = build_site(tmp_path)
    html_text = read(output, "wiki", "seo-ns", "wiki", "concepts", "plain-concept.md.html")

    assert meta_content(html_text, "name", "description") == PLAIN_FIRST_PARAGRAPH
    canonical = generator.SITE_ORIGIN + "/pixi-wiki/wiki/seo-ns/wiki/concepts/plain-concept.md.html"
    assert link_href(html_text, "canonical") == canonical
    assert og_content(html_text, "og:url") == canonical
    assert og_content(html_text, "og:description") == PLAIN_FIRST_PARAGRAPH
    assert og_content(html_text, "og:type") == "article"
    assert "Plain Concept" in (og_content(html_text, "og:title") or "")
    assert meta_content(html_text, "name", "twitter:card") == "summary"


def test_readme_page_uses_namespace_description(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    html_text = read(output, "wiki", "seo-ns", "README.md.html")
    assert meta_content(html_text, "name", "description") == NAMESPACE_DESCRIPTION


def test_homepage_and_updates_have_static_descriptions(tmp_path: Path) -> None:
    generator, output = build_site(tmp_path)
    home = read(output, "index.html")
    updates = read(output, "updates.html")
    assert htmllib.unescape(meta_content(home, "name", "description")) == generator.HOME_DESCRIPTION
    assert og_content(home, "og:type") == "website"
    assert htmllib.unescape(meta_content(updates, "name", "description")) == generator.UPDATES_DESCRIPTION


def test_description_special_characters_are_escaped(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    html_text = read(output, "wiki", "seo-ns", "wiki", "concepts", "escaped-concept.md.html")
    desc = meta_content(html_text, "name", "description")
    assert desc is not None
    assert "&quot;hello&quot;" in desc
    assert "&lt;script&gt;" in desc
    # No raw quote/angle-bracket leaked into the attribute value.
    assert '"' not in desc
    assert "<" not in desc


def test_long_first_paragraph_truncates_at_word_boundary(tmp_path: Path) -> None:
    generator, output = build_site(tmp_path)
    html_text = read(output, "wiki", "seo-ns", "wiki", "concepts", "long-concept.md.html")
    desc = meta_content(html_text, "name", "description")
    assert desc is not None
    assert len(desc) <= 200
    assert desc.endswith("…")
    stem = desc[:-1]
    # The retained prefix is whole words: it is a prefix of the source and the
    # next source character is a space, so no word was cut in half.
    assert LONG_FIRST_PARAGRAPH.startswith(stem)
    assert LONG_FIRST_PARAGRAPH[len(stem)] == " "


def test_truncate_description_helper_word_boundary() -> None:
    generator = load_generator()
    out = generator.truncate_description(LONG_FIRST_PARAGRAPH, limit=50)
    assert len(out) <= 50
    assert " word" not in out[-6:]  # trailing text is a complete word + ellipsis


# ---------------------------------------------------------------------------
# sitemap.xml
# ---------------------------------------------------------------------------

def test_sitemap_lists_every_page_with_conditional_lastmod(tmp_path: Path) -> None:
    generator, output = build_site(tmp_path)
    sitemap_path = output / "sitemap.xml"
    assert sitemap_path.exists()

    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    urls = root.findall("sm:url", SITEMAP_NS)
    locs = [u.find("sm:loc", SITEMAP_NS).text for u in urls]
    lastmods = {
        u.find("sm:loc", SITEMAP_NS).text: (
            u.find("sm:lastmod", SITEMAP_NS).text if u.find("sm:lastmod", SITEMAP_NS) is not None else None
        )
        for u in urls
    }

    origin = generator.SITE_ORIGIN
    # Homepage is first and undated.
    assert locs[0] == origin + "/pixi-wiki/"
    assert lastmods[origin + "/pixi-wiki/"] is None
    # Chrome pages present.
    assert origin + "/pixi-wiki/updates.html" in locs
    # The recent.html redirect stub stays out of the sitemap.
    assert origin + "/pixi-wiki/recent.html" not in locs
    assert origin + "/pixi-wiki/docs/AGENT_SETUP.html" in locs
    assert origin + "/pixi-wiki/docs/REPLICATE_APPROACH.html" in locs
    assert origin + "/pixi-wiki/docs/SIGNAL_GRAPH.html" in locs

    # Every fixture document page (README + each concept) appears.
    doc_rels = [
        "README.md",
        "wiki/concepts/plain-concept.md",
        "wiki/concepts/escaped-concept.md",
        "wiki/concepts/long-concept.md",
        "wiki/concepts/undated-concept.md",
    ]
    for rel in doc_rels:
        assert origin + f"/pixi-wiki/wiki/seo-ns/{rel}.html" in locs

    # lastmod only for strict-ISO dated docs.
    assert lastmods[origin + "/pixi-wiki/wiki/seo-ns/wiki/concepts/plain-concept.md.html"] == "2026-01-03"
    assert lastmods[origin + "/pixi-wiki/wiki/seo-ns/README.md.html"] == "2026-01-02"
    assert lastmods[origin + "/pixi-wiki/wiki/seo-ns/wiki/concepts/undated-concept.md.html"] is None

    # Deterministic ordering: homepage first, then sorted by path.
    assert locs == [locs[0]] + sorted(locs[1:])


# ---------------------------------------------------------------------------
# 404.html
# ---------------------------------------------------------------------------

def test_404_page_has_chrome_and_navigation(tmp_path: Path) -> None:
    _generator, output = build_site(tmp_path)
    path = output / "404.html"
    assert path.exists()
    html_text = path.read_text(encoding="utf-8")
    assert "<h1>Page not found</h1>" in html_text
    assert "rebuilt" in html_text
    assert 'href="/pixi-wiki/"' in html_text
    assert 'href="/pixi-wiki/#wikis"' in html_text
    assert "/pixi-wiki/llms.txt" in html_text
    # Shared chrome: header nav + theme toggle.
    assert 'data-theme-toggle' in html_text
    assert '<footer class="footer">' in html_text
