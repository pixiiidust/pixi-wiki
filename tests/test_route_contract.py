#!/usr/bin/env python3
"""Clean rebuild contract tests for the generated pixi-wiki repo."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CleanRootContractTest(unittest.TestCase):
    def test_only_registry_html_lives_at_root(self) -> None:
        # Allowed root HTML pages. updates.html (the reworked surface, #81),
        # recent.html (now a redirect stub), and search.html (the #85 client
        # search results page) join index.html and 404.html. Assert the present
        # set is a subset of the allowlist (and still includes index.html)
        # rather than an exact match.
        allowed = {"404.html", "index.html", "recent.html", "search.html", "updates.html"}
        root_html = {path.name for path in ROOT.glob("*.html")}
        self.assertTrue(root_html.issubset(allowed), root_html)
        self.assertIn("index.html", root_html)

    def test_legacy_flat_root_pages_are_absent(self) -> None:
        forbidden = [
            "concept-*.html",
            "projects-*.html",
            "knowledge.html",
            "projects.html",
            "maps-of-content.html",
            "root.html",
        ]
        for pattern in forbidden:
            with self.subTest(pattern=pattern):
                self.assertEqual(list(ROOT.glob(pattern)), [])

    def test_old_agent_and_legacy_layers_are_absent(self) -> None:
        for dirname in ["agent", "legacy"]:
            with self.subTest(dirname=dirname):
                self.assertFalse((ROOT / dirname).exists())

    def test_required_root_registry_files_exist(self) -> None:
        for name in ["index.html", "index.json", "llms.txt", "llms-full.txt", ".nojekyll", "README.md"]:
            with self.subTest(file=name):
                self.assertTrue((ROOT / name).exists(), name)

    def test_homepage_has_clean_agent_setup_navigation(self) -> None:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Agent Setup", html)
        self.assertIn("Connect agents via MCP", html)
        self.assertIn("Agents start here", html)
        self.assertIn("$ curl https://pixiiidust.github.io/pixi-wiki/llms.txt", html)
        self.assertIn("GitHub", html)
        self.assertIn('/pixi-wiki/docs/AGENT_SETUP.html', html)
        self.assertIn('/pixi-wiki/docs/REPLICATE_APPROACH.html', html)
        self.assertNotIn("View index.json", html)
        self.assertNotIn("Replicate this for your own knowledge base", html)
        self.assertNotIn("/Namespaces", html)


class NamespaceRegistryContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))

    def test_index_json_is_namespace_only(self) -> None:
        self.assertEqual(self.data["schema_version"], "pixi-agentwikis-registry-v1")
        self.assertEqual(self.data["legacy_root_flat_pages"], "removed")
        self.assertNotIn("concepts", self.data)
        self.assertNotIn("packs", self.data)
        self.assertNotIn("documents", self.data)

    def test_expected_namespaces_are_registered(self) -> None:
        slugs = {wiki["slug"] for wiki in self.data["wikis"]}
        self.assertEqual(
            slugs,
            {
                "pixi-vault",
                "agent-workflows",
                "eval-trace",
                "hermes-agent",
                "ai-native-product-surfaces",
                "content-distribution",
                "rl-sim-labs",
                "curated-tuning-datasets",
                "local-ai-infrastructure",
                "pattern-language",
                "software-architecture-metapatterns",
                "ui-patterns",
            },
        )

    def test_each_registered_namespace_has_raw_and_html_documents(self) -> None:
        for wiki in self.data["wikis"]:
            with self.subTest(namespace=wiki["slug"]):
                self.assertGreater(wiki["documentCount"], 0)
                self.assertTrue((ROOT / "raw" / wiki["slug"] / "README.md").exists())
                self.assertTrue((ROOT / "wiki" / wiki["slug"] / "README.md.html").exists())
                for doc in wiki["documents"]:
                    self.assertTrue((ROOT / doc["raw"].lstrip("/")).exists(), doc)
                    self.assertTrue((ROOT / doc["html"].lstrip("/")).exists(), doc)

    def test_llms_entrypoints_reference_namespaces_not_legacy_layers(self) -> None:
        llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("# Pixi Wiki Namespace Registry", llms)
        self.assertIn("/raw/agent-workflows/README.md", llms)
        self.assertIn("/wiki/agent-workflows/README.md.html", llms)
        self.assertIn("/wiki/agent-workflows/llms.txt", llms)
        self.assertNotIn("Knowledge domain llms.txt", llms)
        self.assertNotIn("concept-knowledge-concepts", llms)

    def test_namespace_descriptions_preserve_complete_scope_text(self) -> None:
        registry = {wiki["slug"]: wiki for wiki in self.data["wikis"]}
        description = registry["agent-workflows"]["description"]
        self.assertIn(
            "verb-first instruction/knowledge design, and workflow reliability practices.",
            description,
        )

    def test_namespace_pages_have_agentwikis_sidebar_and_readme_card(self) -> None:
        html = (ROOT / "wiki" / "agent-workflows" / "README.md.html").read_text(encoding="utf-8")
        self.assertIn("Agent Workflows Knowledge Base", html)
        self.assertIn("33 documents", html)
        self.assertIn("📄 </span>Agent Workflows Knowledge Base", html)
        self.assertIn("📄 </span>Agent Workflows KB — Master Index", html)
        self.assertIn("<summary>WIKI 1</summary>", html)
        self.assertIn("📄 </span>Agent Workflows — Activity Log", html)
        self.assertIn("<summary>CONCEPTS 24</summary>", html)
        self.assertIn("📄 </span>Agent Capability Route Pattern", html)
        self.assertIn("📄 </span>Agent Tooling Plan", html)
        self.assertIn("📄 </span>Agentic Harness Engineering", html)
        self.assertIn("📄 </span>Effective State Load", html)
        self.assertIn("📄 </span>Reader-Centered Outreach Asks", html)
        self.assertIn("📄 </span>Compound Engineering Skill Layer", html)
        self.assertIn("📄 </span>Creative Ideation Routing", html)
        self.assertIn("📄 </span>Visual Plan Review Surfaces", html)
        self.assertIn("📄 </span>Bounded Context Tree Pattern", html)
        self.assertIn("📄 </span>Hermes SOUL.md Wiring", html)
        self.assertIn("📄 </span>High Agency Work Levels", html)
        self.assertIn("📄 </span>Knowledge Pack Routing", html)
        self.assertIn("📄 </span>Matt Pocock SDLC Rhythm", html)
        self.assertIn("📄 </span>Matt Pocock Skills Best Practices", html)
        self.assertIn("📄 </span>Multi-Agent Multiplayer Boundaries", html)
        self.assertIn("📄 </span>Ponytail Minimal Code Discipline", html)
        self.assertIn("📄 </span>Verb-First vs Noun-First: Actions Before Labels", html)
        self.assertIn("<summary>ENTITIES 1</summary>", html)
        self.assertIn("<summary>SUMMARIES 2</summary>", html)
        self.assertIn("📄 </span>Agent Workflow System Summary — Skills, Tools, Scheduling, Delegation", html)
        self.assertIn("📄 </span>Effective State Load Full Report", html)
        self.assertIn("<summary>SYNTHESES 2</summary>", html)
        self.assertIn("<summary>// FOR AGENTS</summary>", html)
        self.assertIn("/wiki/agent-workflows/llms.txt", html)
        self.assertIn("Covers", html)
        self.assertIn("Not Covered", html)
        self.assertIn("Current As Of", html)
        self.assertIn("view as markdown", html)
        self.assertIn("report a mistake", html)
        self.assertIn("prev-next-card", html)

    def test_verb_first_general_and_product_pages_are_reciprocally_linked(self) -> None:
        registry = {wiki["slug"]: wiki for wiki in self.data["wikis"]}
        workflow_paths = {doc["path"] for doc in registry["agent-workflows"]["documents"]}
        product_paths = {doc["path"] for doc in registry["ai-native-product-surfaces"]["documents"]}
        self.assertIn("wiki/concepts/verb-first-knowledge.md", workflow_paths)
        self.assertIn("wiki/concepts/verb-first-product-positioning.md", product_paths)

        general_html = (
            ROOT / "wiki" / "agent-workflows" / "wiki" / "concepts" / "verb-first-knowledge.md.html"
        ).read_text(encoding="utf-8")
        product_html = (
            ROOT
            / "wiki"
            / "ai-native-product-surfaces"
            / "wiki"
            / "concepts"
            / "verb-first-product-positioning.md.html"
        ).read_text(encoding="utf-8")
        self.assertIn(
            'href="/pixi-wiki/wiki/ai-native-product-surfaces/wiki/concepts/verb-first-product-positioning.md.html"',
            general_html,
        )
        self.assertIn(
            'href="/pixi-wiki/wiki/agent-workflows/wiki/concepts/verb-first-knowledge.md.html"',
            product_html,
        )

    def test_pattern_language_namespace_exposes_pattern_corpus_and_agent_guidance(self) -> None:
        registry = {wiki["slug"]: wiki for wiki in self.data["wikis"]}
        wiki = registry["pattern-language"]
        self.assertEqual(wiki["title"], "Pattern Language")
        self.assertGreaterEqual(wiki["documentCount"], 260)
        doc_paths = {doc["path"] for doc in wiki["documents"]}
        self.assertIn("wiki/summaries/for-agents-spatial-pattern-retrieval.md", doc_paths)
        self.assertIn("wiki/syntheses/unreal-mcp-worldbuilding-adapter-deferred.md", doc_paths)
        self.assertIn("wiki/concepts/patterns/activity-nodes-30.md", doc_paths)
        self.assertTrue((ROOT / "raw" / "pattern-language" / "wiki" / "concepts" / "patterns" / "activity-nodes-30.md").exists())
        html = (ROOT / "wiki" / "pattern-language" / "README.md.html").read_text(encoding="utf-8")
        self.assertIn("Non-commercial reuse with attribution", html)
        self.assertIn("For Agents", html)

    def test_pattern_language_search_text_includes_problem_solution_and_related_links(self) -> None:
        text = (ROOT / "raw" / "pattern-language" / "wiki" / "concepts" / "patterns" / "activity-nodes-30.md").read_text(encoding="utf-8")
        self.assertIn("### Problem", text)
        self.assertIn("### Solution", text)
        self.assertIn("### Related Patterns", text)
        self.assertIn("[[Promenade (31)]]", text)
        self.assertIn("source_repository: https://github.com/zenodotus280/apl-md", text)

    def test_software_architecture_metapatterns_namespace_exposes_corpus_and_guidance(self) -> None:
        registry = {wiki["slug"]: wiki for wiki in self.data["wikis"]}
        wiki = registry["software-architecture-metapatterns"]
        self.assertEqual(wiki["title"], "Software Architecture Metapatterns")
        self.assertEqual(wiki["category"], "knowledge-systems")
        self.assertGreaterEqual(wiki["documentCount"], 80)
        doc_paths = {doc["path"] for doc in wiki["documents"]}
        self.assertIn("wiki/summaries/for-agents-software-architecture-retrieval.md", doc_paths)
        self.assertIn("wiki/summaries/license-and-provenance.md", doc_paths)
        self.assertIn("wiki/syntheses/architecture-metapatterns-fit-for-pixi.md", doc_paths)
        self.assertIn("wiki/concepts/source/introduction/metapatterns.md", doc_paths)
        self.assertIn("wiki/concepts/source/basic-metapatterns/services.md", doc_paths)
        text = (ROOT / "raw" / "software-architecture-metapatterns" / "wiki" / "summaries" / "for-agents-software-architecture-retrieval.md").read_text(encoding="utf-8")
        self.assertIn("Retrieve 3–8 relevant pages", text)
        self.assertIn("source is attributed external reference material", text)
        html = (ROOT / "wiki" / "software-architecture-metapatterns" / "README.md.html").read_text(encoding="utf-8")
        self.assertIn("Knowledge Systems", html)
        self.assertIn("Creative Commons", html)

    def test_content_distribution_namespace_exposes_long_form_attention_guide(self) -> None:
        registry = {wiki["slug"]: wiki for wiki in self.data["wikis"]}
        wiki = registry["content-distribution"]
        self.assertEqual(wiki["title"], "Content Distribution Systems")
        self.assertEqual(wiki["category"], "knowledge-systems")
        self.assertEqual(wiki["documentCount"], 5)
        doc_paths = {doc["path"] for doc in wiki["documents"]}
        self.assertIn("wiki/syntheses/attention-architecture-for-long-form-content.md", doc_paths)

        raw = (ROOT / "raw" / "content-distribution" / "wiki" / "syntheses" / "attention-architecture-for-long-form-content.md").read_text(encoding="utf-8")
        self.assertIn("Virality is not a structure you can guarantee", raw)
        self.assertIn("### Long-form video", raw)
        self.assertIn("### Substack or blog essay", raw)
        self.assertIn("### X article or thread", raw)
        self.assertNotIn("namespace: ai-native-product-surfaces", raw)

        asset_root = ROOT / "wiki" / "content-distribution" / "assets" / "attention-architecture-for-long-form-content"
        for name in [
            "01-misconceptions-formula.png",
            "02-question-to-explanation.png",
            "03-a-plot-b-plot-timeline.png",
            "04-framework-summary.png",
        ]:
            with self.subTest(asset=name):
                self.assertTrue((asset_root / name).is_file())

        html = (ROOT / "wiki" / "content-distribution" / "wiki" / "syntheses" / "attention-architecture-for-long-form-content.md.html").read_text(encoding="utf-8")
        self.assertIn('<img src="/pixi-wiki/wiki/content-distribution/assets/attention-architecture-for-long-form-content/01-misconceptions-formula.png"', html)
        self.assertIn("Measure the gates separately", html)
        self.assertNotIn("/wiki/ai-native-product-surfaces/assets/misconception-first-explanation-loop/", html)

        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('<section class="wiki-group" id="knowledge-systems">', homepage)
        self.assertIn('<article class="card" id="content-distribution">', homepage)

        self.assertFalse((ROOT / "raw" / "ai-native-product-surfaces" / "wiki" / "concepts" / "misconception-first-explanation-loop.md").exists())
        self.assertFalse((ROOT / "wiki" / "ai-native-product-surfaces" / "wiki" / "concepts" / "misconception-first-explanation-loop.md.html").exists())

    def test_software_architecture_metapatterns_diagrams_are_local_assets(self) -> None:
        raw = (ROOT / "raw" / "software-architecture-metapatterns" / "wiki" / "concepts" / "source" / "basic-metapatterns" / "basic-metapatterns.md").read_text(encoding="utf-8")
        self.assertIn("![A diagram of Monolith, with explanations.](/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Monolith.png)", raw)
        self.assertNotIn("raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Contents/Monolith.png", raw)
        self.assertNotIn("<img", raw)
        self.assertTrue((ROOT / "wiki" / "software-architecture-metapatterns" / "assets" / "images" / "Contents" / "Monolith.png").is_file())
        html = (ROOT / "wiki" / "software-architecture-metapatterns" / "wiki" / "concepts" / "source" / "basic-metapatterns" / "basic-metapatterns.md.html").read_text(encoding="utf-8")
        self.assertIn('<img src="/pixi-wiki/wiki/software-architecture-metapatterns/assets/images/Contents/Monolith.png"', html)
        self.assertNotIn("&lt;img", html)
        self.assertNotIn("raw.githubusercontent.com/denyspoltorak/metapatterns/main/ArchitecturalMetapatterns/Contents/Monolith.png", html)

    def test_software_architecture_metapatterns_source_artifacts_are_removed(self) -> None:
        raw = (ROOT / "raw" / "software-architecture-metapatterns" / "wiki" / "concepts" / "source" / "appendices" / "evolutions-of-architectures.md").read_text(encoding="utf-8")
        self.assertIn("This appendix details dozens of evolutions", raw)
        self.assertNotIn("| \\<\\<", raw)
        self.assertNotIn("| --- | --- | --- |", raw)
        self.assertNotIn("together\\.", raw)
        self.assertNotIn("re\\-integrate", raw)
        html = (ROOT / "wiki" / "software-architecture-metapatterns" / "wiki" / "concepts" / "source" / "appendices" / "evolutions-of-architectures.md.html").read_text(encoding="utf-8")
        self.assertIn("This appendix details dozens of evolutions", html)
        self.assertNotIn("| \\&lt;\\&lt;", html)
        self.assertNotIn("| --- | --- | --- |", html)
        self.assertNotIn("together\\.", html)
        self.assertNotIn("re\\-integrate", html)

    def test_ui_patterns_namespace_exposes_catalog_and_guardrails(self) -> None:
        registry = {wiki["slug"]: wiki for wiki in self.data["wikis"]}
        wiki = registry["ui-patterns"]
        self.assertEqual(wiki["title"], "UI Patterns")
        self.assertEqual(wiki["category"], "product-design")
        self.assertGreaterEqual(wiki["documentCount"], 180)
        doc_paths = {doc["path"] for doc in wiki["documents"]}
        self.assertIn("wiki/summaries/for-agents-ui-patterns-retrieval.md", doc_paths)
        self.assertIn("wiki/summaries/provenance-and-copyright-boundary.md", doc_paths)
        self.assertIn("wiki/entities/source-site-ui-patterns.md", doc_paths)
        self.assertIn("wiki/concepts/patterns/good-defaults.md", doc_paths)
        self.assertIn("wiki/entities/categories/user-interface-design-patterns-getting-input.md", doc_paths)
        text = (ROOT / "raw" / "ui-patterns" / "wiki" / "concepts" / "patterns" / "good-defaults.md").read_text(encoding="utf-8")
        self.assertIn("Catalog pointer for the UI Patterns source page", text)
        self.assertIn("source_copyright_note", text)
        self.assertIn("Example screenshots detected at source: 8", text)
        self.assertNotIn("The user needs to enter data into the system", text)
        html = (ROOT / "wiki" / "ui-patterns" / "README.md.html").read_text(encoding="utf-8")
        self.assertIn("pattern catalog structure", html)
        self.assertIn("all rights reserved", html)
        self.assertIn("does not republish full source pattern bodies", html)

    def test_rendered_wiki_page_exposes_metadata_tools_and_prev_next(self) -> None:
        html = (ROOT / "wiki" / "agent-workflows" / "wiki" / "concepts" / "knowledge-pack-routing.md.html").read_text(encoding="utf-8")
        self.assertIn("type</span>: concept", html)
        self.assertIn("updated</span>:", html)
        self.assertIn("sources</span>:", html)
        self.assertIn("view as markdown", html)
        self.assertIn("report a mistake", html)
        self.assertIn("← Prev", html)
        self.assertIn("Next", html)

    def test_namespace_local_agent_files_exist(self) -> None:
        for slug in ["pixi-vault", "agent-workflows", "eval-trace"]:
            with self.subTest(slug=slug):
                self.assertTrue((ROOT / "wiki" / slug / "llms.txt").is_file())
                self.assertTrue((ROOT / "wiki" / slug / "llms-full.txt").is_file())
                self.assertTrue((ROOT / "wiki" / slug / "index.json").is_file())

    def test_light_theme_is_default_with_dark_toggle(self) -> None:
        # State-aware CSS assertion. The CSS tokens (dark-theme variables) moved
        # out of every page's inline <style> and into a shared /pixi-wiki/site.css
        # in #61. Page regeneration lands in #65, so the committed tree may still
        # inline the CSS today: if site.css exists the pages must <link> it and the
        # tokens live in that stylesheet; otherwise assert the legacy inline tokens.
        # The theme markup and boot script (data-theme, toggle, localStorage) stay
        # inline in every page in both worlds.
        import hashlib

        site_css = ROOT / "site.css"
        linked = site_css.exists()
        css_source = site_css.read_text(encoding="utf-8") if linked else None
        css_hash = hashlib.sha256(site_css.read_bytes()).hexdigest()[:8] if linked else None
        for path in [ROOT / "index.html", ROOT / "wiki" / "agent-workflows" / "README.md.html", ROOT / "docs" / "AGENT_SETUP.html", ROOT / "docs" / "REPLICATE_APPROACH.html"]:
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn('data-theme="light"', html)
                self.assertIn('data-theme-toggle', html)
                self.assertIn('>☾</button>', html)
                self.assertIn('localStorage.getItem', html)
                if linked:
                    self.assertIn(f'<link rel="stylesheet" href="/pixi-wiki/site.css?v={css_hash}">', html)
                    css = css_source
                else:
                    self.assertIn('<style>', html)
                    css = html
                self.assertIn('[data-theme=dark]', css)
                self.assertIn('--bg:#0d1117', css)
                self.assertIn('--panel:#161b22', css)
                self.assertIn('--text:#e6edf3', css)
                self.assertIn('--accent:#58a6ff', css)
                self.assertIn('--active-bg:#1f6feb33', css)
                self.assertNotIn('--accent:#f59e0b', css)
                self.assertNotIn('--accent2:#fbdc92', css)
                self.assertNotIn('--active-bg:#8b4356', css)

    def test_agent_setup_page_has_subagent_usage_contract(self) -> None:
        html = (ROOT / "docs" / "AGENT_SETUP.html").read_text(encoding="utf-8")
        self.assertIn("Subagents do not inherit your full context", html)
        self.assertIn("Recommended agent workflow", html)
        self.assertIn("Subagent instruction template", html)
        self.assertIn("mcp_pixi_wiki_", html)

    def test_replicate_approach_page_links_to_repo_and_contract(self) -> None:
        html = (ROOT / "docs" / "REPLICATE_APPROACH.html").read_text(encoding="utf-8")
        self.assertIn("Replicate the Approach", html)
        self.assertIn("your own Markdown notes", html)
        self.assertIn("The reusable contract", html)
        self.assertIn("https://github.com/pixiiidust/pixi-wiki", html)
        self.assertIn("local read-only MCP tools", html)


class HardenedSurfaceContractTest(unittest.TestCase):
    """Committed-artifact contracts for the PRD #51 hardening (regenerated in #65).

    These assert on the PUBLISHED tree, complementing the build-seam fixture
    tests that landed with each feature PR (#68-#78).
    """

    def test_renderer_fixes_are_live_on_previously_broken_pages(self) -> None:
        html = (ROOT / "wiki" / "agent-workflows" / "wiki" / "concepts" / "agent-tooling-plan.md.html").read_text(encoding="utf-8")
        self.assertIn('<div class="table-wrap"><table><thead>', html)
        self.assertIn("<th>Bucket</th>", html)
        self.assertNotIn("<p>| Bucket", html)
        self.assertIn("<strong>Agent Tooling Plan</strong>", html)
        pattern = (ROOT / "wiki" / "pattern-language" / "wiki" / "concepts" / "patterns" / "activity-nodes-30.md.html").read_text(encoding="utf-8")
        self.assertIn("<blockquote>", pattern)
        self.assertNotIn("&gt;Community facilities", pattern)

    def test_new_root_surfaces_exist_and_are_consistent(self) -> None:
        import xml.etree.ElementTree as ET

        # updates.html/.json are the reworked surface (#81); recent.html stays as
        # a redirect stub.
        for name in ["updates.html", "updates.json", "recent.html", "sitemap.xml", "404.html", "site.css"]:
            with self.subTest(file=name):
                self.assertTrue((ROOT / name).is_file(), name)
        updates = json.loads((ROOT / "updates.json").read_text(encoding="utf-8"))
        self.assertGreater(updates["count"], 0)
        registry = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
        known = {(w["slug"], d["path"]) for w in registry["wikis"] for d in w["documents"]}
        for entry in updates["entries"]:
            self.assertIn((entry["namespace"], entry["path"]), known)
        # The recent.html stub redirects to updates.html and stays out of the sitemap.
        stub = (ROOT / "recent.html").read_text(encoding="utf-8")
        self.assertIn('http-equiv="refresh"', stub)
        self.assertIn("/pixi-wiki/updates.html", stub)
        tree = ET.parse(ROOT / "sitemap.xml")
        locs = [el.text for el in tree.iter() if el.tag.endswith("loc")]
        self.assertIn("https://pixiiidust.github.io/pixi-wiki/", locs)
        self.assertIn("https://pixiiidust.github.io/pixi-wiki/updates.html", locs)
        self.assertNotIn("https://pixiiidust.github.io/pixi-wiki/recent.html", locs)
        self.assertGreater(len(locs), 600)

    def test_published_pages_carry_the_new_chrome(self) -> None:
        html = (ROOT / "wiki" / "agent-workflows" / "README.md.html").read_text(encoding="utf-8")
        self.assertIn('<meta name="description"', html)
        self.assertIn('<link rel="canonical" href="https://pixiiidust.github.io/pixi-wiki/wiki/agent-workflows/README.md.html">', html)
        # Stylesheet link carries the #81 content-hash cache-buster; the hash is
        # of the committed site.css (which the regenerated pages point at).
        import hashlib

        css_hash = hashlib.sha256((ROOT / "site.css").read_bytes()).hexdigest()[:8]
        self.assertIn(f'<link rel="stylesheet" href="/pixi-wiki/site.css?v={css_hash}">', html)
        self.assertIn('class="site-search" data-registry="/pixi-wiki/index.json"', html)
        self.assertIn('class="skip-link"', html)
        self.assertIn('id="main-content"', html)
        self.assertIn('aria-current="page"', html)
        self.assertIn('aria-label="Toggle color theme"', html)
        self.assertIn('<details class="nav-menu">', html)
        self.assertIn('href="/pixi-wiki/updates.html"', html)
        self.assertIn('<h2 id="', html)
        self.assertIn('class="heading-anchor"', html)

    def test_large_namespace_sidebar_is_grouped_and_filterable(self) -> None:
        html = (ROOT / "wiki" / "pattern-language" / "README.md.html").read_text(encoding="utf-8")
        self.assertIn('class="sidebar-subgroup"', html)
        self.assertIn('class="sidebar-filter"', html)


if __name__ == "__main__":
    unittest.main()
