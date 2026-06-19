#!/usr/bin/env python3
"""Clean rebuild contract tests for the generated pixi-wiki repo."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CleanRootContractTest(unittest.TestCase):
    def test_only_registry_html_lives_at_root(self) -> None:
        root_html = sorted(path.name for path in ROOT.glob("*.html"))
        self.assertEqual(root_html, ["index.html"])

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
                "ai-native-product-surfaces",
                "rl-sim-labs",
                "curated-tuning-datasets",
                "local-ai-infrastructure",
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

    def test_namespace_pages_have_agentwikis_sidebar_and_readme_card(self) -> None:
        html = (ROOT / "wiki" / "agent-workflows" / "README.md.html").read_text(encoding="utf-8")
        self.assertIn("Agent Workflows Knowledge Base", html)
        self.assertIn("15 documents", html)
        self.assertIn("📄 Agent Workflows Knowledge Base", html)
        self.assertIn("📄 Agent Workflows KB — Master Index", html)
        self.assertIn("<summary>WIKI 1</summary>", html)
        self.assertIn("📄 Agent Workflows — Activity Log", html)
        self.assertIn("<summary>CONCEPTS 8</summary>", html)
        self.assertIn("📄 Knowledge Pack Routing", html)
        self.assertIn("📄 Ponytail Minimal Code Discipline", html)
        self.assertIn("<summary>ENTITIES 1</summary>", html)
        self.assertIn("<summary>SYNTHESES 2</summary>", html)
        self.assertIn("<summary>// FOR AGENTS</summary>", html)
        self.assertIn("/wiki/agent-workflows/llms.txt", html)
        self.assertIn("Covers", html)
        self.assertIn("Not Covered", html)
        self.assertIn("Current As Of", html)
        self.assertIn("view as markdown", html)
        self.assertIn("report a mistake", html)
        self.assertIn("prev-next-card", html)

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
        for path in [ROOT / "index.html", ROOT / "wiki" / "agent-workflows" / "README.md.html", ROOT / "docs" / "AGENT_SETUP.html", ROOT / "docs" / "REPLICATE_APPROACH.html"]:
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn('data-theme="light"', html)
                self.assertIn('data-theme-toggle', html)
                self.assertIn('>☾</button>', html)
                self.assertIn('[data-theme=dark]', html)
                self.assertIn('--bg:#111827', html)
                self.assertIn('--text:#d1d5db', html)
                self.assertIn('localStorage.getItem', html)

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


if __name__ == "__main__":
    unittest.main()
