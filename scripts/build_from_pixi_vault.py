#!/usr/bin/env python3
"""Build AgentWikis-style namespace output from pixi-vault.

This generator is intentionally conservative: it adds the new namespace registry
surface while preserving the legacy pixi-wiki contract (`concepts`, `documents`,
flat root compatibility shims, and existing domain routes). Source truth lives in
`pixi-vault/wikis/<slug>/`; this repo is the public generated mirror.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path("/root/ObsidianVault/wikis")
DEFAULT_SEED_SLUGS = [
    "pixi-vault",
    "agent-workflows",
    "eval-trace",
    "ai-native-product-surfaces",
    "rl-sim-labs",
    "curated-tuning-datasets",
    "local-ai-infrastructure",
]
NAMESPACE_LLM_MARKER = "---\n\n# Pixi Wiki Namespace Registry"
NAMESPACE_FULL_MARKER = "<!-- ===== AgentWikis namespace registry skeleton ===== -->"


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse simple YAML-ish frontmatter used by pixi-vault namespace pages."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    fm: dict[str, Any] = {}
    current: str | None = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current:
            fm.setdefault(current, [])
            if isinstance(fm[current], list):
                fm[current].append(line[4:].strip())
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            fm[key] = []
            current = key
        elif value.startswith("[") and value.endswith("]"):
            fm[key] = [part.strip().strip('"\'') for part in value[1:-1].split(",") if part.strip()]
            current = key
        else:
            fm[key] = value.strip('"')
            current = key
    return fm, body


def first_heading(text: str) -> str | None:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def first_paragraph(text: str) -> str:
    lines: list[str] = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped or stripped.startswith(("#", ">", "- ", "---")):
            if lines:
                break
            continue
        lines.append(stripped)
        if len(" ".join(lines)) > 220:
            break
    return " ".join(lines)[:260] or "Compiled namespace."


def extract_section(text: str, start: str, end: str) -> str:
    pattern = re.compile(rf"{re.escape(start)}\n\n(.+?)\n\n{re.escape(end)}", re.DOTALL)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def inline_markdown(value: str) -> str:
    escaped = html.escape(value)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    escaped = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", escaped)
    escaped = re.sub(r"\[\[([^\]]+)\]\]", r"\1", escaped)
    return escaped


def markdown_to_html(markdown: str, title: str) -> str:
    out: list[str] = []
    in_code = False
    code: list[str] = []
    in_ul = False

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    for line in markdown.splitlines():
        stripped = line.rstrip()
        if stripped.strip().startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code = []
                in_code = False
            else:
                close_ul()
                in_code = True
            continue
        if in_code:
            code.append(stripped)
            continue
        if not stripped.strip():
            close_ul()
            continue
        if stripped.startswith("# "):
            close_ul()
            out.append(f"<h1>{inline_markdown(stripped[2:].strip())}</h1>")
        elif stripped.startswith("## "):
            close_ul()
            out.append(f"<h2>{inline_markdown(stripped[3:].strip())}</h2>")
        elif stripped.startswith("### "):
            close_ul()
            out.append(f"<h3>{inline_markdown(stripped[4:].strip())}</h3>")
        elif stripped.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_markdown(stripped[2:].strip())}</li>")
        elif stripped.startswith("> "):
            close_ul()
            out.append(f"<blockquote>{inline_markdown(stripped[2:].strip())}</blockquote>")
        else:
            close_ul()
            out.append(f"<p>{inline_markdown(stripped.strip())}</p>")
    close_ul()
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><link rel="stylesheet" href="/pixi-wiki/agent/styles.css">
<style>body{{font-family:Inter,system-ui,sans-serif;max-width:980px;margin:32px auto;padding:0 20px;line-height:1.6;background:#0b1020;color:#e5edf7}}a{{color:#8bd3ff}}code,pre{{background:#111a2e;border-radius:6px}}pre{{padding:12px;overflow:auto}}.meta{{color:#9fb3c8;font-size:.9rem}}nav{{margin-bottom:20px}}</style>
</head><body><nav><a href="/pixi-wiki/">Pixi Wiki</a> · <a href="/pixi-wiki/llms.txt">llms.txt</a> · <a href="/pixi-wiki/index.json">index.json</a></nav>
{''.join(out)}
</body></html>"""


