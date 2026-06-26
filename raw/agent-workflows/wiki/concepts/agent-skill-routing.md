---
title: Agent Skill Routing
created: 2026-06-23
updated: 2026-06-26
type: concept
status: compiled
namespace: agent-workflows
source: Knowledge/concepts/agent-skill-routing.md
confidence: high
---

# Agent Skill Routing

Agent skill routing is the operating contract that Jamie states the desired outcome while Pixoid chooses the useful skill stack, loads those skills, and carries active skill constraints into any delegated subagent context.

## Why this exists

Tools already work this way: Jamie does not need to say `read_file` or `web_search`; Pixoid selects the tool that fits the job. Skills need the same user-facing behavior, but with one extra step: the parent agent must load the skill contents before relying on them.

## Runtime rule

1. Classify the user intent.
2. Load the smallest useful skill stack with `skill_view`.
3. Execute the task through the loaded procedures.
4. If delegating, add an `Active skill constraints` block to the `delegate_task` context.
5. Verify that the subagent followed the constraints before presenting the result.

## Default skill stacks

| Intent | Primary skill | Common supports |
|---|---|---|
| Delegated research, writing, product strategy, portfolio, or project analysis | `pixi-wiki-first-research` | `business-model-research`, `public-signal-monitoring`, `verb-first` |
| PM portfolio or product case study | `portfolio-build-readiness-review` | `product-case-study`, `verb-first`, `pixi-wiki-first-research` |
| Product positioning or copy | `verb-first` | `find-lock`, `ai-native-framing` |
| Creative inspiration, brainstorming, project ideas, or option generation | `creative-ideation` | `find-lock`, `verb-first`, `ai-native-framing` after an idea is selected |
| PRD or implementation plan needs an inspectable review surface | `visual-plan` | `plan`, `prototype`, `obsidian` when the artifact should be source-controlled |
| Build or implementation slice | `implement` | `test-driven-development`, `ponytail-code-discipline`, `github-operations` |
| Debugging | `debugging` | project-specific skill, `codebase-inspection` |
| PR or diff review | `code-review` | `ponytail-code-discipline`, `github-operations` |
| Vault or source-of-truth update | `obsidian` | `pixi-wiki-first-research` when public/wiki context matters |
| Fresh-session continuity | `handoff` | `obsidian` if a durable note is needed |
| Hermes setup/config/troubleshooting | `hermes-agent` | `hermes-cron-operations`, `hermes-gateway-ops`, `native-mcp` |

## Delegation constraint block

Loaded parent skills do not automatically bind isolated subagents. Delegated tasks that rely on skills should include:

```text
Active skill constraints:
- Skills selected by Pixoid: <skill names>.
- Apply these rules before final output: <short constraints>.
- Report which constraints you followed and what source/tool evidence supports the result.
- If a required source/tool is unavailable, say so directly instead of producing generic output.
```

For delegated research, writing, strategy, portfolio, or project analysis, the Pixi Wiki rule is mandatory by default:

```text
Before producing the final answer, use Pixi Wiki MCP first: list available KBs, search for the task topic, read relevant documents, and tailor the answer to Jamie/project context. Generic output without Pixi Wiki retrieval is incomplete. Report which KBs/docs you used and where public web research differs from Pixi Wiki context.
```

## Boundaries

- Use the smallest useful stack; do not load every adjacent skill.
- Skills do not override current user intent, live repo state, GitHub issues, PRDs, safety rules, or verification evidence.
- Subagent output that does not report required retrieval, evidence, or skill constraints is incomplete.
- Durable lessons still route by layer: facts to memory, concepts to Knowledge/Pixi Wiki, project state to Obsidian/GitHub, procedures to skills.

## Edge cases

- Explicit user-invoked skills or slash commands are the chosen mode unless they conflict with safety or live evidence.
- Ask only when different skill stacks imply materially different artifacts or side effects.
- If a skill might matter but its description is unclear, load it before relying on it or excluding it.
- If required MCP/tool/source access is unavailable, report that directly or use a grounded fallback; do not produce generic output as if the constraint was satisfied.
- For open-ended inspiration or option generation, load `creative-ideation`, route through one method, and produce grounded non-generic ideas before returning to product/build gates.
- For PRD/implementation-plan review surfaces, load `visual-plan` and default to local/private MDX artifacts; hosted Plan auth, share links, and comments are optional, not prerequisites.
- Updating vault/Pixi Wiki source can preserve durable knowledge; pushing public `pixi-wiki` deploys still needs explicit approval.
- If skill routing would overload context, stop and hand off rather than carrying a bloated stack forward.

## Source

Canonical source: `Knowledge/concepts/agent-skill-routing.md`.

Reusable Hermes skill: `~/.hermes/skills/productivity/jamie-skill-router/SKILL.md`.

Related skill: `~/.hermes/skills/research/pixi-wiki-first-research/SKILL.md`.

Creative support skill: `~/.hermes/skills/creative/creative-ideation/SKILL.md`.

Visual review support skill: `~/.hermes/skills/visual-plan/SKILL.md`.
