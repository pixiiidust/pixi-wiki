#!/usr/bin/env python3
"""Read-only MCP server for Pixi Wiki Markdown knowledge bases.

The server reads the generated Pixi Wiki registry (`index.json`) and the raw
Markdown mirrors under `raw/<kb>/`. It intentionally exposes no write/delete
operations.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAX_RESULTS = 20
MAX_READ_BYTES = 1_000_000


class PixiWikiError(Exception):
    """Structured, agent-friendly Pixi Wiki error."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message

    def as_dict(self) -> dict[str, str]:
        return {"error": self.code, "message": self.message}


def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    end = markdown.find("\n---\n", 4)
    if end == -1:
        return {}, markdown
    raw = markdown[4:end]
    body = markdown[end + 5 :]
    data: dict[str, Any] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(line[4:].strip().strip('"\''))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            data[key] = []
            current_key = key
        elif value.startswith("[") and value.endswith("]"):
            data[key] = [part.strip().strip('"\'') for part in value[1:-1].split(",") if part.strip()]
            current_key = key
        else:
            data[key] = value.strip('"\'')
            current_key = key
    return data, body


def _first_heading(markdown: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", markdown, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def _first_paragraph(markdown: str) -> str:
    _frontmatter, body = _parse_frontmatter(markdown)
    lines: list[str] = []
    in_code = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped or stripped.startswith(("#", ">", "- ", "---")):
            if lines:
                break
            continue
        lines.append(stripped)
        if len(" ".join(lines)) >= 260:
            break
    return " ".join(lines)[:300]


def _safe_document_id(document_id: str) -> str:
    normalized = document_id.strip().lstrip("/")
    if not normalized or normalized in {".", ".."}:
        raise PixiWikiError("INVALID_DOCUMENT_ID", "Document id must be a non-empty relative Markdown path.")
    if "\\" in normalized:
        raise PixiWikiError("INVALID_DOCUMENT_ID", "Document id must use forward slashes, not backslashes.")
    parts = Path(normalized).parts
    if any(part in {"", ".", ".."} for part in parts):
        raise PixiWikiError("INVALID_DOCUMENT_ID", "Document id may not contain path traversal segments.")
    if not normalized.endswith(".md"):
        normalized = f"{normalized}.md"
    return normalized


def _mtime_iso(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


@dataclass(frozen=True)
class DocumentRef:
    kb_id: str
    document_id: str
    title: str
    category: str
    raw: str
    html: str | None = None


class PixiWikiStore:
    """Read-only access layer over generated Pixi Wiki Markdown files."""

    def __init__(self, root: Path = ROOT) -> None:
        self.root = root.resolve()
        self.index_path = self.root / "index.json"
        if not self.index_path.is_file():
            raise PixiWikiError("REGISTRY_NOT_FOUND", f"No Pixi Wiki registry found at {self.index_path}.")
        self._index_mtime_ns = 0
        self.registry: dict[str, Any] = {}
        self._kbs: dict[str, dict[str, Any]] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        self.registry = json.loads(self.index_path.read_text(encoding="utf-8"))
        self._kbs = {wiki["slug"]: wiki for wiki in self.registry.get("wikis", [])}
        self._index_mtime_ns = self.index_path.stat().st_mtime_ns

    def _refresh_if_changed(self) -> None:
        current_mtime_ns = self.index_path.stat().st_mtime_ns
        if current_mtime_ns != self._index_mtime_ns:
            self._load_registry()

    def list_kbs(self) -> dict[str, Any]:
        self._refresh_if_changed()
        kbs = []
        for wiki in self.registry.get("wikis", []):
            kbs.append(
                {
                    "kb_id": wiki.get("slug"),
                    "title": wiki.get("title"),
                    "description": wiki.get("description", ""),
                    "category": wiki.get("category"),
                    "tags": wiki.get("tags", []),
                    "document_count": wiki.get("documentCount", len(wiki.get("documents", []))),
                    "last_updated": wiki.get("lastUpdated"),
                    "raw_base": wiki.get("raw_base"),
                    "html_base": wiki.get("html_base"),
                    "llms_txt": wiki.get("llms_txt"),
                }
            )
        return {
            "name": self.registry.get("name", "Pixi Wiki"),
            "schema_version": self.registry.get("schema_version"),
            "kb_count": len(kbs),
            "kbs": kbs,
        }

    def _get_kb(self, kb_id: str) -> dict[str, Any]:
        self._refresh_if_changed()
        kb = self._kbs.get(kb_id)
        if not kb:
            available = ", ".join(sorted(self._kbs)) or "none"
            raise PixiWikiError("KB_NOT_FOUND", f"No KB found with id '{kb_id}'. Available KBs: {available}.")
        return kb

    def _document_refs(self, kb_id: str) -> list[DocumentRef]:
        kb = self._get_kb(kb_id)
        refs = []
        for doc in kb.get("documents", []):
            refs.append(
                DocumentRef(
                    kb_id=kb_id,
                    document_id=doc.get("path", ""),
                    title=doc.get("title") or doc.get("path", ""),
                    category=doc.get("category", "other"),
                    raw=doc.get("raw", ""),
                    html=doc.get("html"),
                )
            )
        return refs

    def list_documents(self, kb_id: str) -> dict[str, Any]:
        kb = self._get_kb(kb_id)
        documents = [
            {
                "kb_id": ref.kb_id,
                "document_id": ref.document_id,
                "title": ref.title,
                "category": ref.category,
                "raw": ref.raw,
                "html": ref.html,
            }
            for ref in self._document_refs(kb_id)
        ]
        return {
            "kb_id": kb_id,
            "title": kb.get("title"),
            "document_count": len(documents),
            "documents": documents,
        }

    def _resolve_document(self, kb_id: str, document_id: str) -> tuple[DocumentRef, Path]:
        self._get_kb(kb_id)
        safe_id = _safe_document_id(document_id)
        ref_by_id = {ref.document_id: ref for ref in self._document_refs(kb_id)}
        ref = ref_by_id.get(safe_id)
        if not ref:
            raise PixiWikiError(
                "DOCUMENT_NOT_FOUND",
                f"No document '{safe_id}' exists in KB '{kb_id}'. Use list_documents to see available documents.",
            )
        path = (self.root / ref.raw.lstrip("/")).resolve()
        raw_root = (self.root / "raw" / kb_id).resolve()
        if raw_root not in path.parents and path != raw_root:
            raise PixiWikiError("INVALID_DOCUMENT_PATH", "Resolved document path is outside the KB raw directory.")
        if not path.is_file():
            raise PixiWikiError("DOCUMENT_FILE_NOT_FOUND", f"Registry points to missing Markdown file: {ref.raw}.")
        return ref, path

    def read_document(self, kb_id: str, document_id: str) -> dict[str, Any]:
        ref, path = self._resolve_document(kb_id, document_id)
        if path.stat().st_size > MAX_READ_BYTES:
            raise PixiWikiError("DOCUMENT_TOO_LARGE", f"Document exceeds {MAX_READ_BYTES} bytes: {ref.document_id}.")
        content = path.read_text(encoding="utf-8")
        frontmatter, body = _parse_frontmatter(content)
        return {
            "kb_id": kb_id,
            "document_id": ref.document_id,
            "title": frontmatter.get("title") or _first_heading(body) or ref.title,
            "category": ref.category,
            "raw": ref.raw,
            "html": ref.html,
            "last_modified": _mtime_iso(path),
            "frontmatter": frontmatter,
            "content": content,
        }

    def get_kb_summary(self, kb_id: str) -> dict[str, Any]:
        kb = self._get_kb(kb_id)
        try:
            readme = self.read_document(kb_id, "README.md")
        except PixiWikiError as exc:
            if exc.code != "DOCUMENT_NOT_FOUND":
                raise
            readme = None
        return {
            "kb_id": kb_id,
            "title": kb.get("title"),
            "description": kb.get("description", ""),
            "scope": kb.get("scope", {}),
            "tags": kb.get("tags", []),
            "document_count": kb.get("documentCount", len(kb.get("documents", []))),
            "last_updated": kb.get("lastUpdated"),
            "summary_document": readme,
        }

    def search_kb(self, kb_id: str, query: str, max_results: int = DEFAULT_MAX_RESULTS) -> dict[str, Any]:
        self._get_kb(kb_id)
        results = self._search_refs(self._document_refs(kb_id), query, max_results)
        return {"query": query, "kb_id": kb_id, "result_count": len(results), "results": results}

    def search_all_kbs(self, query: str, max_results: int = DEFAULT_MAX_RESULTS) -> dict[str, Any]:
        refs: list[DocumentRef] = []
        for kb_id in self._kbs:
            refs.extend(self._document_refs(kb_id))
        results = self._search_refs(refs, query, max_results)
        return {"query": query, "result_count": len(results), "results": results}

    def _search_refs(self, refs: list[DocumentRef], query: str, max_results: int) -> list[dict[str, Any]]:
        cleaned = query.strip()
        if not cleaned:
            raise PixiWikiError("EMPTY_QUERY", "Search query must not be empty.")
        terms = [_slugify(term) for term in re.findall(r"[\w-]+", cleaned)]
        terms = [term for term in terms if term]
        if not terms:
            raise PixiWikiError("EMPTY_QUERY", "Search query must include searchable text.")
        max_results = max(1, min(int(max_results), 50))
        scored: list[tuple[int, dict[str, Any]]] = []
        for ref in refs:
            try:
                _resolved_ref, path = self._resolve_document(ref.kb_id, ref.document_id)
            except PixiWikiError:
                continue
            content = path.read_text(encoding="utf-8", errors="replace")
            haystack = _slugify(" ".join([ref.title, ref.document_id, content]))
            score = sum(haystack.count(term) for term in terms)
            if score <= 0:
                continue
            snippet = self._snippet(content, terms)
            scored.append(
                (
                    score,
                    {
                        "kb_id": ref.kb_id,
                        "document_id": ref.document_id,
                        "title": ref.title,
                        "category": ref.category,
                        "raw": ref.raw,
                        "html": ref.html,
                        "score": score,
                        "snippet": snippet,
                    },
                )
            )
        scored.sort(key=lambda item: (-item[0], item[1]["kb_id"], item[1]["document_id"]))
        return [item for _score, item in scored[:max_results]]

    @staticmethod
    def _snippet(content: str, terms: list[str]) -> str:
        lines = content.splitlines()
        for line in lines:
            normalized = _slugify(line)
            if any(term in normalized for term in terms):
                stripped = re.sub(r"\s+", " ", line).strip()
                return stripped[:260]
        paragraph = _first_paragraph(content)
        return paragraph[:260] if paragraph else "Match found in document metadata."


def _call_safely(method: str, **kwargs: Any) -> dict[str, Any]:
    try:
        store = PixiWikiStore(ROOT)
        return getattr(store, method)(**kwargs)
    except PixiWikiError as exc:
        return exc.as_dict()


def create_mcp_server(root: Path = ROOT):
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - exercised by CLI environments without MCP SDK
        raise SystemExit("The Python MCP SDK is required. Install it with: pip install mcp") from exc

    store = PixiWikiStore(root)
    mcp = FastMCP("pixi-wiki")

    @mcp.tool()
    def list_kbs() -> dict[str, Any]:
        """Return available Pixi Wiki knowledge bases and metadata."""
        return store.list_kbs()

    @mcp.tool()
    def list_documents(kb_id: str) -> dict[str, Any]:
        """Return documents for a selected knowledge base."""
        try:
            return store.list_documents(kb_id)
        except PixiWikiError as exc:
            return exc.as_dict()

    @mcp.tool()
    def read_document(kb_id: str, document_id: str) -> dict[str, Any]:
        """Return Markdown content and metadata for a selected KB document."""
        try:
            return store.read_document(kb_id, document_id)
        except PixiWikiError as exc:
            return exc.as_dict()

    @mcp.tool()
    def search_kb(kb_id: str, query: str, max_results: int = DEFAULT_MAX_RESULTS) -> dict[str, Any]:
        """Search inside one selected knowledge base."""
        try:
            return store.search_kb(kb_id, query, max_results)
        except PixiWikiError as exc:
            return exc.as_dict()

    @mcp.tool()
    def search_all_kbs(query: str, max_results: int = DEFAULT_MAX_RESULTS) -> dict[str, Any]:
        """Search across all Pixi Wiki knowledge bases."""
        try:
            return store.search_all_kbs(query, max_results)
        except PixiWikiError as exc:
            return exc.as_dict()

    @mcp.tool()
    def get_kb_summary(kb_id: str) -> dict[str, Any]:
        """Return the registry metadata and README summary for a selected KB."""
        try:
            return store.get_kb_summary(kb_id)
        except PixiWikiError as exc:
            return exc.as_dict()

    return mcp


def _self_test(root: Path) -> dict[str, Any]:
    store = PixiWikiStore(root)
    kb_payload = store.list_kbs()
    if not kb_payload["kbs"]:
        raise PixiWikiError("NO_KBS", "No KBs are registered.")
    first_kb = kb_payload["kbs"][0]["kb_id"]
    docs_payload = store.list_documents(first_kb)
    if not docs_payload["documents"]:
        raise PixiWikiError("NO_DOCUMENTS", f"KB '{first_kb}' has no documents.")
    first_doc = docs_payload["documents"][0]["document_id"]
    doc_payload = store.read_document(first_kb, first_doc)
    search_payload = store.search_all_kbs("Pixi", max_results=5)
    missing_kb = None
    try:
        store.list_documents("missing-kb")
    except PixiWikiError as exc:
        missing_kb = exc.as_dict()
    missing_doc = None
    try:
        store.read_document(first_kb, "missing-doc.md")
    except PixiWikiError as exc:
        missing_doc = exc.as_dict()
    return {
        "status": "ok",
        "kb_count": kb_payload["kb_count"],
        "first_kb": first_kb,
        "first_doc": first_doc,
        "read_document_bytes": len(doc_payload["content"].encode("utf-8")),
        "search_all_result_count": search_payload["result_count"],
        "missing_kb_error": missing_kb,
        "missing_doc_error": missing_doc,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the read-only Pixi Wiki MCP server.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Pixi Wiki repo/output root. Defaults to this repository.")
    parser.add_argument("--self-test", action="store_true", help="Exercise the read-only store without starting stdio MCP.")
    args = parser.parse_args()

    if args.self_test:
        try:
            print(json.dumps(_self_test(args.root.resolve()), indent=2, sort_keys=True))
        except PixiWikiError as exc:
            print(json.dumps(exc.as_dict(), indent=2, sort_keys=True))
            raise SystemExit(1)
        return

    server = create_mcp_server(args.root.resolve())
    server.run()


if __name__ == "__main__":
    main()
