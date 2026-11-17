# PatchAgent model comparison

Generated: 2026-11-17T09:10:54+08:00

Each model was run once per case with temperature 0, one agent, and a 30-iteration cap. Interactions count LangChain chat-model callback starts; provider retries are not separately counted. Candidate attempts count non-empty patches passed to validate, unique counts use per-run SHA-256, and tool calls are invocations recorded in PatchAgent context logs.

| Model | Completed runs | Patches found | Interactions | Candidate attempts | Unique candidates per run | Tool calls | Input tokens | Output tokens | Elapsed (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek-flash-cyber | 6/6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7.45 |
| deepseek-flash | 6/6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3.44 |
| glm-5.3 | 6/6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3.42 |

## Per-case results

| Model | Case | Status | Patch | Interactions | Candidates | Tool calls | Input tokens | Output tokens | Elapsed (s) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-flash | assimp5763 | error | no | 0 | 0 | 0 | 0 | 0 | 0.57 |
| deepseek-flash | assimp5764 | error | no | 0 | 0 | 0 | 0 | 0 | 0.58 |
| deepseek-flash | assimp5765 | error | no | 0 | 0 | 0 | 0 | 0 | 0.57 |
| deepseek-flash | yasm241 | error | no | 0 | 0 | 0 | 0 | 0 | 0.57 |
| deepseek-flash | yasm242 | error | no | 0 | 0 | 0 | 0 | 0 | 0.59 |
| deepseek-flash | yasm243 | error | no | 0 | 0 | 0 | 0 | 0 | 0.56 |
| deepseek-flash-cyber | assimp5763 | error | no | 0 | 0 | 0 | 0 | 0 | 1.32 |
| deepseek-flash-cyber | assimp5764 | error | no | 0 | 0 | 0 | 0 | 0 | 1.31 |
| deepseek-flash-cyber | assimp5765 | error | no | 0 | 0 | 0 | 0 | 0 | 1.34 |
| deepseek-flash-cyber | yasm241 | error | no | 0 | 0 | 0 | 0 | 0 | 1.17 |
| deepseek-flash-cyber | yasm242 | error | no | 0 | 0 | 0 | 0 | 0 | 1.16 |
| deepseek-flash-cyber | yasm243 | error | no | 0 | 0 | 0 | 0 | 0 | 1.15 |
| glm-5.3 | assimp5763 | error | no | 0 | 0 | 0 | 0 | 0 | 0.57 |
| glm-5.3 | assimp5764 | error | no | 0 | 0 | 0 | 0 | 0 | 0.56 |
| glm-5.3 | assimp5765 | error | no | 0 | 0 | 0 | 0 | 0 | 0.57 |
| glm-5.3 | yasm241 | error | no | 0 | 0 | 0 | 0 | 0 | 0.57 |
| glm-5.3 | yasm242 | error | no | 0 | 0 | 0 | 0 | 0 | 0.58 |
| glm-5.3 | yasm243 | error | no | 0 | 0 | 0 | 0 | 0 | 0.57 |
