#!/usr/bin/env python3
"""Build a clean AgentWikis-style public mirror from pixi-vault namespaces.

Source truth lives in `pixi-vault/wikis/<slug>/`. This repo is derived output:
root registry files, raw Markdown mirrors, rendered HTML namespace pages, and
namespace-local agent entrypoints.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from collections import Counter
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote_plus, urlparse

try:  # Runs both as `python scripts/...` (scripts/ on path) and as `scripts.*` import.
    from scripts.markdown_meta import first_heading, first_paragraph, parse_frontmatter
except ImportError:  # pragma: no cover - direct-script execution fallback
    from markdown_meta import first_heading, first_paragraph, parse_frontmatter

ROOT = Path(__file__).resolve().parents[1]
# The author's own vault path. Replicators of this repo must pass their own
# ``--source``; this default only serves the canonical pixi-wiki build.
DEFAULT_SOURCE = Path("/root/ObsidianVault/wikis")
# Default deployment coordinates for the canonical site. ``--base-path`` and
# ``--site-origin`` override them so one generator can drive a differently named
# GitHub Pages project site or a user/org root site.
DEFAULT_BASE_PATH = "/pixi-wiki"
DEFAULT_SITE_ORIGIN = "https://pixiiidust.github.io"
DEFAULT_SEED_SLUGS = [
    "pixi-vault",
    "agent-workflows",
    "eval-trace",
    "hermes-agent",
    "ai-native-product-surfaces",
    "rl-sim-labs",
    "curated-tuning-datasets",
    "local-ai-infrastructure",
    "pattern-language",
    "software-architecture-metapatterns",
    "ui-patterns",
]
GENERATED_ROOT_FILES = ["404.html", "index.html", "index.json", "llms.txt", "llms-full.txt", "recent.html", "recent.json", "search.html", "site.css", "sitemap.xml", "updates.html", "updates.json"]

# Live deployment coordinates, set per build call from ``build()`` (normalized)
# so every f-string template reads the active values. ``BASE_PATH`` is the
# site-root-relative prefix ("" for a root site) that every HTML chrome href,
# canonical/OG URL, sitemap ``<loc>``, stylesheet link, ``data-registry``, and
# report-a-mistake URL carries. Registry values in index.json/llms.txt stay
# site-root-relative and never gain this prefix. Canonical URL = SITE_ORIGIN +
# BASE_PATH + <path>.
BASE_PATH = DEFAULT_BASE_PATH
SITE_ORIGIN = DEFAULT_SITE_ORIGIN
SITE_NAME = "Pixi Wiki"


def normalize_base_path(base_path: str) -> str:
    """Validate/normalize a base path: strip trailing '/'; require '' or a leading '/'."""
    normalized = base_path.rstrip("/")
    if normalized and not normalized.startswith("/"):
        raise SystemExit(
            f"--base-path must be empty or start with '/': {base_path!r}"
        )
    return normalized

# Static SEO descriptions for the non-document chrome pages.
HOME_DESCRIPTION = "Pixi Wiki turns notes, project docs, research, and working context into structured, maintained knowledge bases. Humans browse them like a wiki; agents read them as Markdown with llms.txt and MCP."
UPDATES_DESCRIPTION = "Browse every updated page across every Pixi Wiki namespace, grouped by the date recorded in each page's frontmatter, indexed by month and filterable by time range."
AGENT_SETUP_DESCRIPTION = "Connect AI agents to Pixi Wiki so they can list, search, and read the same Markdown knowledge bases behind the human wiki."
REPLICATE_DESCRIPTION = "Use Pixi Wiki as a reusable pattern for turning your own Markdown notes, research, docs, or vault into a human wiki plus agent-readable context layer."
SIGNAL_GRAPH_DESCRIPTION = "A local analysis sidecar for mapping Pixi Wiki's Markdown corpus before edits, fit-checks, and agent orientation."
SEARCH_DESCRIPTION = "Search across every Pixi Wiki namespace by title, path, category, and namespace. Results are ranked by relevance and highlighted; agents can retrieve the same corpus through llms.txt and index.json."
LEGACY_ROOT_PATTERNS = ["concept-*.html", "projects-*.html", "knowledge.html", "projects.html", "maps-of-content.html", "root.html"]
GENERATED_DIRS = ["raw", "wiki", "agent", "legacy", "updates"]
CONTENT_DIRS = {"concepts", "entities", "summaries", "syntheses"}

# Updates page/feed: surface every qualifying page (no cap) and only accept
# frontmatter `updated` values that are strict day-granular ISO dates. Everything
# about the ordering is derived from those strings (never today's clock) so an
# unchanged input rebuilds byte-identically.
UPDATE_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Soft per-page entry cap for the paginated Updates surface. Whole date sections
# are accumulated onto a page until its running entry total reaches this target,
# then a new page starts; a date section is never split, so a single heavy import
# day simply becomes one oversized page. Pure function of the data — no clock.
UPDATES_PAGE_ENTRY_TARGET = 60


def sort_update_entries(entries: list[dict[str, str]]) -> list[dict[str, str]]:
    """Order update entries by (date DESC, namespace ASC, title ASC).

    Dates are strict ``YYYY-MM-DD`` strings, so negating each numeric component
    yields a stable, clock-free descending-by-date ordering with ascending
    namespace/title tie-breaks.
    """

    def key(entry: dict[str, str]) -> tuple[int, int, int, str, str]:
        year, month, day = entry["updated"].split("-")
        return (-int(year), -int(month), -int(day), entry["namespace"], entry["title"])

    return sorted(entries, key=key)


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^###\s+{re.escape(heading)}\s*$\n\n(.+?)(?=\n###\s+|\n##\s+|\Z)", re.DOTALL | re.MULTILINE | re.IGNORECASE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def strip_scope_section(markdown: str) -> str:
    return re.sub(r"\n## Scope\n\n.*?(?=\n##\s+|\Z)", "\n", markdown, flags=re.DOTALL)


LinkResolver = Callable[[str], str | None]


def inline_markdown(value: str, link_resolver: LinkResolver | None = None) -> str:
    escaped = html.escape(value)

    # Protect code spans first: their contents may contain characters (notably
    # asterisks) that must stay literal and must not be re-processed as emphasis
    # or links. Swap each span for a control-char placeholder token that cannot
    # appear in escaped content, then restore the rendered <code> spans at the end.
    code_spans: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        code_spans.append(f"<code>{match.group(1)}</code>")
        return f"\x00{len(code_spans) - 1}\x00"

    escaped = re.sub(r"`([^`]+)`", stash_code, escaped)

    def replace_wikilink_with_alias(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        label = match.group(2).strip()
        href = link_resolver(target) if link_resolver else None
        if href:
            return f'<a href="{html.escape(href)}">{html.escape(label)}</a>'
        return html.escape(label)

    def replace_wikilink(match: re.Match[str]) -> str:
        target = match.group(1).strip()
        label = target.split("/")[-1]
        href = link_resolver(target) if link_resolver else None
        if href:
            return f'<a href="{html.escape(href)}">{html.escape(label)}</a>'
        return html.escape(label)

    def replace_image(match: re.Match[str]) -> str:
        alt = match.group(1).strip()
        src = match.group(2).strip()
        return f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(alt, quote=True)}" loading="lazy">'

    escaped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", replace_image, escaped)
    escaped = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", replace_wikilink_with_alias, escaped)
    escaped = re.sub(r"\[\[([^\]]+)\]\]", replace_wikilink, escaped)
    escaped = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)

    # Emphasis runs last, but the generated tags must be hidden from it first:
    # an asterisk inside an href plus a lone '*' later in the line would let the
    # em pattern match across the attribute and corrupt the markup. Stash every
    # tag produced above, apply emphasis to plain text only, then restore.
    tags: list[str] = []

    def stash_tag(match: re.Match[str]) -> str:
        tags.append(match.group(0))
        return f"\x01{len(tags) - 1}\x01"

    escaped = re.sub(r"<[^>]+>", stash_tag, escaped)
    escaped = re.sub(r"\*\*([^*]+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*\s][^*]*?)\*(?!\*)", r"<em>\1</em>", escaped)
    escaped = re.sub(r"\x01(\d+)\x01", lambda m: tags[int(m.group(1))], escaped)

    # Restore protected code spans now that emphasis/link passes are done.
    escaped = re.sub(r"\x00(\d+)\x00", lambda m: code_spans[int(m.group(1))], escaped)
    return escaped


def _split_table_row(line: str) -> list[str]:
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [cell.strip() for cell in inner.split("|")]


def _is_table_separator(line: str) -> bool:
    if not line.strip().startswith("|"):
        return False
    cells = _split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-+:?", cell) for cell in cells if cell != "") and any(cell for cell in cells)


def _render_table(rows: list[str], link_resolver: LinkResolver | None = None) -> str:
    def render_row(cells: list[str], tag: str) -> str:
        return "<tr>" + "".join(f"<{tag}>{inline_markdown(cell, link_resolver)}</{tag}>" for cell in cells) + "</tr>"

    if len(rows) >= 2 and _is_table_separator(rows[1]):
        thead = f"<thead>{render_row(_split_table_row(rows[0]), 'th')}</thead>"
        body = "".join(render_row(_split_table_row(r), "td") for r in rows[2:])
        table = f"<table>{thead}<tbody>{body}</tbody></table>"
    else:
        body = "".join(render_row(_split_table_row(r), "td") for r in rows)
        table = f"<table><tbody>{body}</tbody></table>"
    return f'<div class="table-wrap">{table}</div>'


def heading_plain_text(text: str) -> str:
    """Reduce raw heading Markdown to plain words for slug/label derivation.

    Wikilinks and links collapse to their visible label; backticks and
    emphasis/strikethrough markers are dropped. No HTML escaping happens here.
    """
    plain = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", lambda m: m.group(2), text)
    plain = re.sub(r"\[\[([^\]]+)\]\]", lambda m: m.group(1).split("/")[-1], plain)
    plain = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1), plain)
    plain = plain.replace("`", "")
    plain = re.sub(r"[*_~]", "", plain)
    return plain.strip()


def slugify_heading(text: str) -> str:
    """Slug from RAW heading text: strip markup, lowercase, non-alnum -> '-'."""
    slug = re.sub(r"[^a-z0-9]+", "-", heading_plain_text(text).lower()).strip("-")
    return slug or "section"


def markdown_fragment(markdown: str, link_resolver: LinkResolver | None = None) -> str:
    return markdown_fragment_with_headings(markdown, link_resolver)[0]


def markdown_fragment_with_headings(
    markdown: str, link_resolver: LinkResolver | None = None
) -> tuple[str, list[dict[str, Any]]]:
    """Render a Markdown block fragment, returning HTML plus emitted headings.

    Each emitted h1/h2/h3 gets a stable ``id`` slugged from its raw text and a
    trailing hover anchor link. Duplicate slugs within this single call get
    deterministic ``-2``/``-3`` suffixes (document order); dedup state is local,
    so the same input always yields the same ids with no cross-page leakage.
    """
    out: list[str] = []
    headings: list[dict[str, Any]] = []
    slug_counts: dict[str, int] = {}
    in_code = False
    code: list[str] = []
    in_ul = False
    in_ol = False

    def unique_slug(base: str) -> str:
        count = slug_counts.get(base, 0) + 1
        slug_counts[base] = count
        return base if count == 1 else f"{base}-{count}"

    def emit_heading(level: int, raw: str) -> None:
        slug = unique_slug(slugify_heading(raw))
        anchor = (
            f'<a class="heading-anchor" href="#{slug}" '
            f'aria-label="Link to this section">¶</a>'
        )
        out.append(
            f'<h{level} id="{slug}">{inline_markdown(raw, link_resolver)}{anchor}</h{level}>'
        )
        headings.append({"level": level, "slug": slug, "text": heading_plain_text(raw)})

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    lines = markdown.splitlines()
    total = len(lines)
    i = 0
    while i < total:
        stripped = lines[i].rstrip()
        content = stripped.strip()
        if content.startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code = []
                in_code = False
            else:
                close_lists()
                in_code = True
            i += 1
            continue
        if in_code:
            code.append(stripped)
            i += 1
            continue
        if not content:
            close_lists()
            i += 1
            continue
        if content.startswith("|"):
            close_lists()
            table_rows: list[str] = []
            while i < total and lines[i].strip().startswith("|"):
                table_rows.append(lines[i].strip())
                i += 1
            out.append(_render_table(table_rows, link_resolver))
            continue
        if content.startswith(">"):
            close_lists()
            quote_parts: list[str] = []
            while i < total and lines[i].strip().startswith(">"):
                quote_parts.append(inline_markdown(lines[i].strip()[1:].lstrip(), link_resolver))
                i += 1
            out.append("<blockquote>" + "<br>".join(quote_parts) + "</blockquote>")
            continue
        if content.startswith("# "):
            close_lists()
            emit_heading(1, content[2:].strip())
        elif content.startswith("## "):
            close_lists()
            emit_heading(2, content[3:].strip())
        elif content.startswith("### "):
            close_lists()
            emit_heading(3, content[4:].strip())
        elif content.startswith("- "):
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_markdown(content[2:].strip(), link_resolver)}</li>")
        elif re.match(r"^\d+[.)] ", content):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            item = re.sub(r"^\d+[.)] ", "", content, count=1)
            out.append(f"<li>{inline_markdown(item.strip(), link_resolver)}</li>")
        else:
            close_lists()
            out.append(f"<p>{inline_markdown(content, link_resolver)}</p>")
        i += 1
    close_lists()
    return "\n".join(out), headings


def site_css() -> str:
    return """
