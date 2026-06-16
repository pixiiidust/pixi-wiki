#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AgentTextEntrypointsTest(unittest.TestCase):
    def test_concepts_have_txt_mirrors_and_registry_paths(self) -> None:
        data = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
        for concept in data["concepts"]:
            with self.subTest(concept=concept["title"]):
                raw_text_path = concept.get("raw_text_path")
                self.assertIsNotNone(raw_text_path)
                self.assertTrue(raw_text_path.endswith(".txt"), raw_text_path)
                self.assertTrue((ROOT / raw_text_path).exists(), raw_text_path)
                self.assertEqual(
                    (ROOT / raw_text_path).read_text(encoding="utf-8"),
                    (ROOT / "raw" / concept["source_path"]).read_text(encoding="utf-8"),
                )

    def test_canonical_concept_pages_link_to_local_llms_and_markdown_provenance(self) -> None:
        data = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
        for concept in data["concepts"]:
            html_path = concept["human_html_path"]
            html = (ROOT / html_path).read_text(encoding="utf-8")
            with self.subTest(concept=concept["title"]):
                self.assertEqual(concept["html_path"], html_path)
                self.assertTrue(html_path.startswith("wiki/knowledge/concepts/"))
                self.assertIn('href="llms.txt"', html)
                self.assertIn("local llms.txt", html)
                self.assertIn("view as markdown", html)
                self.assertIn("raw/" + concept["source_path"], html)
                self.assertNotIn("Agent alias", html)
                self.assertNotIn("Agent text", html)
                self.assertNotIn("Markdown source", html)

    def test_root_flat_concept_pages_are_compatibility_shims(self) -> None:
        data = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
        for concept in data["concepts"]:
            legacy_path = concept["legacy_html_path"]
            html = (ROOT / legacy_path).read_text(encoding="utf-8")
            with self.subTest(concept=concept["title"]):
                self.assertIn("compatibility-shim", html)
                self.assertIn('rel="canonical"', html)
                self.assertIn(concept["human_url"], html)
                self.assertIn("root-level page is retained only so old links keep working", html)

    def test_agent_layer_files_exist(self) -> None:
        for name in ["llms.txt", "llms-full.txt", "index.json"]:
            with self.subTest(file=name):
                self.assertTrue((ROOT / "agent" / name).exists())

    def test_agent_index_exposes_clean_entrypoints(self) -> None:
        data = json.loads((ROOT / "agent" / "index.json").read_text(encoding="utf-8"))
        entrypoints = data["entrypoints"]
        self.assertEqual(entrypoints["agent_llms_txt"], "agent/llms.txt")
        self.assertEqual(entrypoints["agent_json_index"], "agent/index.json")
        self.assertEqual(entrypoints["agent_concepts_base"], "agent/concepts/")
        self.assertEqual(entrypoints["agent_packs_base"], "agent/packs/")
        for concept in data["concepts"]:
            with self.subTest(concept=concept["title"]):
                self.assertIn("agent_text_path", concept)
                self.assertIn("raw_source_path", concept)
                self.assertTrue(concept["agent_text_path"].startswith("agent/concepts/"))
                self.assertTrue((ROOT / concept["agent_text_path"]).exists(), concept["agent_text_path"])
                self.assertEqual(
                    (ROOT / concept["agent_text_path"]).read_text(encoding="utf-8"),
                    (ROOT / concept["raw_text_path"]).read_text(encoding="utf-8"),
                )

    def test_agent_pack_aliases_exist(self) -> None:
        data = json.loads((ROOT / "agent" / "index.json").read_text(encoding="utf-8"))
        for pack in data["packs"]:
            with self.subTest(pack=pack["title"]):
                self.assertIn("agent_text_path", pack)
                self.assertIn("raw_source_path", pack)
                self.assertTrue(pack["agent_text_path"].startswith("agent/packs/"))
                self.assertTrue((ROOT / pack["agent_text_path"]).exists(), pack["agent_text_path"])

    def test_root_compatibility_files_still_exist(self) -> None:
        for name in ["llms.txt", "llms-full.txt", "index.json", "index.html"]:
            with self.subTest(file=name):
                self.assertTrue((ROOT / name).exists())

    def test_llms_txt_entries_use_clickable_wiki_and_raw_links(self) -> None:
        for name in ["llms.txt", "llms-full.txt"]:
            with self.subTest(file=name):
                text = (ROOT / name).read_text(encoding="utf-8")
                self.assertNotRegex(text, r"raw: `[^`]+`")
                self.assertIn("[Knowledge domain llms.txt](/pixi-wiki/wiki/knowledge/llms.txt)", text)
                self.assertIn("[Agent Wikis](/pixi-wiki/wiki/knowledge/concepts/agent-wikis/)", text)
                self.assertIn("[markdown](/pixi-wiki/raw/Knowledge/concepts/agent-wikis.md)", text)
        root_text = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("[source](/pixi-wiki/raw/llms.txt)", root_text)


if __name__ == "__main__":
    unittest.main()