def strip_existing_namespace_section(text: str, marker: str) -> str:
    if marker in text:
        return text.split(marker, 1)[0].rstrip()
    return text.rstrip()


def remove_namespace_outputs(output_root: Path, slugs: list[str]) -> None:
    for slug in slugs:
        for base in [output_root / "raw", output_root / "wiki"]:
            target = base / slug
            if target.exists():
                shutil.rmtree(target)


def collect_namespace(source_dir: Path, output_root: Path, slug: str) -> tuple[dict[str, Any], list[tuple[str, str, str, str]]]:
    namespace_dir = source_dir / slug
    readme_path = namespace_dir / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    fm, readme_body = parse_frontmatter(readme)
    title = fm.get("title") or first_heading(readme) or slug
    category = fm.get("category", "")
    last_updated = fm.get("updated", "") or "unknown"
    description = first_paragraph(readme_body)
    covers = extract_section(readme, "### Covers", "### Not Covered") or description
    not_covered = extract_section(readme, "### Not Covered", "### Current As")

    links: list[tuple[str, str, str, str]] = []
    md_files = sorted(namespace_dir.rglob("*.md"))
    for source_file in md_files:
        rel = source_file.relative_to(namespace_dir)
        raw_output = output_root / "raw" / slug / rel
        html_output = output_root / "wiki" / slug / (rel.as_posix() + ".html")
        raw_output.parent.mkdir(parents=True, exist_ok=True)
        html_output.parent.mkdir(parents=True, exist_ok=True)
        text = source_file.read_text(encoding="utf-8")
        raw_output.write_text(text, encoding="utf-8")
        page_fm, body = parse_frontmatter(text)
        page_title = page_fm.get("title") or first_heading(text) or rel.name
        html_output.write_text(markdown_to_html(body if page_fm else text, page_title), encoding="utf-8")
        links.append((page_title, rel.as_posix(), f"/raw/{slug}/{rel.as_posix()}", f"/wiki/{slug}/{rel.as_posix()}.html"))

    wiki_record = {
        "slug": slug,
        "title": title,
        "description": description,
        "tags": [category] if category else [],
        "category": category,
        "scope": {"covers": covers, "notCovered": not_covered, "currentAs": last_updated},
        "lastUpdated": last_updated,
        "documentCount": len(md_files),
        "llms_txt": "/llms.txt",
        "raw_base": f"/raw/{slug}/",
        "html_base": f"/wiki/{slug}/",
    }
    return wiki_record, links


