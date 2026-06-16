#!/usr/bin/env python3
"""Route-contract tests for the compiled wiki layout (Issue #8).

These tests assert the DESIRED route contract from the PRD, not the current
flat model.  Most future-contract tests are marked @unittest.expectedFailure so they
record the RED contract without breaking main before the generator is refactored.

Requirements (from PRD §Testing Decisions):
  - Root compatibility files remain present.
  - Domain routes exist for Knowledge, Projects, and Maps of Content.
  - At least one concept bundle exposes both human route and local llms.txt route.
  - At least one project bundle exposes both human route and local llms.txt route.
  - MOC index route exists and exposes a map/traversal role.
  - Concept pages do NOT expose Agent alias, Agent text, and Markdown source
    as parallel primary CTAs.
  - index.json records include human URL, agent llms.txt, raw source, source
    path, type, and domain fields.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
HTML_BASE = "/pixi-wiki/"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _load_index_json() -> dict:
    return json.loads((ROOT / "index.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Root compatibility  (should PASS — these files already exist)
# ---------------------------------------------------------------------------

class RootCompatibilityTest(unittest.TestCase):
    """Assert root-level compatibility files remain present."""

    def test_root_compatibility_files_exist(self) -> None:
        """Root files: llms.txt, llms-full.txt, index.json, index.html."""
        for name in ["llms.txt", "llms-full.txt", "index.json", "index.html"]:
            with self.subTest(file=name):
                self.assertTrue((ROOT / name).exists(), f"Missing root file: {name}")

    def test_old_concept_html_pages_are_compatibility_shims(self) -> None:
        """Legacy flat concept HTML pages remain as tiny compatibility shims."""
        data = _load_index_json()
        for concept in data.get("concepts", []):
            legacy_path = concept.get("legacy_html_path", "")
            with self.subTest(html=legacy_path):
                self.assertTrue((ROOT / legacy_path).exists(), f"Missing: {legacy_path}")
                html = (ROOT / legacy_path).read_text(encoding="utf-8")
                self.assertIn("compatibility-shim", html)
                self.assertIn(concept.get("human_url", "NOPE"), html)

    def test_no_full_concept_or_project_pages_live_at_root(self) -> None:
        """Root flat pages are allowed only as compatibility shims, never full canonical pages."""
        for html_file in ROOT.glob("*.html"):
            if html_file.name == "index.html":
                continue
            html = html_file.read_text(encoding="utf-8")
            with self.subTest(page=html_file.name):
                self.assertIn("compatibility-shim", html)
                self.assertIn('rel="canonical"', html)

    def test_raw_mirrors_exist(self) -> None:
        """raw/ directory and its contents are present."""
        raw_dir = ROOT / "raw"
        self.assertTrue(raw_dir.is_dir(), "raw/ directory missing")
        # Spot-check a few known raw files
        expected = [
            "raw/llms.txt",
            "raw/Knowledge/llms.txt",
            "raw/Maps of Content/llms.txt",
            "raw/Knowledge/concepts/agent-wikis.md",
            "raw/Knowledge/concepts/agent-wikis.txt",
        ]
        for path in expected:
            with self.subTest(raw=path):
                self.assertTrue((ROOT / path).exists(), f"Missing: {path}")


# ---------------------------------------------------------------------------
# Domain routes  (should PASS — /wiki/... now exists)
# ---------------------------------------------------------------------------

class DomainRoutesTest(unittest.TestCase):
    """Assert new /wiki/ domain routes exist."""

    def test_knowledge_domain_route_exists(self) -> None:
        """Knowledge domain has a /wiki/knowledge/ route."""
        path = ROOT / "wiki" / "knowledge"
        self.assertTrue(path.is_dir(), f"Expected directory: {path}")

    def test_projects_domain_route_exists(self) -> None:
        """Projects domain has a /wiki/projects/ route."""
        path = ROOT / "wiki" / "projects"
        self.assertTrue(path.is_dir(), f"Expected directory: {path}")

    def test_maps_of_content_domain_route_exists(self) -> None:
        """Maps of Content domain has a /wiki/maps-of-content/ route."""
        path = ROOT / "wiki" / "maps-of-content"
        self.assertTrue(path.is_dir(), f"Expected directory: {path}")

    def test_knowledge_domain_llms_txt_exists(self) -> None:
        """Knowledge domain has a local llms.txt."""
        path = ROOT / "wiki" / "knowledge" / "llms.txt"
        self.assertTrue(path.is_file(), f"Expected file: {path}")

    def test_projects_domain_llms_txt_exists(self) -> None:
        """Projects domain has a local llms.txt."""
        path = ROOT / "wiki" / "projects" / "llms.txt"
        self.assertTrue(path.is_file(), f"Expected file: {path}")

    def test_maps_of_content_domain_llms_txt_exists(self) -> None:
        """Maps of Content domain has a local llms.txt."""
        path = ROOT / "wiki" / "maps-of-content" / "llms.txt"
        self.assertTrue(path.is_file(), f"Expected file: {path}")


# ---------------------------------------------------------------------------
# Concept bundles  (should PASS — /wiki/knowledge/concepts/... now exists)
# ---------------------------------------------------------------------------

class ConceptBundleTest(unittest.TestCase):
    """Assert at least one concept exposes both human route and local llms.txt."""

    def test_concept_human_route_exists(self) -> None:
        """At least one concept has a /wiki/knowledge/concepts/<slug>/ index."""
        data = _load_index_json()
        concepts = data.get("concepts", [])
        self.assertGreater(len(concepts), 0, "No concepts in index.json")
        found = False
        for concept in concepts:
            slug = concept.get("slug", "")
            # Derive wiki-style slug from source path
            # e.g. "Knowledge/concepts/agent-wikis.md" → "agent-wikis"
            source = concept.get("source_path", "")
            parts = source.replace("\\", "/").split("/")
            if len(parts) >= 3 and parts[-1].endswith(".md"):
                concept_slug = parts[-1][:-3]
                human_dir = ROOT / "wiki" / "knowledge" / "concepts" / concept_slug
                if human_dir.is_dir():
                    found = True
                    break
        self.assertTrue(found, "No concept has a /wiki/knowledge/concepts/<slug>/ directory")

    def test_concept_llms_txt_exists(self) -> None:
        """At least one concept has a local llms.txt beside its human route."""
        data = _load_index_json()
        concepts = data.get("concepts", [])
        self.assertGreater(len(concepts), 0, "No concepts in index.json")
        found = False
        for concept in concepts:
            source = concept.get("source_path", "")
            parts = source.replace("\\", "/").split("/")
            if len(parts) >= 3 and parts[-1].endswith(".md"):
                concept_slug = parts[-1][:-3]
                llms_path = ROOT / "wiki" / "knowledge" / "concepts" / concept_slug / "llms.txt"
                if llms_path.is_file():
                    found = True
                    break
        self.assertTrue(found, "No concept has a local llms.txt at /wiki/knowledge/concepts/<slug>/llms.txt")


# ---------------------------------------------------------------------------
# Project bundles  (should PASS — /wiki/projects/... now exists)
# ---------------------------------------------------------------------------

class ProjectBundleTest(unittest.TestCase):
    """Assert at least one project exposes both human route and local llms.txt."""

    def test_project_human_route_exists(self) -> None:
        """At least one project has a /wiki/projects/<slug>/ index."""
        data = _load_index_json()
        packs = data.get("packs", [])
        project_packs = [p for p in packs if p.get("slug", "").startswith("projects-")]
        self.assertGreater(len(project_packs), 0, "No project packs in index.json")
        found = False
        for pack in project_packs:
            slug = pack.get("slug", "")
            # e.g. "projects-hermes-mission-control" → "hermes-mission-control"
            project_slug = slug.replace("projects-", "", 1)
            human_dir = ROOT / "wiki" / "projects" / project_slug
            if human_dir.is_dir():
                found = True
                break
        self.assertTrue(found, "No project has a /wiki/projects/<slug>/ directory")

    def test_project_llms_txt_exists(self) -> None:
        """At least one project has a local llms.txt beside its human route."""
        data = _load_index_json()
        packs = data.get("packs", [])
        project_packs = [p for p in packs if p.get("slug", "").startswith("projects-")]
        self.assertGreater(len(project_packs), 0, "No project packs in index.json")
        found = False
        for pack in project_packs:
            slug = pack.get("slug", "")
            project_slug = slug.replace("projects-", "", 1)
            llms_path = ROOT / "wiki" / "projects" / project_slug / "llms.txt"
            if llms_path.is_file():
                found = True
                break
        self.assertTrue(found, "No project has a local llms.txt at /wiki/projects/<slug>/llms.txt")


# ---------------------------------------------------------------------------
# Local llms.txt substance
# ---------------------------------------------------------------------------

class LocalLlmsSubstanceTest(unittest.TestCase):
    """Adjacent /wiki/**/llms.txt files are agent contracts, not stubs."""

    def test_all_wiki_llms_txt_files_are_substantive(self) -> None:
        files = sorted((ROOT / "wiki").rglob("llms.txt"))
        self.assertGreater(len(files), 0, "No /wiki/**/llms.txt files found")
        for path in files:
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertGreaterEqual(path.stat().st_size, 500)
                self.assertIn("---", text[:10], "local llms.txt should contain source frontmatter")

    def test_manifest_local_llms_match_raw_source_for_representative_nodes(self) -> None:
        data = _load_index_json()
        wanted = {
            "Knowledge/concepts/agent-wikis.md",
            "Knowledge/concepts/context-overfitting.md",
            "Knowledge/llms.txt",
            "Maps of Content/llms.txt",
            "Projects/Eval Trace/llms.txt",
        }
        docs = [doc for doc in data.get("documents", []) if doc.get("source_path") in wanted]
        self.assertEqual({doc.get("source_path") for doc in docs}, wanted)
        for doc in docs:
            with self.subTest(source=doc["source_path"]):
                local_path = ROOT / doc["local_llms_txt_path"]
                raw_path = ROOT / doc["raw_source_path"]
                self.assertTrue(local_path.exists(), local_path)
                self.assertTrue(raw_path.exists(), raw_path)
                self.assertEqual(local_path.read_text(encoding="utf-8"), raw_path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# MOC index route  (should PASS — /wiki/maps-of-content/ now exists)
# ---------------------------------------------------------------------------

class MOCIndexRouteTest(unittest.TestCase):
    """Assert MOC index route exists and exposes a map/traversal role."""

    def test_moc_index_route_exists(self) -> None:
        """Maps of Content has a /wiki/maps-of-content/ index."""
        path = ROOT / "wiki" / "maps-of-content" / "index.html"
        self.assertTrue(path.is_file(), f"Expected MOC index: {path}")

    def test_moc_index_mentions_map_role(self) -> None:
        """MOC index page mentions map, traversal, or navigation role."""
        path = ROOT / "wiki" / "maps-of-content" / "index.html"
        self.assertTrue(path.is_file(), "MOC index does not exist yet")
        html = path.read_text(encoding="utf-8")
        # The page should describe itself as a map room / navigation cortex
        map_keywords = ["map", "traversal", "navigation", "cortex", "route"]
        found_keyword = any(kw in html.lower() for kw in map_keywords)
        self.assertTrue(found_keyword, "MOC index does not mention map/traversal role")


class WikiRouteLinkTest(unittest.TestCase):
    """Assert generated /wiki/ HTML links resolve within the static output."""

    def test_wiki_concept_page_exposes_clean_agent_and_provenance_links(self) -> None:
        page = ROOT / "wiki" / "knowledge" / "concepts" / "agent-wikis" / "index.html"
        html = page.read_text(encoding="utf-8")
        self.assertIn('href="llms.txt"', html)
        self.assertIn("local llms.txt", html)
        self.assertIn("view as markdown", html)
        self.assertIn('href="../../../../raw/Knowledge/concepts/agent-wikis.md"', html)
        self.assertNotIn("Agent alias", html)
        self.assertNotIn("Agent text", html)
        self.assertNotIn("Markdown source", html)

    def test_wiki_html_internal_links_resolve(self) -> None:
        wiki_dir = ROOT / "wiki"
        self.assertTrue(wiki_dir.is_dir(), "wiki/ directory missing")
        for html_file in sorted(wiki_dir.rglob("*.html")):
            html = html_file.read_text(encoding="utf-8")
            for href in re.findall(r'href="([^"]+)"', html):
                if href.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                target = (html_file.parent / unquote(href)).resolve()
                if href.endswith("/"):
                    target = target / "index.html"
                with self.subTest(page=html_file.relative_to(ROOT), href=href):
                    self.assertTrue(
                        target.exists(),
                        f"Broken wiki link from {html_file.relative_to(ROOT)}: {href} -> {target}",
                    )


# ---------------------------------------------------------------------------
# Concept page CTA hygiene  (should FAIL — current pages expose all three)
# ---------------------------------------------------------------------------

class ConceptPageCTATest(unittest.TestCase):
    """Assert concept pages do NOT expose Agent alias, Agent text, and
    Markdown source as parallel primary CTAs."""

    def test_concept_pages_do_not_expose_flat_cta_trio(self) -> None:
        """No concept page has Agent alias, Agent text, AND Markdown source
        as parallel links in the agent-callout section."""
        data = _load_index_json()
        for concept in data.get("concepts", []):
            html_path = concept.get("html_path", "")
            if not html_path:
                continue
            html_file = ROOT / html_path
            if not html_file.exists():
                continue
            html = html_file.read_text(encoding="utf-8")
            with self.subTest(concept=concept.get("title", "unknown"), html=html_path):
                # Extract the agent-callout section
                m = re.search(
                    r'<section class="agent-callout">.*?</section>',
                    html,
                    re.DOTALL,
                )
                if m is None:
                    # No callout section at all — that's also a contract concern
                    # but not what this test targets; skip
                    continue
                callout = m.group(0)
                has_alias = "Agent alias" in callout
                has_agent_text = "Agent text" in callout
                has_md_source = "Markdown source" in callout
                # The contract says these should NOT appear as parallel primary CTAs
                self.assertFalse(
                    has_alias and has_agent_text and has_md_source,
                    f"Page {html_path} exposes Agent alias, Agent text, "
                    f"and Markdown source as parallel CTAs",
                )


# ---------------------------------------------------------------------------
# index.json schema  (should FAIL — current index.json uses old field names)
# ---------------------------------------------------------------------------

class IndexJsonSchemaTest(unittest.TestCase):
    """Assert index.json document records include the new contract fields."""

    def test_document_records_have_required_fields(self) -> None:
        """Each document in index.json has: human_url, agent_llms_txt,
        raw_source, source_path, type, domain."""
        data = _load_index_json()
        documents = data.get("documents", [])
        self.assertGreater(len(documents), 0, "No documents in index.json")
        required_fields = {"human_url", "agent_llms_txt", "raw_source",
                           "source_path", "type", "domain"}
        for doc in documents:
            title = doc.get("title", "untitled")
            with self.subTest(doc=title):
                missing = required_fields - set(doc.keys())
                self.assertSetEqual(
                    missing,
                    set(),
                    f"Document '{title}' missing fields: {missing}",
                )

    def test_concept_records_have_required_fields(self) -> None:
        """Each concept record in index.json has: human_url, agent_llms_txt,
        raw_source, source_path, type, domain."""
        data = _load_index_json()
        concepts = data.get("concepts", [])
        self.assertGreater(len(concepts), 0, "No concepts in index.json")
        required_fields = {"human_url", "agent_llms_txt", "raw_source",
                           "source_path", "type", "domain"}
        for concept in concepts:
            title = concept.get("title", "untitled")
            with self.subTest(concept=title):
                missing = required_fields - set(concept.keys())
                self.assertSetEqual(
                    missing,
                    set(),
                    f"Concept '{title}' missing fields: {missing}",
                )


if __name__ == "__main__":
    unittest.main()