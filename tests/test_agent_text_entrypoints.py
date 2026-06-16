#!/usr/bin/env python3
"""Agent-facing text entrypoint tests for the clean namespace registry."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AgentTextEntrypointsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))

    def test_root_agent_entrypoints_exist(self) -> None:
        for name in ["llms.txt", "llms-full.txt", "index.json"]:
            with self.subTest(file=name):
                self.assertTrue((ROOT / name).exists())

    def test_llms_txt_is_the_compact_namespace_map(self) -> None:
        text = (ROOT / "llms.txt").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Pixi Wiki Namespace Registry"))
        for wiki in self.data["wikis"]:
            with self.subTest(namespace=wiki["slug"]):
                self.assertIn(f"## {wiki['title']}", text)
                self.assertIn(f"/raw/{wiki['slug']}/README.md", text)
                self.assertIn(f"/wiki/{wiki['slug']}/README.md.html", text)

    def test_llms_full_contains_concatenated_namespace_corpus(self) -> None:
        text = (ROOT / "llms-full.txt").read_text(encoding="utf-8")
        self.assertIn("<!-- ===== pixi-vault/README.md ===== -->", text)
        self.assertIn("<!-- ===== agent-workflows/README.md ===== -->", text)
        self.assertIn("Wiki Compiler", text)

    def test_index_json_document_records_resolve_to_files(self) -> None:
        for wiki in self.data["wikis"]:
            for doc in wiki["documents"]:
                with self.subTest(namespace=wiki["slug"], path=doc["path"]):
                    self.assertTrue((ROOT / doc["raw"].lstrip("/")).is_file())
                    self.assertTrue((ROOT / doc["html"].lstrip("/")).is_file())

    def test_no_clean_agent_alias_layer_remains(self) -> None:
        self.assertFalse((ROOT / "agent").exists())


if __name__ == "__main__":
    unittest.main()
