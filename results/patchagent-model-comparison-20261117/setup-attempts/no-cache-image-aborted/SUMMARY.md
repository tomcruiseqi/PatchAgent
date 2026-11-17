# PatchAgent model comparison

Generated: 2026-11-17T09:12:08+08:00

Each model was run once per case with temperature 0, one agent, and a 30-iteration cap. Interactions count LangChain chat-model callback starts; provider retries are not separately counted. Candidate attempts count non-empty patches passed to validate, unique counts use per-run SHA-256, and tool calls are invocations recorded in PatchAgent context logs.

| Model | Completed runs | Patches found | Interactions | Candidate attempts | Unique candidates per run | Tool calls | Input tokens | Output tokens | Elapsed (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek-flash-cyber | 0/6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 |
| deepseek-flash | 0/6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 |
| glm-5.3 | 0/6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.00 |

## Per-case results

| Model | Case | Status | Patch | Interactions | Candidates | Tool calls | Input tokens | Output tokens | Elapsed (s) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