:root{color-scheme:light;--bg:#f7f3ea;--panel:#fffaf1;--panel2:#f0e8d8;--border:#d9cdb8;--soft:#eadfcb;--text:#22202a;--muted:#6f6a77;--heading:#111018;--accent:#9b5c00;--accent2:#6f4200;--green:#087a4a;--header:#fffdf8;--active-bg:#fff1d1}
[data-theme=dark]{color-scheme:dark;--bg:#0d1117;--panel:#161b22;--panel2:#21262d;--border:#30363d;--soft:#21262d;--text:#e6edf3;--muted:#8b949e;--heading:#f0f6fc;--accent:#58a6ff;--accent2:#79c0ff;--green:#3fb950;--header:#010409;--active-bg:#1f6feb33}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:"IBM Plex Mono","JetBrains Mono","Roboto Mono",ui-monospace,monospace;font-size:14px;line-height:1.7}a{color:var(--accent);text-decoration:none;border-bottom:1px dotted currentColor}a:hover{color:var(--accent2)}code{background:var(--panel2);border:1px solid var(--border);color:var(--accent2);padding:1px 5px;border-radius:4px}pre{background:var(--panel2);border:1px solid var(--border);padding:14px;overflow:auto}.table-wrap{overflow-x:auto;margin:20px 0;border:1px solid var(--border)}table{border-collapse:collapse;width:100%;font-size:13px}th,td{border:1px solid var(--border);padding:8px 12px;text-align:left;vertical-align:top}thead th{background:var(--panel2);color:var(--heading);font-weight:800;letter-spacing:.04em;text-transform:uppercase;font-size:12px}.article img{max-width:100%;height:auto;display:block;margin:18px auto;border:1px solid var(--border);border-radius:8px;background:var(--panel)}.site-header{height:66px;border-bottom:1px solid var(--border);background:var(--header)}.header-inner{max-width:1180px;margin:0 auto;height:100%;display:flex;align-items:center;justify-content:space-between;padding:0 20px}.logo{color:var(--heading);font-weight:800;letter-spacing:.04em;border:0}.header-nav{display:flex;align-items:center;gap:24px}.nav{display:flex;align-items:center;gap:24px}.nav a{color:var(--muted);border:0;font-size:12px;letter-spacing:.14em;text-transform:uppercase}.nav a:hover{color:var(--heading)}.nav-menu{display:none;position:relative}.nav-menu summary{list-style:none;cursor:pointer;color:var(--muted);border:1px solid var(--border);background:var(--panel);padding:8px 12px;border-radius:999px;font-size:12px;letter-spacing:.14em;text-transform:uppercase}.nav-menu summary::-webkit-details-marker{display:none}.nav-menu summary::before{content:"≡";margin-right:8px;color:var(--accent)}.nav-menu summary:hover{border-color:var(--accent);color:var(--accent)}.nav-panel{position:absolute;right:0;top:calc(100% + 10px);z-index:30;display:flex;flex-direction:column;gap:2px;min-width:190px;padding:10px;background:var(--panel);border:1px solid var(--border);border-radius:10px}.nav-panel a{color:var(--muted);border:0;font-size:12px;letter-spacing:.14em;text-transform:uppercase;padding:8px 10px;border-radius:6px}.nav-panel a:hover{color:var(--heading);background:var(--panel2)}.theme-toggle{border:1px solid var(--border);background:var(--panel);color:var(--text);padding:8px 10px;border-radius:999px;font:inherit;font-size:12px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}.theme-toggle:hover{border-color:var(--accent);color:var(--accent)}.category-bar{border-bottom:1px solid var(--border);background:var(--panel)}.category-inner{max-width:1180px;margin:0 auto;display:flex;gap:22px;min-height:46px;align-items:center;padding:0 20px;flex-wrap:wrap}.category-inner a{color:var(--muted);border:0;font-size:12px;letter-spacing:.12em;text-transform:uppercase}.category-inner a:first-child{color:var(--muted)}.page{max-width:1180px;margin:40px auto 90px;display:grid;grid-template-columns:260px minmax(0,1fr);gap:48px;padding:0 20px}.sidebar{color:var(--muted)}.sidebar-block{border-left:1px solid var(--border);padding-left:12px;margin-bottom:24px}.sidebar-title{color:var(--heading);font-weight:800;margin-bottom:4px}.sidebar-count{color:var(--muted);font-size:11px;margin-bottom:16px}.sidebar a{display:block;padding:6px 10px;color:var(--muted);border:0;font-size:13px}.sidebar a.active{background:var(--active-bg);color:var(--accent2);border-left:2px solid var(--accent);margin-left:-13px;padding-left:11px;font-weight:800}.sidebar-section-title{margin:12px 0 6px;color:var(--muted);font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:800}.sidebar-section{margin:10px 0}.sidebar-section summary{list-style:none;cursor:pointer;color:var(--muted);font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:800;padding:6px 10px;border-radius:8px}.sidebar-section summary::-webkit-details-marker{display:none}.sidebar-section summary::before{content:"▸";display:inline-block;width:14px;color:var(--accent);transition:transform .12s ease}.sidebar-section[open] summary::before{transform:rotate(90deg)}.sidebar-section summary:hover{background:var(--panel2);color:var(--heading)}.sidebar-section-body{margin:2px 0 6px 12px;border-left:1px solid var(--border);padding-left:4px}.sidebar-empty{padding:6px 10px;color:var(--muted);font-size:12px;font-style:italic}.article{min-width:0}.content-header{display:flex;justify-content:space-between;gap:18px;align-items:baseline;margin-bottom:18px;color:var(--muted);font-size:13px}.breadcrumbs a,.markdown-link{color:var(--accent)}h1{margin:0 0 10px;color:var(--heading);font-size:36px;line-height:1.1;font-weight:900;letter-spacing:-.04em;text-transform:uppercase}h2{margin:48px 0 14px;padding-bottom:10px;border-bottom:1px solid var(--border);color:var(--heading);font-size:22px;line-height:1.2;font-weight:900;text-transform:uppercase}h2::before{content:"// ";color:var(--accent2)}h3{margin:26px 0 8px;color:var(--heading);text-transform:uppercase;font-size:15px;letter-spacing:.08em}.updated{color:var(--muted);font-size:13px;margin-bottom:18px}.info-card{border:1px solid var(--border);background:var(--panel);padding:20px 22px;margin:24px 0}.info-row{display:grid;grid-template-columns:136px 1fr;gap:18px;margin-bottom:12px}.info-row:last-child{margin-bottom:0}.info-label{font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:900}.green{color:var(--green)}.yellow{color:var(--accent2)}.white{color:var(--heading)}.agent-card{margin:24px 0 22px;padding:14px 18px;background:var(--active-bg);border:1px solid var(--border);border-left:2px solid var(--accent);color:var(--text)}.agent-card a{font-weight:800;margin-right:12px}.hero-copy{max-width:860px;color:var(--text);font-size:16px}.hero-actions{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0 18px}.button-link{display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--border);border-radius:999px;padding:9px 14px;background:var(--panel);color:var(--heading);font-weight:800;font-size:12px;letter-spacing:.08em;text-transform:uppercase}.button-link.primary{background:var(--active-bg);border-color:var(--accent);color:var(--accent2)}.button-link:hover{border-color:var(--accent);color:var(--accent2)}.agent-setup-callout{max-width:860px;margin:18px 0 34px;padding:16px 18px;background:var(--panel);border:1px solid var(--border);border-left:2px solid var(--accent)}.agent-setup-callout h2{font-size:16px;margin:0 0 6px;padding:0;border:0}.agent-setup-callout h2::before{content:""}.agent-setup-callout p{margin:0;color:var(--muted)}.wiki-nav{display:flex;flex-wrap:wrap;gap:10px;margin:28px 0 8px}.wiki-group{margin-top:34px;padding-top:8px}.group-header{max-width:760px;border-left:3px solid var(--active-bg);padding-left:14px;margin-bottom:14px}.group-header h2{margin:2px 0 4px}.group-header p{margin:0;color:var(--muted)}.eyebrow{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent2)!important;font-weight:800}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-top:18px}.card{border:1px solid var(--border);border-radius:14px;padding:18px;background:var(--panel)}.card h2{border:0;margin:0 0 8px;padding:0;font-size:18px}.card h2::before{content:""}.meta{color:var(--muted);font-size:.9rem}.page-meta{display:flex;flex-wrap:wrap;gap:6px 16px;margin:8px 0 22px;color:var(--muted);font-size:13px}.page-meta span{color:var(--heading);font-weight:800}.page-tools{display:flex;gap:12px;flex-wrap:wrap;justify-content:flex-end}.prev-next{margin-top:54px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.prev-next-card{border:1px solid var(--border);border-bottom:1px dotted var(--accent);background:var(--panel);padding:18px 20px;text-decoration:none;display:block}.prev-card{text-align:left}.next-card{text-align:right}.next-label{display:block;color:var(--muted);font-size:11px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:8px}.next-title{color:var(--heading);font-weight:800}.footer{border-top:1px solid var(--border);background:var(--header);color:var(--muted)}.footer-inner{max-width:1180px;margin:0 auto;padding:28px 20px;display:flex;justify-content:space-between;gap:20px}.footer a{margin-left:12px}@media(max-width:820px){.page{grid-template-columns:1fr}.article{order:1}.sidebar{order:2}.nav{display:none}.nav-menu{display:block}.info-row{grid-template-columns:1fr}.footer-inner{display:block}}
.heading-anchor{margin-left:.4em;color:var(--muted);border:0;font-weight:400;opacity:0;transition:opacity .12s ease}h1:hover .heading-anchor,h2:hover .heading-anchor,h3:hover .heading-anchor,.heading-anchor:focus{opacity:1}.heading-anchor:hover{color:var(--accent)}
.page-toc{border-left:2px solid var(--border);padding:2px 0 2px 16px;margin:0 0 32px}.page-toc-title{color:var(--muted);font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:800;margin-bottom:8px}.page-toc ul{list-style:none;margin:0;padding:0}.page-toc li{margin:4px 0}.page-toc a{color:var(--muted);border:0;font-size:13px}.page-toc a:hover{color:var(--accent)}.page-toc-h3{padding-left:16px}.page-toc-h3 a{color:var(--muted);font-size:12px}
.sidebar-subgroup{margin:2px 0}.sidebar-subgroup summary{list-style:none;cursor:pointer;color:var(--muted);font-size:11px;letter-spacing:.14em;text-transform:uppercase;font-weight:800;padding:4px 10px;border-radius:8px}.sidebar-subgroup summary::-webkit-details-marker{display:none}.sidebar-subgroup summary::before{content:"▸";display:inline-block;width:14px;color:var(--accent2);transition:transform .12s ease}.sidebar-subgroup[open] summary::before{transform:rotate(90deg)}.sidebar-subgroup summary:hover{background:var(--panel2);color:var(--heading)}.sidebar-filter{display:block;width:100%;margin:2px 0 6px;padding:6px 10px;background:var(--panel);border:1px solid var(--border);border-radius:8px;color:var(--text);font:inherit;font-size:12px}.sidebar-filter:focus{outline:none;border-color:var(--accent)}
.recent-group{margin-top:34px}.recent-list{list-style:none;margin:14px 0 0;padding:0}.recent-item{display:flex;flex-wrap:wrap;align-items:baseline;gap:12px;padding:9px 0;border-bottom:1px solid var(--border)}.recent-title{font-weight:800;border-bottom:1px dotted currentColor}.namespace-badge{border:1px solid var(--border);background:var(--panel2);color:var(--accent2);border-radius:999px;padding:2px 10px;font-size:11px;letter-spacing:.08em;text-transform:uppercase}.recent-raw{color:var(--muted);font-size:12px}
.site-search{position:relative;flex:1 1 auto;max-width:420px;margin:0 24px}.search-input{width:100%;padding:8px 16px;background:var(--panel);border:1px solid var(--border);border-radius:999px;color:var(--text);font:inherit;font-size:13px;letter-spacing:.02em}.search-input::placeholder{color:var(--muted);letter-spacing:.08em;text-transform:uppercase;font-size:11px}.search-input:focus{outline:none;border-color:var(--accent)}.search-results{position:absolute;left:0;right:0;top:calc(100% + 10px);z-index:40;max-height:64vh;overflow-y:auto;display:flex;flex-direction:column;gap:2px;padding:8px;background:var(--panel);border:1px solid var(--border);border-radius:10px}.search-result{display:flex;align-items:baseline;justify-content:space-between;gap:12px;padding:8px 10px;border:0;border-radius:6px;color:var(--muted)}.search-result:hover,.search-result.active{background:var(--panel2);color:var(--heading)}.search-result-title{color:var(--heading);font-weight:800}.search-badge{border:1px solid var(--border);background:var(--panel2);color:var(--accent2);border-radius:999px;padding:2px 9px;font-size:10px;letter-spacing:.1em;text-transform:uppercase;white-space:nowrap;flex:0 0 auto}.search-empty{padding:8px 10px;color:var(--muted);font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-style:italic}.search-results[hidden]{display:none}@media(max-width:820px){.site-search{max-width:190px;margin:0 12px}}
.skip-link{position:absolute;width:1px;height:1px;padding:0;margin:0;overflow:hidden;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;border:0}.skip-link:focus{position:fixed;top:12px;left:12px;width:auto;height:auto;padding:8px 14px;clip:auto;clip-path:none;background:var(--accent);color:var(--header);border-radius:999px;z-index:100;font-size:12px;letter-spacing:.08em;text-transform:uppercase;font-weight:800}
pre{position:relative}.copy-button{position:absolute;top:8px;right:8px;padding:4px 10px;background:var(--panel);color:var(--muted);border:1px solid var(--border);border-radius:6px;font:inherit;font-size:11px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}.copy-button:hover,.copy-button:focus{border-color:var(--accent);color:var(--accent)}
.updates-filter{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 6px}.updates-chip{border:1px solid var(--border);background:var(--panel);color:var(--muted);border-radius:999px;padding:6px 14px;font:inherit;font-size:12px;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}.updates-chip:hover{border-color:var(--accent);color:var(--accent)}.updates-chip[aria-pressed=true]{background:var(--active-bg);border-color:var(--accent);color:var(--accent2);font-weight:800}.updates-empty{width:100%;padding:8px 2px;color:var(--muted);font-size:12px;letter-spacing:.06em;text-transform:uppercase;font-style:italic}.updates-months{display:flex;flex-wrap:wrap;gap:6px 10px;margin:14px 0 6px;color:var(--muted);font-size:12px;letter-spacing:.06em}.updates-months a{color:var(--muted);border:0}.updates-months a:hover{color:var(--accent)}.updates-month-anchor{display:block;height:0;overflow:hidden}.updates-group{margin-top:34px}.updates-group[hidden]{display:none}.updates-ns{margin:10px 0}.updates-ns summary{list-style:none;cursor:pointer;color:var(--heading);font-weight:800;font-size:13px;letter-spacing:.04em;padding:6px 0}.updates-ns summary::-webkit-details-marker{display:none}.updates-ns summary::before{content:"▸";display:inline-block;width:16px;color:var(--accent);transition:transform .12s ease}.updates-ns[open] summary::before{transform:rotate(90deg)}.updates-list{list-style:none;margin:4px 0 0;padding:0 0 0 16px}.updates-item{display:flex;flex-wrap:wrap;align-items:baseline;gap:12px;padding:8px 0;border-bottom:1px solid var(--border)}.updates-title{font-weight:800;border-bottom:1px dotted currentColor}.updates-raw{color:var(--muted);font-size:12px}
.pagination{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:54px 0 0;padding-top:24px;border-top:1px solid var(--border)}.pagination a,.pagination span{border:1px solid var(--border);background:var(--panel);color:var(--muted);border-radius:999px;padding:7px 13px;font-size:12px;letter-spacing:.06em;min-width:38px;text-align:center}.pagination a{text-decoration:none}.pagination a:hover{border-color:var(--accent);color:var(--accent)}.pagination .pagination-current{background:var(--active-bg);border-color:var(--accent);color:var(--accent2);font-weight:800}.pagination .pagination-ellipsis{border:0;background:transparent;color:var(--muted);min-width:auto;padding:7px 4px}.pagination-prev,.pagination-next{text-transform:uppercase;letter-spacing:.1em}
.search-page{margin:26px 0 0}.search-page-form{margin:0}.search-page-label{display:block;color:var(--muted);font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:800;margin-bottom:8px}.search-page-input{width:100%;max-width:640px;padding:12px 20px;background:var(--panel);border:1px solid var(--border);border-radius:999px;color:var(--text);font:inherit;font-size:15px}.search-page-input:focus{outline:none;border-color:var(--accent)}.search-page-results{margin-top:20px}.search-count{color:var(--muted);font-size:13px;letter-spacing:.04em;margin:6px 0 14px}.search-list{display:flex;flex-direction:column}.search-result-row{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px;padding:12px 2px;border:0;border-bottom:1px solid var(--border);color:var(--muted)}.search-result-row:hover{color:var(--heading)}.search-result-row .search-result-title{color:var(--heading);font-weight:800}.search-result-meta{color:var(--muted);font-size:12px;width:100%}.search-page-results mark{background:var(--active-bg);color:var(--accent2);border-radius:3px;padding:0 2px}.search-pagination{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:26px 0 0}.search-pagination-item{border:1px solid var(--border);background:var(--panel);color:var(--muted);border-radius:8px;padding:6px 12px;font:inherit;font-size:12px;letter-spacing:.06em;cursor:pointer}.search-pagination-item:hover:not(:disabled){border-color:var(--accent);color:var(--accent)}.search-pagination-item:disabled{opacity:.4;cursor:default}.search-pagination-current{background:var(--active-bg);border-color:var(--accent);color:var(--accent2);font-weight:800}.search-see-all{justify-content:center;color:var(--accent2)!important;font-weight:800}
"""

# Content hash of the shared stylesheet, computed once at import time. Every
# ``<link rel="stylesheet">`` carries it as a ``?v=<hash>`` cache-buster so a CSS
# fix invalidates the browser cache immediately instead of waiting out the old
# cache lifetime. Pure content hash → deterministic across rebuilds.
SITE_CSS_HASH = hashlib.sha256(site_css().encode("utf-8")).hexdigest()[:8]


def stylesheet_link() -> str:
    """Return the shared-stylesheet ``<link>`` with a content-hash cache-buster."""
    return f'<link rel="stylesheet" href="{BASE_PATH}/site.css?v={SITE_CSS_HASH}">'


def theme_script() -> str:
    return """<script>(function(){const key='pixi-wiki-theme';const root=document.documentElement;const saved=localStorage.getItem(key)||'light';root.dataset.theme=saved;function label(){const b=document.querySelector('[data-theme-toggle]');if(b)b.textContent=root.dataset.theme==='dark'?'☀':'☾';}document.addEventListener('DOMContentLoaded',function(){label();const b=document.querySelector('[data-theme-toggle]');if(b)b.addEventListener('click',function(){root.dataset.theme=root.dataset.theme==='dark'?'light':'dark';localStorage.setItem(key,root.dataset.theme);label();});});})();</script>"""


def sidebar_filter_script() -> str:
    """Progressive-enhancement filter for large sidebar sections.

    Wires every ``.sidebar-filter`` input: typing hides links whose text does
    not contain the query (case-insensitive) and auto-opens subgroups so
    matches deeper in the tree stay visible; clearing restores the original
    view. Without JavaScript the input is inert and the full list renders.
    """
    return """<script>document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('.sidebar-filter').forEach(function(input){var section=input.closest('.sidebar-section');if(!section)return;var links=[].slice.call(section.querySelectorAll('a'));var groups=[].slice.call(section.querySelectorAll('.sidebar-subgroup'));var opened=groups.map(function(g){return g.open;});input.addEventListener('input',function(){var q=input.value.trim().toLowerCase();links.forEach(function(a){a.style.display=(!q||a.textContent.toLowerCase().indexOf(q)>-1)?'':'none';});groups.forEach(function(g,i){g.open=q?true:opened[i];});});});});</script>"""


def search_script() -> str:
    """Progressive-enhancement client search over the root registry.

    On DOMContentLoaded this builds a search input plus a hidden results panel
    inside the empty ``.site-search`` placeholder that ``site_header`` emits. The
    237 KB registry named by ``data-registry`` is fetched lazily on the FIRST
    focus/keystroke only (never on page load) and cached; results filter with
    case-insensitive AND-token substring matching. The dropdown renders at most
    ``CAP`` (8) rows and, whenever there are matches, appends a keyboard-reachable
    ``See all N results →`` row linking the dedicated ``search.html`` page.
    Keyboard: ``/`` focuses search from anywhere (unless already typing), Arrow
    keys move the active option, Enter opens the arrow-selected option or (with
    none selected) navigates to the results page for the current query, Escape
    clears/closes, outside clicks close. With JavaScript disabled the placeholder
    stays empty, so the no-JS reading promise holds with zero server-rendered
    search markup.
    """
    return """<script>(function(){document.addEventListener('DOMContentLoaded',function(){var box=document.querySelector('.site-search');if(!box)return;var url=box.getAttribute('data-registry');var base=url.replace(/\\/index\\.json$/,'');var input=document.createElement('input');input.type='search';input.placeholder='Search… ( / )';input.setAttribute('aria-label','Search all pages');input.className='search-input';var panel=document.createElement('div');panel.className='search-results';panel.setAttribute('role','listbox');panel.hidden=true;box.appendChild(input);box.appendChild(panel);var CAP=8;var entries=null,pending=null,loading=false,failed=false,active=-1,rows=[];function flatten(data){var out=[];if(!data||!data.wikis)return out;for(var i=0;i<data.wikis.length;i++){var w=data.wikis[i]||{};var docs=w.documents||[];for(var j=0;j<docs.length;j++){var d=docs[j]||{};out.push({title:String(d.title||d.path||''),path:String(d.path||''),category:String(d.category||''),nsSlug:String(w.slug||''),nsTitle:String(w.title||''),url:String(d.html||'')});}}return out;}function load(cb){if(entries||failed){cb();return;}pending=cb;if(loading)return;loading=true;function done(){loading=false;var p=pending;pending=null;if(p)p();}try{fetch(url).then(function(r){return r.json();}).then(function(data){entries=flatten(data);done();}).catch(function(){failed=true;done();});}catch(e){failed=true;done();}}function filter(q){var tokens=q.toLowerCase().split(/\\s+/).filter(Boolean);if(!tokens.length)return [];var res=[];for(var i=0;i<entries.length;i++){var e=entries[i];var hay=(e.title+' '+e.path+' '+e.category+' '+e.nsSlug+' '+e.nsTitle).toLowerCase();var ok=true;for(var t=0;t<tokens.length;t++){if(hay.indexOf(tokens[t])<0){ok=false;break;}}if(ok)res.push(e);}return res;}function close(){panel.hidden=true;panel.innerHTML='';rows=[];active=-1;}function render(list,q){panel.innerHTML='';rows=[];active=-1;if(failed){var f=document.createElement('div');f.className='search-empty';f.textContent='Search unavailable';panel.appendChild(f);panel.hidden=false;return;}if(!list.length){var n=document.createElement('div');n.className='search-empty';n.textContent='No matches';panel.appendChild(n);panel.hidden=false;return;}for(var i=0;i<list.length&&i<CAP;i++){var e=list[i];var a=document.createElement('a');a.className='search-result';a.setAttribute('role','option');a.setAttribute('aria-selected','false');a.href=base+e.url;var ttl=document.createElement('span');ttl.className='search-result-title';ttl.textContent=e.title;a.appendChild(ttl);var badge=document.createElement('span');badge.className='search-badge';badge.textContent=e.nsTitle||e.nsSlug;a.appendChild(badge);panel.appendChild(a);rows.push(a);}var see=document.createElement('a');see.className='search-result search-see-all';see.setAttribute('role','option');see.setAttribute('aria-selected','false');see.href=base+'/search.html?q='+encodeURIComponent(q);see.textContent='See all '+list.length+' results →';panel.appendChild(see);rows.push(see);panel.hidden=false;}function update(){var q=input.value.trim();if(!q){close();return;}load(function(){if(failed){render([],q);return;}if(!entries)return;render(filter(q),q);});}function setActive(i){if(!rows.length)return;if(active>=0&&rows[active]){rows[active].classList.remove('active');rows[active].setAttribute('aria-selected','false');}active=(i+rows.length)%rows.length;rows[active].classList.add('active');rows[active].setAttribute('aria-selected','true');if(rows[active].scrollIntoView)rows[active].scrollIntoView({block:'nearest'});}input.addEventListener('focus',function(){load(function(){});});input.addEventListener('input',update);input.addEventListener('keydown',function(ev){if(ev.key==='ArrowDown'){ev.preventDefault();setActive(active+1);}else if(ev.key==='ArrowUp'){ev.preventDefault();setActive(active-1);}else if(ev.key==='Enter'){ev.preventDefault();if(active>=0&&rows[active]){window.location.href=rows[active].href;}else{var qq=input.value.trim();if(qq)window.location.href=base+'/search.html?q='+encodeURIComponent(qq);}}else if(ev.key==='Escape'){input.value='';close();input.blur();}});document.addEventListener('keydown',function(ev){if(ev.key!=='/')return;var el=document.activeElement;var tag=el&&el.tagName?el.tagName.toLowerCase():'';if(tag==='input'||tag==='textarea'||(el&&el.isContentEditable))return;ev.preventDefault();input.focus();});document.addEventListener('click',function(ev){if(!box.contains(ev.target))panel.hidden=true;});});})();</script>"""


def search_page_script() -> str:
    """Full-page client search results, injected only on ``search.html``.

    On DOMContentLoaded this reads ``q`` and ``page`` from the URL query
    (``URLSearchParams``), builds a labelled query input plus a live results
    region inside the empty ``.search-page`` placeholder, and lazily fetches the
    same registry the header dropdown uses (``data-registry``). Matching is the
    identical case-insensitive AND-token substring rule; results are RANKED by
    ``3×(token hits in the title) + 1×(token hits in path/category/namespace)``
    then title ASC, with matched tokens wrapped in ``<mark>`` via DOM text nodes
    (never innerHTML with user input). Results paginate at 20/page with
    ``search-pagination`` controls, and the active ``q``/``page`` is mirrored to
    the URL via ``history.replaceState``. Typing re-runs the search debounced
    (~150ms) and resets to page 1. With JavaScript disabled the placeholder stays
    empty and the page's ``<noscript>`` block points at the Markdown entrypoints.
    """
    return """<script>(function(){document.addEventListener('DOMContentLoaded',function(){var box=document.querySelector('.search-page');if(!box)return;var url=box.getAttribute('data-registry');var base=url.replace(/\\/index\\.json$/,'');var params=new URLSearchParams(window.location.search);var rawQ=params.get('q')||'';var page=parseInt(params.get('page'),10);if(!page||page<1)page=1;var q=rawQ.trim();var PER=20;var entries=null,pending=null,loading=false,failed=false,timer=null;var form=document.createElement('form');form.className='search-page-form';form.setAttribute('role','search');var label=document.createElement('label');label.className='search-page-label';label.setAttribute('for','search-page-input');label.textContent='Search all pages';var input=document.createElement('input');input.type='search';input.id='search-page-input';input.className='search-page-input';input.setAttribute('aria-label','Search all pages');input.placeholder='Search all pages…';input.value=rawQ;form.appendChild(label);form.appendChild(input);var region=document.createElement('div');region.className='search-page-results';region.setAttribute('aria-live','polite');box.appendChild(form);box.appendChild(region);function flatten(data){var out=[];if(!data||!data.wikis)return out;for(var i=0;i<data.wikis.length;i++){var w=data.wikis[i]||{};var docs=w.documents||[];for(var j=0;j<docs.length;j++){var d=docs[j]||{};out.push({title:String(d.title||d.path||''),path:String(d.path||''),category:String(d.category||''),nsSlug:String(w.slug||''),nsTitle:String(w.title||''),url:String(d.html||'')});}}return out;}function load(cb){if(entries||failed){cb();return;}pending=cb;if(loading)return;loading=true;function done(){loading=false;var p=pending;pending=null;if(p)p();}try{fetch(url).then(function(r){return r.json();}).then(function(data){entries=flatten(data);done();}).catch(function(){failed=true;done();});}catch(e){failed=true;done();}}function tokenize(s){return s.toLowerCase().split(/\\s+/).filter(Boolean);}function search(tokens){var res=[];for(var i=0;i<entries.length;i++){var e=entries[i];var title=e.title.toLowerCase();var rest=(e.path+' '+e.category+' '+e.nsSlug+' '+e.nsTitle).toLowerCase();var hay=title+' '+rest;var ok=true,score=0;for(var t=0;t<tokens.length;t++){if(hay.indexOf(tokens[t])<0){ok=false;break;}if(title.indexOf(tokens[t])>=0)score+=3;if(rest.indexOf(tokens[t])>=0)score+=1;}if(ok)res.push({e:e,score:score});}res.sort(function(a,b){if(b.score!==a.score)return b.score-a.score;var at=a.e.title.toLowerCase(),bt=b.e.title.toLowerCase();return at<bt?-1:(at>bt?1:0);});var out=[];for(var k=0;k<res.length;k++)out.push(res[k].e);return out;}function highlight(el,text,tokens){var lower=text.toLowerCase();var i=0;while(i<text.length){var best=-1,bestLen=0;for(var t=0;t<tokens.length;t++){if(!tokens[t])continue;var idx=lower.indexOf(tokens[t],i);if(idx>=0&&(best<0||idx<best)){best=idx;bestLen=tokens[t].length;}}if(best<0){el.appendChild(document.createTextNode(text.slice(i)));break;}if(best>i)el.appendChild(document.createTextNode(text.slice(i,best)));var m=document.createElement('mark');m.textContent=text.slice(best,best+bestLen);el.appendChild(m);i=best+bestLen;}}function sync(){if(!history.replaceState)return;var qs=base+'/search.html?q='+encodeURIComponent(q);if(page>1)qs+='&page='+page;history.replaceState(null,'',qs);}function note(msg){var d=document.createElement('div');d.className='search-empty';d.textContent=msg;region.appendChild(d);}function render(){region.innerHTML='';if(failed){note('Search unavailable');return;}if(!q){note('Type to search across every namespace.');return;}var tokens=tokenize(q);var list=search(tokens);var count=document.createElement('p');count.className='search-count';count.textContent=list.length+(list.length===1?' result for ':' results for ')+'\\u201c'+q+'\\u201d';region.appendChild(count);if(!list.length){note('No matches');sync();return;}var pages=Math.ceil(list.length/PER);if(page>pages)page=pages;if(page<1)page=1;var start=(page-1)*PER;var slice=list.slice(start,start+PER);var listEl=document.createElement('div');listEl.className='search-list';for(var i=0;i<slice.length;i++){var e=slice[i];var a=document.createElement('a');a.className='search-result-row';a.href=base+e.url;var ttl=document.createElement('span');ttl.className='search-result-title';highlight(ttl,e.title,tokens);a.appendChild(ttl);var badge=document.createElement('span');badge.className='search-badge';badge.textContent=e.nsTitle||e.nsSlug;a.appendChild(badge);var meta=document.createElement('span');meta.className='search-result-meta';meta.textContent=(e.category?e.category+' · ':'')+e.path;a.appendChild(meta);listEl.appendChild(a);}region.appendChild(listEl);if(pages>1)region.appendChild(pager(pages));sync();}function pager(pages){var nav=document.createElement('nav');nav.className='search-pagination';nav.setAttribute('aria-label','Search results pages');function pill(txt,target,disabled,current){var b=document.createElement('button');b.type='button';b.className='search-pagination-item';b.textContent=txt;if(current){b.className+=' search-pagination-current';b.setAttribute('aria-current','page');}if(disabled){b.disabled=true;}else{b.addEventListener('click',function(){page=target;render();if(region.scrollIntoView)region.scrollIntoView({block:'start'});});}return b;}nav.appendChild(pill('Prev',page-1,page<=1,false));for(var p=1;p<=pages;p++)nav.appendChild(pill(String(p),p,false,p===page));nav.appendChild(pill('Next',page+1,page>=pages,false));return nav;}form.addEventListener('submit',function(ev){ev.preventDefault();q=input.value.trim();page=1;load(render);});input.addEventListener('input',function(){clearTimeout(timer);timer=setTimeout(function(){q=input.value.trim();page=1;load(render);},150);});load(render);if(!q)input.focus();});})();</script>"""


def copy_button_script() -> str:
    """Progressive-enhancement copy buttons for code blocks.

    On DOMContentLoaded, injects a ``.copy-button`` into every ``<pre>`` and
    captures the block's text before the button is appended, so the copied
    payload never includes the button label. Copying prefers the async
    Clipboard API and falls back to a hidden-textarea ``execCommand('copy')``.
    Without JavaScript no button exists and the code block reads normally.
    """
    return """<script>document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('pre').forEach(function(pre){if(pre.querySelector('.copy-button'))return;var text=pre.innerText;var btn=document.createElement('button');btn.type='button';btn.className='copy-button';btn.setAttribute('aria-label','Copy code');btn.textContent='copy';btn.addEventListener('click',function(){function done(){btn.textContent='copied';setTimeout(function(){btn.textContent='copy';},1200);}function fallback(){var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.left='-9999px';document.body.appendChild(ta);ta.focus();ta.select();try{document.execCommand('copy');done();}catch(e){}document.body.removeChild(ta);}if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,fallback);}else{fallback();}});pre.appendChild(btn);});});</script>"""


# Header navigation link sets, built against a base path. Wiki/doc pages share
# WIKI_NAV_LINKS; the homepage and Signal Graph page additionally surface the
# Signal Graph link (HOME_NAV_LINKS). The GitHub link is external and keeps its
# full repo URL. build() refreshes the module-level lists per call from the
# normalized BASE_PATH, so page templates keep consuming the constants directly.
def _wiki_nav_links(base_path: str) -> list[tuple[str, str]]:
    return [
        (f"{base_path}/#wikis", "Wikis"),
        (f"{base_path}/updates.html", "Updates"),
        (f"{base_path}/docs/AGENT_SETUP.html", "Agent Setup"),
        ("https://github.com/pixiiidust/pixi-wiki", "GitHub"),
    ]


def _home_nav_links(base_path: str) -> list[tuple[str, str]]:
    return [
        (f"{base_path}/#wikis", "Wikis"),
        (f"{base_path}/updates.html", "Updates"),
        (f"{base_path}/docs/AGENT_SETUP.html", "Agent Setup"),
        (f"{base_path}/docs/SIGNAL_GRAPH.html", "Signal Graph"),
        ("https://github.com/pixiiidust/pixi-wiki", "GitHub"),
    ]


WIKI_NAV_LINKS = _wiki_nav_links(DEFAULT_BASE_PATH)
HOME_NAV_LINKS = _home_nav_links(DEFAULT_BASE_PATH)


def site_header(nav_links: list[tuple[str, str]]) -> str:
    """Render the shared site header.

    A single inline ``.nav`` is shown on wide viewports; a ``.nav-menu``
    disclosure holding the same links is revealed at <=820px (no JavaScript).
    The theme toggle sits outside both navs as a direct header child so it is
    visible at every width.
    """
    links = "".join(f'<a href="{href}">{label}</a>' for href, label in nav_links)
    return (
        '<header class="site-header"><div class="header-inner">'
        f'<a class="logo" href="{BASE_PATH}/">Pixi Wiki</a>'
        f'<div class="site-search" data-registry="{BASE_PATH}/index.json"></div>'
        '<div class="header-nav">'
        f'<nav class="nav">{links}</nav>'
        '<details class="nav-menu"><summary aria-label="Open menu">Menu</summary>'
        f'<nav class="nav-panel">{links}</nav></details>'
        '<button class="theme-toggle" data-theme-toggle type="button" aria-label="Toggle color theme">☾</button>'
        '</div></div></header>'
    )


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


def make_sidebar(slug: str, title: str, doc_count: int, active_rel: str, sidebar_docs: list[dict[str, str]]) -> str:
    def cls(rel: str) -> str:
        return ' class="active" aria-current="page"' if rel == active_rel else ""

    def link(doc: dict[str, str]) -> str:
        return f'<a{cls(doc["path"])} href="{BASE_PATH}/wiki/{slug}/{html.escape(doc["path"])}.html"><span aria-hidden="true">📄 </span>{html.escape(doc["title"])}</a>'

    def section(label: str, category: str) -> str:
        docs = sorted((doc for doc in sidebar_docs if doc["category"] == category), key=lambda doc: doc["title"].lower())
        count = len(docs)
        open_attr = " open" if any(doc["path"] == active_rel for doc in docs) else ""

        # Split docs into those directly under wiki/<category>/ (or living
        # elsewhere via frontmatter) and those nested one folder deeper, which
        # group by their first subfolder. The disk layout already encodes the
        # grouping, so a flat namespace produces byte-identical markup to before.
        prefix = f"wiki/{category}/"
        ungrouped: list[dict[str, str]] = []
        groups: dict[str, list[dict[str, str]]] = {}
        for doc in docs:
            path = doc["path"]
            if path.startswith(prefix) and "/" in path[len(prefix):]:
                subfolder = path[len(prefix):].split("/", 1)[0]
                groups.setdefault(subfolder, []).append(doc)
            else:
                ungrouped.append(doc)

        ungrouped_links = "".join(link(doc) for doc in ungrouped)
        subgroups = ""
        for subfolder in sorted(groups):
            sub_docs = groups[subfolder]
            sub_open = " open" if any(doc["path"] == active_rel for doc in sub_docs) else ""
            sub_label = subfolder.replace("-", " ").replace("_", " ").upper()
            sub_links = "".join(link(doc) for doc in sub_docs)
            subgroups += f'<details class="sidebar-subgroup"{sub_open}><summary>{sub_label} {len(sub_docs)}</summary><div class="sidebar-section-body">{sub_links}</div></details>'

        filter_box = '<input class="sidebar-filter" type="search" placeholder="Filter…" aria-label="Filter pages">' if count > 25 else ""
        empty = '<div class="sidebar-empty">No pages yet</div>' if not docs else ""
        return f'<details class="sidebar-section"{open_attr}><summary>{label} {count}</summary><div class="sidebar-section-body">{filter_box}{ungrouped_links}{subgroups}{empty}</div></details>'

    rows = [
        f'<aside class="sidebar"><div class="sidebar-block"><div class="sidebar-title">{html.escape(title)}</div><div class="sidebar-count">{doc_count} documents</div>',
        f'<a{cls("README.md")} href="{BASE_PATH}/wiki/{slug}/README.md.html"><span aria-hidden="true">📄 </span>{html.escape(title)} Knowledge Base</a>',
        f'<a{cls("wiki/index.md")} href="{BASE_PATH}/wiki/{slug}/wiki/index.md.html"><span aria-hidden="true">📄 </span>{html.escape(title)} KB — Master Index</a>',
        section("WIKI", "wiki"),
        section("CONCEPTS", "concepts"),
        section("ENTITIES", "entities"),
        section("SUMMARIES", "summaries"),
        section("SYNTHESES", "syntheses"),
        '</div><div class="sidebar-block"><details class="sidebar-section" open><summary>// FOR AGENTS</summary><div class="sidebar-section-body">',
        f'<a href="{BASE_PATH}/wiki/{slug}/llms.txt">llms.txt</a>',
        f'<a href="{BASE_PATH}/wiki/{slug}/llms-full.txt">llms-full.txt</a>',
        f'<a href="{BASE_PATH}/wiki/{slug}/index.json">index.json</a>',
        "</div></details></div></aside>",
    ]
    return "\n".join(rows)


def truncate_description(text: str, limit: int = 200) -> str:
    """Collapse whitespace and truncate to ~``limit`` chars at a word boundary.

    Used for meta/OpenGraph descriptions: the result never exceeds ``limit``
    characters (including the trailing ellipsis) and never cuts a word in half.
    """
    collapsed = " ".join(text.split()).strip()
    if len(collapsed) <= limit:
        return collapsed
    clipped = collapsed[: limit - 1]
    if " " in clipped:
        clipped = clipped[: clipped.rfind(" ")]
    return clipped.rstrip() + "…"


def head_meta(title: str, description: str, canonical_path: str, og_type: str = "website", noindex: bool = False) -> str:
    """Return the SEO/social ``<head>`` block for one page.

    Emits a meta description, canonical link, OpenGraph title/description/url/
    type/site_name, and a Twitter summary card. ``canonical_path`` is a
    site-absolute path (e.g. ``/pixi-wiki/wiki/<slug>/<rel>.html``); the absolute
    URL is ``SITE_ORIGIN`` + that path. The description is collapsed, truncated
    to a word boundary, and HTML-escaped. When ``noindex`` is set a
    ``robots: noindex`` meta is appended, so JS-dependent enhancement surfaces
    (e.g. the client search results page) stay out of the crawl index.
    """
    desc = html.escape(truncate_description(description), quote=True)
    title_attr = html.escape(title, quote=True)
    url = html.escape(SITE_ORIGIN + canonical_path, quote=True)
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    return (
        f'<meta name="description" content="{desc}">'
        f'<link rel="canonical" href="{url}">'
        f'<meta property="og:title" content="{title_attr}">'
        f'<meta property="og:description" content="{desc}">'
        f'<meta property="og:url" content="{url}">'
        f'<meta property="og:type" content="{og_type}">'
        f'<meta property="og:site_name" content="{html.escape(SITE_NAME, quote=True)}">'
        f'<meta name="twitter:card" content="summary">'
        f'{robots}'
    )


def page_shell(slug: str, namespace_title: str, doc_count: int, active_rel: str, sidebar_docs: list[dict[str, str]], article: str, page_title: str, description: str) -> str:
    sidebar = make_sidebar(slug, namespace_title, doc_count, active_rel, sidebar_docs)
    canonical_path = f"{BASE_PATH}/wiki/{slug}/{active_rel}.html"
    meta = head_meta(f"{page_title} — {namespace_title}", description, canonical_path, og_type="article")
    return f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(page_title)} — {html.escape(namespace_title)} — Pixi Wiki</title>{meta}
{stylesheet_link()}{theme_script()}{sidebar_filter_script()}{search_script()}{copy_button_script()}</head><body>
<a class="skip-link" href="#main-content">Skip to content</a>
{site_header(WIKI_NAV_LINKS)}
<main class="page">{sidebar}<article class="article" id="main-content">{article}</article></main>
<footer class="footer"><div class="footer-inner"><p>Plain static HTML. Humans browse it like a wiki; agents read Markdown through <code>llms.txt</code>.</p><p><a href="{BASE_PATH}/llms.txt">/llms.txt</a><a href="{BASE_PATH}/llms-full.txt">/llms-full.txt</a><a href="{BASE_PATH}/index.json">/index.json</a></p></div></footer>
</body></html>"""


