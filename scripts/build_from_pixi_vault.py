#!/usr/bin/env python3
"""Build a clean AgentWikis-style public mirror from pixi-vault namespaces.

Source truth lives in `pixi-vault/wikis/<slug>/`. This repo is derived output:
root registry files, raw Markdown mirrors, rendered HTML namespace pages, and
namespace-local agent entrypoints.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

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
GENERATED_ROOT_FILES = ["index.html", "index.json", "llms.txt", "llms-full.txt"]
LEGACY_ROOT_PATTERNS = ["concept-*.html", "projects-*.html", "knowledge.html", "projects.html", "maps-of-content.html", "root.html"]
GENERATED_DIRS = ["raw", "wiki", "agent", "legacy"]
CONTENT_DIRS = {"concepts", "entities", "summaries", "syntheses"}


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
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
        if len(" ".join(lines)) > 260:
            break
    return " ".join(lines)[:300] or "Compiled namespace."


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^###\s+{re.escape(heading)}\s*$\n\n(.+?)(?=\n###\s+|\n##\s+|\Z)", re.DOTALL | re.MULTILINE | re.IGNORECASE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def strip_scope_section(markdown: str) -> str:
    return re.sub(r"\n## Scope\n\n.*?(?=\n##\s+|\Z)", "\n", markdown, flags=re.DOTALL)


def inline_markdown(value: str) -> str:
    escaped = html.escape(value)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    escaped = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", escaped)
    escaped = re.sub(r"\[\[([^\]]+)\]\]", r"\1", escaped)
    return escaped


def markdown_fragment(markdown: str) -> str:
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
    return "\n".join(out)


def site_css() -> str:
    return """
