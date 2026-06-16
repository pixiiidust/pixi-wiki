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
[data-theme=dark]{color-scheme:dark;--bg:#06070d;--panel:#0b0c15;--panel2:#10111c;--border:#24263a;--soft:#1a1c2c;--text:#d7e2ff;--muted:#7f87a6;--heading:#fff;--accent:#ffb323;--accent2:#ffd166;--green:#24e693;--header:#080912;--active-bg:#2b2116}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:"IBM Plex Mono","JetBrains Mono","Roboto Mono",ui-monospace,monospace;font-size:14px;line-height:1.7}a{color:var(--accent);text-decoration:none;border-bottom:1px dotted currentColor}a:hover{color:var(--accent2)}code{background:var(--panel2);border:1px solid var(--border);color:var(--accent2);padding:1px 5px;border-radius:4px}pre{background:var(--panel2);border:1px solid var(--border);padding:14px;overflow:auto}.site-header{height:66px;border-bottom:1px solid var(--border);background:var(--header)}.header-inner{max-width:1180px;margin:0 auto;height:100%;display:flex;align-items:center;justify-content:space-between;padding:0 20px}.logo{color:var(--heading);font-weight:800;letter-spacing:.04em;border:0}.nav{display:flex;align-items:center;gap:24px}.nav a{color:var(--muted);border:0;font-size:12px;letter-spacing:.14em;text-transform:uppercase}.nav a:hover{color:var(--heading)}.theme-toggle{border:1px solid var(--border);background:var(--panel);color:var(--text);padding:8px 10px;border-radius:999px;font:inherit;font-size:12px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}.theme-toggle:hover{border-color:var(--accent);color:var(--accent)}.category-bar{border-bottom:1px solid var(--border);background:var(--panel)}.category-inner{max-width:1180px;margin:0 auto;display:flex;gap:22px;min-height:46px;align-items:center;padding:0 20px;flex-wrap:wrap}.category-inner a{color:var(--muted);border:0;font-size:12px;letter-spacing:.12em;text-transform:uppercase}.category-inner a:first-child{color:var(--muted)}.page{max-width:1180px;margin:40px auto 90px;display:grid;grid-template-columns:260px minmax(0,1fr);gap:48px;padding:0 20px}.sidebar{color:var(--muted)}.sidebar-block{border-left:1px solid var(--border);padding-left:12px;margin-bottom:24px}.sidebar-title{color:var(--heading);font-weight:800;margin-bottom:4px}.sidebar-count{color:var(--muted);font-size:11px;margin-bottom:16px}.sidebar a{display:block;padding:6px 10px;color:var(--muted);border:0;font-size:13px}.sidebar a.active{background:var(--active-bg);color:var(--accent);border-left:2px solid var(--accent);margin-left:-13px;padding-left:11px;font-weight:800}.sidebar-section-title{margin:12px 0 6px;color:var(--muted);font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:800}.article{min-width:0}.content-header{display:flex;justify-content:space-between;gap:18px;align-items:baseline;margin-bottom:18px;color:var(--muted);font-size:13px}.breadcrumbs a,.markdown-link{color:var(--accent)}h1{margin:0 0 10px;color:var(--heading);font-size:36px;line-height:1.1;font-weight:900;letter-spacing:-.04em;text-transform:uppercase}h2{margin:48px 0 14px;padding-bottom:10px;border-bottom:1px solid var(--border);color:var(--heading);font-size:22px;line-height:1.2;font-weight:900;text-transform:uppercase}h2::before{content:"// ";color:var(--accent2)}h3{margin:26px 0 8px;color:var(--heading);text-transform:uppercase;font-size:15px;letter-spacing:.08em}.updated{color:var(--muted);font-size:13px;margin-bottom:18px}.info-card{border:1px solid var(--border);background:var(--panel);padding:20px 22px;margin:24px 0}.info-row{display:grid;grid-template-columns:136px 1fr;gap:18px;margin-bottom:12px}.info-row:last-child{margin-bottom:0}.info-label{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:900}.green{color:var(--green)}.yellow{color:var(--accent2)}.white{color:var(--heading)}.agent-card{margin:24px 0 22px;padding:14px 18px;background:var(--active-bg);border:1px solid var(--border);border-left:2px solid var(--accent);color:var(--text)}.agent-card a{font-weight:800;margin-right:12px}.hero-copy{max-width:860px;color:var(--text);font-size:16px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:26px}.card{border:1px solid var(--border);border-radius:14px;padding:18px;background:var(--panel)}.card h2{border:0;margin:0 0 8px;padding:0;font-size:18px}.card h2::before{content:""}.meta{color:var(--muted);font-size:.9rem}.next-card{margin-top:48px;margin-left:auto;width:min(360px,100%);border:1px solid var(--border);border-bottom:1px dotted var(--accent);background:var(--panel);padding:18px 20px;text-align:right;text-decoration:none;display:block}.next-label{display:block;color:var(--muted);font-size:11px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:8px}.next-title{color:var(--heading);font-weight:800}.footer{border-top:1px solid var(--border);background:var(--header);color:var(--muted)}.footer-inner{max-width:1180px;margin:0 auto;padding:28px 20px;display:flex;justify-content:space-between;gap:20px}.footer a{margin-left:12px}@media(max-width:820px){.page{grid-template-columns:1fr}.nav{display:none}.info-row{grid-template-columns:1fr}.footer-inner{display:block}}
"""


def theme_script() -> str:
    return """<script>(function(){const key='pixi-wiki-theme';const root=document.documentElement;const saved=localStorage.getItem(key)||'light';root.dataset.theme=saved;function label(){const b=document.querySelector('[data-theme-toggle]');if(b)b.textContent=root.dataset.theme==='dark'?'☀ Light':'☾ Dark';}document.addEventListener('DOMContentLoaded',function(){label();const b=document.querySelector('[data-theme-toggle]');if(b)b.addEventListener('click',function(){root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';localStorage.setItem(key,root.dataset.theme);label();});});})();</script>"""


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


def make_sidebar(slug: str, title: str, doc_count: int, counts: Counter[str], active_rel: str) -> str:
    def cls(rel: str) -> str:
        return ' class="active"' if rel == active_rel else ""

    rows = [
        f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-title">{html.escape(title)}</div><div class="sidebar-count">{doc_count} documents</div>',
        f'<a{cls("README.md")} href="/pixi-wiki/wiki/{slug}/README.md.html">📄 {html.escape(title)} Knowledge Base</a>',
        f'<a{cls("wiki/index.md")} href="/pixi-wiki/wiki/{slug}/wiki/index.md.html">📄 {html.escape(title)} KB — Master Index</a>',
        f'<div class="sidebar-section-title">WIKI {counts.get("wiki", 0)}</div>',
        f'<div class="sidebar-section-title">CONCEPTS {counts.get("concepts", 0)}</div>',
        f'<div class="sidebar-section-title">ENTITIES {counts.get("entities", 0)}</div>',
        f'<div class="sidebar-section-title">SUMMARIES {counts.get("summaries", 0)}</div>',
        f'<div class="sidebar-section-title">SYNTHESES {counts.get("syntheses", 0)}</div>',
        '</div><div class="sidebar-block"><div class="sidebar-section-title">// FOR AGENTS</div>',
        f'<a href="/pixi-wiki/wiki/{slug}/llms.txt">llms.txt</a>',
        f'<a href="/pixi-wiki/wiki/{slug}/llms-full.txt">llms-full.txt</a>',
        f'<a href="/pixi-wiki/wiki/{slug}/index.json">index.json</a>',
        "</div></aside>",
    ]
    return "\n".join(rows)


def page_shell(slug: str, namespace_title: str, doc_count: int, counts: Counter[str], active_rel: str, article: str, page_title: str) -> str:
    sidebar = make_sidebar(slug, namespace_title, doc_count, counts, active_rel)
    return f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(page_title)} — {html.escape(namespace_title)} — Pixi Wiki</title>
<style>{site_css()}</style>{theme_script()}</head><body>
<header class="site-header"><div class="header-inner"><a class="logo" href="/pixi-wiki/">Pixi Wiki</a><nav class="nav"><a href="/pixi-wiki/">Wikis</a><a href="/pixi-wiki/llms.txt">For Agents</a><a href="/pixi-wiki/index.json">Index JSON</a><button class="theme-toggle" data-theme-toggle type="button">☾ Dark</button></nav></div></header>
<nav class="category-bar"><div class="category-inner"><a>/Namespaces</a><a href="/pixi-wiki/wiki/pixi-vault/README.md.html">Pixi Vault</a><a href="/pixi-wiki/wiki/agent-workflows/README.md.html">Agent Workflows</a><a href="/pixi-wiki/wiki/eval-trace/README.md.html">Eval Trace</a><a href="/pixi-wiki/wiki/ai-native-product-surfaces/README.md.html">AI Product Surfaces</a></div></nav>
<main class="page">{sidebar}<article class="article">{article}</article></main>
<footer class="footer"><div class="footer-inner"><p>Plain static HTML. Humans browse it like a wiki; agents read Markdown through <code>llms.txt</code>.</p><p><a href="/pixi-wiki/llms.txt">/llms.txt</a><a href="/pixi-wiki/llms-full.txt">/llms-full.txt</a><a href="/pixi-wiki/index.json">/index.json</a></p></div></footer>
</body></html>"""


def render_readme(slug: str, title: str, fm: dict[str, Any], body: str, covers: str, not_covered: str, current_as: str) -> str:
    updated = fm.get("updated", "unknown")
    description = first_paragraph(body)
    body_without_title = re.sub(r"^#\s+.+\n", "", body, count=1).strip()
    body_without_scope = strip_scope_section(body_without_title).strip()
    article = f"""
<div class="content-header"><div class="breadcrumbs"><a href="/pixi-wiki/">wikis</a> / <a href="/pixi-wiki/wiki/{slug}/README.md.html">{html.escape(title)}</a> / README.md</div><a class="markdown-link" href="/pixi-wiki/raw/{slug}/README.md">view as markdown</a></div>
<h1>{html.escape(title)} Knowledge Base</h1>
<div class="updated">updated: <strong>{html.escape(str(updated))}</strong></div>
<section class="info-card"><div class="info-row"><div class="info-label green">Covers</div><div>{inline_markdown(covers)}</div></div><div class="info-row"><div class="info-label yellow">Not Covered</div><div>{inline_markdown(not_covered or "Out-of-scope or stale material; verify with source notes and live tools.")}</div></div><div class="info-row"><div class="info-label white">Current As Of</div><div>{html.escape(current_as or str(updated))}</div></div></section>
<div class="agent-card">🤖 Agent access: <a href="/pixi-wiki/wiki/{slug}/llms.txt">/wiki/{slug}/llms.txt</a> <a href="/pixi-wiki/wiki/{slug}/llms-full.txt">/wiki/{slug}/llms-full.txt</a> <a href="/pixi-wiki/wiki/{slug}/index.json">/wiki/{slug}/index.json</a></div>
<p>{inline_markdown(description)}</p>
<h2>Structure</h2><ul><li><code>raw/</code> — raw Markdown provenance mirror for agents and source inspection.</li><li><code>wiki/</code> — synthesized knowledge pages: concepts, entities, summaries, and syntheses.</li><li>Schema and maintenance rules: see <code>CLAUDE.md</code>.</li></ul>
<h2>Usage</h2><ul><li><strong>Add new sources:</strong> update canonical source notes in <code>pixi-vault</code>, then compile into this namespace.</li><li><strong>Ask questions:</strong> agents read this wiki and cite raw/source paths.</li><li><strong>Publish:</strong> regenerate <code>pixi-wiki</code>, run tests, then live-verify raw and HTML routes.</li></ul>
{markdown_fragment(body_without_scope) if body_without_scope else ""}
<a class="next-card" href="/pixi-wiki/wiki/{slug}/wiki/index.md.html"><span class="next-label">Next</span><span class="next-title">{html.escape(title)} KB — Master Index →</span></a>
"""
    return article


def render_page(slug: str, title: str, rel: str, page_title: str, body: str) -> str:
    return f"""
<div class="content-header"><div class="breadcrumbs"><a href="/pixi-wiki/">wikis</a> / <a href="/pixi-wiki/wiki/{slug}/README.md.html">{html.escape(title)}</a> / {html.escape(rel)}</div><a class="markdown-link" href="/pixi-wiki/raw/{slug}/{html.escape(rel)}">view as markdown</a></div>
{markdown_fragment(body)}
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
        counts[category_for(rel, page_fm)] += 1

    links: list[tuple[str, str, str, str]] = []
    full_sections: list[tuple[str, str]] = []
    doc_records: list[dict[str, str]] = []

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
        if rel_posix == "README.md":
            article = render_readme(slug, str(title), fm, readme_body, covers, not_covered, current_as)
        else:
            article = render_page(slug, str(title), rel_posix, str(page_title), body if page_fm else text)
        html_output.write_text(page_shell(slug, str(title), len(md_files), counts, rel_posix, article, str(page_title)), encoding="utf-8")
        raw_url = f"/raw/{slug}/{rel_posix}"
        html_url = f"/wiki/{slug}/{rel_posix}.html"
        links.append((str(page_title), rel_posix, raw_url, html_url))
        full_sections.append((f"{slug}/{rel_posix}", text))
        doc_records.append({"title": str(page_title), "path": rel_posix, "raw": raw_url, "html": html_url, "category": category_for(rel, page_fm)})

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
        "> Agent Wikis compiles messy, fast-moving sources — repos, changelogs, video transcripts, community Q&A — into structured, maintained knowledge bases. Humans browse them like a wiki. Agents read them natively as plain Markdown with llms.txt.\n\n",
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

    index_html = f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pixi Wiki</title><style>{site_css()}</style>{theme_script()}</head><body>
<header class="site-header"><div class="header-inner"><a class="logo" href="/pixi-wiki/">Pixi Wiki</a><nav class="nav"><a href="/pixi-wiki/">Wikis</a><a href="/pixi-wiki/llms.txt">For Agents</a><a href="/pixi-wiki/index.json">Index JSON</a><button class="theme-toggle" data-theme-toggle type="button">☾ Dark</button></nav></div></header>
<nav class="category-bar"><div class="category-inner"><a>/Namespaces</a>{''.join(top_links)}</div></nav>
<main style="max-width:1180px;margin:44px auto 90px;padding:0 20px"><h1>Pixi Wiki</h1><p class="hero-copy">Agent Wikis compiles messy, fast-moving sources — repos, changelogs, video transcripts, community Q&A — into structured, maintained knowledge bases. Humans browse them like a wiki. Agents read them natively as plain Markdown with <code>llms.txt</code>.</p><p><a href="/pixi-wiki/llms.txt">llms.txt</a> · <a href="/pixi-wiki/llms-full.txt">llms-full.txt</a> · <a href="/pixi-wiki/index.json">index.json</a></p><section class="grid">{''.join(index_cards)}</section></main>
<footer class="footer"><div class="footer-inner"><p>Plain static HTML. No JavaScript is required to read any page — agents welcome.</p><p><a href="/pixi-wiki/llms.txt">/llms.txt</a><a href="/pixi-wiki/llms-full.txt">/llms-full.txt</a><a href="/pixi-wiki/index.json">/index.json</a></p></div></footer>
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
