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
        self.assertNotIn("Knowledge domain llms.txt", llms)
        self.assertNotIn("concept-knowledge-concepts", llms)


if __name__ == "__main__":
    unittest.main()