:root{color-scheme:light;--bg:#f7f3ea;--panel:#fffaf1;--panel2:#f0e8d8;--border:#d9cdb8;--soft:#eadfcb;--text:#22202a;--muted:#6f6a77;--heading:#111018;--accent:#9b5c00;--accent2:#6f4200;--green:#087a4a;--header:#fffdf8;--active-bg:#fff1d1}
[data-theme=dark]{color-scheme:dark;--bg:#07090d;--panel:#101820;--panel2:#0b1118;--border:#263849;--soft:#172231;--text:#d8dee8;--muted:#95a6b4;--heading:#f6f0df;--accent:#8fb7c8;--accent2:#fbdc92;--green:#fbdc92;--header:#07090d;--active-bg:#8b4356}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:"IBM Plex Mono","JetBrains Mono","Roboto Mono",ui-monospace,monospace;font-size:14px;line-height:1.7}a{color:var(--accent);text-decoration:none;border-bottom:1px dotted currentColor}a:hover{color:var(--accent2)}code{background:var(--panel2);border:1px solid var(--border);color:var(--accent2);padding:1px 5px;border-radius:4px}pre{background:var(--panel2);border:1px solid var(--border);padding:14px;overflow:auto}.site-header{height:66px;border-bottom:1px solid var(--border);background:var(--header)}.header-inner{max-width:1180px;margin:0 auto;height:100%;display:flex;align-items:center;justify-content:space-between;padding:0 20px}.logo{color:var(--heading);font-weight:800;letter-spacing:.04em;border:0}.nav{display:flex;align-items:center;gap:24px}.nav a{color:var(--muted);border:0;font-size:12px;letter-spacing:.14em;text-transform:uppercase}.nav a:hover{color:var(--heading)}.theme-toggle{border:1px solid var(--border);background:var(--panel);color:var(--text);padding:8px 10px;border-radius:999px;font:inherit;font-size:12px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}.theme-toggle:hover{border-color:var(--accent);color:var(--accent)}.category-bar{border-bottom:1px solid var(--border);background:var(--panel)}.category-inner{max-width:1180px;margin:0 auto;display:flex;gap:22px;min-height:46px;align-items:center;padding:0 20px;flex-wrap:wrap}.category-inner a{color:var(--muted);border:0;font-size:12px;letter-spacing:.12em;text-transform:uppercase}.category-inner a:first-child{color:var(--muted)}.page{max-width:1180px;margin:40px auto 90px;display:grid;grid-template-columns:260px minmax(0,1fr);gap:48px;padding:0 20px}.sidebar{color:var(--muted)}.sidebar-block{border-left:1px solid var(--border);padding-left:12px;margin-bottom:24px}.sidebar-title{color:var(--heading);font-weight:800;margin-bottom:4px}.sidebar-count{color:var(--muted);font-size:11px;margin-bottom:16px}.sidebar a{display:block;padding:6px 10px;color:var(--muted);border:0;font-size:13px}.sidebar a.active{background:var(--active-bg);color:var(--accent2);border-left:2px solid var(--accent);margin-left:-13px;padding-left:11px;font-weight:800}.sidebar-section-title{margin:12px 0 6px;color:var(--muted);font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:800}.sidebar-section{margin:10px 0}.sidebar-section summary{list-style:none;cursor:pointer;color:var(--muted);font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:800;padding:6px 10px;border-radius:8px}.sidebar-section summary::-webkit-details-marker{display:none}.sidebar-section summary::before{content:"▸";display:inline-block;width:14px;color:var(--accent);transition:transform .12s ease}.sidebar-section[open] summary::before{transform:rotate(90deg)}.sidebar-section summary:hover{background:var(--panel2);color:var(--heading)}.sidebar-section-body{margin:2px 0 6px 12px;border-left:1px solid var(--border);padding-left:4px}.sidebar-empty{padding:6px 10px;color:var(--muted);font-size:12px;font-style:italic}.article{min-width:0}.content-header{display:flex;justify-content:space-between;gap:18px;align-items:baseline;margin-bottom:18px;color:var(--muted);font-size:13px}.breadcrumbs a,.markdown-link{color:var(--accent)}h1{margin:0 0 10px;color:var(--heading);font-size:36px;line-height:1.1;font-weight:900;letter-spacing:-.04em;text-transform:uppercase}h2{margin:48px 0 14px;padding-bottom:10px;border-bottom:1px solid var(--border);color:var(--heading);font-size:22px;line-height:1.2;font-weight:900;text-transform:uppercase}h2::before{content:"// ";color:var(--accent2)}h3{margin:26px 0 8px;color:var(--heading);text-transform:uppercase;font-size:15px;letter-spacing:.08em}.updated{color:var(--muted);font-size:13px;margin-bottom:18px}.info-card{border:1px solid var(--border);background:var(--panel);padding:20px 22px;margin:24px 0}.info-row{display:grid;grid-template-columns:136px 1fr;gap:18px;margin-bottom:12px}.info-row:last-child{margin-bottom:0}.info-label{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:900}.green{color:var(--green)}.yellow{color:var(--accent2)}.white{color:var(--heading)}.agent-card{margin:24px 0 22px;padding:14px 18px;background:var(--active-bg);border:1px solid var(--border);border-left:2px solid var(--accent);color:var(--text)}.agent-card a{font-weight:800;margin-right:12px}.hero-copy{max-width:860px;color:var(--text);font-size:16px}.hero-actions{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0 18px}.button-link{display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--border);border-radius:999px;padding:9px 14px;background:var(--panel);color:var(--heading);font-weight:800;font-size:12px;letter-spacing:.08em;text-transform:uppercase}.button-link.primary{background:var(--active-bg);border-color:var(--accent);color:var(--accent2)}.button-link:hover{border-color:var(--accent);color:var(--accent2)}.agent-setup-callout{max-width:860px;margin:18px 0 34px;padding:16px 18px;background:var(--panel);border:1px solid var(--border);border-left:2px solid var(--accent)}.agent-setup-callout h2{font-size:16px;margin:0 0 6px;padding:0;border:0}.agent-setup-callout h2::before{content:""}.agent-setup-callout p{margin:0;color:var(--muted)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:26px}.card{border:1px solid var(--border);border-radius:14px;padding:18px;background:var(--panel)}.card h2{border:0;margin:0 0 8px;padding:0;font-size:18px}.card h2::before{content:""}.meta{color:var(--muted);font-size:.9rem}.page-meta{display:flex;flex-wrap:wrap;gap:6px 16px;margin:8px 0 22px;color:var(--muted);font-size:13px}.page-meta span{color:var(--heading);font-weight:800}.page-tools{display:flex;gap:12px;flex-wrap:wrap;justify-content:flex-end}.prev-next{margin-top:54px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.prev-next-card{border:1px solid var(--border);border-bottom:1px dotted var(--accent);background:var(--panel);padding:18px 20px;text-decoration:none;display:block}.prev-card{text-align:left}.next-card{text-align:right}.next-label{display:block;color:var(--muted);font-size:11px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:8px}.next-title{color:var(--heading);font-weight:800}.footer{border-top:1px solid var(--border);background:var(--header);color:var(--muted)}.footer-inner{max-width:1180px;margin:0 auto;padding:28px 20px;display:flex;justify-content:space-between;gap:20px}.footer a{margin-left:12px}@media(max-width:820px){.page{grid-template-columns:1fr}.nav{display:none}.info-row{grid-template-columns:1fr}.footer-inner{display:block}}
"""


def theme_script() -> str:
    return """<script>(function(){const key='pixi-wiki-theme';const root=document.documentElement;const saved=localStorage.getItem(key)||'light';root.dataset.theme=saved;function label(){const b=document.querySelector('[data-theme-toggle]');if(b)b.textContent=root.dataset.theme==='dark'?'☀':'☾';}document.addEventListener('DOMContentLoaded',function(){label();const b=document.querySelector('[data-theme-toggle]');if(b)b.addEventListener('click',function(){root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';localStorage.setItem(key,root.dataset.theme);label();});});})();</script>"""


def clean_generated_output(output_root: Path) -> None:
    for name in GENERATED_DIRS:
        path = output_root / name
        if path.exists():
            shutil.rmtree(path)
    for name in GENERATED_ROOT_FILES:
        path = output_root / name
        if path.exists():
            path.unlink()
    for pattern in LEGACY_ROOT_PATTERNS:
        for path in output_root.glob(pattern):
            if path.is_file():
                path.unlink()


def category_for(rel: Path, fm: dict[str, Any]) -> str:
    if len(rel.parts) >= 3 and rel.parts[0] == "wiki" and rel.parts[1] in CONTENT_DIRS:
        return rel.parts[1]
    if rel.as_posix() == "wiki/index.md":
        return "wiki"
    if fm.get("type") in CONTENT_DIRS:
        return str(fm["type"])
    return "other"


def sidebar_category(rel: Path, fm: dict[str, Any]) -> str:
    rel_posix = rel.as_posix()
    if rel_posix == "wiki/log.md":
        return "wiki"
    if len(rel.parts) >= 3 and rel.parts[0] == "wiki" and rel.parts[1] in CONTENT_DIRS:
        return rel.parts[1]
    if fm.get("type") in CONTENT_DIRS:
        return str(fm["type"])
    return "other"


def make_sidebar(slug: str, title: str, doc_count: int, counts: Counter[str], active_rel: str, sidebar_docs: list[dict[str, str]]) -> str:
    def cls(rel: str) -> str:
        return ' class="active"' if rel == active_rel else ""

    def section(label: str, category: str) -> str:
        docs = sorted((doc for doc in sidebar_docs if doc["category"] == category), key=lambda doc: doc["title"].lower())
        count = len(docs)
        open_attr = " open" if any(doc["path"] == active_rel for doc in docs) else ""
        links = "".join(
            f'<a{cls(doc["path"])} href="/pixi-wiki/wiki/{slug}/{html.escape(doc["path"])}.html">📄 {html.escape(doc["title"])}</a>'
            for doc in docs
        )
        empty = '<div class="sidebar-empty">No pages yet</div>' if not docs else ""
        return f'<details class="sidebar-section"{open_attr}><summary>{label} {count}</summary><div class="sidebar-section-body">{links}{empty}</div></details>'

    rows = [
        f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-title">{html.escape(title)}</div><div class="sidebar-count">{doc_count} documents</div>',
        f'<a{cls("README.md")} href="/pixi-wiki/wiki/{slug}/README.md.html">📄 {html.escape(title)} Knowledge Base</a>',
        f'<a{cls("wiki/index.md")} href="/pixi-wiki/wiki/{slug}/wiki/index.md.html">📄 {html.escape(title)} KB — Master Index</a>',
        section("WIKI", "wiki"),
        section("CONCEPTS", "concepts"),
        section("ENTITIES", "entities"),
        section("SUMMARIES", "summaries"),
        section("SYNTHESES", "syntheses"),
        '</div><div class="sidebar-block"><details class="sidebar-section" open><summary>// FOR AGENTS</summary><div class="sidebar-section-body">',
        f'<a href="/pixi-wiki/wiki/{slug}/llms.txt">llms.txt</a>',
        f'<a href="/pixi-wiki/wiki/{slug}/llms-full.txt">llms-full.txt</a>',
        f'<a href="/pixi-wiki/wiki/{slug}/index.json">index.json</a>',
        "</div></details></div></aside>",
    ]
    return "\n".join(rows)


def page_shell(slug: str, namespace_title: str, doc_count: int, counts: Counter[str], active_rel: str, sidebar_docs: list[dict[str, str]], article: str, page_title: str) -> str:
    sidebar = make_sidebar(slug, namespace_title, doc_count, counts, active_rel, sidebar_docs)
    return f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(page_title)} — {html.escape(namespace_title)} — Pixi Wiki</title>
<style>{site_css()}</style>{theme_script()}</head><body>
<header class="site-header"><div class="header-inner"><a class="logo" href="/pixi-wiki/">Pixi Wiki</a><nav class="nav"><a href="/pixi-wiki/#wikis">Wikis</a><a href="/pixi-wiki/docs/AGENT_SETUP.html">Agent Setup</a><a href="https://github.com/pixiiidust/pixi-wiki">GitHub</a><button class="theme-toggle" data-theme-toggle type="button">☾</button></nav></div></header>
<main class="page">{sidebar}<article class="article">{article}</article></main>
<footer class="footer"><div class="footer-inner"><p>Plain static HTML. Humans browse it like a wiki; agents read Markdown through <code>llms.txt</code>.</p><p><a href="/pixi-wiki/llms.txt">/llms.txt</a><a href="/pixi-wiki/llms-full.txt">/llms-full.txt</a><a href="/pixi-wiki/index.json">/index.json</a></p></div></footer>
</body></html>"""


def report_mistake_url(slug: str, rel: str) -> str:
    title = quote_plus(f"Pixi Wiki correction: {slug}/{rel}")
    body = quote_plus(f"Page: https://pixiiidust.github.io/pixi-wiki/wiki/{slug}/{rel}.html\n\nWhat should be corrected?")
    return f"https://github.com/pixiiidust/pixi-wiki/issues/new?title={title}&body={body}"


def page_tools(slug: str, rel: str) -> str:
    return (
        f'<span class="page-tools"><a class="markdown-link" href="/pixi-wiki/raw/{slug}/{html.escape(rel)}">view as markdown</a>'
        f'<a class="markdown-link" href="{report_mistake_url(slug, rel)}">report a mistake</a></span>'
    )


def metadata_block(fm: dict[str, Any]) -> str:
    rows: list[str] = []
    for key in ["type", "confidence", "updated", "status", "namespace"]:
        value = fm.get(key)
        if value:
            rows.append(f'<div><span>{html.escape(key)}</span>: {html.escape(str(value))}</div>')
    sources = fm.get("sources")
    if isinstance(sources, list) and sources:
        rows.append(f'<div><span>sources</span>: {len(sources)}</div>')
    elif sources:
        rows.append(f'<div><span>sources</span>: {html.escape(str(sources))}</div>')
    return f'<div class="page-meta">{"".join(rows)}</div>' if rows else ""


def with_metadata_after_h1(rendered_body: str, meta: str) -> str:
    if not meta:
        return rendered_body
    return re.sub(r"(</h1>)", r"\1\n" + meta, rendered_body, count=1) if "</h1>" in rendered_body else meta + rendered_body


def prev_next_nav(slug: str, prev_doc: dict[str, str] | None, next_doc: dict[str, str] | None) -> str:
    cards: list[str] = []
    if prev_doc:
        cards.append(
            f'<a class="prev-next-card prev-card" href="/pixi-wiki/wiki/{slug}/{html.escape(prev_doc["path"])}.html">'
            f'<span class="next-label">← Prev</span><span class="next-title">{html.escape(prev_doc["title"])}</span></a>'
        )
    if next_doc:
        cards.append(
            f'<a class="prev-next-card next-card" href="/pixi-wiki/wiki/{slug}/{html.escape(next_doc["path"])}.html">'
            f'<span class="next-label">Next</span><span class="next-title">{html.escape(next_doc["title"])} →</span></a>'
        )
    return f'<nav class="prev-next">{"".join(cards)}</nav>' if cards else ""


def render_readme(slug: str, title: str, fm: dict[str, Any], body: str, covers: str, not_covered: str, current_as: str, next_doc: dict[str, str] | None) -> str:
    updated = fm.get("updated", "unknown")
    description = first_paragraph(body)
    body_without_title = re.sub(r"^#\s+.+\n", "", body, count=1).strip()
    body_without_scope = strip_scope_section(body_without_title).strip()
    article = f"""
<div class="content-header"><div class="breadcrumbs"><a href="/pixi-wiki/">wikis</a> / <a href="/pixi-wiki/wiki/{slug}/README.md.html">{html.escape(title)}</a> / README.md</div>{page_tools(slug, "README.md")}</div>
<h1>{html.escape(title)} Knowledge Base</h1>
{metadata_block(fm)}
<div class="updated">updated: <strong>{html.escape(str(updated))}</strong></div>
<section class="info-card"><div class="info-row"><div class="info-label green">Covers</div><div>{inline_markdown(covers)}</div></div><div class="info-row"><div class="info-label yellow">Not Covered</div><div>{inline_markdown(not_covered or "Out-of-scope or stale material; verify with source notes and live tools.")}</div></div><div class="info-row"><div class="info-label white">Current As Of</div><div>{html.escape(current_as or str(updated))}</div></div></section>
<div class="agent-card">🤖 Agent access: <a href="/pixi-wiki/wiki/{slug}/llms.txt">/wiki/{slug}/llms.txt</a> <a href="/pixi-wiki/wiki/{slug}/llms-full.txt">/wiki/{slug}/llms-full.txt</a> <a href="/pixi-wiki/wiki/{slug}/index.json">/wiki/{slug}/index.json</a></div>
<p>{inline_markdown(description)}</p>
<h2>Structure</h2><ul><li><code>raw/</code> — raw Markdown provenance mirror for agents and source inspection.</li><li><code>wiki/</code> — synthesized knowledge pages: concepts, entities, summaries, and syntheses.</li><li>Schema and maintenance rules: see <code>CLAUDE.md</code>.</li></ul>
<h2>Usage</h2><ul><li><strong>Add new sources:</strong> update canonical source notes in <code>pixi-vault</code>, then compile into this namespace.</li><li><strong>Ask questions:</strong> agents read this wiki and cite raw/source paths.</li><li><strong>Publish:</strong> regenerate <code>pixi-wiki</code>, run tests, then live-verify raw and HTML routes.</li></ul>
{markdown_fragment(body_without_scope) if body_without_scope else ""}
{prev_next_nav(slug, None, next_doc)}
"""
    return article


def render_page(slug: str, title: str, rel: str, page_title: str, fm: dict[str, Any], body: str, prev_doc: dict[str, str] | None, next_doc: dict[str, str] | None) -> str:
    rendered_body = with_metadata_after_h1(markdown_fragment(body), metadata_block(fm))
    return f"""
<div class="content-header"><div class="breadcrumbs"><a href="/pixi-wiki/">wikis</a> / <a href="/pixi-wiki/wiki/{slug}/README.md.html">{html.escape(title)}</a> / {html.escape(rel)}</div>{page_tools(slug, rel)}</div>
{rendered_body}
{prev_next_nav(slug, prev_doc, next_doc)}
"""


def collect_namespace(source_dir: Path, output_root: Path, slug: str) -> tuple[dict[str, Any], list[tuple[str, str, str, str]], list[tuple[str, str]]]:
    namespace_dir = source_dir / slug
    readme_path = namespace_dir / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    fm, readme_body = parse_frontmatter(readme)
    title = fm.get("title") or first_heading(readme) or slug
    category = fm.get("category", "")
    last_updated = fm.get("updated", "") or "unknown"
    description = first_paragraph(readme_body)
    covers = extract_section(readme, "Covers") or description
    not_covered = extract_section(readme, "Not Covered")
    current_as = extract_section(readme, "Current As") or str(last_updated)

    md_files = sorted(namespace_dir.rglob("*.md"))
    parsed: list[tuple[Path, str, dict[str, Any], str, str]] = []
    counts: Counter[str] = Counter()
    for source_file in md_files:
        rel = source_file.relative_to(namespace_dir)
        text = source_file.read_text(encoding="utf-8")
        page_fm, body = parse_frontmatter(text)
        page_title = page_fm.get("title") or first_heading(text) or rel.name
        parsed.append((rel, text, page_fm, body, str(page_title)))
        counts[sidebar_category(rel, page_fm)] += 1

    links: list[tuple[str, str, str, str]] = []
    full_sections: list[tuple[str, str]] = []
    doc_records: list[dict[str, str]] = []
    sidebar_docs = [
        {"title": page_title, "path": rel.as_posix(), "category": sidebar_category(rel, page_fm)}
        for rel, _text, page_fm, _body, page_title in parsed
        if rel.as_posix() not in {"README.md", "wiki/index.md", "CLAUDE.md"}
    ]

    def navigation_rank(item: tuple[Path, str, dict[str, Any], str, str]) -> tuple[int, str]:
        rel, _text, page_fm, _body, page_title = item
        rel_posix = rel.as_posix()
        if rel_posix == "README.md":
            return (0, page_title.lower())
        if rel_posix == "wiki/index.md":
            return (1, page_title.lower())
        category_rank = {"concepts": 2, "entities": 3, "summaries": 4, "syntheses": 5, "wiki": 6, "other": 7}
        return (category_rank.get(sidebar_category(rel, page_fm), 7), page_title.lower())

    nav_docs = [
        {"title": page_title, "path": rel.as_posix()}
        for rel, _text, page_fm, _body, page_title in sorted(parsed, key=navigation_rank)
        if rel.as_posix() != "CLAUDE.md"
    ]
    nav_by_path = {doc["path"]: index for index, doc in enumerate(nav_docs)}

    # Namespace-local agent access files.
    ns_wiki_dir = output_root / "wiki" / slug
    ns_wiki_dir.mkdir(parents=True, exist_ok=True)
    local_llms: list[str] = [f"# {title} Knowledge Base\n\n", f"> {description}\n\n"]
    for rel, text, _page_fm, _body, page_title in parsed:
        rel_posix = rel.as_posix()
        raw_url = f"/raw/{slug}/{rel_posix}"
        html_url = f"/wiki/{slug}/{rel_posix}.html"
        local_llms.append(f"- [{page_title}]({raw_url}) ([html]({html_url}))\n")
    (ns_wiki_dir / "llms.txt").write_text("".join(local_llms).rstrip() + "\n", encoding="utf-8")
    (ns_wiki_dir / "llms-full.txt").write_text("\n\n".join(f"<!-- ===== {slug}/{rel.as_posix()} ===== -->\n\n{text}" for rel, text, *_ in parsed) + "\n", encoding="utf-8")

    for rel, text, page_fm, body, page_title in parsed:
        rel_posix = rel.as_posix()
        raw_output = output_root / "raw" / slug / rel
        html_output = output_root / "wiki" / slug / (rel_posix + ".html")
        raw_output.parent.mkdir(parents=True, exist_ok=True)
        html_output.parent.mkdir(parents=True, exist_ok=True)
        raw_output.write_text(text, encoding="utf-8")
        nav_index = nav_by_path.get(rel_posix)
        prev_doc = nav_docs[nav_index - 1] if nav_index is not None and nav_index > 0 else None
        next_doc = nav_docs[nav_index + 1] if nav_index is not None and nav_index + 1 < len(nav_docs) else None
        if rel_posix == "README.md":
            article = render_readme(slug, str(title), fm, readme_body, covers, not_covered, current_as, next_doc)
        else:
            article = render_page(slug, str(title), rel_posix, str(page_title), page_fm, body if page_fm else text, prev_doc, next_doc)
        html_output.write_text(page_shell(slug, str(title), len(md_files), counts, rel_posix, sidebar_docs, article, str(page_title)), encoding="utf-8")
        raw_url = f"/raw/{slug}/{rel_posix}"
        html_url = f"/wiki/{slug}/{rel_posix}.html"
        links.append((str(page_title), rel_posix, raw_url, html_url))
        full_sections.append((f"{slug}/{rel_posix}", text))
        doc_records.append({"title": str(page_title), "path": rel_posix, "raw": raw_url, "html": html_url, "category": sidebar_category(rel, page_fm)})

    local_index = {
        "slug": slug,
        "title": title,
        "description": description,
        "documentCount": len(md_files),
        "counts": {key: counts.get(key, 0) for key in ["wiki", "concepts", "entities", "summaries", "syntheses"]},
        "documents": doc_records,
    }
    (ns_wiki_dir / "index.json").write_text(json.dumps(local_index, indent=2) + "\n", encoding="utf-8")

    wiki_record = {
        "slug": slug,
        "title": title,
        "description": description,
        "tags": [category] if category else [],
        "category": category,
        "scope": {"covers": covers, "notCovered": not_covered, "currentAs": current_as or last_updated},
        "lastUpdated": last_updated,
        "documentCount": len(md_files),
        "counts": local_index["counts"],
        "llms_txt": f"/wiki/{slug}/llms.txt",
        "llms_full_txt": f"/wiki/{slug}/llms-full.txt",
        "index_json": f"/wiki/{slug}/index.json",
        "raw_base": f"/raw/{slug}/",
        "html_base": f"/wiki/{slug}/",
        "documents": doc_records,
    }
    return wiki_record, links, full_sections


def write_agent_setup_page(output_root: Path) -> None:
    docs_dir = output_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    body = """
<article class="article" style="max-width:900px;margin:44px auto 90px;padding:0 20px">
<div class="content-header"><div class="breadcrumbs"><a href="/pixi-wiki/">wikis</a> / Agent Setup</div><span class="page-tools"><a class="markdown-link" href="/pixi-wiki/docs/MCP_SERVER.md">MCP server docs</a></span></div>
<h1>Agent Setup</h1>
<p class="hero-copy">Connect AI agents to Pixi Wiki so they can list, search, and read the same Markdown knowledge bases behind the human wiki.</p>
<section class="info-card"><div class="info-row"><div class="info-label green">Why</div><div>Subagents do not inherit your full context, preferences, voice, project priorities, or thesis automatically. Make retrieval explicit before research or writing.</div></div><div class="info-row"><div class="info-label yellow">Access</div><div>Read-only local MCP over <code>index.json</code> and <code>raw/&lt;kb&gt;/**/*.md</code>. No write, edit, or delete tools.</div></div><div class="info-row"><div class="info-label white">Use</div><div>Good for project context, public knowledge, portfolio framing, source-backed retrieval, and agent onboarding.</div></div></section>
<h2>Connect the MCP server</h2>
<pre><code>git clone https://github.com/pixiiidust/pixi-wiki.git
cd pixi-wiki
python3 -m pip install mcp
python3 scripts/pixi_wiki_mcp.py --self-test</code></pre>
<p>Then configure your MCP client to launch:</p>
<pre><code>python3 /path/to/pixi-wiki/scripts/pixi_wiki_mcp.py</code></pre>
<h2>Hermes config</h2>
<pre><code>mcp_servers:
  pixi_wiki:
    command: "python3"
    args: ["/root/pixi-wiki/scripts/pixi_wiki_mcp.py"]</code></pre>
<p>Restart Hermes after editing the config. Tools appear with the <code>mcp_pixi_wiki_</code> prefix.</p>
<h2>Recommended agent workflow</h2>
<ul><li>Call <code>list_kbs</code>.</li><li>Call <code>get_kb_summary</code> for relevant KBs.</li><li>Call <code>search_all_kbs</code> for the task topic.</li><li>Call <code>read_document</code> for the best matches.</li><li>Tailor the answer to retrieved context instead of producing generic research.</li></ul>
<h2>Subagent instruction template</h2>
<pre><code>Before doing research, writing, product strategy, or project analysis, use the Pixi Wiki MCP server. Start with list_kbs, then search_all_kbs for the topic, then read the most relevant documents. Tailor the answer to Jamie's documented project context and preferences. Do not produce generic output if Pixi Wiki has relevant context.</code></pre>
<h2>Important boundary</h2>
<p>Pixi Wiki MCP exposes public compiled KBs. Private memory, live chat context, secrets, and profile-only preferences are separate unless intentionally compiled into a private/local-only KB.</p>
<p><a class="button-link primary" href="/pixi-wiki/docs/MCP_SERVER.md">Full MCP server reference →</a></p>
</article>
"""
    page = f"""<!doctype html>
<html lang=\"en\" data-theme=\"light\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>Agent Setup — Pixi Wiki</title><style>{site_css()}</style>{theme_script()}</head><body>
<header class=\"site-header\"><div class=\"header-inner\"><a class=\"logo\" href=\"/pixi-wiki/\">Pixi Wiki</a><nav class=\"nav\"><a href=\"/pixi-wiki/#wikis\">Wikis</a><a href=\"/pixi-wiki/docs/AGENT_SETUP.html\">Agent Setup</a><a href=\"https://github.com/pixiiidust/pixi-wiki\">GitHub</a><button class=\"theme-toggle\" data-theme-toggle type=\"button\">☾</button></nav></div></header>
<main>{body}</main>
<footer class=\"footer\"><div class=\"footer-inner\"><p>Plain static HTML. Agents read Markdown through <code>llms.txt</code> and MCP.</p><p><a href=\"/pixi-wiki/llms.txt\">/llms.txt</a><a href=\"/pixi-wiki/llms-full.txt\">/llms-full.txt</a><a href=\"/pixi-wiki/index.json\">/index.json</a></p></div></footer>
</body></html>"""
    (docs_dir / "AGENT_SETUP.html").write_text(page, encoding="utf-8")


def write_replicate_page(output_root: Path) -> None:
    docs_dir = output_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    body = """
<article class="article" style="max-width:900px;margin:44px auto 90px;padding:0 20px">
<div class="content-header"><div class="breadcrumbs"><a href="/pixi-wiki/">wikis</a> / Replicate the Approach</div><span class="page-tools"><a class="markdown-link" href="https://github.com/pixiiidust/pixi-wiki">GitHub repo</a></span></div>
<h1>Replicate the Approach</h1>
<p class="hero-copy">Use Pixi Wiki as a reusable pattern for turning your own Markdown notes, research, docs, or vault into a human wiki plus agent-readable context layer.</p>
<section class="info-card"><div class="info-row"><div class="info-label green">Input</div><div>Your Markdown knowledge bases: Obsidian vault folders, project docs, research notes, decision logs, or curated public notes.</div></div><div class="info-row"><div class="info-label yellow">Output</div><div>A static web wiki, raw Markdown mirrors, <code>llms.txt</code>, <code>llms-full.txt</code>, <code>index.json</code>, and local read-only MCP tools.</div></div><div class="info-row"><div class="info-label white">Rule</div><div>Keep Markdown files canonical. Generated HTML, registries, and MCP access should read from the same source-shaped KB files.</div></div></section>
<h2>Who this is for</h2>
<ul><li>People with scattered Markdown notes who want a clean public or local knowledge surface.</li><li>Teams that want agents to retrieve from maintained docs instead of stale chat context.</li><li>Researchers, builders, and PMs who want their thesis, project boundaries, and source trails to survive across AI sessions.</li></ul>
<h2>The reusable contract</h2>
<pre><code>your-wiki/
├── README.md
├── index.html
├── index.json
├── llms.txt
├── llms-full.txt
├── raw/&lt;kb&gt;/**/*.md
├── wiki/&lt;kb&gt;/**/*.html
└── scripts/pixi_wiki_mcp.py</code></pre>
<h2>Port your own knowledge base</h2>
<ul><li>Create one folder per knowledge base.</li><li>Add a <code>README.md</code> that explains scope, current status, and what is not covered.</li><li>Add curated Markdown docs under stable paths.</li><li>Generate raw Markdown mirrors and HTML pages.</li><li>Generate <code>index.json</code> so tools can list KBs and documents.</li><li>Generate <code>llms.txt</code> and <code>llms-full.txt</code> so agents have compact and full entrypoints.</li><li>Run the read-only MCP server locally so agents can list, search, and read your KBs.</li></ul>
<h2>Copy this repo</h2>
<p>The implementation lives in the public GitHub repo. Start there if you want to copy the shape and adapt it to your own use case.</p>
<p><a class="button-link primary" href="https://github.com/pixiiidust/pixi-wiki">Open the Pixi Wiki repo →</a></p>
<h2>Recommended adaptation boundary</h2>
<p>Publish only what you want public. Keep private voice, preferences, secrets, and sensitive strategy in a local-only KB or private repo, then connect that private KB to your agent client separately.</p>
</article>
"""
    page = f"""<!doctype html>
<html lang=\"en\" data-theme=\"light\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>Replicate the Approach — Pixi Wiki</title><style>{site_css()}</style>{theme_script()}</head><body>
<header class=\"site-header\"><div class=\"header-inner\"><a class=\"logo\" href=\"/pixi-wiki/\">Pixi Wiki</a><nav class=\"nav\"><a href=\"/pixi-wiki/#wikis\">Wikis</a><a href=\"/pixi-wiki/docs/AGENT_SETUP.html\">Agent Setup</a><a href=\"https://github.com/pixiiidust/pixi-wiki\">GitHub</a><button class=\"theme-toggle\" data-theme-toggle type=\"button\">☾</button></nav></div></header>
<main>{body}</main>
<footer class=\"footer\"><div class=\"footer-inner\"><p>Copy the pattern. Keep your source files canonical.</p><p><a href=\"/pixi-wiki/llms.txt\">/llms.txt</a><a href=\"/pixi-wiki/llms-full.txt\">/llms-full.txt</a><a href=\"/pixi-wiki/index.json\">/index.json</a></p></div></footer>
</body></html>"""
    (docs_dir / "REPLICATE_APPROACH.html").write_text(page, encoding="utf-8")


def build(source_dir: Path, output_root: Path, slugs: list[str]) -> None:
    if not source_dir.is_dir():
        raise SystemExit(f"Source namespace directory not found: {source_dir}")
    missing = [slug for slug in slugs if not (source_dir / slug).is_dir()]
    if missing:
        raise SystemExit(f"Missing namespace source dirs: {', '.join(missing)}")

    clean_generated_output(output_root)

    wikis: list[dict[str, Any]] = []
    all_full_sections: list[tuple[str, str]] = []
    llms_parts = [
        "# Pixi Wiki Namespace Registry\n\n",
        "> Pixi Wiki turns my notes, project docs, research, and working context into structured, maintained knowledge bases. Humans browse them like a wiki. Agents read them natively as plain Markdown with llms.txt.\n\n",
        "> Raw Markdown: `/raw/<slug>/<path>`. Human HTML: `/wiki/<slug>/<path>.html`. Namespace agents: `/wiki/<slug>/llms.txt`.\n\n",
    ]
    index_cards: list[str] = []
    top_links: list[str] = []

    for slug in slugs:
        wiki_record, links, full_sections = collect_namespace(source_dir, output_root, slug)
        wikis.append(wiki_record)
        all_full_sections.extend(full_sections)
        title = wiki_record["title"]
        llms_parts.append(f"## {title}\n\n")
        llms_parts.append(f"> {wiki_record['description']}\n")
        llms_parts.append(f"> Current as of: {wiki_record['scope']['currentAs']}\n")
        llms_parts.append(f"> Agent access: [/wiki/{slug}/llms.txt](/wiki/{slug}/llms.txt) [/wiki/{slug}/llms-full.txt](/wiki/{slug}/llms-full.txt) [/wiki/{slug}/index.json](/wiki/{slug}/index.json)\n\n")
        for doc_title, _rel, raw_url, html_url in links:
            llms_parts.append(f"- [{doc_title}]({raw_url}) ([html]({html_url}))\n")
        llms_parts.append("\n")
        top_links.append(f'<a href="/pixi-wiki/wiki/{slug}/README.md.html">{html.escape(str(title))}</a>')
        index_cards.append(
            f'<article class="card" id="{slug}"><h2><a href="/pixi-wiki/wiki/{slug}/README.md.html">{html.escape(str(title))}</a></h2>'
            f'<p>{html.escape(wiki_record["description"])}</p><p class="meta">{wiki_record["documentCount"]} documents · '
            f'{wiki_record["counts"].get("concepts",0)} concepts · {wiki_record["counts"].get("entities",0)} entities · '
            f'<a href="/pixi-wiki/wiki/{slug}/llms.txt">llms.txt</a></p></article>'
        )

    registry = {
        "name": "Pixi Wiki",
        "description": "Clean AgentWikis-style registry generated from pixi-vault namespaces.",
        "schema_version": "pixi-agentwikis-registry-v1",
        "source_repo": "pixiiidust/ObsidianVault",
        "source_path": "wikis/<slug>/",
        "raw_pattern": "/raw/<slug>/<path>",
        "html_pattern": "/wiki/<slug>/<path>.html",
        "namespace_agent_pattern": "/wiki/<slug>/llms.txt",
        "legacy_root_flat_pages": "removed",
        "wikis": wikis,
        "comingSoon": [],
    }
    (output_root / "index.json").write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    (output_root / "llms.txt").write_text("".join(llms_parts).rstrip() + "\n", encoding="utf-8")
    full_body = "\n\n".join(f"<!-- ===== {name} ===== -->\n\n{text}" for name, text in all_full_sections)
    (output_root / "llms-full.txt").write_text(full_body.rstrip() + "\n", encoding="utf-8")
    write_agent_setup_page(output_root)
    write_replicate_page(output_root)

    index_html = f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pixi Wiki</title><style>{site_css()}</style>{theme_script()}</head><body>
<header class="site-header"><div class="header-inner"><a class="logo" href="/pixi-wiki/">Pixi Wiki</a><nav class="nav"><a href="/pixi-wiki/#wikis">Wikis</a><a href="/pixi-wiki/docs/AGENT_SETUP.html">Agent Setup</a><a href="https://github.com/pixiiidust/pixi-wiki">GitHub</a><button class="theme-toggle" data-theme-toggle type="button">☾</button></nav></div></header>
<main style="max-width:1180px;margin:44px auto 90px;padding:0 20px"><h1>Pixi Wiki</h1><p class="hero-copy">Pixi Wiki turns my notes, project docs, research, and working context into structured, maintained knowledge bases. Humans browse them like a wiki. Agents read them natively as plain Markdown with <code>llms.txt</code> and local MCP access.</p><div class="hero-actions"><a class="button-link primary" href="#wikis">Browse wikis</a><a class="button-link" href="/pixi-wiki/docs/AGENT_SETUP.html">Connect agents via MCP</a></div><section class="agent-setup-callout"><h2>Agents start here</h2><pre><code>$ curl https://pixiiidust.github.io/pixi-wiki/llms.txt</code></pre><p>Use <code>llms.txt</code> as the first routing map, then follow links to raw Markdown, namespace files, or MCP setup.</p></section><section id="wikis" class="grid">{''.join(index_cards)}</section></main>
<footer class="footer"><div class="footer-inner"><p>Plain static HTML. No JavaScript is required to read any page — agents welcome.</p><p><a href="/pixi-wiki/llms.txt">/llms.txt</a><a href="/pixi-wiki/llms-full.txt">/llms-full.txt</a><a href="/pixi-wiki/index.json">/index.json</a><a href="https://github.com/pixiiidust/pixi-wiki">GitHub</a><a href="/pixi-wiki/docs/REPLICATE_APPROACH.html">Copy this approach</a></p></div></footer>
</body></html>"""
    (output_root / "index.html").write_text(index_html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="Path to pixi-vault/wikis")
    parser.add_argument("--output", type=Path, default=ROOT, help="Path to pixi-wiki output repo")
    parser.add_argument("--slug", action="append", dest="slugs", help="Namespace slug to include; repeatable")
    args = parser.parse_args()
    build(args.source.resolve(), args.output.resolve(), args.slugs or DEFAULT_SEED_SLUGS)


if __name__ == "__main__":
    main()