def build(source_dir: Path, output_root: Path, slugs: list[str]) -> None:
    if not source_dir.is_dir():
        raise SystemExit(f"Source namespace directory not found: {source_dir}")
    missing = [slug for slug in slugs if not (source_dir / slug).is_dir()]
    if missing:
        raise SystemExit(f"Missing namespace source dirs: {', '.join(missing)}")

    remove_namespace_outputs(output_root, slugs)

    legacy_index = json.loads((output_root / "index.json").read_text(encoding="utf-8"))
    legacy_llms = strip_existing_namespace_section((output_root / "llms.txt").read_text(encoding="utf-8"), NAMESPACE_LLM_MARKER)
    legacy_full = strip_existing_namespace_section((output_root / "llms-full.txt").read_text(encoding="utf-8"), NAMESPACE_FULL_MARKER)

    wikis: list[dict[str, Any]] = []
    full_sections: list[tuple[str, str]] = []
    namespace_llms = [
        "> AgentWikis-style registry generated from pixi-vault compiled namespaces.\n\n",
        "> Raw Markdown: `/raw/<slug>/<path>`. Human HTML: `/wiki/<slug>/<path>.html`.\n\n",
    ]
    for slug in slugs:
        wiki_record, links = collect_namespace(source_dir, output_root, slug)
        wikis.append(wiki_record)
        namespace_llms.append(f"## {wiki_record['title']}\n\n")
        namespace_llms.append(f"> {wiki_record['description']}\n")
        namespace_llms.append(f"> Current as of: {wiki_record['lastUpdated']}\n\n")
        for title, rel, raw_url, html_url in links:
            namespace_llms.append(f"- [{title}]({raw_url}) ([html]({html_url}))\n")
            full_sections.append((f"{slug}/{rel}", (source_dir / slug / rel).read_text(encoding="utf-8")))
        namespace_llms.append("\n")

    legacy_index["wikis"] = wikis
    legacy_index["comingSoon"] = []
    legacy_index["namespace_registry"] = {
        "schema_version": "pixi-agentwikis-registry-v0",
        "source_repo": "pixiiidust/pixi-vault",
        "source_path": "wikis/<slug>/",
        "raw_pattern": "/raw/<slug>/<path>",
        "html_pattern": "/wiki/<slug>/<path>.html",
        "legacy_root_flat_pages": "temporary-shims",
    }
    (output_root / "index.json").write_text(json.dumps(legacy_index, indent=2), encoding="utf-8")
    llms_text = legacy_llms + "\n\n" + NAMESPACE_LLM_MARKER + "\n\n" + "".join(namespace_llms)
    (output_root / "llms.txt").write_text(llms_text.rstrip() + "\n", encoding="utf-8")
    full_body = "\n\n".join(f"<!-- ===== {name} ===== -->\n\n{text}" for name, text in full_sections)
    full_text = legacy_full + "\n\n" + NAMESPACE_FULL_MARKER + "\n\n" + full_body
    (output_root / "llms-full.txt").write_text(full_text.rstrip() + "\n", encoding="utf-8")

    index_html = (output_root / "index.html").read_text(encoding="utf-8")
    namespace_section = """<section class="card" id="agentwikis-namespace-registry">
  <h2>AgentWikis Namespace Registry</h2>
  <p>New canonical namespace skeleton generated from <code>pixi-vault/wikis/&lt;slug&gt;</code>. Legacy root flat pages remain temporary shims during the migration grace period.</p>
  <ul>
"""
    for wiki in wikis:
        namespace_section += f'    <li><a href="/pixi-wiki/wiki/{wiki["slug"]}/README.md.html">{html.escape(wiki["title"])}</a> <span class="meta">({wiki["documentCount"]} docs)</span></li>\n'
    namespace_section += "  </ul>\n</section>\n"
    if 'id="agentwikis-namespace-registry"' in index_html:
        index_html = re.sub(r'<section class="card" id="agentwikis-namespace-registry">.*?</section>\n?', namespace_section, index_html, flags=re.DOTALL)
    elif "</main>" in index_html:
        index_html = index_html.replace("</main>", namespace_section + "\n</main>")
    else:
        index_html += "\n" + namespace_section
    (output_root / "index.html").write_text(index_html, encoding="utf-8")

    styles = output_root / "agent" / "styles.css"
    styles.parent.mkdir(parents=True, exist_ok=True)
    if not styles.exists():
        styles.write_text("body{font-family:Inter,system-ui,sans-serif;}\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Path to pixi-vault/wikis")
    parser.add_argument("--output", type=Path, default=ROOT, help="Path to pixi-wiki output repo")
    parser.add_argument("--slug", action="append", dest="slugs", help="Namespace slug to include; repeatable")
    args = parser.parse_args()
    build(args.source.resolve(), args.output.resolve(), args.slugs or DEFAULT_SEED_SLUGS)


if __name__ == "__main__":
    main()