def report_mistake_url(slug: str, rel: str) -> str:
    title = quote_plus(f"Pixi Wiki correction: {slug}/{rel}")
    body = quote_plus(f"Page: {SITE_ORIGIN}{BASE_PATH}/wiki/{slug}/{rel}.html\n\nWhat should be corrected?")
    return f"https://github.com/pixiiidust/pixi-wiki/issues/new?title={title}&body={body}"


def page_tools(slug: str, rel: str) -> str:
    return (
        f'<span class="page-tools"><a class="markdown-link" href="{BASE_PATH}/raw/{slug}/{html.escape(rel)}">view as markdown</a>'
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


def is_external_url(value: str) -> bool:
    return value.startswith("https://") or value.startswith("http://")


def external_link_label(url: str, fallback: str | None = None) -> str:
    if fallback:
        return fallback
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    return f"{parsed.netloc}/{path}".rstrip("/") if parsed.netloc else url


def external_links_block(fm: dict[str, Any], body: str) -> str:
    links: dict[str, str] = {}

    for key in ["resource", "source_url", "raw_url"]:
        value = fm.get(key)
        if isinstance(value, str) and is_external_url(value):
            links[value] = external_link_label(value)

    sources = fm.get("sources")
    if isinstance(sources, list):
        for source in sources:
            if isinstance(source, str) and is_external_url(source):
                links[source] = external_link_label(source)
    elif isinstance(sources, str) and is_external_url(sources):
        links[sources] = external_link_label(sources)

    for label, url in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", body):
        links[url] = external_link_label(url, label)

    if not links:
        return ""

    rows = "".join(
        f'<li><a href="{html.escape(url)}">{html.escape(label)}</a></li>'
        for url, label in sorted(links.items(), key=lambda item: item[1].lower())
    )
    return f"<h2>External links</h2>\n<ul>\n{rows}\n</ul>"


def prev_next_nav(slug: str, prev_doc: dict[str, str] | None, next_doc: dict[str, str] | None) -> str:
    cards: list[str] = []
    if prev_doc:
        cards.append(
            f'<a class="prev-next-card prev-card" href="{BASE_PATH}/wiki/{slug}/{html.escape(prev_doc["path"])}.html">'
            f'<span class="next-label">← Prev</span><span class="next-title">{html.escape(prev_doc["title"])}</span></a>'
        )
    if next_doc:
        cards.append(
            f'<a class="prev-next-card next-card" href="{BASE_PATH}/wiki/{slug}/{html.escape(next_doc["path"])}.html">'
            f'<span class="next-label">Next</span><span class="next-title">{html.escape(next_doc["title"])} →</span></a>'
        )
    return f'<nav class="prev-next">{"".join(cards)}</nav>' if cards else ""


def page_toc(headings: list[dict[str, Any]]) -> str:
    """On-this-page TOC from h2/h3 headings; empty for fewer than two sections."""
    sections = [h for h in headings if h["level"] in (2, 3)]
    if len(sections) < 2:
        return ""
    items = "".join(
        f'<li class="page-toc-h{h["level"]}">'
        f'<a href="#{h["slug"]}">{html.escape(h["text"])}</a></li>'
        for h in sections
    )
    return (
        '<nav class="page-toc"><div class="page-toc-title">On this page</div>'
        f"<ul>{items}</ul></nav>"
    )


def insert_toc_before_first_h2(rendered_body: str, toc: str) -> str:
    if not toc:
        return rendered_body
    if "<h2" in rendered_body:
        return rendered_body.replace("<h2", f"{toc}\n<h2", 1)
    return f"{toc}\n{rendered_body}"


def render_readme(
    slug: str,
    title: str,
    fm: dict[str, Any],
    body: str,
    covers: str,
    not_covered: str,
    current_as: str,
    next_doc: dict[str, str] | None,
    link_resolver: LinkResolver | None = None,
) -> str:
    updated = fm.get("updated", "unknown")
    description = first_paragraph(body)
    body_without_title = re.sub(r"^#\s+.+\n", "", body, count=1).strip()
    body_without_scope = strip_scope_section(body_without_title).strip()
    if body_without_scope:
        rendered_body, body_headings = markdown_fragment_with_headings(body_without_scope, link_resolver)
    else:
        rendered_body, body_headings = "", []
    toc = page_toc(body_headings)
    article = f"""
<div class="content-header"><div class="breadcrumbs"><a href="{BASE_PATH}/">wikis</a> / <a href="{BASE_PATH}/wiki/{slug}/README.md.html">{html.escape(title)}</a> / README.md</div>{page_tools(slug, "README.md")}</div>
<h1>{html.escape(title)} Knowledge Base</h1>
{metadata_block(fm)}
<div class="updated">updated: <strong>{html.escape(str(updated))}</strong></div>
<section class="info-card"><div class="info-row"><div class="info-label green">Covers</div><div>{inline_markdown(covers, link_resolver)}</div></div><div class="info-row"><div class="info-label yellow">Not Covered</div><div>{inline_markdown(not_covered or "Out-of-scope or stale material; verify with source notes and live tools.", link_resolver)}</div></div><div class="info-row"><div class="info-label white">Current As Of</div><div>{html.escape(current_as or str(updated))}</div></div></section>
<div class="agent-card"><span aria-hidden="true">🤖 </span>Agent access: <a href="{BASE_PATH}/wiki/{slug}/llms.txt">/wiki/{slug}/llms.txt</a> <a href="{BASE_PATH}/wiki/{slug}/llms-full.txt">/wiki/{slug}/llms-full.txt</a> <a href="{BASE_PATH}/wiki/{slug}/index.json">/wiki/{slug}/index.json</a></div>
<p>{inline_markdown(description, link_resolver)}</p>
<h2>Structure</h2><ul><li><code>raw/</code> — raw Markdown provenance mirror for agents and source inspection.</li><li><code>wiki/</code> — synthesized knowledge pages: concepts, entities, summaries, and syntheses.</li><li>Schema and maintenance rules: see <code>CLAUDE.md</code>.</li></ul>
<h2>Usage</h2><ul><li><strong>Add new sources:</strong> update canonical source notes in <code>pixi-vault</code>, then compile into this namespace.</li><li><strong>Ask questions:</strong> agents read this wiki and cite raw/source paths.</li><li><strong>Publish:</strong> regenerate <code>pixi-wiki</code>, run tests, then live-verify raw and HTML routes.</li></ul>
{toc}
{rendered_body}
{external_links_block(fm, body)}
{prev_next_nav(slug, None, next_doc)}
"""
    return article


def render_page(
    slug: str,
    title: str,
    rel: str,
    page_title: str,
    fm: dict[str, Any],
    body: str,
    prev_doc: dict[str, str] | None,
    next_doc: dict[str, str] | None,
    link_resolver: LinkResolver | None = None,
) -> str:
    fragment, body_headings = markdown_fragment_with_headings(body, link_resolver)
    rendered_body = with_metadata_after_h1(fragment, metadata_block(fm))
    rendered_body = insert_toc_before_first_h2(rendered_body, page_toc(body_headings))
    external_links = external_links_block(fm, body)
    return f"""
<div class="content-header"><div class="breadcrumbs"><a href="{BASE_PATH}/">wikis</a> / <a href="{BASE_PATH}/wiki/{slug}/README.md.html">{html.escape(title)}</a> / {html.escape(rel)}</div>{page_tools(slug, rel)}</div>
{rendered_body}
{external_links}
{prev_next_nav(slug, prev_doc, next_doc)}
"""


def build_global_link_targets(source_dir: Path, slugs: list[str]) -> dict[str, str]:
    targets: dict[str, str] = {}
    for slug in slugs:
        namespace_dir = source_dir / slug
        for source_file in sorted(
            namespace_dir.rglob("*.md"),
            key=lambda p: p.relative_to(namespace_dir).parts,
        ):
            rel = source_file.relative_to(namespace_dir)
            text = source_file.read_text(encoding="utf-8")
            fm, _body = parse_frontmatter(text)
            page_title = fm.get("title") or first_heading(text) or rel.name
            rel_posix = rel.as_posix()
            href = f"{BASE_PATH}/wiki/{slug}/{rel_posix}.html"
            keys = {
                rel_posix,
                rel_posix.removesuffix(".md"),
                rel.stem,
                str(page_title),
                str(page_title).lower(),
            }
            if len(rel.parts) >= 2:
                keys.add("/".join(rel.parts[-2:]).removesuffix(".md"))
            for key in keys:
                targets.setdefault(key, href)
    return targets


def collect_namespace(
    source_dir: Path,
    output_root: Path,
    slug: str,
    global_link_targets: dict[str, str] | None = None,
) -> tuple[dict[str, Any], list[tuple[str, str, str, str]], list[tuple[str, str]], list[dict[str, str]], list[dict[str, str]]]:
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

    md_files = sorted(namespace_dir.rglob("*.md"), key=lambda p: p.relative_to(namespace_dir).parts)
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
    update_entries: list[dict[str, str]] = []
    sitemap_docs: list[dict[str, str]] = []
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

    link_targets: dict[str, str] = dict(global_link_targets or {})
    for rel, _text, _page_fm, _body, page_title in parsed:
        rel_posix = rel.as_posix()
        href = f"{BASE_PATH}/wiki/{slug}/{rel_posix}.html"
        keys = {
            rel_posix,
            rel_posix.removesuffix(".md"),
            rel.stem,
            str(page_title),
            str(page_title).lower(),
        }
        if len(rel.parts) >= 2:
            keys.add("/".join(rel.parts[-2:]).removesuffix(".md"))
        for key in keys:
            link_targets[key] = href

    def resolve_wikilink(target: str) -> str | None:
        normalized = target.strip().removesuffix(".html")
        if normalized in link_targets:
            return link_targets[normalized]
        if normalized.lower() in link_targets:
            return link_targets[normalized.lower()]
        cross_namespace = re.match(r"^\.\./\.\./([^/]+)/(.+)$", normalized)
        if cross_namespace:
            target_slug, target_path = cross_namespace.groups()
            if not target_path.endswith(".md"):
                target_path = f"{target_path}.md"
            return f"{BASE_PATH}/wiki/{target_slug}/{target_path}.html"
        return None

    # Namespace-local agent access files.
    ns_wiki_dir = output_root / "wiki" / slug
    ns_wiki_dir.mkdir(parents=True, exist_ok=True)
    asset_source_dir = namespace_dir / "assets"
    if asset_source_dir.exists():
        for asset in sorted(path for path in asset_source_dir.rglob("*") if path.is_file()):
            rel_asset = asset.relative_to(namespace_dir)
            target = output_root / "wiki" / slug / rel_asset
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset, target)
    local_llms: list[str] = [f"# {title} Knowledge Base\n\n", f"> {description}\n\n"]
    for rel, text, _page_fm, _body, page_title in parsed:
        rel_posix = rel.as_posix()
        raw_url = f"/raw/{slug}/{rel_posix}"
        html_url = f"/wiki/{slug}/{rel_posix}.html"
        local_llms.append(f"- [{page_title}]({raw_url}) ([html]({html_url}))\n")
    (ns_wiki_dir / "llms.txt").write_text("".join(local_llms).rstrip() + "\n", encoding="utf-8", newline="\n")
    (ns_wiki_dir / "llms-full.txt").write_text("\n\n".join(f"<!-- ===== {slug}/{rel.as_posix()} ===== -->\n\n{text}" for rel, text, *_ in parsed) + "\n", encoding="utf-8", newline="\n")

    for rel, text, page_fm, body, page_title in parsed:
        rel_posix = rel.as_posix()
        raw_output = output_root / "raw" / slug / rel
        html_output = output_root / "wiki" / slug / (rel_posix + ".html")
        raw_output.parent.mkdir(parents=True, exist_ok=True)
        html_output.parent.mkdir(parents=True, exist_ok=True)
        raw_output.write_text(text, encoding="utf-8", newline="\n")
        nav_index = nav_by_path.get(rel_posix)
        prev_doc = nav_docs[nav_index - 1] if nav_index is not None and nav_index > 0 else None
        next_doc = nav_docs[nav_index + 1] if nav_index is not None and nav_index + 1 < len(nav_docs) else None
        if rel_posix == "README.md":
            article = render_readme(slug, str(title), fm, readme_body, covers, not_covered, current_as, next_doc, resolve_wikilink)
            page_description = description
        else:
            content_source = body if page_fm else text
            article = render_page(slug, str(title), rel_posix, str(page_title), page_fm, content_source, prev_doc, next_doc, resolve_wikilink)
            page_description = first_paragraph(content_source) or description
        html_output.write_text(page_shell(slug, str(title), len(md_files), rel_posix, sidebar_docs, article, str(page_title), page_description), encoding="utf-8", newline="\n")
        # Sitemap entry for this generated page. lastmod is emitted only when the
        # frontmatter `updated` is a strict YYYY-MM-DD date (deterministic; never
        # the wall clock), matching the Updates date contract.
        updated_for_sitemap = str(page_fm.get("updated", "")) if page_fm else ""
        sitemap_docs.append(
            {
                "path": f"{BASE_PATH}/wiki/{slug}/{rel_posix}.html",
                "lastmod": updated_for_sitemap if UPDATE_DATE_RE.match(updated_for_sitemap) else "",
            }
        )
        raw_url = f"/raw/{slug}/{rel_posix}"
        html_url = f"/wiki/{slug}/{rel_posix}.html"
        links.append((str(page_title), rel_posix, raw_url, html_url))
        full_sections.append((f"{slug}/{rel_posix}", text))
        doc_records.append({"title": str(page_title), "path": rel_posix, "raw": raw_url, "html": html_url, "category": sidebar_category(rel, page_fm)})
        # Updates feed entry — only docs with a strict YYYY-MM-DD `updated`
        # frontmatter value qualify; CLAUDE.md is never surfaced.
        updated_value = str(page_fm.get("updated", "")) if page_fm else ""
        if rel_posix != "CLAUDE.md" and UPDATE_DATE_RE.match(updated_value):
            update_entries.append(
                {
                    "title": str(page_title),
                    "path": rel_posix,
                    "namespace": slug,
                    "namespace_title": str(title),
                    "updated": updated_value,
                    "raw": raw_url,
                    "html": html_url,
                }
            )

    local_index = {
        "slug": slug,
        "title": title,
        "description": description,
        "documentCount": len(md_files),
        "counts": {key: counts.get(key, 0) for key in ["wiki", "concepts", "entities", "summaries", "syntheses"]},
        "documents": doc_records,
    }
    (ns_wiki_dir / "index.json").write_text(json.dumps(local_index, indent=2) + "\n", encoding="utf-8", newline="\n")

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
    return wiki_record, links, full_sections, update_entries, sitemap_docs


