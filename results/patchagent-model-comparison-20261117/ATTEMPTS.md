# Preserved non-scoring attempts

- The first setup attempt failed all 18 jobs before any model request because `/usr/bin/env python` resolved to Python 2.7. Logs are included under `setup-attempts/python2-setup-failed/`.
- A second setup attempt started an unnecessary no-cache yasm image rebuild and was stopped before any model request. Logs are included under `setup-attempts/no-cache-image-aborted/`.
- DeepSeek Flash Cyber yasm243 initially hit `LibclangError` after 7 requests. It passed after loading bundled libclang after PatchAgent imports.
- DeepSeek Flash Cyber Assimp 5763-5765 first hit compiler compatibility errors, then historical fuzzer-source mismatches. The final harness adjustment is recorded under `setup-assimp-compat.patch`; no Assimp source tree was changed.
- DeepSeek Flash Cyber Assimp 5763 had one later `LibclangError` attempt after 4 requests. It passed after correcting the libclang override order.
- DeepSeek Flash yasm241 had a partial setup attempt interrupted before an LLM request.
- GLM-5.3 yasm242 first attempt ended with `RemoteProtocolError` after 783.07 seconds; its retry produced a validated patch.
- GLM-5.3 yasm243 first attempt ended with `RemoteProtocolError` after 29.87 seconds; its retry produced a validated patch.

These records are retained for audit and are excluded from scoring. The final per-case result is the successful retry where one exists.
