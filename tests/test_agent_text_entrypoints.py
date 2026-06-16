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

    def test_agent_callouts_link_to_txt_not_markdown_source_span(self) -> None:
        data = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
        for concept in data["concepts"]:
            html = (ROOT / concept["html_path"]).read_text(encoding="utf-8")
            with self.subTest(concept=concept["title"]):
                self.assertIn(f'href="{concept["raw_text_path"]}"', html)
                agent_callout = re.search(r'<section class="agent-callout">.*?</section>', html, re.S)
                self.assertIsNotNone(agent_callout)
                assert agent_callout is not None
                callout_html = agent_callout.group(0)
                self.assertNotIn("Markdown source:", callout_html)
                self.assertIn("Agent text", callout_html)

    def test_llms_txt_raw_entries_are_clickable_txt_links(self) -> None:
        for name in ["llms.txt", "llms-full.txt"]:
            with self.subTest(file=name):
                text = (ROOT / name).read_text(encoding="utf-8")
                self.assertNotRegex(text, r"raw: `[^`]+`")
                self.assertIn("[raw txt](/pixi-wiki/raw/Knowledge/concepts/ai-native-problem-framing-framework.txt)", text)
        root_text = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertIn("[root raw llms.txt](/pixi-wiki/raw/llms.txt)", root_text)


if __name__ == "__main__":
    unittest.main()