def write_agent_setup_page(output_root: Path) -> None:
    docs_dir = output_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    body = f"""
<article class="article" style="max-width:900px;margin:44px auto 90px;padding:0 20px">
<div class="content-header"><div class="breadcrumbs"><a href="{BASE_PATH}/">wikis</a> / Agent Setup</div><span class="page-tools"><a class="markdown-link" href="{BASE_PATH}/docs/MCP_SERVER.md">MCP server docs</a></span></div>
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
<p><a class="button-link primary" href="{BASE_PATH}/docs/MCP_SERVER.md">Full MCP server reference →</a></p>
</article>
"""
    page = f"""<!doctype html>
<html lang=\"en\" data-theme=\"light\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>Agent Setup — Pixi Wiki</title>{head_meta("Agent Setup", AGENT_SETUP_DESCRIPTION, BASE_PATH + "/docs/AGENT_SETUP.html")}{stylesheet_link()}{theme_script()}{search_script()}{copy_button_script()}</head><body>
<a class=\"skip-link\" href=\"#main-content\">Skip to content</a>
{site_header(WIKI_NAV_LINKS)}
<main id=\"main-content\">{body}</main>
<footer class=\"footer\"><div class=\"footer-inner\"><p>Plain static HTML. Agents read Markdown through <code>llms.txt</code> and MCP.</p><p><a href=\"{BASE_PATH}/llms.txt\">/llms.txt</a><a href=\"{BASE_PATH}/llms-full.txt\">/llms-full.txt</a><a href=\"{BASE_PATH}/index.json\">/index.json</a></p></div></footer>
</body></html>"""
    (docs_dir / "AGENT_SETUP.html").write_text(page, encoding="utf-8", newline="\n")


