---
title: Hermes Remote Artifact Previews
created: 2026-06-27
updated: 2026-06-27
type: concept
status: compiled
namespace: hermes-agent
source: Knowledge/concepts/hermes-remote-artifact-previews.md
confidence: high
---

# Hermes Remote Artifact Previews

Hermes remote artifact previews are HTML/MDX/file artifacts generated on a remote Hermes host and opened from a local Hermes Desktop or dashboard session.

## Core rule

Never hand a remote Desktop session a VPS-local `file://` URL such as:

```text
file:///tmp/.../artifact.html
```

Use the dashboard HTTP/API boundary instead:

```text
remote file on VPS -> dashboard HTTP/API -> local Desktop preview
```

For Jamie's VPS setup:

- dashboard origin: `http://100.82.175.2:9119`
- gateway/API port: `8642` remains separate
- artifact links should be verified `http://...` URLs, not `file://...` paths

## Why this matters

A local Electron/Chromium webview cannot read the VPS filesystem. A dashboard page loaded over HTTP also cannot load arbitrary local resources through `file://`; Chromium reports this as `Not allowed to load local resource` or `chromewebdata`.

## Durable implementation pattern

For product behavior, remote HTML artifacts should be read or served through the Hermes dashboard backend:

- read remote HTML through the authenticated dashboard filesystem API and render a safe data/HTTP preview target; or
- serve the artifact through a dashboard/static route and return that HTTP URL.

Temporary `python3 -m http.server` links are acceptable for demos, but they are not durable product infrastructure.

## Agent operating checklist

1. Inspect topology: local Desktop vs remote VPS.
2. Treat `/tmp/...`, `/root/...`, and similar paths as remote-only when the Desktop is local.
3. Do not paste `file://` as the user-facing preview link.
4. Produce a dashboard HTTP/API URL or explicitly start a temporary HTTP endpoint.
5. Verify with `curl -I` that the URL is `200 OK` before saying it works.

## Related pages

- [[concepts/hermes-capability-routing|Hermes Capability Routing]]
- [[concepts/source-priority|Hermes Source Priority]]
- [[../../agent-workflows/wiki/concepts/runtime-memory-knowledge-routing|Runtime Memory Knowledge Routing]]
