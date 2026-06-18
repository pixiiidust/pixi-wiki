# Pixi Wiki MCP Server

Pixi Wiki includes a local, read-only MCP server for agent access to the same Markdown knowledge bases used by the web UI.

**Deployment status:** the web wiki and this guide are published on GitHub Pages. The MCP server itself is not hosted; it runs locally through stdio on the same machine as your MCP client. To share it, share this repo and have users clone it, install the MCP SDK, and configure their client to launch `scripts/pixi_wiki_mcp.py`.

The server is intentionally boring:

- local stdio MCP transport;
- reads `index.json` plus `raw/<kb>/**/*.md` from this repository;
- exposes list, read, summary, and search tools;
- has no write, edit, or delete tools;
- returns structured errors for missing KBs, missing documents, empty queries, and invalid document IDs.

## Prerequisites

- Python 3.11+ recommended.
- `pytest` for verification.
- `mcp` Python package for running as an MCP server.

Install the MCP SDK if it is not already available:

```bash
python3 -m pip install mcp
```

## KB files

Pixi Wiki is generated from curated Pixi Vault namespaces.

Authoring source:

```text
/root/ObsidianVault/wikis/<namespace>/
```

Generated public Markdown mirror used by the web UI and MCP server:

```text
/root/pixi-wiki/raw/<namespace>/**/*.md
```

Machine registry used by the MCP server:

```text
/root/pixi-wiki/index.json
```

Rendered web pages live under:

```text
/root/pixi-wiki/wiki/<namespace>/**/*.html
```

## Run the web app locally

Pixi Wiki is a static site. Serve the repository root from wherever you cloned it:

```bash
cd /path/to/pixi-wiki
python3 -m http.server 8000
```

Jamie’s VPS path is:

```bash
cd /root/pixi-wiki
python3 -m http.server 8000
```

Open:

```text
http://localhost:8000/
```

## Run the MCP server locally

From a fresh clone:

```bash
git clone https://github.com/pixiiidust/pixi-wiki.git
cd pixi-wiki
python3 -m pip install mcp
python3 scripts/pixi_wiki_mcp.py --self-test
```

Then run the stdio MCP server from the repo root:

```bash
cd /path/to/pixi-wiki
python3 scripts/pixi_wiki_mcp.py
```

Jamie’s VPS path is:

```bash
cd /root/pixi-wiki
python3 scripts/pixi_wiki_mcp.py
```

The command runs a stdio MCP server. It is meant to be launched by an MCP client, not visited in a browser.

Optional self-test without starting MCP stdio:

```bash
python3 scripts/pixi_wiki_mcp.py --self-test
```

## Hermes MCP config example

Add this to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  pixi_wiki:
    command: "python3"
    args: ["/root/pixi-wiki/scripts/pixi_wiki_mcp.py"]
```

Restart Hermes after editing the config. Hermes will expose tools with the `mcp_pixi_wiki_` prefix, for example:

```text
mcp_pixi_wiki_list_kbs
mcp_pixi_wiki_search_all_kbs
mcp_pixi_wiki_read_document
```

## Tools

### `list_kbs`

Returns all registered KBs and metadata from `index.json`.

Example response shape:

```json
{
  "name": "Pixi Wiki",
  "schema_version": "pixi-agentwikis-registry-v1",
  "kb_count": 7,
  "kbs": [
    {
      "kb_id": "pixi-vault",
      "title": "Pixi Vault",
      "description": "...",
      "document_count": 7,
      "raw_base": "/raw/pixi-vault/"
    }
  ]
}
```

### `list_documents`

Input:

```json
{"kb_id": "pixi-vault"}
```

Returns stable document IDs for a KB. Document IDs are relative Markdown paths such as:

```text
README.md
wiki/index.md
wiki/concepts/wiki-compiler-map-and-source-classes.md
```

### `read_document`

Input:

```json
{"kb_id": "pixi-vault", "document_id": "README.md"}
```

Returns Markdown content plus metadata:

```json
{
  "kb_id": "pixi-vault",
  "document_id": "README.md",
  "title": "Pixi Vault",
  "raw": "/raw/pixi-vault/README.md",
  "html": "/wiki/pixi-vault/README.md.html",
  "last_modified": "...",
  "frontmatter": {},
  "content": "# Pixi Vault\n..."
}
```

### `search_kb`

Input:

```json
{"kb_id": "agent-workflows", "query": "Ponytail", "max_results": 5}
```

Returns scored document hits with snippets. Agents should call `read_document` for full content.

### `search_all_kbs`

Input:

```json
{"query": "Pixi Wiki", "max_results": 10}
```

Searches all registered KBs and returns snippets.

### `get_kb_summary`

Input:

```json
{"kb_id": "pixi-vault"}
```

Returns registry metadata plus the KB `README.md` content when present.

## Error behavior

Missing KB:

```json
{
  "error": "KB_NOT_FOUND",
  "message": "No KB found with id 'foo'. Available KBs: ..."
}
```

Missing document:

```json
{
  "error": "DOCUMENT_NOT_FOUND",
  "message": "No document 'missing.md' exists in KB 'pixi-vault'. Use list_documents to see available documents."
}
```

Invalid document ID:

```json
{
  "error": "INVALID_DOCUMENT_ID",
  "message": "Document id may not contain path traversal segments."
}
```

Empty search query:

```json
{
  "error": "EMPTY_QUERY",
  "message": "Search query must not be empty."
}
```

## How to add a new KB

1. Add or update the canonical namespace in Pixi Vault:

   ```text
   /root/ObsidianVault/wikis/<namespace>/
   ```

2. Include at least:

   ```text
   README.md
   wiki/index.md
   ```

3. Rebuild the generated public mirror:

   ```bash
   cd /root/pixi-wiki
   python3 scripts/build_from_pixi_vault.py --source /root/ObsidianVault/wikis --output /root/pixi-wiki
   ```

4. Verify:

   ```bash
   pytest -q
   python3 scripts/pixi_wiki_mcp.py --self-test
   ```

The new KB should appear in `index.json`, the web UI, and `list_kbs`.

## How to add or edit Markdown documents

Edit the canonical source under:

```text
/root/ObsidianVault/wikis/<namespace>/
```

Then rebuild into this generated repo with:

```bash
cd /root/pixi-wiki
python3 scripts/build_from_pixi_vault.py --source /root/ObsidianVault/wikis --output /root/pixi-wiki
```

Do not hand-edit generated files under `raw/` or `wiki/` unless you are making a temporary local test. Rebuilds replace generated output.

## Assumptions

- `index.json` is the registry of available KBs and documents.
- `raw/<namespace>/**/*.md` is the generated Markdown mirror read by agents.
- The web UI and MCP server should agree because both rely on the same generated registry/files.
- V1 is read-only: no write, edit, delete, sync, auth, remote hosting, embeddings, or vector search.