def write_replicate_page(output_root: Path) -> None:
    docs_dir = output_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    body = f"""
<article class="article" style="max-width:900px;margin:44px auto 90px;padding:0 20px">
<div class="content-header"><div class="breadcrumbs"><a href="{BASE_PATH}/">wikis</a> / Replicate the Approach</div><span class="page-tools"><a class="markdown-link" href="https://github.com/pixiiidust/pixi-wiki">GitHub repo</a></span></div>
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
<title>Replicate the Approach — Pixi Wiki</title>{head_meta("Replicate the Approach", REPLICATE_DESCRIPTION, BASE_PATH + "/docs/REPLICATE_APPROACH.html")}{stylesheet_link()}{theme_script()}{search_script()}{copy_button_script()}</head><body>
<a class=\"skip-link\" href=\"#main-content\">Skip to content</a>
{site_header(WIKI_NAV_LINKS)}
<main id=\"main-content\">{body}</main>
<footer class=\"footer\"><div class=\"footer-inner\"><p>Copy the pattern. Keep your source files canonical.</p><p><a href=\"{BASE_PATH}/llms.txt\">/llms.txt</a><a href=\"{BASE_PATH}/llms-full.txt\">/llms-full.txt</a><a href=\"{BASE_PATH}/index.json\">/index.json</a></p></div></footer>
</body></html>"""
    (docs_dir / "REPLICATE_APPROACH.html").write_text(page, encoding="utf-8", newline="\n")


