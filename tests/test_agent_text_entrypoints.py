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

    def test_agent_callouts_link_to_local_llms_and_markdown_provenance(self) -> None:
        data = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
        for concept in data["concepts"]:
            html = (ROOT / concept["html_path"]).read_text(encoding="utf-8")
            with self.subTest(concept=concept["title"]):
                agent_callout = re.search(r'<section class="agent-callout">.*?</section>', html, re.S)
                self.assertIsNotNone(agent_callout)
                assert agent_callout is not None
                callout_html = agent_callout.group(0)
                self.assertIn(f'href="{concept["local_llms_txt_path"]}"', callout_html)
                self.assertIn(f'href="{concept["raw_source_path"]}"', callout_html)
                self.assertIn("local llms.txt", callout_html)
                self.assertIn("view as markdown", callout_html)
                self.assertNotIn("Agent alias", callout_html)
                self.assertNotIn("Agent text", callout_html)
                self.assertNotIn("Markdown source", callout_html)

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
