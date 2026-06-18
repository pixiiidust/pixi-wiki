#!/usr/bin/env python3
"""Tests for the read-only Pixi Wiki MCP access layer."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.pixi_wiki_mcp import PixiWikiError, PixiWikiStore


class PixiWikiMcpStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.store = PixiWikiStore()

    def test_list_kbs_returns_registered_namespaces(self) -> None:
        payload = self.store.list_kbs()
        kb_ids = {kb["kb_id"] for kb in payload["kbs"]}
        self.assertEqual(payload["schema_version"], "pixi-agentwikis-registry-v1")
        self.assertIn("pixi-vault", kb_ids)
        self.assertIn("agent-workflows", kb_ids)
        self.assertGreater(payload["kb_count"], 0)

    def test_list_documents_returns_stable_document_ids(self) -> None:
        payload = self.store.list_documents("pixi-vault")
        doc_ids = {doc["document_id"] for doc in payload["documents"]}
        self.assertIn("README.md", doc_ids)
        self.assertIn("wiki/index.md", doc_ids)
        self.assertEqual(payload["kb_id"], "pixi-vault")

    def test_read_document_returns_markdown_and_metadata(self) -> None:
        payload = self.store.read_document("pixi-vault", "README.md")
        self.assertEqual(payload["kb_id"], "pixi-vault")
        self.assertEqual(payload["document_id"], "README.md")
        self.assertIn("# Pixi Vault", payload["content"])
        self.assertIn("last_modified", payload)
        self.assertEqual(payload["raw"], "/raw/pixi-vault/README.md")

    def test_get_kb_summary_includes_readme(self) -> None:
        payload = self.store.get_kb_summary("pixi-vault")
        self.assertEqual(payload["kb_id"], "pixi-vault")
        self.assertIn("description", payload)
        self.assertIsNotNone(payload["summary_document"])
        self.assertIn("content", payload["summary_document"])

    def test_search_kb_returns_snippets(self) -> None:
        payload = self.store.search_kb("agent-workflows", "Ponytail", max_results=5)
        self.assertEqual(payload["kb_id"], "agent-workflows")
        self.assertGreater(payload["result_count"], 0)
        self.assertIn("snippet", payload["results"][0])
        self.assertIn("document_id", payload["results"][0])

    def test_search_all_kbs_returns_cross_namespace_results(self) -> None:
        payload = self.store.search_all_kbs("Pixi Wiki", max_results=10)
        self.assertGreater(payload["result_count"], 0)
        kb_ids = {result["kb_id"] for result in payload["results"]}
        self.assertIn("pixi-vault", kb_ids)

    def test_missing_kb_fails_gracefully(self) -> None:
        with self.assertRaises(PixiWikiError) as ctx:
            self.store.list_documents("nope")
        self.assertEqual(ctx.exception.code, "KB_NOT_FOUND")
        self.assertIn("Available KBs", ctx.exception.message)

    def test_missing_document_fails_gracefully(self) -> None:
        with self.assertRaises(PixiWikiError) as ctx:
            self.store.read_document("pixi-vault", "missing.md")
        self.assertEqual(ctx.exception.code, "DOCUMENT_NOT_FOUND")

    def test_document_path_traversal_is_rejected(self) -> None:
        with self.assertRaises(PixiWikiError) as ctx:
            self.store.read_document("pixi-vault", "../README.md")
        self.assertEqual(ctx.exception.code, "INVALID_DOCUMENT_ID")

    def test_empty_search_query_is_rejected(self) -> None:
        with self.assertRaises(PixiWikiError) as ctx:
            self.store.search_all_kbs("   ")
        self.assertEqual(ctx.exception.code, "EMPTY_QUERY")


if __name__ == "__main__":
    unittest.main()