def write_signal_graph_page(output_root: Path) -> None:
    docs_dir = output_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    body = f"""
<article class="article" style="max-width:900px;margin:44px auto 90px;padding:0 20px">
<div class="content-header"><div class="breadcrumbs"><a href="{BASE_PATH}/">wikis</a> / Signal Graph</div><span class="page-tools"><a class="markdown-link" href="{BASE_PATH}/docs/SIGNAL_GRAPH.md">Markdown docs</a></span></div>
<h1>Signal Graph</h1>
<p class="hero-copy">A local analysis sidecar for mapping Pixi Wiki's Markdown corpus before edits, fit-checks, and agent orientation.</p>
<section class="info-card"><div class="info-row"><div class="info-label green">Input</div><div>Generated Pixi Wiki Markdown under <code>raw/</code>: namespaces, frontmatter, tags, headings, wikilinks, Markdown links, and declared sources.</div></div><div class="info-row"><div class="info-label yellow">Output</div><div>A Graphify-compatible <code>graphify-out/graph.json</code> plus optional <code>GRAPH_REPORT.md</code> and <code>graph.html</code>.</div></div><div class="info-row"><div class="info-label white">Boundary</div><div>The graph is disposable and ignored by Git. It helps orientation; it does not replace raw Markdown, <code>llms.txt</code>, <code>index.json</code>, or MCP retrieval.</div></div></section>
<h2>Run it locally</h2>
<pre><code>python scripts/build_signal_graph.py raw graphify-out
graphify cluster-only . --graph graphify-out/graph.json --no-label</code></pre>
<h2>Why it exists</h2>
<p>Naive corpus graphs over-weight generic glue like <code>status: compiled</code>, <code>type: concept</code>, <code>Rules</code>, and <code>Boundaries</code>. The signal graph filters that noise so the report highlights real documents, concepts, bridges, and source classes.</p>
<h2>Use it for</h2>
<ul><li>Map-before-edit orientation.</li><li>Finding cross-namespace concept bridges.</li><li>I-know-kungfu / Knowledge Pack fit-checks.</li><li>Choosing which Pixi Wiki MCP documents to read next.</li></ul>
<p><a class="button-link primary" href="{BASE_PATH}/docs/SIGNAL_GRAPH.md">Read the implementation notes →</a></p>
</article>
"""
    page = f"""<!doctype html>
<html lang=\"en\" data-theme=\"light\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>Signal Graph — Pixi Wiki</title>{head_meta("Signal Graph", SIGNAL_GRAPH_DESCRIPTION, BASE_PATH + "/docs/SIGNAL_GRAPH.html")}{stylesheet_link()}{theme_script()}{search_script()}{copy_button_script()}</head><body>
<a class=\"skip-link\" href=\"#main-content\">Skip to content</a>
{site_header(HOME_NAV_LINKS)}
<main id=\"main-content\">{body}</main>
<footer class=\"footer\"><div class=\"footer-inner\"><p>Generated graph artifacts stay local unless intentionally shared.</p><p><a href=\"{BASE_PATH}/llms.txt\">/llms.txt</a><a href=\"{BASE_PATH}/llms-full.txt\">/llms-full.txt</a><a href=\"{BASE_PATH}/index.json\">/index.json</a></p></div></footer>
</body></html>"""
    (docs_dir / "SIGNAL_GRAPH.html").write_text(page, encoding="utf-8", newline="\n")


def updates_filter_script() -> str:
    """Progressive-enhancement time-range filter for the Updates page.

    On DOMContentLoaded this builds a chip bar (All / 7 / 30 / 90 days) inside
    the empty ``.updates-filter`` placeholder, so nothing renders without
    JavaScript and the full history stays readable. Clicking a chip reads the
    CLIENT clock (client-side JS may use the clock; the generator never does),
    computes a cutoff, hides every ``.updates-group`` whose ``data-date`` is
    older, marks the active chip via ``aria-pressed``, and reveals a small
    "no updates in this range" note when the whole list is hidden.
    """
    return """<script>(function(){document.addEventListener('DOMContentLoaded',function(){var box=document.querySelector('.updates-filter');if(!box)return;var groups=[].slice.call(document.querySelectorAll('.updates-group'));if(!groups.length)return;var ranges=[['All',0],['7 days',7],['30 days',30],['90 days',90]];var note=document.createElement('div');note.className='updates-empty';note.hidden=true;note.textContent='No updates in this range.';var buttons=[];function toUTC(s){var p=(s||'').split('-');if(p.length!==3)return NaN;return Date.UTC(+p[0],+p[1]-1,+p[2]);}function apply(days,active){for(var i=0;i<buttons.length;i++){buttons[i].setAttribute('aria-pressed',buttons[i]===active?'true':'false');}var visible=0;if(!days){for(var j=0;j<groups.length;j++){groups[j].hidden=false;visible++;}}else{var now=new Date();var cutoff=Date.UTC(now.getFullYear(),now.getMonth(),now.getDate())-days*86400000;for(var k=0;k<groups.length;k++){var t=toUTC(groups[k].getAttribute('data-date'));var keep=!isNaN(t)&&t>=cutoff;groups[k].hidden=!keep;if(keep)visible++;}}note.hidden=visible>0;}for(var r=0;r<ranges.length;r++){(function(range){var b=document.createElement('button');b.type='button';b.className='updates-chip';b.textContent=range[0];b.setAttribute('aria-pressed','false');b.addEventListener('click',function(){apply(range[1],b);});box.appendChild(b);buttons.push(b);})(ranges[r]);}box.appendChild(note);apply(0,buttons[0]);});})();</script>"""


def group_updates_by_date(
    entries: list[dict[str, str]],
) -> list[tuple[str, list[dict[str, str]]]]:
    """Collapse pre-sorted entries into contiguous date-descending sections."""
    groups: list[tuple[str, list[dict[str, str]]]] = []
    for entry in entries:
        if not groups or groups[-1][0] != entry["updated"]:
            groups.append((entry["updated"], []))
        groups[-1][1].append(entry)
    return groups


def paginate_update_groups(
    groups: list[tuple[str, list[dict[str, str]]]],
    target: int = UPDATES_PAGE_ENTRY_TARGET,
) -> list[list[tuple[str, list[dict[str, str]]]]]:
    """Split whole date sections into pages at a soft ``target`` entry cap.

    Sections are appended to the current page until its running entry total
    reaches ``target``; the page is then flushed and a new one begins. A section
    is never split across pages, so a single import day larger than ``target``
    becomes one oversized page. Pure function of the data; an empty corpus still
    yields exactly one (empty) page so ``updates.html`` always exists.
    """
    pages: list[list[tuple[str, list[dict[str, str]]]]] = []
    current: list[tuple[str, list[dict[str, str]]]] = []
    running = 0
    for date, items in groups:
        current.append((date, items))
        running += len(items)
        if running >= target:
            pages.append(current)
            current = []
            running = 0
    if current or not pages:
        pages.append(current)
    return pages


