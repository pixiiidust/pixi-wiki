#!/usr/bin/env python3
"""Build a deterministic, high-signal Pixi Wiki graph.

This script creates a Graphify-compatible graph from the generated Pixi Wiki raw
Markdown corpus without using an LLM. It is a local analysis sidecar: generated,
disposable, and not canonical project truth.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")
MDLINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,4})\s+(.+?)\s*$", re.M)

GENERIC_HEADINGS = {
    "rules",
    "source",
    "sources",
    "scope",
    "boundaries",
    "related pages",
    "canonical",
    "current status",
    "current synthesis",
    "application",
    "applications",
    "definition",
    "what it does",
    "why it exists",
    "why it matters",
    "namespace role",
    "source roots",
    "concepts",
    "entities",
    "summaries",
    "syntheses",
    "not covered",
    "covers",
    "maintenance",
    "public output contract",
    "crosslinks",
    "cross-namespace links",
    "current boundary",
    "routing rules",
    "use policy",
    "import boundary",
    "priority order",
    "source classes",
}
GENERIC_TAGS = {
    "ai",
    "workflow",
    "architecture",
    "agent-systems",
    "knowledge-management",
    "product",
    "agents",
    "evaluation",
    "infrastructure",
    "knowledge-systems",
}
SOURCE_CLASSES = {
    "Knowledge/": "source-class:Knowledge",
    "Projects/": "source-class:Projects",
    "Wiki Compiler Maps/": "source-class:Wiki Compiler Maps",
    "/root/.hermes/skills/": "source-class:Hermes skills",
    "/root/.hermes/knowledge/": "source-class:Hermes knowledge",
    "https://github.com/": "source-class:GitHub repo",
}


def slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[`*_~<>\[\](){}:;,'\"/\\|]+", " ", text)
    text = re.sub(r"[^a-z0-9._-]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")[:140] or "node"


def norm_title(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).strip("# ")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    raw = text[4:end]
    body = text[end + 5 :]
    frontmatter: dict[str, Any] = {}
    current_key: str | None = None

    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            frontmatter.setdefault(current_key, [])
            if isinstance(frontmatter[current_key], list):
                frontmatter[current_key].append(line[4:].strip().strip('"'))
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        current_key = key
        if not value:
            frontmatter[key] = []
        elif value.startswith("[") and value.endswith("]"):
            frontmatter[key] = [
                item.strip().strip('"\'') for item in value[1:-1].split(",") if item.strip()
            ]
        else:
            frontmatter[key] = value.strip('"')

    return frontmatter, body


class SignalGraphBuilder:
    def __init__(self, raw_dir: Path) -> None:
        self.raw_dir = raw_dir.resolve()
        self.nodes: dict[str, dict[str, Any]] = {}
        self.links: list[dict[str, Any]] = []
        self.seen_edges: set[tuple[str, str, str]] = set()
        self.doc_meta: dict[Path, dict[str, Any]] = {}
        self.title_to_doc: dict[str, str] = {}
        self.stem_to_docs: dict[str, list[str]] = defaultdict(list)
        self.rel_to_doc: dict[str, str] = {}

    def add_node(self, node_id: str, label: str, kind: str, **attrs: Any) -> None:
        if node_id in self.nodes:
            return
        node = {
            "id": node_id,
            "label": label,
            "kind": kind,
            "file_type": "document",
            "source_file": "",
        }
        node.update({key: value for key, value in attrs.items() if value is not None})
        self.nodes[node_id] = node

    def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
        *,
        source_file: str = "",
        confidence: str = "EXTRACTED",
        context: str = "",
        weight: float = 1.0,
    ) -> None:
        key = (source, target, relation)
        if source not in self.nodes or target not in self.nodes or key in self.seen_edges:
            return
        self.seen_edges.add(key)
        edge: dict[str, Any] = {
            "source": source,
            "target": target,
            "relation": relation,
            "confidence": confidence,
            "weight": weight,
        }
        if source_file:
            edge["source_file"] = source_file
        if context:
            edge["context"] = context
        self.links.append(edge)

    def scan_documents(self) -> list[Path]:
        md_files = sorted(self.raw_dir.rglob("*.md"))
        for path in md_files:
            rel = path.relative_to(self.raw_dir).as_posix()
            namespace = rel.split("/", 1)[0]
            text = path.read_text(encoding="utf-8", errors="replace")
            frontmatter, body = parse_frontmatter(text)
            title = str(frontmatter.get("title") or "").strip()
            if not title:
                h1 = re.search(r"^#\s+(.+)$", body, re.M)
                title = norm_title(h1.group(1)) if h1 else Path(rel).stem.replace("-", " ").title()

            doc_id = f"doc:{rel}"
            self.doc_meta[path] = {
                "rel": rel,
                "namespace": namespace,
                "title": title,
                "frontmatter": frontmatter,
                "body": body,
                "doc_id": doc_id,
            }
            self.rel_to_doc[rel] = doc_id
            self.title_to_doc[slug(title)] = doc_id
            self.stem_to_docs[slug(Path(rel).stem)].append(doc_id)
        return md_files

    def build(self) -> dict[str, Any]:
        md_files = self.scan_documents()
        for meta in self.doc_meta.values():
            self.add_document(meta)

        kind_counts = Counter(node["kind"] for node in self.nodes.values())
        namespace_counts = Counter(
            node.get("namespace")
            for node in self.nodes.values()
            if node.get("kind") == "document" and node.get("namespace")
        )
        edge_counts = Counter(edge["relation"] for edge in self.links)

        return {
            "raw": str(self.raw_dir),
            "docs": len(md_files),
            "nodes": len(self.nodes),
            "links": len(self.links),
            "kind_counts": dict(kind_counts),
            "namespace_counts": dict(namespace_counts),
            "edge_counts": dict(edge_counts),
            "filtered": {
                "metadata_nodes_excluded": ["type", "status", "confidence"],
                "generic_heading_count": len(GENERIC_HEADINGS),
                "generic_tag_count": len(GENERIC_TAGS),
            },
        }

    def add_document(self, meta: dict[str, Any]) -> None:
        rel = meta["rel"]
        namespace = meta["namespace"]
        title = meta["title"]
        frontmatter = meta["frontmatter"]
        body = meta["body"]
        doc_id = meta["doc_id"]

        self.add_node(doc_id, title, "document", source_file=rel, namespace=namespace)
        namespace_id = f"namespace:{namespace}"
        self.add_node(namespace_id, namespace, "namespace")
        self.add_edge(namespace_id, doc_id, "contains", source_file=rel, context="namespace")

        self.add_tags(doc_id, rel, frontmatter)
        self.add_sources(doc_id, rel, frontmatter)
        self.add_sections(doc_id, rel, body)
        self.add_wikilinks(doc_id, rel, body)
        self.add_markdown_links(doc_id, rel, body)

    def add_tags(self, doc_id: str, rel: str, frontmatter: dict[str, Any]) -> None:
        tags = frontmatter.get("tags", []) if isinstance(frontmatter.get("tags"), list) else []
        for tag in tags:
            if tag.lower().strip() in GENERIC_TAGS:
                continue
            tag_id = f"tag:{slug(tag)}"
            self.add_node(tag_id, f"#{tag}", "tag")
            self.add_edge(doc_id, tag_id, "tagged", source_file=rel, context="frontmatter")

    def add_sources(self, doc_id: str, rel: str, frontmatter: dict[str, Any]) -> None:
        sources = frontmatter.get("sources", []) if isinstance(frontmatter.get("sources"), list) else []
        for source in sources:
            for prefix, label in SOURCE_CLASSES.items():
                if source.startswith(prefix) or prefix in source:
                    self.add_node(label, label.replace("source-class:", "Source: "), "source_class")
                    self.add_edge(doc_id, label, "cites_source_class", source_file=rel, context="frontmatter")
                    break

            stem = slug(Path(source).stem)
            candidates = self.stem_to_docs.get(stem, [])
            if len(candidates) == 1 and candidates[0] != doc_id:
                self.add_edge(
                    doc_id,
                    candidates[0],
                    "cites_document",
                    source_file=rel,
                    confidence="INFERRED",
                    context="source_filename_match",
                    weight=0.7,
                )

    def add_sections(self, doc_id: str, rel: str, body: str) -> None:
        for index, (hashes, heading) in enumerate(HEADING_RE.findall(body)):
            clean = norm_title(re.sub(r"\s*#+$", "", heading))
            if not clean or slug(clean) in GENERIC_HEADINGS:
                continue
            if index > 18:
                break
            section_id = f"section:{rel}:{slug(clean)}"
            self.add_node(section_id, clean, "section", source_file=rel, source_location=f"H{len(hashes)}")
            self.add_edge(doc_id, section_id, "has_section", source_file=rel, context="heading", weight=0.5)

    def add_wikilinks(self, doc_id: str, rel: str, body: str) -> None:
        for target, alias in WIKILINK_RE.findall(body):
            raw_target = target.strip()
            target_key = slug(Path(raw_target).stem)
            candidates = self.stem_to_docs.get(target_key) or (
                [self.title_to_doc[target_key]] if target_key in self.title_to_doc else []
            )
            if len(candidates) == 1 and candidates[0] != doc_id:
                self.add_edge(
                    doc_id,
                    candidates[0],
                    "references_document",
                    source_file=rel,
                    context="wikilink",
                    weight=1.5,
                )
                continue

            label = norm_title(alias or Path(raw_target).stem.replace("-", " "))
            if not label or slug(label) in GENERIC_HEADINGS:
                continue
            concept_id = f"concept:{slug(label)}"
            self.add_node(concept_id, label, "concept")
            self.add_edge(doc_id, concept_id, "mentions_concept", source_file=rel, context="wikilink", weight=0.8)

    def add_markdown_links(self, doc_id: str, rel: str, body: str) -> None:
        for _label, url in MDLINK_RE.findall(body):
            if url.startswith("#") or url.startswith("mailto:"):
                continue
            clean_url = url.split("#", 1)[0]
            if clean_url.startswith("http"):
                if "github.com" in clean_url:
                    source_id = "source-class:GitHub repo"
                    self.add_node(source_id, "Source: GitHub repo", "source_class")
                    self.add_edge(doc_id, source_id, "links_to_source_class", source_file=rel, context="markdown_link")
                continue

            candidate_rel = (Path(rel).parent / clean_url).as_posix()
            candidate_rel = str(Path(candidate_rel))
            if candidate_rel in self.rel_to_doc and self.rel_to_doc[candidate_rel] != doc_id:
                self.add_edge(
                    doc_id,
                    self.rel_to_doc[candidate_rel],
                    "links_to_document",
                    source_file=rel,
                    context="markdown_link",
                    weight=1.2,
                )

    def graph_payload(self) -> dict[str, Any]:
        return {
            "input_tokens": 0,
            "output_tokens": 0,
            "nodes": list(self.nodes.values()),
            "links": self.links,
            "graphify_note": (
                "High-signal deterministic Pixi Wiki Markdown graph; generic metadata/headings "
                "filtered; document links resolved where possible."
            ),
        }


def build_signal_graph(raw_dir: Path, out_dir: Path) -> dict[str, Any]:
    builder = SignalGraphBuilder(raw_dir)
    summary = builder.build()
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "graph.json").write_text(
        json.dumps(builder.graph_payload(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (out_dir / "SIGNAL_MARKDOWN_GRAPH_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a deterministic Pixi Wiki signal graph")
    parser.add_argument("raw_dir", nargs="?", default="raw", help="Raw Pixi Wiki Markdown directory")
    parser.add_argument("out_dir", nargs="?", default="graphify-out", help="Output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = build_signal_graph(Path(args.raw_dir), Path(args.out_dir))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
