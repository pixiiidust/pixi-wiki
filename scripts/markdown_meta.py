#!/usr/bin/env python3
"""Shared Markdown frontmatter + text-extraction helpers for Pixi Wiki.

Historically three scripts each carried a private, near-identical copy of this
logic and the copies had drifted:

  * ``scripts/build_from_pixi_vault.py`` (the generator),
  * ``scripts/pixi_wiki_mcp.py`` (the read-only MCP server),
  * ``scripts/build_signal_graph.py`` (the analysis sidecar).

The committed published artifacts (631 HTML pages plus the JSON/txt registries)
were produced by the generator, so **the generator's behavior is canonical**.
Where the three copies disagreed, this shared module adopts the generator's
semantics; the MCP server and signal graph now import these functions too.

Reconciliation decisions
------------------------
``parse_frontmatter``:

  * Scalar values strip only double quotes (``value.strip('"')``).
    - Generator: strips ``"`` only.  MCP: stripped both ``"`` and ``'``.
      Signal graph: stripped ``"`` only.  → Generator wins: strip ``"`` only.
  * List items (``  - x`` block items) do NOT strip quotes
    (``line[4:].strip()``).
    - Generator: no quote stripping.  MCP: stripped ``"'``.  Signal graph:
      stripped ``"``.  → Generator wins: no quote stripping on block list items.
  * Inline lists (``key: [a, b]``) strip both ``"`` and ``'`` per element.
    - All three copies agreed here; kept as-is.
  * Key/value split uses ``":" in line`` + ``line.split(":", 1)``.
    - Generator + MCP: split on the first colon.  Signal graph: required the key
      to match ``^[A-Za-z0-9_-]+:``.  → Generator wins: split on first colon, so
      keys containing other characters (and values containing colons, e.g. URLs)
      are handled exactly as the canonical generator handled them.
  * A ``  - `` continuation line only appends when a ``current`` key exists and
    its accumulated value is still a list (matches all three prior copies).

``first_heading``:

  * Identical across the generator and MCP (regex ``^#\\s+(.+)$`` multiline);
    the signal graph had no standalone copy.  Kept verbatim.

``first_paragraph``:

  * Operates on the *body text it is given* (generator semantics).  The MCP copy
    stripped frontmatter internally first; that responsibility now lives at the
    MCP call site, which strips frontmatter before calling this function.
  * Length cutoff uses ``> 260`` (generator).  MCP used ``>= 260``.
    → Generator wins: ``> 260``.
  * Returns ``" ".join(lines)[:300] or "Compiled namespace."`` — the generator's
    default fallback is preserved.  MCP had no fallback; its ``_snippet`` call
    site keeps its own downstream fallback, so behavior there is unaffected in
    practice (the fallback only appears for empty bodies).
"""

from __future__ import annotations

import re
from typing import Any

__all__ = ["parse_frontmatter", "first_heading", "first_paragraph"]


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split leading ``---`` YAML-ish frontmatter from the body.

    Returns ``(frontmatter_dict, body_text)``.  If no well-formed frontmatter
    block is present, returns ``({}, text)``.
    """
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
    """Return the first ``# `` heading text, or ``None`` if there is none."""
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def first_paragraph(text: str) -> str:
    """Return the first prose paragraph of a Markdown *body*.

    Skips fenced code blocks, headings, blockquotes, list items, and rules.
    The caller is responsible for stripping frontmatter first if needed.
    """
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