def updates_page_path(page_num: int) -> str:
    """Site-absolute path for Updates page ``N`` (1 -> root, N>=2 -> subdir)."""
    if page_num <= 1:
        return f"{BASE_PATH}/updates.html"
    return f"{BASE_PATH}/updates/{page_num}.html"


def pagination_window(current: int, total: int, edge: int = 2) -> list[int | None]:
    """Deterministic page-number window with ellipses for long ranges.

    Ranges of nine pages or fewer render every number. Longer ranges keep the
    first page, the last page, and ``current ± edge``, collapsing each remaining
    gap into a single ``None`` sentinel (rendered as an ellipsis).
    """
    if total <= 9:
        return list(range(1, total + 1))
    keep = {1, total}
    for page in range(current - edge, current + edge + 1):
        if 1 <= page <= total:
            keep.add(page)
    result: list[int | None] = []
    previous: int | None = None
    for page in sorted(keep):
        if previous is not None and page - previous > 1:
            result.append(None)
        result.append(page)
        previous = page
    return result


def render_pagination(current: int, total: int) -> str:
    """Bottom pagination bar: Prev, numbered pills (current marked), Next.

    Omitted entirely for a single-page corpus (nothing to paginate). Prev is
    dropped on the first page and Next on the last; the current page renders as a
    non-link ``aria-current="page"`` pill.
    """
    if total <= 1:
        return ""
    items: list[str] = []
    if current > 1:
        items.append(
            f'<a class="pagination-prev" rel="prev" '
            f'href="{updates_page_path(current - 1)}">← Prev</a>'
        )
    for page in pagination_window(current, total):
        if page is None:
            items.append('<span class="pagination-ellipsis" aria-hidden="true">…</span>')
        elif page == current:
            items.append(
                f'<span class="pagination-pill pagination-current" '
                f'aria-current="page">{page}</span>'
            )
        else:
            items.append(
                f'<a class="pagination-pill" href="{updates_page_path(page)}">{page}</a>'
            )
    if current < total:
        items.append(
            f'<a class="pagination-next" rel="next" '
            f'href="{updates_page_path(current + 1)}">Next →</a>'
        )
    return f'<nav class="pagination" aria-label="Pagination">{"".join(items)}</nav>'


def _updates_month_strip(
    months_order: list[str], month_page: dict[str, int], current_page: int
) -> str:
    """Month index strip shared by every page; hrefs cross-link off-page months.

    A month whose first (newest) date section lives on the current page links to
    a bare ``#m-YYYY-MM`` anchor; every other month links to its page URL plus
    that anchor, so the strip works identically from any page.
    """
    if not months_order:
        return ""
    links: list[str] = []
    for month in months_order:
        target_page = month_page[month]
        href = f"#m-{month}" if target_page == current_page else f"{updates_page_path(target_page)}#m-{month}"
        links.append(f'<a href="{html.escape(href, quote=True)}">{html.escape(month)}</a>')
    return f'<nav class="updates-months" aria-label="Jump to month">{" · ".join(links)}</nav>'


def _render_updates_section(
    date: str, items: list[dict[str, str]], is_month_first: bool
) -> str:
    """One date section: optional month anchor, heading, per-namespace roll-ups."""
    month = date[:7]
    month_anchor = (
        f'<span class="updates-month-anchor" id="m-{month}"></span>'
        if is_month_first
        else ""
    )
    ns_runs: list[tuple[str, list[dict[str, str]]]] = []
    for item in items:
        if not ns_runs or ns_runs[-1][0] != item["namespace"]:
            ns_runs.append((item["namespace"], []))
        ns_runs[-1][1].append(item)
    blocks: list[str] = []
    for _namespace, run in ns_runs:
        rows = "".join(
            f'<li class="updates-item">'
            f'<a class="updates-title" href="{BASE_PATH}{html.escape(item["html"])}">{html.escape(item["title"])}</a>'
            f'<a class="updates-raw" href="{BASE_PATH}{html.escape(item["raw"])}">raw</a>'
            f'</li>'
            for item in run
        )
        blocks.append(
            f'<details class="updates-ns">'
            f'<summary>{html.escape(run[0]["namespace_title"])} ({len(run)})</summary>'
            f'<ul class="updates-list">{rows}</ul></details>'
        )
    return (
        f'{month_anchor}<section class="updates-group" id="d-{date}" data-date="{date}">'
        f'<h2>{html.escape(date)}</h2>{"".join(blocks)}</section>'
    )


def render_updates_page(
    page_num: int,
    total_pages: int,
    page_groups: list[tuple[str, list[dict[str, str]]]],
    months_order: list[str],
    month_first_date: dict[str, str],
    month_page: dict[str, int],
) -> str:
    """Render one Updates page's full HTML document.

    Every page carries standard chrome, the h1 + hero line, the cross-page month
    strip, its own date sections, and the pagination bar. Only page 1 emits the
    time-filter chip placeholder and its script: a "7 days" chip on a deeper page
    would be meaningless, so deeper pages get neither.
    """
    month_strip = _updates_month_strip(months_order, month_page, page_num)
    sections = [
        _render_updates_section(date, items, month_first_date.get(date[:7]) == date)
        for date, items in page_groups
    ]
    grouped = "".join(sections) or '<p class="hero-copy">No dated updates yet.</p>'
    pagination = render_pagination(page_num, total_pages)

    canonical = updates_page_path(page_num)
    if page_num == 1:
        title = "Updates"
        description = UPDATES_DESCRIPTION
        filter_placeholder = '<div class="updates-filter"></div>'
        filter_js = updates_filter_script()
    else:
        title = f"Updates — page {page_num}"
        description = f"Updates — page {page_num} of {total_pages}. {UPDATES_DESCRIPTION}"
        filter_placeholder = ""
        filter_js = ""

    rel_links = ""
    if page_num > 1:
        prev_url = html.escape(SITE_ORIGIN + updates_page_path(page_num - 1), quote=True)
        rel_links += f'<link rel="prev" href="{prev_url}">'
    if page_num < total_pages:
        next_url = html.escape(SITE_ORIGIN + updates_page_path(page_num + 1), quote=True)
        rel_links += f'<link rel="next" href="{next_url}">'

    body = (
        '<article class="article" style="max-width:900px;margin:44px auto 90px;padding:0 20px">'
        f'<div class="content-header"><div class="breadcrumbs"><a href="{BASE_PATH}/">wikis</a> / Updates</div>'
        f'<span class="page-tools"><a class="markdown-link" href="{BASE_PATH}/updates.json">updates.json</a></span></div>'
        f'<h1>{html.escape(title)}</h1>'
        '<p class="hero-copy">Every updated page across every Pixi Wiki namespace, grouped by the date recorded in each page\'s frontmatter. Jump by month, or filter by time range.</p>'
        f'{filter_placeholder}'
        f'{month_strip}'
        f'{grouped}'
        f'{pagination}'
        '</article>'
    )
    return f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — Pixi Wiki</title>{head_meta(title, description, canonical)}{rel_links}{stylesheet_link()}{theme_script()}{search_script()}{filter_js}</head><body>
<a class="skip-link" href="#main-content">Skip to content</a>
{site_header(HOME_NAV_LINKS)}
<main id="main-content">{body}</main>
<footer class="footer"><div class="footer-inner"><p>Plain static HTML. Humans browse it like a wiki; agents read Markdown through <code>llms.txt</code>.</p><p><a href="{BASE_PATH}/llms.txt">/llms.txt</a><a href="{BASE_PATH}/llms-full.txt">/llms-full.txt</a><a href="{BASE_PATH}/index.json">/index.json</a></p></div></footer>
</body></html>"""


def write_updates_page(output_root: Path, entries: list[dict[str, str]]) -> list[str]:
    """Render the paginated Updates surface and return every page's URL path.

    Entries arrive pre-sorted (date DESC, namespace ASC, title ASC). They are
    grouped into date-descending sections, chunked into pages at the
    ``UPDATES_PAGE_ENTRY_TARGET`` soft cap (whole sections only), and each page is
    written: page 1 to ``updates.html`` and page N>=2 to ``updates/N.html``. The
    returned site-absolute paths feed the sitemap. The month strip, per-month
    anchors, and pagination bar are all pre-rendered so every page is fully
    browsable with no JavaScript.
    """
    groups = group_updates_by_date(entries)
    pages = paginate_update_groups(groups)
    total_pages = len(pages)

    # Global month order and each month's first (newest) date section — the date
    # that carries the ``m-`` anchor, wherever it lands across pages.
    month_first_date: dict[str, str] = {}
    months_order: list[str] = []
    for date, _items in groups:
        month = date[:7]
        if month not in month_first_date:
            month_first_date[month] = date
            months_order.append(month)

    # Which page holds each month's anchor, so the strip can cross-link.
    month_page: dict[str, int] = {}
    for index, page_groups in enumerate(pages, start=1):
        for date, _items in page_groups:
            month = date[:7]
            if month not in month_page:
                month_page[month] = index

    updates_dir = output_root / "updates"
    paths: list[str] = []
    for index, page_groups in enumerate(pages, start=1):
        page_html = render_updates_page(
            index, total_pages, page_groups, months_order, month_first_date, month_page
        )
        if index == 1:
            (output_root / "updates.html").write_text(page_html, encoding="utf-8", newline="\n")
        else:
            updates_dir.mkdir(parents=True, exist_ok=True)
            (updates_dir / f"{index}.html").write_text(page_html, encoding="utf-8", newline="\n")
        paths.append(updates_page_path(index))
    return paths


def write_recent_redirect(output_root: Path) -> None:
    """Emit ``recent.html`` as a tiny meta-refresh stub to the renamed Updates page.

    The old ``/recent.html`` URL was short-lived; this keeps it working by
    redirecting to ``updates.html`` immediately. It carries no site chrome and is
    deliberately kept out of the sitemap.
    """
    target = f"{BASE_PATH}/updates.html"
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="0;url={target}"><meta name="robots" content="noindex">
<link rel="canonical" href="{html.escape(SITE_ORIGIN + target, quote=True)}"><title>Moved to Updates — Pixi Wiki</title></head><body>
<p>This page has moved to <a href="{target}">Updates</a>.</p>
</body></html>"""
    (output_root / "recent.html").write_text(page, encoding="utf-8", newline="\n")


