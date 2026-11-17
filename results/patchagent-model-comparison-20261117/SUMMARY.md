# PatchAgent model comparison

Generated: 2026-11-17T10:43:11+08:00

Each scored result used temperature 0, one agent, and a 30-iteration cap. Transport or infrastructure errors were archived under attempts/ and retried; failed attempts are excluded from scored totals. Interactions count LangChain chat-model callback starts; provider-internal retries are not separately counted. Candidate attempts count non-empty patches passed to validate, unique counts use per-run SHA-256, and tool calls are invocations recorded in PatchAgent context logs.

| Model | Scored runs | Unscored errors | Patches found | Interactions | Candidate attempts | Unique candidates per run | Tool calls | Input tokens | Output tokens | Elapsed (s) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deepseek-flash-cyber | 6/6 | 0 | 6 | 37 | 6 | 6 | 54 | 447759 | 34631 | 1001.25 |
| deepseek-flash | 6/6 | 0 | 5 | 41 | 10 | 9 | 55 | 414033 | 23204 | 592.71 |
| glm-5.3 | 6/6 | 0 | 5 | 33 | 9 | 7 | 35 | 315528 | 33368 | 1213.07 |

## Per-case results

| Model | Case | Status | Patch | Interactions | Candidates | Tool calls | Input tokens | Output tokens | Elapsed (s) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| deepseek-flash | assimp5763 | patch_not_found | no | 12 | 5 | 14 | 168243 | 6177 | 54.87 |
| deepseek-flash | assimp5764 | patch_found | yes | 4 | 1 | 6 | 57921 | 1237 | 104.55 |
| deepseek-flash | assimp5765 | patch_found | yes | 4 | 1 | 4 | 21027 | 2643 | 257.69 |
| deepseek-flash | yasm241 | patch_found | yes | 5 | 1 | 8 | 23139 | 1741 | 49.62 |
| deepseek-flash | yasm242 | patch_found | yes | 5 | 1 | 8 | 32387 | 4657 | 43.48 |
| deepseek-flash | yasm243 | patch_found | yes | 11 | 1 | 15 | 111316 | 6749 | 82.50 |
| deepseek-flash-cyber | assimp5763 | patch_found | yes | 6 | 1 | 9 | 45039 | 1500 | 102.42 |
| deepseek-flash-cyber | assimp5764 | patch_found | yes | 4 | 1 | 5 | 62653 | 1700 | 190.22 |
| deepseek-flash-cyber | assimp5765 | patch_found | yes | 3 | 1 | 4 | 15138 | 4724 | 409.87 |
| deepseek-flash-cyber | yasm241 | patch_found | yes | 7 | 1 | 12 | 39134 | 1885 | 73.54 |
| deepseek-flash-cyber | yasm242 | patch_found | yes | 12 | 1 | 19 | 259032 | 21868 | 173.48 |
| deepseek-flash-cyber | yasm243 | patch_found | yes | 5 | 1 | 5 | 26763 | 2954 | 51.72 |
| glm-5.3 | assimp5763 | patch_found | yes | 5 | 1 | 5 | 32920 | 652 | 116.33 |
| glm-5.3 | assimp5764 | patch_not_found | no | 12 | 4 | 12 | 207638 | 2536 | 177.78 |
| glm-5.3 | assimp5765 | patch_found | yes | 2 | 1 | 2 | 6054 | 340 | 240.16 |
| glm-5.3 | yasm241 | patch_found | yes | 5 | 1 | 6 | 17245 | 568 | 63.24 |
| glm-5.3 | yasm242 | patch_found | yes | 7 | 1 | 8 | 46112 | 27583 | 554.32 |
| glm-5.3 | yasm243 | patch_found | yes | 2 | 1 | 2 | 5559 | 1689 | 61.24 |
