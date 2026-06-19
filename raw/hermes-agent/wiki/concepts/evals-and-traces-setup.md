---
title: Hermes Evals and Traces Setup
created: 2026-06-18
updated: 2026-06-18
type: concept
status: compiled
namespace: hermes-agent
tags: [hermes-agent, evals, traces, observability, langfuse, nemo-relay, trajectories]
sources:
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/batch-processing
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins
  - /usr/local/lib/hermes-agent/website/docs/developer-guide/trajectory-format.md
  - /usr/local/lib/hermes-agent/plugins/observability/nemo_relay/README.md
confidence: high
---

# Hermes Evals and Traces Setup

Hermes has native trace surfaces and trajectory capture, but it does not ship a full generic pass/fail eval dashboard. Use the right layer for the job.

## Native trace layers

| Layer | Use | Setup |
|---|---|---|
| `state.db` sessions | Review real conversations, tool calls, usage, cost, and platform history. | Built in. Use `hermes sessions ...`. |
| Session JSONL export | Build eval datasets or review failure traces outside Hermes. | `hermes sessions export ...`. |
| `/insights` | Usage analytics: models, tools, skills, tokens, cost, platforms, top sessions. | Built in. Use `hermes insights --days N`. |
| Trajectory saving | ShareGPT-compatible turn/tool traces from CLI sessions. | `agent.save_trajectories: true` or `--save-trajectories`. |
| Batch runner | Run many prompts and collect structured trajectories/statistics. | `python batch_runner.py ...`. |
| Langfuse plugin | External LLM observability dashboard for turns, LLM calls, and tool calls. | Enable `observability/langfuse` and set keys. |
| NeMo Relay plugin | ATOF/ATIF exports for replay, evaluation, and harness analysis. | Enable `observability/nemo_relay` and set export env vars. |

## Session export

```bash
hermes sessions export sessions.jsonl
hermes sessions export --source discord discord.jsonl
hermes sessions export --session-id <session_id> one-session.jsonl
```

Use this for failure review, dataset building, replay-style analysis, and tool-use trace mining.

## Insights

```bash
hermes insights --days 30
hermes insights --days 7 --source cli
```

Use this for operational analytics, not task correctness scoring.

## Trajectory saving

Official developer docs describe ShareGPT-compatible JSONL trajectories written as:

```text
trajectory_samples.jsonl      # completed=True
failed_trajectories.jsonl     # failed or interrupted
```

Enable in config:

```yaml
agent:
  save_trajectories: true
```

or run with:

```bash
hermes chat --save-trajectories -q "..."
```

The batch runner always saves trajectories.

## Batch eval runner

Official batch-processing docs describe `batch_runner.py` as the native path for running many prompts and producing trajectory data plus statistics.

```bash
python batch_runner.py   --dataset_file=data/eval_suite.jsonl   --batch_size=10   --run_name=eval_gpt55   --model=gpt-5.5   --num_workers=4   --max_turns=10
```

Outputs:

```text
data/<run_name>/
├── trajectories.jsonl
├── batch_0.jsonl
├── checkpoint.json
└── statistics.json
```

Tracked fields include `completed`, `partial`, `api_calls`, `toolsets_used`, `tool_stats`, and `tool_error_counts`.

## Langfuse setup

Official built-in plugin docs say the Langfuse plugin traces Hermes turns, LLM calls, and tool invocations.

Interactive setup:

```bash
hermes tools          # choose Langfuse Observability
```

Manual setup:

```bash
pip install langfuse
hermes plugins enable observability/langfuse
```

Add credentials to `~/.hermes/.env`:

```bash
HERMES_LANGFUSE_PUBLIC_KEY=pk-lf-...
HERMES_LANGFUSE_SECRET_KEY=sk-lf-...
HERMES_LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

Verify:

```bash
hermes plugins list
hermes chat -q "hello"
```

Then check Langfuse for a `Hermes turn` trace.

## NeMo Relay ATOF/ATIF setup

The NeMo Relay plugin maps Hermes observer hooks to scopes, LLM spans, tool spans, marks, ATOF, and ATIF. It can export raw lifecycle events as ATOF JSONL and ATIF trajectory files for replay/eval harnesses.

Enable plugin:

```bash
hermes plugins enable observability/nemo_relay
```

Install runtime if needed:

```bash
pip install "nemo-relay==0.3"
```

Local export settings:

```bash
export HERMES_NEMO_RELAY_ATOF_ENABLED=1
export HERMES_NEMO_RELAY_ATOF_OUTPUT_DIRECTORY=.nemo-relay/atof
export HERMES_NEMO_RELAY_ATIF_ENABLED=1
export HERMES_NEMO_RELAY_ATIF_OUTPUT_DIRECTORY=.nemo-relay/atif
```

Optional controls include `HERMES_NEMO_RELAY_ATOF_FILENAME`, `HERMES_NEMO_RELAY_ATOF_MODE`, `HERMES_NEMO_RELAY_ATIF_FILENAME_TEMPLATE`, `HERMES_NEMO_RELAY_ATIF_AGENT_NAME`, `HERMES_NEMO_RELAY_ATIF_AGENT_VERSION`, `HERMES_NEMO_RELAY_ATIF_MODEL_NAME`, and `HERMES_NEMO_RELAY_ATIF_SUBAGENT_EXPORT_MODE`.

## Decision rule

Use the lightest trace surface that answers the question:

```text
Need to inspect one past run?       → sessions export / session_search
Need usage trends?                  → insights
Need many-prompt eval trajectories? → batch_runner.py
Need external observability UI?     → Langfuse
Need replay/harness trajectory form?→ NeMo Relay ATIF/ATOF
```