def write_sitemap(
    output_root: Path,
    doc_entries: list[dict[str, str]],
    updates_paths: list[str],
) -> None:
    """Emit ``sitemap.xml`` with one ``<url>`` per generated HTML page.

    ``doc_entries`` covers every namespace document/README page (each a dict with
    a site-absolute ``path`` and a possibly-empty ``lastmod``). The homepage,
    every paginated Updates page in ``updates_paths``, and the three docs pages
    are added here as undated chrome. The ``recent.html`` redirect stub is
    intentionally excluded, as is ``search.html`` (a ``robots: noindex``
    JS-dependent enhancement surface with no crawlable content of its own).
    Ordering is deterministic: the homepage first, then all other URLs sorted by
    path, so an unchanged corpus rebuilds byte-identically.
    """
    chrome_paths = list(updates_paths) + [
        f"{BASE_PATH}/docs/AGENT_SETUP.html",
        f"{BASE_PATH}/docs/REPLICATE_APPROACH.html",
        f"{BASE_PATH}/docs/SIGNAL_GRAPH.html",
    ]
    rest = list(doc_entries) + [{"path": path, "lastmod": ""} for path in chrome_paths]
    ordered = [{"path": f"{BASE_PATH}/", "lastmod": ""}] + sorted(rest, key=lambda entry: entry["path"])

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for entry in ordered:
        loc = html.escape(SITE_ORIGIN + entry["path"])
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        if entry.get("lastmod"):
            lines.append(f"    <lastmod>{entry['lastmod']}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    (output_root / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_404_page(output_root: Path) -> None:
    """Emit a standard-chrome ``404.html`` for GitHub Pages not-found routing."""
    body = (
        '<article class="article" style="max-width:900px;margin:44px auto 90px;padding:0 20px">'
        '<h1>Page not found</h1>'
        '<p class="hero-copy">This page is missing. Pixi Wiki is regenerated from source Markdown, '
        'so a page you bookmarked may have been renamed, moved, or rebuilt at a new path.</p>'
        '<div class="hero-actions">'
        f'<a class="button-link primary" href="{BASE_PATH}/">Go to the homepage</a>'
        f'<a class="button-link" href="{BASE_PATH}/#wikis">Browse all namespaces</a>'
        '</div>'
        f'<div class="agent-card">🤖 Agents: start from <a href="{BASE_PATH}/llms.txt">/llms.txt</a> '
        'to re-route to the current Markdown pages.</div>'
        '</article>'
    )
    page = f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Page not found — Pixi Wiki</title>{head_meta("Page not found", "The page you requested does not exist in Pixi Wiki. Return to the homepage or browse the namespace list.", BASE_PATH + "/404.html")}{stylesheet_link()}{theme_script()}</head><body>
{site_header(HOME_NAV_LINKS)}
<main>{body}</main>
<footer class="footer"><div class="footer-inner"><p>Plain static HTML. Humans browse it like a wiki; agents read Markdown through <code>llms.txt</code>.</p><p><a href="{BASE_PATH}/llms.txt">/llms.txt</a><a href="{BASE_PATH}/llms-full.txt">/llms-full.txt</a><a href="{BASE_PATH}/index.json">/index.json</a></p></div></footer>
</body></html>"""
    (output_root / "404.html").write_text(page, encoding="utf-8", newline="\n")


def write_search_page(output_root: Path) -> None:
    """Emit the JavaScript-enhanced ``search.html`` results page.

    The page ships an empty ``.search-page`` placeholder that
    ``search_page_script`` fills on DOMContentLoaded with a prominent query
    input, a ranked/highlighted result list, and client-side pagination. Because
    search is a deliberate JS-dependent enhancement surface, the page carries a
    ``robots: noindex`` meta and is intentionally excluded from ``sitemap.xml``
    (see ``write_sitemap``); its ``<noscript>`` block says so and routes agents
    and no-JS readers to the Markdown entrypoints (``llms.txt``/``index.json``)
    for retrieval. Standard chrome (header dropdown search included) still loads.
    """
    body = (
        '<article class="article" style="max-width:900px;margin:44px auto 90px;padding:0 20px">'
        f'<div class="content-header"><div class="breadcrumbs"><a href="{BASE_PATH}/">wikis</a> / Search</div>'
        f'<span class="page-tools"><a class="markdown-link" href="{BASE_PATH}/index.json">index.json</a></span></div>'
        '<h1>Search</h1>'
        '<p class="hero-copy">Search every Pixi Wiki namespace by title, path, category, and namespace. '
        'Results are ranked by relevance and matched terms are highlighted.</p>'
        f'<div class="search-page" data-registry="{BASE_PATH}/index.json"></div>'
        '<noscript>'
        '<p class="hero-copy">Search is a JavaScript enhancement layered over the page registry, so it needs '
        f'JavaScript enabled. Without it, browse the namespaces from the <a href="{BASE_PATH}/">homepage</a>, '
        'or retrieve pages the way agents do: read '
        f'<a href="{BASE_PATH}/llms.txt">llms.txt</a> for the routing map and '
        f'<a href="{BASE_PATH}/index.json">index.json</a> for the full machine-readable index.</p>'
        '</noscript>'
        '</article>'
    )
    page = f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Search — Pixi Wiki</title>{head_meta("Search", SEARCH_DESCRIPTION, BASE_PATH + "/search.html", noindex=True)}{stylesheet_link()}{theme_script()}{search_script()}{search_page_script()}</head><body>
<a class="skip-link" href="#main-content">Skip to content</a>
{site_header(HOME_NAV_LINKS)}
<main id="main-content">{body}</main>
<footer class="footer"><div class="footer-inner"><p>Plain static HTML. Humans browse it like a wiki; agents read Markdown through <code>llms.txt</code>.</p><p><a href="{BASE_PATH}/llms.txt">/llms.txt</a><a href="{BASE_PATH}/llms-full.txt">/llms-full.txt</a><a href="{BASE_PATH}/index.json">/index.json</a></p></div></footer>
</body></html>"""
    (output_root / "search.html").write_text(page, encoding="utf-8", newline="\n")


def build(
    source_dir: Path,
    output_root: Path,
    slugs: list[str],
    base_path: str = DEFAULT_BASE_PATH,
    site_origin: str = DEFAULT_SITE_ORIGIN,
) -> None:
    # Publish the deployment coordinates for this build. They are set
    # deterministically per call (normalized), so repeated builds never leak
    # state and every f-string template reads the active values.
    global BASE_PATH, SITE_ORIGIN, WIKI_NAV_LINKS, HOME_NAV_LINKS
    BASE_PATH = normalize_base_path(base_path)
    SITE_ORIGIN = site_origin.rstrip("/")
    WIKI_NAV_LINKS = _wiki_nav_links(BASE_PATH)
    HOME_NAV_LINKS = _home_nav_links(BASE_PATH)

    if not source_dir.is_dir():
        raise SystemExit(f"Source namespace directory not found: {source_dir}")
    missing = [slug for slug in slugs if not (source_dir / slug).is_dir()]
    if missing:
        raise SystemExit(f"Missing namespace source dirs: {', '.join(missing)}")

    clean_generated_output(output_root)

    # One shared stylesheet for every page. Pages link this file instead of
    # inlining the full CSS, so the byte-identical `site_css()` output lives in a
    # single cacheable resource. The theme-boot script stays inline per page to
    # avoid a flash of the wrong theme.
    (output_root / "site.css").write_text(site_css(), encoding="utf-8", newline="\n")

    global_link_targets = build_global_link_targets(source_dir, slugs)

    wikis: list[dict[str, Any]] = []
    all_full_sections: list[tuple[str, str]] = []
    all_update_entries: list[dict[str, str]] = []
    all_sitemap_docs: list[dict[str, str]] = []
    llms_parts = [
        "# Pixi Wiki Namespace Registry\n\n",
        "> Pixi Wiki turns my notes, project docs, research, and working context into structured, maintained knowledge bases. Humans browse them like a wiki. Agents read them natively as plain Markdown with llms.txt.\n\n",
        "> Raw Markdown: `/raw/<slug>/<path>`. Human HTML: `/wiki/<slug>/<path>.html`. Namespace agents: `/wiki/<slug>/llms.txt`.\n\n",
    ]
    top_links: list[str] = []
    category_groups = [
        {
            "key": "agent-ops",
            "title": "Agent Operations",
            "description": "Hermes, crew workflows, traces, and quality gates for running agents well.",
            "slugs": {"agent-workflows", "hermes-agent", "eval-trace"},
        },
        {
            "key": "knowledge-systems",
            "title": "Knowledge Systems",
            "description": "The wiki/compiler layer, local retrieval, infrastructure, and curated source/data readiness.",
            "slugs": {"pixi-vault", "local-ai-infrastructure", "curated-tuning-datasets"},
        },
        {
            "key": "labs-products",
            "title": "Labs & Product Surfaces",
            "description": "AI-native products, simulations, demos, and experiment-facing project labs.",
            "slugs": {"ai-native-product-surfaces", "rl-sim-labs"},
        },
    ]
    card_by_slug: dict[str, str] = {}

    for slug in slugs:
        wiki_record, links, full_sections, update_entries, sitemap_docs = collect_namespace(source_dir, output_root, slug, global_link_targets)
        wikis.append(wiki_record)
        all_full_sections.extend(full_sections)
        all_update_entries.extend(update_entries)
        all_sitemap_docs.extend(sitemap_docs)
        title = wiki_record["title"]
        llms_parts.append(f"## {title}\n\n")
        llms_parts.append(f"> {wiki_record['description']}\n")
        llms_parts.append(f"> Current as of: {wiki_record['scope']['currentAs']}\n")
        llms_parts.append(f"> Agent access: [/wiki/{slug}/llms.txt](/wiki/{slug}/llms.txt) [/wiki/{slug}/llms-full.txt](/wiki/{slug}/llms-full.txt) [/wiki/{slug}/index.json](/wiki/{slug}/index.json)\n\n")
        for doc_title, _rel, raw_url, html_url in links:
            llms_parts.append(f"- [{doc_title}]({raw_url}) ([html]({html_url}))\n")
        llms_parts.append("\n")
        top_links.append(f'<a href="{BASE_PATH}/wiki/{slug}/README.md.html">{html.escape(str(title))}</a>')
        card_by_slug[slug] = (
            f'<article class="card" id="{slug}"><h2><a href="{BASE_PATH}/wiki/{slug}/README.md.html">{html.escape(str(title))}</a></h2>'
            f'<p>{html.escape(wiki_record["description"])}</p><p class="meta">{wiki_record["documentCount"]} documents · '
            f'{wiki_record["counts"].get("concepts",0)} concepts · {wiki_record["counts"].get("entities",0)} entities · '
            f'<a href="{BASE_PATH}/wiki/{slug}/llms.txt">llms.txt</a></p></article>'
        )

    grouped_sections: list[str] = []
    assigned_slugs = {slug for group in category_groups for slug in group["slugs"]}
    for group in category_groups:
        cards = "".join(card_by_slug[slug] for slug in slugs if slug in group["slugs"] and slug in card_by_slug)
        if not cards:
            continue
        grouped_sections.append(
            f'<section class="wiki-group" id="{group["key"]}"><div class="group-header"><p class="eyebrow">{html.escape(group["title"])}</p>'
            f'<h2>{html.escape(group["title"])}</h2><p>{html.escape(group["description"])}</p></div><div class="grid">{cards}</div></section>'
        )
    overflow_cards = "".join(card_by_slug[slug] for slug in slugs if slug not in assigned_slugs and slug in card_by_slug)
    if overflow_cards:
        grouped_sections.append(
            f'<section class="wiki-group" id="other-wikis"><div class="group-header"><p class="eyebrow">Other Wikis</p>'
            f'<h2>Other Wikis</h2><p>Additional namespaces that do not yet fit one of the main shelves.</p></div><div class="grid">{overflow_cards}</div></section>'
        )
    grouped_index = "".join(grouped_sections)

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
    (output_root / "index.json").write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8", newline="\n")
    (output_root / "llms.txt").write_text("".join(llms_parts).rstrip() + "\n", encoding="utf-8", newline="\n")
    full_body = "\n\n".join(f"<!-- ===== {name} ===== -->\n\n{text}" for name, text in all_full_sections)
    (output_root / "llms-full.txt").write_text(full_body.rstrip() + "\n", encoding="utf-8", newline="\n")
    write_agent_setup_page(output_root)
    write_replicate_page(output_root)
    write_signal_graph_page(output_root)

    update_entries = sort_update_entries(all_update_entries)
    updates_paths = write_updates_page(output_root, update_entries)
    write_recent_redirect(output_root)
    updates_payload = {
        "generated_from": "frontmatter updated fields",
        "count": len(update_entries),
        "entries": update_entries,
    }
    (output_root / "updates.json").write_text(json.dumps(updates_payload, indent=2) + "\n", encoding="utf-8", newline="\n")

    index_html = f"""<!doctype html>
<html lang="en" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pixi Wiki</title>{head_meta("Pixi Wiki", HOME_DESCRIPTION, BASE_PATH + "/")}{stylesheet_link()}{theme_script()}{search_script()}{copy_button_script()}</head><body>
<a class="skip-link" href="#main-content">Skip to content</a>
{site_header(HOME_NAV_LINKS)}
<main id="main-content" style="max-width:1180px;margin:44px auto 90px;padding:0 20px"><h1>Pixi Wiki</h1><p class="hero-copy">Pixi Wiki turns my notes, project docs, research, and working context into structured, maintained knowledge bases. Humans browse them like a wiki. Agents read them natively as plain Markdown with <code>llms.txt</code> and local MCP access.</p><div class="hero-actions"><a class="button-link primary" href="#wikis">Browse wikis</a><a class="button-link" href="{BASE_PATH}/docs/AGENT_SETUP.html">Connect agents via MCP</a><a class="button-link" href="{BASE_PATH}/docs/SIGNAL_GRAPH.html">Signal graph sidecar</a></div><section class="agent-setup-callout"><h2>Agents start here</h2><pre><code>$ curl {SITE_ORIGIN}{BASE_PATH}/llms.txt</code></pre><p>Use <code>llms.txt</code> as the first routing map, then follow links to raw Markdown, namespace files, or MCP setup.</p></section><nav class="wiki-nav" aria-label="Wiki categories"><a class="button-link" href="#agent-ops">Agent Operations</a><a class="button-link" href="#knowledge-systems">Knowledge Systems</a><a class="button-link" href="#labs-products">Labs & Product Surfaces</a></nav><div id="wikis">{grouped_index}</div></main>
<footer class="footer"><div class="footer-inner"><p>Plain static HTML. No JavaScript is required to read any page — agents welcome.</p><p><a href="{BASE_PATH}/llms.txt">/llms.txt</a><a href="{BASE_PATH}/llms-full.txt">/llms-full.txt</a><a href="{BASE_PATH}/index.json">/index.json</a><a href="{BASE_PATH}/docs/SIGNAL_GRAPH.html">Signal Graph</a><a href="https://github.com/pixiiidust/pixi-wiki">GitHub</a><a href="{BASE_PATH}/docs/REPLICATE_APPROACH.html">Copy this approach</a></p></div></footer>
</body></html>"""
    (output_root / "index.html").write_text(index_html, encoding="utf-8", newline="\n")

    write_sitemap(output_root, all_sitemap_docs, updates_paths)
    write_404_page(output_root)
    write_search_page(output_root)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=(
            "Path to your vault's wikis directory. The default is the author's "
            "own vault path; replicators must pass their own."
        ),
    )
    parser.add_argument("--output", type=Path, default=ROOT, help="Path to pixi-wiki output repo")
    parser.add_argument("--slug", action="append", dest="slugs", help="Namespace slug to include; repeatable")
    parser.add_argument(
        "--base-path",
        default=DEFAULT_BASE_PATH,
        help=(
            "Site-root-relative path prefix for the deployed site "
            "(e.g. '/my-wiki' for a project site, '' for a user/org root site)."
        ),
    )
    parser.add_argument(
        "--site-origin",
        default=DEFAULT_SITE_ORIGIN,
        help="Absolute origin (scheme + host) used for canonical/OpenGraph URLs and sitemap locs.",
    )
    args = parser.parse_args()
    build(
        args.source.resolve(),
        args.output.resolve(),
        args.slugs or DEFAULT_SEED_SLUGS,
        base_path=args.base_path,
        site_origin=args.site_origin,
    )


if __name__ == "__main__":
    main()
